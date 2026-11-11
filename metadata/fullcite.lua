-- fullcite.lua
--
-- Lets you drop the FULL formatted reference for a single source at an
-- arbitrary point in the document (e.g. next to "**Citation:**" in an
-- annotated bibliography entry), instead of only getting citeproc's one
-- combined "References" list at the end.
--
-- Usage: place a marker on its own line/paragraph:
--
--     [[fullcite:trinkaus1984]]
--
-- and run citeproc BEFORE this filter, e.g.:
--
--     pandoc doc.md --citeproc --lua-filter=fullcite.lua -o out.pdf
--
-- (order on the command line matters: --citeproc must come first so this
-- filter can consume the bibliography div citeproc produces)
--
-- The filter harvests each per-source entry from citeproc's combined
-- bibliography div (id="refs", children id="ref-<citekey>"), substitutes it
-- wherever the matching [[fullcite:<citekey>]] marker appears, and removes
-- the now-redundant combined bibliography div.

-- APA hanging indent, 0.5in. Pandoc's citeproc marks the *combined*
-- bibliography div with a "hanging-indent" class (and the LaTeX/HTML/docx
-- writers do honor that), but that class lives on the outer div this filter
-- discards -- and even with it, Pandoc's typst writer (checked directly: a
-- plain `pandoc --citeproc -t typst` with no custom filter at all) ignores
-- "hanging-indent" entirely and emits a flush-left paragraph. So for typst
-- specifically, this filter applies the indent itself via a raw
-- `#set par(hanging-indent: ...)` block instead of relying on Pandoc's
-- writer to do it. Other output formats (LaTeX/HTML/docx) still lose the
-- indent here, same pre-existing gap as before -- only typst is fixed,
-- since that's the only writer this project's pdfmd-options.engine uses.
local TYPST_HANGING_INDENT = "1.27cm"

local refs = {}

local function harvest_and_strip(blocks)
  local kept = pandoc.List()
  for _, blk in ipairs(blocks) do
    if blk.t == "Div" and blk.identifier == "refs" then
      for _, entry in ipairs(blk.content) do
        if entry.t == "Div" and entry.identifier:match("^ref%-") then
          refs[entry.identifier:sub(5)] = entry.content
        end
      end
      -- drop the combined bibliography div; entries now live inline instead
    else
      kept:insert(blk)
    end
  end
  return kept
end

local function expand(blocks)
  local out = pandoc.List()
  for _, blk in ipairs(blocks) do
    if blk.t == "Para" or blk.t == "Plain" then
      local text = pandoc.utils.stringify(blk):match("^%s*(.-)%s*$")
      local key = text:match("^%[%[fullcite:(.-)%]%]$")
      if key then
        local entry = refs[key]
        if entry then
          if FORMAT == "typst" then
            -- #par(...)[...] (the direct element-function call), not
            -- #block[ #set par(hanging-indent: ...) ... ] -- tested both
            -- directly with the typst CLI (0.15.1): #block silently drops
            -- the hanging-indent entirely (no error, just flush-left output,
            -- confirmed at 1.27cm AND 5cm), while #par(...)[...] renders it
            -- correctly. Root cause not chased further; this form is what
            -- actually works.
            local rendered = pandoc.write(pandoc.Pandoc(entry), "typst")
            out:insert(pandoc.RawBlock("typst",
              "#par(hanging-indent: " .. TYPST_HANGING_INDENT .. ")[\n"
              .. rendered .. "]"))
          else
            for _, b in ipairs(entry) do out:insert(b) end
          end
        else
          io.stderr:write("fullcite.lua: no reference found for citekey '" .. key .. "' (check references.bib and spelling)\n")
          out:insert(blk)
        end
      else
        out:insert(blk)
      end
    else
      out:insert(blk)
    end
  end
  return out
end

-- Inline code (`like this`) is used for verbatim quotes from sources: render
-- it as a normal curly-quoted quotation in the body font, not monospace.
-- Double quotes inside the quote become single quotes (quote-within-quote).
function Code(el)
  local text = el.text:gsub('"', "'")
  local parsed = pandoc.read('"' .. text .. '"', 'markdown+smart')
  if parsed.blocks[1] then return parsed.blocks[1].content end
end

function Pandoc(doc)
  local blocks = harvest_and_strip(doc.blocks)
  doc.blocks = expand(blocks)
  return doc
end
