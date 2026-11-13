#!/usr/bin/env python3
"""The upload sheet: everything the author types or uploads, on paper.

    python projects/job-search/metadata_pdf.py

Metadata, description, keywords, chapter titles and lengths, the per-store
upload table, the spoken credit text, and a pre-submit checklist. The same
values as projects/job-search/README.md; if one changes, change both.
"""
from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (Flowable, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

OUT = Path(os.environ.get(
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-job-hunting"))
PDF = OUT / "Job-Hunting-in-the-Age-of-AI-metadata.pdf"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")
ACCENT = HexColor("#C8402E")

TITLE = "Job Hunting in the Age of AI"
SUBTITLE = "Why Nobody Answers Anymore, and How to Reach a Human"
AUTHOR = "Oktay Shakirov"
SLUG = "Job-Hunting-in-the-Age-of-AI"

S = {
    "t": ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=22,
                        leading=26, textColor=INK, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=10,
                          leading=14, textColor=MUTED, spaceAfter=12),
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13,
                        leading=16, textColor=ACCENT, spaceBefore=12,
                        spaceAfter=6),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.5,
                        leading=13.5, textColor=INK, spaceAfter=6),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.8,
                           leading=11.5, textColor=INK),
    "mono": ParagraphStyle("mono", fontName="Courier", fontSize=8.8,
                           leading=11.5, textColor=INK),
    "box": ParagraphStyle("box", fontName="Helvetica", fontSize=9.5,
                          leading=13.5, textColor=INK),
}


def P(t, s="p"):
    return Paragraph(t, S[s])


def C(t, s="cell"):
    return Paragraph(t, S[s])


class _Square(Flowable):
    def wrap(self, *_):
        return 4 * mm, 4 * mm

    def draw(self):
        self.canv.setStrokeColor(INK)
        self.canv.setLineWidth(0.7)
        self.canv.rect(0, 0.4 * mm, 3.2 * mm, 3.2 * mm)


def BOX(t):
    row = Table([[_Square(), Paragraph(t, S["box"])]],
                colWidths=[7 * mm, 163 * mm], hAlign="LEFT")
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("TOPPADDING", (0, 0), (-1, -1), 1),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return row


def grid(rows, widths, header=True):
    t = Table(rows, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HexColor("#F2F2F5")))
    t.setStyle(TableStyle(style))
    return t


META = [
    ("Title", TITLE),
    ("Subtitle", SUBTITLE),
    ("Author", AUTHOR),
    ("Narrator", "Kokoro (AI Voice)"),
    ("Language", "English"),
    ("Category", "BUSINESS & ECONOMICS / Careers / Job Hunting (BUS037020)"),
    ("Second category", "COMPUTERS / Artificial Intelligence / General "
                        "(COM004000)"),
    ("Price", "$4.99 on every store (Google enforces price parity)"),
    ("Runtime", "61:42, 14 tracks"),
    ("Copyright", "\u00a9 2026 Oktay Shakirov"),
    ("AI narration", "Yes. Disclose on every store."),
]

DESCRIPTION = [
    "Five hundred and eighty seven job postings in one week. Four worth an "
    "application.",
    "You have sent dozens of applications, maybe hundreds, and heard nothing "
    "back. Job Hunting in the Age of AI is a one-hour, plain-spoken guide to "
    "why that happens and what to do instead. It opens around 1970, with a "
    "graduate student asking a few hundred workers how they found their jobs, "
    "and an answer that still explains hiring today: not a friend, an "
    "acquaintance.",
    "Then it follows what happened when AI made applying free. Why a "
    "polished, tailored cover letter stopped meaning anything. Where the "
    "famous claim that software rejects three quarters of applications really "
    "came from, and what actually happens after you press send. Why the door "
    "for beginners narrowed, and why some of the jobs you apply for were "
    "never there. Four short chapters cover the mistakes that make an "
    "application easy to ignore: letting the machine write the letter, "
    "applying to everything, missing the fine print, and trying to trick the "
    "filter.",
    "Then the practice: ten steps for a search a person on the other side "
    "will answer, and a thirty day plan to rebuild yours around them. For "
    "graduates, career changers, people coming back to work, and anyone "
    "applying through a screen and hearing nothing.",
    "No promise of a job. No tricks for beating the machines. Just how hiring "
    "works now, and how to reach a human.",
    "Narrated by Kokoro, an AI voice.",
]

KEYWORDS = ("job search, job hunting, ai job search, ghost jobs, applicant "
            "tracking system, resume, cover letter, entry level jobs, tech "
            "jobs, ai interview, career change, hiring")

