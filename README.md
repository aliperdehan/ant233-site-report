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

## Command cheat sheet

Typical session:

```bash
git status                       # see what you've changed
git add bib/annotated-bibliography.md   # stage a specific file
git commit -m "add annotation for Rink 1995"   # save a snapshot with a message
git push                         # send committed snapshots to GitHub
```

Other useful commands:

```bash
git log --oneline    # see commit history, one line each
git diff              # see unstaged changes line-by-line
git diff --staged     # see staged changes before committing
```

Commit message style: present tense, describe what changed
(`"add annotation for Trinkaus 1984"`, not `"update"` or `"wip"`).

## Layout

- `bib/annotated-bibliography.md` — annotated bibliography (one entry per source)
- `info/` — course handouts (not tracked in git, see `.gitignore`)
- `sources/` — source PDFs (not tracked in git, see `.gitignore`)
- `report/` — site report (added later)

## If your professor wants to see the history

`git log --stat` or the GitHub commit view shows every incremental change with
timestamps.
