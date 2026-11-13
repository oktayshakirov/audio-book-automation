# Job Hunting in the Age of AI

The fourth title built with this pipeline, in the same series format as
*Shut Up, Tinnitus*, *Stop Losing Money in Crypto* and *Stop Making AI Slop*.
14 tracks, 61:42, narrated locally with Kokoro. Built from what an automated
job search measured, plus outside sources; every claim is cited in the
git-ignored `book/SOURCES.md`.

## Listing metadata

Public once listed, so it lives here rather than in the git-ignored `book/`.
**Title and subtitle must be typed character for character** - they match the
cover art and the spoken credits, and a mismatch is a rejection.

| Field | Value |
|---|---|
| Title | `Job Hunting in the Age of AI` |
| Subtitle | `Why Nobody Answers Anymore, and How to Reach a Human` |
| Author | `Oktay Shakirov` |
| Narrator | `Kokoro (AI Voice)` |
| Language | English |
| Category | BUSINESS & ECONOMICS / Careers / Job Hunting (BUS037020) |
| Second category | COMPUTERS / Artificial Intelligence / General (COM004000) |
| Price | $4.99, the same on every store (Google enforces price parity) |
| Runtime | 61:42 |
| Copyright | © 2026 Oktay Shakirov |
| AI narration | Yes - disclose on every store |

Confirm both category codes in each store's picker; the names are what
matter if a code is not offered.

*Job Hunting in the AI Era* (a different book) already exists. The subtitle
is what tells them apart in a store listing: keep it in every field that
takes one.

### Description

> Five hundred and eighty seven job postings in one week. Four worth an application.
>
> You have sent dozens of applications, maybe hundreds, and heard nothing back. Job Hunting in the Age of AI is a one-hour, plain-spoken guide to why that happens and what to do instead. It opens around 1970, with a graduate student asking a few hundred workers how they found their jobs, and an answer that still explains hiring today: not a friend, an acquaintance.
>
> Then it follows what happened when AI made applying free. Why a polished, tailored cover letter stopped meaning anything. Where the famous claim that software rejects three quarters of applications really came from, and what actually happens after you press send. Why the door for beginners narrowed, and why some of the jobs you apply for were never there. Four short chapters cover the mistakes that make an application easy to ignore: letting the machine write the letter, applying to everything, missing the fine print, and trying to trick the filter.
>
> Then the practice: ten steps for a search a person on the other side will answer, and a thirty day plan to rebuild yours around them. For graduates, career changers, people coming back to work, and anyone applying through a screen and hearing nothing.
>
> No promise of a job. No tricks for beating the machines. Just how hiring works now, and how to reach a human.
>
> Narrated by Kokoro, an AI voice.

### Keywords

job search, job hunting, ai job search, ghost jobs, applicant tracking
system, resume, cover letter, entry level jobs, tech jobs, ai interview,
career change, hiring

### Chapters

| # | File | Chapter | Length |
|---|---|---|---|
| 1 | `01-intro` | Introduction: You Are Not Being Rejected. You Are Not Being Read. | 4:00 |
| 2 | `02-ch01` | Chapter 1: Not a Friend, an Acquaintance | 5:11 |
| 3 | `03-ch02` | Chapter 2: Applying Got Free, So It Stopped Meaning Anything | 5:07 |
| 4 | `04-ch03` | Chapter 3: Nobody Is Rejecting You at Two in the Morning | 5:26 |
| 5 | `05-ch04` | Chapter 4: The Door for Beginners Got Narrower | 4:48 |
| 6 | `06-ch05` | Chapter 5: The Job That Was Never There | 4:36 |
| 7 | `07-ch06` | Chapter 6: You Let the Machine Write the Letter | 3:06 |
| 8 | `08-ch07` | Chapter 7: You Applied to Everything | 3:09 |
| 9 | `09-ch08` | Chapter 8: You Saw the Word Remote and Stopped Reading | 3:26 |
| 10 | `10-ch09` | Chapter 9: You Tried to Trick the Machine | 3:38 |
| 11 | `11-ch10` | Chapter 10: You Are Not Applying to Jobs. You Are Choosing Companies. | 3:08 |
| 12 | `12-ch11` | Chapter 11: Run a Search a Human Will Answer | 7:48 |
| 13 | `13-ch12` | Chapter 12: The Thirty Day Search Reset | 5:13 |
| 14 | `14-outro` | Conclusion: Be the Application a Person Wants to Answer | 2:58 |

## Upload kit

Built in `~/Desktop/audiobook-job-hunting/` (delete after publishing; rebuild
with the commands below).

| File | Google Play | Spotify | Author's Republic |
|---|---|---|---|
| `01-intro.mp3` ... `14-outro.mp3` | yes | yes | yes |
| `Job-Hunting-in-the-Age-of-AI-sample-spotify.mp3` (9:13) | - | yes | - |
| `Job-Hunting-in-the-Age-of-AI-sample-ar.mp3` (4:01) | - | - | yes |
| `Job-Hunting-in-the-Age-of-AI-opening-credits.mp3` (0:11) | - | - | yes |
| `Job-Hunting-in-the-Age-of-AI-closing-credits.mp3` (0:12) | - | - | yes |
| `Job-Hunting-in-the-Age-of-AI-cover-3000.jpg` | yes | yes | yes |
| `Job-Hunting-in-the-Age-of-AI-companion.pdf` (6 pages) | yes | - | - |

Every audio file: 44.1 kHz, 192 kbps MP3, 1.5s silence at head and tail,
-21 LUFS, true peak -3.2 dB or lower.

**Do not distribute to Google Play through Author's Republic.** This title
goes to Google Play direct, so deselect that channel there or there will be
two competing listings. Their opt-out needs an email.

## Rebuilding

```bash
python projects/job-search/job-hunting-in-the-age-of-ai.py               # all 14 tracks, ~40 min
python projects/job-search/job-hunting-in-the-age-of-ai.py --track 12-ch11.md
python projects/job-search/job-hunting-in-the-age-of-ai.py --credits
python projects/job-search/job-hunting-in-the-age-of-ai.py --preview     # both samples
python projects/job-search/supplemental_pdf.py                           # companion PDF
python projects/job-search/metadata_pdf.py                               # upload sheet
```

Run a full render in a terminal, not an agent background task. **The samples
are built from the chapter files**: re-render the intro or chapter 1 and
rebuild them.

## Decisions worth not relitigating

**Same narrator and pace as the series** (`atlas`, setting 4.38 syl/sec).
Confirmed on this book's chapter 11 (4.29 measured), not re-auditioned.

**Credits at 1.15 (opening) and 1.22 (closing).** Re-probed for this text
against its own chapters; at 1.00 the closing would have measured well
below them, the "very slow" fault the crypto credits were rejected for.

**The author's own search appears as ratios only.** No employer, no city, no
outcome of the search, no salary. The book describes the method and what it
measured.

**"resume" is respelled globally** (`rezzumay`, the noun). The lexicon is
applied everywhere, so a manuscript can never use "resume" as a verb; write
"continue" instead. Past-tense "read" after a plain subject is said "reed",
and "still live" is said "liv": both are reworded in the text, not
respelled.

**No researcher names where espeak cannot say them.** Chapter two names no
economists; the 2022 LinkedIn study is "a team from LinkedIn, MIT, Harvard
and Stanford".