CHAPTERS = [
    ("01-intro", "Introduction: You Are Not Being Rejected. You Are Not Being "
                 "Read.", "4:00"),
    ("02-ch01", "Chapter 1: Not a Friend, an Acquaintance", "5:11"),
    ("03-ch02", "Chapter 2: Applying Got Free, So It Stopped Meaning "
                "Anything", "5:07"),
    ("04-ch03", "Chapter 3: Nobody Is Rejecting You at Two in the Morning",
     "5:26"),
    ("05-ch04", "Chapter 4: The Door for Beginners Got Narrower", "4:48"),
    ("06-ch05", "Chapter 5: The Job That Was Never There", "4:36"),
    ("07-ch06", "Chapter 6: You Let the Machine Write the Letter", "3:06"),
    ("08-ch07", "Chapter 7: You Applied to Everything", "3:09"),
    ("09-ch08", "Chapter 8: You Saw the Word Remote and Stopped Reading",
     "3:26"),
    ("10-ch09", "Chapter 9: You Tried to Trick the Machine", "3:38"),
    ("11-ch10", "Chapter 10: You Are Not Applying to Jobs. You Are Choosing "
                "Companies.", "3:08"),
    ("12-ch11", "Chapter 11: Run a Search a Human Will Answer", "7:48"),
    ("13-ch12", "Chapter 12: The Thirty Day Search Reset", "5:13"),
    ("14-outro", "Conclusion: Be the Application a Person Wants to Answer",
     "2:58"),
]

UPLOADS = [
    ("01-intro.mp3 ... 14-outro.mp3", "yes", "yes", "yes"),
    (f"{SLUG}-sample-spotify.mp3 (9:13)", "-", "yes", "-"),
    (f"{SLUG}-sample-ar.mp3 (4:01)", "-", "-", "yes"),
    (f"{SLUG}-opening-credits.mp3 (0:11)", "-", "-", "yes"),
    (f"{SLUG}-closing-credits.mp3 (0:12)", "-", "-", "yes"),
    (f"{SLUG}-cover-3000.jpg", "yes", "yes", "yes"),
    (f"{SLUG}-companion.pdf (6 pages)", "yes", "-", "-"),
]

OPENING = (f"This is {TITLE}. {SUBTITLE}. Written by {AUTHOR}. "
           "Narrated by Kokoro.")
CLOSING = (f"You have been listening to {TITLE}. Written by {AUTHOR}. "
           "Narrated by Kokoro. The End. Thank you for listening.")

CHECKS = [
    "Cover text read back character for character: title and subtitle "
    "exactly as above, no word shortened to fit.",
    "Cover flattened to an RGB JPEG, 3000 x 3000 (ChatGPT exports carry an "
    "alpha channel).",
    "Title and subtitle pasted, not typed, into every store's fields. The "
    "subtitle is what tells this book apart from Job Hunting in the AI Era: "
    "never leave it out where a field takes one.",
    "Narrator field reads Kokoro (AI Voice); AI narration disclosed on every "
    "store.",
    "Price $4.99 on all three stores.",
    "Author's Republic: Google Play deselected as a channel (email them; it "
    "is not self-serve).",
    "Author's Republic: opening and closing credits and the 4:01 sample "
    "uploaded. Spotify: the 9:13 sample.",
    "Google Play: companion PDF attached.",
    "All 14 chapter files uploaded in order, titles as in the chapter table.",
    "Spot-listen: the first 30 seconds of the intro and the opening credits "
    "(the title is the line a reviewer always hears).",
]


def furniture(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(20 * mm, A4[1] - 12 * mm, A4[0] - 20 * mm, A4[1] - 12 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, f"{TITLE} - upload sheet")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"page {doc.page}")
    canvas.restoreState()


def story():
    s = [P(TITLE, "t"),
         P("Upload sheet: everything the stores ask for, in one place.", "sub"),
         P("Metadata", "h"),
         grid([[C(f"<b>{k}</b>"), C(v)] for k, v in META],
              [34 * mm, 136 * mm], header=False),
         P("Description", "h")]
    s += [P(p) for p in DESCRIPTION]
    s += [P("Keywords", "h"), P(KEYWORDS),
          PageBreak(),
          P("Chapters", "h"),
          grid([[C("<b>#</b>"), C("<b>File</b>"), C("<b>Chapter title</b>"),
                 C("<b>Length</b>")]] +
               [[C(str(i)), C(f, "mono"), C(t), C(d)]
                for i, (f, t, d) in enumerate(CHAPTERS, 1)],
               [8 * mm, 22 * mm, 124 * mm, 16 * mm]),
          P("Total 61:42. Every file 44.1 kHz, 192 kbps MP3, 1.5 seconds of "
            "silence at head and tail, peak -3.2 dB or lower."),
          P("Uploads per store", "h"),
          grid([[C("<b>File</b>"), C("<b>Google Play</b>"),
                 C("<b>Spotify</b>"), C("<b>Author's Republic</b>")]] +
               [[C(f, "mono"), C(a), C(b), C(c)] for f, a, b, c in UPLOADS],
               [86 * mm, 26 * mm, 22 * mm, 36 * mm]),
          P("All files are in ~/Desktop/audiobook-job-hunting/."),
          P("Spoken credits", "h"),
          P(f"<b>Opening:</b> {OPENING}"),
          P(f"<b>Closing:</b> {CLOSING}"),
          PageBreak(),
          P("Before you press submit", "h")]
    s += [BOX(c) for c in CHECKS]
    s += [Spacer(1, 10),
          P("If a store rejects anything, note the exact wording of the "
            "rejection: the fix is usually one line in "
            "projects/job-search/job-hunting-in-the-age-of-ai.py and a re-render of "
            "one file.", "sub")]
    return s


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(PDF), pagesize=A4, leftMargin=20 * mm,
                            rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm,
                            title=f"{TITLE} - upload sheet", author=AUTHOR)
    doc.build(story(), onFirstPage=furniture, onLaterPages=furniture)
    print(f"{PDF}  ({PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
