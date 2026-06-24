"""Resume text extraction from PDF / DOCX."""
import os
import re

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return _from_pdf(path)
    if ext == ".docx":
        return _from_docx(path)
    return ""

def _from_pdf(path):
    import pdfplumber
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def _from_docx(path):
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

LINK_PATTERNS = {
    "github": r"github\.com/[A-Za-z0-9_-]+",
    "linkedin": r"linkedin\.com/in/[A-Za-z0-9_-]+",
}

def extract_links(text):
    found = {}
    for name, pat in LINK_PATTERNS.items():
        m = re.search(pat, text, re.I)
        if m:
            found[name] = "https://" + m.group(0)
    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    if emails:
        found["email"] = emails[0]
    return found
