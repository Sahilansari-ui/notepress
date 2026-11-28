import os
import html
from datetime import datetime, timezone

BASE_URL = "https://sahilansari-ui.github.io/notepress"
# Apni doosri website ka link baad mein yahan daal sakte ho (khali chhodoge toh section hide rahega)
SECOND_SITE_URL = ""
SECOND_SITE_LABEL = "Free Sarkari Form Photo & Signature Resizer Tool"

PAGES = [
    ("pw-black-pdf-to-white-printable", "PW Class Notes Black PDF to White Printable Converter", "Physics Wallah (PW)", "Convert 400+ page PW dark board class notes into crisp white jet-black A4 pages without turning white textbook boxes black."),
    ("allen-digital-board-notes-printable", "Allen Digital Board Class Notes to Printable PDF", "Allen Coaching", "Clean dark Allen lecture slides, remove empty margins, skip duplicate slides, and print readable A4 study notes at 80% lower cost."),
    ("unacademy-dark-slides-to-white-pdf", "Unacademy Dark Background Slides to White PDF", "Unacademy", "Convert Unacademy dark maroon and black class slides into clean white printable pages with bold stylus ink for easy highlighting."),
    ("neet-2027-physics-oneshot-printable", "NEET 2027 Physics One-Shot Notes Compact PDF Printer", "NEET Physics", "Turn 450+ page NEET Physics one-shot PDFs into 45-60 readable A4 pages while keeping handwritten derivations and graphs large."),
    ("neet-biology-class-slides-printable", "NEET Biology NCERT & Class Slides Printable Converter", "NEET Biology", "Keep embedded NCERT white diagram boxes clean while converting dark board notes around them to pure white printable pages."),
    ("neet-chemistry-notes-black-to-white", "NEET Chemistry Organic & Physical Notes to White PDF", "NEET Chemistry", "Make thin colored chemical reactions and mechanisms dark jet-black so they never fade under yellow highlighters."),
    ("jee-mains-physics-notes-printable", "JEE Mains Physics Class Notes Printable PDF Converter", "JEE Mains Physics", "Pack long JEE Physics derivations and graphs smartly onto A4 sheets with Anti-Tiny Handwriting full-width protection."),
    ("jee-advanced-maths-board-notes", "JEE Advanced Maths Handwritten Board Notes Printer", "JEE Maths", "Squish blank vertical gaps inside dense Maths solution slides without shrinking tiny equations, limits, or integration symbols."),
    ("jee-chemistry-slides-to-white-book", "JEE Chemistry Dark Class Slides to Printable Book", "JEE Chemistry", "Convert dark periodic tables, organic flowcharts, and coaching slides into high-contrast A4 study booklets for revision."),
    ("ssc-cgl-maths-dark-notes-printable", "SSC CGL Maths & Reasoning Dark Board Notes Printable", "SSC CGL", "Save 75% on print costs by converting SSC CGL dark classroom PDFs into crisp white A4 sheets with side pen-margins."),
    ("ssc-chsl-gd-coaching-pdf-converter", "SSC CHSL & GD Coaching Notes Low-Cost Print Tool", "SSC CHSL / GD", "Turn lengthy SSC CHSL and GD coaching PDFs into compact, readable A4 handouts directly in your mobile or PC browser."),
    ("upsc-coaching-slides-printable-pdf", "UPSC Current Affairs & Class Slides Printable PDF", "UPSC CSE", "Convert dark UPSC coaching PPTs into clean printable notes with optional Cornell side margins for adding your own points."),
    ("gate-engineering-notes-black-to-white", "GATE Engineering Class Notes Black to White PDF", "GATE Exam", "Clean dark circuit diagrams, formulas, and handwritten GATE board slides into razor-sharp black-and-white A4 prints."),
    ("class-12-cbse-board-notes-printable", "Class 12 CBSE Physics & Maths Board Slides Printable", "Class 12 Boards", "Convert online tuition and YouTube one-shot Class 12 dark slides into neat white revision books at zero cost."),
    ("class-11-science-notes-invert-pdf", "Class 11 Science Coaching Notes Invert Without Black Box", "Class 11 Science", "Invert dark board Class 11 notes smartly so embedded white question images stay white instead of wasting printer ink."),
    ("invert-pdf-without-black-box", "Invert Dark PDF Notes Without Turning White Cards Black", "Anti-Blackbox Engine", "Fix the biggest flaw of normal PDF inverters: convert black backgrounds to white while protecting embedded white question cards."),
    ("reduce-500-page-pdf-to-50-pages", "Convert 500 Page One-Shot PDF into 50 Readable Pages", "Page Saver Engine", "Combine auto-crop, internal gap squishing, and duplicate slide skipping to cut 500-page coaching PDFs down by 80%."),
    ("remove-blank-space-inside-pdf-slides", "Remove Blank Space Inside Coaching PDF Slides Free", "Gap Squisher", "Automatically detect and collapse empty blank bands inside lecture slides so fonts stay big while page count drops."),
    ("make-handwriting-dark-bold-pdf-print", "Make Thin Stylus Handwriting Dark & Bold for Printing", "Ink Boldener", "Boost faint yellow, cyan, and pink digital board handwriting into thick, jet-black print ink that survives highlighters."),
    ("add-cornell-margin-to-pdf-notes", "Add Side Pen-Margin (Cornell Notes) to Coaching PDFs", "Cornell Margin", "Automatically add a clean lined note-taking strip on the right side of every printed A4 page for tricks and formulas."),
    ("skip-duplicate-pyq-slides-in-pdf", "Auto-Skip Duplicate & Half Slides in Coaching PDFs", "Duplicate Cleaner", "Stop paying to print question-only slides that repeat on the next solution page — auto-detect and remove them in one click."),
    ("maroon-blue-slides-to-white-pdf", "Convert Dark Maroon & Blue Coaching Slides to White", "Color Board Cleaner", "Remove dark maroon, navy blue, and green digital board backgrounds cleanly without leaving grey patches on your printout."),
    ("smart-book-vs-6-in-1-pdf-layout", "Why 6-in-1 Grid Makes Notes Tiny (Better Alternative)", "Smart Adaptive Layout", "Compare rigid 6-in-1 PDF grids against Smart Adaptive Book packing that gives wide handwritten boards full A4 width."),
    ("free-alternative-digital-to-printable", "Free Online Alternative to Digital to Printable App", "Web App Alternative", "Use NotePress Pro directly in Chrome on phone or PC — no app download, no black boxes, and bigger pen-friendly text."),
    ("railway-rrb-ntpc-notes-printable", "Railway RRB NTPC & Group D Class Slides to Printable PDF", "Railway RRB", "Convert dark Railway exam class PDFs and GK slides into crisp white, low-cost printable study sheets in minutes."),
    ("banking-ibps-sbi-notes-pdf-converter", "Banking IBPS PO & SBI Clerk Board Notes PDF Converter", "Banking Exams", "Turn dark DI graphs, puzzles, and quant class notes into crystal-clear A4 printouts with zero server upload."),
    ("ca-foundation-inter-slides-printable", "CA Foundation & Inter Dark Class Slides Printable Book", "CA Exams", "Convert lengthy CA lecture slide PDFs into neatly packed, dark-ink A4 study notes to cut printing expenses drastically."),
    ("cuet-ug-coaching-notes-black-to-white", "CUET UG 2027 Coaching Notes Black to White Converter", "CUET UG", "Clean CUET domain subject and general test dark PDFs into readable white printouts directly from your browser."),
    ("nda-cds-defence-notes-printable-pdf", "NDA & CDS Defence Coaching Slides Printable PDF Tool", "NDA / CDS", "Convert NDA Maths and GAT dark board PDFs into compact, bold-ink A4 revision sheets completely free."),
    ("state-pcs-police-exam-notes-printable", "State PCS & Police Exam Digital Board Notes Converter", "State Exams", "Turn UP Police, Bihar SSC, and State PCS dark coaching slides into clean white printable books without losing clarity.")
]

