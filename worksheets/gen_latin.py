#!/usr/bin/env python3
"""
Workbooks for Latin-script targets (Spanish).

This one is deliberately NOT a handwriting book. An Indian learner who has been to school
already writes the Latin alphabet fluently from English, so four books of tracing a b c
would be busywork. What is genuinely new is narrower and more interesting: the letters
English does not have, the inverted opening marks, the written accent as a STRESS RULE that
distinguishes real word pairs, and the spelling patterns an Indian English speaker gets
wrong by transfer. The pair file decides the books; this file renders whatever it declares
through the "kind" field on each book.

Ruling: a Latin copybook has four lines - ascender, x-height, baseline, descender - where
the Brahmic sheets have two bands and Hangul has squares. Measured with canvas TextMetrics
(calibrate_latin.html) as fractions of the font size, in Noto Serif:
    x-height 0.546 · ascender 0.770 · capital 0.725 · descender 0.240
    accent top 0.766, which is within 0.004 of the ascender: an accented vowel reaches
    almost exactly the ascender line, so four rules are enough and the accent bounds itself.

  python3 gen_latin.py                       # every Latin-target pair with a data file
  python3 gen_latin.py bengali_to_spanish    # one pair
"""
import os, html, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

SCRIPTS = {"es": {"font":"Noto Serif", "xh":0.546, "asc":0.770, "desc":0.240}}

SOURCE_FONTS = {
 "bn":"Noto Serif Bengali",   "hi":"Noto Serif Devanagari", "mr":"Noto Serif Devanagari",
 "te":"Noto Serif Telugu",    "ta":"Noto Serif Tamil",      "kn":"Noto Serif Kannada",
 "ml":"Noto Serif Malayalam", "pa":"Noto Serif Gurmukhi",   "ur":"Noto Nastaliq Urdu",
}
def _fam(n):
    w = "wght@400;500" if "Nastaliq" in n else "wght@400;500;600;700"
    return "family=" + n.replace(" ","+") + ":" + w
def fonts_url(*names):
    seen=[]
    for n in names:
        if n and n not in seen: seen.append(n)
    return ("https://fonts.googleapis.com/css2?" + "&".join(_fam(n) for n in seen)
            + "&family=JetBrains+Mono:wght@400;500&display=swap")

SHARED_PUNCT = {0x0964, 0x0965}
REQUIRED_UI = ["trace","fill","self","times","start_given","finish_row","fill_row","in_word",
               "then_self","model","grey","hollow","faint","legend","words_hint","sent_seq",
               "sent_head","sent_hint","dict_head","dict_hint","mark_hint","open_first"]
REQUIRED_TOP = ["pair","source_iso","target_iso","sub","title","book","digits","words_word",
                "sent_word","index_blurb","print_note","books","letters","words1","words2",
                "sent1","sent2"]

_CACHE={}
def C(pair):
    if pair not in _CACHE:
        with open(os.path.join(DATA_DIR,f"{pair}.json"),encoding="utf-8") as f:
            _CACHE[pair]=json.load(f)
    return _CACHE[pair]
def G(pair): return SCRIPTS[C(pair)["target_iso"]]
def U(pair,k): return C(pair)["ui"][k]
def D(pair,n):
    d=C(pair)["digits"]; return "".join(d[int(c)] for c in str(n))

