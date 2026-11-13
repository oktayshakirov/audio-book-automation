#!/usr/bin/env python3
"""The supplemental PDF that ships beside the audiobook.

    python projects/job-search/supplemental_pdf.py

Six pages: the argument in one page, the hard filter sheet, the ten steps as
a per-application checklist, an application log, the thirty day reset, and
the sources. Written out rather than generated from the manuscript, because a
listener wants a working document, not a transcript.

**Boxes to tick, like the crypto and slop companions.** The ten-step page is
meant to be printed once per application; the log is meant to be printed as
many times as it fills.

Every number matches the audiobook and its audit in `book/SOURCES.md`. The
author's own search appears as ratios only, as in the book: no employer, no
city, no outcome.

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
                                PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-job-hunting"))
PDF = OUT / "Job-Hunting-in-the-Age-of-AI-companion.pdf"

TITLE = "Job Hunting in the Age of AI"
AUTHOR = "Oktay Shakirov"

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
    "cell": ParagraphStyle("cell", fontName="Helvetica-Bold", fontSize=8.2,
                           leading=10, textColor=INK),
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
    """A check or a one-off job, with a box to tick when it is done."""
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
    canvas.drawString(20 * mm, 12 * mm, TITLE)
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, AUTHOR)
    canvas.restoreState()


def story():
    s = []

    # --- 1: the argument in one page -------------------------------------
    s += [P(TITLE, "title"),
          P("Why nobody answers anymore, and how to reach a human.", "sub"),
          rule(),
          P("This is the working companion to the audiobook: your hard "
            "filters, the ten steps as a checklist for every application, a "
            "log to keep, and the thirty day reset. Print the checklist and "
            "the log. Write the filters before you look at a single posting.",
            "lead"),
          P("No promise of a job. Nothing here can promise an outcome that "
            "depends on a market and a stranger's decision.", "note"),
          P("The argument in one page", "h"),
          P("AI made applying free, so applying stopped meaning anything. "
            "Both sides now automate, and the cold application is the one "
            "channel the machines flooded. Jobs still move the way they always "
            "did: through people who know of you. Use the machine for finding, "
            "reading and checking. Do the part it cannot do yourself: "
            "choosing, proving and being real."),
          LI("<b>Jobs move through people.</b> Around 1970, more than half "
             "of the workers in Granovetter's Newton survey found their job "
             "through someone they knew, most often an acquaintance. In 2022, "
             "a test on more than twenty million LinkedIn users found the "
             "moderately weak ties did the most to move people into new jobs."),
          LI("<b>A free signal says nothing.</b> After an AI cover letter tool "
             "arrived on a large freelance platform, the link between a "
             "well-matched letter and a callback fell by about half."),
          LI("<b>The void is mostly volume.</b> The famous \"three in four "
             "applications are rejected by software\" has no study behind it. "
             "Knockout questions do reject automatically, on your own answers; "
             "most other applications are simply never reached."),
          LI("<b>Some jobs are not there.</b> One hiring software company "
             "estimated that about one in five postings on its platform were "
             "for roles nobody was actively trying to fill."),
          LI("<b>Almost nothing survives a real filter.</b> In one week of the "
             "author's own search, five hundred and eighty seven postings left "
             "four worth an application."),
          P("The one rule", "h"),
          P("Do not reject yourself on wishes. <b>Do reject the job on "
            "gates.</b> And put one real person on the other side of every "
            "application you send.", "lead"),
          PageBreak()]

    # --- 2: the hard filter sheet ----------------------------------------
    s += [P("My hard filters", "title"),
          P("Step one. Write these before you open a job board, with a clear "
            "head. At eleven at night, after a week of silence, this page is "
            "the only thing that argues with the tired version of you.", "sub"),
          rule(),
          P("Where I can live and work:", "q"),
          P("Countries, cities, time zones. Work permits I already hold.",
            "note"),
          write_lines(2),
          P("Office days I can manage, at most:", "q"),
          write_lines(1),
          P("Languages I can really work in, and at what level:", "q"),
          write_lines(2),
          P("The kind of work I want:", "q"),
          write_lines(2),
          P("The kind of work I will not do:", "q"),
          write_lines(2),
          P("My honest level, one step up at most:", "q"),
          write_lines(1),
          P("Anything else that is a gate for me:", "q"),
          P("Contract type, travel, shifts, a licence I hold or do not.",
            "note"),
          write_lines(2),
          P("If a filter does not fit on one line, it is not a filter yet.",
            "note"),
          PageBreak()]

    # --- 3: the ten steps, per application --------------------------------
    s += [P("The ten steps", "title"),
          P("Chapter eleven, as a checklist. Print one per application.", "sub"),
          rule(),
          Table([["Company", "", "Role", ""]],
                colWidths=[18 * mm, 70 * mm, 12 * mm, 66 * mm], hAlign="LEFT",
                style=TableStyle([
                    ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, RULE),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, RULE)])),
          Spacer(1, 6),
          BOX("<b>1. Filters.</b> The role passes every line of my hard "
              "filter sheet."),
          BOX("<b>2. Company first.</b> This organisation is on my list, or "
              "has earned a place on it, with one line on why."),
          BOX("<b>3. Source checked.</b> Found on the employer's own page, "
              "still open, published within about two months by their date, "
              "and the employer is the one hiring."),
          BOX("<b>4. Gates and wishes.</b> Every gate cleared. Core "
              "requirements missed: about one, apply; three or more, skip."),
          BOX("<b>5. Fine print.</b> Where the person can live, office days, "
              "language level and use, real vacancy, salary range: answered "
              "in the ad or asked."),
          BOX("<b>6. Machine as checker.</b> AI listed the gates and wishes, "
              "compared my CV with the ad, and flagged every claim my CV does "
              "not back. Nothing it invented is left in."),
          BOX("<b>7. Short, in the ad's language, with proof.</b> One specific "
              "reason I chose them, one piece of work a stranger can open, one "
              "honest sentence about my biggest gap."),
          BOX("<b>8. One human.</b> A real person connected to this role, "
              "written to with one specific question, not a request for a "
              "job."),
          BOX("<b>9. Interview ready.</b> Examples prepared as for a person, "
              "including for an AI interview; asked whether a human "
              "conversation is possible."),
          BOX("<b>10. Logged.</b> Date, link, check, contact and status "
              "written in the log."),
          Spacer(1, 8),
          P("The person I contacted, and the question I asked:", "q"),
          write_lines(2),
          P("Notes", "q"),
          write_lines(3),
          PageBreak()]

    # --- 4: the application log -------------------------------------------
    head = ["Date", "Company", "Link to the employer's posting", "Checked",
            "Person contacted", "Status"]
    widths = [16 * mm, 28 * mm, 44 * mm, 19 * mm, 33 * mm, 26 * mm]
    rows = [[Paragraph(h, S["cell"]) for h in head]] + \
           [[""] * len(head) for _ in range(18)]
    log = Table(rows, colWidths=widths, rowHeights=[9 * mm] + [10 * mm] * 18,
                hAlign="LEFT", repeatRows=1)
    log.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F2F2F5")),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE")]))
    s += [P("The application log", "title"),
          P("Step ten. One row per application. After a few weeks it becomes "
            "a funnel, and the funnel tells you where the search breaks.",
            "sub"),
          rule(),
          log,
          P("No replies at all: the channel or the fit. Replies but nothing "
            "moves: the CV and the proof. Interviews but no offers: the "
            "interviews.", "note"),
          PageBreak()]

    # --- 5: the thirty day reset ------------------------------------------
    s += [P("The thirty day reset", "title"),
          P("Chapter twelve. One job a week. For these thirty days, every "
            "application goes through the ten steps, or it does not go.",
            "sub"),
          rule(),
          P("Week one: build the frame", "h2"),
          BOX("Day 1. Hard filters written, one page, one line each."),
          BOX("Thirty organisations listed, each with one line on why it is "
              "there."),
          BOX("Every careers page visited; everything open checked against "
              "the filters and the employer's own date."),
          P("Week two: build your proof, and your people", "h2"),
          BOX("CV rewritten role by role: every duty replaced with a result "
              "or a piece of evidence."),
          BOX("Two pieces of work a stranger can open, linked where a reader "
              "sees them first."),
          BOX("Ten moderately weak ties listed and contacted, each with one "
              "real question."),
          P("Week three: apply, carefully", "h2"),
          BOX("At most ten applications, each through all ten steps."),
          BOX("A human attached to every one, or a note in the log that none "
              "could be found."),
          P("Week four: read the funnel, and change one thing", "h2"),
          BOX("Counted: applications, replies, conversations, interviews."),
          BOX("Where it breaks, written down."),
          BOX("One change chosen, and the result that would prove it failed "
              "written down before the data comes in."),
          P("The change, and the result that would prove it failed:", "q"),
          write_lines(2),
          BOX("Day 30. Same filters unless one proved wrong, the list "
              "updated, more proof, more people. Start again."),
          PageBreak()]

    # --- 6: sources -------------------------------------------------------
    s += [P("Sources", "title"),
          P("The main outside sources behind the audiobook. Every figure was "
            "checked against these before narration. The author's own search "
            "is stated as ratios only.", "sub"),
          rule()]
    refs = [
        ("Weak ties",
         ["Mark Granovetter, \"The Strength of Weak Ties\", American Journal "
          "of Sociology 78(6), 1973; Getting a Job, 1974.",
          "Rajkumar, Saint-Jacques, Bojinov, Brynjolfsson and Aral, \"A causal "
          "test of the strength of weak ties\", Science 377, 2022.",
          "Brown, Setren and Topa, \"Do Informal Referrals Lead to Better "
          "Matches?\", Journal of Labor Economics, 2016."]),
        ("Applying got free",
         ["Galdin and Silbert, \"Making Talk Cheap: Generative AI and Labor "
          "Market Signaling\", arXiv 2511.08785, 2025.",
          "Cui, Dias and Ye, \"Signaling in the Age of AI: Evidence from Cover "
          "Letters\", arXiv 2509.25054, 2025.",
          "Wiles, Munyikwa and Horton, \"Algorithmic Writing Assistance on "
          "Jobseekers' Resumes Increases Hires\", NBER w30886; Management "
          "Science, 2025.",
          "Greenhouse, AI in Hiring Report, 19 November 2025; Candidate AI "
          "Interview Report, 2026."]),
        ("What happens to an application",
         ["CIO.com and Fortune (22 August 2014) on Preptel and the 75 percent "
          "figure.",
          "Workable and Gem help centres on knockout questions.",
          "Harvard Business School and Accenture, \"Hidden Workers: Untapped "
          "Talent\", September 2021.",
          "Reuters, 10 October 2018, on Amazon's experimental screening tool.",
          "Mobley v. Workday, N.D. Cal., collective certified May 2025."]),
        ("The market",
         ["U.S. Bureau of Labor Statistics, Job Openings and Labor Turnover "
          "Survey, 2026 releases.",
          "Stanford Digital Economy Lab, \"Canaries in the Coal Mine\" and "
          "its 2026 updates.",
          "Yale Budget Lab, AI and the labor market, 2025 and 2026.",
          "Indeed Hiring Lab, software development postings index, via FRED.",
          "Bitkom, IT skills study, 2025.",
          "Greenhouse internal data as reported by the Wall Street Journal, "
          "January 2025; Gartner candidate surveys, 2024 and 2025.",
          "Ontario Employment Standards Act, job posting rules in force 1 "
          "January 2026."]),
        ("Gates, wishes and tricks",
         ["Behavioural Insights Team, \"Gender differences in response to "
          "requirements in job adverts\", March 2022.",
          "Burning Glass Institute and Harvard Business School, "
          "\"Skills-Based Hiring\", February 2024.",
          "The New York Times, October 2025, on hidden text in resumes "
          "(ManpowerGroup, Greenhouse).",
          "U.S. Department of Justice, 30 June 2025, on North Korean remote "
          "IT worker schemes."]),
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
        title=f"{TITLE} - companion", author=AUTHOR,
        subject=f"Companion to the audiobook {TITLE}")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="body")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=page_furniture)])
    doc.build(story())
    print(f"{PDF}  ({PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
