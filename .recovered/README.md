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
- **Every one has its full stage set.** Corridor B pairs carry stages 0 to 9, corridor C
  pairs 0 to 11. What is missing from each is only the TAIL: the closing `</div></main>`,
  the v2 router script, the progress bar and the colophon, then `</body></html>`.
  `prompts/kit/03_router_and_footer.html` is exactly that block, but its footer prose is
  Bengali, so the router can be copied as-is while the button labels and colophon must be
  rewritten in the course's own source language.

### Which series to use

| pair | series | files | stages | what it needs |
|---|---|---|---|---|
| bengali_to_punjabi | `pNN_` | 14 | 0-9 | tail, and one stray unclosed div |
| hindi_to_bengali | `pNN_` | 10 | 0-9 | tail, and one stray unclosed div |
| hindi_to_kannada | `NN_` | 7 | 0-11 | tail, and one stray unclosed div |
| hindi_to_malayalam | `sNN` | 10 | 0-9 | balanced already, needs head check plus tail |

Assemble by sorting the chosen series by filename, concatenating, then appending the tail.
Run `python3 prompts/check_course.py` afterwards: it will name anything still missing.
- The research behind them is the expensive part and it is embedded in the prose: verified
  anchors, dictionary citations, example words. That is what is worth recovering.

## Why they stalled

Not the briefs. The platform degraded: agents began stalling during reading, then on their
first message, and the session's own tool calls started timing out on the safety classifier
at the same time. Retrying into that burns full token cost for nothing.
