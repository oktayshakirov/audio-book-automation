"""Named, reproducible narrator profiles.

A profile is the whole recipe, not a voice name: Kokoro renders from a
`(voice, speed)` pair and the post chain does at least as much work as either.
The profile is the unit that gets named, approved and referenced.

**Speed is recorded as measured words per minute, not just as the Kokoro
parameter**, because the parameter means different things depending on how the
text is chunked. The same 192 words at the same setting measured 196 wpm as a
single call and 147 wpm split across seven paragraph calls.

For the same reason, `speed` here is a **starting point, not the value a book
is rendered at**. Chapters differ in paragraph length, so one setting gives
different paces; pass `target_wpm` to `render.book` and let it calibrate each
track to the `wpm` below. See `docs/voice.md`.

**Status is not a rating.** `approved` means it has shipped in a finished
book. `candidate` means it is shortlisted and waiting on a decision. Nothing
here gets promoted without the author saying so.
"""
from __future__ import annotations

from dataclasses import dataclass

SR = 24000          # Kokoro's native rate


# --- post chains ---------------------------------------------------------

# The audiobook chain. Deliberately NOT the chains a video pipeline uses:
# those are built for a phone speaker and a 40-second attention span, so they
# sit at -14 to -16 LUFS and often pitch up a few percent for presence.
#
# An audiobook is an hour on headphones, and the distributors want roughly
# -20 LUFS with real peak headroom. So this is quieter, flatter and less
# processed, with no pitch shift at all. The voice should sound like a person
# in a room, not a product.
BOOK = (
    "highpass=f=75,"
    "acompressor=threshold=-21dB:ratio=2.2:attack=20:release=300:makeup=1.5,"
    "equalizer=f=200:t=q:w=1.2:g=1.5,"      # a little chest, for warmth
    "equalizer=f=3200:t=q:w=1.2:g=-1.5,"    # pull the harsh presence band down
    "equalizer=f=9000:t=q:w=1.0:g=2,"       # a touch of air back on top
    "loudnorm=I=-20:TP=-3:LRA=11"
)


@dataclass(frozen=True)
class Narrator:
    voice: "str | dict[str, float]"   # Kokoro voice, or a weighted blend
    speed: float
    chain: str
    status: str
    wpm: int                           # measured, paragraph-split, with gaps
    note: str = ""


PROFILES: dict[str, Narrator] = {
    "atlas": Narrator(
        voice={"am_puck": 0.60, "am_onyx": 0.40}, speed=0.88, chain=BOOK,
        status="approved", wpm=192,
        note="The book voice. All male on purpose: a blend carrying a "
             "breathy-female component reads androgynous on long prose, which "
             "was rejected on a real script in the sibling video project. "
             "am_puck carries the steadier base (graded C+ with hours of "
             "training data), am_onyx adds the darker character.\n\n"
             "Speed was converged on by ear against measured wpm. 0.67 (151 "
             "wpm) was 'too slow and robotic' - Kokoro degrades when pushed "
             "far below its natural range. 0.74 (179) still slow, 0.80 (200) "
             "too fast, 0.93 (200, paragraph-split) too fast again. 0.88 "
             "lands at 192, the midpoint of the two rejections.",
    ),
}

APPROVED = {n: p for n, p in PROFILES.items() if p.status == "approved"}
DEFAULT = PROFILES["atlas"]


def get(name: str) -> Narrator:
    if name not in PROFILES:
        raise KeyError(f"unknown narrator {name!r}; "
                       f"known: {', '.join(sorted(PROFILES))}")
    return PROFILES[name]
