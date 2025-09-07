# sweep.py
# Hyperparameter sweeps for Exercise 3.

import argparse, csv, os
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
    ap.add_argument("--mode", default="PST", choices=["PST","PSD"])
    ap.add_argument("--out", default="../artifacts/sweep_results.csv")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    docs = [d for d in load_products_gz(args.data)]

    K_values = [2,3,5,7,10]
    H_values = [10,20,50,100,150]
    bands_for = {10:2, 20:4, 50:10, 100:20, 150:25}
    rows_for  = {10:5, 20:5, 50:5, 100:5, 150:6}

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mode","K","num_hashes","bands","rows","meanP@10","MAP@10"])
        for K in K_values:
            for H in H_values:
                bands = bands_for[H]
                rows = rows_for[H]
                idx = build_index(docs, k=K, num_hashes=H, bands=bands)
                mean_p, map10 = run_eval(docs, idx, mode=args.mode, k=10)
                w.writerow([args.mode, K, H, bands, rows, f"{mean_p:.4f}", f"{map10:.4f}"])
                print(f"Done mode={args.mode} K={K} H={H} -> P@10={mean_p:.4f} MAP@10={map10:.4f}")

if __name__ == "__main__":
    main()
