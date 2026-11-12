"""Job Hunting in the Age of AI - build recipe.

    python projects/job-search/job-hunting-in-the-age-of-ai.py                  # whole book
    python projects/job-search/job-hunting-in-the-age-of-ai.py --track 12-ch11.md 13-ch12.md
    python projects/job-search/job-hunting-in-the-age-of-ai.py --audition 4.38
    python projects/job-search/job-hunting-in-the-age-of-ai.py --credits   # opening + closing
    python projects/job-search/job-hunting-in-the-age-of-ai.py --preview   # both samples

The manuscript sits next to this file in book/. It is **git-ignored**: this
repo is public and the book is a paid product. Rendered audio goes to the
Desktop. Override either path with AUDIOBOOK_MANUSCRIPT / AUDIOBOOK_OUT.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from audiobook_automation.core import pacing, pronounce, render, voices  # noqa: E402

HERE = Path(__file__).resolve().parent

MANUSCRIPT = Path(os.environ.get(
    "AUDIOBOOK_MANUSCRIPT", HERE / "book" / "manuscript"))
OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-job-hunting"))

# Same narrator as Shut Up, Tinnitus, Stop Losing Money in Crypto and Stop
# Making AI Slop: the books are one series, and a listener who comes from
# one to the next should hear the same voice.
NARRATOR_PROFILE = voices.get("atlas")

# Per-paragraph pace in syllables per second (see docs/voice.md for why not
# wpm). This is the *setting*, not the result: the series pace, approved
# twice (crypto, and the slop book's 2026-11-04 two-take audition, where 4.38
# measured 4.30 syl/sec and 214 wpm). This book only confirms it on its own
# chapter 11 (PLAN.md: do not relitigate the pace). Audition 2026-11-11:
# 4.38 measured 4.29 syl/sec, 205 wpm, 7:48, -21.0 LUFS, true peak -3.2 dBFS.
# Keep the setting, not the measurement.
EVEN_PACE = 4.38

# The practice chapter: longest, most instructional, the one people replay.
AUDITION_TRACK = "12-ch11.md"

# Runtime is an outcome, not a target. Recorded for reference only.
# Rendered 2026-11-11/12: 14 tracks, 61:42, every track 4.24 to 4.41
# syl/sec, all -21 LUFS, true peak -3.2 to -3.3 dBFS.
# A full render takes ~45 minutes; run it in a terminal, not an agent
# background task (one was killed at ~27 minutes on the first book).
ACTUAL_RUNTIME = "61:42"


# --- listing metadata -------------------------------------------------------
#
# Title, subtitle, author and narrator must match the cover art, the retailer
# metadata and the spoken credits character for character. Author's Republic
# rejected the tinnitus book over a subtitle shortened to fit its cover, so
# this one is fixed here first and the cover is set from these strings.
# Frozen by the author 2026-11-11 (PLAN.md). *Job Hunting in the AI Era*
# already exists: keep the subtitle in every field that takes one.
TITLE = "Job Hunting in the Age of AI"
SUBTITLE = ("Why Nobody Answers Anymore, and How to Reach a Human")
AUTHOR = "Oktay Shakirov"
NARRATOR = "Kokoro"          # metadata field: "Kokoro (AI Voice)", per the APA

# --- credit tracks (Author's Republic requires both, 3 min max each) -------
#
# Each segment carries a fixed speed, measured to match the book's tempo.
#
# History, so nobody repeats it. The tinnitus recipe read the title at 0.72
# and the credit lines at 0.90 for emphasis; copied here, the credits came out
# far slower than the book and were rejected on the first listen (2026-10-22).
# Calibrating them with speak_at_pace did not fix it: anything under
# render.MIN_SYLLABLES_TO_PACE is left at base speed, and on these lines the
# espeak syllable count runs low (it drops the reduced vowel in "Narrated",
# "Collapses" and the respelled names), so the calibrator thought they were
# slow and stopped at its drift cap.
#
# So the speeds below were probed directly: rendered at 1.00 / 1.08 / 1.16 /
# 1.24 and measured in syllables per second with a spelling-based count,
# speech only, the same way on every chapter (chapters: 4.79 to 5.14, median
# 4.92). The opening, dense with long words and commas, needs 1.22 to land in
# that range; the closing lands at 1.00. Both sit inside the 0.94 to 1.27 the
# book's own chapter titles calibrated to, well short of the 1.40 that once
# garbled a title.
#
# This book's lines probed 2026-11-12 the same way (spelling-based
# syllables, speech only, silences over 0.25s cut; this probe's absolute
# numbers run higher than the slop book's, so compare within one probe only).
# Chapters 5.16 to 5.52, median 5.32. Opening: 1.00 -> 4.94, 1.08 -> 5.07,
# 1.15 -> 5.30, 1.24 -> 5.70. Closing: 1.00 -> 4.68, 1.15 -> 5.10,
# 1.20 -> 5.23, 1.22 -> 5.33, 1.24 -> 5.52. So the opening sits at 1.15 and
# the closing at 1.22; at 1.00 the closing would have been the "very slow"
# fault again.
CREDIT_GAP = 0.7

OPENING = [
    (f"This is {TITLE}. {SUBTITLE}. "
     f"Written by {AUTHOR}. Narrated by {NARRATOR}.", 1.15),
]

CLOSING = [
    (f"You have been listening to {TITLE}. "
     f"Written by {AUTHOR}. Narrated by {NARRATOR}.", 1.22),
    ("The End.", 1.22),
    ("Thank you for listening.", 1.22),
]

# --- retail samples ----------------------------------------------------------
#
#   Spotify:           up to 10 minutes
#   Author's Republic: 1 to 5 minutes
#
# Long: the introduction and chapter one unbroken, about 9 minutes; chapter
# one ends on "And then, almost overnight, the effort disappeared.", a hook.
# Short: the introduction alone, self-contained, ending on "Be worth
# answering." Check both lengths after rendering.
#
# The samples are built from the chapter files: re-render the intro or
# chapter one and the samples must be rebuilt, or they ship stale audio.
PREVIEWS = {
    "spotify": (["01-intro.mp3", "02-ch01.mp3"], 60, 10 * 60),
    "ar":      (["01-intro.mp3"], 60, 5 * 60),
}
PREVIEW_GAP = 1.6
SLUG = "Job-Hunting-in-the-Age-of-AI"


def _concat(parts: list[Path], out: Path, cwd: Path) -> None:
    lst = cwd / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe",
                    "0", "-i", str(lst), "-codec:a", "libmp3lame", "-b:a",
                    "192k", "-ar", "44100", str(out)], check=True)


def credits_tracks() -> int:
    """Opening and closing credits, through the book's narrator and chain."""
    OUT.mkdir(parents=True, exist_ok=True)
    worst = 0
    for name, segments in (("opening", OPENING), ("closing", CLOSING)):
        out = OUT / f"{SLUG}-{name}-credits.mp3"
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            gap = render.silence(CREDIT_GAP, tmp / "gap.wav")
            parts = [render.silence(render.LEAD_SILENCE, tmp / "head.wav")]
            for i, (text, speed) in enumerate(segments):
                if i:
                    parts.append(gap)
                parts.append(render.speak(
                    text, replace(NARRATOR_PROFILE, speed=speed),
                    tmp / f"s{i}.wav"))
            parts.append(render.silence(render.TAIL_SILENCE, tmp / "tail.wav"))
            _concat(parts, out, tmp)
        d = render.ffprobe_duration(out)
        m, sec = divmod(int(round(d)), 60)
        bad = "  !! OVER 3 MINUTES" if d > 180 else ""
        worst = max(worst, 1 if bad else 0)
        print(f"{out.name}  {m}:{sec:02d}{bad}")
    return worst


