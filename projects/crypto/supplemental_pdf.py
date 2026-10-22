#!/usr/bin/env python3
"""The supplemental PDF that ships beside the audiobook.

    python projects/crypto/supplemental_pdf.py

Six pages: the five exits, the vault, the thirty day reset, a rules sheet to
fill in, the letter for your family, and the sources. Written out rather than
generated from the manuscript, because a listener wants a working document,
not a transcript.

**Unlike the tinnitus companion, this one has boxes to tick.** That book
argued against monitoring, so a checklist would have taught the habit it
dismantles. This book's practice is a set of one-off jobs - buy the device,
test the backup, write the rules - and a checklist is the point. Nothing here
is ongoing tracking, and nothing invites checking the price.

Every number matches the audiobook and its audit in `book/SOURCES.md`.

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
    "AUDIOBOOK_OUT", Path.home() / "Desktop" / "audiobook-crypto"))
PDF = OUT / "Stop-Losing-Money-in-Crypto-companion.pdf"

INK = HexColor("#111114")
MUTED = HexColor("#5A5A62")
RULE = HexColor("#CFCFD6")
GOLD = HexColor("#B8892B")      # the cover's one accent colour

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
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(20 * mm, A4[1] - 12 * mm, A4[0] - 20 * mm, A4[1] - 12 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "Stop Losing Money in Crypto")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "thecrypto.wiki")
    canvas.restoreState()


def story():
    s = []

    # --- 1: the five exits ---------------------------------------------
    s += [P("Stop Losing Money in Crypto", "title"),
          P("The scams, collapses, leverage and lost keys that take it, and "
            "how to keep yours.", "sub"),
          rule(),
          P("This is the working companion to the audiobook: the vault, the "
            "thirty day reset, a sheet for your own rules, and a letter for "
            "your family. Print it. Tick the boxes once. Then put it away.",
            "lead"),
          P("Not financial advice. Nothing here tells you what to buy, when, "
            "or how much.", "note"),
          P("The argument in one page", "h"),
          P("The price can hurt you, but a price drop on a coin you still "
            "hold is a bad day, not the end of the story. The losses that end "
            "the story are total, permanent, and mostly preventable. They "
            "leave through five doors."),
          LI("<b>Scams.</b> Americans reported more than eleven billion "
             "dollars of crypto-related fraud losses to the FBI in 2025. "
             "Crypto investment scams alone were 7.2 billion, the largest "
             "category in the report."),
          LI("<b>Collapses.</b> A balance on an exchange is a promise, not a "
             "coin. QuadrigaCX, Mt. Gox, FTX and Celsius all held customers' "
             "crypto, and all failed them."),
          LI("<b>Leverage.</b> At 10x, a 10 percent move wipes you out. At "
             "100x, 1 percent. On 10 October 2025, more than 19 billion "
             "dollars of positions were liquidated in about a day."),
          LI("<b>Panic.</b> People arrive after prices rise and sell after "
             "they fall. A majority of crypto app users studied by the BIS "
             "from 2015 to 2022 lost money on their bitcoin."),
          LI("<b>Lost keys.</b> Your recovery phrase is your money. Lose your "
             "only copy, or let anyone else see it, and it is gone."),
          P("The one question", "h"),
          P("Before any crypto transaction, for the rest of your life: "
            "<b>did I find this, or did it find me?</b> If it found you, stop. "
            "Open the official app yourself. Real problems survive a ten "
            "minute pause. Scams do not.", "lead"),
          P("Nobody can reverse a blockchain transaction for a fee. Anyone "
            "who says they can is the second scam.", "lead"),
          PageBreak()]

    # --- 2: build your vault -------------------------------------------
    s += [P("Build your vault", "title"),
          P("Chapter eleven, as a checklist. Do it once, with a small amount "
            "first. An afternoon, maybe two.", "sub"),
          rule(),
          P("1. Split what you spend from what you keep", "h2"),
          BOX("Write down the amount that stays on an exchange or phone app "
              "for spending and trading. Everything else goes in the vault."),
          P("2. Get a hardware wallet", "h2"),
          BOX("Bought from the maker's own website, or a reseller the maker "
              "lists. Not a marketplace, not second hand."),
          BOX("Packaging checked. <b>No recovery phrase in the box, and the "
              "device is not already set up.</b> If either is true, do not "
              "use it."),
          P("3. Get the software from the right place", "h2"),
          BOX("Maker's web address typed by hand and bookmarked. Never "
              "installed from a search result or an advert."),
          P("4. Create and protect your words", "h2"),
          BOX("Recovery phrase written on paper, in order, numbered, and "
              "checked word by word on the device."),
          BOX("Copied onto a backup that survives fire and water, such as a "
              "stamped or engraved steel plate."),
          BOX("Two copies, in two different places. Neither labelled crypto."),
          BOX("No photo, screenshot, cloud note, email or password manager "
              "holds the words. They are typed only into the device itself."),
          P("5. Prove you can recover", "h2"),
          BOX("While the wallet is still empty: reset the device and restore "
              "it from your written words. Same wallet, same receiving "
              "address."),
          P("6. Move your coins, with a test", "h2"),
          BOX("Receiving address shown on the device screen and compared "
              "with the exchange, <b>every character</b>, not just the start "
              "and end."),
          BOX("Correct network chosen. Small test sent, arrived, then the "
              "rest."),
          P("7. Lock the door you still use", "h2"),
          BOX("Unique long password on every exchange you keep."),
          BOX("Two factor from an authenticator app or security key. Text "
              "message codes removed."),
          BOX("Withdrawal address allowlist switched on, if offered."),
          BOX("Holdings no longer mentioned on social media."),
          P("8. Write the letter", "h2"),
          BOX("Letter written (page five) and kept with your will, apart from "
              "the backups."),
          PageBreak()]

    # --- 3: the thirty day reset ---------------------------------------
    s += [P("The thirty day reset", "title"),
          P("Chapter twelve. One job a week. By day thirty, every exit has "
            "something standing in front of it.", "sub"),
          rule(),
          P("Week one: find everything", "h2"),
          BOX("Day 1. List every exchange, app and wallet you have ever "
              "used, including the forgotten ones."),
          BOX("Day 2. Hunt for your recovery phrase in your camera roll, "
              "screenshots, notes, cloud storage and email. Move it to paper. "
              "Delete every digital copy, including recently deleted and "
              "cloud backups."),
          BOX("Day 3. New password and authenticator two factor on every "
              "exchange you keep. Phone number removed as a login or "
              "recovery method where possible."),
          BOX("Days 4 to 7. Close accounts you do not use. For any platform "
              "paying interest on your crypto, read the terms: once you put "
              "it in, who owns it?"),
          P("Week two: build the vault", "h2"),
          BOX("Day 8. Order the hardware wallet from the maker's site."),
          BOX("When it arrives: page two, steps 4 to 6. Recovery test before "
              "any real coin goes in."),
          P("Week three: write your rules", "h2"),
          BOX("Fill in page four. Sign and date it."),
          BOX("Unfollow every account that tells you what to buy without "
              "saying what it is paid."),
          P("Week four: make it quiet", "h2"),
          BOX("All price alerts off."),
          BOX("One fixed time a week to look, and close the app when you "
              "are done."),
          BOX("Letter written and stored (page five)."),
          BOX("One trusted person told that you have a system, and that you "
              "will call them before acting on any message about your "
              "crypto."),
          BOX("Day 30. Read your rules out loud. Once."),
          PageBreak()]

    # --- 4: my crypto rules ---------------------------------------------
    s += [P("My crypto rules", "title"),
          P("Written on a calm day, for the loud ones. Your answers, in your "
            "words. When the market screams, you do not have to be brave or "
            "clever. You only have to read this.", "sub"),
          rule(),
          P("The most I will ever put into crypto, in total:", "q"),
          P("An amount I could watch fall by three quarters and still sleep. "
            "It has happened before, more than once.", "note"),
          write_lines(1),
          P("How I will buy:", "q"),
          P("All at once, or the same amount on the same day each month, "
            "whatever the news says.", "note"),
          write_lines(2),
          P("What would make me sell:", "q"),
          P("Decided now, so I am not inventing a reason at three in the "
            "morning in the middle of a crash.", "note"),
          write_lines(2),
          P("My memecoin lottery budget (never topped up):", "q"),
          write_lines(1),
          P("The short rules", "h"),
          LI("No leverage. Not a little, not once."),
          LI("Anything that finds me waits forty eight hours before I do "
             "anything at all."),
          LI("I never type my recovery phrase anywhere but the hardware "
             "wallet, and nobody real will ever ask for it."),
          LI("I check every character of an address, and I send a test "
             "first."),
          LI("Anyone offering to recover lost crypto for a fee is a scam."),
          Spacer(1, 14),
          Table([["Signed", "", "Date", ""]],
                colWidths=[16 * mm, 78 * mm, 14 * mm, 58 * mm], hAlign="LEFT",
                style=TableStyle([
                    ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, RULE),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, RULE)])),
          PageBreak()]

    # --- 5: the letter --------------------------------------------------
    s += [P("The letter", "title"),
          P("For the people who would need to find your crypto if you could "
            "not tell them. Quadriga's customers learned what happens when "
            "one person holds everything.", "sub"),
          rule(),
          P("<b>Never write your recovery phrase in this letter.</b> The "
            "letter says where to look. The backup is the key. Keep the two "
            "apart, keep the letter with your will, and talk to whoever "
            "handles your will about how they would reach the rest.", "lead"),
          P("What I own", "q"),
          P("Which coins, roughly. No need for exact amounts.", "note"),
          write_lines(2),
          P("Where it is held", "q"),
          P("Which hardware wallet, and where the device is kept.", "note"),
          write_lines(2),
          P("Where the backups are", "q"),
          P("The two places the recovery phrase copies are stored.", "note"),
          write_lines(2),
          P("Exchanges and apps I use", "q"),
          write_lines(2),
          P("Who you can trust to help", "q"),
          write_lines(1),
          P("Who you should never trust", "q"),
          P("Anyone who contacts you offering to recover or unlock my crypto. "
            "Anyone who asks for the recovery phrase. Real help never "
            "contacts you first.", "lead"),
          PageBreak()]

    # --- 6: sources -----------------------------------------------------
    s += [P("Sources", "title"),
          P("The main sources behind the audiobook. Every figure was checked "
            "against these before narration.", "sub"),
          rule()]
    refs = [
        ("Fraud and scams",
         ["FBI Internet Crime Complaint Center. 2025 Internet Crime Report, "
          "April 2026. Crypto-related losses of $11.37 billion across "
          "181,565 complaints; crypto investment fraud $7.2 billion.",
          "FBI IC3 public service announcements: scammers impersonating "
          "cryptocurrency exchanges (August 2024); fictitious law firms "
          "targeting crypto scam victims (June 2024); search engine adverts "
          "impersonating brands (December 2022); SIM swapping (February "
          "2022).",
          "Federal Trade Commission. Top text scams of 2024, Data Spotlight, "
          "April 2025.",
          "UN Office of the High Commissioner for Human Rights. Online scam "
          "operations and trafficking into forced criminality in Southeast "
          "Asia, August 2023."]),
        ("Collapses",
         ["Ontario Securities Commission staff. QuadrigaCX: A Review by "
          "Staff of the Ontario Securities Commission, June 2020.",
          "United States v. Bankman-Fried, S.D.N.Y. Verdict November 2023, "
          "sentence March 2024.",
          "In re Celsius Network LLC, Bankr. S.D.N.Y. Memorandum opinion on "
          "Earn account ownership, 4 January 2023."]),
        ("Keys and wallets",
         ["Bitcoin Improvement Proposal 39 (BIP39): mnemonic code for "
          "generating deterministic keys, 2013.",
          "Nakamoto S. Bitcoin: A Peer-to-Peer Electronic Cash System, 2008.",
          "Kaspersky. SparkCat: malware in App Store and Google Play apps "
          "scanning photo galleries for recovery phrases, February 2025."]),
        ("Markets, leverage and memecoins",
         ["Bank for International Settlements. Crypto shocks and retail "
          "losses, BIS Bulletin No 69, February 2023; and Auer et al., "
          "Crypto trading and Bitcoin prices, BIS Working Paper No 1049, "
          "2022.",
          "CoinGlass liquidation data, 10 to 11 October 2025.",
          "UK Financial Conduct Authority. Ban on the sale of crypto "
          "derivatives to retail consumers, effective January 2021.",
          "European Securities and Markets Authority. Product intervention "
          "on CFDs, March 2018: 74 to 89 percent of retail accounts lose "
          "money.",
          "Solidus Labs. The 2025 Rug Pull Report.",
          "US Securities and Exchange Commission: actions against Kim "
          "Kardashian (2022), Floyd Mayweather and DJ Khaled (2018), and "
          "Justin Sun and eight celebrities (2023) for undisclosed paid "
          "crypto promotion."]),
    ]
    for heading, items in refs:
        s.append(P(heading, "h2"))
        for it in items:
            s.append(Paragraph(it, S["ref"]))
    s += [rule(),
          P("Narration is synthetic. More free guides at thecrypto.wiki. "
            "Nothing in this audiobook or document is financial advice.",
            "note")]
    return s


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=20 * mm,
        title="Stop Losing Money in Crypto - companion",
        author="Oktay Shakirov",
        subject="Companion to the audiobook Stop Losing Money in Crypto")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="body")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=page_furniture)])
    doc.build(story())
    print(f"{PDF}  ({PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
