#!/usr/bin/env python3
"""
Handwriting workbooks for Hangul targets.

Hangul is not an abugida and not an abjad, so it does not get ruled lines. A Korean
syllable is drawn inside a notional square and every syllable gets the same square
whatever it contains, which is why Korean practice paper is a grid (wongoji) rather
than a set of baselines. This generator draws that grid, with faint cross-hairs in
each cell the way children's practice paper does, and puts ONE SYLLABLE PER CELL all
the way through: in the word books and the sentence books too, because that is the
habit the learner needs and the thing a Brahmic-trained hand will not do by default.

Geometry, measured with canvas TextMetrics (calibrate_hangul.html), as fractions of
the font size: a full block with a batchim runs 0.804 up and 0.084 down; the widest
blocks advance 0.966. So a block is very nearly square and fills the em, and the only
number that matters is how much of the cell it should occupy. That is FILL below.

  python3 gen_hangul.py                      # every Hangul-target pair with a data file
  python3 gen_hangul.py bengali_to_korean    # one pair
"""
import os, html, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

SCRIPTS = {"ko": {"font": "Noto Serif KR", "fill": 0.80}}

SOURCE_FONTS = {
 "bn":"Noto Serif Bengali",   "hi":"Noto Serif Devanagari", "mr":"Noto Serif Devanagari",
 "te":"Noto Serif Telugu",    "ta":"Noto Serif Tamil",      "kn":"Noto Serif Kannada",
 "ml":"Noto Serif Malayalam", "pa":"Noto Serif Gurmukhi",   "ur":"Noto Nastaliq Urdu",
}
def _fam(n):
    w = "wght@400;500" if "Nastaliq" in n else "wght@400;500;600;700"
    return "family=" + n.replace(" ", "+") + ":" + w
def fonts_url(*names):
    seen = []
    for n in names:
        if n and n not in seen: seen.append(n)
    return ("https://fonts.googleapis.com/css2?" + "&".join(_fam(n) for n in seen)
            + "&family=JetBrains+Mono:wght@400;500&display=swap")

REQUIRED_UI = ["trace","fill","self","times","start_given","finish_row","fill_row","in_word",
               "then_self","model","grey","hollow","faint","legend","box","box_hint","slots",
               "stroke_order","parts_head","assemble","same_jamo","batchim_head","batchim_hint",
               "written_heard","words_hint","sent_seq","sent_head","sent_hint"]
REQUIRED_TOP = ["pair","source_iso","target_iso","sub","title","book","digits","words_word",
                "sent_word","index_blurb","print_note","books","letters","words1","words2",
                "sent1","sent2"]

SHARED_PUNCT = {0x0964, 0x0965}   # danda and double danda: common to all Indic scripts

_CACHE = {}
def C(pair):
    if pair not in _CACHE:
        with open(os.path.join(DATA_DIR, f"{pair}.json"), encoding="utf-8") as f:
            _CACHE[pair] = json.load(f)
    return _CACHE[pair]
def G(pair): return SCRIPTS[C(pair)["target_iso"]]
def U(pair, k): return C(pair)["ui"][k]
def BOOK(pair, i): return C(pair)["books"][i]
def D(pair, n):
    d = C(pair)["digits"]
    return "".join(d[int(c)] for c in str(n))

