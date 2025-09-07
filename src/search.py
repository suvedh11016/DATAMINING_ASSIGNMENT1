# search.py
# Provide user-facing search helpers

from typing import List, Dict, Tuple
from src.index import ProductIndex

def topk_similar(index: ProductIndex, doc_id: int, mode: str, top_k: int = 10) -> List[Tuple[int, float]]:
    return index.query(doc_id, mode=mode, top_k=top_k)

def format_results(docs: List[Dict], results: List[tuple]) -> List[Dict]:
    out = []
    for cid, score in results:
        d = docs[cid]
        out.append({
            "asin": d.get("asin"),
            "title": d.get("title","")[:120],
            "score": round(score, 4)
        })
    return out
