# ANT 233 — Site Report Project

Annotated bibliography (and, later, site report) for ANT 233: Stone Age
Archaeology of Eurasia, Prof. Reed Coil, Nazarbayev University. Topic:
cannibalism and mortuary practice at Krapina.

## Why this is a git repository

The course's AI policy asks students to write in Google Docs, or an
equivalent that keeps a revision history, so authorship isn't only a
plagiarism-detector's guess. A git repository serves the same purpose: every
commit is a real, timestamped snapshot of the document as it grew, entry by
entry, over several days — not a single pasted block of text. The repository
is hosted on GitHub, so commit timestamps are also server-verified, not just
set on my own machine.

**For a quick look at the writing process:** the [commit
history](https://github.com/aliperdehan/ant233-site-report/commits/main)
shows the bibliography being built up source by source, plus a later pass
for factual review and one for grammar (see `AI-USE.md` below for exactly
what each pass did).

## What's here

- **`bib/annotated-bibliography.md`** — the annotated bibliography, source.
- **`AI-USE.md`** — a full account of what AI assistance was and wasn't used
  for on this assignment (tooling/setup vs. writing, plus a separate
  research-and-checking pass and a Grammarly pass, each documented with
  what changed and why).
- **`bib/references.bib`**, **`bib/fullcite.lua`** — citation data and a
  small rendering filter (see "Rendering" below).
- **`report/`** — site report, added later in the term.
- **`info/`**, **`sources/`** — course handouts and source PDFs, kept
  locally for reference but not version-controlled (not my own writing).

## Rendering

The bibliography and `AI-USE.md` render to PDF via
[Pandoc](https://pandoc.org) and are concatenated into one submission file.
Sources are in `bib/references.bib` (BibTeX), styled with an APA CSL. Each
entry cites its source as `@citekey` (renders as an in-text citation
automatically) and pulls that one source's full formatted reference inline
via a small custom filter (`bib/fullcite.lua`), rather than only getting a
single combined bibliography at the end of the document.

<details>
<summary>Commands (for my own reference)</summary>

Typical writing session:

```bash
git status
git add bib/annotated-bibliography.md
git commit -m "add annotation for Rink 1995"
git push
```

Render (via [pdfmd](https://github.com/aliperdehan/pdfmd), which picks up
the citation filter automatically from the document's own front matter):

```bash
cd bib && pdfmd annotated-bibliography.md
pdfmd AI-USE.md   # from the repo root
qpdf --empty --pages bib/annotated-bibliography.pdf AI-USE.pdf -- annotated-bibliography-with-ai-use.pdf
```

Without pdfmd, call pandoc directly:

```bash
pandoc bib/annotated-bibliography.md --citeproc --lua-filter=bib/fullcite.lua --resource-path=bib -o bib/annotated-bibliography.pdf
```

(`--citeproc` has to come before `--lua-filter` — the filter reads
citeproc's resolved output.)

</details>
