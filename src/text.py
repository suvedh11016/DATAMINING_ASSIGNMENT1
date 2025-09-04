# text.py
# Text cleaning and shingling utilities.

import re
from html import unescape
from typing import Set

_WS = re.compile(r'\s+')
_HTML_TAG = re.compile(r'<[^>]+>')

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = unescape(s)
    s = _HTML_TAG.sub(' ', s)  # strip HTML tags
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)  # keep alnum + space
    s = _WS.sub(' ', s).strip()
    return s

def char_shingles(s: str, k: int) -> Set[str]:
    if not s or k <= 0:
        return set()
    s = f' {s} '  # pad
    if len(s) < k:
        return {s}
    return { s[i:i+k] for i in range(len(s)-k+1) }
