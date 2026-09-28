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
          for _, b in ipairs(entry) do out:insert(b) end
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
