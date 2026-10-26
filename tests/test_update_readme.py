import tempfile
import unittest
from pathlib import Path

from scripts.update_readme import (
    BLOG_END,
    BLOG_START,
    UPDATED_END,
    UPDATED_START,
    _replace_managed_section,
    fetch_recent_posts,
    render_posts,
)


class ManagedSectionTests(unittest.TestCase):
    def test_appends_section_without_changing_existing_text(self):
        original = "# Profile\n\nKeep this text.\n"
        updated = _replace_managed_section(original, BLOG_START, BLOG_END, "Generated")
        self.assertIn("Keep this text.", updated)
        self.assertIn("Generated", updated)
        self.assertTrue(updated.endswith(BLOG_END + "\n"))

    def test_replaces_only_marked_section(self):
        original = f"before\n{BLOG_START}\nold\n{BLOG_END}\nafter\n"
        updated = _replace_managed_section(original, BLOG_START, BLOG_END, "new")
        self.assertIn("before\n", updated)
        self.assertIn("\nafter\n", updated)
        self.assertNotIn("old", updated)
        self.assertIn("new", updated)

    def test_rejects_unbalanced_or_duplicate_markers(self):
        with self.assertRaises(ValueError):
            _replace_managed_section(f"{BLOG_START}\nonly start", BLOG_START, BLOG_END, "new")
        with self.assertRaises(ValueError):
            _replace_managed_section(
                f"{BLOG_START}\na\n{BLOG_END}\n{BLOG_START}\nb\n{BLOG_END}",
                BLOG_START, BLOG_END, "new"
            )

    def test_rejects_non_https_feed(self):
        with self.assertRaises(ValueError):
            fetch_recent_posts("http://example.com/feed.xml")

    def test_render_posts_escapes_markdown_label_breakouts(self):
        rendered = render_posts([{
            "title": "hello] (https://evil.example)\n[",
            "link": "https://example.com/post",
            "published": "today\nextra",
        }])
        self.assertIn("https://example.com/post", rendered)
        self.assertNotIn("\n[", rendered)


if __name__ == "__main__":
    unittest.main()