def audit(pair):
    c=C(pair); miss=[]
    miss += [f"top-level: {k}" for k in REQUIRED_TOP if k not in c]
    miss += [f"ui: {k}" for k in REQUIRED_UI if k not in c.get("ui",{})]
    bks=c.get("books",[])
    if not bks: miss.append("books: none")
    for i,b in enumerate(bks):
        if "kind" not in b: miss.append(f"books[{i}].kind")
        if "rows" not in b: miss.append(f"books[{i}].rows")
        elif b["rows"] not in c and b["rows"] not in c.get("letters",{}):
            miss.append(f'books[{i}].rows -> "{b["rows"]}" resolves to nothing')
    if len(c.get("digits",""))!=10: miss.append("digits: need exactly 10 characters")
    import re as _re
    plain=[_re.sub(r"<[^>]+>","",r) for r in c.get("rules",[])]
    if plain:
        tot,lng=sum(len(x) for x in plain),max(len(x) for x in plain)
        if tot>1200 or lng>280:
            miss.append(f"rules too long for the cover: {tot} chars, longest {lng}")
    RANGES={"bn":(0x980,0x9FF),"te":(0xC00,0xC7F),"kn":(0xC80,0xCFF),"ta":(0xB80,0xBFF),
            "ml":(0xD00,0xD7F),"pa":(0xA00,0xA7F),"hi":(0x900,0x97F)}
    iso=c.get("source_iso"); blob=json.dumps(c,ensure_ascii=False)
    for other,(lo,hi) in RANGES.items():
        if other==iso: continue
        hits=[ch for ch in blob if lo<=ord(ch)<=hi and ord(ch) not in SHARED_PUNCT]
        if hits: miss.append(f"{len(hits)} characters of {other} script in a {iso} pair file")
    if "—" in blob: miss.append("em-dash characters present; this project uses '-'")
    return miss

STYLE = """
:root{
  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --ochre:#B8802D; --teal:#1F4D4A;
  --line:#9aa8b8; --line-soft:#c7d0da; --paper:#FDFBF6;
}
@page{ size:A4; margin:12mm 10mm; }
*{ box-sizing:border-box; }
body{ font-family:'{SFONT}',serif; color:var(--ink); font-size:10pt; margin:0;
      background:var(--paper); }
.sheet{ page-break-after:always; break-after:page; padding:0 2mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }
.es{ font-family:'{TFONT}',serif; }

.ph{ display:flex; justify-content:space-between; align-items:flex-start;
     border-bottom:0.4mm solid var(--line-soft); padding-bottom:2.5mm; margin-bottom:3.5mm; }
.ph-l{ display:flex; gap:6mm; align-items:flex-start; }
.big{ font-size:{BIG}; line-height:1.05; font-family:'{TFONT}',serif; }
.meta{ padding-top:1.5mm; }
.meta .eq{ font-size:12.5pt; }
.meta .tr{ font-family:'JetBrains Mono',monospace; font-size:9pt; color:var(--faded);
           letter-spacing:.08em; margin-top:1mm; }
.meta .ex{ font-size:10pt; color:var(--faded); margin-top:1.5mm; }
.ph-r{ text-align:right; max-width:62mm; }
.grp{ font-size:9pt; color:var(--teal); }
.num{ font-size:14pt; color:var(--faded); margin-top:1mm; }
.note{ font-size:9.5pt; color:var(--faded); background:#F4F1EA; border-left:1mm solid var(--ochre);
       padding:2mm 3mm; margin:0 0 3mm; line-height:1.6; }
.pair{ font-size:10pt; color:var(--sindoor); margin:0 0 2.5mm; }

/* ---- the four rules of a Latin copybook ---- */
.rowlabel{ display:flex; justify-content:space-between; font-size:8.5pt; color:var(--faded);
           margin:0 0 0.8mm; }
.row{ position:relative; height:{ROWH}; margin-bottom:3mm; }
.row.w{ height:{ROWHW}; }
.ln{ position:absolute; left:0; right:0; }
.ln.a{ top:{ASC};  border-top:0.22mm dashed var(--line-soft); }
.ln.x{ top:{XH};   border-top:0.22mm dashed var(--line-soft); }
.ln.b{ top:{BASE}; border-top:0.38mm solid var(--line); }
.ln.d{ top:{DESC}; border-top:0.22mm dashed var(--line-soft); }
.row.w .ln.a{ top:{ASCW}; } .row.w .ln.x{ top:{XHW}; }
.row.w .ln.b{ top:{BASEW}; } .row.w .ln.d{ top:{DESCW}; }
.cells{ position:absolute; left:0; top:0; right:0; white-space:nowrap; }
.c{ font-family:'{TFONT}',serif; font-size:{GS}; line-height:0; margin-right:{GAP}; }
.row.w .c{ font-size:{GSW}; margin-right:{GAPW}; }
/* zero-width strut: pins the text baseline to --base whatever the font's line metrics say */
.st{ display:inline-block; width:0; height:{BASE}; vertical-align:baseline; }
.row.w .st{ height:{BASEW}; }
.t-model{ color:var(--ink); }
.t-trace{ color:#BFB6A6; }
.t-out{ color:transparent; -webkit-text-stroke:0.2mm #BFB6A6; }
.t-faint{ color:#E7E1D3; }

.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-family:'JetBrains Mono',monospace; font-size:9pt; letter-spacing:.2em;
                color:var(--sindoor); }
.cover h1{ font-size:24pt; margin:4mm 0 2mm; font-weight:600; }
.cover h1 .es{ display:block; font-size:32pt; margin-bottom:3mm; }
.cover .sub{ font-size:11pt; color:var(--faded); max-width:132mm; margin:0 auto 8mm; line-height:1.8; }
.rules{ max-width:140mm; margin:0 auto; text-align:left; }
.rules h2{ font-size:11pt; color:var(--teal); margin:0 0 3mm; }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ font-size:10pt; line-height:1.85; margin-bottom:2.5mm; color:var(--faded); }
.rules li b{ color:var(--ink); }
.legend{ max-width:140mm; margin:8mm auto 0; text-align:left; }
.legend h3{ font-size:10pt; color:var(--teal); margin:0 0 2mm; }
.lg{ display:flex; gap:7mm; }
.lg div{ font-size:8.5pt; color:var(--faded); text-align:center; }
.lg .s{ display:block; font-size:11mm; line-height:1.2; font-family:'{TFONT}',serif; }
.foot{ margin-top:12mm; font-family:'JetBrains Mono',monospace; font-size:8pt;
       letter-spacing:.14em; color:var(--faded); }
.pf{ display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace;
     font-size:7.5pt; letter-spacing:.1em; color:#B9AE9B; margin-top:3mm;
     border-top:0.3mm solid var(--line-soft); padding-top:1.5mm; }
"""