def audit(pair):
    c = C(pair); miss = []
    miss += [f"top-level: {k}" for k in REQUIRED_TOP if k not in c]
    miss += [f"ui: {k}" for k in REQUIRED_UI if k not in c.get("ui", {})]
    if len(c.get("books", [])) != 8:
        miss.append(f'books: expected 8, found {len(c.get("books", []))}')
    if len(c.get("digits","")) != 10: miss.append("digits: need exactly 10 characters")
    for k in ("jaeum","moeum","moa","batchim"):
        if not c.get("letters", {}).get(k): miss.append(f"letters.{k}")
    import re as _re
    plain = [_re.sub(r"<[^>]+>","",r) for r in c.get("rules", [])]
    if plain:
        tot, longest = sum(len(x) for x in plain), max(len(x) for x in plain)
        if tot > 1200 or longest > 280:
            miss.append(f"rules too long for the cover: {tot} chars, longest {longest}")
    RANGES = {"bn":(0x980,0x9FF),"te":(0xC00,0xC7F),"kn":(0xC80,0xCFF),"ta":(0xB80,0xBFF),
              "ml":(0xD00,0xD7F),"pa":(0xA00,0xA7F),"hi":(0x900,0x97F)}
    iso = c.get("source_iso")
    blob = json.dumps(c, ensure_ascii=False)
    for other,(lo,hi) in RANGES.items():
        if other == iso: continue
        hits = [ch for ch in blob if lo <= ord(ch) <= hi and ord(ch) not in SHARED_PUNCT]
        if hits:
            miss.append(f"{len(hits)} characters of {other} script in a {iso} pair file "
                        f"(e.g. {''.join(hits[:6])})")
    n1 = sum(len(v) for v in c.get("words1",{}).values())
    n2 = sum(len(v) for v in c.get("words2",{}).values())
    if n1 < 50: miss.append(f"words1: {n1} words, the brief asks for 50 to 60")
    if n2 < 50: miss.append(f"words2: {n2} words, the brief asks for 50 to 60")
    if len(c.get("sent1",[])) < 25: miss.append(f'sent1: {len(c.get("sent1",[]))}, need 25 to 30')
    if len(c.get("sent2",[])) < 25: miss.append(f'sent2: {len(c.get("sent2",[]))}, need 25 to 30')
    if "—" in blob: miss.append("em-dash characters present; this project uses '-'")
    return miss

STYLE = """
:root{
  --cell: 15mm;             /* one syllable square, letter books */
  --gs:   {GS};             /* block size, derived so the glyph fills FILL of the cell */
  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --ochre:#B8802D; --teal:#1F4D4A;
  --line:#9aa8b8; --line-soft:#c7d0da; --paper:#FDFBF6;
}
@page{ size:A4; margin:12mm 10mm; }
*{ box-sizing:border-box; }
body{ font-family:'{SFONT}',serif; color:var(--ink); font-size:10pt; margin:0;
      background:var(--paper); }
.sheet{ page-break-after:always; break-after:page; padding:0 2mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }
.ko{ font-family:'{TFONT}',serif; }

/* ---- page head ---- */
.ph{ display:flex; justify-content:space-between; align-items:flex-start;
     border-bottom:0.4mm solid var(--line-soft); padding-bottom:2.5mm; margin-bottom:4mm; }
.ph-l{ display:flex; gap:6mm; align-items:flex-start; }
.big{ font-size:26mm; line-height:1; font-family:'{TFONT}',serif; }
.meta{ padding-top:2mm; }
.meta .eq{ font-size:13pt; }
.meta .tr{ font-family:'JetBrains Mono',monospace; font-size:9pt; color:var(--faded);
           letter-spacing:.08em; margin-top:1mm; }
.meta .ex{ font-size:10pt; color:var(--faded); margin-top:1.5mm; }
.ph-r{ text-align:right; }
.grp{ font-size:9pt; color:var(--teal); max-width:60mm; }
.num{ font-size:14pt; color:var(--faded); margin-top:1mm; }
.note{ font-size:9.5pt; color:var(--faded); background:#F4F1EA; border-left:1mm solid var(--ochre);
       padding:2mm 3mm; margin:0 0 3.5mm; line-height:1.6; }

/* ---- the grid: one syllable per square, with the faint cross-hairs of practice paper ---- */
.rowlabel{ display:flex; justify-content:space-between; font-size:8.5pt; color:var(--faded);
           margin:0 0 1mm; }
.grid{ display:flex; flex-wrap:wrap; gap:0; margin-bottom:3.5mm; }
/* Word and sentence rows stack three grids per item, so they get a tighter square. */
.grid.w{ --cell:12mm; --gs:{GSW}; margin-bottom:0; }
.grid.s{ --cell:11mm; --gs:{GSS}; margin-bottom:0; }
.grid.w:last-of-type, .grid.s:last-of-type{ margin-bottom:3mm; }
.cell{ width:var(--cell); height:var(--cell); border:0.25mm solid var(--line-soft);
       margin:-0.125mm 0 0 -0.125mm; display:flex; align-items:center; justify-content:center;
       font-family:'{TFONT}',serif; font-size:var(--gs); line-height:1; overflow:hidden;
       background-image:
         linear-gradient(to bottom, transparent calc(50% - 0.06mm), var(--line-soft) calc(50% - 0.06mm),
                         var(--line-soft) calc(50% + 0.06mm), transparent calc(50% + 0.06mm)),
         linear-gradient(to right,  transparent calc(50% - 0.06mm), var(--line-soft) calc(50% - 0.06mm),
                         var(--line-soft) calc(50% + 0.06mm), transparent calc(50% + 0.06mm)); }
.cell.gap{ border-color:transparent; background-image:none; }
.t-model{ color:var(--ink); }
.t-trace{ color:#BFB6A6; }
.t-out{ color:transparent; -webkit-text-stroke:0.22mm #BFB6A6; }
.t-faint{ color:#E4DECF; }

/* ---- covers ---- */
.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-family:'JetBrains Mono',monospace; font-size:9pt; letter-spacing:.2em;
                color:var(--sindoor); }
.cover h1{ font-size:24pt; margin:4mm 0 2mm; font-weight:600; }
.cover h1 .ko{ display:block; font-size:34pt; margin-bottom:3mm; }
.cover .sub{ font-size:11pt; color:var(--faded); max-width:130mm; margin:0 auto 8mm;
             line-height:1.8; }
.rules{ max-width:140mm; margin:0 auto; text-align:left; }
.rules h2{ font-size:11pt; color:var(--teal); margin:0 0 3mm; }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ font-size:10pt; line-height:1.85; margin-bottom:2.5mm; color:var(--faded); }
.rules li b{ color:var(--ink); }
.legend{ max-width:140mm; margin:8mm auto 0; text-align:left; }
.legend h3{ font-size:10pt; color:var(--teal); margin:0 0 2mm; }
.lg{ display:flex; gap:6mm; }
.lg div{ font-size:8.5pt; color:var(--faded); text-align:center; }
.lg .s{ display:block; font-size:13mm; line-height:1.1; font-family:'{TFONT}',serif; }
.foot{ margin-top:12mm; font-family:'JetBrains Mono',monospace; font-size:8pt;
       letter-spacing:.14em; color:var(--faded); }
.pf{ display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace;
     font-size:7.5pt; letter-spacing:.1em; color:#B9AE9B; margin-top:3mm;
     border-top:0.3mm solid var(--line-soft); padding-top:1.5mm; }
"""

