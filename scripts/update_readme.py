#!/usr/bin/env python3
"""Safely update generated sections in the repository's GitHub profile README.

The script uses only the Python standard library. Set BLOG_FEED_URL to an RSS
or Atom feed URL to refresh recent posts. Without a feed URL, only the timestamp
section is refreshed; no network request is made.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_README = ROOT / ".github" / "profile" / "README.md"
MAX_FEED_BYTES = 2_000_000
TIMEOUT_SECONDS = 10
BLOG_START = "<!-- BLOG-POSTS:START -->"
BLOG_END = "<!-- BLOG-POSTS:END -->"
UPDATED_START = "<!-- LAST-UPDATED:START -->"
UPDATED_END = "<!-- LAST-UPDATED:END -->"


def _valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _text(element: ET.Element, names: Iterable[str]) -> str:
    for child in element.iter():
        local = child.tag.rsplit("}", 1)[-1]
        if local in names and child.text and child.text.strip():
            return child.text.strip()
    return ""


def fetch_recent_posts(feed_url: str, max_posts: int = 5) -> list[dict[str, str]]:
    """Fetch and parse RSS 2.0 or Atom entries, rejecting unsafe feed URLs."""
    if not _valid_https_url(feed_url):
        raise ValueError("BLOG_FEED_URL must be a valid HTTPS URL")
    if not 1 <= max_posts <= 20:
        raise ValueError("max_posts must be between 1 and 20")

    request = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "gh.io-readme-updater/1.0", "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        payload = response.read(MAX_FEED_BYTES + 1)
    if len(payload) > MAX_FEED_BYTES:
        raise ValueError("Feed response exceeded the 2 MB safety limit")

    root = ET.fromstring(payload)
    entries = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] in {"item", "entry"}]
    posts: list[dict[str, str]] = []
    for entry in entries[:max_posts]:
        title = _text(entry, {"title"}) or "Untitled"
        published = _text(entry, {"pubDate", "published", "updated", "date"}) or "Date unavailable"
        link = ""
        for child in entry:
            if child.tag.rsplit("}", 1)[-1] == "link":
                href = child.attrib.get("href", "").strip()
                candidate = href or (child.text or "").strip()
                if _valid_https_url(candidate):
                    link = candidate
                    break
        if not link:
            continue
        posts.append({"title": title, "link": link, "published": published})
    return posts


def _replace_managed_section(content: str, start: str, end: str, replacement: str) -> str:
    """Replace exactly one marked section, or append one if markers are absent."""
    starts, ends = content.count(start), content.count(end)
    if starts != ends or starts > 1:
        raise ValueError(f"Invalid or duplicate markers: {start} / {end}")
    block = f"{start}\n{replacement.rstrip()}\n{end}"
    if starts == 1:
        start_at = content.index(start)
        end_at = content.index(end, start_at) + len(end)
        return content[:start_at] + block + content[end_at:]
    separator = "" if not content or content.endswith("\n\n") else ("\n" if content.endswith("\n") else "\n\n")
    return content + separator + block + "\n"


def render_posts(posts: list[dict[str, str]]) -> str:
    if not posts:
        return "_No recent posts were found in the configured feed._"
    lines = []
    for post in posts:
        # Markdown link labels cannot safely contain unescaped brackets/newlines.
        title = re.sub(r"[\r\n\[\]]", " ", post["title"]).strip() or "Untitled"
        date = re.sub(r"[\r\n]", " ", post["published"]).strip()
        lines.append(f"- [{title}]({post['link']})" + (f" — {date}" if date else ""))
    return "\n".join(lines)


def update_readme(readme_path: Path = DEFAULT_README, feed_url: str | None = None) -> None:
    readme_path = readme_path.resolve()
    if not readme_path.is_file():
        raise FileNotFoundError(f"README not found: {readme_path}")
    content = readme_path.read_text(encoding="utf-8")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = _replace_managed_section(content, UPDATED_START, UPDATED_END, f"Last updated: {now}")

    configured_feed = (feed_url or os.environ.get("BLOG_FEED_URL", "")).strip()
    if configured_feed:
        posts = fetch_recent_posts(configured_feed, int(os.environ.get("BLOG_MAX_POSTS", "5")))
        content = _replace_managed_section(content, BLOG_START, BLOG_END, render_posts(posts))

    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=readme_path.parent, delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name
    os.replace(temp_name, readme_path)


def main() -> int:
    try:
        update_readme()
    except (OSError, ValueError, ET.ParseError, urllib.error.URLError) as exc:
        print(f"README update failed: {exc}", file=sys.stderr)
        return 1
    print(f"Updated {DEFAULT_README.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
