"""Shut Up, Tinnitus - build recipe.

    python projects/tinnitus/shut-up-tinnitus.py            # whole book
    python projects/tinnitus/shut-up-tinnitus.py --track 11-ch10.md
    python projects/tinnitus/shut-up-tinnitus.py --sample   # ch10, 7 paragraphs

The manuscript lives in the tinnitus-blog repo, not here: it is a commercial
product and this repo is public. Override with AUDIOBOOK_MANUSCRIPT.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from audiobook_automation.core import render, voices  # noqa: E402

MANUSCRIPT = Path(os.environ.get(
    "AUDIOBOOK_MANUSCRIPT",
    Path.home() / "Coding/tinnitus-blog/audiobook/script"))
OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT",
    Path.home() / "Coding/tinnitus-blog/audiobook/out"))

NARRATOR = voices.get("atlas")

# Every chapter is held at one measured pace, not one speed setting. At a
# fixed setting a long-paragraph chapter reads audibly faster than a
# beat-heavy one (202 vs 192 wpm here, pause time already excluded), because
# short paragraphs are cold starts. Chapter 1 is the reference: it is the one
# auditioned and approved, so the whole book is tuned to its pace.
TARGET_WPM = 192.0

# The practice chapter. Longest track, most instructional, and the one people
# replay - so it is the audition track. A voice that survives it survives
# everything.
AUDITION_TRACK = "11-ch10.md"

# Runtime is an outcome now, not a target: holding every chapter at one pace
# means the total lands where it lands. Recorded for reference only.
ACTUAL_RUNTIME = "57:50"      # 13 tracks at 192 wpm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()

    if a.sample:
        print(render.track(MANUSCRIPT / AUDITION_TRACK, OUT, NARRATOR, limit=7))
        return 0
    if a.track:
        print(render.track(MANUSCRIPT / a.track, OUT, NARRATOR,
                           target_wpm=TARGET_WPM))
        return 0

    results = render.book(MANUSCRIPT, OUT, NARRATOR, target_wpm=TARGET_WPM)
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
