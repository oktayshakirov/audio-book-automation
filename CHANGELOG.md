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