def page_head(pair, title):
    c = C(pair); g = G(pair)
    f = g["fill"] / 0.96                  # block occupies ~0.96 of the em
    css = (STYLE.replace("{GS}",  f"{15.0*f:.2f}mm")
                .replace("{GSW}", f"{12.0*f:.2f}mm")
                .replace("{GSS}", f"{11.0*f:.2f}mm")
                .replace("{TFONT}", g["font"])
                .replace("{SFONT}", SOURCE_FONTS[c["source_iso"]]))
    return f"""<!DOCTYPE html>
<html lang="{c['source_iso']}">
<head>
<meta charset="UTF-8"/>
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{fonts_url(SOURCE_FONTS[c['source_iso']], g['font'])}" rel="stylesheet"/>
<style>{css}</style>
</head>
<body>
"""

def cellhtml(t, cls): return f'<span class="cell {cls}">{t}</span>'
def gap(): return '<span class="cell gap"></span>'
def grid(cells_html, lab_l="", lab_r="", cls=""):
    lab = (f'<div class="rowlabel"><span>{lab_l}</span><span>{lab_r}</span></div>'
           if (lab_l or lab_r) else "")
    return f'{lab}<div class="grid {cls}">{cells_html}</div>'
def n_of(t, n, cls): return "".join(cellhtml(t, cls) for _ in range(n))
def footer(pair, book, n):
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span>BHASHASETU &middot; {C(pair)["sub"]} &middot; {D(pair, n)}</span></div>')

