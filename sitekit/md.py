"""Tiny Markdown dialect for CoupeFab guides (no external deps).

Supported: ## / ### / #### headings (auto ids), paragraphs, - and 1. lists (one nesting level
by 2+ space indent), - [ ] checklists, pipe tables, ``` code fences, > callouts with
> [!NOTE] / [!TIP] / [!WARN] / [!SHOP] markers, **bold**, *italic*, `code`, [text](url),
raw HTML blocks (a line starting with "<"), and "---" horizontal rules.
"""
import html
import re
import unicodedata

CALLOUT_LABELS = {
    "fr": {"NOTE": "À savoir", "TIP": "Astuce d’atelier", "WARN": "Attention", "SHOP": "À valider en atelier"},
    "en": {"NOTE": "Good to know", "TIP": "Shop tip", "WARN": "Caution", "SHOP": "To confirm in the shop"},
}


def slugify(text: str) -> str:
    t = unicodedata.normalize("NFKD", text)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"<[^>]+>", "", t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60] or "section"


_INLINE_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITAL = re.compile(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])")


def inline(text: str) -> str:
    codes = []

    def keep_code(m):
        codes.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return f"\x00{len(codes)-1}\x00"

    t = _INLINE_CODE.sub(keep_code, text)
    # escape, but keep &nbsp; style entities and simple <br>, <kbd>, <abbr>, <sub>, <sup>
    t = html.escape(t, quote=False)
    t = re.sub(r"&lt;(/?)(br|kbd|abbr|sub|sup|small|span|mark)((?: [a-z-]+=&quot;[^&]*&quot;| [a-z-]+=\"[^\"]*\")*)\s*/?&gt;",
               lambda m: "<" + m.group(1) + m.group(2) + m.group(3).replace("&quot;", '"') + ">", t)
    t = re.sub(r"&amp;(#?\w+);", r"&\1;", t)

    def link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        attrs = ' rel="noopener"' if ext else ""
        cls = ' class="ext"' if ext else ""
        return f'<a href="{url}"{cls}{attrs}>{label}</a>'

    t = _LINK.sub(link, t)
    t = _BOLD.sub(r"<strong>\1</strong>", t)
    t = _ITAL.sub(r"<em>\1</em>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], t)
    return t


def _table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    head, body = rows[0], rows[2:] if len(rows) > 1 and re.match(r"^[\s|:\-]+$", lines[1]) else rows[1:]
    aligns = []
    if len(lines) > 1 and re.match(r"^[\s|:\-]+$", lines[1]):
        for c in lines[1].strip().strip("|").split("|"):
            c = c.strip()
            aligns.append("num" if c.endswith(":") and not c.startswith(":") else "")
    def td(tag, c, i):
        cls = f' class="{aligns[i]}"' if i < len(aligns) and aligns[i] else ""
        return f"<{tag}{cls}>{inline(c)}</{tag}>"
    out = ['<div class="table-wrap" tabindex="0"><table>', "<thead><tr>" + "".join(td("th", c, i) for i, c in enumerate(head)) + "</tr></thead><tbody>"]
    for r in body:
        out.append("<tr>" + "".join(td("td", c, i) for i, c in enumerate(r)) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def _list(lines):
    """lines: raw lines of a list block. Supports 1 nesting level."""
    ordered = bool(re.match(r"^\d+\.\s", lines[0].lstrip()))
    items = []  # (text, [sublines])
    for l in lines:
        if re.match(r"^(\s{2,}|\t)", l) and items:
            items[-1][1].append(l.strip())
        elif re.match(r"^\s*([-*]|\d+\.)\s+", l):
            items.append([re.sub(r"^\s*([-*]|\d+\.)\s+", "", l), []])
        elif items:
            items[-1][0] += " " + l.strip()
    check = all(i[0].startswith("[ ]") or i[0].startswith("[x]") for i in items)
    tag = "ol" if ordered else "ul"
    cls = ' class="checklist"' if check else (' class="steps"' if ordered else "")
    out = [f"<{tag}{cls}>"]
    for text, sub in items:
        if check:
            text = text[3:].strip()
        inner = inline(text)
        if sub:
            inner += _list(sub)
        out.append(f"<li>{inner}</li>")
    out.append(f"</{tag}>")
    return "".join(out)


def render(src: str, lang: str = "fr"):
    """Return (html, toc) where toc is a list of (level, id, text)."""
    lines = src.strip("\n").split("\n")
    out, toc, used = [], [], set()
    i = 0
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(s.strip() for s in para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("```"):
            flush()
            lang_hint = s[3:].strip()
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j]); j += 1
            cls = f' class="lang-{lang_hint}"' if lang_hint else ""
            out.append(f"<pre{cls}><code>" + html.escape("\n".join(buf), quote=False) + "</code></pre>")
            i = j + 1; continue
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            flush()
            level = len(m.group(1))
            text = m.group(2).strip()
            hid = slugify(text)
            base, n = hid, 2
            while hid in used:
                hid = f"{base}-{n}"; n += 1
            used.add(hid)
            toc.append((level, hid, re.sub(r"[`*]", "", text)))
            out.append(f'<h{level} id="{hid}">{inline(text)}</h{level}>')
            i += 1; continue
        if s == "---":
            flush(); out.append("<hr>"); i += 1; continue
        if s.startswith("|"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                buf.append(lines[i]); i += 1
            out.append(_table(buf)); continue
        if s.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            kind = "NOTE"
            mm = re.match(r"^\[!(NOTE|TIP|WARN|SHOP)\]\s*(.*)$", buf[0].strip())
            if mm:
                kind = mm.group(1)
                buf[0] = mm.group(2)
            label = CALLOUT_LABELS["fr" if lang == "fr" else "en"][kind]
            inner, _ = render("\n".join(buf), lang)
            out.append(f'<aside class="callout callout-{kind.lower()}"><p class="callout-label">{label}</p>{inner}</aside>')
            continue
        if re.match(r"^([-*]|\d+\.)\s+", s):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip() and (re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or re.match(r"^(\s{2,}|\t)\S", lines[i])):
                buf.append(lines[i]); i += 1
            out.append(_list(buf)); continue
        if s.startswith("<"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i]); i += 1
            out.append("\n".join(buf)); continue
        para.append(s)
        i += 1
    flush()
    return "\n".join(out), toc