os.makedirs("pages", exist_ok=True)
today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

cross_promo_html = ""
if SECOND_SITE_URL.strip():
    cross_promo_html = f"""
    <div class="bg-indigo-950/50 border border-indigo-500/30 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <div class="text-xs sm:text-sm text-indigo-100"><b>Also useful for students:</b> {html.escape(SECOND_SITE_LABEL)}</div>
      <a href="{html.escape(SECOND_SITE_URL)}" target="_blank" rel="noopener" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-bold text-white shrink-0">Open Free Tool →</a>
    </div>"""

def build_page(idx, slug, title, tag, desc):
    related = [PAGES[(idx + k) % len(PAGES)] for k in range(1, 6)]
    related_links = "\n".join(
        f'<li><a href="{r[0]}.html" class="text-indigo-400 hover:text-indigo-300 underline-offset-2 hover:underline">{html.escape(r[1])}</a></li>'
        for r in related
    )
    page_url = f"{BASE_URL}/pages/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} — NotePress Pro (Free)</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{page_url}" />
  <link rel="manifest" href="../manifest.json" />
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
  <header class="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-30">
    <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../index.html" class="flex items-center gap-2 font-extrabold text-base text-white">
        <span class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">N</span>
        <span>NotePress <span class="text-indigo-400">Pro</span></span>
      </a>
      <a href="../index.html" class="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-bold text-white">Open Free Converter →</a>
    </div>
  </header>

  <main class="max-w-5xl w-full mx-auto px-4 py-8 space-y-8 flex-1">
    <section class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-4">
      <span class="inline-block text-[11px] font-bold px-3 py-1 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30">{html.escape(tag)} • 100% Free Browser Tool</span>
      <h1 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">{html.escape(title)}</h1>
      <p class="text-sm sm:text-base text-slate-300 leading-relaxed">{html.escape(desc)}</p>
      <div class="pt-2 flex flex-wrap gap-3">
        <a href="../index.html" class="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 font-bold text-sm text-white shadow-lg shadow-indigo-600/30">
          📄 Upload PDF & Convert Free Now →
        </a>
        <a href="index.html" class="px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 font-semibold text-sm text-slate-200">
          Browse All Exam Guides
        </a>
      </div>
      <p class="text-xs text-emerald-400">🔒 Zero Server Upload • Runs 100% offline inside your phone or laptop Chrome browser</p>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-1.5">
        <h2 class="font-bold text-sm text-white">1. Zero Black Boxes</h2>
        <p class="text-xs text-slate-400 leading-relaxed">Smart region detection turns dark {html.escape(tag)} boards pure white while keeping embedded white question boxes clean.</p>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-1.5">
        <h2 class="font-bold text-sm text-white">2. Big Pen-Friendly Text</h2>
        <p class="text-xs text-slate-400 leading-relaxed">Internal Gap Squisher removes empty white space and gives dense handwritten slides full A4 width so text never shrinks tiny.</p>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-1.5">
        <h2 class="font-bold text-sm text-white">3. Save 75–85% Print Cost</h2>
        <p class="text-xs text-slate-400 leading-relaxed">Auto-skips blank and repeated PYQ slides so a 450-page chapter prints cleanly in 45–65 A4 sheets instead of ₹900.</p>
      </div>
    </section>

    <section class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
      <h2 class="font-bold text-lg text-white">Best Settings for {html.escape(tag)} PDFs</h2>
      <ol class="list-decimal list-inside text-xs sm:text-sm text-slate-300 space-y-2">
        <li>Open <a href="../index.html" class="text-indigo-400 underline font-semibold">NotePress Pro Converter</a> and select your PDF file (supports 500+ pages).</li>
        <li>Keep <b>Smart Adaptive Book</b> mode ON with <b>Deep Jet-Black</b> ink and <b>Bold (Highlighter Safe)</b> thickness.</li>
        <li>Keep <b>Internal Gap Squisher</b>, <b>Protect Wide Handwriting</b>, and <b>Smart Skip Duplicates</b> checked.</li>
        <li>Click <b>Generate Preview</b>, verify font clarity with <b>100% Real Print Size</b>, and click <b>Download PDF</b>.</li>
      </ol>
    </section>

    {cross_promo_html}

    <section class="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-3">
      <h2 class="font-bold text-base text-white">Related Free Coaching PDF Guides</h2>
      <ul class="space-y-2 text-xs sm:text-sm">{related_links}</ul>
    </section>
  </main>

  <footer class="border-t border-slate-800 py-5 text-center text-xs text-slate-500">
    NotePress Pro • Free Student Study Tool • Updated {today_iso}
  </footer>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "How to use {html.escape(title)}?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{html.escape(desc)} Open NotePress Pro, upload your PDF, select Smart Adaptive Book mode, and download your A4 printable book free."
        }}
      }}
    ]
  }}
  </script>