def cover(pair, bno, native, title, sub):
    c = C(pair); u = c["ui"]
    ol = "".join(f"<li>{r}</li>" for r in c.get("rules", []))
    rules_html = (f'<div class="rules"><h2>{c.get("rules_head","")}</h2><ol>{ol}</ol></div>'
                  if ol else "")
    s = native[0]
    lg = f"""<div class="legend"><h3>{u["legend"]}</h3><div class="lg">
      <div><span class="s ko t-model">{s}</span>{u["model"]}</div>
      <div><span class="s ko t-trace">{s}</span>{u["grey"]}</div>
      <div><span class="s ko t-out">{s}</span>{u["hollow"]}</div>
      <div><span class="s ko t-faint">{s}</span>{u["faint"]}</div></div></div>"""
    return f"""<div class="sheet cover">
  <div class="kicker">{c["book"]} {bno}</div>
  <h1><span class="ko">{native}</span>{title}</h1>
  <p class="sub">{sub}</p>
  {rules_html}
  {lg}
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""

def jamo_sheet(pair, book, n, r):
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="big">{r["t"]}</div>
      <div class="meta"><div class="eq">= <b>{r["eq"]}</b></div><div class="tr">{r["roman"]}</div>
        <div class="ex"><span class="ko">{r["ex"]}</span> &middot; {r["gloss"]}</div></div></div>
    <div class="ph-r"><div class="grp">{r["group"]}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  <div class="note"><b>{U(pair,"stroke_order")}</b> &middot; {r.get("note","")}</div>
  {grid(n_of(r["t"],8,'t-trace'), U(pair,"trace"), U(pair,"times"))}
  {grid(n_of(r["t"],8,'t-out'), U(pair,"fill"), U(pair,"times"))}
  {grid(cellhtml(r["t"],'t-model')+n_of(r["t"],3,'t-faint')+n_of('',4,''),
        U(pair,"start_given"), U(pair,"finish_row"))}
  {grid(n_of('',8,''), U(pair,"self"), U(pair,"fill_row"))}
  {footer(pair, book, n)}
</div>"""

def block_sheet(pair, book, n, r, head, hint):
    parts = r.get("parts","")
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="big">{r["t"]}</div>
      <div class="meta"><div class="eq">= <b>{r["eq"]}</b></div><div class="tr">{r["roman"]}</div>
        <div class="ex"><b>{U(pair,"parts_head")}:</b> <span class="ko">{parts}</span></div>
        <div class="ex"><span class="ko">{r["ex"]}</span> &middot; {r["gloss"]}</div></div></div>
    <div class="ph-r"><div class="grp">{r["group"]}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  <div class="note"><b>{head}</b> &middot; {r.get("note", hint)}</div>
  {grid(n_of(r["t"],8,'t-trace'), U(pair,"trace"), U(pair,"times"))}
  {grid(n_of(r["t"],8,'t-out'), U(pair,"fill"), U(pair,"assemble"))}
  {grid(cellhtml(r["t"],'t-model')+n_of(r["t"],3,'t-faint')+n_of('',4,''),
        U(pair,"start_given"), U(pair,"finish_row"))}
  {grid(n_of('',8,''), U(pair,"self"), U(pair,"fill_row"))}
  {footer(pair, book, n)}
