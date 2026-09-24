#!/usr/bin/env python3
"""
Handwriting workbooks for Devanagari targets (Hindi, and Marathi when it arrives).

Devanagari hangs from a headline, so the geometry differs from the baseline-sitting
scripts in gen_brahmic.py. Everything source-language lives in worksheets/data/{pair}.json.

This file used to hold two pairs at once, with a Telugu override map layered over Bengali
defaults. That layering leaked: the word-group headings and the consonant varga labels had
no Telugu override at all, so the shipped telugu_to_hindi workbooks carried 200 runs of
Bengali text. One pair per file makes that class of bug impossible.

  python3 gen_deva.py                    # every Devanagari-target pair with a data file
  python3 gen_deva.py telugu_to_hindi    # one pair
"""
import os, html, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

SOURCE_FONTS = {
 "bn":"Noto Serif Bengali",   "hi":"Noto Serif Devanagari", "mr":"Noto Serif Devanagari",
 "te":"Noto Serif Telugu",    "ta":"Noto Serif Tamil",      "kn":"Noto Serif Kannada",
 "ml":"Noto Serif Malayalam", "pa":"Noto Serif Gurmukhi",   "ur":"Noto Nastaliq Urdu",
}
def _fam(n):
    w = "wght@400;500" if "Nastaliq" in n else "wght@400;500;600;700"
    return "family=" + n.replace(" ", "+") + ":" + w
def fonts_url(*names):
    seen=[]
    for n in names:
        if n and n not in seen: seen.append(n)
    return ("https://fonts.googleapis.com/css2?" + "&".join(_fam(n) for n in seen)
            + "&family=JetBrains+Mono:wght@400;500&display=swap")

REQUIRED_UI = ["vowels","consonants","matra","conj","words","sentences","trace","fill",
               "self","start_given","sent_flow","matra_rule","letter_note","nukta_note",
               "nukta_note_known"]
REQUIRED_TOP = ["pair","source_iso","target_iso","sub","title","book","digits","words_word",
                "sent_word","index_blurb","print_note","books","letters","words1","words2",
                "sent1","sent2","rules","conj_rules"]

SHARED_PUNCT = {0x0964, 0x0965}   # danda and double danda: common to all Indic scripts

_CACHE = {}
def C(pair):
    if pair not in _CACHE:
        with open(os.path.join(DATA_DIR, f"{pair}.json"), encoding="utf-8") as f:
            _CACHE[pair] = json.load(f)
    return _CACHE[pair]
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
    for k in ("vowels","cons","nukta","matra","conjuncts"):
        if not c.get("letters",{}).get(k): miss.append(f"letters.{k}")
    import re as _re
    plain = [_re.sub(r"<[^>]+>","",r) for r in c.get("rules",[])]
    if plain:
        tot, longest = sum(len(x) for x in plain), max(len(x) for x in plain)
        if tot > 1200 or longest > 280:
            miss.append(f"rules too long for the cover: {tot} chars, longest {longest}")
    # the leak this rewrite exists to kill: source-language text from ANOTHER script
    RANGES = {"hi":(0x900,0x97F),"bn":(0x980,0x9FF),"te":(0xC00,0xC7F),"kn":(0xC80,0xCFF),"ta":(0xB80,0xBFF),
              "ml":(0xD00,0xD7F),"pa":(0xA00,0xA7F)}
    iso = c.get("source_iso")
    own = {SCRIPTS.get(iso, {}).get("script", iso),
           SCRIPTS.get(c.get("target_iso"), {}).get("script", c.get("target_iso"))}
    blob = json.dumps({k:v for k,v in c.items() if k != "letters"}, ensure_ascii=False)
    blob += json.dumps(c.get("letters",{}).get("cons",[]), ensure_ascii=False)
    for other,(lo,hi) in RANGES.items():
        if other in own or other == iso: continue
        hits = [ch for ch in blob if lo <= ord(ch) <= hi and ord(ch) not in SHARED_PUNCT]
        if hits:
            miss.append(f"{len(hits)} characters of {other} script in a {iso} pair file "
                        f"(e.g. {''.join(hits[:6])}); labels must be in the source language")
    n1 = sum(len(v) for v in c.get("words1",{}).values())
    n2 = sum(len(v) for v in c.get("words2",{}).values())
    if n1 < 50: miss.append(f"words1: {n1} words, the brief asks for 50 to 60")
    if n2 < 50: miss.append(f"words2: {n2} words, the brief asks for 50 to 60")
    if "\u2014" in json.dumps(c, ensure_ascii=False):
        miss.append("em-dash characters present; this project uses '-'")
    return miss


