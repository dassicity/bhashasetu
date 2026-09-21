#!/usr/bin/env python3
"""
Handwriting workbooks for Brahmic targets that sit on a baseline (Telugu, Tamil).

Everything that depends on the SOURCE language lives in worksheets/data/{pair}.json,
written by the course agent who built that pair. Everything that depends on the TARGET
script lives in SCRIPTS below plus worksheets/data/targets/{iso}.json. Nothing in this
file is language-specific, which is the whole point: adding a pair is adding a JSON file.

The geometry is measured, not guessed. See calibrate_brahmic.html and README.md.
  body = letter height above the baseline, as a fraction of font size
  top  = how far signs above the letter reach
  bot  = how far signs below the letter reach
Because these are properties of the SCRIPT, every pair sharing a target reuses them.

  python3 gen_brahmic.py                 # every pair with a data file
  python3 gen_brahmic.py hindi_to_tamil  # one pair
"""
import os, html, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

SCRIPTS = {
 "te": {"font":"Noto Serif Telugu", "cls":"te", "body":0.772, "top":1.020, "bot":0.460,
        "signs":"gunintam", "combo":"ottu",   "others":("\u0c16","\u0c17")},
 "ta": {"font":"Noto Serif Tamil",  "cls":"ta", "body":0.497, "top":0.810, "bot":0.280,
        "signs":"uyirmei",  "combo":"pulli",  "others":("\u0bb8","\u0baa")},
}

REQUIRED_UI = ["trace","times","fill","start_given","finish_row","self","fill_row",
               "in_word","then_self","model","grey","hollow","faint","legend",
               "same_sign","words_hint","sent_seq","sent_head","sent_hint"]
REQUIRED_TOP = ["pair","source_iso","target_iso","sub","title","book","digits",
                "words_word","sent_word","index_blurb","print_note","books",
                "letters","words1","words2","sent1","sent2"]

_CACHE = {}

def C(pair):
    if pair not in _CACHE:
        with open(os.path.join(DATA_DIR, f"{pair}.json"), encoding="utf-8") as f:
            _CACHE[pair] = json.load(f)
    return _CACHE[pair]

def GEOM(pair):  return SCRIPTS[C(pair)["target_iso"]]
def U(pair, k):  return C(pair)["ui"][k]
def BOOK(pair, i): return C(pair)["books"][i]

def D(pair, n):
    d = C(pair)["digits"]
    return "".join(d[int(ch)] for ch in str(n))

def audit(pair):
    """Report what a pair file is missing rather than failing halfway through a build."""
    c = C(pair); miss = []
    miss += [f"top-level: {k}" for k in REQUIRED_TOP if k not in c]
    miss += [f'ui: {k}' for k in REQUIRED_UI if k not in c.get("ui", {})]
    if len(c.get("books", [])) != 8:
        miss.append(f'books: expected 8, found {len(c.get("books", []))}')
    for i in (2, 3):
        if i < len(c.get("books", [])) and not c["books"][i].get("rule"):
            miss.append(f'books[{i}].rule')
    if not c.get("rules"):
        miss.append("rules (the five cover lines)")
    if len(c.get("digits", "")) != 10:
        miss.append("digits: need exactly 10 characters")
    g = SCRIPTS[c["target_iso"]]
    for key in ("vowels", "cons", g["signs"], g["combo"]):
        if not c.get("letters", {}).get(key):
            miss.append(f"letters.{key}")
    for grp, items in c.get("words1", {}).items():
        pass
    n1 = sum(len(v) for v in c.get("words1", {}).values())
    n2 = sum(len(v) for v in c.get("words2", {}).values())
    if n1 < 50: miss.append(f"words1: {n1} words, the brief asks for 50 to 60")
    if n2 < 50: miss.append(f"words2: {n2} words, the brief asks for 50 to 60")
    if len(c.get("sent1", [])) < 25: miss.append(f'sent1: {len(c.get("sent1", []))} sentences, need 25 to 30')
    if len(c.get("sent2", [])) < 25: miss.append(f'sent2: {len(c.get("sent2", []))} sentences, need 25 to 30')
    # The cover has a fixed height. Long rule lines silently push it onto a second page,
    # which then repeats in every book of the pair (found in kannada_to_telugu: 1334 chars
    # of rules made all eight books one page longer than their sheet count).
    import re as _re
    plain = [_re.sub(r"<[^>]+>", "", r) for r in c.get("rules", [])]
    if plain:
        tot, longest = sum(len(x) for x in plain), max(len(x) for x in plain)
        if tot > 1200 or longest > 280:
            miss.append(f"rules too long for the cover: {tot} chars total, longest {longest}. "
                        f"Keep the total at or under 1200 and each line at or under 280, "
                        f"or the cover runs to a second page in every book")
    blob = json.dumps(c, ensure_ascii=False)
    if "\u2014" in blob: miss.append("em-dash characters present; this project uses '-'")
    return miss

