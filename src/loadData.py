# from data import load_products_gz

# # set the path to your dataset
# path = "../data/meta_Appliances.json.gz"   # adjust based on your folder

# # load and print first 5 products
# for i, product in enumerate(load_products_gz(path)):
#     print(product['asin'], product['description'])  # print asin + title

# list_products.py
# Exercise 1: Load and list first 10 products neatly

from data import load_products_gz
import textwrap

def main():
    path = "../data/meta_Appliances.json.gz"  # adjust if needed
    products = load_products_gz(path)

    print(f"{'ASIN'} | {'Title'} | Description")
    print("-" * 120)

    for i, p in enumerate(products):
        asin = p["asin"] or "N/A"
        title = (p["title"] or "").strip()
        desc = (p["description"] or "").strip()

        # truncate description for display
        short_desc = textwrap.shorten(desc, width=60, placeholder="...")

        print(f"{asin} | {title} | {short_desc}")

        if i >= 9:  # only show 10 products
            break

if __name__ == "__main__":
    main()
