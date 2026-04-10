#!/usr/bin/env python3
"""ForkFox — Restaurant Pitch One-Pager PDF Builder (FOR-12)"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

NAVY  = HexColor('#0A1A2F')
GOLD  = HexColor('#D4A534')
BLUE  = HexColor('#3A7CD5')
LIGHT = HexColor('#F7F9FC')
GRAY  = HexColor('#6B7280')
WHITE = white


def build():
    base   = os.path.dirname(__file__)
    output = os.path.join(base, "strategy", "forkfox-restaurant-pitch.pdf")

    doc = SimpleDocTemplate(
        output,
        pagesize=letter,
        leftMargin=0.55*inch,
        rightMargin=0.55*inch,
        topMargin=0.45*inch,
        bottomMargin=0.4*inch,
    )

    # ── Styles ─────────────────────────────────────────────────────────────
    logo_s   = ParagraphStyle('Logo',   fontSize=28, textColor=NAVY,  fontName='Helvetica-Bold', alignment=TA_LEFT,   spaceAfter=0)
    tag_s    = ParagraphStyle('Tag',    fontSize=10, textColor=GOLD,  fontName='Helvetica-Bold', alignment=TA_LEFT,   spaceAfter=0)
    hero_s   = ParagraphStyle('Hero',   fontSize=22, textColor=NAVY,  fontName='Helvetica-Bold', alignment=TA_CENTER, spaceBefore=12, spaceAfter=4, leading=26)
    sub_s    = ParagraphStyle('Sub',    fontSize=11, textColor=GRAY,  fontName='Helvetica',      alignment=TA_CENTER, spaceAfter=10)
    sec_s    = ParagraphStyle('Sec',    fontSize=12, textColor=NAVY,  fontName='Helvetica-Bold', spaceBefore=10,      spaceAfter=5)
    body_s   = ParagraphStyle('Body',   fontSize=10, textColor=NAVY,  fontName='Helvetica',      leading=14,          spaceAfter=3)
    bul_s    = ParagraphStyle('Bul',    fontSize=10, textColor=NAVY,  fontName='Helvetica',      leading=13,          spaceAfter=2, leftIndent=14)
    step_s   = ParagraphStyle('Step',   fontSize=10, textColor=NAVY,  fontName='Helvetica-Bold', leading=13,          spaceAfter=2)
    stepsub  = ParagraphStyle('StSub',  fontSize=9,  textColor=GRAY,  fontName='Helvetica',      leading=12,          spaceAfter=4, leftIndent=14)
    cta_s    = ParagraphStyle('CTA',    fontSize=12, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
    ctasub_s = ParagraphStyle('CtaSub', fontSize=9,  textColor=HexColor('#BDC3CD'), fontName='Helvetica', alignment=TA_CENTER)
    foot_s   = ParagraphStyle('Foot',   fontSize=8,  textColor=GRAY,  fontName='Helvetica',      alignment=TA_CENTER)

    elements = []

    # ── HEADER ROW (Logo + Tagline + Contact) ──────────────────────────────
    header_data = [[
        Paragraph('🦊 ForkFox', logo_s),
        Paragraph('Your best dishes get found first.', tag_s),
        Paragraph('<font color="#6B7280">forkfox.ai/restaurants</font>', ParagraphStyle('R', fontSize=9, fontName='Helvetica', alignment=TA_RIGHT, textColor=GRAY)),
    ]]
    header_tbl = Table(header_data, colWidths=[2.0*inch, 3.8*inch, 1.9*inch])
    header_tbl.setStyle(TableStyle([
        ('VALIGN',    (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',     (0,0), (0,0),  'LEFT'),
        ('ALIGN',     (1,0), (1,0),  'CENTER'),
        ('ALIGN',     (2,0), (2,0),  'RIGHT'),
    ]))
    elements.append(header_tbl)
    elements.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=8))

    # ── HERO ──────────────────────────────────────────────────────────────
    elements.append(Paragraph("AI that puts your <font color='#D4A534'>best dishes</font> in front of hungry customers first.", hero_s))
    elements.append(Paragraph("ForkFox scores every dish on your menu — flavor, texture, value, authenticity — and surfaces your top performers when people are ready to order.", sub_s))
    elements.append(HRFlowable(width="100%", thickness=1, color=HexColor('#E5E7EB'), spaceAfter=8))

    # ── THREE COLUMNS: Problem | Solution | Results ────────────────────────
    col_title = ParagraphStyle('CT', fontSize=11, textColor=NAVY, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=6)
    col_body  = ParagraphStyle('CB', fontSize=9,  textColor=NAVY, fontName='Helvetica',      leading=12, alignment=TA_LEFT, spaceAfter=3)
    col_bul   = ParagraphStyle('CBu',fontSize=9,  textColor=NAVY, fontName='Helvetica',      leading=12, leftIndent=10, spaceAfter=2)

    problem_content = [
        Paragraph("THE PROBLEM", col_title),
        Paragraph("• Yelp rates your <i>restaurant</i> — not your $28 lamb chop", col_bul),
        Paragraph("• Your best dishes are invisible to new customers", col_bul),
        Paragraph("• Great menus get buried under generic star ratings", col_bul),
    ]
    solution_content = [
        Paragraph("HOW IT WORKS", col_title),
        Paragraph("① Add your menu to ForkFox", col_bul),
        Paragraph("② AI scores each dish across 8 dimensions", col_bul),
        Paragraph("③ Your top dishes surface first in discovery", col_bul),
        Paragraph("④ Guests find you based on <i>what</i> you make", col_bul),
    ]
    results_content = [
        Paragraph("FOR RESTAURANTS", col_title),
        Paragraph("✓ <b>More discovery</b> — rank where it matters", col_bul),
        Paragraph("✓ <b>Better-fit guests</b> — they want what you make", col_bul),
        Paragraph("✓ <b>Dish analytics</b> — see which items drive returns", col_bul),
        Paragraph("✓ <b>Reduced waste</b> — data on what to promote", col_bul),
    ]

    three_col = Table(
        [[problem_content, solution_content, results_content]],
        colWidths=[2.45*inch, 2.45*inch, 2.45*inch],
    )
    three_col.setStyle(TableStyle([
        ('VALIGN',      (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND',  (0,0), (0,0),   HexColor('#FFF7EC')),
        ('BACKGROUND',  (1,0), (1,0),   HexColor('#EFF6FF')),
        ('BACKGROUND',  (2,0), (2,0),   HexColor('#F0FDF4')),
        ('BOX',         (0,0), (0,0),   1, HexColor('#FDE68A')),
        ('BOX',         (1,0), (1,0),   1, HexColor('#BFDBFE')),
        ('BOX',         (2,0), (2,0),   1, HexColor('#BBF7D0')),
        ('LEFTPADDING',  (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
    ]))
    elements.append(three_col)
    elements.append(Spacer(1, 0.12*inch))

    # ── PRICING TEASER ─────────────────────────────────────────────────────
    pricing_data = [[
        Paragraph("<b>Free Beta Access</b><br/><font size='8' color='#6B7280'>During beta, early partners get full access at no cost. Lock in lifetime preferred pricing before we launch.</font>", ParagraphStyle('P1', fontSize=10, textColor=NAVY, fontName='Helvetica', leading=13)),
        Paragraph("<b>Coming Soon</b><br/><font size='8' color='#6B7280'>Starter · Growth · Enterprise tiers based on menu size and analytics depth.</font>", ParagraphStyle('P2', fontSize=10, textColor=NAVY, fontName='Helvetica', leading=13)),
        Paragraph("<b>Early Partner Benefit</b><br/><font size='8' color='#6B7280'>Beta partners influence product roadmap and get priority support at launch.</font>", ParagraphStyle('P3', fontSize=10, textColor=NAVY, fontName='Helvetica', leading=13)),
    ]]
    pricing_tbl = Table(pricing_data, colWidths=[2.45*inch, 2.45*inch, 2.45*inch])
    pricing_tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), NAVY),
        ('TEXTCOLOR',    (0,0), (-1,-1), WHITE),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
        ('INNERGRID',    (0,0), (-1,-1), 0.5, HexColor('#1E3A5F')),
    ]))
    elements.append(pricing_tbl)
    elements.append(Spacer(1, 0.12*inch))

    # ── SOCIAL PROOF (placeholder) ─────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1, color=HexColor('#E5E7EB'), spaceAfter=8))
    elements.append(Paragraph(
        '"ForkFox surfaces the dishes we\'re most proud of — and brings in guests who actually order them."',
        ParagraphStyle('Q', fontSize=10, fontName='Helvetica-Oblique', textColor=GRAY, alignment=TA_CENTER, spaceAfter=2, leftIndent=40, rightIndent=40)
    ))
    elements.append(Paragraph(
        '— Beta Partner, Philadelphia Independent Restaurant',
        ParagraphStyle('QA', fontSize=8, fontName='Helvetica', textColor=GRAY, alignment=TA_CENTER, spaceAfter=8)
    ))
    elements.append(HRFlowable(width="100%", thickness=1, color=HexColor('#E5E7EB'), spaceAfter=8))

    # ── CTA BANNER ─────────────────────────────────────────────────────────
    cta_data = [[
        Paragraph("Join the Beta — Free for Early Partners", cta_s),
        Paragraph("Claim your spot before we open to the public →  forkfox.ai/restaurants", ctasub_s),
    ]]
    cta_tbl = Table([[
        [Paragraph("Join the Beta — Free for Early Partners", cta_s),
         Paragraph("forkfox.ai/restaurants  |  Spots are limited", ctasub_s)]
    ]], colWidths=[7.4*inch])
    cta_tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), BLUE),
        ('LEFTPADDING',  (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
    ]))
    elements.append(cta_tbl)
    elements.append(Spacer(1, 0.1*inch))

    # ── FOOTER ─────────────────────────────────────────────────────────────
    foot_data = [[
        Paragraph('🦊 ForkFox  |  Rate the dish, not the restaurant', foot_s),
        Paragraph('forkfox.ai/restaurants  |  Ali Mabsoute, Founder', ParagraphStyle('FR', fontSize=8, textColor=GRAY, fontName='Helvetica', alignment=TA_RIGHT)),
    ]]
    foot_tbl = Table(foot_data, colWidths=[3.7*inch, 3.7*inch])
    foot_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(foot_tbl)

    doc.build(elements)
    print(f"Built: {output}")


if __name__ == "__main__":
    build()
