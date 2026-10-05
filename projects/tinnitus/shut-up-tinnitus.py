"""Shut Up, Tinnitus - build recipe.

    python projects/tinnitus/shut-up-tinnitus.py            # whole book
    python projects/tinnitus/shut-up-tinnitus.py --track 11-ch10.md
    python projects/tinnitus/shut-up-tinnitus.py --sample   # ch10, 7 paragraphs

The manuscript sits next to this file in book/. It is **git-ignored**: this
repo is public and the book is a paid product, so the text is kept out of
history until that is a deliberate decision. Rendered audio goes to the
Desktop. Override either path with AUDIOBOOK_MANUSCRIPT / AUDIOBOOK_OUT.
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from audiobook_automation.core import render, voices  # noqa: E402

HERE = Path(__file__).resolve().parent

MANUSCRIPT = Path(os.environ.get(
    "AUDIOBOOK_MANUSCRIPT", HERE / "book" / "manuscript"))
OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook"))

NARRATOR = voices.get("atlas")

# Every chapter is held at one measured pace, not one speed setting. At a
# fixed setting a long-paragraph chapter reads audibly faster than a
# beat-heavy one (202 vs 192 wpm here, pause time already excluded), because
# short paragraphs are cold starts. Chapter 1 is the reference: it is the one
# auditioned and approved, so the whole book is tuned to its pace.
TARGET_WPM = 192.0

# Tracks where auto-calibration cannot land cleanly, with the speed that was
# measured by hand. The conclusion is short and beat-heavy, and its speed/wpm
# response is badly quantised: 0.797 gives 187 wpm, 0.800 gives 192.4, 0.802
# gives 197.7. The loop cannot reliably find a 0.003-wide window, so it is
# pinned. Re-measure if the text changes.
PINNED_SPEED = {"13-outro.md": 0.800}

# Even out the pace *within* a track as well as across tracks. Track-level
# calibration only fixes a chapter's average; inside one, individual
# paragraphs were landing anywhere from 144 to 249 wpm, and that swing is what
# a listener hears as the narrator speeding up and slowing down. An 8% dead
# band leaves natural micro-variation alone and only pulls in the outliers.
# Measured in **syllables per second**, not words per minute. Every chapter
# hit 192 wpm and the introduction still sounded too slow, because it is
# written in shorter words: 4.07 syl/sec against 4.23 to 4.31 elsewhere. The
# author picked the chapter-3/chapter-4 tempo as correct, which measures 4.24.
EVEN_PACE = 4.24

# The practice chapter. Longest track, most instructional, and the one people
# replay - so it is the audition track. A voice that survives it survives
# everything.
AUDITION_TRACK = "11-ch10.md"

# Runtime is an outcome now, not a target: holding every chapter at one pace
# means the total lands where it lands. Recorded for reference only.
ACTUAL_RUNTIME = "57:50"      # 13 tracks at 192 wpm


def _one(name: str):
    """Render one track: pinned speed if it has one, else calibrated."""
    start = replace(NARRATOR, speed=PINNED_SPEED.get(name, NARRATOR.speed))
    return render.track(MANUSCRIPT / name, OUT, start, even_pace=EVEN_PACE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()

    if a.sample:
        print(render.track(MANUSCRIPT / AUDITION_TRACK, OUT, NARRATOR, limit=7))
        return 0
    if a.track:
        print(_one(a.track))
        return 0

    results = [_one(f.name) for f in sorted(MANUSCRIPT.glob("*.md"))]
    for r in results:
        print(" ", r)
    total = sum(r.seconds for r in results)
    words = sum(r.words for r in results)
    pause = sum(r.pause_seconds for r in results)
    m, s = divmod(int(total), 60)
    print(f"\n{len(results)} tracks  {m}:{s:02d}  {words} words  "
          f"{pause / 60:.1f} min pause  "
          f"{words / ((total - pause) / 60):.0f} wpm spoken")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
