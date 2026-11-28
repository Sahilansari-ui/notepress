import os
import html
import textwrap
from datetime import date, datetime, timedelta, timezone
from email.utils import format_datetime
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://sahilansari-ui.github.io/notepress"
BRAND_NAME = "Reb ToolBox"
START_DATE = date(2026, 11, 28)

TOPICS = [
    ("pw-black-pdf-to-white-printable", "PW Class Notes", "PW NOTES", "471 Slides -> 50 Readable Pages • Save Rs.800+"),
    ("allen-digital-board-notes-printable", "Allen Digital Board Notes", "ALLEN NOTES", "Zero Black Boxes • Big Pen-Friendly Text"),
    ("unacademy-dark-slides-to-white-pdf", "Unacademy Dark Slides", "UNACADEMY PDF", "Dark Maroon & Black -> Pure White Book"),
    ("neet-2027-physics-oneshot-printable", "NEET 2027 Physics One-Shot", "NEET PHYSICS", "Keep Derivations & Graphs Big & Clear"),
    ("neet-biology-class-slides-printable", "NEET Biology NCERT Slides", "NEET BIOLOGY", "Embedded White Diagram Cards Stay Clean"),
    ("neet-chemistry-notes-black-to-white", "NEET Chemistry Reactions", "NEET CHEMISTRY", "Highlighter-Safe Bold Ink for Revision"),
    ("jee-mains-physics-notes-printable", "JEE Mains Physics Notes", "JEE PHYSICS", "Anti-Tiny Handwriting Auto Full-Width"),
    ("jee-advanced-maths-board-notes", "JEE Advanced Maths Notes", "JEE MATHS", "Squish Blank Gaps Without Shrinking Text"),
    ("jee-chemistry-slides-to-white-book", "JEE Chemistry Dark Slides", "JEE CHEMISTRY", "Crisp Organic Flowcharts & Equations"),
    ("ssc-cgl-maths-dark-notes-printable", "SSC CGL Maths Board PDF", "SSC CGL PREP", "Save 75% Print Money + Add Pen Margin"),
    ("ssc-chsl-gd-coaching-pdf-converter", "SSC CHSL & GD Notes PDF", "SSC EXAMS", "Works 100% Free Inside Phone Chrome"),
    ("upsc-coaching-slides-printable-pdf", "UPSC Coaching Dark PPTs", "UPSC CSE", "Add Lined Cornell Side Margin Automatically"),
    ("gate-engineering-notes-black-to-white", "GATE Circuit & Board Notes", "GATE EXAM", "Razor-Sharp B&W Diagrams & Formulas"),
    ("class-12-cbse-board-notes-printable", "Class 12 CBSE One-Shot PDF", "CLASS 12 BOARDS", "Zero Watermark • Zero Login • 100% Free"),
    ("class-11-science-notes-invert-pdf", "Class 11 Science Board PDF", "CLASS 11 NOTES", "Smart White-Card Protection Engine"),
    ("invert-pdf-without-black-box", "Black PDF Without Black Box", "STUDY HACK", "Fix Normal PDF Inverter Mistakes Free"),
    ("reduce-500-page-pdf-to-50-pages", "500-Page PDF into 50 Pages", "MONEY SAVER", "Rs.900 Printout Now Costs Only Rs.90"),
    ("remove-blank-space-inside-pdf-slides", "Remove Slide Blank Space", "GAP SQUISHER", "Fewer A4 Pages With 2x Larger Letters"),
    ("make-handwriting-dark-bold-pdf-print", "Dark Bold Stylus Print Ink", "INK BOLDENER", "Thick Jet-Black Print • Highlighter Safe"),
    ("add-cornell-margin-to-pdf-notes", "Add Cornell Pen Margin", "CORNELL NOTES", "Write Your Own Tricks Beside Printouts"),
    ("skip-duplicate-pyq-slides-in-pdf", "Skip Repeated PYQ Slides", "DUPLICATE CLEANER", "Stop Paying to Print Half-Empty Slides"),
    ("maroon-blue-slides-to-white-pdf", "Maroon & Blue Board Slides", "BOARD CLEANER", "No Grey Patches • Pure White Background"),
    ("smart-book-vs-6-in-1-pdf-layout", "Better Than 6-in-1 PDF Grid", "SMART LAYOUT", "Wide Boards Get Full Width Automatically"),
    ("free-alternative-digital-to-printable", "Free Digital-to-Printable", "WEB TOOL", "No App Download • Bigger Clearer Font"),
    ("railway-rrb-ntpc-notes-printable", "Railway RRB NTPC Notes", "RAILWAY RRB", "Convert 400+ Slides in 60 Seconds Free"),
    ("banking-ibps-sbi-notes-pdf-converter", "Banking IBPS & SBI Notes", "BANKING EXAMS", "100% Private • Zero Server File Upload"),
    ("ca-foundation-inter-slides-printable", "CA Foundation & Inter PDF", "CA EXAMS", "Cut Coaching Printout Bills by 80%"),
    ("cuet-ug-coaching-notes-black-to-white", "CUET UG 2027 Dark Notes", "CUET UG", "Instant A4 Preview Before You Print"),
    ("nda-cds-defence-notes-printable-pdf", "NDA & CDS Defence Notes", "NDA / CDS", "Bold Jet-Black Ink • Zero Ink Waste"),
    ("state-pcs-police-exam-notes-printable", "State PCS & Police Notes", "STATE EXAMS", "Print Entire Chapters Under Rs.80"),
]

