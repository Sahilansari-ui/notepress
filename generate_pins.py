import os
import html
import textwrap
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://sahilansari-ui.github.io/notepress"

PINS = [
    ("pw-black-pdf-to-white-printable", "PW Black PDF to White Printable in 1 Click", "PW CLASS NOTES", "471 Slides -> 50 Readable Pages • Save Rs.800+"),
    ("allen-digital-board-notes-printable", "Print Allen Digital Board Notes at 80% Less Cost", "ALLEN NOTES", "Zero Black Boxes • Big Pen-Friendly Text"),
    ("unacademy-dark-slides-to-white-pdf", "Convert Unacademy Dark Slides to Crisp White PDF", "UNACADEMY PDF", "Dark Maroon & Black -> Pure White Book"),
    ("neet-2027-physics-oneshot-printable", "NEET 2027 Physics One-Shot Notes Compact Book", "NEET PHYSICS", "Keep Derivations & Graphs Big & Clear"),
    ("neet-biology-class-slides-printable", "Print NEET Biology NCERT Slides Without Black Box", "NEET BIOLOGY", "Embedded White Diagram Cards Stay Clean"),
    ("neet-chemistry-notes-black-to-white", "Make NEET Chemistry Reactions Dark Jet-Black", "NEET CHEMISTRY", "Highlighter-Safe Bold Ink for Revision"),
    ("jee-mains-physics-notes-printable", "JEE Mains Physics Notes to Printable A4 Book", "JEE PHYSICS", "Anti-Tiny Handwriting Auto Full-Width"),
    ("jee-advanced-maths-board-notes", "Print JEE Maths Board Solutions Clearly on A4", "JEE MATHS", "Squish Blank Gaps Without Shrinking Text"),
    ("jee-chemistry-slides-to-white-book", "JEE Chemistry Dark Slides to White Study Notes", "JEE CHEMISTRY", "Crisp Organic Flowcharts & Equations"),
    ("ssc-cgl-maths-dark-notes-printable", "SSC CGL Maths Dark Board PDF to White Printable", "SSC CGL PREP", "Save 75% Print Money + Add Pen Margin"),
    ("ssc-chsl-gd-coaching-pdf-converter", "SSC CHSL & GD Coaching PDF Low-Cost Print Hack", "SSC EXAMS", "Works 100% Free Inside Phone Chrome"),
    ("upsc-coaching-slides-printable-pdf", "UPSC Dark Coaching PPTs to Printable A4 Notes", "UPSC CSE", "Add Lined Cornell Side Margin Automatically"),
    ("gate-engineering-notes-black-to-white", "GATE Circuit & Board Notes Black to White PDF", "GATE EXAM", "Razor-Sharp B&W Diagrams & Formulas"),
    ("class-12-cbse-board-notes-printable", "Class 12 CBSE YouTube One-Shot PDF to Book", "CLASS 12 BOARDS", "Zero Watermark • Zero Login • 100% Free"),
    ("class-11-science-notes-invert-pdf", "Invert Class 11 Science PDF Without Black Box", "CLASS 11 NOTES", "Smart White-Card Protection Engine"),
    ("invert-pdf-without-black-box", "Stop Turning White Cards Black While Inverting PDF", "STUDY HACK", "Fix Normal PDF Inverter Mistakes Free"),
    ("reduce-500-page-pdf-to-50-pages", "500 Page One-Shot PDF into 50 Readable Pages", "MONEY SAVER", "Rs.900 Printout Now Costs Only Rs.90"),
    ("remove-blank-space-inside-pdf-slides", "Auto-Remove Empty Space Inside Lecture Slides", "GAP SQUISHER", "Fewer A4 Pages With 2x Larger Letters"),
    ("make-handwriting-dark-bold-pdf-print", "Fix Faint Grey Stylus Handwriting in PDF Prints", "INK BOLDENER", "Thick Jet-Black Print • Highlighter Safe"),
    ("add-cornell-margin-to-pdf-notes", "Add Pen-Writing Side Margin to Any Coaching PDF", "CORNELL NOTES", "Write Your Own Tricks Beside Printouts"),
    ("skip-duplicate-pyq-slides-in-pdf", "Auto-Skip Repeated PYQ & Blank Coaching Slides", "DUPLICATE CLEANER", "Stop Paying to Print Half-Empty Slides"),
    ("maroon-blue-slides-to-white-pdf", "Clean Dark Maroon & Blue Class Slides to White", "BOARD CLEANER", "No Grey Patches • Pure White Background"),
    ("smart-book-vs-6-in-1-pdf-layout", "Why 6-in-1 PDF Grids Ruin Your Eyes (Better Way)", "SMART LAYOUT", "Wide Boards Get Full Width Automatically"),
    ("free-alternative-digital-to-printable", "Free Online Alternative to Digital to Printable App", "WEB TOOL", "No App Download • Bigger Clearer Font"),
    ("railway-rrb-ntpc-notes-printable", "Railway RRB NTPC Dark Class PDF to Printable Book", "RAILWAY RRB", "Convert 400+ Slides in 60 Seconds Free"),
    ("banking-ibps-sbi-notes-pdf-converter", "Banking IBPS & SBI Dark DI Graphs to White PDF", "BANKING EXAMS", "100% Private • Zero Server File Upload"),
    ("ca-foundation-inter-slides-printable", "CA Foundation & Inter Dark Slides Low-Cost Print", "CA EXAMS", "Cut Coaching Printout Bills by 80%"),
    ("cuet-ug-coaching-notes-black-to-white", "CUET UG 2027 Coaching Notes Black to White Tool", "CUET UG", "Instant A4 Preview Before You Print"),
    ("nda-cds-defence-notes-printable-pdf", "NDA & CDS Defence Dark Slides to Revision Book", "NDA / CDS", "Bold Jet-Black Ink • Zero Ink Waste"),
    ("state-pcs-police-exam-notes-printable", "State PCS & Police Exam Notes Compact PDF Maker", "STATE EXAMS", "Print Entire Chapters Under Rs.80")
]

