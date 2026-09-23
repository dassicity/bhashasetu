# BHASHASETU - tasks

Started 2026-09-20. Brief version 2 (`prompts/MASTER_BRIEF.md`). Status marks: `[ ]` open · `[~]` in progress · `[x]` done.

## 1. Spec amendments (done first)

- [x] Cultural anchors ("references") added to the brief as a required element, with markup in `V2_SNIPPETS.html` (block 5) and a field in the knowledge sidecar
- [x] Corridor F (Indian → foreign: Korean, Spanish) added to `STRUCTURE_VARIANTS.md` with stage plans, extra data fields, and source-script transliteration rows
- [x] Target fact sheets: `prompts/targets/korean.md`, `prompts/targets/spanish.md`
- [x] Checker: `prompts/check_course.py` (structure, v2 requirements, English leaks, sidecar)
- [x] Index: "Beyond India" target group, Korean and Spanish cards, fonts, counts, VERSIONS entries

## 2. New courses - COMPLETE (all v2, corridor F, built and verified 2026-09-20)

| # | Course | Prompt sheet | Built | Sidecar | Checker | Browser | Index |
|---|---|---|---|---|---|---|---|
| 1 | `bengali_to_korean` | [x] | [x] | [x] | [x] | [x] | [x] |
| 2 | `telugu_to_korean` | [x] | [x] | [x] | [x] | [x] | [x] |
| 3 | `kannada_to_korean` | [x] | [x] | [x] | [x] | [x] | [x] |
| 4 | `bengali_to_spanish` | [x] | [x] | [x] | [x] | [x] | [x] |
| 5 | `telugu_to_spanish` | [x] | [x] | [x] | [x] | [x] | [x] |
| 6 | `kannada_to_spanish` | [x] | [x] | [x] | [x] | [x] | [x] |

Progress tracker inside each course (saved stage, per-stage "done" button, dots) comes from `V2_SNIPPETS.html` block 4 and block 2 and is part of "Built".

All six pass `prompts/check_course.py` and were checked live in the browser (desktop + 375px, hash routing, self-checks, speak buttons, no console errors). Each has a sidecar in `prompts/pair_knowledge/` recording its aha moments, anchors with verification URLs, and what was dropped for lack of evidence.


## 2b. Handwriting worksheets - ten pairs

Static A4 PDFs, built once, sent on request. Three generators, because three script
families sit on the page differently. Since 2026-09-21 a pair is a JSON file in
`worksheets/data/`, not code: see `worksheets/README.md`. All rendered by `worksheets/build_pdfs.sh`
with headless Chrome.

| Pair | Target script | Generator | Pages | Linked into course |
|---|---|---|---|---|
| `bengali_to_hindi` | Devanagari | `gen_worksheets.py` | 169 | [x] stages 0-5 |
| `telugu_to_hindi` | Devanagari | `gen_worksheets.py` | 169 | [x] stages 0,1,2,3,4,6 |
| `bengali_to_urdu` | Perso-Arabic | `gen_worksheets_urdu.py` | 136 | [x] stages 0-5 |
| `bengali_to_telugu` | Telugu | `gen_worksheets_brahmic.py` | 138 | [x] stages 0,1,2,3,4,6 |
| `bengali_to_tamil` | Tamil | `gen_brahmic.py` | 121 | [x] stages 0,1,2,3,4,6 |
| `telugu_to_urdu` | Perso-Arabic | `gen_urdu.py` | 138 | [x] 6 blocks |
| `telugu_to_tamil` | Tamil | `gen_brahmic.py` | 126 | [x] 7 blocks |
| `hindi_to_telugu` | Telugu | `gen_brahmic.py` | 141 | [x] 6 blocks |
| `hindi_to_tamil` | Tamil | `gen_brahmic.py` | 125 | [x] 7 blocks |
| `kannada_to_telugu` | Telugu | `gen_brahmic.py` | 142 | [x] 6 blocks |

Books 1, 2 and 5-8 are the same everywhere: vowels, consonants, easy words, harder
words, short sentences, longer sentences. **Books 3 and 4 are where scripts diverge:**

