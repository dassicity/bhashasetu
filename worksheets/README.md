# হাতের লেখার খাতা - handwriting worksheets

Printable A4 workbooks that teach a **Bengali** speaker to *write* **Devanagari**,
in the order `courses/bengali_to_hindi.html` teaches it: letters -> vowel signs ->
words -> sentences. Every instruction is in Bengali.

The PDFs are built once and committed. They are static files, meant to be sent to
a learner on request - nothing is generated on the fly.

## What is here

| Book | File | Pages | Contents |
|---|---|---|---|
| ১ স্বরবর্ণ | `01_svarabarna.pdf` | 14 | 13 vowels, one per page |
| ২ ব্যঞ্জনবর্ণ | `02_byanjanbarna.pdf` | 41 | 33 consonants by varga + 7 nukta letters |
| ৩ মাত্রা | `03_matra.pdf` | 14 | the 13 forms of the ক barakhadi |
| ৪ যুক্তাক্ষর | `04_juktakshar.pdf` | 35 | 66 conjuncts, grouped by the rule that forms them |
| ৫ শব্দ ১ | `05_shabda_1.pdf` | 18 | 64 easy words - no conjuncts, no nukta |
| ৬ শব্দ ২ | `06_shabda_2.pdf` | 17 | 58 harder words - conjuncts, nukta, long forms |
| ৭ বাক্য ১ | `07_bakya_1.pdf` | 15 | 28 short sentences built from শব্দ ১ |
| ৮ বাক্য ২ | `08_bakya_2.pdf` | 15 | 28 longer sentences built from শব্দ ২ |

169 pages total. `index.html` links them all.

## How the two parts are graded

Difficulty is defined by what the hand has to *draw*, not by meaning:

- **Part 1** - no conjunct, no nukta, short words, simple matras.
- **Part 2** - conjuncts (ক্ষ জ্ঞ ত্র স্ত), nukta (ড় ঢ় জ় ফ়), longer words, and
  sentences with questions, negation and postpositions.

Sentence books are built only from words that appear in the matching word book,
so nothing arrives that the hand has not already practised.

## Conjuncts: rules, not a thousand pairs

33 consonants make over a thousand theoretical pairs. Listing them all would be
useless, so book 4 teaches the four systems that generate them, with every
conjunct that actually occurs in Hindi:

1. **Half-form** - the left letter loses its vertical stem (স + ত = স্ত).
   Stemless letters (ট ড ঠ) stack vertically instead.
2. **The two faces of র** - before a consonant it climbs on top as the reph
   (ধর্ম); after one it hangs below as a slanted stroke (প্রেম).
3. **Irregular ligatures** - ক্ষ জ্ঞ ত্র শ্র দ্য দ্ধ, where the parts are no longer
   visible and the shape has to be memorised.
4. **য-ফলা and ব-ফলা**, and nasal clusters that may also be written with anusvara
   (অন্ত / অংত), both forms shown.

The bridge: Bengali has conjuncts too, and many are the *same* pair - ক্ষ, জ্ঞ,
স্ত. The concept transfers; only the drawing is new.

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
python3 gen_worksheets.py   # writes the HTML
./build_pdfs.sh             # renders A4 PDFs with headless Chrome
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