ANGLES = [
    ("Print {topic} in Crisp White at 80% Less Cost", "CONVERT YOUR PDF FREE ->"),
    ("Convert {topic} to Big-Font Printable Book", "TRY FREE IN BROWSER ->"),
    ("Stop Wasting Money Printing {topic} Dark PDFs", "SAVE 80% PRINT COST ->"),
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
font_title = load_font(64, bold=True)
font_stat = load_font(34, bold=True)
font_bullet = load_font(35, bold=False)
font_cta = load_font(36, bold=True)
font_url = load_font(28, bold=False)

now_utc = datetime.now(timezone.utc)
today = now_utc.date()
window_start = today if today <= START_DATE else max(START_DATE, today - timedelta(days=5))

keep_daily_files = set()
rss_items = []

# Generate rolling 6-day window (3 fresh pins added every single day)
days_count = (today - window_start).days + 1
for offset in range(days_count):
    d = today - timedelta(days=offset)
    day_num = max(0, (d - START_DATE).days)
    d_str = d.strftime("%Y%m%d")

    for slot in (2, 1, 0):
        seq = day_num * 3 + slot
        slug, topic_name, badge, stat_line = TOPICS[seq % len(TOPICS)]
        angle_tmpl, cta_text = ANGLES[(seq // len(TOPICS)) % len(ANGLES)]
        headline = angle_tmpl.format(topic=topic_name)
        bg_col, accent_col, light_col, box_col = THEMES[(seq + slot) % len(THEMES)]

        filename = f"pin_{d_str}_{slot + 1}.jpg"
        keep_daily_files.add(filename)
        out_path = os.path.join("pins", filename)

        img = Image.new("RGB", (1000, 1500), bg_col)
        draw = ImageDraw.Draw(img)

        draw.rounded_rectangle([32, 32, 968, 1468], radius=36, outline=accent_col, width=4)
        draw.rounded_rectangle([72, 82, 540, 152], radius=35, fill=box_col, outline=accent_col, width=2)
        draw.text((102, 100), badge, fill=light_col, font=font_badge)
        draw.text((680, 100), BRAND_NAME, fill="#94a3b8", font=font_badge)

        lines = textwrap.wrap(headline, width=19)[:4]
        y = 215
        for line in lines:
            draw.text((75, y), line, fill="#ffffff", font=font_title)
            y += 84

        stat_y = max(610, y + 45)
        draw.rounded_rectangle([72, stat_y, 928, stat_y + 150], radius=24, fill=box_col, outline=light_col, width=3)
        stat_lines = textwrap.wrap(stat_line, width=34)[:2]
        sy = stat_y + (52 if len(stat_lines) == 1 else 28)
        for sl in stat_lines:
            draw.text((105, sy), sl, fill=light_col, font=font_stat)
            sy += 50

        bullets = [
            "✓  Zero Black Boxes on White Cards",
            "✓  Big Pen-Friendly Jet-Black Font",
            "✓  100% Free • Runs in Phone Browser",
        ]
        by = stat_y + 205
        for b in bullets:
            draw.text((85, by), b, fill="#e2e8f0", font=font_bullet)
            by += 76

        draw.rounded_rectangle([72, 1215, 928, 1330], radius=24, fill=accent_col)
        draw.text((175, 1252), cta_text, fill="#ffffff", font=font_cta)
        draw.text((225, 1378), "sahilansari-ui.github.io/notepress", fill="#94a3b8", font=font_url)

        img.save(out_path, "JPEG", quality=88, optimize=True)
        file_size = os.path.getsize(out_path)

        page_url = f"{BASE_URL}/pages/{slug}.html?utm_source=pinterest&pin={d_str}_{slot + 1}"
        img_url = f"{BASE_URL}/pins/{filename}"
        pub_dt = format_datetime(datetime(d.year, d.month, d.day, 3 + slot * 5, 0, 0, tzinfo=timezone.utc))
        desc = (
            f"{headline}. {stat_line}. Free online tool by {BRAND_NAME} (NotePress Pro) for NEET, JEE, "
            f"PW, Allen, Unacademy, SSC & UPSC students to print dark board notes at 80% lower cost."
        )

        rss_items.append(f"""    <item>
      <title>{html.escape(headline)}</title>
      <link>{html.escape(page_url)}</link>
      <guid isPermaLink="true">{html.escape(page_url)}</guid>
      <pubDate>{pub_dt}</pubDate>
      <description>{html.escape(desc)}</description>
      <enclosure url="{html.escape(img_url)}" length="{file_size}" type="image/jpeg" />
      <media:content url="{html.escape(img_url)}" medium="image" type="image/jpeg" width="1000" height="1500" />
    </item>""")

# Clean up older daily pin files (>6 days) so repo stays lightweight forever
for fname in os.listdir("pins"):
    if fname.startswith("pin_") and fname.endswith(".jpg") and fname not in keep_daily_files:
        os.remove(os.path.join("pins", fname))

rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>{BRAND_NAME} — Free Coaching Notes to Printable PDF</title>
    <link>{BASE_URL}/</link>
    <description>Daily printable notes tips &amp; free browser tools by {BRAND_NAME} to convert 400+ page dark blackboard coaching PDFs into crisp white A4 study books.</description>
    <language>en-in</language>
    <lastBuildDate>{format_datetime(now_utc)}</lastBuildDate>
{chr(10).join(rss_items)}
  </channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

print(f"Daily drip updated: {len(rss_items)} active items in feed.xml (3 fresh pins/day).")