def page_head(pair, title):
    c=C(pair); g=G(pair)
    def band(xh_mm):
        gs = xh_mm / g["xh"]
        base = xh_mm + 4.0
        return dict(gs=gs, base=base, asc=base-g["asc"]*gs, xh=base-g["xh"]*gs,
                    desc=base+g["desc"]*gs)
    L = band(6.0)      # letter, mark, rule and spelling books
    W = band(4.3)      # word and sentence books, tighter
    rep = {
      "{SFONT}":SOURCE_FONTS[c["source_iso"]], "{TFONT}":g["font"],
      "{BIG}":"24mm", "{GS}":f'{L["gs"]:.2f}mm', "{GSW}":f'{W["gs"]:.2f}mm',
      "{GAP}":"3.5mm", "{GAPW}":"2.5mm",
      "{ASC}":f'{L["asc"]:.2f}mm', "{XH}":f'{L["xh"]:.2f}mm',
      "{BASE}":f'{L["base"]:.2f}mm', "{DESC}":f'{L["desc"]:.2f}mm',
      "{ROWH}":f'{L["desc"]+2.0:.2f}mm',
      "{ASCW}":f'{W["asc"]:.2f}mm', "{XHW}":f'{W["xh"]:.2f}mm',
      "{BASEW}":f'{W["base"]:.2f}mm', "{DESCW}":f'{W["desc"]:.2f}mm',
      "{ROWHW}":f'{W["desc"]+1.5:.2f}mm',
    }
    css = STYLE
    for k,v in rep.items(): css = css.replace(k,v)
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

