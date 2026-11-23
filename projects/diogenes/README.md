# The Art of Not Caring What They Think

The fifth title built with this pipeline, after *Shut Up, Tinnitus*, *Stop
Losing Money in Crypto*, *Stop Making AI Slop* and *Job Hunting in the Age
of AI*, and the first in the "The Art of ..." shape. 13 tracks, 50:21,
narrated locally with Kokoro. Built from the ancient sources on Diogenes
(Diogenes Laertius, *Lives of Eminent Philosophers*, Book VI) and modern
social psychology; every claim is cited in the git-ignored
`book/SOURCES.md`.

## Listing metadata

Public once listed, so it lives here rather than in the git-ignored `book/`.
**Title and subtitle must be typed character for character** - they match the
cover art and the spoken credits, and a mismatch is a rejection.

| Field | Value |
|---|---|
| Title | `The Art of Not Caring What They Think` |
| Subtitle | `Diogenes, the Cynics and the Freedom of Needing Nothing` |
| Author | `Oktay Shakirov` |
| Narrator | `Kokoro (AI Voice)` |
| Language | English |
| Category | PHILOSOPHY / History & Surveys / Ancient & Classical (PHI002000) |
| Second category | SELF-HELP / Personal Growth / Self-Esteem (SEL023000) |
| Price | $4.99, the same on every store (Google enforces price parity) |
| Runtime | 50:21 |
| Copyright | © 2026 Oktay Shakirov |
| AI narration | Yes - disclose on every store |

Codes checked against the BISG lists 2026-11-23; confirm them in each
store's picker. No comma before "and" in the subtitle.

The title sits close to *The Subtle Art of Not Giving a F\*ck*, and *The Art
of Diogenes of Sinope* (a different book) was due out 2026-12-05. The
subtitle is what makes this one a philosophy book and tells them apart:
keep it in every field that takes one.

### Description

> A man stands on a slave auction block. The crier asks what he can do. He answers: govern men. Then he points at a rich buyer in the crowd and says, sell me to that man. He needs a master.
>
> You edit a message four times before you send it. You rehearse conversations that never happen. You say yes when you mean no, and stay quiet when you have the answer. The Art of Not Caring What They Think is a one-hour guide to why, built on one of the strangest philosophers of ancient Greece: Diogenes, the man who lived in a tub, told Alexander the Great to stand out of his light, and begged from statues to practise being refused.
>
> His secret was not that he stopped caring. It was that he needed almost nothing from anybody, and a person who needs nothing cannot be bought, flattered or frightened. The book follows that idea from the old stories into modern research: why you feel watched far more than you are, why people like you more than you think, why saying no costs less than you fear, and why reaching goals like money and image so often fails to help. Three short chapters name where the approval habit hides: in what you buy, in the yes you did not mean, and in the ambitions you were handed.
>
> Then the practice: five exercises drawn from what the Cynics actually did, from begging at statues to dragging a wine jar through the street, with their modern descendants from psychology, and a thirty day plan to put them to work.
>
> No promise that you will stop caring in a month. No invitation to live in a tub. Just a way to need less from what goes on in other people's heads.
>
> Narrated by Kokoro, an AI voice.

### Keywords

diogenes, cynicism, stoicism, ancient philosophy, people pleasing, social
anxiety, self esteem, confidence, spotlight effect, minimalism, how to stop
caring what people think, philosophy for everyday life

### Chapters

