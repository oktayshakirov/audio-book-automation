"""Stop Losing Money in Crypto - build recipe.

    python projects/crypto/stop-losing-money.py                      # whole book
    python projects/crypto/stop-losing-money.py --track 12-ch11.md 13-ch12.md
    python projects/crypto/stop-losing-money.py --audition 4.10 4.38

The manuscript sits next to this file in book/. It is **git-ignored**: this
repo is public and the book is a paid product. Rendered audio goes to the
Desktop. Override either path with AUDIOBOOK_MANUSCRIPT / AUDIOBOOK_OUT.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from audiobook_automation.core import pacing, pronounce, render, voices  # noqa: E402

HERE = Path(__file__).resolve().parent

MANUSCRIPT = Path(os.environ.get(
    "AUDIOBOOK_MANUSCRIPT", HERE / "book" / "manuscript"))
OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-crypto"))

# Same narrator as Shut Up, Tinnitus: the two books are one series, and a
# listener who comes from one to the other should hear the same voice.
NARRATOR_PROFILE = voices.get("atlas")

# Per-paragraph pace in syllables per second (see docs/voice.md for why not
# wpm). This is the *setting*, not the result: approved 2026-10-20 from a
# two-take audition of chapter 11, where 4.38 measured 4.30 syl/sec and
# 202 wpm, and 4.10 measured 4.15 / 195. The calibration's dead band pulls the
# result toward the voice's natural rate, so to reproduce the approved take,
# keep the setting, not the measurement. A shade faster than the tinnitus
# book's 4.24.
EVEN_PACE = 4.38

# The practice chapter: longest, most instructional, the one people replay.
AUDITION_TRACK = "12-ch11.md"

# Runtime is an outcome, not a target. Recorded for reference only.
# Rendered 2026-10-20: 14 tracks, 63:44, every track 4.26 to 4.39 syl/sec.
# A full render takes ~45 minutes; run it in a terminal, not an agent
# background task (one was killed at ~27 minutes on the first book).
ACTUAL_RUNTIME = "63:44"


def _one(name: str, out: Path, pace: float) -> render.Rendered:
    return render.track(MANUSCRIPT / name, out, NARRATOR_PROFILE, even_pace=pace)


def _measure(r: render.Rendered, manuscript: Path) -> str:
    """wpm and syllables/sec of speech, designed gaps and end padding excluded."""
    t = pacing.parse(manuscript)
    text = " ".join([t.title, *t.paragraphs])
    speech = r.seconds - r.pause_seconds - render.LEAD_SILENCE - render.TAIL_SILENCE
    m, s = divmod(int(r.seconds), 60)
    return (f"{r.path.name}  {m}:{s:02d}  {r.words / (speech / 60):.0f} wpm  "
            f"{pronounce.syllables(text) / speech:.2f} syl/sec")


def audition(paces: list[float]) -> None:
    """Render the audition track once per pace, side by side, and measure each."""
    dest = OUT / "audition"
    dest.mkdir(parents=True, exist_ok=True)
    for pace in paces:
        work = dest / f"_{pace:.2f}"
        r = _one(AUDITION_TRACK, work, pace)
        final = dest / f"ch11-build-your-vault-{pace:.2f}sps.mp3"
        shutil.move(r.path, final)
        work.rmdir()
        r.path = final
        print(_measure(r, MANUSCRIPT / AUDITION_TRACK), flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", nargs="+")
    ap.add_argument("--audition", type=float, nargs="+", metavar="SYL_PER_SEC")
    a = ap.parse_args()
    if a.audition:
        audition(a.audition)
        return 0
    names = a.track or sorted(p.name for p in MANUSCRIPT.glob("*.md"))
    for name in names:
        print(_measure(_one(name, OUT, EVEN_PACE), MANUSCRIPT / name), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
