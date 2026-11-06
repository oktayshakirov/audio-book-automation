#!/usr/bin/env python3
"""The upload sheet: everything the author types or uploads, on paper.

    python projects/ai-content/metadata_pdf.py

Metadata, description, keywords, chapter titles and lengths, the per-store
upload table, the spoken credit text, and a pre-submit checklist. The same
values as projects/ai-content/README.md; if one changes, change both.
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
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-ai-slop"))
PDF = OUT / "Stop-Making-AI-Slop-metadata.pdf"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")
ACCENT = HexColor("#C8402E")

TITLE = "Stop Making AI Slop"
SUBTITLE = ("Why Most AI Videos Die in Seven Seconds, "
            "and How to Make Ones People Actually Watch")
AUTHOR = "Oktay Shakirov"
SLUG = "Stop-Making-AI-Slop"

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
    ("Category", "BUSINESS & ECONOMICS / E-Commerce / Internet Marketing "
                 "(BUS090010)"),
    ("Second category", "COMPUTERS / Artificial Intelligence / General "
                        "(COM004000)"),
    ("Price", "$4.99 on every store (Google enforces price parity)"),
    ("Runtime", "62:49, 14 tracks"),
    ("Copyright", "© 2026 Oktay Shakirov"),
    ("AI narration", "Yes. Disclose on every store."),
]

DESCRIPTION = [
    "In twenty twenty five, Merriam-Webster's word of the year was slop: low "
    "quality content, made in quantity, by AI. You have scrolled past "
    "thousands of these videos. Maybe you have made some.",
    "Stop Making AI Slop is a one-hour, no-nonsense guide for creators who use "
    "AI to make YouTube, Shorts, TikTok and Reels videos, and want people to "
    "actually watch them. It opens with Demand Media, the content farm that "
    "let software pick its topics, published thousands of pieces a day and "
    "was valued at more than a billion dollars, until one Google update. AI "
    "content is the same business with the writers taken out, and the same "
    "thing is happening again.",
    "You will learn why a video is usually lost before its second sentence "
    "ends, how YouTube decides who sees your upload, why no platform has "
    "banned AI content but every one is penalising the template, and the four "
    "mistakes that give an AI video away: the topic nobody searches for, the "
    "robotic voice, the picture that says something else, and the template "
    "that shows.",
    "Then the practice: ten checks to run on every video, and a thirty day "
    "plan to rebuild your channel around them.",
    "No earnings promises. No secret prompt. Just how to use the same tools "
    "as everyone else and make something people choose to watch.",
    "Narrated by Kokoro, an AI voice.",
]

KEYWORDS = ("ai slop, ai content creation, faceless youtube channel, youtube "
            "automation, youtube shorts, ai video, youtube algorithm, audience "
            "retention, ai voiceover, content creator, tiktok, inauthentic "
            "content")

CHAPTERS = [
    ("01-intro", "Introduction: AI Can Make Anything. It Cannot Make Anyone "
                 "Watch.", "3:34"),
    ("02-ch01", "Chapter 1: The Billion Dollar Content Farm", "4:55"),
    ("03-ch02", "Chapter 2: Everyone Has the Same Machine Now", "5:17"),
    ("04-ch03", "Chapter 3: You Have Seven Seconds, and Sentence Two Spends "
                "Them", "5:03"),
    ("05-ch04", "Chapter 4: The Algorithm Is Not Counting Your Uploads",
     "5:38"),
    ("06-ch05", "Chapter 5: The Rules Changed While You Were Uploading",
     "5:47"),
    ("07-ch06", "Chapter 6: You Picked a Topic Nobody Is Looking For", "3:32"),
    ("08-ch07", "Chapter 7: Your Voice Sounds Robotic Because You Slowed It "
                "Down", "3:37"),
    ("09-ch08", "Chapter 8: The Picture Is Saying Something Else", "3:26"),
    ("10-ch09", "Chapter 9: Your Template Is the Tell", "3:12"),
    ("11-ch10", "Chapter 10: You Are Not a Factory. You Are the Editor.",
     "2:55"),
    ("12-ch11", "Chapter 11: Build a Pipeline That Does Not Make Slop",
     "7:25"),
    ("13-ch12", "Chapter 12: The Thirty Day Channel Reset", "5:17"),
    ("14-outro", "Conclusion: Make the Video You Would Actually Watch",
     "3:02"),
]

UPLOADS = [
    ("01-intro.mp3 ... 14-outro.mp3", "yes", "yes", "yes"),
    (f"{SLUG}-sample-spotify.mp3 (8:32)", "-", "yes", "-"),
    (f"{SLUG}-sample-ar.mp3 (3:34)", "-", "-", "yes"),
    (f"{SLUG}-opening-credits.mp3 (0:13)", "-", "-", "yes"),
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
    "Title and subtitle pasted, not typed, into every store's fields.",
    "Narrator field reads Kokoro (AI Voice); AI narration disclosed on every "
    "store.",
    "Price $4.99 on all three stores.",
    "Author's Republic: Google Play deselected as a channel (email them; it "
    "is not self-serve).",
    "Author's Republic: opening and closing credits and the 3:34 sample "
    "uploaded. Spotify: the 8:32 sample.",
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
          P("Total 62:49. Every file 44.1 kHz, 192 kbps MP3, 1.5 seconds of "
            "silence at head and tail, peak -3.2 dB or lower."),
          P("Uploads per store", "h"),
          grid([[C("<b>File</b>"), C("<b>Google Play</b>"),
                 C("<b>Spotify</b>"), C("<b>Author's Republic</b>")]] +
               [[C(f, "mono"), C(a), C(b), C(c)] for f, a, b, c in UPLOADS],
               [86 * mm, 26 * mm, 22 * mm, 36 * mm]),
          P("All files are in ~/Desktop/audiobook-ai-slop/."),
          P("Spoken credits", "h"),
          P(f"<b>Opening:</b> {OPENING}"),
          P(f"<b>Closing:</b> {CLOSING}"),
          PageBreak(),
          P("Before you press submit", "h")]
    s += [BOX(c) for c in CHECKS]
    s += [Spacer(1, 10),
          P("If a store rejects anything, note the exact wording of the "
            "rejection: the fix is usually one line in "
            "projects/ai-content/stop-making-ai-slop.py and a re-render of "
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