STYLE = """
:root{
  --base: 18mm;        /* the baseline - letters SIT on this */
  --body: {BODY};      /* letter height above baseline, as a fraction of size */
  --top:  {TOP};       /* how far signs above reach */
  --bot:  {BOT};       /* how far signs below reach */
  --gs:   {GS};        /* practice font size, derived so body = 10mm */
  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --teal:#1F4D4A;
  --line:#9aa8b8; --line-soft:#c7d0da;
  --trace:#c9c9c9; --outline:#bdbdbd; --faint:#e3e3e3;
}
@page{ size:A4; margin:11mm 10mm 12mm 10mm; }
*{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
html,body{ margin:0; padding:0; background:#fff; }
body{ font-family:'{SFONT}',serif; color:var(--ink); font-size:10pt; }
.tg{ font-family:'{TFONT}',serif; }

.sheet{ page-break-after:always; break-after:page; position:relative; min-height:262mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }

.ph{ display:flex; align-items:flex-end; justify-content:space-between;
     border-bottom:0.5mm solid var(--ink); padding-bottom:2mm; margin-bottom:3mm; }
.ph-l{ display:flex; align-items:flex-end; gap:5mm; }
.ph .big{ font-size:20mm; line-height:1.35; }
.ph .meta{ padding-bottom:1.5mm; }
.ph .eq{ font-size:13pt; } .ph .eq b{ color:var(--sindoor); }
.ph .tr{ font-family:'JetBrains Mono',monospace; font-size:9pt; color:var(--sindoor); }
.ph .ex{ font-size:10pt; color:var(--faded); margin-top:1mm; }
.ph-r{ text-align:right; padding-bottom:1.5mm; }
.ph-r .grp{ font-size:9pt; color:var(--faded); }
.ph-r .num{ font-size:9pt; color:var(--faded); letter-spacing:.14em; }

.note{ font-size:9.5pt; line-height:1.65; margin:0 0 3mm; padding:2mm 3mm;
       background:rgba(31,77,74,0.06); border-left:2mm solid var(--teal); }
.note b{ color:var(--sindoor); }

.rowlabel{ font-size:8.5pt; color:var(--faded); margin:0 0 0.8mm;
           display:flex; justify-content:space-between; align-items:baseline; }
.rowlabel b{ color:var(--teal); font-weight:600; }
.row{ position:relative; margin-bottom:2.2mm;
      --asc:  calc(var(--base) - var(--top) * var(--gs));
      --bodyline: calc(var(--base) - var(--body) * var(--gs));
      --desc: calc(var(--base) + var(--bot) * var(--gs));
      height: calc(var(--desc) + 2mm); }
.row .ln{ position:absolute; left:0; right:0; height:0; }
.ln.a{ top:var(--asc);      border-top:0.25mm dashed var(--line-soft); }
.ln.h{ top:var(--bodyline); border-top:0.4mm solid var(--line); }
.ln.b{ top:var(--base);     border-top:0.45mm solid var(--line); }
.ln.d{ top:var(--desc);     border-top:0.25mm dashed var(--line-soft); }
/* strut pins the text baseline to --base whatever the font's line metrics */
.row .cells{ position:absolute; left:0; right:0; top:0; display:flex; line-height:0; }
.st{ display:inline-block; width:0; height:var(--base); vertical-align:baseline; }
.row .c{ font-family:'{TFONT}',serif; font-size:var(--gs); line-height:0;
         flex:0 0 auto; width:24mm; text-align:center; }
.row.wide{ --base:14mm; --gs:{GSW}; }
.row.wide .c{ width:auto; padding-right:10mm; text-align:left; }
.row.sent{ --base:12mm; --gs:{GSS}; }
.row.sent .cells{ display:block; }
.row.sent .c{ display:block; width:auto; text-align:left; }

.t-model{ color:var(--ink); } .t-trace{ color:var(--trace); }
.t-out{ color:transparent; -webkit-text-stroke:0.28mm var(--outline); }
.t-faint{ color:var(--faint); }

.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-size:10pt; letter-spacing:.24em; color:var(--sindoor); }
.cover h1{ font-size:28pt; margin:6mm 0 2mm; line-height:1.3; }
.cover h1 .tg{ display:block; font-size:32pt; margin-bottom:4mm; line-height:1.5; }
.cover .sub{ font-size:12pt; color:var(--faded); max-width:140mm; margin:0 auto; line-height:1.75; }
.rules{ text-align:left; max-width:152mm; margin:11mm auto 0; }
.rules h2{ font-size:12pt; margin:0 0 3mm; color:var(--sindoor); }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ margin-bottom:3mm; line-height:1.7; font-size:10.5pt; }
.rules li b{ color:var(--teal); }
.legend{ margin:9mm auto 0; max-width:152mm; border:0.3mm solid var(--line-soft);
         border-radius:1.5mm; padding:4mm 5mm; }
.legend h3{ margin:0 0 2.5mm; font-size:10pt; color:var(--teal); }
.legend .lg{ display:flex; gap:7mm; align-items:flex-end; }
.legend .lg div{ text-align:center; font-size:8.5pt; color:var(--faded); }
.legend .lg .s{ font-size:12mm; line-height:1.4; display:block; }
.cover .foot{ position:absolute; bottom:6mm; left:0; right:0; text-align:center;
              font-family:'JetBrains Mono',monospace; font-size:8pt; letter-spacing:.16em;
              text-transform:uppercase; color:var(--sindoor); }
.pf{ position:absolute; bottom:0; left:0; right:0; display:flex; justify-content:space-between;
     border-top:0.25mm solid var(--line-soft); padding-top:1.5mm; font-size:8pt; color:var(--faded); }
"""

