#!/usr/bin/env python3
"""The supplemental PDF that ships beside the audiobook.

    python projects/ai-content/supplemental_pdf.py

Six pages: the argument in one page, the ten checks as a pre-publish sheet,
the thirty day reset, a channel rules sheet to fill in, an experiment card,
and the sources. Written out rather than generated from the manuscript,
because a listener wants a working document, not a transcript.

**Boxes to tick, like the crypto companion.** The practice here is a set of
checks done on every video and a month of one-off jobs, so a checklist is
the point. The ten-check page is meant to be printed once per video.

Every number matches the audiobook and its audit in `book/SOURCES.md`. Our
own channel findings appear as ratios and seconds only, as in the book.

Google Play Books takes one PDF per audiobook, under 100MB. Spotify has no
documented supplemental upload.
"""
from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, HRFlowable,
                                PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-ai-slop"))
PDF = OUT / "Stop-Making-AI-Slop-companion.pdf"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")
ACCENT = HexColor("#C8402E")    # one accent colour, a signal red

# White page, dark ink: a companion gets printed.
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
    "box": ParagraphStyle("box", fontName="Helvetica", fontSize=10,
                          leading=14.5, textColor=INK),
    "ref": ParagraphStyle("ref", fontName="Helvetica", fontSize=8.4,
                          leading=12, textColor=INK, leftIndent=11,
                          firstLineIndent=-11, spaceAfter=6),
    "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9,
                           leading=13.5, textColor=MUTED, spaceBefore=6,
                           spaceAfter=8),
    "q": ParagraphStyle("q", fontName="Helvetica-Bold", fontSize=10,
                        leading=14, textColor=INK, spaceBefore=8,
                        spaceAfter=2),
}


def P(t, s="p"):
    return Paragraph(t, S[s])


def LI(t):
    return Paragraph(t, S["li"], bulletText="•")


class _Square(Flowable):
    """An empty tick box, drawn rather than typed.

    Helvetica has no empty-box glyph and substitutes a filled square, which
    reads as "already done"; a ZapfDingbats box rendered filled as well.
    """

    def wrap(self, *_):
        return 4 * mm, 4 * mm

    def draw(self):
        self.canv.setStrokeColor(INK)
        self.canv.setLineWidth(0.7)
        self.canv.rect(0, 0.4 * mm, 3.2 * mm, 3.2 * mm)


def BOX(t):
    """A one-off job with a box to tick when it is done."""
    row = Table([[_Square(), Paragraph(t, S["box"])]],
                colWidths=[7 * mm, 159 * mm], hAlign="LEFT")
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("TOPPADDING", (0, 0), (-1, -1), 1),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return row


def rule():
    return HRFlowable(width="100%", thickness=0.6, color=RULE,
                      spaceBefore=4, spaceAfter=10)


def write_lines(n=2):
    """Blank ruled lines to write an answer on."""
    t = Table([[""] for _ in range(n)], colWidths=[166 * mm],
              rowHeights=[8 * mm] * n, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE)]))
    return t