</body>
</html>
"""

urls = [f"{BASE_URL}/", f"{BASE_URL}/pages/"]
directory_cards = []

for idx, (slug, title, tag, desc) in enumerate(PAGES):
    out_path = os.path.join("pages", f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(build_page(idx, slug, title, tag, desc))
    urls.append(f"{BASE_URL}/pages/{slug}.html")
    directory_cards.append(
        f'<a href="{slug}.html" class="block bg-slate-900 border border-slate-800 hover:border-indigo-500 rounded-2xl p-4 transition">'
        f'<span class="text-[10px] font-bold text-indigo-400 uppercase">{html.escape(tag)}</span>'
        f'<h2 class="font-bold text-sm text-white mt-1">{html.escape(title)}</h2>'
        f'<p class="text-xs text-slate-400 mt-1.5 line-clamp-2">{html.escape(desc)}</p></a>'
    )

# Build /pages/index.html hub so Google discovers all 30 pages cleanly
hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All Exam & Coaching PDF Print Guides — NotePress Pro</title>
  <meta name="description" content="Browse 30+ free guides to convert PW, Allen, Unacademy, NEET, JEE, SSC, and UPSC dark blackboard PDFs into readable white A4 printables." />
  <link rel="canonical" href="{BASE_URL}/pages/" />
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
  <header class="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-30">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../index.html" class="font-extrabold text-base text-white">NotePress <span class="text-indigo-400">Pro</span></a>
      <a href="../index.html" class="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-bold text-white">Open PDF Converter →</a>
    </div>
  </header>
  <main class="max-w-6xl mx-auto px-4 py-8 space-y-6">
    <div class="text-center max-w-2xl mx-auto">
      <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Free Coaching & Exam PDF Print Guides</h1>
      <p class="text-xs sm:text-sm text-slate-400 mt-2">Select your exam or coaching platform to convert dark board notes into crisp, big-font printable A4 books.</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {"".join(directory_cards)}
    </div>
  </main>
</body>
</html>
"""
with open(os.path.join("pages", "index.html"), "w", encoding="utf-8") as f:
    f.write(hub_html)

# Auto-generate sitemap.xml with all 32 URLs
sitemap_items = "\n".join(
    f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today_iso}</lastmod>\n    <priority>{'1.0' if i == 0 else '0.8'}</priority>\n  </url>"
    for i, u in enumerate(urls)
)
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}
</urlset>
"""
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

# Ensure robots.txt stays updated
robots_txt = f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n"
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_txt)

print(f"Autopilot complete: {len(PAGES)} SEO pages + hub + sitemap.xml + robots.txt generated.")