# Geometry is a property of the TARGET SCRIPT, not the pair, so every pair sharing a target
# reuses it. These three scripts all hang their letters from a headline, which is why they
# share a generator; the baseline-sitting scripts live in gen_brahmic.py.
#   asc = height of a bare letter above the baseline, i.e. where the headline sits
#   top = how far signs rise ABOVE that headline (a guide line only, it does not affect fit)
#   bot = how far signs drop below the baseline (this DOES set the row height)
# All fractions of the font size, measured with canvas TextMetrics.
# Devanagari's numbers are the originals and are left exactly as shipped: they are proved by
# 169-page books. Re-measuring them in 2026-09 reproduced asc 0.642 and bot 0.290 exactly,
# which is what validated the method for the two scripts added below.
SCRIPTS = {
 "hi": {"font":"Noto Serif Devanagari", "asc":0.642, "top":0.283, "bot":0.290,
        "script":"hi", "sample":"\u0915", "others":("\u0916","\u0917")},
 "mr": {"font":"Noto Serif Devanagari", "asc":0.642, "top":0.283, "bot":0.290,
        "script":"hi", "sample":"\u0915", "others":("\u0916","\u0917")},
 "bn": {"font":"Noto Serif Bengali",    "asc":0.935, "top":0.039, "bot":0.353,
        "script":"bn", "sample":"\u0995", "others":("\u0996","\u0997")},
 "pa": {"font":"Noto Serif Gurmukhi",   "asc":0.577, "top":0.280, "bot":0.295,
        "script":"pa", "sample":"\u0A15", "others":("\u0A16","\u0A17")},
}

