# Repository agent guidance

- Inspect repository contents before proposing or applying changes.
- Keep changes focused, reversible, and documented.
- Do not invent project behavior, URLs, credentials, or test results.
- Run `python -m unittest discover -s tests -v` for README updater changes.
- Never overwrite content outside the updater's explicit managed markers.
- Use a feature branch and pull request; do not merge unless required checks pass and repository policy permits it.
