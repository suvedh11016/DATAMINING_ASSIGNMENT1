# eval.py
# Evaluation utilities: precision@k, AP, MAP, hyperparameter sweeps.

from typing import List, Dict, Tuple
from index import ProductIndex

def precision_at_k(pred: List[str], gold: List[str], k: int = 10) -> float:
    k = min(k, len(pred))
    if k == 0: return 0.0
    pset = set(pred[:k])
    gset = set(gold)
    if not gset: return 0.0
    return len(pset & gset) / k

def average_precision_at_k(pred: List[str], gold: List[str], k: int = 10) -> float:
    if not gold: return 0.0
    gset = set(gold)
    ap = 0.0
    hit = 0
    for i, a in enumerate(pred[:k], start=1):
        if a in gset:
            hit += 1
            ap += hit / i
    return ap / min(k, len(gold)) if k>0 else 0.0

def map_at_10(all_preds: List[List[str]], all_golds: List[List[str]]) -> float:
    aps = [average_precision_at_k(p, g, k=10) for p,g in zip(all_preds, all_golds)]
    return sum(aps)/len(aps) if aps else 0.0

def build_eval_set(docs: List[Dict], top_n: int = 100) -> List[int]:
    sizes = [(i, len(d.get("similar_item", []))) for i,d in enumerate(docs)]
    sizes.sort(key=lambda x: x[1], reverse=True)
    return [i for i,_ in sizes[:top_n]]

def run_eval(docs: List[Dict], index: ProductIndex, mode: str = "PST", k: int = 10) -> Tuple[float, float]:
    eval_ids = build_eval_set(docs, top_n=100)
    preds, golds = [], []
    for i in eval_ids:
        res = index.query(i, mode=mode, top_k=k)
        pred_asins = [docs[cid].get("asin") for cid,_ in res]
        gold = docs[i].get("similar_item", [])
        preds.append(pred_asins)
        golds.append(gold)
    mean_p = sum(precision_at_k(p,g,k) for p,g in zip(preds,golds)) / len(preds) if preds else 0.0
    m_ap10 = map_at_10(preds, golds)
    return mean_p, m_ap10
