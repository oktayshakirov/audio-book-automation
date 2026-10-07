# Shut Up, Tinnitus

The first title built with this pipeline. **Published October 2026** to Google
Play Books, Spotify for Authors and Author's Republic.

13 tracks, 57:34, assembled from the tinnitushelp.me archive and narrated
locally with Kokoro.

## Listing metadata

Public once listed, so it lives here rather than in the git-ignored `book/`.

| Field | Value |
|---|---|
| Title | `Shut Up, Tinnitus` |
| Subtitle | `The No-Nonsense Guide to Why Your Ears Ring, Why It Gets Louder, and How to Make It Disappear Into the Background` |
| Author | `Oktay Shakirov` |
| Narrator | `Kokoro (AI Voice)` |
| Category | HEA035000 — HEALTH & FITNESS / Hearing & Speech |
| Second category | SELF-HELP / Stress Management |
| Price | $4.99, the same on every store |
| Runtime | 57:34 |

**The narrator credit follows the Audio Publishers Association's AI narration
naming guidelines**: name the voice and label it. The spoken credit says only
"Narrated by Kokoro"; the parenthetical is for the metadata field.

**Price parity is a Google rule**, not a preference: the Play Books list price
must not be higher than the same title elsewhere. One number everywhere.

### Chapters

| # | File | Chapter | Length |
|---|---|---|---|
| 1 | `01-intro` | Introduction: The Sound Is Not the Problem | 3:11 |
| 2 | `02-ch01` | Chapter 1: Beethoven's Letter from Vienna | 5:04 |
| 3 | `03-ch02` | Chapter 2: Your Ears Are Not Ringing. Your Brain Is. | 5:08 |
| 4 | `04-ch03` | Chapter 3: The Fear Loop | 5:01 |
| 5 | `05-ch04` | Chapter 4: Silence Is Making It Worse | 5:00 |
| 6 | `06-ch05` | Chapter 5: The Three A.M. Problem | 4:08 |
| 7 | `07-ch06` | Chapter 6: Your Jaw, Your Neck, Your Ears | 4:07 |
| 8 | `08-ch07` | Chapter 7: Coffee, Wine, and Other Things You Blamed | 3:38 |
| 9 | `09-ch08` | Chapter 8: The Supplement Aisle Is Lying to You | 4:14 |
| 10 | `10-ch09` | Chapter 9: You Are Not Broken. You Are Hypervigilant. | 2:48 |
| 11 | `11-ch10` | Chapter 10: Stop Listening For It | 7:22 |
| 12 | `12-ch11` | Chapter 11: The Thirty Day Tinnitus Reset | 5:24 |
| 13 | `13-outro` | Conclusion: The Day You Stop Checking | 2:28 |

The spoken titles drop "Introduction" and "Conclusion" - the player already
shows the track name, so saying it too was redundant. Numbered chapters keep
their number, which helps navigation.

## Rebuilding any of it

Audio and generated files live outside the repo, on the Desktop by default,
because they are large and regenerable. Override with `AUDIOBOOK_OUT`.

```bash
python projects/tinnitus/shut-up-tinnitus.py                 # all 13 tracks
python projects/tinnitus/shut-up-tinnitus.py --track 04-ch03.md
python projects/tinnitus/shut-up-tinnitus.py --credits       # opening + closing
python projects/tinnitus/shut-up-tinnitus.py --preview       # both samples
python projects/tinnitus/supplemental_pdf.py                 # companion PDF
```

**A full render takes ~45 minutes and does not survive an agent background
task** - it was killed partway through track 9 at about 27 minutes. Run it in
a terminal, or in two batches with `--track`.

**The samples do not follow the tracks.** Re-render the intro or chapter 1 and
you must rebuild the samples, or they ship built from stale audio.

## Decisions worth not relitigating

**Per-chapter speed is calibrated, not fixed.** One speed setting is not one
pace: the final speeds span 0.80 to 0.90 to hold every chapter at the same
measured syllable rate.

**The conclusion's speed is pinned** at 0.800 in `PINNED_SPEED`. Its
speed/wpm response is quantised in a 0.003-wide window, so auto-calibration
cannot land it reliably.

**Credits are weighted segments, not one utterance.** Kokoro has no emotion
parameter, so the title gets its weight from being a standalone utterance,
read slower than the credit lines around it, with a beat either side.

**Do not distribute to Google Play through Author's Republic.** This title
goes direct, so that channel must stay deselected there or you get two
competing listings. Their opt-out is not self-serve; it needs an email.

## Still open

- Cover is a lanczos upscale from 1254px. Regenerate at a true 3000x3000.
- Companion PDF ships on Google Play. Spotify has no documented route for one,
  and Author's Republic has not said.
- No Audible: ACX prohibits unauthorised TTS. Revisit if a human-narrated
  edition is ever worth ~$200-400 for 58 minutes.
