# Finding Similar Products with MinHash + LSH (Amazon Appliances)

Implements:
- Product listing (Exercise 1)
- Similarity search with PST / PSD / PSTD (Exercise 2)
- MinHash + LSH
- Evaluation (precision@10, MAP@10)
- Hyperparameter sweeps (Exercise 3)

## Usage

```bash
# List products
python3 src/app.py --data data/meta_Appliances.json.gz --list 10

# Search similar products by ASIN
python3 src/app.py --data data/meta_Appliances.json.gz --mode PST --asin B000XXXXXX --topk 10

# Evaluate
python3 src/run_eval.py --data data/meta_Appliances.json.gz --mode PST
python3 src/run_eval.py --data data/meta_Appliances.json.gz --mode PSD

# Hyperparameter sweep
python3 src/sweep.py --data data/meta_Appliances.json.gz --mode PST
