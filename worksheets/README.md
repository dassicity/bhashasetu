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
| `gen_deva.py` | Devanagari targets: Hindi, Marathi | headline-hanging, converted 2026-09-22 |
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

### All three generators are now JSON-driven

`gen_deva.py` replaced `gen_worksheets.py` on 2026-09-22 and the conversion found a shipped
bug worth recording. That generator held two pairs at once: a Bengali default set with a
Telugu override map layered on top. The overrides covered the letter equivalents and the
glosses, but **not the word-group headings and not the consonant varga labels**, because
nothing forced them to. So the printed `telugu_to_hindi` workbooks carried about 200 runs of
Bengali text, showing a Telugu learner Bengali category names for three books.

One pair per file makes that impossible to express. `audit()` also now compares every string
in a pair file against the Unicode range of every OTHER Indic script and refuses to build
when it finds a foreign one, so the class of bug fails loudly rather than printing.

Verification for the conversion, same as the other two: `bengali_to_hindi` rebuilt to 169
pages, matching all eight shipped PDFs book for book. `telugu_to_hindi` correctly refused to
build until its 23 labels were written in Telugu.

### Calibrated target scripts

| Script | body | top | bot | Measured |
|---|---|---|---|---|
| Telugu | 0.772 | 1.020 | 0.460 | 2026-09-21 |
| Tamil | 0.497 | 0.810 | 0.280 | 2026-09-21 |
| Kannada | 0.790 | 0.826 | 0.431 | 2026-09-22 |
| Malayalam | 0.524 | 0.767 | 0.297 | 2026-09-22 |

Measured with `calibrate_kn_ml.html`: canvas `TextMetrics`, `actualBoundingBoxAscent` and
`actualBoundingBoxDescent` over a set of base consonants, consonants carrying an above sign,
and consonants carrying a below sign, at 200px, divided by the size. That run re-measured
Telugu as a control and reproduced `body` 0.772 exactly, with `top` 1.003 and `bot` 0.444
against the shipped 1.020 and 0.460, which shows the shipped numbers carry about 0.016 of
deliberate headroom. The same headroom was added to the two new scripts.

Do not re-measure per pair. Geometry is a property of the script, so every pair sharing a
target reuses it, and that is what makes a new course with an existing target cheap.

### Still needed for Kannada and Malayalam targets

The geometry is done, but neither has a letter spine yet: `data/targets/kn.json` and
`data/targets/ml.json` do not exist. The spine is the target-script half of the inventory,
verified once and shared by every pair with that target (letters, Roman values, example
words). The first agent to build a Kannada-target or Malayalam-target course should produce
it in the shape of `targets/te.json`, and every later pair fills only the source-language
columns. Check any new spine for foreign-script leakage before it goes out: the Tamil one
shipped with a Bengali column because it was extracted from the Bengali course.

---

## Non-Indic targets, 2026-09-22

Two generators were added for targets that are neither abugida nor abjad, and both needed a
different page, not just different numbers.

### `gen_hangul.py` - Korean

A Hangul syllable is drawn inside a notional square and every syllable gets the same square
whatever it holds, so Korean practice paper is a grid (wongoji), not a set of baselines. The
sheets draw that grid with the faint cross-hairs children's practice paper uses, and put
**one syllable per cell all the way through**, including the word and sentence books. That
is deliberate: writing jamo in a row like Bengali letters instead of stacking them into a
block is exactly the mistake a Brahmic-trained hand makes, and a page of squares prevents it
in a way a sentence of instructions does not.

Measured (calibrate_hangul.html): a block with a batchim runs 0.804 up and 0.084 down, and
the widest blocks advance 0.966, so a block is very nearly square and fills the em. The only
tunable is `fill`, how much of the cell the glyph should occupy.

Two bugs are worth remembering. The word and sentence books overflowed by about 80 percent,
because three stacked 15mm grids per item do not fit A4; cell size is now per grid type. And
the "write it yourself" row was **invisible**, because it was built out of spaces and a space
renders as a borderless gap cell. Page counts were perfectly consistent while the most
important row on the page had no boxes in it. Only rendering the page showed it.

### `gen_latin.py` - Spanish

This one is deliberately not a handwriting book. An Indian learner who has been to school
already writes the Latin alphabet from English, so four books of tracing a b c would be
busywork. The pair file decides the books and declares a `kind` on each; the generator
renders whatever is declared. For Spanish that came out as: the letters English does not
have, the inverted opening marks, the written accent as a stress RULE with minimal pairs,
and the spelling patterns an Indian English speaker gets wrong by transfer. Dictation is the
mode of the word books rather than a ninth book.

Ruling is the four-line copybook - ascender, x-height, baseline, descender. Measured in Noto
Serif: x-height 0.546, ascender 0.770, capital 0.725, descender 0.240. The useful finding is
that an accented vowel tops out at 0.766, within 0.004 of the ascender, so the accent bounds
itself and no fifth rule is needed.

Because one book mixes bare marks, whole words and whole sentences in the same inventory,
repetition count is derived from the length of the thing being practised rather than fixed.

| Pair | Books | Pages | Parity |
|---|---|---|---|
| bengali_to_korean | 8 | 158 | verified |
| bengali_to_spanish | 8 | 150 | verified |

### Generators now

| File | Targets | Page |
|---|---|---|
| `gen_deva.py` | Hindi, Marathi, Bengali, Punjabi | hangs from a headline |
| `gen_brahmic.py` | Telugu, Tamil, Kannada, Malayalam | sits on a baseline |
| `gen_urdu.py` | Urdu | one baseline, right to left |
| `gen_hangul.py` | Korean | square grid |
| `gen_latin.py` | Spanish | four-line copybook |

### A limitation worth knowing, found building hindi_to_marathi

`gen_deva.py` is data-driven about CONTENT but not about book SHAPE. Books 1 to 4 are wired
to `letters.vowels`, `letters.cons` plus `nukta`, `letters.matra` and `letters.conjuncts`,
and the audit insists on exactly eight books with all five inventories non-empty. So a pair
that needs a different set of books cannot express it here, unlike `gen_latin.py`, where each
book declares its own `kind` and the generator renders whatever is declared.

The Hindi to Marathi agent worked within the constraint rather than around it, and the result
is better than a generic workbook: it filled the fixed slots with difference-only content.
Five vowels instead of thirteen, because only five behave differently. Five barakhadi rows
instead of twelve. And the consonant book gives च two pages, one dental and one palatal, so
the central teaching of the pair sits in the page structure itself. Books 1 and 3 are six
pages each and their bridges say plainly that this is the point.

If a future same-script pair needs genuinely different books, port the `kind`/`rows`
dispatch from `gen_latin.py` rather than padding inventories to fit the slots.