def preview(which: str) -> int:
    """Build one retail sample; `which` picks the retailer's length rule."""
    tracks, lo, hi = PREVIEWS[which]
    parts = [OUT / t for t in tracks]
    missing = [p.name for p in parts if not p.exists()]
    if missing:
        print(f"!! render these first: {', '.join(missing)}")
        return 1
    out = OUT / f"{SLUG}-sample-{which}.mp3"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        gap = tmp / "gap.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "anullsrc=r=44100:cl=mono", "-t", str(PREVIEW_GAP),
                        "-codec:a", "libmp3lame", "-b:a", "192k", str(gap)],
                       check=True)
        # Chapter files already carry head and tail silence; nothing to add.
        seq = [parts[0]]
        for p in parts[1:]:
            seq += [gap, p]
        _concat(seq, out, tmp)
    d = render.ffprobe_duration(out)
    m, sec = divmod(int(round(d)), 60)
    bad = "" if lo <= d <= hi else f"  !! OUTSIDE {lo // 60}-{hi // 60} MIN"
    print(f"{out.name}  {m}:{sec:02d}{bad}")
    return 1 if bad else 0


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
        final = dest / f"ch11-run-a-search-{pace:.2f}sps.mp3"
        shutil.move(r.path, final)
        work.rmdir()
        r.path = final
        print(_measure(r, MANUSCRIPT / AUDITION_TRACK), flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", nargs="+")
    ap.add_argument("--audition", type=float, nargs="+", metavar="SYL_PER_SEC")
    ap.add_argument("--credits", action="store_true")
    ap.add_argument("--preview", nargs="?", const="all",
                    choices=["all", *PREVIEWS])
    a = ap.parse_args()
    if a.credits:
        return credits_tracks()
    if a.preview:
        which = list(PREVIEWS) if a.preview == "all" else [a.preview]
        return max(preview(w) for w in which)
    if a.audition:
        audition(a.audition)
        return 0
    names = a.track or sorted(p.name for p in MANUSCRIPT.glob("*.md"))
    for name in names:
        print(_measure(_one(name, OUT, EVEN_PACE), MANUSCRIPT / name), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
