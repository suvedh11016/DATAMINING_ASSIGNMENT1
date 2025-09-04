# # data.py
# # Load Amazon Appliances metadata (2018) from JSON.gz (one JSON per line).

# import gzip
# import json
# from typing import Iterator, Dict, Any
# import re

# def clean_html(raw: str) -> str:
#     # remove HTML tags
#     text = re.sub(r"<.*?>", " ", raw)
#     # collapse extra spaces
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()


# def load_products_gz(path: str) -> Iterator[Dict[str, Any]]:
#     """
#     Yields product dicts with keys: asin, title, description, similar_item.
#     """
#     with gzip.open(path, 'rt', encoding='utf-8') as f:
#         for line in f:
#             try:
#                 obj = json.loads(line)
#             except json.JSONDecodeError:
#                 continue
#             asin = obj.get('asin')
#             title = obj.get('title') or ""
#             # desc = obj.get('description')
#             # if isinstance(desc, list):
#             #     desc = " ".join([str(x) for x in desc if x])
#             desc = obj.get('description') or obj.get('feature') or ""
#             if isinstance(desc, list):
#                 desc = " ".join([str(x) for x in desc if x])
#             desc = clean_html(desc)

#             similar = obj.get('also_buy') or obj.get('also_view') or obj.get('similar_item') or []
#             if not isinstance(similar, list):
#                 similar = []
#             yield {
#                 "asin": asin,
#                 "title": title or "",
#                 "description": desc or "",
#                 "similar_item": similar
#             }



# data.py
# Load Amazon Appliances metadata (2018) from JSON.gz (one JSON per line).

import gzip
import json
from typing import Iterator, Dict, Any
from bs4 import BeautifulSoup

path = "data/meta_Appliances.json.gz"

def clean_html(raw_html: str) -> str:
    """Remove HTML tags and extra spaces from raw HTML/text."""
    if not raw_html:
        return ""
    return BeautifulSoup(raw_html, "lxml").get_text(" ", strip=True)

def load_products_gz(path: str) -> Iterator[Dict[str, Any]]:
    """
    Yields product dicts with keys: asin, title, description, similar_item.
    """
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            asin = obj.get('asin')
            title = obj.get('title') or ""
            desc = obj.get('description') or obj.get('feature') or ""
            if isinstance(desc, list):
                
                desc = " ".join([str(x) for x in desc if x])
            desc = clean_html(desc)  # ✅ Clean description text
            similar = obj.get('also_buy') or obj.get('also_view') or obj.get('similar_item') or []
            if not isinstance(similar, list):
                similar = []
            yield {
                "asin": asin,
                "title": title.strip(),
                "description": desc.strip(),
                "similar_item": similar
            }
