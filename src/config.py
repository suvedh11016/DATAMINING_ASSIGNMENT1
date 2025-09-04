# config.py
# Central place to tweak hyperparameters for the assignment

DATA_PATH = "../data/meta_Appliances.json.gz"    # change if needed
SAVE_DIR  = "../artifacts"

# Default text fields to use
USE_TITLE = True
USE_DESC  = True

# Shingling
K_SHINGLE = 5           # default k for char-level shingles

# MinHash
NUM_HASHES = 100        # number of hash functions

# LSH
BANDS = 20              # number of bands
ROWS  = NUM_HASHES // BANDS  # rows per band; ensure NUM_HASHES % BANDS == 0

# Search
TOP_K = 10              # top-k similar products to return

# Random seed for reproducibility
# SEED = None
