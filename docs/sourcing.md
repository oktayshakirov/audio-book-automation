# Sourcing, and the drift that will bite you

This matters most for health, finance, legal or any other subject where a
confident wrong number can hurt someone. It is also the part of making a book
that is easiest to skip and most expensive to skip.

## The finding

On the first book built with this pipeline, **thirteen factual claims were
audited after drafting. Seven were wrong or overstated.**

Every single error ran in the same direction: the drafted version was more
dramatic than the evidence supported.

That is not bad luck. It is a systematic bias in how persuasive prose gets
written, and it will happen again unless something catches it.

## What the seven looked like

They were not fabrications. Each one started from something real:

- **A collated range presented as a finding.** "38 to 85 percent across the
  studies" had no single paper behind it, and the draft then used a sentence
  sitting at the extreme end. Replaced with one surgeon's published outcome:
  45 percent improved, 55 percent the same or worse. Weaker number, far
  stronger citation.
- **A secondary summary mistaken for a primary series.** "Roughly half"
  became, on checking the actual papers, between one in ten and one in five.
- **Two evidence grades merged under one confident word.** "Probably better
  than X or Y" where only one of the two comparisons was moderate certainty
  and the other was low certainty from a single study.
- **An inference stated as a finding.** "It does not reduce loudness" when the
  review simply does not measure loudness. The correction was both true and
  rhetorically stronger: the best-supported treatment is not even asking.
- **A traditional account repeated past the current scholarship.** A
  biographical detail "everyone knows" that specialists now dispute.
- **Understating** in one case, which is the same sin pointed the other way: a
  positive meta-analysis omitted because it complicated the argument.
- **Unsourced flourishes.** "It has been embarrassing researchers for forty
  years." "In every species that has ever been studied." These sound like
  claims and are not, and they survive because no flag is attached to them.

## The rules

1. **Never invent an expert, a quote, a study or a statistic.** The obvious
   one, and not the one that fails.
2. **Source before drafting, not after.** The audit exists to catch what slips
   through, not to do the work.
3. **Keep a `SOURCES.md` with a row per claim**, carrying the exact numbers,
   the named source, and a status. An item with no status is an item nobody
   checked.
4. **Mark the status honestly.** "Verified" means someone read it. "Verified
   (secondary)" is a different thing and must say so.
5. **Write care points.** When a sentence is load-bearing for safety or
   honesty, say so next to the claim, so a later edit for pace does not remove
   it. Examples that earned one: a drug interaction warning, a
   protect-your-ears-here-but-not-there distinction, and a chapter that
   deliberately predicts the reader will not feel better in thirty days.
6. **Watch the flourishes.** Any sentence of the form "in every X" or "for
   forty years" is a claim wearing a costume.
7. **Inherit nothing.** Content from your own site or blog is not a source. If
   the blog's own figure carries an unresolved placeholder, you will ship it.

## Blocked lookups

If a source cannot be reached - a paywall, a bot wall, a sandbox refusal -
**say so in `SOURCES.md` and leave the claim marked open.** Do not quietly
downgrade to a secondary citation and call it verified. On this book the one
genuinely load-bearing claim was behind Cloudflare on two hosts and had to be
read from the publisher's own summary page instead; the route taken is
recorded next to the claim.
