from flask import Flask, render_template, request
import os
from src.data import load_products_gz
from src.index import ProductIndex
from src.search import topk_similar, format_results

app = Flask(__name__)

# Load and index once
DATA_PATH = "data/meta_Appliances.json.gz"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Data file not found at {DATA_PATH}")

try:
    docs = [d for d in load_products_gz(DATA_PATH)]
    idx = ProductIndex(docs, k=5, num_hashes=100, bands=20, rows=5, seed=42)
    idx.build()
    id_map = {d.get("asin"): i for i, d in enumerate(docs)}
except Exception as e:
    raise RuntimeError(f"Failed to load or index data: {e}")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        asin = request.form.get("asin")
        qid = id_map.get(asin)
        if qid is None:
            return render_template("home.html", error=f"ASIN {asin} not found")

        res = topk_similar(idx, qid, mode="PST", top_k=10)
        results = format_results(docs, res)
        return render_template("results.html", query=docs[qid], results=results)

    return render_template("home.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

