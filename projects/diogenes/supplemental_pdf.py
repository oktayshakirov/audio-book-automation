#!/usr/bin/env python3
"""The supplemental PDF that ships beside the audiobook.

    python projects/diogenes/supplemental_pdf.py

Seven pages: the argument on one page, the nightly cup audit, the five
exercises, the ask and wine jar logs, the thirty day plan, the list test,
and the sources. Written out rather than generated from the manuscript,
because a listener wants a working document, not a transcript.

Boxes to tick and lines to write on, like the earlier companions. Every
claim matches the audiobook and its audit in `book/SOURCES.md`; the stories
are told as stories, as in the book.

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
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-not-caring"))
PDF = OUT / "The-Art-of-Not-Caring-What-They-Think-companion.pdf"

TITLE = "The Art of Not Caring What They Think"
AUTHOR = "Oktay Shakirov"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")
ACCENT = HexColor("#B07A2A")    # one accent colour, a bronze

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


def grid(header, n_rows, widths, row_h=9):
    """A blank log: a header row and empty rows to write in."""
    rows = [[Paragraph(h, S["cell"]) for h in header]]
    rows += [[""] * len(header) for _ in range(n_rows)]
    t = Table(rows, colWidths=[w * mm for w in widths],
              rowHeights=[8 * mm] + [row_h * mm] * n_rows, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F1EEE8")),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
    ]))
    return t


def story():
    s = []

    # --- 1. The argument ----------------------------------------------------
    s += [P(TITLE, "title"),
          P("Diogenes, the Cynics and the Freedom of Needing Nothing. "
            "Companion to the audiobook: the idea on one page, then the "
            "sheets for the exercises and the thirty day plan.", "sub"),
          P("You are exactly as free as your list of needs is short.", "lead"),
          P("Diogenes was not free because he did not care. He did not care "
            "because he needed almost nothing from anybody, and a person who "
            "needs nothing cannot be bought, flattered or frightened. Stopping "
            "caring is not a switch. Needing less is a practice."),
          P("Three piles", "h"),
          LI("<b>Needs.</b> Food, water, warmth, sleep, a roof, a few people who "
             "would come if you called at night. Short, and real. Keep them."),
          LI("<b>Wants.</b> Things you would like and would be fine without. "
             "A want you know is a want has no grip on you."),
          LI("<b>Handles.</b> A need that lives in someone else's head: a need "
             "for an opinion, not a thing. It disguises itself as a real need. "
             "Whoever holds the other end can move you."),
          P("The two questions", "h"),
          LI("Is this a need, a want, or a handle?"),
          LI("If I did not have this, what would actually happen?"),
          P("Three ways people reach for a handle", "h"),
          P("<b>Reward</b> (do this and you will get that), <b>flattery</b> "
            "(you are the only one who understands), <b>threat</b> (the "
            "disapproval, the friend who goes quiet). Each one only works "
            "through a need. Noticing which of the three it is changes the "
            "moment."),
          P("The audience in your head", "h"),
          P("Three findings from social psychology, all pointing the same way. "
            "People overestimate how much others notice their appearance and "
            "actions (the spotlight effect). They overestimate how much others "
            "can see what they feel inside (the illusion of transparency). And "
            "after a conversation they underestimate how much the other person "
            "liked them (the liking gap). The audience in your head is bigger, "
            "sharper and harsher than the one in the room."),
          PageBreak()]

    # --- 2. The cup audit -----------------------------------------------------
    s += [P("The cup audit", "title"),
          P("Every evening: three moments from the day when you did something "
            "for the audience. Name the handle. Do not fix anything yet; just "
            "count. Print one sheet per week.", "sub"),
          grid(["Day", "The moment", "Whose opinion?", "Need, want or handle?"],
               21, [14, 82, 40, 30], row_h=9),
          P("At the end of the week: which two or three handles came back most "
            "often? Those are your biggest cups.", "note"),
          write_lines(2),
          PageBreak()]

    # --- 3. The five exercises --------------------------------------------------
    s += [P("The five exercises", "title"),
          P("Each one trains a different handle. They are reps, not a cure: "
            "nobody stops minding a no after the first one.", "sub"),
          P("1. The cup audit", "h2"),
          P("Three moments a night, named and counted. It shows you the "
            "handles."),
          P("2. Begging from statues", "h2"),
          P("The story goes that Diogenes asked a statue for money, \"to get "
            "practice in being refused.\" Once a day, ask for something you "
            "expect to be refused: a discount, a better table, a favour, more "
            "time. Expect more yeses than you think; in one study people "
            "underestimated how often others would agree to a direct request "
            "by as much as half."),
          P("3. The wine jar", "h2"),
          P("The story goes that Diogenes dragged a wine jar on a rope through "
            "the streets, to teach a man who was too embarrassed to pick up a "
            "dropped loaf. In 1968 the psychologist Albert Ellis created the "
            "shame attacking exercise: something mildly embarrassing, in "
            "public, on purpose. His examples: calling out the time in a "
            "crowded department store, wearing something strange, asking a "
            "hardware store whether it sells tobacco. It is a standard part of "
            "his therapy but has not been tested on its own in a controlled "
            "trial."),
          P("4. Hot sand and snow", "h2"),
          P("Diogenes rolled in hot sand in summer and hugged snow covered "
            "statues in winter. Once a day, choose a small discomfort: walk "
            "instead of the bus, a plain meal, the phone left at home for an "
            "evening. Nothing dangerous; nothing that harms your body."),
          P("5. The warm no", "h2"),
          P("Once a week, decline something you do not want to do. \"Thank you "
            "for thinking of me, I am going to pass this time.\" No excuse, no "
            "long apology. People who turn down invitations overestimate how "
            "much the other person minds."),
          rule(),
          P("The rule for every exercise", "h2"),
          P("Harm nobody. Not yourself, not anyone else. Nothing illegal, "
            "nothing that frightens people, nothing at another person's "
            "expense. The embarrassment is yours alone."),
          P("If the fear of being judged stops ordinary life (speaking up in "
            "class, asking for help, talking to a cashier), that may be social "
            "anxiety disorder. It is common, and cognitive behavioural therapy "
            "is a research supported treatment for it. See a therapist: they "
            "will take you through this kind of practice more safely than an "
            "audiobook can.", "note"),
          PageBreak()]

    # --- 4. Logs ------------------------------------------------------------------
    s += [P("The statue log", "title"),
          P("One ask a day. Write what you asked and what happened.", "sub"),
          grid(["Day", "What I asked for", "Yes or no", "How it felt after"],
               10, [14, 86, 22, 44], row_h=9),
          P("The wine jar log", "h"),
          P("Before: how bad do you expect it to feel, from 0 to 10? After: "
            "how many people actually reacted? You are measuring your own "
            "spotlight effect.", "p"),
          grid(["Day", "What I did (harmless)", "Expected (0 to 10)",
                "People who reacted"], 6, [14, 86, 33, 33], row_h=10),
          PageBreak()]

    # --- 5. Thirty days -----------------------------------------------------------
    s += [P("Thirty days without a handle", "title"),
          P("One exercise added each week. The honest prediction: on day "
            "thirty you will still care. What changes is the speed. You will "
            "notice the pull sooner, and have a moment to choose.", "sub"),
          P("Week one, days 1 to 7: notice", "h2"),
          BOX("Cup audit every evening. Change nothing else."),
          BOX("Day 7: find your two or three biggest cups."),
          P("Week two, days 8 to 14: beg from statues", "h2"),
          BOX("Keep the audit. One ask a day, starting tiny."),
          BOX("Raise the stakes a little each day."),
          BOX("Day 14: ask for something you really want and would normally "
              "never request."),
          P("Week three, days 15 to 21: the warm no and the shopping test", "h2"),
          BOX("Keep the audit and the daily ask."),
          BOX("At least two warm noes this week."),
          BOX("Before every purchase: would I still want this if nobody could "
              "ever see it?"),
          P("Week four, days 22 to 28: the wine jar, hot sand and snow", "h2"),
          BOX("Keep the audit; ask every other day."),
          BOX("One chosen discomfort every day."),
          BOX("Three wine jars this week, smallest first. Harm nobody."),
          P("Days 29 and 30: restamp the currency", "h2"),
          BOX("Day 29: the list test, on the next page."),
          BOX("Day 30: write the message you have been putting off. Write it "
              "once, check it once, send it, put the phone down."),
          P("After day thirty, keep two habits: the cup audit a few evenings a "
            "week, and one statue a week.", "note"),
          PageBreak()]

    # --- 6. The list test ---------------------------------------------------------
    s += [P("The list test", "title"),
          P("The list you were handed: the job, the title, the salary, the "
            "flat, the life. For each item, the hardest question in the "
            "audiobook. Keep what survives. For what does not, do nothing "
            "dramatic: just know which coins are lead.", "sub"),
          grid(["Item on the list", "Who handed it to me?",
                "If I reached it and could never tell anyone, would I still "
                "want it?"], 9, [62, 44, 60], row_h=12),
          P("Deface the currency", "h"),
          P("Every society runs on a currency of approval: what counts as a "
            "respectable job, what a successful person owns, what you may say "
            "at dinner. Pick each coin up and look at it. Who stamped this? "
            "What is it actually worth? Why am I paying with it?"),
          write_lines(4),
          PageBreak()]

    # --- 7. Sources ---------------------------------------------------------------
    s += [P("Sources", "title"),
          P("The stories come to us mostly through one ancient writer, who "
            "collected them from older books, most of them now lost, and often "
            "gives rival versions. They are told as stories, not as "
            "documented events.", "sub")]
    refs = [
        ("The ancient source",
         ["Diogenes Laertius, Lives of Eminent Philosophers, Book VI, trans. "
          "R. D. Hicks (Loeb, 1925): the auction (6.29, 6.74), the cup (6.37), "
          "Alexander (6.32, 6.38, 6.60, 6.68), the statue (6.49), sand and "
          "snow (6.23, 6.34), the coinage (6.20, 6.21, 6.56, 6.71), the wine "
          "jar (6.35), the laughers (6.58), Crates (6.85 to 6.93), Hipparchia "
          "(6.96 to 6.98), his death and grave (6.76 to 6.78)."]),
        ("Feeling watched, seen through and disliked",
         ["Gilovich, Medvec and Savitsky, \"The spotlight effect in social "
          "judgment\", Journal of Personality and Social Psychology 78(2), "
          "2000.",
          "Gilovich, Savitsky and Medvec, \"The illusion of transparency\", "
          "Journal of Personality and Social Psychology 75(2), 1998.",
          "Boothby, Cooney, Sandstrom and Clark, \"The liking gap in "
          "conversations\", Psychological Science, 2018."]),
        ("Buying, saying yes, chasing",
         ["Dittmar, Bond, Hurst and Kasser, \"The relationship between "
          "materialism and personal well-being: a meta-analysis\", Journal of "
          "Personality and Social Psychology 107(5), 2014.",
          "Givi and Kirk, \"Saying no: The negative ramifications from "
          "invitation declines are less severe than we think\", Journal of "
          "Personality and Social Psychology, 2024.",
          "Flynn and Lake, \"If you need help, just ask\", Journal of "
          "Personality and Social Psychology 95(1), 2008.",
          "Niemiec, Ryan and Deci, \"The path taken\", Journal of Research in "
          "Personality, 2009.",
          "Thorstein Veblen, The Theory of the Leisure Class, 1899."]),
        ("Practice",
         ["Albert Ellis on shame attacking exercises, as quoted in Donald "
          "Robertson, The Philosophy of Cognitive-Behavioural Therapy "
          "(Ellis and MacLaren 2005; Dryden and Ellis 2001).",
          "Ray DiGiuseppe, \"A forty year follow-up of the efficacy of shame "
          "attacking exercises: a single case study\", Albert Ellis Institute.",
          "National Institute of Mental Health, \"Social Anxiety Disorder: "
          "What You Need to Know\"."]),
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
