# gh.io

Repository for the Qubuhub organization’s web presence and documentation assets.

## Repository layout

- `.github/profile/README.md` — organization profile shown by GitHub.
- `scripts/update_readme.py` — safe updater for explicitly marked generated sections.
- `tests/` — standard-library unit tests for README update behavior.
- `packages/rsc/` — package-specific documentation.
- `docs/` — maintenance notes and audit findings.
- `index.html` — retained site template; see the maintenance notes before changing its rendering pipeline.

## Local validation

Requires Python 3.10 or later. No third-party packages are needed.

```sh
python -m unittest discover -s tests -v
```

To refresh the profile timestamp:

```sh
python scripts/update_readme.py
```

To include recent blog posts, configure the repository variable `BLOG_FEED_URL` with a valid HTTPS RSS or Atom feed URL. If it is unset, the script does not make a network request or overwrite the blog section.

## Safety and maintenance

The updater only edits content enclosed by its own HTML comment markers. It rejects malformed markers and non-HTTPS feed URLs, caps feed responses at 2 MB, uses a request timeout, and writes updates atomically. Review changes before merging; scheduled automation should never be treated as a substitute for code review.