THEMES = [
    ("#0f172a", "#4f46e5", "#818cf8", "#1e1b4b"),
    ("#090d16", "#059669", "#34d399", "#064e3b"),
    ("#130d1f", "#7c3aed", "#a78bfa", "#2e1065"),
    ("#0c1424", "#0284c7", "#38bdf8", "#0c4a6e"),
    ("#17100c", "#d97706", "#fbbf24", "#451a03"),
]

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)

os.makedirs("pins", exist_ok=True)
font_badge = load_font(30, bold=True)
font_title = load_font(66, bold=True)
font_stat = load_font(34, bold=True)
font_bullet = load_font(35, bold=False)
font_cta = load_font(36, bold=True)
font_url = load_font(28, bold=False)

now = datetime.now(timezone.utc)
rss_items = []

for idx, (slug, headline, badge, stat_line) in enumerate(PINS):
    bg_col, accent_col, light_col, box_col = THEMES[idx % len(THEMES)]
    img = Image.new("RGB", (1000, 1500), bg_col)
    draw = ImageDraw.Draw(img)

    # Outer clean frame
    draw.rounded_rectangle([32, 32, 968, 1468], radius=36, outline=accent_col, width=4)

    # Top brand + badge pill
    draw.rounded_rectangle([72, 82, 560, 152], radius=35, fill=box_col, outline=accent_col, width=2)
    draw.text((105, 100), badge, fill=light_col, font=font_badge)
    draw.text((665, 100), "NotePress Pro", fill="#94a3b8", font=font_badge)

    # Big wrapped headline
    lines = textwrap.wrap(headline, width=19)[:4]
    y = 215
    for line in lines:
        draw.text((75, y), line, fill="#ffffff", font=font_title)
        y += 86

    # Highlight stat card
    stat_y = max(610, y + 45)
    draw.rounded_rectangle([72, stat_y, 928, stat_y + 150], radius=24, fill=box_col, outline=light_col, width=3)
    stat_lines = textwrap.wrap(stat_line, width=34)[:2]
    sy = stat_y + (52 if len(stat_lines) == 1 else 28)
    for sl in stat_lines:
        draw.text((105, sy), sl, fill=light_col, font=font_stat)
        sy += 50

    # 3 crisp benefit bullets
    bullets = [
        "✓  Zero Black Boxes on White Cards",
        "✓  Big Pen-Friendly Jet-Black Font",
        "✓  100% Free • Runs in Phone Browser"
    ]
    by = stat_y + 205
    for b in bullets:
        draw.text((85, by), b, fill="#e2e8f0", font=font_bullet)
        by += 76

    # Bottom CTA button
    draw.rounded_rectangle([72, 1215, 928, 1330], radius=24, fill=accent_col)
    draw.text((175, 1252), "CONVERT YOUR PDF FREE NOW ->", fill="#ffffff", font=font_cta)

    # Footer URL
    draw.text((225, 1378), "sahilansari-ui.github.io/notepress", fill="#94a3b8", font=font_url)

    out_path = os.path.join("pins", f"{slug}.jpg")
    img.save(out_path, "JPEG", quality=88, optimize=True)
    file_size = os.path.getsize(out_path)

    page_url = f"{BASE_URL}/pages/{slug}.html"
    img_url = f"{BASE_URL}/pins/{slug}.jpg"
    pub_dt = format_datetime(now - timedelta(hours=idx * 2))
    desc = f"{headline}. {stat_line}. Free online tool for NEET, JEE, PW, Allen, Unacademy, SSC & UPSC students to print dark board notes at 80% lower cost."

    rss_items.append(f"""    <item>
      <title>{html.escape(headline)}</title>
      <link>{page_url}</link>
      <guid isPermaLink="true">{page_url}</guid>
      <pubDate>{pub_dt}</pubDate>
      <description>{html.escape(desc)}</description>
      <enclosure url="{img_url}" length="{file_size}" type="image/jpeg" />
      <media:content url="{img_url}" medium="image" type="image/jpeg" width="1000" height="1500" />
    </item>""")

rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>NotePress Pro — Free Coaching Notes to Printable PDF</title>
    <link>{BASE_URL}/</link>
    <description>Convert 400+ page dark blackboard coaching PDFs into crisp white big-font printable A4 study books free.</description>
    <language>en-in</language>
    <lastBuildDate>{format_datetime(now)}</lastBuildDate>
{chr(10).join(rss_items)}
  </channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

print(f"Generated {len(PINS)} Pinterest vertical pins + feed.xml successfully.")