STYLE = """
:root{
  --head:  9mm;        /* SHIRO-REKHA - letters hang from here   */
  --base:  19mm;       /* baseline - letters sit here            */
  /* Noto Serif Devanagari metrics, measured with canvas TextMetrics
     (see calibrate_font.html). Fractions of the font size, from the baseline:
       bare letter  shirorekha ....... 0.642 up
       matras above ..................  0.925 up
       matras below ..................  0.290 down */
  --asc-ratio:  {ASC};
  --top-ratio:  {TOP};
  --bot-ratio:  {BOT};

  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --ochre:#B8802D; --teal:#1F4D4A;
  --line:#9aa8b8; --line-soft:#c7d0da;
  --trace:#c9c9c9; --outline:#bdbdbd; --faint:#e3e3e3;
}
@page{ size:A4; margin:11mm 10mm 12mm 10mm; }
*{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
html,body{ margin:0; padding:0; background:#fff; }
body{ font-family:'{SRC_FONT}',serif; color:var(--ink); font-size:10pt; }
.deva{ font-family:'{TFONT}',serif; }

.sheet{ page-break-after:always; break-after:page; position:relative; min-height:262mm; }
/* Headroom ONLY on sheets that open with the big header glyph (letter and matra sheets).
   Its line-height is 0.95, so tall letters (Bengali independent i, ii and u, Devanagari ii, Gurmukhi iri) rise
   above their line box, and as the first thing on a sheet that ink printed in the previous
   page's bottom margin. Applying it to every sheet instead pushed the dense Gurmukhi
   conjunct sheets onto a second page (book 4 went from 10 pages to 18). */
.sheet.tall{ padding-top:5mm; min-height:257mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }

.ph{ display:flex; align-items:flex-end; justify-content:space-between;
     border-bottom:0.5mm solid var(--ink); padding-bottom:2mm; margin-bottom:3mm; }
.ph-l{ display:flex; align-items:flex-end; gap:5mm; }
.ph .big{ font-size:22mm; line-height:0.95; }
.ph .meta{ padding-bottom:1.5mm; }
.ph .eq{ font-size:13pt; color:var(--ink); }
.ph .eq b{ color:var(--sindoor); }
.ph .tr{ font-family:'JetBrains Mono',monospace; font-size:9pt; color:var(--sindoor); letter-spacing:.04em; }
.ph .ex{ font-size:10pt; color:var(--faded); margin-top:1mm; }
.ph-r{ text-align:right; padding-bottom:1.5mm; }
.ph-r .grp{ font-size:9pt; color:var(--faded); }
.ph-r .num{ font-size:9pt; color:var(--faded); letter-spacing:.14em; }

.steps{ display:flex; gap:4mm; align-items:flex-end; margin:0 0 3mm; }
.step{ border:0.3mm dashed var(--line-soft); border-radius:1mm; padding:1.5mm 3mm 1mm; text-align:center; }
.step .g{ font-size:16mm; line-height:1.05; position:relative; display:inline-block; }
.step .mask{ position:absolute; left:-1mm; right:-1mm; top:0; height:2.6mm; background:#fff; }
.step .cap{ font-size:8pt; color:var(--faded); margin-top:0.5mm; }
.step .cap b{ color:var(--teal); }
.steps .note{ font-size:9pt; color:var(--ink); line-height:1.5; padding-bottom:2mm; flex:1; }
.steps .note b{ color:var(--sindoor); }

.rowlabel{ font-size:8.5pt; color:var(--faded); margin:0 0 0.8mm;
           display:flex; justify-content:space-between; align-items:baseline; }
.rowlabel b{ color:var(--teal); font-weight:600; }
.row{ position:relative; margin-bottom:2.2mm;
      --gs:   calc((var(--base) - var(--head)) / var(--asc-ratio));
      --asc:  calc(var(--head) - var(--top-ratio) * var(--gs));
      --desc: calc(var(--base) + var(--bot-ratio) * var(--gs));
      height: calc(var(--desc) + 1.5mm); }
.row .ln{ position:absolute; left:0; right:0; height:0; }
.ln.a{ top:var(--asc);  border-top:0.25mm dashed var(--line-soft); }
.ln.h{ top:var(--head); border-top:0.4mm solid var(--line); }
.ln.b{ top:var(--base); border-top:0.4mm solid var(--line); }
.ln.d{ top:var(--desc); border-top:0.25mm dashed var(--line-soft); }
/* strut: an inline-block whose bottom edge sits on the text baseline, so the
   baseline lands on --base whatever the font's line metrics say */
.row .cells{ position:absolute; left:0; right:0; top:0;
             display:flex; justify-content:flex-start; line-height:0; }
.st{ display:inline-block; width:0; height:var(--base); vertical-align:baseline; }
.row .c{ font-size:var(--gs); line-height:0; flex:0 0 auto; width:24mm; text-align:center; }
.row.words{ --head:6.5mm; --base:14mm; }
.row.words .c{ width:auto; padding-right:10mm; text-align:left; }
.row.sent{ --head:5.5mm; --base:11.5mm; }
.row.sent .cells{ display:block; }
.row.sent .c{ display:block; width:auto; text-align:left; }

.t-model{ color:var(--ink); } .t-trace{ color:var(--trace); }
.t-out{ color:transparent; -webkit-text-stroke:0.28mm var(--outline); }
.t-faint{ color:var(--faint); }

.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-size:10pt; letter-spacing:.24em; color:var(--sindoor); }
.cover h1{ font-size:30pt; margin:6mm 0 2mm; line-height:1.25; }
.cover h1 .deva{ display:block; font-size:34pt; color:var(--ink); margin-bottom:3mm; }
.cover .sub{ font-size:12pt; color:var(--faded); max-width:135mm; margin:0 auto; line-height:1.7; }
.rules{ text-align:left; max-width:150mm; margin:12mm auto 0; }
.rules h2{ font-size:12pt; margin:0 0 3mm; color:var(--sindoor); }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ margin-bottom:3mm; line-height:1.65; font-size:10.5pt; }
.rules li b{ color:var(--teal); }
.legend{ margin:10mm auto 0; max-width:150mm; border:0.3mm solid var(--line-soft);
         border-radius:1.5mm; padding:4mm 5mm; }
.legend h3{ margin:0 0 2.5mm; font-size:10pt; color:var(--teal); }
.legend .lg{ display:flex; gap:7mm; align-items:flex-end; }
.legend .lg div{ text-align:center; font-size:8.5pt; color:var(--faded); }
.legend .lg .s{ font-size:13mm; line-height:1.1; display:block; }
.cover .foot{ position:absolute; bottom:6mm; left:0; right:0; text-align:center;
              font-family:'JetBrains Mono',monospace; font-size:8pt; letter-spacing:.16em;
              text-transform:uppercase; color:var(--sindoor); }

.pf{ position:absolute; bottom:0; left:0; right:0; display:flex; justify-content:space-between;
     border-top:0.25mm solid var(--line-soft); padding-top:1.5mm; font-size:8pt; color:var(--faded); }
.pf .r{ letter-spacing:.06em; }
"""