def page_furniture(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(20 * mm, A4[1] - 12 * mm, A4[0] - 20 * mm, A4[1] - 12 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "Stop Making AI Slop")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Oktay Shakirov")
    canvas.restoreState()


def story():
    s = []

    # --- 1: the argument in one page -------------------------------------
    s += [P("Stop Making AI Slop", "title"),
          P("Why most AI videos die in seven seconds, and how to make ones "
            "people actually watch.", "sub"),
          rule(),
          P("This is the working companion to the audiobook: the ten checks "
            "to run on every video, the thirty day reset, a sheet for your "
            "own channel rules, and an experiment card. Print the checks. "
            "Keep the rules where you and your AI tools will read them.",
            "lead"),
          P("No earnings promises. Nothing here says what a channel will make.",
            "note"),
          P("The argument in one page", "h"),
          P("AI made making a video free, so making stopped being an "
            "advantage. Everyone has the same tools. What decides whether a "
            "video lives is what the tools cannot do: choosing a subject "
            "people already want, the first seconds, a picture that says what "
            "the voice says, and an editor who says no. Slop is not a tool. "
            "It is a missing editor."),
          LI("<b>Supply is not attention.</b> In April 2026 Deezer said 44 "
             "percent of the new tracks delivered to it each day were fully AI "
             "generated, and that AI music was 1 to 3 percent of streams, 85 "
             "percent of those detected as fraudulent."),
          LI("<b>The feed is full of it.</b> In Kapwing's test, 104 of the "
             "first 500 Shorts shown to a brand new account were AI slop: "
             "about one in five."),
          LI("<b>Sentence two decides.</b> In our curves, Shorts that gave the "
             "answer away in sentence two lost half their audience in about "
             "nine seconds. Those that held it back kept half for about "
             "eighteen."),
          LI("<b>The rules target the template, not the tool.</b> YouTube "
             "does not monetise \"AI-generated content made with generic or "
             "unoriginal templates giving the impression of mass "
             "production.\" It does allow the same intro and outro if the "
             "bulk of each video is different."),
          LI("<b>The platform tests every upload.</b> YouTube's signals are "
             "clicks, watch time, survey responses, sharing, likes and "
             "dislikes. Volume does not train it to like you."),
          P("The one question", "h"),
          P("Before every upload, watched on a phone, as a stranger: "
            "<b>would I watch this?</b> If the answer is no, fix it or let it "
            "go.", "lead"),
          PageBreak()]

    # --- 2: the ten checks ----------------------------------------------
    s += [P("The ten checks", "title"),
          P("Chapter eleven, as a pre-publish sheet. Print one per video. A "
            "rough pass on every check beats a perfect pass on three.", "sub"),
          rule(),
          Table([["Video", "", "Date", ""]],
                colWidths=[14 * mm, 96 * mm, 12 * mm, 44 * mm], hAlign="LEFT",
                style=TableStyle([
                    ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, RULE),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, RULE)])),
          Spacer(1, 6),
          BOX("<b>1. Demand.</b> People are already choosing to watch this subject. Somebody "
              "much bigger is not already answering it well. The people "
              "looking for it are the viewers I want back."),
          BOX("<b>2. Title.</b> Written before the script, as the phrase people actually type. "
              "For a Short, the first spoken line asks that same question."),
          BOX("The door I expect viewers to use, written down: search, home, "
              "suggested or the Shorts feed."),
          BOX("<b>3. Sentence two.</b> It does not give the answer away. It hands over a task, names "
              "the kind of answer, or overturns what the title assumed."),
          BOX("<b>4. The ear.</b> Script read aloud. Empty clever lines cut. Turns between ideas "
              "said in words. Numbers written as spoken. No one word "
              "sentences."),
          BOX("<b>5. Facts.</b> Every number, date and quote read in its source. Anything "
              "without a source is cut."),
          BOX("<b>6. Voice.</b> The channel's one voice, at its measured pace. Every name "
              "listened to, and every fix added to the names list."),
          BOX("<b>7. Picture.</b> Watched with the sound off, then listened to with eyes closed. "
              "Every noun the voice says is on screen. Lists appear one item "
              "at a time. Spoken numbers are shown. Text only where it adds "
              "something."),
          BOX("<b>8. Thumbnail.</b> Checked at phone size in a feed. Every word readable. It asks "
              "the title's question and never points at the wrong answer. A "
              "face only if the video is about that person."),
          BOX("<b>9. Ending and disclosure.</b> A Short ends cold, on the fact or the thing to do, so it loops. "
              "No closing \"what do you think?\"."),
          BOX("Realistic synthetic content disclosed in the upload screen."),
          BOX("<b>10. The curve.</b> After a few days: the first hard drop found and matched to the "
              "script line; traffic source checked against the door I wrote "
              "down; one change chosen for the next video."),
          Spacer(1, 8),
          P("Notes", "q"),
          write_lines(5),
          PageBreak()]

    # --- 3: the thirty day reset ----------------------------------------
    s += [P("The thirty day reset", "title"),
          P("Chapter twelve. One job a week. Thirty days will not make a "
            "channel big; they change how you work.", "sub"),
          rule(),
          P("Week one: the audit (make nothing)", "h2"),
          BOX("Day 1. Last ten videos: the second each one first drops hard, "
              "and the exact sentence spoken there."),
          BOX("Day 2. The traffic source of each of the ten, next to its "
              "title."),
          BOX("Day 3. What each video's sentence two did: gave the answer, "
              "handed over a task, named the kind of answer, or overturned "
              "the title."),
          BOX("Days 4 and 5. A topic list from what people already watch, "
              "every topic through the three demand questions."),
          BOX("Days 6 and 7. Three old videos in a row with the sound off. "
              "Every place the picture and the voice disagree, written down."),
          P("Week two: the rebuild (upload nothing)", "h2"),
          BOX("Four topics written through all ten checks."),
          BOX("Voice chosen, pace measured in words per minute and written "
              "down, names list started."),
          BOX("At least three openers, and none runs three videos in a row."),
          BOX("Thumbnail rules decided. Picture built line by line for all "
              "four scripts."),
          P("Week three: the experiment", "h2"),
          BOX("One change chosen, its judging number named, and what would "
              "prove it wrong written down before any data (page five)."),
          BOX("The four videos published across the week, not at once. No "
              "panic fifth video."),
          P("Week four: the reading", "h2"),
          BOX("New curves read beside the ten old ones. Result judged against "
              "the line written in week three, failed or not."),
          BOX("Everything learned written as rules on page four, where you "
              "and your AI tools will read them every time."),
          BOX("Day 30. Next round planned: a shorter audit, four topics, one "
              "change."),
          PageBreak()]

    # --- 4: my channel rules --------------------------------------------
    s += [P("My channel rules", "title"),
          P("The editor, written down. Start it in week four and add to it "
            "after every video. Paste it into the instructions your AI tools "
            "work from.", "sub"),
          rule(),
          P("My channel is for:", "q"),
          P("The viewers I want back, in one sentence.", "note"),
          write_lines(1),
          P("My voice, and its measured pace:", "q"),
          write_lines(1),
          P("Names and terms the voice gets wrong, and the fix:", "q"),
          write_lines(3),
          P("Sentence twos that hold for my audience:", "q"),
          write_lines(2),
          P("My openers, in rotation:", "q"),
          write_lines(2),
          P("Thumbnail rules:", "q"),
          write_lines(2),
          P("Things I have rejected, and why:", "q"),
          P("Every rejection becomes a rule, so the same mistake gets harder "
            "to make.", "note"),
          write_lines(4),
          PageBreak()]

    # --- 5: the experiment card -----------------------------------------
    s += [P("The experiment card", "title"),
          P("One change at a time. Fill in the first three lines before the "
            "video goes out. Once the numbers are in front of you, it is easy "
            "to tell yourself a story.", "sub"),
          rule()]
    for n in (1, 2):
        s += [P(f"Experiment {n}", "h"),
              P("The one thing I am changing:", "q"),
              write_lines(1),
              P("The number that judges it:", "q"),
              write_lines(1),
              P("The result that would prove me wrong:", "q"),
              write_lines(1),
              P("What happened, and the rule I am keeping:", "q"),
              write_lines(2)]
    s.append(PageBreak())

    # --- 6: sources -----------------------------------------------------
    s += [P("Sources", "title"),
          P("The main outside sources behind the audiobook. Every figure was "
            "checked against these before narration. Findings from our own "
            "channels are stated as ratios and seconds.", "sub"),
          rule()]
    refs = [
        ("The content farm",
         ["Nieman Lab Encyclo, Demand Media; Christian Science Monitor, 25 "
          "November 2009, on Wired's \"The Answer Factory\" (October 2009).",
          "CNN Money, 26 January 2011: Demand Media IPO valued at more than "
          "$1 billion.",
          "Google Official Blog, \"Finding more high-quality sites in "
          "search\", 24 February 2011 (the Panda update).",
          "SEC filings: Leaf Group Ltd., formerly Demand Media, Inc. (2016); "
          "Graham Holdings acquisition of Leaf Group (2021)."]),
        ("Supply and the feed",
         ["Merriam-Webster, 2025 Word of the Year: slop.",
          "Deezer, as reported by TechCrunch, 20 April 2026: 44 percent of "
          "daily new uploads fully AI; 1 to 3 percent of streams.",
          "Kapwing, \"AI Slop Report: The Global Rise of Low Quality AI "
          "Videos\", 28 November 2025.",
          "The Guardian, 12 August 2025: AI-only channels among YouTube's "
          "fastest growing (Playboard data)."]),
        ("How YouTube recommends",
         ["Cristos Goodrow, \"On YouTube's recommendation system\", YouTube "
          "blog, 15 September 2021."]),
        ("The rules",
         ["YouTube, \"5 ways we're toughening our approach to protect "
          "families\", 22 November 2017.",
          "Google Search, March 2024 core update and spam policies (scaled "
          "content abuse), 5 March 2024.",
          "YouTube, \"How we're helping creators disclose altered or "
          "synthetic content\", 18 March 2024.",
          "YouTube Help, \"YouTube channel monetization policies\" "
          "(inauthentic content, from 15 July 2025).",
          "Meta for Creators, unoriginal content on Facebook, 14 July 2025.",
          "Spotify, AI protections and spam removals, 25 September 2025.",
          "Neal Mohan, \"From the CEO: What's coming to YouTube in 2026\", "
          "21 January 2026."]),
    ]
    for heading, items in refs:
        s.append(P(heading, "h2"))
        for it in items:
            s.append(Paragraph(it, S["ref"]))
    s += [rule(),
          P("Narration is synthetic: the audiobook is read by Kokoro, an AI "
            "voice, from a script a person chose, checked and signed off.",
            "note")]
    return s


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=20 * mm,
        title="Stop Making AI Slop - companion",
        author="Oktay Shakirov",
        subject="Companion to the audiobook Stop Making AI Slop")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="body")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=page_furniture)])
    doc.build(story())
    print(f"{PDF}  ({PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
