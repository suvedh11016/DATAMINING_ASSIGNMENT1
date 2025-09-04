# minhash.py
# Simple MinHash implementation for Jaccard approximation.

import random
from typing import Iterable, List

_LARGE_PRIME = 4294967311

class MinHasher:
    def __init__(self, num_hashes: int = 100, seed: int = 42):
        self.num_hashes = num_hashes
        rnd = random.Random(seed)
        self._a = [rnd.randrange(1, _LARGE_PRIME-1) for _ in range(num_hashes)]
        self._b = [rnd.randrange(0, _LARGE_PRIME-1) for _ in range(num_hashes)]

    def _to_int(self, token: str) -> int:
        h = 2166136261
        for ch in token:
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
        return h

    def signature(self, tokens: Iterable[str]) -> List[int]:
        ints = { self._to_int(t) for t in tokens }
        if not ints:
            return [2**63-1] * self.num_hashes
        sig = []
        for a,b in zip(self._a, self._b):
            m = 2**63-1
            for x in ints:
                val = (a * x + b) % _LARGE_PRIME
                if val < m:
                    m = val
            sig.append(m)
        return sig

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))