def page_head(pair, title):
    cfg = C(pair); g = SCRIPTS[cfg["target_iso"]]
    css = (STYLE.replace('{SRC_FONT}', SOURCE_FONTS[cfg['source_iso']])
                .replace('{TFONT}', g['font'])
                .replace('{ASC}', str(g['asc'])).replace('{TOP}', str(g['top']))
                .replace('{BOT}', str(g['bot'])))
    return f"""<!DOCTYPE html>
<html lang="{cfg['source_iso']}">
<head>
<meta charset="UTF-8"/>
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{fonts_url(SOURCE_FONTS[cfg['source_iso']], g['font'])}" rel="stylesheet"/>
<style>{css}</style>
</head>
<body>
"""

def row(cells_html, label_left, label_right="", cls=""):
    return f"""<div class="rowlabel"><span>{label_left}</span><span>{label_right}</span></div>
<div class="row {cls}">
  <div class="ln a"></div><div class="ln h"></div><div class="ln b"></div><div class="ln d"></div>
  <div class="cells">{cells_html}</div>
</div>"""

def cells(glyph, n, cls):
    return "".join(f'<span class="c deva {cls}"><i class="st"></i>{glyph}</span>' for _ in range(n))

def one(glyph, cls):
    return f'<span class="c deva {cls}"><i class="st"></i>{glyph}</span>'

def footer(pair, book, n):
    cfg = C(pair)
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span class="r">BHASHASETU &middot; {cfg["sub"]} &middot; {D(pair, n)}</span></div>')

ADVANCE = 0.55
def check_width(text, band_mm, label):
    gs = band_mm / 0.642
    est = len(text) * ADVANCE * gs
    if est > 185:
        print(f"  !! too wide ({est:.0f}mm > 185mm): {label} :: {text}")

def cover(pair, book_no, deva_title, src_title, sub, rules):
    U = C(pair)["ui"]
    lg = f"""<div class="legend"><h3>{U['legend']}</h3><div class="lg">
      <div><span class="s deva t-model">{SCRIPTS[C(pair)["target_iso"]]["sample"]}</span>{U['model']}</div>
      <div><span class="s deva t-trace">{SCRIPTS[C(pair)["target_iso"]]["sample"]}</span>{U['grey']}</div>
      <div><span class="s deva t-out">{SCRIPTS[C(pair)["target_iso"]]["sample"]}</span>{U['hollow']}</div>
      <div><span class="s deva t-faint">{SCRIPTS[C(pair)["target_iso"]]["sample"]}</span>{U['faint']}</div>
      </div></div>"""
    ol = "".join(f"<li>{r}</li>" for r in rules)
    return f"""<div class="sheet cover">
  <div class="kicker">{C(pair)['book']} {book_no}</div>
  <h1><span class="deva">{deva_title}</span>{src_title}</h1>
  <p class="sub">{sub}</p>
  <div class="rules"><h2>{U['before']}</h2><ol>{ol}</ol></div>
  {lg}
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""

def letter_sheet(pair, book, n, deva, bn_eq, tr, ex, bn_gloss, group, note=None):
    U = C(pair)["ui"]
    eq, gloss = bn_eq, bn_gloss          # pre-resolved in the pair file
    if note is None:
        note = U["letter_note"]
    return f"""<div class="sheet tall">
  <div class="ph">
    <div class="ph-l">
      <div class="big deva">{deva}</div>
      <div class="meta">
        <div class="eq">= <b>{eq}</b></div>
        <div class="tr">{tr}</div>
        <div class="ex"><span class="deva">{ex}</span> &middot; {gloss}</div>
      </div>
    </div>
    <div class="ph-r"><div class="grp">{group}</div><div class="num">{D(pair, n)}</div></div>
  </div>
  <div class="steps">
    <div class="step"><span class="g deva">{deva}<span class="mask"></span></span>
      <div class="cap"><b>{D(pair,1)}</b> {U['step1']}</div></div>
    <div class="step"><span class="g deva">{deva}</span>
      <div class="cap"><b>{D(pair,2)}</b> {U['step2']}</div></div>
    <div class="note">{note}</div>
  </div>
  {row(cells(deva,7,'t-trace'), U['trace'], U['times'])}
  {row(cells(deva,7,'t-out'), U['fill'], U['times'])}
  {row(one(deva,'t-model')+one(deva,'t-faint'), U['start_given'], U['finish_row'])}
  {row('', U['self'], U['fill_row'])}
  {row('', U['self'], '')}
  {row(one(ex,'t-model')+one(ex,'t-trace')+(one(ex,'t-out') if len(ex)<=4 else ''),
       f"{U['in_word']} - <span class=\"deva\">{ex}</span> ({gloss})", U['then_self'], 'words')}
  {footer(pair, book, n)}
