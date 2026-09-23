#!/usr/bin/env python3
"""
Handwriting workbooks for Perso-Arabic targets (Urdu): right to left, one solid
baseline, and letters whose shape depends on where they sit in the word.

Everything source-language lives in worksheets/data/{pair}.json, written by the course
agent for that pair. Positional forms are NOT hardcoded: they are produced with ZWJ
(U+200D) so the font shapes them, which is the only way to get Nastaliq right.

  python3 gen_urdu.py                     # every Urdu-target pair with a data file
  python3 gen_urdu.py telugu_to_urdu      # one pair
"""
import os, html, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

REQUIRED_UI = ["trace","fill","self","times","times6","start_given","start_given_short",
               "finish_row","fill_row","in_word","then_self","model","grey","hollow",
               "faint","legend","rtl_hint","joins_yes","joins_no","pos_iso","pos_fin",
               "pos_med","pos_ini","forms_head","forms_grp","forms_hint","forms_note",
               "no_join_tag","join_head","join_hint","join_grp","harakat_grp",
               "words_hint","sent_seq","sent_head","sent_hint"]
REQUIRED_TOP = ["pair","source_iso","target_iso","sub","title","book","digits",
                "words_word","sent_word","index_blurb","print_note","books","letters",
                "words1","words2","sent1","sent2"]

_CACHE = {}; CUR = None

def C():
    return _CACHE[CUR]
def U(k):
    return C()["ui"][k]
def BOOK(i):
    return C()["books"][i]
def D(n):
    d = C()["digits"]
    return "".join(d[int(ch)] for ch in str(n))

def load(pair):
    global CUR
    if pair not in _CACHE:
        with open(os.path.join(DATA_DIR, f"{pair}.json"), encoding="utf-8") as f:
            _CACHE[pair] = json.load(f)
    CUR = pair
    return _CACHE[pair]

def audit(pair):
    c = load(pair); miss = []
    miss += [f"top-level: {k}" for k in REQUIRED_TOP if k not in c]
    miss += [f"ui: {k}" for k in REQUIRED_UI if k not in c.get("ui", {})]
    if len(c.get("books", [])) != 8:
        miss.append(f'books: expected 8, found {len(c.get("books", []))}')
    if len(c.get("digits", "")) != 10:
        miss.append("digits: need exactly 10 characters")
    for key in ("letters", "harakat", "joining"):
        if not c.get("letters", {}).get(key):
            miss.append(f"letters.{key}")
    for r in c.get("letters", {}).get("letters", []):
        if "joins_left" not in r:
            miss.append(f'letters.letters: {r.get("t","?")} has no joins_left flag'); break
    n1 = sum(len(v) for v in c.get("words1", {}).values())
    n2 = sum(len(v) for v in c.get("words2", {}).values())
    if n1 < 50: miss.append(f"words1: {n1} words, the brief asks for 50 to 60")
    if n2 < 50: miss.append(f"words2: {n2} words, the brief asks for 50 to 60")
    if len(c.get("sent1", [])) < 25: miss.append(f'sent1: {len(c.get("sent1",[]))} sentences, need 25 to 30')
    if len(c.get("sent2", [])) < 25: miss.append(f'sent2: {len(c.get("sent2",[]))} sentences, need 25 to 30')
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
    if "\u2014" in json.dumps(c, ensure_ascii=False):
        miss.append("em-dash characters present; this project uses '-'")
    return miss

ZWJ  = "‍"

def forms(ch, joins_left=True):
    """The four positional shapes, composed with ZWJ rather than hardcoded."""
    if not joins_left:                      # ا د ڈ ذ ر ڑ ز ژ و join only to the right
        return [ch, ZWJ + ch, ZWJ + ch, ch]
    return [ch, ZWJ + ch, ZWJ + ch + ZWJ, ch + ZWJ]

