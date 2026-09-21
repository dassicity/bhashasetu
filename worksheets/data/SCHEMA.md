# worksheets/data/{pair}.json

One file per pair. The course agent writes it; the generators read it. Never edit a
generator .py from an agent: five agents share three generator files and would collide.

All learner-facing strings are in the SOURCE language. No English. No em-dash characters
anywhere (use "-"). Words and sentences must come only from what the course actually teaches.

{
  "pair": "hindi_to_telugu",
  "source_iso": "hi",
  "target_iso": "te",
  "sub": "हिन्दी से तेलुगु",          // subtitle, source language
  "title": "लिखाई की कॉपी",            // cover title, source language
  "book": "कॉपी",                      // the word for "workbook", source language
  "primer": "बालबोध",                  // the source culture's first-primer word, if one exists
  "digits": "०१२३४५६७८९",             // source-script digits, index 0-9, ONE char each

  "ui": {                              // every caption on every sheet, source language
    "trace": "...", "times": "...", "fill": "...",
    "start_given": "...", "finish_row": "...",
    "self": "...", "fill_row": "...",
    "in_word": "...", "then_self": "...",
    "model": "...", "grey": "...", "hollow": "...", "faint": "...",
    "legend": "..."
  },

  "books": [                           // exactly 8, in order
    {"slug":"01_acchulu", "native":"అచ్చులు", "label":"स्वर",
     "bridge":"one or two sentences, source language, saying what this book asks of a
               writer who already writes THIS source script. Written per pair, never
               translated from another pair: the same fact inverts between sources."}
    // ... 8 entries. Books 5-6 are words part 1 and 2; books 7-8 are sentences part 1 and 2.
  ],

  "words1": {                          // 50-60 words total, grouped; easier half
    "<group label in source language>": [["<target word>","<source gloss>"], ...]
  },
  "words2": { ... },                   // 50-60 words, harder half: conjuncts, tatsama, idiom
  "sent1":  [["<target sentence>","<source gloss>"], ...],   // 25-30, only taught material
  "sent2":  [["<target sentence>","<source gloss>"], ...],   // 25-30, longer

  "khata_how": "2-4 sentences, source language, telling the learner how to use the books:
                print, how many times to trace, when to move on. Goes in the course."
}

Target-specific notes for books 1-4:
  Telugu  : acchulu, hallulu, gunintamulu, ottulu
  Tamil   : uyir, mei, uyirmei, pulli and the special letters. Tamil has no conjuncts:
            say so in the bridge rather than inventing a book.
  Urdu    : letters, the four positional forms, joined groups, and the marks. RTL.


## ADDED 2026-09-21 - these fields are REQUIRED, the generator hardcoded Bengali before

The worksheet generators previously served only Bengali-source pairs, so a lot of
source-language prose sat inside the .py files. It is now per-pair and comes from you.
Add these top-level keys:

  "words_word":    "<the source-language noun for 'word', used in book titles>",
  "sent_word":     "<the source-language noun for 'sentence'>",
  "index_blurb":   "<one sentence, source language: what these eight books are>",
  "print_note":    "<source language: print on A4 at 100 percent, with \"fit to page\" OFF.
                     The quoted control name stays in English on purpose - it is what the
                     print dialog actually says. This is the one allowed exception.>",

  "sub_words1":    "<cover subtitle for the easy word book, source language>",
  "sub_words2":    "<cover subtitle for the hard word book: conjuncts, tatsama, and the
                     roots that have no bridge back to the source language>",
  "sub_sent1":     "<cover subtitle for the easy sentence book>",
  "sub_sent2":     "<cover subtitle for the long sentence book>",

Books 3 and 4 additionally need a rule line, which is the single most important sentence
in the whole workbook. Add to those two entries in "books":

  "rule": "<source language, may contain <b> tags. State the bridge as a fact about a
            habit the learner ALREADY HAS, then say what changes. Written per pair.
            The same fact inverts between sources: a headline is an existing habit for a
            Bengali writer, a new one for a Telugu writer, and absent in Urdu. Never
            translate another pair's rule line.>"

All of this is learner-facing, so: source language only, and no em-dash characters.


## The letter inventories - read worksheets/data/targets/{te,ta,ur}.json

Books 1 to 4 are built from a letter inventory. The TARGET-script half of that inventory
already exists and is verified: the letters themselves, their Roman values, the example
words, and for Urdu which letters join to the left. You do not rewrite any of that, and
changing it will break the generator.

What is missing is the SOURCE-language half, and only you can write it. Copy the file for
your target into your pair file under a "letters" key, and fill every empty string:

  "eq"     the nearest letter in the SOURCE script. Follow the transliteration row for
           your source in STRUCTURE_VARIANTS. Where the source genuinely cannot carry the
           distinction, say so in the row rather than forcing a wrong letter. Mark a row
           that has no honest equivalent with the lightning mark the other courses use.
  "gloss"  the SOURCE-language meaning of the example word that is already in the row.
  "group"  the SOURCE-language label for the family this letter belongs to. Letters must
           be grouped by family, never listed flat.
  "note"   (gunintam / uyirmei / harakat rows) one short source-language line saying what
           the sign does.
  "name"   (Urdu only) the letter's name written in the source script.
  "sound"  (Urdu only) the sound written in the source script.
  "read"   (Urdu joining rows) how the joined form is read, in the source script.

Two things that decide whether this is any good:
- Group labels carry the teaching. "kantha varga" tells a learner why six letters sit
  together; "group 1" tells them nothing.
- An honest "the source has no letter for this" is worth more than a near-miss that
  teaches a wrong sound. Previous courses marked these and were better for it.


## Optional but wanted: "rules"

Each cover page carries a short numbered list headed "five things before you write".
If you can, add:

  "rules_head": "<source language heading, e.g. the equivalent of 'five things before you write'>",
  "rules": ["<five short source-language lines>", ...]

These are posture and hand advice for someone about to write THIS target script with a
hand trained on THIS source script: stroke direction, where the hand rests, what to do
slowly, what the common first mistake is. Pair-specific. If you omit this, you will be
asked for it when you deliver, so it is cheaper to write it now.

Note also: each entry in "books" already has a "bridge", and that bridge is used as the
cover subtitle for its book. Write all eight.