</div>"""

def matra_sheet(pair, book, n, form, bn_eq, tr, bn_note):
    U = C(pair)["ui"]
    eq, note = bn_eq, bn_note
    base, sign = form[0], form[1:]
    applied = "".join(one(c+sign,'t-model')+one(c+sign,'t-trace')+one(c+sign,'t-out') for c in SCRIPTS[C(pair)["target_iso"]]["others"])
    rule = U['matra_rule'].replace('{b}', f'<span class="deva">{base}</span>').replace('{f}', f'<span class="deva">{form}</span>')
    return f"""<div class="sheet tall">
  <div class="ph">
    <div class="ph-l">
      <div class="big deva">{form}</div>
      <div class="meta"><div class="eq">= <b>{eq}</b></div><div class="tr">{tr}</div>
        <div class="ex">{note}</div></div>
    </div>
    <div class="ph-r"><div class="grp">{U['matra']}</div><div class="num">{D(pair, n)}</div></div>
  </div>
  <div class="steps">
    <div class="step"><span class="g deva">{base}</span><div class="cap"><b>{D(pair,1)}</b> {U['consonants']}</div></div>
    <div class="step"><span class="g deva">{form}</span><div class="cap"><b>{D(pair,2)}</b> + {U['matra']}</div></div>
    <div class="note">{rule}</div>
  </div>
  {row(cells(form,7,'t-trace'), U['trace'], U['times'])}
  {row(cells(form,7,'t-out'), U['fill'], U['times'])}
  {row(one(form,'t-model')+one(form,'t-faint'), U['start_given'], U['finish_row'])}
  {row(applied, U['apply'], U['then_self'])}
  {row('', U['self'], '')}
  {footer(pair, book, n)}
</div>"""

def conjunct_sheet(pair, book, n, items):
    U = C(pair)["ui"]
    blocks = ""
    for cj, a, bpart, ex, bn_gloss, grp in items:
        gloss = bn_gloss
        check_width(ex, 7.5, f"conjunct {n}")
        label = (f'<span class="deva" style="font-size:13pt">{a}</span> + '
                 f'<span class="deva" style="font-size:13pt">{bpart}</span> = '
                 f'<span class="deva" style="font-size:15pt"><b>{cj}</b></span>'
                 f' &nbsp;&middot;&nbsp; <span class="deva">{ex}</span> ({gloss})')
        blocks += row(cells(cj, 7, 't-trace'), label, U['trace'])
        blocks += row(cells(cj, 4, 't-out') + one(cj,'t-model'), U['fill'], U['then_self'])
        blocks += row(one(ex,'t-model')+one(ex,'t-trace'), U['in_word'], U['then_self'], 'words')
        blocks += row('', '', U['self'], 'words')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>{items[0][5]}</b></div>
      <div class="ex">{U['conj_intro']}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{U['conj']}</div><div class="num">{D(pair, n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

def words_sheet(pair, book, n, group, items):
    U = C(pair)["ui"]
    blocks = ""
    for w, bn_gloss in items:
        gloss = bn_gloss
        blocks += row(one(w,'t-model')+one(w,'t-trace'),
                      f'<span class="deva" style="font-size:12pt">{w}</span> &nbsp; = &nbsp; <b>{gloss}</b>',
                      U['start_given'], 'words')
        blocks += row('', '', U['self'], 'words')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>{group}</b></div>
      <div class="ex">{U['word_intro']}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{U['words']}</div><div class="num">{D(pair, n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

def sentence_sheet(pair, book, n, items):
    U = C(pair)["ui"]
    blocks = ""
    for hi, bn_gloss in items:
        gloss = bn_gloss
        check_width(hi, 6.0, f"sentence {n}")
        blocks += f'<div class="rowlabel"><span><b>{gloss}</b></span><span>{U["sent_flow"]}</span></div>'
        blocks += row(one(hi,'t-model'), '', '', 'sent')
        blocks += row(one(hi,'t-trace'), U['trace'], '', 'sent')
        blocks += row('', U['self'], '', 'sent')
        blocks += row('', '', '', 'sent')
        blocks += row('', '', '', 'sent')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>{U['sent_head']}</b></div>
      <div class="ex">{U['sent_intro']}</div>
    </div></div>
    <div class="ph-r"><div class="grp">{U['sentences']}</div><div class="num">{D(pair, n)}</div></div>
  </div>
  {blocks}
  {footer(pair, book, n)}
</div>"""

