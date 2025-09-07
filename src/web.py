from flask import Flask, render_template, request
from data import load_products_gz
from index import ProductIndex
from search import topk_similar, format_results

app = Flask(__name__)

# Load and index once
DATA_PATH = "data/meta_Appliances.json.gz"
docs = [d for d in load_products_gz(DATA_PATH)]
idx = ProductIndex(docs, k=5, num_hashes=100, bands=20, rows=5, seed=42)
idx.build()
id_map = {d.get("asin"): i for i, d in enumerate(docs)}

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
    app.run(host="0.0.0.0", port=5000, debug=True)
