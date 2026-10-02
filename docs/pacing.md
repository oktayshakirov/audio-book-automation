# Pacing rules

Where the silence goes. These are rules, not taste, so every track is paced
the same way and a re-render is reproducible.

Speed and the cost of splitting are in `voice.md`.

## Where the pauses come from

**The paragraph is the unit.** Each paragraph is sent to Kokoro as one call
and the silence is inserted between calls, never inside one.

That split is deliberate and it follows the measurement already recorded in
the sibling video project: synthesising **sentence by
sentence** makes every sentence a cold start, which measured 258, 271, 229,
227 and 246 Hz on five consecutive lines, against 199 Hz falling to 193 when
the same five went in as one utterance. A script of cold starts is what
"reading a list" sounds like.

So within a paragraph, the model keeps its own breaths, its own declination
and its own sentence rhythm, and we do not touch it. The short stabbed
sentences ("Whistle and buzz. Continually. Day and night.") are *meant* to be
inside one run. Forcing silence between them would sound stilted, not
dramatic.

## The four gaps

| Gap | Length | When |
|---|---|---|
| `TITLE` | 1.30s | After the chapter title line, before the body starts |
| `BEAT` | 1.00s | Either side of a **beat paragraph** (12 words or fewer) |
| `PARA` | 0.55s | Every other paragraph boundary |
| `QUOTE` | 0.90s | Before a quoted passage set as its own paragraph |

When two rules meet at the same boundary, **the longer one wins.** A beat
paragraph following a quote gets 1.00s, not 1.90s.

## Why a beat paragraph gets the long gap

The book's hammer lines are already written as one-line paragraphs, on
purpose:

> Tinnitus is not a disease that you caught.

> There is no day when it stops. There is a Tuesday.

> You will probably not feel much better.

Those lines do their work by sitting alone. A second of silence either side is
what makes them land as a statement rather than as the next sentence along.
Twelve words is the cutoff because it catches every one of them in the
thirteen tracks without catching ordinary short prose.

**One known cost.** A beat paragraph is a single sentence, so sending it as
its own call makes it a cold start, with the higher pitch onset the
measurements above describe. For a standalone hammer line that is arguably
right, since a fresh deliberate delivery is what the line wants. It is a
trade, not a free win, and if a particular beat sounds wrong it is the first
thing to check.

## Quotes

A quoted passage is written as its own paragraph in the script, so it inherits
a paragraph boundary automatically. There is no reliable way to detect a quote
from the text alone, since the book quotes without quotation marks:

> My ears whistle and buzz continually, he writes. Day and night.

So the rule is a **writing** rule, not a parser rule: **a quotation always
gets its own paragraph.** Keep it that way, and the pacing follows.

## Checking before you render

```bash
python -m audiobook_automation plan <manuscript.md>
```

Prints every gap, its rule and the paragraph it precedes, without synthesising
anything. Use it to confirm the beat rule is catching the lines you meant and
nothing else. Synthesis is slow; this is instant.

## The manuscript format the rules depend on

```
# Track 2 - Chapter 1: ...
Any notes, word counts, sources.
---
**[TITLE]** Chapter One. The Title.

**[BODY]**

First paragraph.

Second paragraph.
```

Everything above the `---` is for humans and is never spoken. Blank lines
separate paragraphs, and paragraphs are what the pacing acts on, so **how you
break paragraphs is a performance decision, not a typographic one.**
