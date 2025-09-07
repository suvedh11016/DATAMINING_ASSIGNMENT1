# index.py
# Build shingle sets, MinHash signatures, and LSH indices.

from typing import List, Dict, Tuple, Set
from src.text import clean_text, char_shingles
from src.minhash import MinHasher, jaccard
from src.lsh import LSH

class FieldIndex:
    def __init__(self, k_shingle: int, num_hashes: int, bands: int, rows: int, seed: int = 42):
        self.k = k_shingle
        self.mh = MinHasher(num_hashes=num_hashes, seed=seed)
        self.lsh = LSH(bands=bands, rows=rows)
        self.doc_tokens: Dict[int, Set[str]] = {}
        self.doc_sig: Dict[int, List[int]] = {}

    def build_for_field(self, docs: List[Dict], field_getter) -> None:
        for i, d in enumerate(docs):
            text = clean_text(field_getter(d))
            tokens = char_shingles(text, self.k)
            self.doc_tokens[i] = tokens
            sig = self.mh.signature(tokens)
            self.doc_sig[i] = sig
            self.lsh.add(i, sig)

    def query(self, q_tokens: Set[str], top_k: int = 10):
        qsig = self.mh.signature(q_tokens)
        cands = self.lsh.candidates(qsig)
        scores = []
        for cid in cands:
            tokens = self.doc_tokens.get(cid, set())
            score = jaccard(q_tokens, tokens)
            scores.append((cid, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

class ProductIndex:
    def __init__(self, docs: List[Dict], k: int, num_hashes: int, bands: int, rows: int, seed: int = 42):
        self.docs = docs
        self.title_index = FieldIndex(k, num_hashes, bands, rows, seed)
        self.desc_index  = FieldIndex(k, num_hashes, bands, rows, seed)
        self.hybrid_index = FieldIndex(k, num_hashes, bands, rows, seed)

    def build(self):
        self.title_index.build_for_field(self.docs, lambda d: d.get("title",""))
        self.desc_index.build_for_field(self.docs, lambda d: d.get("description",""))
        self.hybrid_index.build_for_field(self.docs, lambda d: (d.get("title","") + " " + d.get("description","")).strip())

    def query(self, doc_id: int, mode: str = "PST", top_k: int = 10):
        doc = self.docs[doc_id]
        if mode == "PST":
            q = clean_text(doc.get("title",""))
            idx = self.title_index
        elif mode == "PSD":
            q = clean_text(doc.get("description",""))
            idx = self.desc_index
        else:
            q = clean_text((doc.get("title","") + " " + doc.get("description","")).strip())
            idx = self.hybrid_index
        q_tokens = char_shingles(q, self.title_index.k)
        return idx.query(q_tokens, top_k=top_k)
