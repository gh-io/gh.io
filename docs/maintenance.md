# Repository maintenance and audit

## Verified issues addressed by this repair

- The profile README is stored at `.github/profile/README.md`, while both legacy update scripts pointed to `profile/README.md`.
- The profile README contained reStructuredText/Docutils material, malformed `tittle` metadata, and relative links not verified in this repository.
- The RSS updater used a placeholder feed URL, assumed a target directory, and replaced content beyond the generated section in some cases.
- The file named `bash` contained a mixture of MSBuild, Mono, and Azure Pipelines commands rather than a runnable Bash script.
- `index.html` is a Jinja/Sphinx-style template, not a self-contained static HTML document. It is retained until the intended publishing pipeline is confirmed.

## Target structure

```text
gh.io/
├── .codex/AGENT.md
├── .github/
│   ├── profile/README.md
│   └── workflows/validate-and-update.yml
├── docs/maintenance.md
├── packages/rsc/README.md
├── scripts/update_readme.py
├── tests/test_update_readme.py
├── index.html
├── README.md
└── pyproject.toml (optional; add only if packaging or tooling needs it)
```

## Updater behavior

- Paths are anchored to the repository root, not the current working directory.
- Blog updates are opt-in through `BLOG_FEED_URL`; the URL must use HTTPS.
- Feed responses are time-limited and capped at 2 MB.
- Only the `BLOG-POSTS` and `LAST-UPDATED` marker blocks are managed.
- Malformed or duplicate markers fail instead of risking unrelated README content.
- Writes are atomic, and tests use Python's standard library.

## Follow-up items requiring owner confirmation

- Confirm whether `index.html` is intended for a Sphinx/Jinja build or GitHub Pages static hosting before changing it.
- Review unusually named documentation files and placeholders individually before deleting them; their purpose cannot be established from filenames alone.
- Configure `BLOG_FEED_URL` only after the canonical feed URL is known.
- Confirm whether the legacy root file `bash` is used by an external build before removing or relocating it.
