# AI Use Acknowledgement (Site Report)

Tool: Claude Code, running Claude Sonnet 5.5 (Anthropic), 10--15 November 2026.

This documents what AI assistance was used for in the site report (`SR/SR.md`). The text of the report and of its figure caption is my own writing. Earlier uses in this repository (scaffolding, `fullcite.lua`, the annotated bibliography check) are recorded in `AB/AI-USE.md` and were submitted alongside the annotated bibliography.

## Standing rules

Claude was given these rules at the start of the session, and they are shown here as I formalised them.

```
STANDING RULES FOR THIS SESSION

Role: a mechanical tool within this repository. Follow the course AI policy
(info/ANT233_Syllabus_PaleoArchEurasia_F26.pdf) and do not act beyond its
permitted usage. Read the assignment description
(info/Site Report Description and Rubric_F26.pdf) to understand the task.

Permitted:
- checking grammar and pointing to awkward phrasing (point only; give no
  replacement wording)
- mechanically verifying facts, claims, citations and the bibliography
- tooling (e.g. Lua filters for pdfmd)
- building a map for the report from coordinates supplied by the author

Verification: never invent data. Check every claim against the PDFs in
sources/, rendering the pages with pdftoppm at medium resolution and looking
at them before pointing to a slip.

Prohibited: edits to the repository beyond the authorised list; rewriting
paragraphs; any use beyond the course AI policy. All original thought and
writing stems from me.
```

## What Claude was used for

- **Fact and citation checking.** Claude read the cited PDFs in `sources/`, checked each figure, quote and page number against the rendered pages, and pointed to slips with the page where the source says otherwise. The first pass was on the draft as it stood at commit `eddb582` (before any of Claude's work in this session), a second came after my rewrites, and a third on the figure caption. It gave no replacement wording, and every correction was written by me.
- **Tooling.** `metadata/pagecite.lua` (turns a bare `[p. 107]` after a citation into the page reference), and the bibliography, References heading and filter settings in `metadata/metadata.yaml`.
- **Bibliography entries.** The entries for Higham et al. (2006), Devièse et al. (2017) and Radovčić et al. (2016) were created from the first pages of their PDFs.
- **The map (`map/`).** It was first prepared in a separate Claude Code session from coordinates I supplied. That session also offered a suggested caption, which I deleted before moving the project. In this session Claude cross-checked the coordinates against Wikipedia and GeoNames, regenerated the figure in Times New Roman, changed two labels, added the panel letters, and built panel B. For B, Claude measured the band heights on the reproduction of Gorjanović-Kramberger's section in Radovčić et al. (2016); the method and sources are in `map/strat.py`.
- **Web look-ups.** The coordinate cross-check, and one search on the Vindija dating that led me to Higham et al. (2006) and Devièse et al. (2017). I obtained and read both papers myself. Nothing from the web was copied into the report.

## What Claude was not used for

- Writing, rewriting or paraphrasing any sentence of the report or of the figure caption. Every commit to `SR/SR.md` is mine.
- Choosing arguments, interpretations or which sources to cite.

## Grammar checking (Grammarly)

Grammarly was run once over the finished report text, as the course AI policy permits for grammar checking. The pre-Grammarly draft is commit `f663cdd`, and the Grammarly pass is commit `3b8790d`. `git diff f663cdd 3b8790d` shows every change.

## Verification

Every commit in which Claude took part carries a `Co-Authored-By` trailer: `git log -i --grep "co-authored-by"`. The full revision history is at <https://github.com/aliperdehan/ant233-site-report/commits/main>. The prompts for this session are in the Claude Code session transcript, which I can provide on request.
