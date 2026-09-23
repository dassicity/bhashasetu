# Recovered partial courses, 2026-09-22

Four agents were killed by a 600s no-progress watchdog after doing their research and most
of their writing. This is what survived in the session scratchpad, copied here because the
scratchpad is session-scoped and gets cleaned.

Each directory holds numbered HTML fragments: a head (doctype, stylesheet, masthead, tabs),
one file per stage, and in some cases a tail (progress bar, router, colophon).

## Before reusing any of it

- **Some directories hold TWO overlapping attempts.** `hindi_to_malayalam` has both a
  `NN_name.html` series and an `sNN.html` series; `hindi_to_bengali` and `bengali_to_punjabi`
  likewise have `NN_` and `pNN_` series. Concatenating everything produces duplicate
  `<html>`, `<body>` and `<style>` tags. Pick ONE series.
- **None of them is complete.** An earlier version of this file said all four had their full
  stage sets. That was wrong: it counted every `data-stage` attribute, and the tab buttons in
  each head carry those too. Counting real `<section class="stage">` elements gives:

| pair | needs | best series | real stages | still to write |
|---|---|---|---|---|
| bengali_to_punjabi | 0-9 | `pNN_stageNN` + `p00_head_a` (attempt B) | 0-5 | stages 6-9, tail, sidecar, workbook data |
| hindi_to_bengali | 0-9 | `pNN_` | 0-8 | stage 9, tail, sidecar, workbook data |
| hindi_to_kannada | 0-11 | `NN_` | 0-5 | stages 6-11, tail, sidecar (workbook data exists) |
| hindi_to_malayalam | 0-11 | `sNN` | 0-9 | stages 10-11, tail, sidecar (workbook data exists) |

- **Series cannot be mixed.** Where two attempts exist they split the stages differently, and
  each head's tab titles match only its own attempt. In `bengali_to_punjabi` both attempts use
  a `p` prefix and interleave by filename: attempt B is `p00_head_a` plus `pNN_stageNN`, attempt
  A is `p01_head` plus `pNN_sN`. In attempt B, `p03_stage02a` leaves a section and a div open and
  `p03_stage02b` closes them.
- **Do not overwrite a working v1 with fewer stages.** Every v1 here has its full stage count.
  Replacing it with a partial v2 removes content from the live course. Finish the missing
  stages first, using the v1's own later stages as the content source.

## Why they stalled

Not the briefs. The platform degraded: agents began stalling during reading, then on their
first message, and the session's own tool calls started timing out on the safety classifier
at the same time. Retrying into that burns full token cost for nothing.
