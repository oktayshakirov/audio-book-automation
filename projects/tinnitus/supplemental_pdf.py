#!/usr/bin/env python3
"""The supplemental PDF that ships beside the audiobook.

    python projects/tinnitus/supplemental_pdf.py

Four pages: what the book argues, the thirty day reset, the practice, and the
sources. Written out rather than generated from the manuscript, because a
listener wants a reminder card and not a transcript.

**Deliberately not a tracker.** The book names the elimination diet as the
fear loop "wearing an apron", and chapter eleven says to write one line a week
and never daily. A tidy daily checklist would contradict the argument and
teach the monitoring behaviour the book spends an hour dismantling. Nothing
here has a box to tick.

Google Play Books takes one PDF per audiobook, under 100MB. Spotify has no
documented supplemental upload. Keep it to a handful of pages.
"""
from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, PageBreak,
                                PageTemplate, Paragraph, Spacer)

OUT = Path(os.environ.get("AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook"))
PDF = OUT / "Shut-Up-Tinnitus-companion.pdf"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")

# White page, dark ink. The cover is near-black, but a companion PDF gets
# printed, and nobody thanks you for a full-bleed black A4.
S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26,
                            leading=29, textColor=INK, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=10.5,
                          leading=15, textColor=MUTED, spaceAfter=18),
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=14,
                        leading=17, textColor=INK, spaceBefore=16,
                        spaceAfter=7),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5,
                         leading=14, textColor=INK, spaceBefore=11,
                         spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10, leading=15,
                        textColor=INK, spaceAfter=8, alignment=TA_LEFT),
    "lead": ParagraphStyle("lead", fontName="Helvetica", fontSize=11.5,
                           leading=17, textColor=INK, spaceAfter=10),
    "li": ParagraphStyle("li", fontName="Helvetica", fontSize=10, leading=15,
                         textColor=INK, leftIndent=11, bulletIndent=1,
                         spaceAfter=5),
    "ref": ParagraphStyle("ref", fontName="Helvetica", fontSize=8.4,
                          leading=12, textColor=INK, leftIndent=11,
                          firstLineIndent=-11, spaceAfter=6),
    "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9,
                           leading=13.5, textColor=MUTED, spaceBefore=6,
                           spaceAfter=8),
}


def P(t, s="p"):
    return Paragraph(t, S[s])


def LI(t):
    return Paragraph(t, S["li"], bulletText="•")


def rule():
    return HRFlowable(width="100%", thickness=0.6, color=RULE,
                      spaceBefore=4, spaceAfter=10)


def page_furniture(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "Shut Up, Tinnitus")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "tinnitushelp.me")
    canvas.restoreState()


