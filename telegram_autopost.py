import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE = "https://sahilansari-ui.github.io/notepress"

POSTS = [
    f"<b>450 Page PW Class Notes ₹900 ki jagah ₹90 mein print karwao!</b>\n\nNormal apps white question boxes ko kaala dabba bana dete hain aur handwriting cheenti barabar ho jaati hai.\n\n✅ Zero Black Box on White Cards\n✅ Khali jagah auto-squish\n✅ Bada jet-black pen-friendly font\n\n👉 Free Use Karo: {BASE}/pages/pw-black-pdf-to-white-printable.html",
    f"<b>Allen Digital Board Notes ko Low-Cost Book mein badlo!</b>\n\nRepeated PYQs aur blank slides apne aap skip hongi aur print cost 80% tak kam ho jayegi — bina login ke.\n\n👉 Open Tool: {BASE}/pages/allen-digital-board-notes-printable.html",
    f"<b>Unacademy ki Dark Maroon / Black Slides kaise print karein?</b>\n\nYellow, pink aur cyan patli handwriting ko 1 click mein solid <b>Jet-Black Bold Ink</b> mein badlo taaki highlighter chalane par text feeka na pade.\n\n👉 Free Tool: {BASE}/pages/unacademy-dark-slides-to-white-pdf.html",
    f"<b>NEET 2027 Physics One-Shot PDF bahut lambi hai?</b>\n\nAb 470 slides ko 50-60 readable A4 pages mein convert karo — bina ek bhi derivation ya graph chhota kiye.\n\n👉 Try Now: {BASE}/pages/neet-2027-physics-oneshot-printable.html",
    f"<b>NEET Biology NCERT diagram slides ko bina kaala kiye print karo!</b>\n\nDark board pure white hoga aur NCERT wale white diagram boxes bilkul crisp print honge.\n\n👉 Free Tool: {BASE}/pages/neet-biology-class-slides-printable.html",
    f"<b>NEET Chemistry Organic reactions print mein halki grey aati hain?</b>\n\n<b>Bold (Highlighter Safe)</b> mode ON karo — har reaction arrow aur formula deep jet-black print hoga.\n\n👉 Free Converter: {BASE}/pages/neet-chemistry-notes-black-to-white.html",
    f"<b>JEE Mains Physics derivations print mein bahut chhote aate hain?</b>\n\n<b>Anti-Tiny Handwriting Lock</b> dense boards ko apne aap full A4 width deta hai aur chhote graphs ko side-by-side pack karta hai.\n\n👉 Free Converter: {BASE}/pages/jee-mains-physics-notes-printable.html",
    f"<b>JEE Advanced Maths ki lambi integration aur limits slides ko book jaisa pack karo!</b>\n\nZero watermark • Zero login • 100% browser mein offline processing.\n\n👉 Use Free: {BASE}/pages/jee-advanced-maths-board-notes.html",
    f"<b>JEE Chemistry dark flowcharts aur periodic tables ko clean A4 book banao!</b>\n\nDukaan par ₹800 kharch karne se pehle 60 second mein 80% pages kam kar lo.\n\n👉 Open Free: {BASE}/pages/jee-chemistry-slides-to-white-book.html",
    f"<b>SSC CGL Maths aur Reasoning dark board PDF print trick!</b>\n\n500-page PDF ke liye ₹1000 mat kharch karo. Phone Chrome mein hi compact white printable PDF banao — zero server upload.\n\n👉 Open Now: {BASE}/pages/ssc-cgl-maths-dark-notes-printable.html",
    f"<b>SSC CHSL aur GD Coaching PDF ko ₹50-₹70 mein print karwao!</b>\n\nBlank slides aur empty margins auto-cut honge, akshar padhne mein 2x bade rahenge.\n\n👉 Try Free: {BASE}/pages/ssc-chsl-gd-coaching-pdf-converter.html",
    f"<b>UPSC Coaching dark slides ko clean A4 handout mein badlo!</b>\n\nCurrent affairs aur class PPTs ko kam pages mein side pen-margin ke saath print karwao.\n\n👉 Open Tool: {BASE}/pages/upsc-coaching-slides-printable-pdf.html",
    f"<b>GATE Engineering circuit diagrams aur handwritten notes print trick!</b>\n\nCrisp jet-black output, zero black boxes, aur 100% browser privacy.\n\n👉 Open Tool: {BASE}/pages/gate-engineering-notes-black-to-white.html",
    f"<b>Class 12 CBSE YouTube One-Shot notes ko free mein revision book banao!</b>\n\nPrint karwane se pehle <b>100% Real Print Size</b> preview dekho taaki 1 rupaya bhi waste na ho.\n\n👉 Open Free: {BASE}/pages/class-12-cbse-board-notes-printable.html",
    f"<b>Class 11 Science coaching PDF invert karne par kaali ho jaati hai?</b>\n\nNormal inverter chhodo — NotePress Pro sirf dark background hatata hai aur white boxes safe rakhta hai.\n\n👉 Try Now: {BASE}/pages/class-11-science-notes-invert-pdf.html",
    f"<b>Coaching PDF invert karne par white cards kaale dabbe kyun bante hain?</b>\n\nHumara <b>Anti-Blackbox Engine</b> is dikkat ko 100% khatam kar deta hai. Ek baar preview check karo.\n\n👉 Free Converter: {BASE}/pages/invert-pdf-without-black-box.html",
    f"<b>500 Page One-Shot PDF ko 50 Readable Pages mein kaise badlein?</b>\n\n1. PDF upload karo\n2. Smart Adaptive Book rakho\n3. Extra PYQs uncheck karke Download PDF dabao!\n\n👉 Free Tool: {BASE}/pages/reduce-500-page-pdf-to-50-pages.html",
    f"<b>Lecture slides ke andar ki khali jagah print mein paise barbad karti hai!</b>\n\nNotePress Pro ka <b>Internal Gap Squisher</b> khali pattiyan hata kar font bina chhota kiye pages kam kar deta hai.\n\n👉 Try Free: {BASE}/pages/remove-blank-space-inside-pdf-slides.html",
    f"<b>Digital board ki patli stylus handwriting print mein dikhti nahi?</b>\n\n<b>Extra Bold Ink</b> option on karo — halka yellow/cyan text bhi solid black print hoga.\n\n👉 Open Tool: {BASE}/pages/make-handwriting-dark-bold-pdf-print.html",
    f"<b>Notes print karwate waqt side mein pen se likhne ki jagah chahiye?</b>\n\nNotePress Pro mein <b>Right Pen-Margin (Cornell Notes)</b> tick karo — har A4 page par apni tricks likhne ki saaf lined jagah milegi.\n\n👉 Try Karo: {BASE}/pages/add-cornell-margin-to-pdf-notes.html",
    f"<b>Coaching PDF mein repeated question slides par paise kyun barbad karein?</b>\n\nAadhi-adhuri question slides aur blank pages auto-skip honge + manual Slide Manager bhi free milta hai.\n\n👉 Try Free: {BASE}/pages/skip-duplicate-pyq-slides-in-pdf.html",
    f"<b>Dark Maroon, Navy Blue ya Green board slides grey patch chhodti hain?</b>\n\nSmart color cleaner background ko 100% pure white kar deta hai — zero printer ink waste.\n\n👉 Clean Now: {BASE}/pages/maroon-blue-slides-to-white-pdf.html",
    f"<b>6-in-1 PDF app se handwriting cheenti barabar ho jaati hai!</b>\n\nSmart Adaptive Book mode wide boards ko full width deta hai aur chhoti slides ko neat 2-column mein jamata hai.\n\n👉 Difference Dekho: {BASE}/pages/smart-book-vs-6-in-1-pdf-layout.html",
    f"<b>Digital to Printable app ka 100% Free Online Alternative!</b>\n\nBina koi app download kiye seedha Chrome mein 500+ page dark PDF ko bade aksharon mein printable banao.\n\n👉 Try Now: {BASE}/pages/free-alternative-digital-to-printable.html",
    f"<b>Railway RRB NTPC aur Group D class PDFs 80% kam pages mein print karo!</b>\n\nDark slides → Pure White A4 book in 60 seconds, bilkul free.\n\n👉 Free Link: {BASE}/pages/railway-rrb-ntpc-notes-printable.html",
    f"<b>Banking IBPS PO aur SBI Clerk DI graphs ko clean white PDF banao!</b>\n\nDukaan par ₹500 dene se pehle is free browser tool se page count 75% kam kar lo.\n\n👉 Try Now: {BASE}/pages/banking-ibps-sbi-notes-pdf-converter.html",
    f"<b>CA Foundation & Inter ki lambi lecture PDFs ko saste mein print karwao!</b>\n\nDark slides ko crisp jet-black revision booklet mein badlo — zero signup.\n\n👉 Open Tool: {BASE}/pages/ca-foundation-inter-slides-printable.html",
    f"<b>CUET UG 2027 dark coaching notes ko white printable book banao!</b>\n\nUpload karo, 100% Real Print Size preview dekho, aur free download karo.\n\n👉 Use Free: {BASE}/pages/cuet-ug-coaching-notes-black-to-white.html",
    f"<b>NDA & CDS Defence Maths aur GAT dark slides print hack!</b>\n\nZero black boxes, bold highlighter-safe ink, aur 80% paper saving.\n\n👉 Free Tool: {BASE}/pages/nda-cds-defence-notes-printable-pdf.html",
    f"<b>UP Police, Bihar SSC aur State PCS dark board PDFs ko compact book banao!</b>\n\nPoora chapter ₹60-₹80 mein print hoga aur har word crystal clear dikhega.\n\n👉 Try Free: {BASE}/pages/state-pcs-police-exam-notes-printable.html"
]

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("ERROR: TELEGRAM_BOT_TOKEN ya TELEGRAM_CHAT_ID GitHub Secrets mein missing hai.")
        sys.exit(1)

    now = datetime.now(timezone.utc)
    if now.hour < 6:
        slot = 0
    elif now.hour < 12:
        slot = 1
    else:
        slot = 2

    idx = (now.timetuple().tm_yday * 3 + slot) % len(POSTS)
    text = POSTS[idx]

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"SUCCESS! Slot {slot} (Post #{idx + 1}) sent:", resp.status)
    except urllib.error.HTTPError as e:
        print("TELEGRAM API ERROR:", e.code, e.read().decode("utf-8", errors="ignore"))
        sys.exit(1)

if __name__ == "__main__":
    main()
