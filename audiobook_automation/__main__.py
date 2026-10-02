"""audiobook-automation CLI.

    python -m audiobook_automation render <manuscript.md> [-o DIR] [--limit N]
    python -m audiobook_automation book <manuscript-dir> [-o DIR]
    python -m audiobook_automation plan <manuscript.md>
    python -m audiobook_automation calibrate <manuscript.md> [--speeds ...]
    python -m audiobook_automation pronounce verify
    python -m audiobook_automation pronounce check <manuscript.md> ...
    python -m audiobook_automation voices
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from .core import pacing, pronounce, voices


def _render(a) -> int:
    from .core import render
    n = voices.get(a.narrator)
    if a.speed:
        n = replace(n, speed=a.speed)
    print(render.track(a.manuscript, a.out, n, limit=a.limit))
    return 0


def _book(a) -> int:
    from .core import render
    n = voices.get(a.narrator)
    if a.speed:
        n = replace(n, speed=a.speed)
    results = render.book(a.manuscript_dir, a.out, n)
    total = sum(r.seconds for r in results)
    words = sum(r.words for r in results)
    pause = sum(r.pause_seconds for r in results)
    for r in results:
        print(" ", r)
    m, s = divmod(int(total), 60)
    print(f"\n{len(results)} tracks  {m}:{s:02d}  {words} words  "
          f"{pause / 60:.1f} min of pause  "
          f"{words / ((total - pause) / 60):.0f} wpm spoken")
    return 0


def _plan(a) -> int:
    """Dry run: what the pacing rules will do, without synthesising."""
    t = pacing.parse(a.manuscript)
    gaps = pacing.gaps(t.paragraphs)
    print(f"{t.title}\n")
    for i, (gap, para) in enumerate(zip(gaps, t.paragraphs)):
        kind = ("TITLE" if i == 0
                else "BEAT" if gap == pacing.BEAT_GAP else "para")
        print(f"  {gap:4.2f}s {kind:5} {len(para.split()):3}w  {para[:64]}")
    print(f"\n{t.words} words, {sum(gaps):.1f}s of pause, "
          f"{sum(1 for p in t.paragraphs if pacing.is_beat(p))} beats")
    return 0


def _calibrate(a) -> int:
    """Measure wpm at several speeds. Judge by wpm, never by the parameter."""
    from .core import render
    n = voices.get(a.narrator)
    out = Path(a.out)
    for speed in a.speeds:
        r = render.track(a.manuscript, out, replace(n, speed=speed),
                         limit=a.limit)
        print(f"  speed {speed:.2f}  {r.spoken_wpm:5.0f} wpm spoken  "
              f"{r.seconds:6.1f}s total")
        r.path.unlink(missing_ok=True)
    return 0


def _pronounce(a) -> int:
    if a.action == "verify":
        bad = pronounce.verify()
        for b in bad:
            print("  !", b)
        print("lexicon clean" if not bad else f"{len(bad)} problem(s)")
        return 1 if bad else 0

    for path in a.files:
        t = pacing.parse(path)
        text = t.title + " " + " ".join(t.paragraphs)
        rows = pronounce.check(text)
        print(f"\n{Path(path).name}")
        for word, phonemes, handled in rows:
            mark = "ok " if handled else "  ?"
            print(f"  {mark} {word:<20} {phonemes}")
    print("\n'?' means nobody has checked it. Listen, or run espeak-ng "
          "yourself, then add it to LEXICON or LEAVE_ALONE.")
    return 0


def _voices(a) -> int:
    for name, p in voices.PROFILES.items():
        star = "*" if p.status == "approved" else " "
        print(f"{star} {name:<10} {p.voice}  speed {p.speed}  ~{p.wpm} wpm")
        for line in p.note.splitlines():
            print(f"      {line}")
    print("\n* = approved (has shipped in a finished book).")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="audiobook_automation")
    ap.add_argument("--narrator", default="atlas")
    ap.add_argument("--speed", type=float, default=None,
                    help="override the profile's speed (for auditions)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("render"); r.set_defaults(fn=_render)
    r.add_argument("manuscript")
    r.add_argument("-o", "--out", default="out")
    r.add_argument("--limit", type=int, default=0,
                   help="only the first N paragraphs, for a sample")

    b = sub.add_parser("book"); b.set_defaults(fn=_book)
    b.add_argument("manuscript_dir")
    b.add_argument("-o", "--out", default="out")

    p = sub.add_parser("plan"); p.set_defaults(fn=_plan)
    p.add_argument("manuscript")

    c = sub.add_parser("calibrate"); c.set_defaults(fn=_calibrate)
    c.add_argument("manuscript")
    c.add_argument("-o", "--out", default="out")
    c.add_argument("--limit", type=int, default=7)
    c.add_argument("--speeds", type=float, nargs="+",
                   default=[0.80, 0.85, 0.88, 0.92])

    pr = sub.add_parser("pronounce"); pr.set_defaults(fn=_pronounce)
    pr.add_argument("action", choices=["verify", "check"])
    pr.add_argument("files", nargs="*")

    v = sub.add_parser("voices"); v.set_defaults(fn=_voices)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
