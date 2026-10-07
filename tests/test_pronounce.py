import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audiobook_automation.core import pronounce  # noqa: E402

needs_espeak = pytest.mark.skipif(not shutil.which("espeak-ng"),
                                  reason="espeak-ng not installed")


def test_say_respells_and_preserves_case():
    assert pronounce.say("Ludwig van Beethoven") == "Loodvig van Beethoven"
    assert pronounce.say("the ginkgo story") == "the ghinkgo story"


def test_say_leaves_checked_words_alone():
    # these are deliberately NOT in the lexicon
    for w in ("tinnitus", "Beethoven", "cochlea"):
        assert pronounce.say(w) == w


def test_say_does_not_match_inside_words():
    assert pronounce.say("percepts") == "percepts"


@needs_espeak
def test_lexicon_still_does_what_it_claims():
    """Fails if espeak's behaviour changes under us."""
    assert pronounce.verify() == []


def test_say_is_case_insensitive_and_preserves_case():
    """A sentence-initial word is exactly where a listener hears the miss.

    This shipped: `ginkgo` was replaced and `Ginkgo` was not, so one chapter
    pronounced it both ways.
    """
    assert pronounce.say("ginkgo biloba") == "ghinkgo biloba"
    assert pronounce.say("Ginkgo biloba") == "Ghinkgo biloba"
    assert pronounce.say("GINKGO") == "GHINKGO"
    # and the other direction, for keys stored capitalised
    assert pronounce.say("Cochrane") == "Kockrun"
    assert pronounce.say("the cochrane review") == "the kockrun review"