# The source script's font follows the source language, not the generator. Before this was
# parameterised every workbook requested Noto Serif Bengali whatever the source was, so a
# Telugu or Hindi source fell back to whatever the machine happened to have. That renders
# differently on every printer, which defeats the point of pinning the geometry.
SOURCE_FONTS = {
 "bn":"Noto Serif Bengali",   "hi":"Noto Serif Devanagari", "mr":"Noto Serif Devanagari",
 "te":"Noto Serif Telugu",    "ta":"Noto Serif Tamil",      "kn":"Noto Serif Kannada",
 "ml":"Noto Serif Malayalam", "pa":"Noto Serif Gurmukhi",   "ur":"Noto Nastaliq Urdu",
}

def _fam(name):
    w = "wght@400;500" if "Nastaliq" in name else "wght@400;500;600;700"
    return "family=" + name.replace(" ", "+") + ":" + w

def fonts_url(*names):
    seen = []
    for n in names:
        if n and n not in seen: seen.append(n)
    return ("https://fonts.googleapis.com/css2?" + "&".join(_fam(n) for n in seen)
            + "&family=JetBrains+Mono:wght@400;500&display=swap")

# The rule that differs from the Devanagari books: there is no headline here.
def page_head(pair, title):
    c = C(pair); g = GEOM(pair)
    gs = 10.0 / g["body"]
    css = (STYLE.replace("{BODY}", str(g["body"])).replace("{TOP}", str(g["top"]))
           .replace("{BOT}", str(g["bot"])).replace("{GS}", f"{gs:.2f}mm")
           .replace("{GSW}", f"{gs*0.78:.2f}mm").replace("{GSS}", f"{gs*0.62:.2f}mm")
           .replace("{TFONT}", g["font"])
           .replace("{SFONT}", SOURCE_FONTS[c["source_iso"]]))
    return f"""<!DOCTYPE html>
<html lang="{c["source_iso"]}">
<head>
<meta charset="UTF-8"/>
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{fonts_url(SOURCE_FONTS[c["source_iso"]], g["font"])}" rel="stylesheet"/>
<style>{css}</style>
</head>
<body>
"""

