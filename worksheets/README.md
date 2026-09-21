# হাতের লেখার খাতা - handwriting worksheets

Printable A4 workbooks that teach a **Bengali** speaker to *write* **Devanagari**,
in the order `courses/bengali_to_hindi.html` teaches it: letters -> vowel signs ->
words -> sentences. Every instruction is in Bengali.

The PDFs are built once and committed. They are static files, meant to be sent to
a learner on request - nothing is generated on the fly.

## What is here

Three pairs. Two teach **Devanagari** and share a generator; one teaches the
**Perso-Arabic** script and has its own, because almost nothing carries over.

### Devanagari targets - `gen_worksheets.py`, 169 pages each

| Book | bengali_to_hindi | telugu_to_hindi | Pages | Contents |
|---|---|---|---|---|
| 1 | `01_svarabarna` | `01_achchulu` | 14 | 13 vowels |
| 2 | `02_byanjanbarna` | `02_hallulu` | 41 | 33 consonants + 7 nukta |
| 3 | `03_matra` | `03_gunintalu` | 14 | the क barakhadi |
| 4 | `04_juktakshar` | `04_samyuktakshara` | 35 | 66 conjuncts by rule |
| 5 | `05_shabda_1` | `05_padalu_1` | 18 | 64 easy words |
| 6 | `06_shabda_2` | `06_padalu_2` | 17 | 58 harder words |
| 7 | `07_bakya_1` | `07_vakyalu_1` | 15 | 28 short sentences |
| 8 | `08_bakya_2` | `08_vakyalu_2` | 15 | 28 longer sentences |

### Perso-Arabic target - `gen_worksheets_urdu.py`, 136 pages

`bengali_to_urdu`. The book structure had to change, because an abjad does not
have vowels, matras or conjuncts to practise:

| Book | File | Pages | Contents |
|---|---|---|---|
| 1 | `01_huruf` | 41 | 40 letters, grouped **by shape** (ب پ ت ٹ ث together), each with its four positional forms |
| 2 | `02_char_shakal` | 10 | the four forms drilled on their own - the lesson with no Bengali parallel |
| 3 | `03_harakat` | 13 | zabar, zer, pesh, jazm, tashdid; long vowels as letters; do-chashmi he |
| 4 | `04_jor` | 9 | joining: the nine letters that never join leftward, and common ligatures |
| 5 | `05_alfaz_1` | 18 | 64 easy words |
| 6 | `06_alfaz_2` | 15 | 56 harder words, opening with words Bengali already borrowed |
| 7 | `07_jumle_1` | 15 | 28 short sentences |
| 8 | `08_jumle_2` | 15 | 28 longer sentences |

## Two rulings, because two scripts sit differently

Devanagari **hangs from** a headline; Arabic script **sits on** a baseline.

```
Devanagari                     Perso-Arabic (Nastaliq)
- - - - - matras above         - - - - - ascenders  ا ل ک
_________ SHIRO-REKHA          ......... x-height   ب س ر
_________ baseline             _________ BASELINE
- - - - - matras below         - - - - - descenders م ج ع ی
```

Two solid lines for Devanagari, one for Urdu. Metrics were measured per font
with canvas `TextMetrics` (`calibrate_font.html`, `calibrate_nastaliq.html`):

| | Devanagari | Nastaliq |
|---|---|---|
| ascender | 0.642 (the headline) | 0.714 (ا ل ک) |
| descender | 0.290 | 0.420 (م is deepest at 0.383, plus the Nastaliq cascade) |

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