</div>"""

def blank_cells(n):
    """Empty practice cells. These keep their border and cross-hairs: this is the row the
       learner actually writes in, so it must look like a place to write."""
    return "".join(cellhtml("", "") for _ in range(n))

def syl_cells(text, cls):
    """One cell per syllable. A space becomes an empty, borderless cell, because on
       practice paper the gap between words is itself a square."""
    return "".join(gap() if ch == " " else cellhtml(ch, cls) for ch in text)

def words_sheet(pair, book, n, group, items):
    blocks = ""
    for w, gloss in items:
        blocks += grid(syl_cells(w,'t-model'),
                       f'<span class="ko" style="font-size:12pt">{w}</span> &nbsp;=&nbsp; <b>{gloss}</b>',
                       U(pair,"model"), 'w')
        blocks += grid(syl_cells(w,'t-trace'), '', U(pair,"trace"), 'w')
        blocks += grid(blank_cells(len(w)), '', U(pair,"self"), 'w')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta"><div class="eq" style="font-size:15pt"><b>{group}</b></div>
      <div class="ex">{U(pair,"words_hint")}</div></div></div>
    <div class="ph-r"><div class="grp">{U(pair,"box_hint")}</div>
      <div class="num">{D(pair,n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

def sentence_sheet(pair, book, n, items):
    blocks = ""
    for tgt, gloss in items:
        blocks += f'<div class="rowlabel"><span><b>{gloss}</b></span><span>{U(pair,"sent_seq")}</span></div>'
        blocks += grid(syl_cells(tgt,'t-model'), '', '', 's')
        blocks += grid(syl_cells(tgt,'t-trace'), '', '', 's')
        blocks += grid(blank_cells(len(tgt.replace(' ',''))), '', U(pair,"self"), 's')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta"><div class="eq" style="font-size:15pt"><b>{U(pair,"sent_head")}</b></div>
      <div class="ex">{U(pair,"sent_hint")}</div></div></div>
    <div class="ph-r"><div class="grp">{U(pair,"box")}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

def build(pair):
    c = C(pair); L = c["letters"]; bks = c["books"]
    out = os.path.join(HERE, pair); os.makedirs(out, exist_ok=True)
    made = []
    def bl(i): return f'{c["book"]} {D(pair,i+1)} · {bks[i]["label"]}'
    def cov(i): return cover(pair, D(pair,i+1), bks[i]["native"], bks[i]["label"],
                             bks[i].get("bridge",""))

    for i, key in ((0,"jaeum"), (1,"moeum")):
        p = [cov(i)]
        for n, r in enumerate(L[key], 1):
            p.append(jamo_sheet(pair, bl(i), n, r))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    for i, key, head, hint in ((2,"moa",U(pair,"assemble"),U(pair,"box_hint")),
                               (3,"batchim",U(pair,"batchim_head"),U(pair,"batchim_hint"))):
        p = [cov(i)]
        for n, r in enumerate(L[key], 1):
            p.append(block_sheet(pair, bl(i), n, r, head, hint))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    for i, key in ((4,"words1"), (5,"words2")):
        p = [cov(i)]; n = 1
        for group, its in c[key].items():
            for k in range(0, len(its), 4):
                p.append(words_sheet(pair, bl(i), n, group, [tuple(x) for x in its[k:k+4]])); n += 1
        made.append((bks[i]["slug"], bks[i]["label"], p))

    for i, key in ((6,"sent1"), (7,"sent2")):
        p = [cov(i)]; its = c[key]
        for k in range(0, len(its), 2):
            p.append(sentence_sheet(pair, bl(i), k//2+1, [tuple(x) for x in its[k:k+2]]))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    rows = ""
    for slug, title, pages in made:
        fn = f"{slug}.html"
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write(page_head(pair, f'{title} - {c["sub"]}') + "\n".join(pages) + "\n</body>\n</html>")
        print(f"  {fn:<24} {len(pages):>3} pages")
        rows += (f'<tr><td><b>{title}</b></td><td>{D(pair,len(pages))}</td>'
                 f'<td><a href="{slug}.pdf">PDF</a></td><td><a href="{fn}">HTML</a></td></tr>')
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_head(pair, f'{c["title"]} - {c["sub"]}') +
                f"""<div style="max-width:150mm;margin:20mm auto;font-size:11pt">
        <h1 style="font-size:20pt">{c["title"]}</h1>
        <p style="color:#6B5B48;line-height:1.7">{c["index_blurb"]}<br/>{c["print_note"]}</p>
        <table style="width:100%;border-collapse:collapse;margin-top:8mm">{rows}</table></div>
        </body></html>""")
    total = sum(len(p) for _,_,p in made)
    print(f"  total {total} pages")
    return total

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = sorted(f[:-5] for f in os.listdir(DATA_DIR)
                      if f.endswith(".json") and not f.startswith("_"))
    for pr in args:
        fp = os.path.join(DATA_DIR, f"{pr}.json")
        if not os.path.exists(fp): print(f"{pr}: no data file, skipped"); continue
        if json.load(open(fp, encoding="utf-8")).get("target_iso") not in SCRIPTS: continue
        miss = audit(pr)
        if miss:
            print(f"{pr}: NOT BUILT, the pair file is missing:")
            for m in miss: print(f"    - {m}")
            continue
        print(f"{pr}:"); build(pr)
