# Stop Losing Money in Crypto

The second title built with this pipeline, in the same series format as
*Shut Up, Tinnitus*. 14 tracks, 63:44, narrated locally with Kokoro. Sources
are thecrypto.wiki's topics, but every claim is cited to a primary or
reputable secondary source in the git-ignored `book/SOURCES.md`.

## Listing metadata

Public once listed, so it lives here rather than in the git-ignored `book/`.
**Title and subtitle must be typed character for character** - they match the
cover art and the spoken credits, and a mismatch is a rejection.

| Field | Value |
|---|---|
| Title | `Stop Losing Money in Crypto` |
| Subtitle | `The Scams, Collapses, Leverage and Lost Keys That Take It, and How to Keep Yours` |
| Author | `Oktay Shakirov` |
| Narrator | `Kokoro (AI Voice)` |
| Language | English |
| Category | BUSINESS & ECONOMICS / Personal Finance / Investing |
| Second category | BUSINESS & ECONOMICS / Investments & Securities / General (or a digital-currency heading, if the store's picker offers one) |
| Price | $4.99, the same on every store (Google enforces price parity) |
| Runtime | 63:44 |
| Copyright | © 2026 Oktay Shakirov |
| AI narration | Yes - disclose on every store |

### Description

> In 2025, Americans reported losing more than eleven billion dollars to crypto fraud. Almost none of it was lost because a chart went red.
>
> Stop Losing Money in Crypto is a one-hour, no-nonsense guide to the five ways money actually leaves people in crypto: scams, collapses, leverage, panic and lost keys. It opens with QuadrigaCX, the Canadian exchange whose founder supposedly took everyone's money to his grave, and what regulators found when they dug in. The real story is worse, and it is the most useful story in crypto.
>
> You will learn why a balance on an exchange is a promise rather than a coin, why twelve words can be worth everything you own, how wrong-number texts, fake support agents and paid influencers really work, why leverage turns a survivable crash into a permanent loss, and why most memecoins were never going to make you rich.
>
> Then the practice: how to build a vault for your crypto, step by step, and a thirty day plan to close every exit.
>
> No price predictions. No coin picks. Not financial advice. Just the ways people lose money in crypto, and how to make sure none of them take yours.
>
> Narrated by Kokoro, an AI voice.

### Keywords

crypto security, crypto scams, how to store crypto, seed phrase, hardware wallet,
crypto for beginners, bitcoin, not your keys not your coins, crypto leverage,
memecoins, FTX, QuadrigaCX

### Chapters

| # | File | Chapter | Length |
|---|---|---|---|
| 1 | `01-intro` | Introduction: The Price Is Not What Takes Your Money | 3:19 |
| 2 | `02-ch01` | Chapter 1: The Man Who Took the Keys to His Grave | 5:40 |
| 3 | `03-ch02` | Chapter 2: Nobody Can Reverse It. That Is the Point. | 4:58 |
| 4 | `04-ch03` | Chapter 3: Twelve Words Worth Everything You Own | 5:29 |
| 5 | `05-ch04` | Chapter 4: Not Your Keys | 5:36 |
| 6 | `06-ch05` | Chapter 5: The Scam Is Always Friendly | 5:47 |
| 7 | `07-ch06` | Chapter 6: You Bought the Top Because Everyone Else Did | 4:37 |
| 8 | `08-ch07` | Chapter 7: The Influencer Was Paid to Say That | 3:08 |
| 9 | `09-ch08` | Chapter 8: Leverage Is a Machine for Liquidating You | 3:08 |
| 10 | `10-ch09` | Chapter 9: The Memecoin Was Never Going to Make You Rich | 3:11 |
| 11 | `11-ch10` | Chapter 10: You Are Not Unlucky. You Are Unprotected. | 3:12 |
| 12 | `12-ch11` | Chapter 11: Build Your Vault | 7:28 |
| 13 | `13-ch12` | Chapter 12: The Thirty Day Crypto Reset | 5:21 |
| 14 | `14-outro` | Conclusion: The Day You Stop Checking the Price | 2:45 |

## Upload kit

All in `~/Desktop/audiobook-crypto/`.

| File | Google Play | Spotify | Author's Republic |
|---|---|---|---|
| `01-intro.mp3` ... `14-outro.mp3` | yes | yes | yes |
| `Stop-Losing-Money-in-Crypto-sample-spotify.mp3` (9:02) | - | yes | - |
| `Stop-Losing-Money-in-Crypto-sample-ar.mp3` (3:20) | - | - | yes |
| `Stop-Losing-Money-in-Crypto-opening-credits.mp3` (0:16) | - | - | yes |
| `Stop-Losing-Money-in-Crypto-closing-credits.mp3` (0:20) | - | - | yes |
| `Stop-Losing-Money-in-Crypto-cover-3000.jpg` | yes | yes | yes |

Every audio file: 44.1 kHz, 192 kbps MP3, 1.5s silence at head and tail,
peak -3.2 dB or lower.

**Do not distribute to Google Play through Author's Republic.** This title
goes to Google Play direct, so deselect that channel there or there will be
two competing listings. Their opt-out needs an email.

## Rebuilding

```bash
python projects/crypto/stop-losing-money.py                 # all 14 tracks, ~45 min
python projects/crypto/stop-losing-money.py --track 04-ch03.md
python projects/crypto/stop-losing-money.py --credits
python projects/crypto/stop-losing-money.py --preview       # both samples
```

Run a full render in a terminal, not an agent background task. **The samples
are built from the chapter files**: re-render the intro or chapter 1 and
rebuild them.

## Decisions worth not relitigating

**Same narrator as the tinnitus book** (`atlas`), so the series sounds like
one series.

**Pace is a setting of 4.38 syl/sec, which measures ~4.30.** Approved from a
two-take audition of chapter 11. Store the setting, not the measurement, or
the next render comes out slower than the approved one.

**No disclaimer per chapter.** "Not your financial adviser" is said once, in
the introduction.