| Target | Book 3 | Book 4 |
|---|---|---|
| Devanagari | matras | 66 conjuncts by formation rule |
| Urdu | harakat, mostly unwritten | joining; the nine letters that never join leftward |
| Telugu | గుణింతం | ఒత్తు, hung below |
| Tamil | உயிர்மெய் | புள்ளி, which is **not** a conjunct |

**Measured metrics** (canvas `TextMetrics`; `calibrate_font.html`,
`calibrate_nastaliq.html`, `calibrate_brahmic.html`), as fractions of font size:

| | body / ascender | signs above | signs below |
|---|---|---|---|
| Devanagari | 0.642 (headline) | 0.925 | 0.290 |
| Nastaliq | 0.714 | | 0.420 |
| Telugu | 0.772 | 1.003 | 0.444 |
| Tamil | 0.497 | 0.787 | 0.250 |

Tamil's body is barely half Telugu's, so the same letter height needs a far larger
font size. Guessing instead of measuring would have made one of them wrong.

**Bridges are written per pair, never translated**, because they invert. The headline
is an existing habit for a Bengali writer, absent for a Telugu or Tamil one, and
absent entirely in Urdu. Conjuncts are the same idea in Devanagari, the opposite
direction in Telugu (ottu below), and **not a category at all** in Tamil.

- [ ] more pairs: another Devanagari, Telugu or Tamil target needs only a config entry
      plus equivalents, glosses and sentence translations. Another Perso-Arabic target
      reuses the Urdu generator. A new script needs its three ratios measured first.
- [ ] optional: true stroke-order arrows (needs per-glyph vector data, not available)
- [ ] discoverability: `.khata` blocks sit at the bottom of each stage and are easy to
      miss. Decide between a persistent masthead pointer and a dedicated tab.

## 3. Modifications - documented now, attempt later

### 3a. Convert existing v1 courses to the v2 brief

58 courses carry `data-version="1"`. Conversion is cheaper than a rebuild where the v1
prose is already good: keep the hand-written Bengali/Hindi/Tamil text, add the v2 layer.

**What a conversion means, per course** (from `prompts/MASTER_BRIEF.md`):

| # | Requirement |
|---|---|
| 1 | `data-version="2"`, `data-built`, `data-pair`, `data-target`, `data-speak-label`; meta tag; v2 badge |
| 2 | Self-check at the end of every stage from 01 to the last before Literature, 5-8 items, 2+ formats |
| 3 | Graded passage in every stage from 04 on, except the reading stage and Literature |
| 4 | Vocabulary split: 04 function words and verbs, 07 semantic fields, 08 phrases only, no word twice |
| 5 | Source-script transliteration primary, Roman secondary or dropped |
| 6 | `data-say` on every card plus the speak script |
| 7 | v2 router: hash routing, saved stage, saved completed checks, resume hint |
| 8 | 8+ verified cultural anchors, one per stage where one exists |
| 9 | 8+ false friends |
| 10 | Numbers only with the working shown |
| 11 | Sidecar `prompts/pair_knowledge/{pair}.json` |
| 12 | `VERSIONS` entry in `index.html` bumped to v2 |
| 13 | Passes `python3 prompts/check_course.py courses/{pair}.html` with no `--v1` |

**Done**

