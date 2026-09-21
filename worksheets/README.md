# হাতের লেখার খাতা - handwriting worksheets

Printable A4 workbooks that teach a **Bengali** speaker to *write* **Devanagari**,
in the order `courses/bengali_to_hindi.html` teaches it: letters -> vowel signs ->
words -> sentences. Every instruction is in Bengali.

The PDFs are built once and committed. They are static files, meant to be sent to
a learner on request - nothing is generated on the fly.

## What is here

Two pairs so far, both teaching **Devanagari**, 169 pages each.

| Book | bengali_to_hindi | telugu_to_hindi | Pages | Contents |
|---|---|---|---|---|
| 1 | `01_svarabarna` | `01_achchulu` | 14 | 13 vowels |
| 2 | `02_byanjanbarna` | `02_hallulu` | 41 | 33 consonants by varga + 7 nukta |
| 3 | `03_matra` | `03_gunintalu` | 14 | the 13 forms of the क barakhadi |
| 4 | `04_juktakshar` | `04_samyuktakshara` | 35 | 66 conjuncts grouped by formation rule |
| 5 | `05_shabda_1` | `05_padalu_1` | 18 | 64 easy words (no conjunct, no nukta) |
| 6 | `06_shabda_2` | `06_padalu_2` | 17 | 58 harder words |
| 7 | `07_bakya_1` | `07_vakyalu_1` | 15 | 28 short sentences |
| 8 | `08_bakya_2` | `08_vakyalu_2` | 15 | 28 longer sentences |

Each pair has its own `index.html`.

## Same target, different bridges

The target is Devanagari for both pairs, so the ruling geometry, the font metrics
and the Hindi content are shared. What changes is not just the language of the
instructions but **which bridges are actually true**:

| | Bengali source | Telugu source |
|---|---|---|
| শিরোরেখা / శిరోరేఖ | Already drawn last, as the মাত্রা. A habit to transfer. | **New.** Telugu letters stand separately with no headline. Said plainly on every letter page. |
| Conjuncts | Same concept, many *identical* pairs (ক্ষ, জ্ঞ, স্ত). | Same concept, **opposite direction**. Telugu stacks the second consonant below as an ottu; Devanagari cuts the stem and puts it beside. |
| ड़ / ढ़ | Familiar - Bengali has ড় and ঢ়. | **New sounds.** Not in Telugu; taught as a retroflex flap. |
| Short e / o | Neither writes them. | Telugu has ఎ and ఒ; Hindi has only the long ए and ओ. Noted on the vowel cover. |

Getting these backwards would teach a Telugu learner something false, so they are
encoded per pair in `RULES`, `CONJ_RULES` and the per-letter notes, not translated.

## Adding a pair

For another Devanagari target, add an entry to `LANGS` (font, digits, interface
strings), extend `EQ_TE`-style equivalents, glosses and sentence translations, and
write the two rule sets. For a different target script you would also need to
remeasure the three font-metric ratios with `calibrate_font.html`.

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
python3 gen_worksheets.py                  # every pair
python3 gen_worksheets.py telugu_to_hindi  # just one
./build_pdfs.sh                            # renders A4 PDFs with headless Chrome
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