# ---------------------------------------------------------------- letters
STYLE = """
:root{
  --base: 17mm;         /* the baseline - letters SIT on this */
  --gs:   15mm;         /* practice font size */
  --asc-ratio:  0.714;  /* ا ل ک reach this far above the baseline */
  --desc-ratio: 0.420;  /* م and the Nastaliq cascade reach this far below */
  --x-ratio:    0.310;  /* x-height of ب س ر, drawn as a faint guide */
  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --teal:#1F4D4A;
  --line:#9aa8b8; --line-soft:#c7d0da;
  --trace:#c9c9c9; --outline:#bdbdbd; --faint:#e3e3e3;
}
@page{ size:A4; margin:11mm 10mm 12mm 10mm; }
*{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
html,body{ margin:0; padding:0; background:#fff; }
body{ font-family:'{SFONT}',serif; color:var(--ink); font-size:10pt; direction:ltr; }
.ur{ font-family:'Noto Nastaliq Urdu',serif; direction:rtl; unicode-bidi:isolate; }

.sheet{ page-break-after:always; break-after:page; position:relative; min-height:262mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }

.ph{ display:flex; align-items:flex-end; justify-content:space-between;
     border-bottom:0.5mm solid var(--ink); padding-bottom:2mm; margin-bottom:3mm; }
.ph-l{ display:flex; align-items:flex-end; gap:6mm; }
.ph .big{ font-size:24mm; line-height:1.5; }
.ph .meta{ padding-bottom:2mm; }
.ph .eq{ font-size:13pt; } .ph .eq b{ color:var(--sindoor); }
.ph .nm{ font-size:11pt; color:var(--teal); }
.ph .ex{ font-size:10pt; color:var(--faded); margin-top:1mm; }
.ph-r{ text-align:right; padding-bottom:2mm; }
.ph-r .grp{ font-size:9pt; color:var(--faded); }
.ph-r .num{ font-size:9pt; color:var(--faded); letter-spacing:.14em; }

.note{ font-size:9.5pt; line-height:1.6; color:var(--ink); margin:0 0 3mm;
       padding:2mm 3mm; background:rgba(31,77,74,0.06); border-right:2mm solid var(--teal); }
.note b{ color:var(--sindoor); }

.rowlabel{ font-size:8.5pt; color:var(--faded); margin:0 0 0.8mm;
           display:flex; justify-content:space-between; align-items:baseline; }
.rowlabel b{ color:var(--teal); font-weight:600; }
.row{ position:relative; margin-bottom:2.4mm;
      --asc:  calc(var(--base) - var(--asc-ratio) * var(--gs));
      --xh:   calc(var(--base) - var(--x-ratio) * var(--gs));
      --desc: calc(var(--base) + var(--desc-ratio) * var(--gs));
      height: calc(var(--desc) + 2mm); }
.row .ln{ position:absolute; left:0; right:0; height:0; }
.ln.a{ top:var(--asc);  border-top:0.25mm dashed var(--line-soft); }
.ln.x{ top:var(--xh);   border-top:0.2mm dotted #dde3ea; }
.ln.b{ top:var(--base); border-top:0.45mm solid var(--line); }
.ln.d{ top:var(--desc); border-top:0.25mm dashed var(--line-soft); }
/* right-to-left: cells run from the right edge; the strut pins the baseline */
.row .cells{ position:absolute; left:0; right:0; top:0;
             display:flex; flex-direction:row; justify-content:flex-start;
             direction:rtl; line-height:0; }
.st{ display:inline-block; width:0; height:var(--base); vertical-align:baseline; }
.row .c{ font-family:'Noto Nastaliq Urdu',serif; font-size:var(--gs); line-height:0;
         flex:0 0 auto; padding-left:7mm; text-align:center; }
/* word and joining rows: a tighter band so eight rows fit one page */
.row.wide{ --base:13mm; --gs:12mm; }
.row.wide .c{ padding-left:12mm; }
.row.sent{ --gs:11mm; }
.row.sent .cells{ display:block; }
.row.sent .c{ display:block; padding:0; text-align:right; }

.t-model{ color:var(--ink); } .t-trace{ color:var(--trace); }
.t-out{ color:transparent; -webkit-text-stroke:0.25mm var(--outline); }
.t-faint{ color:var(--faint); }

.forms{ display:flex; gap:3mm; margin:0 0 3mm; direction:rtl; }
.formbox{ border:0.3mm dashed var(--line-soft); border-radius:1mm;
          padding:1mm 4mm 0.5mm; text-align:center; flex:1; }
.formbox .g{ font-family:'Noto Nastaliq Urdu',serif; font-size:13mm; line-height:2; }
.formbox .cap{ font-size:8pt; color:var(--faded); direction:ltr; }
.formbox .cap b{ color:var(--teal); }

.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-size:10pt; letter-spacing:.24em; color:var(--sindoor); }
.cover h1{ font-size:28pt; margin:6mm 0 2mm; line-height:1.3; }
.cover h1 .ur{ display:block; font-size:32pt; margin-bottom:5mm; line-height:2; }
.cover .sub{ font-size:12pt; color:var(--faded); max-width:140mm; margin:0 auto; line-height:1.75; }
.rules{ text-align:left; max-width:152mm; margin:10mm auto 0; }
.rules h2{ font-size:12pt; margin:0 0 3mm; color:var(--sindoor); }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ margin-bottom:3mm; line-height:1.7; font-size:10.5pt; }
.rules li b{ color:var(--teal); }
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

def page_head(title):
    sfont = SOURCE_FONTS[C()["source_iso"]]
    css = STYLE.replace("{SFONT}", sfont)
    links = fonts_url(sfont, "Noto Nastaliq Urdu")
    return f"""<!DOCTYPE html>