| Course | Corridor | Converted | Result |
|---|---|---|---|
| `bengali_to_hindi` | B (cross-script, same family) | 2026-09-21 | [x] 10 stages, 167 KB, 8 self-checks, 7 passages, 10 anchors, 183 `data-say`, 12 false friends. All six `.khata` blocks byte-identical. Checker PASS. |
| `telugu_to_hindi` | **D (Dravidian to Indo-Aryan)** | 2026-09-21 | [x] **10 stages to 11** - the single grammar stage was split into నామరూపం (gender, agreement, oblique, ergative ने) and క్రియ (copula, tenses, compound verbs). 243 KB, 9 self-checks, 8 passages, 11 anchors, 256 `data-say`, 87 gender tags, 10 false friends. Six `.khata` blocks added after conversion. Checker PASS. |
| `bengali_to_urdu` | **E (Perso-Arabic target)** | 2026-09-21 | [x] Stages 01-03 **rewritten** - v1 taught an abjad using Brahmic categories (স্বরবর্ণ / ব্যঞ্জনবর্ণ) and mentioned the four positional forms once. Now হরফ grouped by shape with all four forms, স্বরচিহ্ন (and which are normally unwritten), যোগ ও দিক. 258 KB, 8 self-checks, 7 passages, 11 anchors, 281 `data-say`, **823 `dir="rtl"`** (v1 had none), 12 false friends. Six `.khata` blocks added after. Checker PASS. |
| `bengali_to_telugu` | **C (Indo-Aryan to Dravidian)** | 2026-09-21 | [x] **10 stages to 12** - the one grammar stage split into নাম ও বিভক্তি (cases, oblique, dative subject), ক্রিয়া (tenses, the negative as its own paradigm) and বাক্যের ছাঁচ (relative and verbal participles). 202 KB, 10 self-checks, 9 passages, 14 anchors, 218 `data-say`, 20 false friends from the DSAL research. Six `.khata` blocks added after. Checker PASS. |
| `bengali_to_tamil` | **C (Indo-Aryan to Dravidian)** | 2026-09-21 | [x] **10 stages to 12**, same three-way grammar split. 218 KB, 10 self-checks, 9 passages, 13 anchors, 249 `data-say`, 10 false friends from DSAL. The Bengali pronunciation line does real work here: Tamil writes one letter for k/g and t/d, so it shows what is *heard* (நன்றி = নন্দ্রি), which Roman "naṉṟi" hides. Six `.khata` blocks added after. Checker PASS. |

| `telugu_to_urdu` | **E (Perso-Arabic target)** | 2026-09-21 | [x] Stages 01-03 rewritten for the abjad. 10 stages, 8 self-checks, 11 anchors, 226 `data-say`, 10 false friends verified in Platts and Brown. The Deccan history is the spine and is genuinely shared ground: Charminar, the Northern Circars from *sarkar*, Osmania's 1917 firman, Makhdoom, Dasarathi's *Ghalib Geetalu*. The Bengali course's 1952 framing was deliberately NOT imported. 6 `.khata` blocks, 138 pages. Checker PASS. |
| `telugu_to_tamil` | B (cross-script, same family) | 2026-09-21 | [x] Both Dravidian, so the grammar skeleton is shared and the stages go to the script and the sound system. Tamil writes one letter for k/g, t/d, p/b, so stage 02 is a four-position voicing table and the Telugu line shows what is *heard*. Book 4 is the pulli book, not an ottu book, because Tamil has no ottu: the hardest habit in Telugu handwriting is simply absent. 10 anchors, 225 `data-say`, 10 DSAL-verified false friends. 7 `.khata` blocks, 126 pages. Checker PASS. |
| `hindi_to_telugu` | **C (Indo-Aryan to Dravidian)** | 2026-09-21 | [x] **10 stages to 12.** Agglutination owns stage 05 alone, verbs 06, sentence patterns 07. Every noun card carries a mahat/amahat tag. Three bridges exist only for a Hindi source: मुझे = నాకు one-to-one, -इए = -ండి, -कर = -ఇ. 12 anchors, 274 `data-say`, 17 false friends. Cut three v1 numbers that could not be derived, including "47 of 44 phonemes", which is impossible on its face. 6 `.khata` blocks, 141 pages. Checker PASS. |
| `hindi_to_tamil` | **C (Indo-Aryan to Dravidian)** | 2026-09-21 | [x] **10 stages to 12.** Devanagari already owns ऴ ळ ऱ ऎ ऒ, so unlike the Bengali course nothing had to be collapsed; only ன has no honest Devanagari letter and the course says so. The oblique stem, the dative subject and -कर carry the corridor. Voicing is anchored on Hindi's own spellings: मदुरै, इडली, पोंगल already encode it. 13 anchors, 243 `data-say`, 12 false friends. Language politics in stage 10 carries both halves, the 1965 agitation and Gandhi's Madras Hindi Prachar Sabha, and lands on the learner: chosen and imposed are not the same thing. 7 `.khata` blocks, 125 pages. Checker PASS. |
| `kannada_to_telugu` | B (cross-script, same family) | 2026-09-21 | [x] Sibling scripts, so similarity is the trap rather than the gift: a Telugu word transposed letter-for-letter into Kannada often spells a real, different Kannada word. Stages 01-03 cover the eight drifted shapes, the four look-alike pairs, and the fact that Telugu's upper vowel signs swallow the talakattu where Kannada's merely attach. 10 anchors, 269 `data-say`, 12 false friends from Kittel and Brown. 6 `.khata` blocks, 142 pages. Its cover rules overran the fixed-height cover and added a page to every book; trimmed from 1334 to 781 characters with all five findings intact, and the generator now guards the limit. Also caught a class collision the reference would have caused: `.kn` is already this course's Kannada font class, and the reference's `.kn` rule sets a monospace face with no Kannada glyphs, so the book numbers would have rendered as tofu. Renamed to `.kbn`. Checker PASS. |

