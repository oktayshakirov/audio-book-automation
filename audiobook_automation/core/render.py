"""Manuscript in, audio out.

One synthesiser call per paragraph, each one trimmed, then concatenated with
the gaps `pacing` asks for. Everything downstream works off *measured*
durations, never estimates.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, replace
from pathlib import Path

from . import pacing, pronounce
from .voices import DEFAULT, Narrator

SR_OUT = 44100

# Kokoro leaves roughly 2.8s of near-silence on every call. Invisible when a
# whole chapter is one call; dominant at one call per paragraph. Trim it so the
# gaps in `pacing` are the only silence in the file and mean what they say.
#
# ffmpeg's `silenceremove` at -50dB only recovered 0.5-0.9s of it, so this
# works on the sample array directly, which is exact and testable.
TRIM_DB = 40.0          # below peak
TRIM_PAD = 0.04         # seconds kept either side, so decay and breath survive


def trim(audio, sr: int):
    """Strip leading and trailing near-silence, keeping a short pad."""
    import numpy as np
    a = np.asarray(audio, dtype="float32")
    peak = float(np.abs(a).max())
    if peak <= 0:
        return a
    loud = np.where(np.abs(a) > peak * (10 ** (-TRIM_DB / 20)))[0]
    if loud.size == 0:
        return a
    pad = int(TRIM_PAD * sr)
    return a[max(0, loud[0] - pad):min(len(a), loud[-1] + pad)]


def _kokoro():
    """Lazily built Kokoro session. Import-time cost is ~350MB of model."""
    global _K
    try:
        return _K
    except NameError:
        pass
    from kokoro_onnx import Kokoro
    import os
    home = Path(os.environ.get("KOKORO_HOME",
                               Path.home() / ".local/share/kokoro"))
    _K = Kokoro(str(home / "kokoro-v1.0.onnx"), str(home / "voices-v1.0.bin"))
    return _K


def _style(voice):
    """A blend is a weighted sum of (510,1,256) style tensors.

    That makes it one new speaker identity the model renders as a single
    person, not two voices mixed as audio.

    The weights are **not** normalised, matching the sibling video project's
    `voice_style`. Profiles here sum to 1.0 so it makes no difference today,
    but normalising would silently change the sound of any future profile
    whose weights do not, and break reproduction of an approved audition.
    """
    if isinstance(voice, str):
        return voice
    k = _kokoro()
    return sum(k.get_voice_style(n) * w for n, w in voice.items())


def ffprobe_duration(path: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip())


def silence(seconds: float, out: Path) -> Path:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    f"anullsrc=r={SR_OUT}:cl=mono", "-t", f"{seconds:.3f}",
                    str(out)], check=True)
    return out


def speak(text: str, narrator: Narrator, out: Path) -> Path:
    """One paragraph, one call. Never split a paragraph into sentences."""
    import soundfile as sf
    audio, sr = _kokoro().create(pronounce.say(text), voice=_style(narrator.voice),
                                 speed=narrator.speed, lang="en-us")
    raw = out.with_suffix(".raw.wav")
    sf.write(str(raw), trim(audio, sr), sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw),
                    "-af", narrator.chain, "-ar", str(SR_OUT), "-ac", "1",
                    str(out)], check=True)
    raw.unlink(missing_ok=True)
    return out


@dataclass
class Rendered:
    path: Path
    seconds: float
    words: int
    pause_seconds: float
    speed: float = 0.0

    @property
    def spoken_wpm(self) -> float:
        speech = self.seconds - self.pause_seconds
        return self.words / (speech / 60) if speech > 0 else 0.0

    def __str__(self) -> str:
        m, s = divmod(int(self.seconds), 60)
        return (f"{self.path.name}  {m}:{s:02d}  {self.words} words  "
                f"{self.pause_seconds:.1f}s pause  "
                f"speed {self.speed:.3f}  {self.spoken_wpm:.0f} wpm spoken")


def track(manuscript: Path | str, out_dir: Path | str,
          narrator: Narrator = DEFAULT, limit: int = 0,
          target_wpm: float | None = None, tolerance: float = 4.0,
          max_rounds: int = 6) -> Rendered:
    """Render one manuscript file to one MP3.

    With `target_wpm`, the speed is calibrated per track until the **measured
    spoken** rate hits the target. Set it to keep every chapter at one pace.

    Why that is not the same as one speed setting everywhere: at a fixed
    speed, a chapter built from long paragraphs reads faster than one built
    from short ones, because short paragraphs are cold starts and Kokoro
    delivers a standalone utterance more slowly. On the first book that was
    192 wpm in a beat-heavy chapter against 202 in a long-paragraph one, with
    pause time already excluded. Same setting, audibly different pace.
    """
    if target_wpm is not None:
        # Converge on measured pace.
        #
        # Two things make this harder than it looks. The first correction is a
        # ratio, which assumes wpm is proportional to speed; it is not,
        # because the per-call overhead does not scale. And the response is
        # **quantised, not smooth**: on one short track 0.800 gave 192.4 wpm
        # and 0.802 gave 197.7, a 2.7% jump from a 0.25% change, because
        # phoneme durations land on frame boundaries.
        #
        # So: ratio for the first step, secant after that to follow the real
        # local slope, and always keep the best measurement seen. Without that
        # last part the loop returns whatever its final attempt happened to be,
        # which can be worse than something it already found.
        pts: list[tuple[float, float]] = []
        best: tuple[float, float] | None = None       # (speed, wpm)
        r = None
        for _ in range(max_rounds):
            r = track(manuscript, out_dir, narrator, limit)
            if best is None or abs(r.spoken_wpm - target_wpm) < abs(best[1] - target_wpm):
                best = (narrator.speed, r.spoken_wpm)
            if abs(r.spoken_wpm - target_wpm) <= tolerance:
                return r
            pts.append((narrator.speed, r.spoken_wpm))
            if len(pts) == 1:
                nxt = narrator.speed * (target_wpm / r.spoken_wpm)
            else:
                (s1, w1), (s2, w2) = pts[-2], pts[-1]
                if abs(w2 - w1) < 1e-6:
                    break
                nxt = s2 + (target_wpm - w2) * (s2 - s1) / (w2 - w1)
            narrator = replace(narrator, speed=min(1.40, max(0.50, nxt)))

        # Out of rounds. Leave the best attempt on disk, not the last one.
        if best is not None and best[0] != narrator.speed:
            r = track(manuscript, out_dir, replace(narrator, speed=best[0]), limit)
        return r

    src = Path(manuscript)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / f".work-{src.stem}"
    work.mkdir(exist_ok=True)

    t = pacing.parse(src)
    paras = t.paragraphs[:limit] if limit else t.paragraphs
    plan = list(zip(pacing.gaps(paras), paras))

    parts = [speak(t.title, narrator, work / "title.wav")]
    for i, (gap, para) in enumerate(plan):
        parts.append(silence(gap, work / f"g{i:03d}.wav"))
        parts.append(speak(para, narrator, work / f"p{i:03d}.wav"))

    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    final = out_dir / f"{src.stem}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", "concat.txt", "-codec:a", "libmp3lame", "-b:a",
                    "192k", "-ar", str(SR_OUT), str(final.resolve())],
                   check=True, cwd=work)

    for p in parts:
        p.unlink(missing_ok=True)
    lst.unlink(missing_ok=True)
    work.rmdir()

    words = len(t.title.split()) + sum(len(p.split()) for p in paras)
    return Rendered(final, ffprobe_duration(final), words,
                    sum(g for g, _ in plan), narrator.speed)


def book(manuscript_dir: Path | str, out_dir: Path | str,
         narrator: Narrator = DEFAULT,
         target_wpm: float | None = None) -> list[Rendered]:
    """Render every manuscript file in a directory, in filename order.

    Pass `target_wpm` to hold every chapter at one measured pace rather than
    one speed setting. That is usually what a listener means by "the same
    speed": see `track`.
    """
    files = sorted(Path(manuscript_dir).glob("*.md"))
    if not files:
        raise FileNotFoundError(f"no .md manuscripts in {manuscript_dir}")
    return [track(f, out_dir, narrator, target_wpm=target_wpm) for f in files]
