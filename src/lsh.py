# lsh.py
# LSH for MinHash signatures using banding technique.

from collections import defaultdict
from typing import List, Dict, Set, Iterable

def _band_hash(rows: Iterable[int]) -> int:
    h = 1469598103934665603
    for x in rows:
        h ^= x & 0xFFFFFFFFFFFFFFFF
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

class LSH:
    def __init__(self, bands: int, rows: int):
        self.bands = bands
        self.rows = rows
        self.tables: List[Dict[int, Set[int]]] = [defaultdict(set) for _ in range(bands)]

    def add(self, doc_id: int, signature: List[int]):
        for b in range(self.bands):
            start = b * self.rows
            end = start + self.rows
            key = _band_hash(signature[start:end])
            self.tables[b][key].add(doc_id)

    def candidates(self, signature: List[int]) -> Set[int]:
        cands: Set[int] = set()
        for b in range(self.bands):
            start = b * self.rows
            end = start + self.rows
            key = _band_hash(signature[start:end])
            bucket = self.tables[b].get(key)
            if bucket:
                cands.update(bucket)
        return cands
