# ANT233 — Site Report Project

Working repo for the annotated bibliography and site report, version-controlled
as a Google-Docs-style revision history (per instructor's request to write
against AI-detection false positives).

## Why git instead of Google Docs

The commit history is the evidence: many small commits over time, each with a
real diff, show the writing was built up incrementally by a person rather than
pasted in all at once. A private GitHub remote adds server-side push
timestamps, which are harder to fabricate than local commit timestamps.

## Workflow

- Commit often — after each paragraph or source entry, not just at the end
  of a session. A handful of large commits looks the same as a single paste.
- Write real commit messages describing what changed (`add annotation for
  Radovčić 2015`, not `update`).
- Don't squash or rebase history before submitting — the granular log is the
  point.
- Push to GitHub regularly so timestamps are server-verified, not just local.

## Layout

- `bib/annotated-bibliography.md` — annotated bibliography (one entry per source)
- `info/` — course handouts (not tracked in git, see `.gitignore`)
- `sources/` — source PDFs (not tracked in git, see `.gitignore`)
- `report/` — site report (added later)

## If your professor wants to see the history

`git log --stat` or the GitHub commit view shows every incremental change with
timestamps.
