# Changelog

## 0.1.0

First release, extracted from building *Shut Up, Tinnitus* (13 tracks, ~60
minutes).

- Rule-based pacing: paragraph as the synthesis unit, beat rule for one-line
  hammer paragraphs, four gap lengths with longest-wins resolution.
- Verifiable pronunciation lexicon. Nine words fixed, each storing the IPA
  before and after; `pronounce verify` re-measures them.
- `atlas` narrator approved: 60/40 am_puck/am_onyx, speed 0.88, 192 wpm.
- `BOOK` post chain at -20 LUFS / -3 dBTP, no pitch shift, for headphones
  rather than phone speakers.
- Per-call silence trimming on the sample array, after ffmpeg `silenceremove`
  at -50dB proved to recover only a fraction of it.
- `plan` dry run, `calibrate` speed sweep.
- Docs: the short-audiobook format, sourcing discipline, distribution rules.

## 0.1.1

- `target_wpm` on `render.track` / `render.book`: calibrate each chapter to a
  constant **measured** pace. One speed setting is not one pace - a
  long-paragraph chapter reads audibly faster than a beat-heavy one, 192 vs
  202 wpm on the first book with pause time already excluded.
- Convergence is a ratio step then secant steps, keeps the best measurement
  seen, and defaults to a 4 wpm tolerance because the speed/wpm response is
  quantised (0.800 -> 192.4, 0.802 -> 197.7).
- `Rendered` now reports the speed it was rendered at.
- Corrected `docs/voice.md`, which had wrongly advised a single fixed speed.

## 0.1.2

- `even_pace` on `render.track`: calibrate every **paragraph**, not just the
  chapter average. Delivered pace was ranging 144-249 wpm within a single
  track at one speed setting, which is audible as the narrator speeding up and
  slowing down. An 8% dead band leaves natural variation alone. On the
  reported chapter, spread fell from 74 wpm to 29.
- `paragraph_wpm` and `speak_at_pace` exposed for diagnosing a track.
- Docs: writing for the ear rather than the page, and why the pace complaint
  lands on track one even when a later track is measurably worse.

## 0.1.3

- Calibrate **syllables per second**, not words per minute. wpm ignores word
  length: a chapter written in shorter words measured the same 192 wpm as the
  rest of its book but 4.07 syl/sec against 4.23-4.31, and was audibly slower.
  `pronounce.syllables` counts from espeak's phonemes.
- `even_pace` now takes a syllables/sec target and overrides `target_wpm`,
  which it previously fought: the per-track pass was overwriting the
  per-paragraph one.
- Dead band 8% -> 2%. At 8% a systematic 4% error sat entirely inside it and
  nothing was corrected.

## 0.1.4

- Documented that a full-length render does not fit an agent background-task
  time limit: ~45 minutes for 13 tracks, killed at ~27. Render in batches.

## 0.1.5

- Do not pace-calibrate utterances below 25 syllables, and never drift more
  than 15% from the narrator's own speed. Every synthesis call carries fixed
  onset/decay overhead; on a short utterance it dominates, so the measured
  rate reads far low and the correction chases an artifact. Chapter titles
  were rendering at 0.94-1.39 against a 0.88 body speed, and a 5-syllable
  title hit the 1.40 ceiling and came out unintelligible.

## 0.1.6

- Supplemental PDF generator for the tinnitus project: four pages, built with
  reportlab, written to the audio output directory. Google Play Books takes
  one PDF per audiobook under 100MB; Spotify has no documented route for one.

## 0.1.7

- `pronounce.say` matches case-insensitively and preserves the original case.
  It was two case-sensitive passes, so a lowercase lexicon key missed the
  sentence-initial form: one chapter pronounced "ginkgo" correctly three times
  and "Ginkgo" incorrectly three times.
- Writing rule: never write a bare "Chapter N." as a sentence. The narrator
  opens every track with that cadence, so mid-chapter it sounds like the file
  jumped. Caught by a listener on a shipped render.
- `--preview` builds the retail sample: the opening tracks concatenated, with
  a check against the ten-minute limit retailers impose.
