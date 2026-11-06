"""Stop Making AI Slop - build recipe.

    python projects/ai-content/stop-making-ai-slop.py                      # whole book
    python projects/ai-content/stop-making-ai-slop.py --track 12-ch11.md 13-ch12.md
    python projects/ai-content/stop-making-ai-slop.py --audition 4.38 4.62
    python projects/ai-content/stop-making-ai-slop.py --credits     # opening + closing
    python projects/ai-content/stop-making-ai-slop.py --preview     # both samples

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
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-ai-slop"))

# Same narrator as Shut Up, Tinnitus and Stop Losing Money in Crypto: the
# books are one series, and a listener who comes from one to the next should
# hear the same voice.
NARRATOR_PROFILE = voices.get("atlas")

# Per-paragraph pace in syllables per second (see docs/voice.md for why not
# wpm). This is the *setting*, not the result: approved 2026-11-04 from a
# two-take audition of chapter 11, where 4.38 measured 4.30 syl/sec and
# 214 wpm, and 4.62 measured 4.43 / 221. The same setting and measurement as
# the crypto book, so the series keeps one pace. Keep the setting, not the
# measurement.
EVEN_PACE = 4.38

# The practice chapter: longest, most instructional, the one people replay.
AUDITION_TRACK = "12-ch11.md"

# Runtime is an outcome, not a target. Recorded for reference only.
# Rendered 2026-11-05: 14 tracks, 62:49, every track 4.21 to 4.45 syl/sec.
# A full render takes ~45 minutes; run it in a terminal, not an agent
# background task (one was killed at ~27 minutes on the first book).
ACTUAL_RUNTIME = "62:49"


# --- listing metadata -------------------------------------------------------
#
# Title, subtitle, author and narrator must match the cover art, the retailer
# metadata and the spoken credits character for character. Author's Republic
# rejected the tinnitus book over a subtitle shortened to fit its cover, so
# this one is fixed here first and the cover is set from these strings.
# The subtitle is still open (PLAN.md): "Most" may be softened before the
# cover freezes it. Change it here first if it changes.
TITLE = "Stop Making AI Slop"
SUBTITLE = ("Why Most AI Videos Die in Seven Seconds, "
            "and How to Make Ones People Actually Watch")
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
# This book's lines were re-probed 2026-11-05 the same way. Chapters measure
# 4.81 to 4.93 (median ~4.9, as crypto). Opening: 1.10 -> 4.70, 1.20 -> 5.07.
# Closing: 1.10 -> 4.75, 1.20 -> 5.10. So both sit at 1.15; at the crypto
# book's 1.00 the closing would have measured 4.58, the "very slow" fault.
CREDIT_GAP = 0.7

OPENING = [
    (f"This is {TITLE}. {SUBTITLE}. "
     f"Written by {AUTHOR}. Narrated by {NARRATOR}.", 1.15),
]

CLOSING = [
    (f"You have been listening to {TITLE}. "
     f"Written by {AUTHOR}. Narrated by {NARRATOR}.", 1.15),
    ("The End.", 1.15),
    ("Thank you for listening.", 1.15),
]

# --- retail samples ----------------------------------------------------------
#
#   Spotify:           up to 10 minutes
#   Author's Republic: 1 to 5 minutes
#
# Long: the introduction and chapter one unbroken, about 9 minutes; chapter
# one ends on "Until you notice who else got the same news.", a hook. Short:
# the introduction alone, self-contained, ending on "Because you became the
# editor." Check both lengths after rendering.
#
# The samples are built from the chapter files: re-render the intro or
# chapter one and the samples must be rebuilt, or they ship stale audio.
PREVIEWS = {
    "spotify": (["01-intro.mp3", "02-ch01.mp3"], 60, 10 * 60),
    "ar":      (["01-intro.mp3"], 60, 5 * 60),
}
PREVIEW_GAP = 1.6
SLUG = "Stop-Making-AI-Slop"


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
        final = dest / f"ch11-build-a-pipeline-{pace:.2f}sps.mp3"
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