<html lang="{C()["source_iso"]}">
<head>
<meta charset="UTF-8"/>
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{links}" rel="stylesheet"/>
<style>{css}</style>
</head>
<body>
"""

def row(cells_html, lab_l, lab_r="", cls=""):
    return f"""<div class="rowlabel"><span>{lab_l}</span><span>{lab_r}</span></div>
<div class="row {cls}">
  <div class="ln a"></div><div class="ln x"></div><div class="ln b"></div><div class="ln d"></div>
  <div class="cells">{cells_html}</div>
</div>"""

def one(txt, cls):
    return f'<span class="c {cls}"><i class="st"></i>{txt}</span>'
def cells(txt, n, cls):
    return "".join(one(txt, cls) for _ in range(n))
def footer(book, n):
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span>BHASHASETU &middot; {C()["sub"]} &middot; {D(n)}</span></div>')

def letter_sheet(book, n, ch, name, eq, ex, gloss, joins, group):
    iso, fin, med, ini = forms(ch, joins)
    jn = (U("joins_yes") if joins else
          U("joins_no"))
    fb = "".join(
        f'<div class="formbox"><div class="g ur">{g}</div><div class="cap"><b>{i}</b> {c}</div></div>'
        for i, (g, c) in enumerate([(iso,U("pos_iso")),(fin,U("pos_fin")),(med,U("pos_med")),(ini,U("pos_ini"))], 1))
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big ur">{ch}</div>
      <div class="meta">
        <div class="nm">{name}</div>
        <div class="eq">= <b>{eq}</b></div>
        <div class="ex"><span class="ur">{ex}</span> &middot; {gloss}</div>
      </div>
    </div>
    <div class="ph-r"><div class="grp">{group}</div><div class="num">{D(n)}</div></div>
  </div>
  <div class="note">{jn}</div>
  <div class="forms">{fb}</div>
  {row(cells(iso,6,'t-trace'), U("trace"), U("rtl_hint"))}
  {row(cells(iso,6,'t-out'), U("fill"), U("times6"))}
  {row(one(iso,'t-model')+one(iso,'t-faint'), U("start_given"), U("finish_row"))}
  {row('', U("self"), U("fill_row"))}
  {row(one(ex,'t-model')+one(ex,'t-trace'), f'{U("in_word")} - <span class="ur">{ex}</span> ({gloss})', U("then_self"), 'wide')}
  {footer(book, n)}
</div>"""

