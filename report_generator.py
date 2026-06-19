"""
PDF Report Generator - Creates a formatted PDF report with ATS score and tips
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from datetime import datetime


# Colors
NAVY = HexColor("#1E3A8A")
DARK_NAVY = HexColor("#0F172A")
LIGHT_BG = HexColor("#F1F5F9")
GREEN = HexColor("#22C55E")
ORANGE = HexColor("#F59E0B")
RED = HexColor("#EF4444")
GRAY = HexColor("#64748B")
LIGHT_GRAY = HexColor("#E2E8F0")


def get_score_color(score):
    if score >= 80:
        return GREEN
    elif score >= 55:
        return ORANGE
    else:
        return RED


def draw_rounded_rect(c, x, y, w, h, radius, fill_color):
    """Draw a rounded rectangle."""
    c.setFillColor(fill_color)
    c.setStrokeColor(fill_color)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)


def draw_progress_bar(c, x, y, width, height, score, max_score, color):
    """Draw a horizontal progress bar."""
    # Background
    draw_rounded_rect(c, x, y, width, height, height / 2, LIGHT_GRAY)
    # Fill
    fill_width = (score / max_score) * width if max_score > 0 else 0
    if fill_width > 0:
        draw_rounded_rect(c, x, y, fill_width, height, height / 2, color)


def draw_radial_gauge(c, cx, cy, radius, score, color):
    """Draw a radial/circular gauge."""
    import math

    # Background circle
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(12)
    c.circle(cx, cy, radius, fill=0, stroke=1)

    # Score arc
    c.setStrokeColor(color)
    c.setLineWidth(12)
    start_angle = 90
    end_angle = 90 - (score / 100) * 360

    # Draw arc using small line segments
    steps = 100
    angle_range = (score / 100) * 360
    for i in range(steps):
        a1 = math.radians(90 - (i / steps) * angle_range)
        a2 = math.radians(90 - ((i + 1) / steps) * angle_range)
        x1 = cx + radius * math.cos(a1)
        y1 = cy + radius * math.sin(a1)
        x2 = cx + radius * math.cos(a2)
        y2 = cy + radius * math.sin(a2)
        c.line(x1, y1, x2, y2)


def generate_report(results: dict, filename: str = "ATS_Report.pdf") -> bytes:
    """
    Generate a PDF report and return bytes.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ─── Header ───────────────────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, height - 80, width, 80, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30, height - 45, "YALLA BANKING ATS SCORE")

    c.setFont("Helvetica", 11)
    c.drawString(30, height - 65, "ATS Compatibility Report")

    # Date
    c.setFont("Helvetica", 9)
    c.drawRightString(
        width - 30,
        height - 65,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    )

    # ─── Score Section ────────────────────────────────────────────────────
    y_pos = height - 180
    score_color = get_score_color(results["total_score"])

    # Score circle
    draw_radial_gauge(c, 100, y_pos + 30, 45, results["total_score"], score_color)

    # Score text in center
    c.setFillColor(score_color)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(100, y_pos + 22, str(results["total_score"]))
    c.setFont("Helvetica", 10)
    c.drawCentredString(100, y_pos + 8, "/ 100")

    # Level text
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, y_pos + 45, f"Score: {results['level']}")

    c.setFont("Helvetica", 11)
    c.setFillColor(GRAY)
    c.drawString(
        180,
        y_pos + 25,
        f"Word Count: {results['word_count']} | Pages: {results['page_count']}",
    )

    # ─── Breakdown Section ────────────────────────────────────────────────
    y_pos = height - 270

    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y_pos, "Score Breakdown")

    y_pos -= 10

    # Draw line
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(1)
    c.line(30, y_pos, width - 30, y_pos)

    breakdown = results["breakdown"]
    items = [
        (
            "Readability",
            breakdown["readability"]["score"],
            breakdown["readability"]["max"],
        ),
        ("Sections", breakdown["sections"]["score"], breakdown["sections"]["max"]),
        (
            "Keywords & Skills",
            breakdown["keywords"]["score"],
            breakdown["keywords"]["max"],
        ),
        ("Contact Info", breakdown["contact"]["score"], breakdown["contact"]["max"]),
    ]

    for label, score, max_s in items:
        y_pos -= 35
        c.setFillColor(DARK_NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y_pos + 5, label)

        c.setFont("Helvetica", 10)
        c.drawRightString(width - 30, y_pos + 5, f"{score}/{max_s}")

        # Progress bar
        bar_color = get_score_color((score / max_s) * 100) if max_s > 0 else GRAY
        draw_progress_bar(c, 30, y_pos - 10, width - 60, 8, score, max_s, bar_color)

    # ─── Tips Section ─────────────────────────────────────────────────────
    y_pos -= 50

    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y_pos, "Recommendations")

    y_pos -= 10
    c.line(30, y_pos, width - 30, y_pos)

    all_tips = results["all_tips"]

    if not all_tips:
        y_pos -= 25
        c.setFillColor(GREEN)
        c.setFont("Helvetica", 11)
        c.drawString(30, y_pos, "Excellent! Your CV passes most ATS checks.")
    else:
        for category, tip in all_tips:
            y_pos -= 25

            # Check if we need a new page
            if y_pos < 60:
                c.showPage()
                y_pos = height - 50
                c.setFillColor(DARK_NAVY)
                c.setFont("Helvetica-Bold", 14)
                c.drawString(30, y_pos, "Recommendations (continued)")
                y_pos -= 10
                c.line(30, y_pos, width - 30, y_pos)
                y_pos -= 25

            # Category badge
            badge_width = len(category) * 6 + 12
            draw_rounded_rect(c, 30, y_pos - 2, badge_width, 14, 3, NAVY)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(36, y_pos + 1, category)

            # Tip text - use Frame for wrapping
            c.setFillColor(DARK_NAVY)
            c.setFont("Helvetica", 9)
            tip_x = 30 + badge_width + 8
            available_width = width - tip_x - 30

            # Simple text wrapping
            words = tip.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if c.stringWidth(test_line, "Helvetica", 9) < available_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            for i, line in enumerate(lines):
                c.drawString(tip_x, y_pos + 1 - (i * 12), line)

            if len(lines) > 1:
                y_pos -= (len(lines) - 1) * 12

    # ─── Keyword Analysis (if JD was provided) ────────────────────────────
    kw_analysis = breakdown["keywords"].get("analysis", {})
    if kw_analysis.get("jd_match_percentage", 0) > 0:
        y_pos -= 40
        if y_pos < 120:
            c.showPage()
            y_pos = height - 50

        c.setFillColor(DARK_NAVY)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y_pos, "Keyword Match Analysis")
        y_pos -= 10
        c.line(30, y_pos, width - 30, y_pos)

        y_pos -= 25
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 10)
        c.drawString(
            30, y_pos, f"Job Description Match: {kw_analysis['jd_match_percentage']}%"
        )

        matched = kw_analysis.get("jd_matched_keywords", [])
        if matched:
            y_pos -= 20
            c.setFillColor(GREEN)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(30, y_pos, "Matched Keywords:")
            c.setFillColor(DARK_NAVY)
            c.setFont("Helvetica", 9)
            kw_text = ", ".join(matched[:15])
            y_pos -= 15
            c.drawString(30, y_pos, kw_text[:120])

        missing = kw_analysis.get("jd_missing_keywords", [])
        if missing:
            y_pos -= 20
            c.setFillColor(RED)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(30, y_pos, "Missing Keywords to Add:")
            c.setFillColor(DARK_NAVY)
            c.setFont("Helvetica", 9)
            kw_text = ", ".join(missing[:15])
            y_pos -= 15
            c.drawString(30, y_pos, kw_text[:120])

    # ─── Footer ───────────────────────────────────────────────────────────
    c.setFillColor(LIGHT_GRAY)
    c.rect(0, 0, width, 30, fill=1, stroke=0)
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(
        width / 2, 12, "YALLA BANKING ATS SCORE | Powered by Advanced ATS Analysis"
    )

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
