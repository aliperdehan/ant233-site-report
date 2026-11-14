-- pagecite.lua
--
-- Lets a bare page marker written after a citation stand for that citation's page:
--
--     ... as the authors note [@simek1997, p. 562]. The shifts are small [p. 569].
--
-- `[p. 569]`, `[pp. 567, 569--570]` and the like are plain text to Pandoc (not citations).
-- This filter finds each such marker and replaces it with a parenthetical page reference,
-- using the most recent citation in the same paragraph as "the previous source".
--
-- Modes (metadata key `pagecite`, default `bare`):
--   bare : the marker becomes literal text "(p. 569)"; works whatever the filter order.
--   full : the marker becomes a real citation of the previous source with that locator,
--          i.e. "(Simek & Smith, 1997, p. 569)". The filter must then run BEFORE
--          citeproc: `pandoc --lua-filter=pagecite.lua --citeproc ...`.
--
-- A marker with no earlier citation in its paragraph is left unchanged, with a warning on
-- stderr. A warning is also printed when the previous citation holds several sources
-- (the last one is used). `pagecite-verbose: true` prints every marker -> source pairing.
--
-- Citations Pandoc already understands, such as `@simek1997 [p. 562]` or
-- `[@simek1997, p. 562]`, are never touched.

local mode = "bare"
local verbose = false

local function meta_string(v)
  if v == nil then return nil end
  return pandoc.utils.stringify(v)
end

function Meta(meta)
  local m = meta_string(meta.pagecite)
  if m == "bare" or m == "full" then mode = m end
  local vb = meta_string(meta["pagecite-verbose"])
  if vb == "true" then verbose = true end
end

local function warn(msg) io.stderr:write("pagecite.lua: " .. msg .. "\n") end

-- "[p.", "[pp." (the marker's first token, already known to start with "[")
local function opens_marker(s)
  return s:match("^%[pp?%.") ~= nil
end

local function process(inlines, where)
  local out = pandoc.List()
  local prev_key = nil
  local i = 1
  while i <= #inlines do
    local el = inlines[i]
    if el.t == "Cite" then
      local ids = el.citations
      prev_key = ids[#ids].id
      if #ids > 1 then prev_key = { id = prev_key, multi = true } end
      out:insert(el)
      i = i + 1
    elseif el.t == "Str" and opens_marker(el.text) then
      -- gather tokens up to the one that contains "]"
      local j, buf, closed = i, {}, false
      local tail = ""
      while j <= #inlines do
        local t = inlines[j]
        local s
        if t.t == "Str" then s = t.text
        elseif t.t == "Space" or t.t == "SoftBreak" then s = " "
        else break end
        local close = s:find("]", 1, true)
        if close then
          buf[#buf + 1] = s:sub(1, close - 1)
          tail = s:sub(close + 1)
          closed = true
          break
        end
        buf[#buf + 1] = s
        j = j + 1
      end
      if closed then
        local text = table.concat(buf):sub(2)             -- drop the opening "["
        text = text:gsub("\u{00A0}", " "):gsub("%-%-", "\u{2013}"):gsub("%s+", " ")
        text = text:match("^%s*(.-)%s*$")
        local key = type(prev_key) == "table" and prev_key.id or prev_key
        if key == nil then
          warn("no earlier citation in " .. where .. " for marker [" .. text .. "]; left as is")
          out:insert(el)
          i = i + 1
        else
          if type(prev_key) == "table" then
            warn("marker [" .. text .. "] follows a multi-source citation; using " .. key)
          end
          if verbose then io.stderr:write("pagecite.lua: [" .. text .. "] -> @" .. key .. "\n") end
          if mode == "full" then
            local doc = pandoc.read("[@" .. key .. ", " .. text .. "]", "markdown")
            local cite = doc.blocks[1].content[1]
            out:insert(cite)
          else
            out:insert(pandoc.Str("(" .. text .. ")"))
          end
          if tail ~= "" then out:insert(pandoc.Str(tail)) end
          i = j + 1
        end
      else
        out:insert(el)
        i = i + 1
      end
    else
      out:insert(el)
      i = i + 1
    end
  end
  return out
end

function Para(el)
  el.content = process(el.content, "this paragraph")
  return el
end

function Plain(el)
  el.content = process(el.content, "this paragraph")
  return el
end

-- Meta must run before the blocks so the mode is known
return {
  { Meta = Meta },
  { Para = Para, Plain = Plain },
}