def story():
    s = []

    # --- 1: what the book argues ---------------------------------------
    s += [P("Shut Up, Tinnitus", "title"),
          P("Why your ears ring, why it gets louder, and how to make it "
            "disappear into the background.", "sub"),
          rule(),
          P("This is a companion to the audiobook. It is a reminder, not a "
            "summary, and it is not a worksheet. There is nothing here to "
            "fill in, on purpose.", "lead"),
          P("The argument in one page", "h"),
          P("There is no cure for tinnitus. That matters far less than it "
            "sounds, because the volume of your tinnitus and the suffering "
            "it causes are two different measurements and they are barely "
            "related."),
          LI("<b>The sound is normal.</b> Eighty adults with healthy hearing "
             "and no tinnitus were put in a soundproof room. Ninety four "
             "percent of them heard it within minutes."),
          LI("<b>It is not in your ears.</b> Surgeons cut the auditory nerve "
             "to stop it. In one published series, fifty five percent of "
             "patients were the same or worse, permanently deaf in that ear "
             "with the ringing still there."),
          LI("<b>The suffering is learned.</b> Two people with identical "
             "measurements live completely different lives. What differs is "
             "whether the signal is wired to threat."),
          LI("<b>So it is reachable.</b> The loop runs on your reaction, not "
             "on the volume, and a loop only needs one link broken."),
          P("You are not going to make it shut up. You are going to stop "
            "listening.", "lead"),
          PageBreak()]

    # --- 2: the thirty day reset ---------------------------------------
    s += [P("The thirty day reset", "title"),
          P("One change at a time. Parts of it feel worse before they feel "
            "better, and the chapter says where.", "sub"),
          rule(),
          P("Week one, sound and nothing else", "h2"),
          P("Low, dull sound in the rooms you live in, quiet enough that you "
            "can still find your tinnitus underneath it. In the bedroom from "
            "lights out until morning, every night, running before anything "
            "happens rather than switched on when things get bad. Earplugs "
            "out of ordinary life: they stay for concerts, power tools, "
            "motorbikes and anything genuinely loud, and nowhere else."),
          P("Week two, the three second practice", "h2"),
          P("Every time you notice the sound: notice it, do not check it, "
            "put your attention back on what you were doing. You will do it "
            "badly. Catching yourself late still counts. Plus the highest "
            "value minute of your day, which is getting out of bed on waking "
            "rather than lying there running the morning inventory."),
          P("Week three, drop one safety behaviour", "h2"),
          P("One. The one you would miss least. For a few days afterwards "
            "you will feel more anxious and the sound will seem more "
            "present. That is not a relapse and it is not evidence the "
            "behaviour was helping. Removing a protection reliably raises "
            "anxiety in the short term and lowers it over the longer one. "
            "Also this week: stop searching. One month off."),
          P("Week four, occupation", "h2"),
          P("Three times this week, do something that genuinely demands you. "
            "Not pleasant background activity, which leaves half your "
            "attention free to drift back and check. Something slightly too "
            "hard. Move your body most days, for the sleep and the arousal "
            "rather than for your ears."),
          P("Day thirty", "h2"),
          P("You will probably not feel much better, and that is written "
            "here deliberately. Habituation does not run on a thirty day "
            "clock. What changes first is not the volume and not how often "
            "you notice. It is the recovery: a spike that used to wreck "
            "three days starts costing an afternoon."),
          P("Do not score yourself. If you write anything down, one line a "
            "week, never daily.", "note"),
          PageBreak()]

    # --- 3: the practice ------------------------------------------------
    s += [P("The practice", "title"),
          P("Three seconds, done badly, several hundred times a week.",
            "sub"),
          rule(),
          P("1. Notice it. 2. Do not check it: no comparing to this morning, "
            "no measuring against yesterday, no testing whether it is better "
            "or worse. 3. Let it stay, and put your attention back on "
            "whatever you were doing.", "lead"),
          P("Every time the sound is present and you do not react, you run "
            "one trial in which the alarm fires and nothing bad follows. "
            "That is how learned fear comes apart. Not through insight, "
            "through repetition without consequence."),
          P("Safety behaviours to drop, one at a time", "h"),
          P("Anything you do to protect yourself from the sound. Each one "
            "feels protective and each one sends the same message to your "
            "nervous system: this is dangerous, stay alert. You cannot talk "
            "yourself out of fear while behaving like a person in danger."),
          LI("Earplugs in a normal restaurant, or avoiding the restaurant"),
          LI("Masking cranked up to drown it rather than sit underneath it"),
          LI("Checking, first thing, every morning"),
          LI("Testing it in the car when the engine goes off"),
          LI("Searching for new research at one in the morning"),
          LI("Asking someone whether they think it sounds louder today"),
          P("Sound enrichment, three rules", "h"),
          LI("<b>Keep it boring.</b> No lyrics, no podcasts, no music you "
             "love. Rain, a fan, broadband noise, moving water."),
          LI("<b>Match it roughly.</b> A high ring blends into white noise "
             "or rain; a lower tone or roar sits better under brown noise."),
          LI("<b>Keep it quiet.</b> If you can still hear your own sound "
             "faintly underneath, the level is right. You are not trying to "
             "drown it out: your brain cannot habituate to a signal it is "
             "not receiving."),
          P("When to see a doctor instead", "h"),
          P("<b>If your tinnitus is only in one ear, pulses in time with "
            "your heartbeat, arrived suddenly, or came with hearing loss or "
            "dizziness, get examined.</b> Those specific patterns can mean "
            "something treatable and occasionally something serious. This "
            "audiobook is not a diagnosis and its author is not your "
            "doctor."),
          PageBreak()]

    # --- 4: sources -----------------------------------------------------
    s += [P("Sources", "title"),
          P("Every number in the audiobook traces to one of these. Thirteen "
            "claims were audited after drafting and seven were corrected, "
            "all of them in the same direction: the draft was more dramatic "
            "than the evidence supported.", "sub"),
          rule()]
    refs = [
        ("The sound is normal",
         ["Heller MF, Bergman M. Tinnitus aurium in normally hearing "
          "persons. Annals of Otology, Rhinology and Laryngology, 1953; "
          "62:73-83.",
          "Del Bo L et al. Tinnitus aurium in persons with normal hearing: "
          "55 years later. Otolaryngology-Head and Neck Surgery, 2008; "
          "139(3):391-394."]),
        ("It is generated centrally",
         ["House JW. Management of the Tinnitus Patient. Annals of Otology, "
          "Rhinology and Laryngology, 1981; 90(6).",
          "Roberts LE et al. Ringing Ears: The Neuroscience of Tinnitus. "
          "Journal of Neuroscience, 2010; 30(45):14972."]),
        ("Distress is separate from loudness",
         ["Jastreboff PJ, Hazell JWP. A neurophysiological approach to "
          "tinnitus: clinical implications. British Journal of Audiology, "
          "1993; 27:7-17.",
          "Meyer M et al. Psychoacoustic Tinnitus Loudness and "
          "Tinnitus-Related Distress Show Different Associations with "
          "Oscillatory Brain Activity. PLOS ONE, 2013; 8(1):e53180."]),
        ("Silence, sound and overprotection",
         ["Formby C et al., 2003. Two weeks of earplug use reduced sound "
          "tolerance by an average of about 7 dB.",
          "Bootzin RR. Stimulus control therapy, 1972. A core component of "
          "CBT for insomnia."]),
        ("Jaw and neck",
         ["Won JY et al. Prevalence and Factors Associated with Neck and Jaw "
          "Muscle Modulation of Tinnitus. Audiology and Neurotology, 2013; "
          "18(4). 163 patients, 19 manoeuvres, 57 percent of ears "
          "modulated."]),
        ("Caffeine and supplements",
         ["St Claire L et al. Caffeine abstinence: an ineffective and "
          "potentially distressing tinnitus therapy. International Journal "
          "of Audiology, 2010.",
          "Sereda M et al. Ginkgo biloba for tinnitus. Cochrane Database of "
          "Systematic Reviews, 2022; CD013514.pub2.",
          "Person OC et al. Zinc supplementation for tinnitus. Cochrane "
          "Database of Systematic Reviews, 2016; CD009832.pub2.",
          "Nocini R, Henry BM, Mattiuzzi C, Lippi G. Effect of melatonin "
          "supplementation on tinnitus. Acta Biomedica, 2024; "
          "95(2):e2024006."]),
        ("How common, and what works",
         ["Jarach CM et al. Global Prevalence and Incidence of Tinnitus: A "
          "Systematic Review and Meta-analysis. JAMA Neurology, 2022.",
          "Fuller T et al. Cognitive behavioural therapy for tinnitus. "
          "Cochrane Database of Systematic Reviews, 2020; CD012614.pub2."]),
    ]
    for heading, items in refs:
        s.append(P(heading, "h2"))
        for it in items:
            s.append(Paragraph(it, S["ref"]))
    s += [rule(),
          P("Narration is synthetic. More at tinnitushelp.me, including a "
            "free library of sound sessions for the enrichment described in "
            "week one.", "note")]
    return s


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=20 * mm,
        title="Shut Up, Tinnitus - companion",
        author="tinnitushelp.me",
        subject="Companion to the audiobook Shut Up, Tinnitus")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="body")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=page_furniture)])
    doc.build(story())
    print(f"{PDF}  ({PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
