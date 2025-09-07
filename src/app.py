# # app.py
# # CLI to list products and search similar ones via PST/PSD/PSTD.

# import argparse
# from data import load_products_gz
# from index import ProductIndex
# from search import topk_similar, format_results

# def build_index(docs, k, num_hashes, bands):
#     rows = num_hashes // bands
#     if rows * bands != num_hashes:
#         raise ValueError("NUM_HASHES must be divisible by BANDS")
#     idx = ProductIndex(docs, k=k, num_hashes=num_hashes, bands=bands, rows=rows, seed=42)
#     print("Building indices...")
#     idx.build()
#     return idx

# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--data", required=True)
#     ap.add_argument("--mode", default="PST", choices=["PST","PSD","PSTD"])
#     ap.add_argument("--kshingle", type=int, default=5)
#     ap.add_argument("--numhashes", type=int, default=100)
#     ap.add_argument("--bands", type=int, default=20)
#     ap.add_argument("--topk", type=int, default=10)
#     ap.add_argument("--list", action="store_true")
#     ap.add_argument("--asin", type=str, default=None)
#     args = ap.parse_args()

#     docs = [d for d in load_products_gz(args.data)]
#     print(f"Loaded {len(docs)} products")
#     idx = build_index(docs, args.kshingle, args.numhashes, args.bands)

#     if args.list:
#         for i,d in enumerate(docs[:10]):
#             print(f"{i:5d}  {d.get('asin')}  {d.get('title','')[:80]}")
#         return

#     id_map = { d.get("asin"): i for i,d in enumerate(docs) }
#     qid = id_map.get(args.asin, 0) if args.asin else 0

#     print(f"Query asin={docs[qid].get('asin')} mode={args.mode}")
#     res = topk_similar(idx, qid, mode=args.mode, top_k=args.topk)
#     for r in format_results(docs, res):
#         print(f"{r['asin']:>12} | {r['score']:.4f} | {r['title']}")

# if __name__ == "__main__":
#     main()

# app.py
# CLI to list products and search similar ones via PST/PSD/PSTD.

import argparse
from src.data import load_products_gz
from src.index import ProductIndex
from src.search import topk_similar, format_results

def build_index(docs, k, num_hashes, bands):
    rows = num_hashes // bands
    if rows * bands != num_hashes:
        raise ValueError("NUM_HASHES must be divisible by BANDS")
    idx = ProductIndex(docs, k=k, num_hashes=num_hashes, bands=bands, rows=rows, seed=42)
    print("Building indices...")
    idx.build()
    return idx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--mode", default="PST", choices=["PST","PSD","PSTD"])
    ap.add_argument("--kshingle", type=int, default=5)
    ap.add_argument("--numhashes", type=int, default=100)
    ap.add_argument("--bands", type=int, default=20)
    ap.add_argument("--topk", type=int, default=10)
    ap.add_argument("--list", nargs="?", const=10, type=int, help="List first N products (default 10)")
    ap.add_argument("--asin", type=str, default=None)
    args = ap.parse_args()

    docs = [d for d in load_products_gz(args.data)]
    print(f"Loaded {len(docs)} products")

    # ✅ If --list, just show N products with title + description
    if args.list:
        n = args.list
        for i, d in enumerate(docs[:n]):
            print(f"{i:5d}  {d.get('asin')}")
            print(f"Title       : {d.get('title','')}")
            print(f"Description : {d.get('description','')}")
            print("-" * 80)
        return

    # Otherwise build index
    idx = build_index(docs, args.kshingle, args.numhashes, args.bands)

    id_map = { d.get("asin"): i for i,d in enumerate(docs) }
    qid = id_map.get(args.asin, 0) if args.asin else 0

    print(f"Query asin={docs[qid].get('asin')} mode={args.mode}")
    res = topk_similar(idx, qid, mode=args.mode, top_k=args.topk)
    for r in format_results(docs, res):
        print(f"{r['asin']:>12} | {r['score']:.4f} | {r['title']}")

if __name__ == "__main__":
    main()