**Operational note for conversions (learned the hard way, 2026-09-21).** The
`bengali_to_telugu` and `bengali_to_tamil` agents stalled on a 600s no-progress
watchdog three times between them. Two causes, both avoidable:
- **Parallel web-research fan-outs.** Batching ten WebSearch/WebFetch calls in one
  block is what trips the watchdog. Cap it at two per tool block.
- **Subagents.** The first attempt spawned three researchers, which stalled the
  parent as well. Tell conversion agents not to spawn any.
Also tell them to write in pieces under about 40 KB and to save each finished stage
to its own scratchpad file, so a stall costs one stage rather than the whole course.
Nothing was lost either time, because the course file is only written at the end.

**A stalled agent's work can still be worth having.** One researcher that outlived its
stalled parent returned 36 Bengali-Telugu false friends verified against Brown's Telugu
dictionary and Samsad Bengali at DSAL, with 20 documented rejections. Saved to
`prompts/research/bengali_telugu_false_friends.md`.

**Also fixed while converting `bengali_to_hindi`** (v1 content errors found by fact-checking):
- Nirala's "Woh Todti Patthar" was dated 1935 without support; now hedged to composition c. 1935, collected in the second edition of *Anamika*
- Begum Rokeya's *Sultana's Dream* was implied to be Bengali; it was written in English (1905, *Indian Ladies' Magazine*, Madras)
- Nazrul's "Bidrohi" now carries both dates (written 1921, published January 1922)
- Both YouTube embeds were dead `listType=search` URLs, which now need an API key; replaced with two oEmbed-verified IDs
- Seven English words were sitting in learner-facing prose

**Order for the rest.** Thinnest first, since they gain the most. Cross-family pairs
(Indo-Aryan to Dravidian and back, 32 of the 56) should move to corridor C or D plans,
12 or 11 stages, not the baseline 10.

Tier 1 (under 800 lines, or off-structure):
- [ ] `punjabi_to_telugu` (663) · [ ] `malayalam_to_tamil` (682) · [ ] `kannada_to_punjabi` (696) · [ ] `urdu_to_punjabi` (708)
- [ ] `kannada_to_telugu` (726) · [ ] `kannada_to_malayalam` (727) · [ ] `malayalam_to_kannada` (736) · [ ] `malayalam_to_punjabi` (737)
- [ ] `urdu_to_tamil` (740, no `.aside` markup) · [ ] `malayalam_to_bengali` (749) · [ ] `kannada_to_hindi` (757) · [ ] `malayalam_to_telugu` (774)
- [ ] `malayalam_to_hindi` (795) · [ ] `urdu_to_bengali` (813) · [ ] `punjabi_to_hindi` (854) · [ ] `urdu_to_telugu` (877)
- [ ] `punjabi_to_tamil` (1121, no `<h3>` sections)

Tier 2 (800-1100 lines):
- [ ] `kannada_to_tamil` · [ ] `punjabi_to_malayalam` · [ ] `punjabi_to_urdu` · [ ] `kannada_to_urdu` · [ ] `urdu_to_hindi` · [ ] `urdu_to_kannada` · [ ] `punjabi_to_bengali` · [ ] `urdu_to_malayalam`

Tier 3 (strong v1 courses; convert last, mostly to add the v2 mechanics):
- [ ] remaining Bengali-source (6) · [ ] all Hindi-source (7, plus `hindi_to_marathi`) · [ ] all Tamil-source (7) · [ ] all Telugu-source (7) · [ ] `punjabi_to_kannada` · [ ] `malayalam_to_urdu` · [ ] `kannada_to_bengali`

**The 1952 Language Movement is in `bengali_to_urdu` stage 00, not buried.** A Bengali
opening a course to learn Urdu has it in mind on page one, so the course meets it on page
one: the dates, the names of the six who died, UNESCO 1999 and the UN in 2002, and then
plainly where the quarrel lay - with a state policy that put one language above all others,
not with the Urdu language, not with its speakers, "not with Ghalib, Mir or Faiz at all".
It closes by turning the principle both ways: no one's mother tongue can be taken, and
learning someone else's is not giving up your own.

**Corridor matters more than it looks.** `telugu_to_hindi` is Dravidian to Indo-Aryan,
so brief rule 11 forced it from 10 stages to the 11-stage corridor D plan. A cross-family
course with one grammar stage is still a v1 course no matter how good its prose is.
32 of the 56 sister-language courses are cross-family and will need the same split.

**Three things learned converting the first two:**
- Agent-written courses reintroduce em-dashes by default. The checker now fails on them; check after every conversion.
- v1 courses carry their own bugs. `bengali_to_hindi` had a stray `</p>` that left `section` and `main` unclosed, and English "Stage 00" labels. `telugu_to_hindi` had an 8px mobile overflow from `.guni-wrap` out-denting further than the wrapper's padding. Run the checker with `--v1` before converting to see what is pre-existing.
- Both courses' YouTube embeds were dead: v1 used `listType=search` playlist URLs with no video ID, which now need an API key. Assume every v1 embed is broken and re-verify.

### 3b. Add cultural anchors to `hindi_to_marathi` (built before the anchors rule)
- [ ] at least eight anchors; Sairat, Lata Mangeshkar, Natsamrat already in prose but not in anchor markup

### 3c. Repository hygiene
- [ ] Remove the old speak-button experiment from `hindi_to_bengali`, `tamil_to_kannada`, `urdu_to_hindi` (superseded by snippets block 3)
- [ ] Stop gitignoring `prompts/` docs (`MASTER_BRIEF.md`, `STRUCTURE_VARIANTS.md`, `V2_SNIPPETS.html`, `USAGE.md`, `targets/`, `pair_knowledge/`, `check_course.py`) so the spec is versioned
- [ ] Restore or rebuild the `data/` directory `gen_prompts.js` expects (languages, comparisons); fix the glossing bugs seen in v1 prompts
- [ ] Marathi pairs remaining: 15 (`marathi_to_*` ×8, `*_to_marathi` ×7)

### 3d. Index
- [ ] Per-source "coming soon" for foreign targets is automatic; revisit when more sources get foreign courses
- [ ] Consider a v2 filter/legend count on the index once several v2 courses exist

**What this batch taught (2026-09-21, five courses in parallel).** The stall advice above
held: capping web calls at two per block and forbidding subagents meant no agent stalled
once in five. Three new lessons, all of them things a checker caught and a reading would
not have:

- **Sheet count against PDF page count is the test that matters.** Every `kannada_to_telugu`
  book came out exactly one page longer than its sheet count. A uniform offset means the
  cover, the one page every book shares: 1334 characters of cover rules against the
  reference's 649 spilled onto a second page, and all eight books inherited it. The
  generator now refuses to build when the rules exceed what the cover holds.
- **Check the fonts actually embedded, not just that the PDF renders.** `pdffonts` showed
  the Telugu-source Urdu workbook embedding Noto Serif Bengali and rendering its Telugu in
  a macOS system fallback, because both generators requested the Bengali family whatever
  the source was. It would have printed differently on any other machine. The font now
  follows `source_iso`.
- **Reference data carries the reference's language.** The Tamil letter spine handed to the
  agents had its `parts` column pre-filled with Bengali, because it was extracted from the
  Bengali course without noticing that column is source-language for Tamil. An agent caught
  it in its own copy. Any new spine should be checked for source-script leakage before it
  goes out, with a plain codepoint-range count.

**Worth doing before the next batch.** Agents delivered courses and worksheet data reliably,
but none of them produced the six source-language worksheet strings (`same_sign`,
`words_hint`, `sent_seq`, `sent_head`, `sent_hint`, `rules`) without being asked in a second
round, because those were added to the schema after they had started. Put them in the brief
from the start and the batch is one round shorter.

## 2c. Infrastructure and discoverability (2026-09-22)

**Worksheet discoverability, decided.** The `.khata` blocks sit at the bottom of each stage,
which is why the Telugu-to-Hindi workbooks looked missing once. All ten worksheet courses now
also carry a persistent `.khata-ptr` pill under the masthead, outside every `section.stage`
so the stage router cannot hide it, linking to that pair's workbook index with its real page
count in the source script. Verified on all ten: pointer present, placed before the first
stage section, claimed page count equal to the actual sum of the PDFs, all links resolving,
zero em-dashes, checker PASS.

**All three generators are now JSON-driven.** `gen_worksheets.py` became `gen_deva.py` and is
deleted; `gen_brahmic.py` and `gen_urdu.py` were converted the day before. A pair is now a
file in `worksheets/data/`, and adding a pair touches no Python. Each conversion was proved by
rebuilding the already-shipped pairs and matching the PDFs book for book: 169, 169, 139, 122,
136 pages, no mismatches.

**Kannada and Malayalam calibrated as target scripts** (see `worksheets/README.md` for the
table and the method). Telugu was re-measured as a control and reproduced `body` 0.772
exactly, which also revealed that the shipped `top`/`bot` numbers carry about 0.016 of
deliberate headroom; the same was applied to the new scripts. Neither has a letter spine yet,
and the first agent to build a course with that target should produce one.

### Four bugs found, three of them already shipped

- **Telugu learners were being shown Bengali.** `gen_worksheets.py` held two pairs at once,
  with a Telugu override map over Bengali defaults. The overrides covered letter equivalents
  and glosses but not the word-group headings or the consonant varga labels, so the printed
  `telugu_to_hindi` workbooks carried about 200 runs of Bengali across three books: a Telugu
  word book headed সর্বনাম, শরীর, পরিবার. Two of the 23 labels were also wrong in content,
  not just language, telling a Telugu reader that "Bengali's ড় ঢ় are right here" when Telugu
  has no such sound. All 23 rewritten in Telugu, PDFs rebuilt, 169 pages unchanged.
- **`telugu_to_urdu.html` had a duplicated `<style>` tag** at lines 13-14, in the committed
  file. The inner tag was parsed as CSS text, which invalidated the selector of the whole
  `:root` block, so **every CSS variable in that course was undefined at runtime** and the
  page rendered with none of its palette. One line deleted. All 63 courses and `index.html`
  were scanned; no other file is unbalanced.
- **Wrong fonts embedded in the PDFs.** Both generators requested Noto Serif Bengali whatever
  the source language was, so a Telugu or Hindi source silently fell back to a system font and
  would print differently on another machine. Caught with `pdffonts`, not by looking. The font
  now follows `source_iso`.
- **Stale page counts inside two courses.** Topping up word book 2 from 48 to 52 words grew
  book 6 by a page; the PDFs were rebuilt but the numbers printed inside
  `bengali_to_telugu` and `bengali_to_tamil` were not. Both now sum correctly.

### The check that keeps paying

Sheet count against PDF page count catches things reading never will: the cover overflow that
added a page to all eight Kannada books, and the conjunct batching error during the Brahmic
conversion. `audit()` now also refuses to build a pair file containing characters from any
Indic script other than its own source, which is the mechanical form of the Bengali-labels bug.

