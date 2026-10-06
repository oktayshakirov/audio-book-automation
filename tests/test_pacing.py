import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audiobook_automation.core import pacing  # noqa: E402

MANUSCRIPT = """# Track 2 - Chapter 1
Target 6:00.
---
**[TITLE]** Chapter One. The Title.

**[BODY]**

A long opening paragraph that runs well past the beat threshold because it
keeps going and going and going and going and going and going.

A hammer line.

Another long one that also runs past the threshold, going on and on and on
and on and on and on and on and on and on and on and on.
"""


def _track(tmp_path):
    p = tmp_path / "02-ch01.md"
    p.write_text(MANUSCRIPT)
    return pacing.parse(p)


def test_parse_splits_header_title_and_paragraphs(tmp_path):
    t = _track(tmp_path)
    assert t.title == "Chapter One. The Title."
    assert len(t.paragraphs) == 3
    # the header above the --- is never spoken
    assert "Target 6:00" not in " ".join(t.paragraphs)
    # paragraphs are reflowed to one line
    assert "\n" not in t.paragraphs[0]


def test_beat_rule(tmp_path):
    t = _track(tmp_path)
    assert not pacing.is_beat(t.paragraphs[0])
    assert pacing.is_beat(t.paragraphs[1])


def test_gaps_longest_rule_wins(tmp_path):
    t = _track(tmp_path)
    g = pacing.gaps(t.paragraphs)
    assert g[0] == pacing.TITLE_GAP
    # either side of the beat gets BEAT, not PARA
    assert g[1] == pacing.BEAT_GAP
    assert g[2] == pacing.BEAT_GAP


def test_legacy_voice_markers_still_parse(tmp_path):
    p = tmp_path / "legacy.md"
    p.write_text(MANUSCRIPT.replace("[TITLE]", "[FEMALE VOICE]")
                           .replace("[BODY]", "[MALE VOICE]"))
    assert pacing.parse(p).title == "Chapter One. The Title."


# --- pace-calibration guards -------------------------------------------
# These exist because a real book shipped with unintelligible chapter titles.
# Short utterances carry a fixed per-call overhead, so their measured rate
# reads far below the true rate and the calibration drove a 5-syllable title
# to the speed ceiling. Both guards are cheap and neither is obvious.

def test_short_utterances_are_never_pace_calibrated():
    from audiobook_automation.core import pronounce, render
    # every chapter title in a real book fell below the floor
    for title in ("Chapter Three. The Fear Loop.",
                  "The Sound Is Not the Problem.",
                  "The Day You Stop Checking."):
        assert pronounce.syllables(title) < render.MIN_SYLLABLES_TO_PACE, title


def test_a_full_paragraph_is_still_pace_calibrated():
    from audiobook_automation.core import pronounce, render
    para = ("Take two people. Put them both in a clinic and measure their "
            "tinnitus properly, the way an audiologist does it. Match the "
            "pitch. Match the loudness.")
    assert pronounce.syllables(para) >= render.MIN_SYLLABLES_TO_PACE


def test_drift_cap_keeps_speed_near_the_narrator():
    """A correction that changes the voice is not a correction."""
    from audiobook_automation.core import render
    base = 0.88
    lo = base * (1 - render.MAX_SPEED_DRIFT)
    hi = base * (1 + render.MAX_SPEED_DRIFT)
    # the title that shipped broken was driven to 1.392 from a 0.88 base
    assert not lo <= 1.392 <= hi
    assert hi < 1.05
