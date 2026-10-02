# Voice and speed

How a written paragraph becomes audio, and how to choose a narrator without
guessing.

## Judge speed by measured wpm, never by the speed parameter

This is the single most important thing in this file.

Kokoro's `speed` parameter does **not** mean the same thing depending on how
the text is chunked. The same 192 words at the same setting measured:

- **58.8s as one call** = 196 wpm
- **78.5s split across seven paragraph calls** = 147 wpm

A 33% difference from chunking alone. So a speed that sounded right in one
mode is wrong in the other, and any note that records only the parameter is
useless. **Record wpm.**

## Paragraph splitting costs about 16% of pace

The first theory was trailing silence, and it is partly true: Kokoro leaves
roughly 2.8s of near-silence on every call, which is invisible when a chapter
is one call and dominant at one call per paragraph.

But trimming does not explain it. Trimming the sample array at -40dB below
peak recovers only 0.5 to 0.9s per call, and the head of each segment already
carries signal at -3dB, so speech starts almost immediately. **After
trimming**, a standalone paragraph still reads at 164 wpm while the same words
inside a long run read at 196.

**Kokoro genuinely speaks a short standalone utterance more slowly than the
same text embedded in a longer one.** It is the cold-start effect, appearing
at paragraph scale.

So pauses are not free. They buy drama and cost roughly 16% of pace, and the
speed setting has to be raised to pay for it. Trim anyway, so the gaps in
`pacing.md` are the only silence in the file and mean what they say.

## The converged speed, and how it was found

Every row below is a real measurement on the same passage, with a real verdict
from the author. Audiobook convention says 150 to 160 wpm; this landed higher,
which is a reminder to converge by ear rather than by convention.

Single call, no pauses:

| speed | wpm | verdict |
|---|---|---|
| 0.60 | 137 | |
| 0.67 | 151 | **too slow, robotic** |
| 0.74 | 179 | too slow |
| 0.80 | 200 | too fast |
| 0.90 | 227 | far too fast |

Paragraph-split, with gaps:

| speed | wpm | verdict |
|---|---|---|
| 0.77 | 154 | too slow, exactly as the 16% cost predicts |
| **0.88** | **192** | **approved** |
| 0.93 | 200 | the rate already rejected |

**"Robotic" usually means too slow.** Kokoro degrades when pushed far below
its natural range. The first instinct on hearing a synthetic read is to slow
it down; for this model that makes it worse, not better.

## Choosing the voice itself

**A blend is a new speaker, not a mix.** A Kokoro voice is a `(510, 1, 256)`
style tensor, so a weighted sum is one new speaker identity the model renders
as a single person. It is not two voices layered as audio.

Weights are **not** normalised, matching the sibling video project. Profiles
here sum to 1.0 so it makes no difference today, but normalising would
silently change any future profile whose weights do not.

**For long prose, keep a male narrator all-male.** A 60/40 male/breathy-female
blend was tried in the sibling video project and read androgynous on a real
explainer script. It was rejected. Blends with a breathy-female component also
lose most of the bare voice's slowness.

**Prefer voices graded well on hours of data.** The model card grades
`am_onyx` D on 10 to 100 minutes, the weakest of the American males;
`am_puck`, `am_michael` and `am_fenrir` are C+ with hours. The approved book
voice is 60% `am_puck` for a steady base and 40% `am_onyx` for character.

**Kokoro cannot clone a voice.** No training or fine-tuning code has been
released, so blending existing embeddings is the ceiling without leaving it.

## One voice for the whole book

An early sample used a female voice for the chapter title line and a male
voice for the body. It was rejected immediately: it read as a different
product breaking into the narration. Slowing the title voice to match only
made it worse.

**Chapter titles are read by the narrator, like everything else.**

## The post chain

Do not reuse a video chain. Those are built for a phone speaker and a
40-second attention span, so they sit at -14 to -16 LUFS and often pitch up a
few percent for presence.

An audiobook is an hour on headphones and the distributors want roughly
-20 LUFS with real peak headroom. The `BOOK` chain is quieter, flatter and
less processed, with **no pitch shift at all**: a little chest at 200Hz for
warmth, the harsh presence band at 3.2kHz pulled down, a touch of air at 9kHz,
then `loudnorm=I=-20:TP=-3`.

## Auditioning

```bash
python -m audiobook_automation calibrate <manuscript.md> --speeds 0.84 0.88 0.92
```

Renders the first few paragraphs at each speed, prints measured wpm, and
deletes the files. Send two at a time, bracketing the likely answer: one round
trip converges faster than one file at a time.

## Hold every chapter at one measured pace, not one speed setting

At the same approved setting, chapter 1 of the first book measured 192 wpm and
chapter 10 measured 202. Nothing changed but the prose: chapter 10 has longer
paragraphs, so proportionally fewer cold starts, so a faster average.

**That difference is audible, and it is not pause time** - `spoken_wpm`
already excludes the designed gaps. It is the speech itself. A chapter built
from long paragraphs genuinely flows faster than a beat-heavy one at the same
setting, because Kokoro delivers a standalone utterance more slowly.

An earlier draft of this file said to converge on one chapter and leave the
setting alone. **That was wrong**, and the author caught it on the first
listen. One setting does not produce one pace; it produces a book that
quietly speeds up whenever the paragraphs get longer.

So:

```python
render.book(manuscript, out, narrator, target_wpm=192)
```

Each track is rendered, measured, and re-rendered at a corrected speed until
its **measured spoken wpm** hits the target. Typically two rounds.

Two things make the convergence harder than it looks:

- **wpm is not proportional to speed**, because the per-call overhead does not
  scale with it. So only the first correction is a ratio; every step after
  that is a secant through the two most recent measurements, which follows the
  real local slope instead of assuming one.
- **The response is quantised, not smooth.** On one short track 0.800 gave
  192.4 wpm and 0.802 gave 197.7: a 2.7% jump from a 0.25% change, because
  phoneme durations land on frame boundaries. Chasing a tight tolerance
  against that is a coin flip, so the default tolerance is 4 wpm (about 2%,
  inaudible) and the loop always **keeps the best measurement it has seen**
  rather than returning its last attempt.

On the first book, twelve of thirteen tracks converged to within 1 wpm of
target in two rounds. The thirteenth was short and beat-heavy and needed a
manual probe.

**Pick the target from the chapter you auditioned**, since that is the pace
the author actually approved. Expect the per-chapter speed settings to spread
by a few percent either side of the audition speed; that spread is the
correction doing its job, not drift.

Total runtime moves as a result. Let it. Consistent pace is worth more than a
round number, and the runtime was never the product.
