# AI Use Acknowledgement

Tool: Claude Code, running Claude Sonnet 5 (Anthropic).

This documents what AI assistance was used for in this repository. The
written content of the annotated bibliography and site report (source
summaries, evaluations, analysis, argument) is my own work.

## What Claude was used for

- Setting up this repository: `git init`, initial `.gitignore`, and creating
  a private GitHub remote (`aliperdehan/ant233-site-report`) for revision
  history with server-verified timestamps.
- Scaffolding project structure and documentation: `README.md`, the
  annotated bibliography template (`bib/annotated-bibliography.md`), and
  this file.
- Configuring citation tooling: installing an APA CSL style into pandoc's
  user data directory, setting up `bib/references.bib` as a citation data
  source, and writing `bib/fullcite.lua`, a pandoc Lua filter that inlines
  a single source's full formatted reference at a chosen point in the
  document (rather than only citeproc's default combined bibliography).
- Git/GitHub instruction: walking through `git add` / `commit` / `push`
  usage and commit message conventions.

## What Claude was not used for

- Bibliographic data entry (`bib/references.bib` entries) — entered by hand.
- Source summaries, evaluations, and analysis in the annotated bibliography.
- Any site report writing.

## Verification

Full incremental history, including this acknowledgement, is visible at
https://github.com/aliperdehan/ant233-site-report/commits/main
