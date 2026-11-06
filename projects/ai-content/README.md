# Stop Making AI Slop

The third title built with this pipeline, in the same series format as
*Shut Up, Tinnitus* and *Stop Losing Money in Crypto*. 14 tracks, 62:49,
narrated locally with Kokoro. Built from what running AI-made video channels
taught us, plus outside sources; every claim is cited in the git-ignored
`book/SOURCES.md`.

## Listing metadata

Public once listed, so it lives here rather than in the git-ignored `book/`.
**Title and subtitle must be typed character for character** - they match the
cover art and the spoken credits, and a mismatch is a rejection.

| Field | Value |
|---|---|
| Title | `Stop Making AI Slop` |
| Subtitle | `Why Most AI Videos Die in Seven Seconds, and How to Make Ones People Actually Watch` |
| Author | `Oktay Shakirov` |
| Narrator | `Kokoro (AI Voice)` |
| Language | English |
| Category | BUSINESS & ECONOMICS / E-Commerce / Internet Marketing (BUS090010) |
| Second category | COMPUTERS / Artificial Intelligence / General (COM004000) |
| Price | $4.99, the same on every store (Google enforces price parity) |
| Runtime | 62:49 |
| Copyright | © 2026 Oktay Shakirov |
| AI narration | Yes - disclose on every store |

Confirm both category codes in each store's picker; the names are what
matter if a code is not offered.

### Description

> In twenty twenty five, Merriam-Webster's word of the year was slop: low quality content, made in quantity, by AI. You have scrolled past thousands of these videos. Maybe you have made some.
>
> Stop Making AI Slop is a one-hour, no-nonsense guide for creators who use AI to make YouTube, Shorts, TikTok and Reels videos, and want people to actually watch them. It opens with Demand Media, the content farm that let software pick its topics, published thousands of pieces a day and was valued at more than a billion dollars, until one Google update. AI content is the same business with the writers taken out, and the same thing is happening again.
>
> You will learn why a video is usually lost before its second sentence ends, how YouTube decides who sees your upload, why no platform has banned AI content but every one is penalising the template, and the four mistakes that give an AI video away: the topic nobody searches for, the robotic voice, the picture that says something else, and the template that shows.
>
> Then the practice: ten checks to run on every video, and a thirty day plan to rebuild your channel around them.
>
> No earnings promises. No secret prompt. Just how to use the same tools as everyone else and make something people choose to watch.
>
> Narrated by Kokoro, an AI voice.

### Keywords

ai slop, ai content creation, faceless youtube channel, youtube automation,
youtube shorts, ai video, youtube algorithm, audience retention, ai voiceover,
content creator, tiktok, inauthentic content

### Chapters

| # | File | Chapter | Length |
|---|---|---|---|
| 1 | `01-intro` | Introduction: AI Can Make Anything. It Cannot Make Anyone Watch. | 3:34 |
| 2 | `02-ch01` | Chapter 1: The Billion Dollar Content Farm | 4:55 |
| 3 | `03-ch02` | Chapter 2: Everyone Has the Same Machine Now | 5:17 |
| 4 | `04-ch03` | Chapter 3: You Have Seven Seconds, and Sentence Two Spends Them | 5:03 |
| 5 | `05-ch04` | Chapter 4: The Algorithm Is Not Counting Your Uploads | 5:38 |
| 6 | `06-ch05` | Chapter 5: The Rules Changed While You Were Uploading | 5:47 |
| 7 | `07-ch06` | Chapter 6: You Picked a Topic Nobody Is Looking For | 3:32 |
| 8 | `08-ch07` | Chapter 7: Your Voice Sounds Robotic Because You Slowed It Down | 3:37 |
| 9 | `09-ch08` | Chapter 8: The Picture Is Saying Something Else | 3:26 |
| 10 | `10-ch09` | Chapter 9: Your Template Is the Tell | 3:12 |
| 11 | `11-ch10` | Chapter 10: You Are Not a Factory. You Are the Editor. | 2:55 |
| 12 | `12-ch11` | Chapter 11: Build a Pipeline That Does Not Make Slop | 7:25 |
| 13 | `13-ch12` | Chapter 12: The Thirty Day Channel Reset | 5:17 |
| 14 | `14-outro` | Conclusion: Make the Video You Would Actually Watch | 3:02 |

## Upload kit

All in `~/Desktop/audiobook-ai-slop/`.

| File | Google Play | Spotify | Author's Republic |
|---|---|---|---|
| `01-intro.mp3` ... `14-outro.mp3` | yes | yes | yes |
| `Stop-Making-AI-Slop-sample-spotify.mp3` (8:32) | - | yes | - |
| `Stop-Making-AI-Slop-sample-ar.mp3` (3:34) | - | - | yes |
| `Stop-Making-AI-Slop-opening-credits.mp3` (0:13) | - | - | yes |
| `Stop-Making-AI-Slop-closing-credits.mp3` (0:12) | - | - | yes |
| `Stop-Making-AI-Slop-cover-3000.jpg` | yes | yes | yes |
| `Stop-Making-AI-Slop-companion.pdf` (6 pages) | yes | - | - |

Every audio file: 44.1 kHz, 192 kbps MP3, 1.5s silence at head and tail,
peak -3.2 dB or lower.

**Do not distribute to Google Play through Author's Republic.** This title
goes to Google Play direct, so deselect that channel there or there will be
two competing listings. Their opt-out needs an email.

## Rebuilding

```bash
python projects/ai-content/stop-making-ai-slop.py                 # all 14 tracks, ~45 min
python projects/ai-content/stop-making-ai-slop.py --track 12-ch11.md
python projects/ai-content/stop-making-ai-slop.py --credits
python projects/ai-content/stop-making-ai-slop.py --preview       # both samples
python projects/ai-content/supplemental_pdf.py                    # companion PDF
python projects/ai-content/metadata_pdf.py                        # upload sheet
```

Run a full render in a terminal, not an agent background task. **The samples
are built from the chapter files**: re-render the intro or chapter 1 and
rebuild them.

## Decisions worth not relitigating

**Same narrator and pace as the crypto book** (`atlas`, setting 4.38 syl/sec,
measuring ~4.30), approved from a two-take audition of chapter 11 against
4.62. Store the setting, not the measurement.

**Credits at 1.15, not the crypto book's 1.22 / 1.00.** Re-probed for this
text: at 1.00 the closing would have measured well below the chapters, the
"very slow" fault the crypto credits were rejected for.

**No channel sizes in the book.** Findings from our own channels are stated
as ratios, seconds and before/after. Invented scale would be the one claim a
reader could check and catch.

**The subtitle stays as written** (author's call, 2026-11-05), although
"Most" is a cover line rather than a sourced figure: the book's own curves
cover our Shorts.

**No conversational filler before a list.** "Here we go." was cut from
chapter 11 after the audition; it read as robotic. Now rule 12 in
`docs/structure.md`.
