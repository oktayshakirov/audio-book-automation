# Pronunciation

Kokoro phonemizes with **espeak**, which reads from spelling. A word the model
gets wrong is therefore fixed by respelling it for the engine, not by
annotating it.

## Check before you listen

You can read what the model will say without rendering anything:

```bash
espeak-ng -q --ipa -v en-us "cochlear"      # kˈɑːtʃlɪɹ  <- wrong
espeak-ng -q --ipa -v en-us "cocklear"      # kˈɑːklɪɹ   <- right
```

This is faster and more reliable than auditioning by ear, and it works for
words you are not sure how to judge.

```bash
python -m audiobook_automation pronounce check <manuscript.md>
python -m audiobook_automation pronounce verify
```

`check` lists unusual words in a manuscript with the phonemes espeak gives, so
a human can judge. `verify` re-measures every lexicon entry and fails if
espeak's behaviour has changed under you.

## The respelling never touches the manuscript

Respelling happens on the way into the synthesiser. The written manuscript
stays spelled correctly, because it is also a document a human reads and it is
the thing you would hand to a human narrator.

## What actually goes wrong

From one real book, nine of nine checked words were wrong in four patterns:

**Soft g where it should be hard.** `ginkgo` -> "JINK-go". `Wegeler` ->
"WEJ-uh-ler". `Heiligenstadt` -> "HY-ly-jen-stat".

**ch read as CH where it should be K.** `anechoic` -> "ayn-CHO-ik".
`cochlear` -> "KOTCH-lir" (while `cochlea` alone is correct, so check every
inflection).

**Foreign names anglicised to the wrong word entirely.** `Pawel` -> "Paul".
`Ludwig` -> "LUD-wig" with a hard English W.

**Noun/verb stress.** `percept` as per-CEPT rather than PER-cept.

## Three traps

**The word that sounds wrong may not be the wrong word.** A listener reported
"Beethoven" sounding wrong. espeak renders Beethoven correctly. The error was
**Ludwig**, immediately before it, plus a too-slow speed smearing the phrase.
Check the neighbours before respelling the word someone named.

**A respelling can be worse than the default.** Every attempt to "fix"
Beethoven made it worse: one turned the hard t into an American flap
("BAY-doh-ven"), hyphenated forms added a second stress. **Measure the
respelling, do not assume it helps.** That is why the lexicon stores the IPA
before and after.

**Check the word your book says hundreds of times, first.** For a tinnitus
book that is "tinnitus" - `tˈɪnɪɾəs`, which is correct. If it had not been,
every track would have needed re-rendering.

## Deliberate non-fixes

Keep a `LEAVE_ALONE` list with reasons, or someone will "fix" a word that was
right. Example: `Jastreboff` gets an English J rather than the Polish "ya-",
because he has published in English for decades and clinicians say the J.