def row(cells_html, lab_l, lab_r="", cls=""):
    return f"""<div class="rowlabel"><span>{lab_l}</span><span>{lab_r}</span></div>
<div class="row {cls}">
  <div class="ln a"></div><div class="ln h"></div><div class="ln b"></div><div class="ln d"></div>
  <div class="cells">{cells_html}</div>
</div>"""

def one(t, c): return f'<span class="c {c}"><i class="st"></i>{t}</span>'
def cells(t, n, c): return "".join(one(t, c) for _ in range(n))
def footer(pair, book, n):
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span>BHASHASETU &middot; {C(pair)["sub"]} &middot; {D(pair,n)}</span></div>')

def cover(pair, bno, native, title, sub):
    c = C(pair); u = c["ui"]
    ol = "".join(f"<li>{r}</li>" for r in c.get("rules", []))
    rules_html = (f'<div class="rules"><h2>{c.get("rules_head","")}</h2><ol>{ol}</ol></div>'
                  if ol else "")
    lg = f"""<div class="legend"><h3>{u["legend"]}</h3><div class="lg">
      <div><span class="s tg t-model">{native[0]}</span>{u["model"]}</div>
      <div><span class="s tg t-trace">{native[0]}</span>{u["grey"]}</div>
      <div><span class="s tg t-out">{native[0]}</span>{u["hollow"]}</div>
      <div><span class="s tg t-faint">{native[0]}</span>{u["faint"]}</div></div></div>"""
    return f"""<div class="sheet cover">
  <div class="kicker">{c["book"]} {bno}</div>
  <h1><span class="tg">{native}</span>{title}</h1>
  <p class="sub">{sub}</p>
  {rules_html}
  {lg}
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""

def letter_sheet(pair, book, n, ch, eq, tr, ex, gloss, group):
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big tg">{ch}</div>
      <div class="meta"><div class="eq">= <b>{eq}</b></div><div class="tr">{tr}</div>
        <div class="ex"><span class="tg">{ex}</span> &middot; {gloss}</div></div>
    </div>
    <div class="ph-r"><div class="grp">{group}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {row(cells(ch,7,'t-trace'), U(pair,"trace"), U(pair,"times"))}
  {row(cells(ch,7,'t-out'), U(pair,"fill"), U(pair,"times"))}
  {row(one(ch,'t-model')+one(ch,'t-faint'), U(pair,"start_given"), U(pair,"finish_row"))}
  {row('', U(pair,"self"), U(pair,"fill_row"))}
  {row('', U(pair,"self"), '')}
  {row(one(ex,'t-model')+one(ex,'t-trace'), f'{U(pair,"in_word")} - <span class="tg">{ex}</span> ({gloss})', U(pair,"then_self"), 'wide')}
  {footer(pair, book, n)}
</div>"""

