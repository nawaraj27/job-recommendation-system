"""Thin wrapper around Google Gemini with safe JSON parsing + offline fallback."""
import json
import re
from django.conf import settings

def _client():
    if not settings.GEMINI_API_KEY:
        return None
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(settings.GEMINI_MODEL)

def generate_json(prompt, fallback=None):
    """Run prompt, expect JSON back. Returns dict. Falls back when no key/error."""
    model = _client()
    if model is None:
        return fallback if fallback is not None else {}
    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip()
        text = re.sub(r"^```(json)?|```$", "", text, flags=re.M).strip()
        return json.loads(text)
    except Exception:
        return fallback if fallback is not None else {}

def generate_text(prompt, fallback=""):
    model = _client()
    if model is None:
        return fallback
    try:
        return model.generate_content(prompt).text.strip()
    except Exception:
        return fallback
