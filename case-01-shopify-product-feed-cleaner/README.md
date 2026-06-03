# Case Study 01: Shopify Product Feed Cleaner

## Client scenario

A small ecommerce store has product data collected from suppliers, old spreadsheets, and manual notes. The data is inconsistent:

- Duplicate or missing SKUs
- Messy product titles
- Inconsistent categories
- Prices with different formats
- Missing inventory values
- No SEO fields

## What this automation does

The script converts a messy supplier-style CSV into a Shopify-ready import file.

It automatically:

- Normalizes titles, vendors, categories, tags, and handles
- Cleans price and inventory fields
- Generates missing SKUs when possible
- Flags rows that need manual review
- Creates SEO title and SEO description fields
- Exports a clean CSV and a short business-readable report

## Files

- `data/raw_products.csv`: sample messy input file
- `src/clean_product_feed.py`: automation script
- `output/cleaned_shopify_products.csv`: generated Shopify-ready output
- `output/product_cleanup_report.md`: generated summary report

## Run

```bash
python3 src/clean_product_feed.py
```

Run this command from this case folder.

## Client value

This is useful for Shopify agencies, ecommerce operators, dropshipping teams, and small brands that need to import or clean product catalogs without spending hours editing spreadsheets by hand.