def sign_sheet(pair, book, n, form, eq, tr, note):
    bk = BOOK(pair,2)
    others = ("ఖ","గ") if C(pair)["target_iso"]=="te" else ("ச","ப")
    sign = form[1:]
    applied = "".join(one(c+sign,'t-model')+one(c+sign,'t-trace') for c in others)
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="big tg">{form}</div>
      <div class="meta"><div class="eq">= <b>{eq}</b></div><div class="tr">{tr}</div>
        <div class="ex">{note}</div></div></div>
    <div class="ph-r"><div class="grp">{bk['label']}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  <div class="note">{bk.get('rule','')}</div>
  {row(cells(form,7,'t-trace'), U(pair,"trace"), U(pair,"times"))}
  {row(cells(form,7,'t-out'), U(pair,"fill"), U(pair,"times"))}
  {row(one(form,'t-model')+one(form,'t-faint'), U(pair,"start_given"), U(pair,"finish_row"))}
  {row(applied, U(pair,"same_sign"), U(pair,"then_self"))}
  {row('', U(pair,"self"), '')}
  {footer(pair, book, n)}
</div>"""

def combo_sheet(pair, book, n, items):
    bk = BOOK(pair,3); blocks = ""
    for cj, parts, ex, gloss, grp in items:
        lab = (f'<span class="tg" style="font-size:13pt">{parts}</span> = '
               f'<span class="tg" style="font-size:15pt"><b>{cj}</b></span>'
               f' &nbsp;&middot;&nbsp; <span class="tg">{ex}</span> ({gloss})')
        blocks += row(cells(cj,6,'t-trace'), lab, U(pair,"trace"))
        blocks += row(cells(cj,4,'t-out')+one(cj,'t-model'), U(pair,"fill"), U(pair,"then_self"))
        blocks += row(one(ex,'t-model')+one(ex,'t-trace'), U(pair,"in_word"), U(pair,"then_self"), 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>{grpv(items[0][4])}</b></div>
      <div class="ex">{bk['label']}</div></div></div>
    <div class="ph-r"><div class="grp">{bk['label']}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  <div class="note">{bk.get('rule','')}</div>
  {blocks}
  {footer(pair, book, n)}
</div>"""
def grpv(g): return g

