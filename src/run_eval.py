# run_eval.py
# Run evaluation for Exercise 3.

import argparse
from src.data import load_products_gz
from src.index import ProductIndex
from src.eval import run_eval

def build_index(docs, k, num_hashes, bands):
    rows = num_hashes // bands
    idx = ProductIndex(docs, k=k, num_hashes=num_hashes, bands=bands, rows=rows, seed=42)
    idx.build()
    return idx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--mode", default="PST", choices=["PST","PSD","PSTD"])
    ap.add_argument("--kshingle", type=int, default=5)
    ap.add_argument("--numhashes", type=int, default=100)
    ap.add_argument("--bands", type=int, default=20)
    args = ap.parse_args()

    docs = [d for d in load_products_gz(args.data)]
    idx = build_index(docs, args.kshingle, args.numhashes, args.bands)
    mean_p, map10 = run_eval(docs, idx, mode=args.mode, k=10)
    print(f"Results mode={args.mode} k={args.kshingle} H={args.numhashes} bands={args.bands}:")
    print(f"  Mean Precision@10: {mean_p:.4f}")
    print(f"  MAP@10:           {map10:.4f}")

if __name__ == "__main__":
    main()