def forms_sheet(book, n, items):
    blocks = ""
    for ch, name, eq, ex, gloss, joins, _g in items:
        iso, fin, med, ini = forms(ch, joins)
        seq = [(ini,U("pos_ini")),(med,U("pos_med")),(fin,U("pos_fin")),(iso,U("pos_iso"))]
        lab = (f'<span class="ur" style="font-size:12pt">{ch}</span> &nbsp; {name} &nbsp; = &nbsp; <b>{eq}</b>'
               + ("" if joins else f' &nbsp; <b style="color:#A83024">{U("no_join_tag")}</b>'))
        blocks += row("".join(one(g,'t-model')+one(g,'t-trace') for g,_ in seq), lab, U("forms_head"), 'wide')
        blocks += row('', '', U("self"), 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>{U("forms_head")}</b></div>
      <div class="ex">{U("forms_hint")}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{U("forms_grp")}</div><div class="num">{D(n)}</div></div>
  </div>
  <div class="note">{U("forms_note")}</div>
  {blocks}
  {footer(book, n)}
</div>"""

def harakat_sheet(book, n, item):
    shown, name, bn, note = item
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big ur">{shown}</div>
      <div class="meta"><div class="nm">{name}</div><div class="eq">= <b>{bn}</b></div></div>
    </div>
    <div class="ph-r"><div class="grp">{U("harakat_grp")}</div><div class="num">{D(n)}</div></div>
  </div>
  <div class="note">{note}</div>
  {row(cells(shown,6,'t-trace'), U("trace"), U("rtl_hint"))}
  {row(cells(shown,6,'t-out'), U("fill"), U("times6"))}
  {row(one(shown,'t-model')+one(shown,'t-faint'), U("start_given_short"), U("finish_row"))}
  {row('', U("self"), '')}
  {row('', U("self"), '')}
  {footer(book, n)}
</div>"""

def joining_sheet(book, n, items):
    blocks = ""
    for w, gloss, note in items:
        blocks += row(one(w,'t-model')+one(w,'t-trace')+one(w,'t-out'),
                      f'<span class="ur" style="font-size:13pt">{w}</span> &nbsp; <b>{gloss}</b> &nbsp; <span style="color:#6B5B48">{note}</span>',
                      U("rtl_hint"), 'wide')
        blocks += row('', '', U("self"), 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>{U("join_head")}</b></div>
      <div class="ex">{U("join_hint")}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{U("join_grp")}</div><div class="num">{D(n)}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

def words_sheet(book, n, group, items):
    blocks = ""
    for w, gloss in items:
        blocks += row(one(w,'t-model')+one(w,'t-trace'),
                      f'<span class="ur" style="font-size:13pt">{w}</span> &nbsp; = &nbsp; <b>{gloss}</b>',
                      U("rtl_hint"), 'wide')
        blocks += row('', '', U("self"), 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>{group}</b></div>
      <div class="ex">{U("words_hint")}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{C()["words_word"]}</div><div class="num">{D(n)}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

def sentence_sheet(book, n, items):
    blocks = ""
    for ur, bn in items:
        blocks += f'<div class="rowlabel"><span><b>{bn}</b></span><span>{U("sent_seq")}</span></div>'
        blocks += row(one(ur,'t-model'), '', '', 'sent')
        blocks += row(one(ur,'t-trace'), U("trace"), '', 'sent')
        blocks += row('', U("self"), '', 'sent')
        blocks += row('', '', '', 'sent')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>{U("sent_head")}</b></div>
      <div class="ex">{U("sent_hint")}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{C()["sent_word"]}</div><div class="num">{D(n)}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

# ---------------------------------------------------------------- build
def cover(bno, native, title, sub):
    c = C(); u = c["ui"]
    ol = "".join(f"<li>{r}</li>" for r in c.get("rules", []))
    rules_html = (f'<div class="rules"><h2>{c.get("rules_head","")}</h2><ol>{ol}</ol></div>'
                  if ol else "")
    lg = f"""<div class="legend"><h3>{u["legend"]}</h3><div class="lg">
      <div><span class="s ur t-model">{native[0]}</span>{u["model"]}</div>
      <div><span class="s ur t-trace">{native[0]}</span>{u["grey"]}</div>
      <div><span class="s ur t-out">{native[0]}</span>{u["hollow"]}</div>
      <div><span class="s ur t-faint">{native[0]}</span>{u["faint"]}</div></div></div>"""
    return f"""<div class="sheet cover">
  <div class="kicker">{c["book"]} {bno}</div>
  <h1><span class="ur">{native}</span>{title}</h1>
  <p class="sub">{sub}</p>
  {rules_html}
  {lg}
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""

# ---------------------------------------------------------------- build
def build(pair):
    c = load(pair); L = c["letters"]; bks = c["books"]
    out = os.path.join(HERE, pair); os.makedirs(out, exist_ok=True)
    made = []
    def cov(i): 
        b = bks[i]
        return cover(D(i + 1), b["native"], b.get("cover_title", b["label"]),
                     b.get("bridge", ""))
    def bl(i):
        return f'{c["book"]} {D(i+1)} \u00b7 {bks[i]["label"]}'

    # 1: the letters
    p = [cov(0)]
    for n, r in enumerate(L["letters"], 1):
        p.append(letter_sheet(bl(0), n, r["t"], r["name"], r["sound"], r["ex"],
                              r["gloss"], r["joins_left"], r["group"]))
    made.append((bks[0]["slug"], bks[0]["label"], p))

    # 2: the four positional forms, for the letters that join
    p = [cov(1)]
    joiners = [r for r in L["letters"] if r["joins_left"]]
    for n, k in enumerate(range(0, len(joiners), 3), 1):
        items = [(r["t"], r["name"], r["sound"], r["ex"], r["gloss"],
                  r["joins_left"], r["group"]) for r in joiners[k:k+3]]
        p.append(forms_sheet(bl(1), n, items))
    made.append((bks[1]["slug"], bks[1]["label"], p))

    # 3: the marks
    p = [cov(2)]
    for n, r in enumerate(L["harakat"], 1):
        p.append(harakat_sheet(bl(2), n, (r["ex"], r["name"], r["sound"], r["note"])))
    made.append((bks[2]["slug"], bks[2]["label"], p))

    # 4: joined groups
    p = [cov(3)]
    jn = [(r["t"], r["read"], r["note"]) for r in L["joining"]]
    for n, k in enumerate(range(0, len(jn), 2), 1):
        p.append(joining_sheet(bl(3), n, jn[k:k+2]))
    made.append((bks[3]["slug"], bks[3]["label"], p))

    # 5 and 6: words
    for i, key in ((4, "words1"), (5, "words2")):
        p = [cov(i)]; n = 1
        for group, its in c[key].items():
            for k in range(0, len(its), 4):
                p.append(words_sheet(bl(i), n, group, [tuple(x) for x in its[k:k+4]])); n += 1
        made.append((bks[i]["slug"], bks[i]["label"], p))

    # 7 and 8: sentences
    for i, key in ((6, "sent1"), (7, "sent2")):
        p = [cov(i)]; its = c[key]
        for k in range(0, len(its), 2):
            p.append(sentence_sheet(bl(i), k//2 + 1, [tuple(x) for x in its[k:k+2]]))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    rows = ""
    for slug, title, pages in made:
        fn = f"{slug}.html"
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write(page_head(f'{title} - {c["sub"]}') + "\n".join(pages) + "\n</body>\n</html>")
        print(f"  {fn:<24} {len(pages):>3} pages")
        rows += (f'<tr><td><b>{title}</b></td><td>{D(len(pages))}</td>'
                 f'<td><a href="{slug}.pdf">PDF</a></td><td><a href="{fn}">HTML</a></td></tr>')
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_head(f'{c["title"]} - {c["sub"]}') +
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
        if not os.path.exists(fp): print(f"{pr}: no data file, skipped"); continue
        if json.load(open(fp, encoding="utf-8")).get("target_iso") != "ur": continue
        miss = audit(pr)
        if miss:
            print(f"{pr}: NOT BUILT, the pair file is missing:")
            for m in miss: print(f"    - {m}")
            continue
        print(f"{pr}:"); build(pr)