def one(t,cls): return f'<span class="c {cls}"><i class="st"></i>{t}</span>'
def reps(t,n,cls): return "".join(one(t,cls) for _ in range(n))
def row(cells,l="",r="",w=False):
    lab=(f'<div class="rowlabel"><span>{l}</span><span>{r}</span></div>' if (l or r) else "")
    return (f'{lab}<div class="row{" w" if w else ""}">'
            f'<div class="ln a"></div><div class="ln x"></div>'
            f'<div class="ln b"></div><div class="ln d"></div>'
            f'<div class="cells">{cells}</div></div>')
def footer(pair,book,n):
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span>BHASHASETU &middot; {C(pair)["sub"]} &middot; {D(pair,n)}</span></div>')

def fit(t):
    """How many times a thing fits on one ruled line. A single mark repeats across the row;
       a whole sentence gets written once. The pair file mixes all of these in one book."""
    n=len(t)
    return 8 if n<=2 else 6 if n<=4 else 4 if n<=8 else 2 if n<=16 else 1

def cover(pair,bno,native,title,sub):
    c=C(pair); u=c["ui"]
    ol="".join(f"<li>{r}</li>" for r in c.get("rules",[]))
    rules_html=(f'<div class="rules"><h2>{c.get("rules_head","")}</h2><ol>{ol}</ol></div>'
                if ol else "")
    s=native[0] if native else "a"
    lg=f"""<div class="legend"><h3>{u["legend"]}</h3><div class="lg">
      <div><span class="s es t-model">{s}</span>{u["model"]}</div>
      <div><span class="s es t-trace">{s}</span>{u["grey"]}</div>
      <div><span class="s es t-out">{s}</span>{u["hollow"]}</div>
      <div><span class="s es t-faint">{s}</span>{u["faint"]}</div></div></div>"""
    return f"""<div class="sheet cover">
  <div class="kicker">{c["book"]} {bno}</div>
  <h1><span class="es">{native}</span>{title}</h1>
  <p class="sub">{sub}</p>
  {rules_html}
  {lg}
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""

def item_sheet(pair,book,n,r,kind):
    """One row of the declared inventory. The same renderer serves a bare glyph, a mark, a
       stress-rule word and a spelling sequence, because the pair file says which it is and
       only the repetition count really changes."""
    t=r["t"]; k=fit(t)
    big=f'<div class="big">{t}</div>' if len(t)<=6 else ""
    par=(f'<div class="pair">{r["par"]} &rarr; <b>{t}</b></div>' if r.get("par") else "")
    tr=f'<div class="tr">{r["roman"]}</div>' if r.get("roman") else ""
    ex=(f'<div class="ex"><span class="es">{r["ex"]}</span> &middot; {r["gloss"]}</div>'
        if r.get("ex") else "")
    note = (f'<div class="note">{r["note"]}</div>' if r.get("note") else "")
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">{big}
      <div class="meta"><div class="eq">= <b>{r.get("eq","")}</b></div>{tr}{ex}</div></div>
    <div class="ph-r"><div class="grp">{r.get("group","")}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {par}
  {note}
  {row(reps(t,k,'t-trace'), U(pair,"trace"), U(pair,"times"))}
  {row(reps(t,k,'t-out'), U(pair,"fill"), U(pair,"times"))}
  {row(one(t,'t-model')+reps(t,max(1,k//2),'t-faint'), U(pair,"start_given"), U(pair,"finish_row"))}
  {row('', U(pair,"self"), U(pair,"fill_row"))}
  {row('', U(pair,"dict_head"), U(pair,"dict_hint"))}
  {footer(pair,book,n)}
</div>"""

def words_sheet(pair,book,n,group,items):
    blocks=""
    for w,gloss in items:
        blocks+=row(one(w,'t-model')+one(w,'t-trace'),
                    f'<span class="es" style="font-size:12pt">{w}</span> &nbsp;=&nbsp; <b>{gloss}</b>',
                    U(pair,"start_given"), True)
        blocks+=row('','',U(pair,"self"),True)
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta"><div class="eq" style="font-size:15pt"><b>{group}</b></div>
      <div class="ex">{U(pair,"words_hint")}</div></div></div>
    <div class="ph-r"><div class="grp">{U(pair,"dict_hint")}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {blocks}
  {footer(pair,book,n)}