def words_sheet(pair, book, n, group, items):
    blocks = ""
    for w, gloss in items:
        blocks += row(one(w,'t-model')+one(w,'t-trace'),
                      f'<span class="tg" style="font-size:12pt">{w}</span> &nbsp; = &nbsp; <b>{gloss}</b>',
                      U(pair,"start_given"), 'wide')
        blocks += row('', '', U(pair,"self"), 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta"><div class="eq" style="font-size:16pt"><b>{group}</b></div>
      <div class="ex">{U(pair,"words_hint")}</div></div></div>
    <div class="ph-r"><div class="grp">{C(pair)["words_word"]}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

def sentence_sheet(pair, book, n, items):
    blocks = ""
    for tgt, bn in items:
        blocks += f'<div class="rowlabel"><span><b>{bn}</b></span><span>{U(pair,"sent_seq")}</span></div>'
        blocks += row(one(tgt,'t-model'), '', '', 'sent')
        blocks += row(one(tgt,'t-trace'), U(pair,"trace"), '', 'sent')
        blocks += row('', U(pair,"self"), '', 'sent')
        blocks += row('', '', '', 'sent')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta"><div class="eq" style="font-size:16pt"><b>{U(pair,"sent_head")}</b></div>
      <div class="ex">{U(pair,"sent_hint")}</div></div></div>
    <div class="ph-r"><div class="grp">{C(pair)["sent_word"]}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

# ---------------------------------------------------------------- build
# ---------------------------------------------------------------- build
def build(pair):
    c = C(pair); g = GEOM(pair); L = c["letters"]
    out = os.path.join(HERE, pair); os.makedirs(out, exist_ok=True)
    bks = c["books"]; made = []

    def cov(i, sub=None):
        b = bks[i]
        return cover(pair, D(pair, i + 1), b["native"], b.get("cover_title", b["label"]),
                     sub if sub is not None else b.get("bridge", ""))

    # books 1 and 2: the letters
    for i, key in ((0, "vowels"), (1, "cons")):
        p = [cov(i)]
        for n, r in enumerate(L[key], 1):
            p.append(letter_sheet(pair, f'{c["book"]} {D(pair, i+1)} \u00b7 {bks[i]["label"]}',
                                  n, r["t"], r["eq"], r["roman"], r["ex"], r["gloss"], r["group"]))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    # book 3: the vowel signs
    p = [cov(2)]
    for n, r in enumerate(L[g["signs"]], 1):
        p.append(sign_sheet(pair, f'{c["book"]} {D(pair,3)} \u00b7 {bks[2]["label"]}',
                            n, r["t"], r["eq"], r["roman"], r["note"]))
    made.append((bks[2]["slug"], bks[2]["label"], p))

    # book 4: conjuncts, or whatever the target does instead
    p = [cov(3)]
    items = [(r["t"], r["parts"], r["ex"], r["gloss"], r["group"]) for r in L[g["combo"]]]
    for n, k in enumerate(range(0, len(items), 2), 1):
        p.append(combo_sheet(pair, f'{c["book"]} {D(pair,4)} \u00b7 {bks[3]["label"]}',
                             n, items[k:k+2]))
    made.append((bks[3]["slug"], bks[3]["label"], p))

    # books 5 and 6: words
    for i, key in ((4, "words1"), (5, "words2")):
        p = [cov(i)]; n = 1
        bl = f'{c["book"]} {D(pair, i+1)} \u00b7 {bks[i]["label"]}'
        for group, its in c[key].items():
            for k in range(0, len(its), 4):
                p.append(words_sheet(pair, bl, n, group, [tuple(x) for x in its[k:k+4]])); n += 1
        made.append((bks[i]["slug"], bks[i]["label"], p))

    # books 7 and 8: sentences
    for i, key in ((6, "sent1"), (7, "sent2")):
        p = [cov(i)]
        bl = f'{c["book"]} {D(pair, i+1)} \u00b7 {bks[i]["label"]}'
        its = c[key]
        for k in range(0, len(its), 2):
            p.append(sentence_sheet(pair, bl, k//2 + 1, [tuple(x) for x in its[k:k+2]]))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    rows = ""
    for slug, title, pages in made:
        fn = f"{slug}.html"
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write(page_head(pair, f'{title} - {c["sub"]}') + "\n".join(pages) + "\n</body>\n</html>")
        print(f"  {fn:<24} {len(pages):>3} pages")
        rows += (f'<tr><td><b>{title}</b></td><td>{D(pair, len(pages))}</td>'
                 f'<td><a href="{slug}.pdf">PDF</a></td><td><a href="{fn}">HTML</a></td></tr>')
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_head(pair, f'{c["title"]} - {c["sub"]}') +
                f"""<div style="max-width:150mm;margin:20mm auto;font-size:11pt">
        <h1 style="font-size:20pt">{c["title"]}</h1>
        <p style="color:#6B5B48;line-height:1.7">{c["index_blurb"]}<br/>{c["print_note"]}</p>
        <table style="width:100%;border-collapse:collapse;margin-top:8mm">{rows}</table></div>
        </body></html>""")
    total = sum(len(p) for _, _, p in made)
    print(f"  total {total} pages")
    return total

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = sorted(f[:-5] for f in os.listdir(DATA_DIR)
                      if f.endswith(".json") and not f.startswith("_"))
    for pr in args:
        fp = os.path.join(DATA_DIR, f"{pr}.json")
        if not os.path.exists(fp):
            print(f"{pr}: no data file, skipped"); continue
        iso = json.load(open(fp, encoding="utf-8")).get("target_iso")
        if iso not in SCRIPTS:
            if len(args) < len(os.listdir(DATA_DIR)):   # named explicitly, so say why
                print(f"{pr}: target '{iso}' is not a baseline-sitting Brahmic script; "
                      f"use the generator for that script")
            continue
        miss = audit(pr)
        if miss:
            print(f"{pr}: NOT BUILT, the pair file is missing:")
            for m in miss: print(f"    - {m}")
            continue
        print(f"{pr}:"); build(pr)