| # | File | Chapter | Length |
|---|---|---|---|
| 1 | `01-intro` | Introduction: You Edited That Message Four Times. | 3:52 |
| 2 | `02-ch01` | Chapter 1: The Man on the Auction Block | 4:40 |
| 3 | `03-ch02` | Chapter 2: The Cup | 4:22 |
| 4 | `04-ch03` | Chapter 3: Stand Out of My Light | 4:05 |
| 5 | `05-ch04` | Chapter 4: The Audience in Your Head | 4:02 |
| 6 | `06-ch05` | Chapter 5: Deface the Currency | 4:05 |
| 7 | `07-ch06` | Chapter 6: You Are Not Shopping. You Are Buying an Opinion. | 2:39 |
| 8 | `08-ch07` | Chapter 7: You Are Not Being Polite. You Are Hiding. | 2:56 |
| 9 | `09-ch08` | Chapter 8: You Call It Ambition. It Is a Leash. | 2:58 |
| 10 | `10-ch09` | Chapter 9: Needing Nothing Is Not Having Nothing | 2:39 |
| 11 | `11-ch10` | Chapter 10: Begging From Statues | 6:17 |
| 12 | `12-ch11` | Chapter 11: Thirty Days Without a Handle | 5:08 |
| 13 | `13-outro` | Conclusion: Prepared for Every Fortune | 2:31 |

## Upload kit

Built in `~/Desktop/audiobook-not-caring/` (delete after publishing; rebuild
with the commands below).

| File | Google Play | Spotify | Author's Republic |
|---|---|---|---|
| `01-intro.mp3` ... `13-outro.mp3` | yes | yes | yes |
| `The-Art-of-Not-Caring-What-They-Think-sample-spotify.mp3` (8:34) | - | yes | - |
| `The-Art-of-Not-Caring-What-They-Think-sample-ar.mp3` (3:52) | - | - | yes |
| `The-Art-of-Not-Caring-What-They-Think-opening-credits.mp3` (0:11) | - | - | yes |
| `The-Art-of-Not-Caring-What-They-Think-closing-credits.mp3` (0:12) | - | - | yes |
| `The-Art-of-Not-Caring-What-They-Think-cover-3000.jpg` | yes | yes | yes |
| `The-Art-of-Not-Caring-What-They-Think-companion.pdf` | yes | - | - |

Every audio file: 44.1 kHz, 192 kbps MP3, 1.5s silence at head and tail,
-21 LUFS, true peak -3.2 dB or lower.

**Do not distribute to Google Play through Author's Republic.** This title
goes to Google Play direct, so deselect that channel there or there will be
two competing listings. Their opt-out needs an email.

## Rebuilding

```bash
python projects/diogenes/the-art-of-not-caring.py                # all 13 tracks, ~45 min
python projects/diogenes/the-art-of-not-caring.py --track 11-ch10.md
python projects/diogenes/the-art-of-not-caring.py --credits
python projects/diogenes/the-art-of-not-caring.py --preview      # both samples
python projects/diogenes/supplemental_pdf.py                     # companion PDF
python projects/diogenes/metadata_pdf.py                         # upload sheet
```

Run a full render in a terminal, not an agent background task. **The samples
are built from the chapter files**: re-render the intro or chapter 1 and
rebuild them.

## Decisions worth not relitigating

**Same narrator and pace as the series** (`atlas`, setting 4.38 syl/sec).
Not re-auditioned; every track measured 4.22 to 4.35.

**Shorter than the series on purpose.** 50:21 against 61 to 64 minutes for
the earlier books. The author chose to render the 9,562-word manuscript as
it stood rather than grow it.

**Credits at 1.25 (opening) and 1.15 (closing).** Probed against this
book's chapters (median 5.20 syl/sec on the probe's scale). The opening is
the denser line, so it needs the faster setting this time.

**Greek names are respelled globally** in `core/pronounce.py`: Diogenes,
Plato, Crates, Sinope, Antisthenes, Xeniades, Laertius, Menippus, plus
Gilovich, Isthmus, drachmas and nomisma. Checked against Wiktionary and
Wikipedia 2026-11-23. **"Crates" is the risky one**: a later book that
says "crates" (boxes) must not inherit it.

**Every anecdote is told as a story.** The ancient source is a collector
writing long after Diogenes, often giving rival versions; the book says
"the story goes" and never narrates an anecdote as plain history. Laertius's
wording is used where it was checked: "Stand out of my light", not the
popular "sun".