</div>"""

def sentence_sheet(pair,book,n,items):
    blocks=""
    for tgt,gloss in items:
        blocks+=f'<div class="rowlabel"><span><b>{gloss}</b></span><span>{U(pair,"sent_seq")}</span></div>'
        blocks+=row(one(tgt,'t-model'),'','',True)
        blocks+=row(one(tgt,'t-trace'),'',U(pair,"trace"),True)
        blocks+=row('','',U(pair,"self"),True)
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta"><div class="eq" style="font-size:15pt"><b>{U(pair,"sent_head")}</b></div>
      <div class="ex">{U(pair,"sent_hint")}</div></div></div>
    <div class="ph-r"><div class="grp">{U(pair,"open_first")}</div><div class="num">{D(pair,n)}</div></div>
  </div>
  {blocks}
  {footer(pair,book,n)}
</div>"""

def build(pair):
    c=C(pair); bks=c["books"]
    out=os.path.join(HERE,pair); os.makedirs(out,exist_ok=True)
    made=[]
    for i,b in enumerate(bks):
        bl=f'{c["book"]} {D(pair,i+1)} · {b["label"]}'
        p=[cover(pair,D(pair,i+1),b.get("native",b["label"]),b["label"],b.get("bridge",""))]
        kind=b["kind"]; key=b["rows"]
        if kind in ("words",):
            n=1
            for group,its in c[key].items():
                for k in range(0,len(its),4):
                    p.append(words_sheet(pair,bl,n,group,[tuple(x) for x in its[k:k+4]])); n+=1
        elif kind in ("sentences",):
            its=c[key]
            for k in range(0,len(its),3):
                p.append(sentence_sheet(pair,bl,k//3+1,[tuple(x) for x in its[k:k+3]]))
        else:
            for n,r in enumerate(c["letters"][key],1):
                p.append(item_sheet(pair,bl,n,r,kind))
        made.append((b["slug"],b["label"],p))

    rows=""
    for slug,title,pages in made:
        fn=f"{slug}.html"
        with open(os.path.join(out,fn),"w",encoding="utf-8") as f:
            f.write(page_head(pair,f'{title} - {c["sub"]}')+"\n".join(pages)+"\n</body>\n</html>")
        print(f"  {fn:<24} {len(pages):>3} pages")
        rows+=(f'<tr><td><b>{title}</b></td><td>{D(pair,len(pages))}</td>'
               f'<td><a href="{slug}.pdf">PDF</a></td><td><a href="{fn}">HTML</a></td></tr>')
    with open(os.path.join(out,"index.html"),"w",encoding="utf-8") as f:
        f.write(page_head(pair,f'{c["title"]} - {c["sub"]}')+
                f"""<div style="max-width:150mm;margin:20mm auto;font-size:11pt">
        <h1 style="font-size:20pt">{c["title"]}</h1>
        <p style="color:#6B5B48;line-height:1.7">{c["index_blurb"]}<br/>{c["print_note"]}</p>
        <table style="width:100%;border-collapse:collapse;margin-top:8mm">{rows}</table></div>
        </body></html>""")
    total=sum(len(p) for _,_,p in made)
    print(f"  total {total} pages")
    return total

if __name__=="__main__":
    args=sys.argv[1:]
    if not args:
        args=sorted(f[:-5] for f in os.listdir(DATA_DIR)
                    if f.endswith(".json") and not f.startswith("_"))
    for pr in args:
        fp=os.path.join(DATA_DIR,f"{pr}.json")
        if not os.path.exists(fp): print(f"{pr}: no data file, skipped"); continue
        if json.load(open(fp,encoding="utf-8")).get("target_iso") not in SCRIPTS: continue
        miss=audit(pr)
        if miss:
            print(f"{pr}: NOT BUILT, the pair file is missing:")
            for m in miss: print(f"    - {m}")
            continue
        print(f"{pr}:"); build(pr)