# ---------------------------------------------------------------- books
# ---------------------------------------------------------------- build
def build(pair):
    c = C(pair); L = c["letters"]; bks = c["books"]; U = c["ui"]
    out = os.path.join(HERE, pair); os.makedirs(out, exist_ok=True)
    made = []
    def bl(i): return f'{c["book"]} {D(pair, i+1)} \u00b7 {bks[i]["label"]}'
    def cov(i): return cover(pair, D(pair, i+1), bks[i]["native"], bks[i]["label"],
                             bks[i].get("bridge",""), c["rules"])

    p = [cov(0)]
    for n, r in enumerate(L["vowels"], 1):
        p.append(letter_sheet(pair, bl(0), n, r["t"], r["eq"], r["roman"], r["ex"],
                              r["gloss"], r["group"]))
    made.append((bks[0]["slug"], bks[0]["label"], p))

    p = [cov(1)]
    for n, r in enumerate(L["cons"], 1):
        p.append(letter_sheet(pair, bl(1), n, r["t"], r["eq"], r["roman"], r["ex"],
                              r["gloss"], r["group"]))
    known = set(c.get("nukta_known", []))
    for n, r in enumerate(L["nukta"], len(L["cons"]) + 1):
        note = U["nukta_note_known"] if r["t"] in known else U["nukta_note"]
        p.append(letter_sheet(pair, bl(1), n, r["t"], r["eq"], r["roman"], r["ex"],
                              r["gloss"], r["group"], note))
    made.append((bks[1]["slug"], bks[1]["label"], p))

    p = [cov(2)]
    for n, r in enumerate(L["matra"], 1):
        p.append(matra_sheet(pair, bl(2), n, r["t"], r["eq"], r["roman"], r["note"]))
    made.append((bks[2]["slug"], bks[2]["label"], p))

    p = [cover(pair, D(pair,4), bks[3]["native"], bks[3]["label"],
               bks[3].get("bridge",""), c["conj_rules"])]
    grouped = {}
    for r in L["conjuncts"]: grouped.setdefault(r["group"], []).append(r)
    n = 1
    for grp, items in grouped.items():
        for k in range(0, len(items), 2):
            tup = [(x["t"], x["a"], x["b"], x["ex"], x["gloss"], x["group"]) for x in items[k:k+2]]
            p.append(conjunct_sheet(pair, bl(3), n, tup)); n += 1
    made.append((bks[3]["slug"], bks[3]["label"], p))

    for i, key in ((4,"words1"), (5,"words2")):
        p = [cov(i)]; n = 1
        for group, its in c[key].items():
            for k in range(0, len(its), 4):
                p.append(words_sheet(pair, bl(i), n, group, [tuple(x) for x in its[k:k+4]])); n += 1
        made.append((bks[i]["slug"], bks[i]["label"], p))

    for i, key in ((6,"sent1"), (7,"sent2")):
        p = [cov(i)]; its = c[key]
        for k in range(0, len(its), 2):
            p.append(sentence_sheet(pair, bl(i), k//2 + 1, [tuple(x) for x in its[k:k+2]]))
        made.append((bks[i]["slug"], bks[i]["label"], p))

    rows = ""
    for slug, title, pages in made:
        fn = f"{slug}.html"
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write(page_head(pair, f'{title} - {c["sub"]}') + "\n".join(pages) + "\n</body>\n</html>")
        print(f"  {fn:<26} {len(pages):>3} pages")
        rows += (f'<tr><td><b>{title}</b></td><td>{D(pair, len(pages))}</td>'
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
