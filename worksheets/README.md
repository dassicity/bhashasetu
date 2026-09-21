# হাতের লেখার খাতা - handwriting worksheets

Printable A4 workbooks that teach a **Bengali** speaker to *write* **Devanagari**,
in the order `courses/bengali_to_hindi.html` teaches it: letters -> vowel signs ->
words -> sentences. Every instruction is in Bengali.

The PDFs are built once and committed. They are static files, meant to be sent to
a learner on request - nothing is generated on the fly.

## What is here

Five pairs, three generators, because three script families sit on the page in
three different ways.

| Generator | Target | Pairs | Pages each |
|---|---|---|---|
| `gen_worksheets.py` | Devanagari | `bengali_to_hindi`, `telugu_to_hindi` | 169 |
| `gen_worksheets_urdu.py` | Perso-Arabic | `bengali_to_urdu` | 136 |
| `gen_worksheets_brahmic.py` | Telugu, Tamil | `bengali_to_telugu` (138), `bengali_to_tamil` (121) | |

Every pair has eight books and its own `index.html`. Books 1, 2 and 5 to 8 are the
same idea everywhere: vowels, consonants, easy words, harder words, short
sentences, longer sentences. **Books 3 and 4 are where the scripts diverge**, because
each family joins letters differently:

| Pair | Book 3 | Book 4 |
|---|---|---|
| to Devanagari | matras (the क barakhadi) | 66 conjuncts grouped by formation rule |
| to Urdu | harakat, and which are normally unwritten | joining, and the nine letters that never join leftward |
| to Telugu | గుణింతం | ఒత్తు, the subscript consonant |
| to Tamil | உயிர்மெய் | புள்ளி, which is **not** a conjunct at all |

## Three rulings, because the scripts sit differently

Devanagari **hangs from** a headline. Arabic script **sits on** a baseline and runs
right to left. Telugu and Tamil sit on a baseline too, but left to right and with
no headline at all, so their top solid line is a **height guide, not a connector** -
calling it a headline would teach a Devanagari habit these scripts do not have.

```
Devanagari              Nastaliq (RTL)          Telugu / Tamil
- - - matras above      - - - ascenders         - - - signs above
_____ SHIRO-REKHA       ..... x-height          _____ height guide
_____ baseline          _____ BASELINE          _____ baseline
- - - matras below      - - - descenders        - - - signs below
```

All metrics measured per font with canvas `TextMetrics` (`calibrate_font.html`,
`calibrate_nastaliq.html`, `calibrate_brahmic.html`), as fractions of the font size
from the baseline:

| | body / ascender | signs above | signs below |
|---|---|---|---|
| Devanagari | 0.642 (the headline) | 0.925 | 0.290 |
| Nastaliq | 0.714 (ا ل ک) | | 0.420 (م is 0.383, plus the cascade) |
| Telugu | 0.772 | 1.003 | 0.444 (ottu hangs deep) |
| Tamil | 0.497 | 0.787 | 0.250 |

Tamil's body is barely half Telugu's, so the same letter height needs a much larger
font size. Guessing instead of measuring would have made one of them wrong.

## What is genuinely new for an Urdu learner

Right to left, but numerals still left to right. Letters take **four shapes**
depending on position, which Bengali has no parallel for at all. **Nine letters
never join leftward** (ا د ڈ ذ ر ڑ ز ژ و), so a gap mid-word is a rule, not a
mistake. And short vowels are marks that are **normally not written**, so every
word in these books carries a Bengali pronunciation with the vowels supplied.

The positional forms are generated with ZWJ rather than hardcoded, so they stay
correct if the font changes.

## Known limits

- **Nastaliq cascades diagonally** inside a ligature, so a word does not sit flat
  on the baseline. The descender zone is sized to absorb it, but the ruling
  cannot show the slope; the covers say so instead.
- **No true stroke order** in any pair. Needs per-glyph vector data.

## The page design

Four ruled lines, the way a Hindi सुलेख copybook rules them:

```
- - - - - - - -   dashed: ceiling for matras above (ि ी े ै)
______________    solid:  SHIRO-REKHA - the letter hangs from here
______________    solid:  baseline - the letter sits here
- - - - - - - -   dashed: floor for matras below (ु ू ृ)
```

Each letter page runs: **two-step box** (body first, headline last) -> **trace**
the grey glyph -> **fill** the hollow outline -> **start given, finish the row**
-> **two blank rows** -> the letter inside a real word.

The two-step box is the one genuinely important stroke rule in Devanagari, and
it is a bridge the learner already owns: Bengali writes the মাত্রা last too.

## Rebuilding

```bash
python3 gen_worksheets.py                  # both Devanagari pairs
python3 gen_worksheets.py telugu_to_hindi  # just one
python3 gen_worksheets_urdu.py             # the Perso-Arabic pair
./build_pdfs.sh                            # renders A4 PDFs for every pair
```

