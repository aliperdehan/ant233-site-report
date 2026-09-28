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

## Research and checking assistance (Claude, Cowork)

A separate Claude session (Cowork) was used on 28 September 2026 to:

- read the course syllabus, site report rubric and AI policy, and list the
  assignment requirements;
- suggest and verify candidate sources (bibliographic details, DOIs, and that
  the PDFs I obtained were the correct, complete papers);
- check the finished draft mechanically: per-entry word counts, a broken
  citation key, rendering/formatting problems (quote font, margins, header,
  title capitalisation in `references.bib`), and factual accuracy of my
  statements against the source PDFs. Where it found a factual error, it
  pointed to what the paper actually says; the corrections were written by me;
- make small tooling edits: a fix to `fullcite.lua` (render inline-code
  quotes as quotation marks), the course/instructor header in the front
  matter, and one unbalanced brace in `references.bib`.

It did not write, paraphrase, proofread or grammar-check any annotation text.

## Grammar checking (Grammarly)

Grammarly was run once over the finished annotations on 28 September 2026,
as the course AI policy permits for grammar checking.

- **Pre-Grammarly draft:** commit `9e2b993` (22:59). **After Grammarly:**
  commit `7dc9538` (23:11). `git diff 9e2b993 7dc9538` shows every change.
- **Prompts:** none. No generative features (GrammarlyGO, rewrite or
  "improve" prompts) were used; I only accepted or rejected Grammarly's
  inline suggestions.
- **Accepted changes** (wording only, no change to content or claims):
  - Russell: "conducted a microscopic inspection of a total of" to
    "microscopically inspected"; removed "found" from "oldest found".
  - Radovčić summary: "This is the largest…, and challenges…" to "As the
    largest…, it challenges…"; "demonstrating that" to "showing";
    "well ahead of modern human appearance" to "well before modern humans
    appeared".
  - Radovčić evaluation: "Methodology is" to "Methodology includes";
    "Even though the sample size is small," to "Despite the small sample
    size,".
  - Carbonell: "of which 165 are of" to "165 belonging to".
  - Saladié: "a large corpus of literature" to "a broad literature corpus".
