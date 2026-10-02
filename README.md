# audio-book-automation

Turn a written manuscript into a distributable audiobook, locally and for
free. Local Kokoro synthesis, rule-based pacing, and a pronunciation lexicon
you can verify instead of guess at.

Built while making a real 13-track, ~60-minute title. Everything in `docs/` is
a measurement or a mistake that cost something, not advice.

Sibling project: [video-edit-automation](https://github.com/oktayshakirov/video-edit-automation).

## What it does

- **Paces by rule.** The paragraph is the synthesis unit; silence goes between
  calls, never inside one. A short paragraph standing alone is a *beat* and
  gets a longer gap either side, because that is how a hammer line is read.
- **Fixes pronunciation at source.** Kokoro phonemizes from spelling, so the
  lexicon respells words for the engine and records the IPA before and after.
  `pronounce verify` re-measures it.
- **Measures everything.** Runtime, words per minute and pause time come from
  the rendered audio. Word count times an assumed rate is a proxy, and it was
  wrong by 30% here.

## Install

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
brew install ffmpeg espeak-ng
```

The Kokoro model (~350MB) lives in `~/.local/share/kokoro`, overridable with
`KOKORO_HOME`.

## Use

```bash
python -m audiobook_automation plan      manuscript/02-ch01.md
python -m audiobook_automation calibrate manuscript/02-ch01.md --speeds 0.84 0.88 0.92
python -m audiobook_automation render    manuscript/02-ch01.md -o out
python -m audiobook_automation book      manuscript/ -o out
python -m audiobook_automation pronounce check manuscript/*.md
python -m audiobook_automation voices
```

`plan` is a dry run: it prints every gap and the rule behind it without
synthesising. Use it before every render, because synthesis is slow and the
pacing is the part you will get wrong.

## Manuscript format

```
# Track 2 - Chapter 1: Beethoven's Letter from Vienna
Target 6:00 / 900 words. Sources: ...
---
**[TITLE]** Chapter One. Beethoven's Letter from Vienna.

**[BODY]**

First paragraph.

A hammer line.
```

Everything above the `---` is for humans and is never spoken. Blank lines
separate paragraphs, and paragraphs drive the pacing, so **how you break
paragraphs is a performance decision, not a typographic one.**

## Where the content lives

```
projects/<book>/
  <book>.py            the build recipe - narrator, target pace, pinned speeds
  book/                git-ignored
    manuscript/        the tracks, one .md per track
    PLAN.md            format, voice decisions, what is still open
    SOURCES.md         a row per factual claim, with its status
```

**`projects/*/book/` is git-ignored, and that is a decision rather than an
oversight.** This repo is public and a finished manuscript is a paid product,
so the text stays on disk and out of history. The machinery, the docs and the
build recipe are the shareable parts; the book is not.

Do not remove that rule to be helpful. If a book's text is ever published it
goes to its own site, which is a separate publishing decision for its author
to make.

Rendered audio goes wherever the recipe points - by default somewhere outside
the repo, since it is large and regenerable.

## Docs

| | |
|---|---|
| [`docs/voice.md`](docs/voice.md) | Choosing a narrator and a speed. **Read this first.** |
| [`docs/pacing.md`](docs/pacing.md) | Where the silence goes, and why the paragraph is the unit |
| [`docs/pronunciation.md`](docs/pronunciation.md) | What espeak gets wrong and how to check |
| [`docs/structure.md`](docs/structure.md) | The short-audiobook format, reverse-engineered |
| [`docs/sourcing.md`](docs/sourcing.md) | Factual discipline. Seven of thirteen claims were overstated on the first book |
| [`docs/distribution.md`](docs/distribution.md) | Platform rules for AI narration. Decide **before** you narrate |

## Three things that cost the most time

**Judge speed by measured words per minute, not the speed parameter.** The
same 192 words measured 196 wpm as one call and 147 wpm split across seven.
The parameter means different things in different modes.

**"Robotic" usually means too slow.** Kokoro degrades when pushed far below
its natural range. The instinct to slow a synthetic voice down makes it worse.

**The word that sounds wrong may not be the wrong word.** A reported
"Beethoven" problem was actually "Ludwig" immediately before it, plus a
too-slow read. Check the neighbours first.
