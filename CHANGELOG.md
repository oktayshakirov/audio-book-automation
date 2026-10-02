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
