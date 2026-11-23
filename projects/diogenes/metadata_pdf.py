#!/usr/bin/env python3
"""The upload sheet: everything the author types or uploads, on paper.

    python projects/diogenes/metadata_pdf.py

Metadata, description, keywords, chapter titles and lengths, the per-store
upload table, the spoken credit text, and a pre-submit checklist. The same
values as projects/diogenes/README.md; if one changes, change both.
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
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-not-caring"))
PDF = OUT / "The-Art-of-Not-Caring-What-They-Think-metadata.pdf"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")
ACCENT = HexColor("#B07A2A")

TITLE = "The Art of Not Caring What They Think"
SUBTITLE = "Diogenes, the Cynics and the Freedom of Needing Nothing"
AUTHOR = "Oktay Shakirov"
SLUG = "The-Art-of-Not-Caring-What-They-Think"

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
    ("Category", "PHILOSOPHY / History &amp; Surveys / Ancient &amp; Classical "
                 "(PHI002000)"),
    ("Second category", "SELF-HELP / Personal Growth / Self-Esteem "
                        "(SEL023000)"),
    ("Price", "$4.99 on every store (Google enforces price parity)"),
    ("Runtime", "50:21, 13 tracks"),
    ("Copyright", "\u00a9 2026 Oktay Shakirov"),
    ("AI narration", "Yes. Disclose on every store."),
]

DESCRIPTION = [
    "A man stands on a slave auction block. The crier asks what he can do. "
    "He answers: govern men. Then he points at a rich buyer in the crowd and "
    "says, sell me to that man. He needs a master.",
    "You edit a message four times before you send it. You rehearse "
    "conversations that never happen. You say yes when you mean no, and stay "
    "quiet when you have the answer. The Art of Not Caring What They Think "
    "is a one-hour guide to why, built on one of the strangest philosophers "
    "of ancient Greece: Diogenes, the man who lived in a tub, told Alexander "
    "the Great to stand out of his light, and begged from statues to "
    "practise being refused.",
    "His secret was not that he stopped caring. It was that he needed almost "
    "nothing from anybody, and a person who needs nothing cannot be bought, "
    "flattered or frightened. The book follows that idea from the old "
    "stories into modern research: why you feel watched far more than you "
    "are, why people like you more than you think, why saying no costs less "
    "than you fear, and why reaching goals like money and image so often "
    "fails to help. Three short chapters name where the approval habit "
    "hides: in what you buy, in the yes you did not mean, and in the "
    "ambitions you were handed.",
    "Then the practice: five exercises drawn from what the Cynics actually "
    "did, from begging at statues to dragging a wine jar through the street, "
    "with their modern descendants from psychology, and a thirty day plan "
    "to put them to work.",
    "No promise that you will stop caring in a month. No invitation to live "
    "in a tub. Just a way to need less from what goes on in other people's "
    "heads.",
    "Narrated by Kokoro, an AI voice.",
]

KEYWORDS = ("diogenes, cynicism, stoicism, ancient philosophy, people "
            "pleasing, social anxiety, self esteem, confidence, spotlight "
            "effect, minimalism, how to stop caring what people think, "
            "philosophy for everyday life")

CHAPTERS = [
    ("01-intro", "Introduction: You Edited That Message Four Times.", "3:52"),
    ("02-ch01", "Chapter 1: The Man on the Auction Block", "4:40"),
    ("03-ch02", "Chapter 2: The Cup", "4:22"),
    ("04-ch03", "Chapter 3: Stand Out of My Light", "4:05"),
    ("05-ch04", "Chapter 4: The Audience in Your Head", "4:02"),
    ("06-ch05", "Chapter 5: Deface the Currency", "4:05"),
    ("07-ch06", "Chapter 6: You Are Not Shopping. You Are Buying an "
                "Opinion.", "2:39"),
    ("08-ch07", "Chapter 7: You Are Not Being Polite. You Are Hiding.",
     "2:56"),
    ("09-ch08", "Chapter 8: You Call It Ambition. It Is a Leash.", "2:58"),
    ("10-ch09", "Chapter 9: Needing Nothing Is Not Having Nothing", "2:39"),
    ("11-ch10", "Chapter 10: Begging From Statues", "6:17"),
    ("12-ch11", "Chapter 11: Thirty Days Without a Handle", "5:08"),
    ("13-outro", "Conclusion: Prepared for Every Fortune", "2:31"),
]

UPLOADS = [
    ("01-intro.mp3 ... 13-outro.mp3", "yes", "yes", "yes"),
    (f"{SLUG}-sample-spotify.mp3 (8:34)", "-", "yes", "-"),
    (f"{SLUG}-sample-ar.mp3 (3:52)", "-", "-", "yes"),
    (f"{SLUG}-opening-credits.mp3 (0:11)", "-", "-", "yes"),
    (f"{SLUG}-closing-credits.mp3 (0:12)", "-", "-", "yes"),
    (f"{SLUG}-cover-3000.jpg", "yes", "yes", "yes"),
    (f"{SLUG}-companion.pdf (7 pages)", "yes", "-", "-"),
]

OPENING = (f"This is {TITLE}. {SUBTITLE}. Written by {AUTHOR}. "
           "Narrated by Kokoro.")
CLOSING = (f"You have been listening to {TITLE}. Written by {AUTHOR}. "
           "Narrated by Kokoro. The End. Thank you for listening.")

CHECKS = [
    "Cover text read back character for character: title and subtitle "
    "exactly as above, no word shortened to fit, no comma before \"and\".",
    "Cover flattened to an RGB JPEG, 3000 x 3000 (ChatGPT exports carry an "
    "alpha channel).",
    "Title and subtitle pasted, not typed, into every store's fields. The "
    "subtitle is what makes this a philosophy book and tells it apart from "
    "The Subtle Art of Not Giving a F*ck and The Art of Diogenes of Sinope: "
    "never leave it out where a field takes one.",
    "Narrator field reads Kokoro (AI Voice); AI narration disclosed on every "
    "store.",
    "Price $4.99 on all three stores.",
    "Author's Republic: Google Play deselected as a channel (email them; it "
    "is not self-serve).",
    "Author's Republic: opening and closing credits and the 3:52 sample "
    "uploaded. Spotify: the 8:34 sample.",
    "Google Play: companion PDF attached.",
    "All 13 chapter files uploaded in order, titles as in the chapter table.",
    "Spot-listen: the first 30 seconds of the intro and the opening credits "
    "(the title and \"Diogenes\" are what a reviewer always hears).",
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
          P("Total 50:21. Every file 44.1 kHz, 192 kbps MP3, 1.5 seconds of "
            "silence at head and tail, peak -3.2 dB or lower."),
          P("Uploads per store", "h"),
          grid([[C("<b>File</b>"), C("<b>Google Play</b>"),
                 C("<b>Spotify</b>"), C("<b>Author's Republic</b>")]] +
               [[C(f, "mono"), C(a), C(b), C(c)] for f, a, b, c in UPLOADS],
               [86 * mm, 26 * mm, 22 * mm, 36 * mm]),
          P("All files are in ~/Desktop/audiobook-not-caring/."),
          P("Spoken credits", "h"),
          P(f"<b>Opening:</b> {OPENING}"),
          P(f"<b>Closing:</b> {CLOSING}"),
          PageBreak(),
          P("Before you press submit", "h")]
    s += [BOX(c) for c in CHECKS]
    s += [Spacer(1, 10),
          P("If a store rejects anything, note the exact wording of the "
            "rejection: the fix is usually one line in "
            "projects/diogenes/the-art-of-not-caring.py and a re-render of "
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