Chrome does the rendering because it shapes Devanagari correctly (matras,
conjuncts, nukta). reportlab and fpdf do not, without a lot of extra work.

## Retuning the ruling

Only two numbers are set by hand, in `STYLE` in the generator:

```css
--head: 9mm;   /* shirorekha */
--base: 19mm;  /* baseline   */
```

Glyph size, both dashed guide lines and the row height all derive from them
using the font's real metrics:

```css
--asc-ratio: 0.642;  /* baseline -> shirorekha, as a fraction of font-size */
--top-ratio: 0.283;  /* how far matras above clear the headline            */
--bot-ratio: 0.290;  /* how far matras below drop past the baseline        */
```

Those three came from measuring Noto Serif Devanagari with canvas
`TextMetrics` - open `calibrate_font.html` over a local server and read the
numbers off it. Remeasure if the font ever changes.

The baseline is pinned by a zero-width `<i class="st">` strut whose bottom edge
sits on the text baseline, so the letters land on the ruling regardless of the
font's line-height metrics.

## Known limits

- **No true stroke order.** The two-step box teaches body-then-headline, which is
  the rule that actually matters, but there are no numbered stroke arrows - that
  needs per-glyph vector data this does not have.
- Print at **100%**, not "fit to page", or the ruling will not match the glyph size.

---

## Architecture change, 21 Sept 2026: pairs are data, not code

Before this, each generator carried its own pair data AND its own source-language prose
hardcoded in Python. That was fine while every pair had Bengali as the source. It stopped
being fine the moment a Kannada, Hindi or Telugu source appeared: adding a pair meant
editing a generator, and five course agents working in parallel would have collided in
the same file.

Now a pair is a JSON file and nothing else.

| File | Serves | Geometry |
|---|---|---|
| `gen_brahmic.py` | baseline-sitting Brahmic targets: Telugu, Tamil | `SCRIPTS` in the file, measured |
| `gen_urdu.py` | Perso-Arabic targets: Urdu | one solid baseline, RTL |
| `gen_worksheets.py` | Devanagari targets: Hindi, Marathi | not yet converted, see below |
| `data/{pair}.json` | one pair: all source-language text, words, sentences | - |
| `data/targets/{iso}.json` | one target script: the letter spine, already verified | - |
| `data/SCHEMA.md` | what a pair file must contain | - |

The split that matters: **geometry belongs to the script, not to the pair.** The measured
`body`/`top`/`bot` ratios for Telugu were paid for once and every Telugu-target pair reuses
them. That is why a new course with an already-calibrated target is cheap, and a course
with a new target script is not.

Likewise the letter inventory splits in two. The target-script half (the letters, their
Roman values, example words, and for Urdu which letters join leftward) is verified once and
shared. Only the source-language half (equivalent letter, gloss, family label) is written
per pair, by the agent that built that course, since it is the one that knows what the
course actually taught.

### Adding a pair

1. Write `data/{pair}.json` against `data/SCHEMA.md`.
2. `python3 gen_brahmic.py {pair}` (or `gen_urdu.py`). If the file is incomplete the
   generator refuses to build and prints exactly what is missing, rather than producing a
   half-correct workbook.
3. `./build_pdfs.sh {pair}`
4. Check parity: the sheet count the generator prints must equal the PDF page count.
   A mismatch means a sheet overflowed onto a second page.

### Bridges are written per pair and never translated

The same fact inverts depending on who is reading. A headline over the letters is an
existing habit for a Bengali or Hindi writer, a new one for a Telugu writer, and absent
in Urdu. Conjuncts are a familiar idea in Devanagari, always-below in Telugu, and not a
category at all in Tamil, where the hardest chapter of Devanagari simply does not exist.
Translating another pair's bridge produces something that is fluent and wrong.

### Verification

Both converted generators were checked by rebuilding the pairs that already shipped and
comparing against the PDFs in the repo:

| Pair | Books | Shipped pages | Rebuilt | Result |
|---|---|---|---|---|
| bengali_to_telugu | 8 | 138 | 138 | identical |
| bengali_to_tamil | 8 | 121 | 121 | identical |
| bengali_to_urdu | 8 | 136 | 136 | identical |

One real bug surfaced during the conversion: word book 2 held 48 words in both Brahmic
pairs, under the 50 to 60 the brief asks for. The generator now refuses to build a pair
that is short, and both pairs were topped up to 52 (Telugu and Tamil books 6 are now 14
pages, so those two PDFs changed).

### Still to convert

`gen_worksheets.py` (Devanagari targets) has not been moved to the JSON layout, because
no pair in the current batch targets Devanagari. It should be converted before the next
Hindi-target or Marathi-target course, using the same three steps: export the existing
pairs to `data/`, splice out the hardcoded source strings, then prove page parity against
the shipped PDFs before deleting anything.
