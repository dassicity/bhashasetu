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

## 3. Modifications - documented now, attempt later

### 3a. Rebuild existing v1 courses under the v2 brief
All 57 courses carry `data-version="1"`. Rebuild order: thinnest first (they gain the most), strong ones last.

Tier 1 (under 800 lines, or off-structure):
- [ ] `punjabi_to_telugu` (663) · [ ] `malayalam_to_tamil` (682) · [ ] `kannada_to_punjabi` (696) · [ ] `urdu_to_punjabi` (708)
- [ ] `kannada_to_telugu` (726) · [ ] `kannada_to_malayalam` (727) · [ ] `malayalam_to_kannada` (736) · [ ] `malayalam_to_punjabi` (737)
- [ ] `urdu_to_tamil` (740, no `.aside` markup) · [ ] `malayalam_to_bengali` (749) · [ ] `kannada_to_hindi` (757) · [ ] `malayalam_to_telugu` (774)
- [ ] `malayalam_to_hindi` (795) · [ ] `urdu_to_bengali` (813) · [ ] `punjabi_to_hindi` (854) · [ ] `urdu_to_telugu` (877)
- [ ] `punjabi_to_tamil` (1121, no `<h3>` sections)

Tier 2 (800–1100 lines):
- [ ] `kannada_to_tamil` · [ ] `punjabi_to_malayalam` · [ ] `punjabi_to_urdu` · [ ] `kannada_to_urdu` · [ ] `urdu_to_hindi` · [ ] `urdu_to_kannada` · [ ] `punjabi_to_bengali` · [ ] `urdu_to_malayalam`

Tier 3 (strong v1 courses; rebuild last, mostly to add v2 mechanics):
- [ ] all Bengali-source (7) · [ ] all Hindi-source (7, plus `hindi_to_marathi`) · [ ] all Tamil-source (7) · [ ] all Telugu-source (7) · [ ] `punjabi_to_kannada` · [ ] `malayalam_to_urdu` · [ ] `kannada_to_bengali`

Cross-family v1 courses (Indo-Aryan↔Dravidian, 32 of the 56) should be rebuilt on corridor C or D plans (12 or 11 stages), not the baseline.

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
