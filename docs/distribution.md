# Distribution

Researched, not yet executed. Verify before relying on any of it: these
platform rules move.

## Decide the route before you narrate

This is the one decision that can invalidate finished audio, so make it early
even though it feels like the last step.

**Spotify's own direct upload path reportedly only accepts AI-narrated audio
produced through its partners** (ElevenLabs, Google Play Books, Spoken), not
an externally produced file. A locally synthesised file therefore needs to
come in through an aggregator.

**Author's Republic accepts third-party AI narration** with written
disclosure, and follows the Audio Publishers Association's AI narration naming
guidelines. But **not all of its downstream retailers accept AI-narrated
titles**, so reach is smaller than the catalogue suggests.

**Disclosure is required essentially everywhere now.** Plan for the audiobook
to be labelled synthetic. That is a marketing fact to design around, not a
problem to hide.

So: if the voice must be locally synthesised, the route is an aggregator. If
wide distribution matters more than the voice, that argues for a partner
engine instead, and that decision changes which tool renders the book.

## Licensing

Kokoro is **Apache 2.0**, so commercial use of the output is fine. Confirm the
licence of any voice pack you add; a community collection is not automatically
permissive.

## Audio specs

Targets gathered during research, to confirm against the distributor's current
spec sheet:

- 44.1 kHz sample rate
- 192 kbps or higher MP3
- peak at -3 dBFS or below
- roughly -23 to -18 dB RMS
- **one file per chapter**

The `BOOK` chain in `core/voices.py` targets `loudnorm=I=-20:TP=-3`, and the
renderer writes 44.1 kHz 192 kbps MP3, one file per manuscript. Loudness
normalisation to a LUFS target is not identical to an RMS window, so measure
the finished files against whatever the distributor actually asks for rather
than assuming the chain satisfies it.

## Pricing

The reference title sits at $3.99 with a $4.99 recommended price, for 68
minutes. That is the shape of this market: short, cheap, and sold on the hook
rather than the hour count.
