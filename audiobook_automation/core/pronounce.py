"""Pronunciation control for the synthesiser.

Kokoro phonemizes with espeak, which reads from **spelling**. So a word the
model gets wrong is fixed by respelling it for the engine, not by annotating
it. This module keeps the respellings in one place and, crucially, keeps them
*checkable*: every entry records the IPA espeak produced before and after, and
`verify()` re-runs espeak to confirm the respelling still does what the comment
claims.

The written manuscript is never altered. Respelling happens on the way into the
synthesiser only, because the manuscript is also a document a human reads.

    python -m audiobook_automation pronounce verify
    python -m audiobook_automation pronounce check <file.md> ...
"""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class Fix:
    """One respelling, with the evidence for it."""
    respell: str
    was: str        # IPA espeak gave for the real spelling
    now: str        # IPA espeak gives for the respelling
    why: str


# Words espeak gets wrong. Measured with:
#     espeak-ng -q --ipa -v en-us "<word>"
LEXICON: dict[str, Fix] = {
    "Ludwig": Fix(
        "Loodvig", "lˈʌdwɪɡ", "lˈuːdvɪɡ",
        "Hard English W. Should be a V, as in LOOD-vig."),
    "Wegeler": Fix(
        "Vaygueler", "wˈɛdʒəlɚ", "vˈeɪɡɛlɚ",
        "Read as WEJ-uh-ler. German: VAY-guh-ler, hard g."),
    "Heiligenstadt": Fix(
        "Hyliggenshtat", "hˈaɪlaɪdʒənstˌæt", "hˈaɪlɪɡˌɛnʃtæt",
        "Soft g and a flat st. German has a hard g and a sht."),
    "Pawel": Fix(
        "Pahvel", "pˈɔːl", "pˈɑːvəl",
        "espeak says 'Paul'. The Polish name is PAH-vel."),
    "anechoic": Fix(
        "annekoic", "eɪntʃˈoʊɪk", "ˌænɪkˈoʊɪk",
        "Read with a CH. The ch is a hard k."),
    "cochlear": Fix(
        "cocklear", "kˈɑːtʃlɪɹ", "kˈɑːklɪɹ",
        "Same CH error. Note 'cochlea' on its own is already correct."),
    "Cochrane": Fix(
        "Kockrun", "kˈɑːkɹeɪn", "kˈɑːkɹʌn",
        "Rhymed with 'rain'. The organisation is KOK-run."),
    "ginkgo": Fix(
        "ghinkgo", "dʒˈɪŋkɡoʊ", "ɡˈɪŋkɡoʊ",
        "Soft g: JINK-go. Should be a hard GINK-go."),
    "percept": Fix(
        "persept", "pɚsˈɛpt", "pˈɜːsɛpt",
        "Verb stress. As a noun it is PER-cept."),
}

# Checked and deliberately NOT fixed. Kept here so nobody 'fixes' them later.
LEAVE_ALONE: dict[str, str] = {
    "tinnitus": "tˈɪnɪɾəs is the standard clinical pronunciation. Correct. "
                "Worth checking first in any tinnitus book, since it is said "
                "hundreds of times.",
    "Beethoven": "bˈeɪtoʊvən is already correct. Every respelling tried was "
                 "worse: 'Baytohven' turns the hard t into an American flap "
                 "(BAY-doh-ven) and hyphenated forms add a second stress. "
                 "When a listener says Beethoven sounds wrong, check the word "
                 "*before* it - it was 'Ludwig' - and check the speed.",
    "Jastreboff": "dʒˈæstɹɪbˌɔf. The Polish would be 'ya-', but he has "
                  "published in English for decades and clinicians say the J.",
    "cochlea": "kˈɑːkliːə. Correct, unlike 'cochlear'.",
    "audiologist": "ˌɔːdɪˈoʊlədʒˌɪst. Correct.",
    "a.m.": "'three a.m.' gives θɹˈiː ˌeɪˈɛm, which reads naturally.",
}


def say(text: str) -> str:
    """Manuscript text in, synthesiser text out."""
    for word, fix in LEXICON.items():
        text = re.sub(rf"\b{re.escape(word)}\b", fix.respell, text)
        text = re.sub(rf"\b{re.escape(word.lower())}\b",
                      fix.respell.lower(), text)
    return text


def ipa(text: str) -> str:
    """What espeak will hand the model. Empty string if espeak is missing."""
    if not shutil.which("espeak-ng"):
        return ""
    return subprocess.run(["espeak-ng", "-q", "--ipa", "-v", "en-us", text],
                          capture_output=True, text=True).stdout.strip()


def verify() -> list[str]:
    """Re-measure every entry. Returns a list of problems, empty if clean."""
    if not shutil.which("espeak-ng"):
        return ["espeak-ng not installed, cannot verify"]
    bad = []
    for word, fix in LEXICON.items():
        was, now = ipa(word), ipa(fix.respell)
        if was != fix.was:
            bad.append(f"{word}: espeak now gives {was!r}, "
                       f"lexicon recorded {fix.was!r}")
        if now != fix.now:
            bad.append(f"{word} -> {fix.respell}: now {now!r}, "
                       f"recorded {fix.now!r}")
        if now == was:
            bad.append(f"{word}: respelling changes nothing")
    return bad


# Words worth a look in any manuscript: proper nouns, and the technical terms
# that recur in health writing. `check` reports what espeak does with each one
# found, so a human can judge. It cannot know what is *right* - only a person
# who knows the word can - so it reports rather than asserts.
def check(text: str) -> list[tuple[str, str, bool]]:
    """Return (word, ipa, is_handled) for unusual words found in `text`."""
    words = set(re.findall(r"\b[A-Za-z][A-Za-z'-]{3,}\b", text))
    interesting = {
        w for w in words
        if (w[0].isupper() and w.lower() not in _COMMON) or len(w) > 11
    }
    known = {k.lower() for k in LEXICON} | {k.lower() for k in LEAVE_ALONE}
    return sorted((w, ipa(w), w.lower() in known) for w in interesting)


_COMMON = {
    "the", "this", "that", "these", "those", "there", "then", "they", "their",
    "what", "when", "where", "which", "while", "with", "would", "your", "you",
    "and", "but", "for", "not", "now", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten", "here", "have", "has", "had",
    "because", "before", "after", "about", "every", "most", "some", "something",
    "nothing", "anything", "everything", "chapter", "conclusion", "introduction",
}
