"""Where the silence goes.

An audiobook is paced by rules, not by feel, so that every track sounds the
same and a re-render is reproducible. The whole model is two ideas:

1. **The paragraph is the unit.** Each paragraph is one synthesiser call.
   Silence is inserted *between* calls and never inside one.
2. **A short paragraph standing alone is a beat** and gets a longer gap either
   side, because that is how a written hammer line is read aloud.

Why the paragraph and not the sentence: synthesising sentence by sentence
makes every sentence a cold start. Measured on five consecutive lines, alone
they opened at 258, 271, 229, 227 and 246 Hz; as one utterance they sat at
199 Hz falling to 193, which is a calm register with real paragraph
declination. A script of cold starts is what "reading a list" sounds like.

So inside a paragraph the model keeps its own breaths, declination and
sentence rhythm, untouched. A run of short stabbed sentences is *meant* to be
one call. Forcing silence between them sounds stilted, not dramatic.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Gap lengths in seconds. When two rules meet at one boundary the longer wins,
# so a beat after a quote gets BEAT, not BEAT + QUOTE.
TITLE_GAP = 1.30     # after the chapter title line, before the body
BEAT_GAP = 1.00      # either side of a beat paragraph
PARA_GAP = 0.55      # every other paragraph boundary
QUOTE_GAP = 0.90     # before a quotation set as its own paragraph

# A paragraph this short, standing alone, is a hammer line. Twelve was chosen
# by running it over a finished 13-track manuscript: it caught every
# deliberate one-line paragraph and no ordinary short prose.
BEAT_WORDS = 12


@dataclass(frozen=True)
class Track:
    title: str
    paragraphs: list[str]

    @property
    def words(self) -> int:
        return len(self.title.split()) + sum(len(p.split())
                                             for p in self.paragraphs)


def parse(path: Path | str) -> Track:
    """Read a manuscript file.

    Expected shape, which is also readable as a document:

        # Track 2 - Chapter 1: ...
        <notes, sources, anything>
        ---
        **[TITLE]** Chapter One. The Title.

        **[BODY]**

        First paragraph.

        Second paragraph.

    `[FEMALE VOICE]` / `[MALE VOICE]` are accepted as legacy spellings of
    `[TITLE]` / `[BODY]`.
    """
    raw = Path(path).read_text()
    if "\n---\n" not in raw:
        raise ValueError(f"{path}: no '---' separating the header from the text")
    raw = raw.split("\n---\n", 1)[1]

    m = re.search(r"\*\*\[(?:TITLE|FEMALE VOICE)\]\*\*(.*)", raw)
    if not m:
        raise ValueError(f"{path}: no **[TITLE]** line")
    title = m.group(1).strip()

    body = re.split(r"\*\*\[(?:BODY|MALE VOICE)\]\*\*", raw, maxsplit=1)
    if len(body) < 2:
        raise ValueError(f"{path}: no **[BODY]** marker")

    paras = [" ".join(b.split()) for b in body[1].split("\n\n") if b.strip()]
    if not paras:
        raise ValueError(f"{path}: no body paragraphs")
    return Track(title, paras)


def is_beat(paragraph: str) -> bool:
    return len(paragraph.split()) <= BEAT_WORDS


def gaps(paragraphs: list[str]) -> list[float]:
    """Silence *before* each paragraph, in seconds.

    Index 0 is the gap after the title line.
    """
    out: list[float] = []
    for i, para in enumerate(paragraphs):
        if i == 0:
            out.append(TITLE_GAP)
        elif is_beat(para) or is_beat(paragraphs[i - 1]):
            out.append(BEAT_GAP)
        else:
            out.append(PARA_GAP)
    return out


def plan(track: Track) -> list[tuple[float, str]]:
    """(gap_before, paragraph) for the whole track, after the title."""
    return list(zip(gaps(track.paragraphs), track.paragraphs))
