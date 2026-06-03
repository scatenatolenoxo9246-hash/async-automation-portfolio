#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw_products.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_CSV = OUTPUT_DIR / "cleaned_shopify_products.csv"
REPORT_FILE = OUTPUT_DIR / "product_cleanup_report.md"


CATEGORY_RULES = [
    ("Apparel & Accessories > Clothing", ["legging", "yoga", "women", "apparel", "clothing"]),
    ("Home & Garden > Lighting", ["lamp", "light", "lighting", "led strip"]),
    ("Home & Garden > Kitchen & Dining", ["cutting board", "kitchen", "mug", "coffee"]),
    ("Sporting Goods > Outdoor Recreation", ["bottle", "outdoor", "travel", "packing"]),
    ("Electronics > Audio", ["speaker", "bluetooth"]),
    ("Animals & Pet Supplies > Pet Grooming", ["pet", "grooming", "brush"]),
    ("Office Supplies", ["mouse", "office"]),
]

ACRONYMS = {"LED", "USB", "RGB", "IPX7", "750ML", "5M"}


def clean_space(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def clean_vendor(value: str) -> str:
    value = clean_space(value)
    known = {
        "brighthome": "Bright Home",
        "bright home": "Bright Home",
        "fit wear": "FitWear",
        "fitwear": "FitWear",
    }
    return known.get(value.lower(), value)


def smart_title(value: str) -> str:
    value = clean_space(value.replace("-", " "))
    words = []
    for word in value.split(" "):
        upper = word.upper()
        if upper in ACRONYMS:
            words.append(upper)
        elif re.fullmatch(r"\d+(ml|pc|pcs|m)", word.lower()):
            words.append(word.upper())
        else:
            words.append(word.capitalize())
    return " ".join(words)


def parse_price(value: str) -> Decimal | None:
    cleaned = re.sub(r"[^0-9.]", "", value or "")
    if not cleaned:
        return None
    try:
        return Decimal(cleaned).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None


def parse_inventory(value: str) -> int:
    match = re.search(r"-?\d+", value or "")
    if not match:
        return 0
    return max(0, int(match.group()))


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def normalize_sku(value: str, vendor: str, title: str, row_number: int) -> tuple[str, str | None]:
    raw = clean_space(value).upper().replace(" ", "-")
    if raw:
        return raw, None
    vendor_code = "".join(part[0] for part in re.findall(r"[A-Za-z]+", vendor))[:3].upper() or "SKU"
    title_code = "".join(re.findall(r"[A-Za-z0-9]+", title.upper()))[:8] or f"ITEM{row_number}"
    return f"{vendor_code}-{title_code}-{row_number:03d}", "Generated missing SKU"


def infer_category(title: str, category: str) -> str:
    haystack = f"{title} {category}".lower()
    for normalized, keywords in CATEGORY_RULES:
        if any(keyword in haystack for keyword in keywords):
            return normalized
    return "General"


def build_tags(category: str, material: str, color: str) -> str:
    tags = [category.split(">")[-1].strip().lower()]
    for value in [material, color]:
        value = clean_space(value).lower()
        if value:
            tags.append(value)
    return ", ".join(dict.fromkeys(tags))


def build_body(title: str, material: str, color: str, notes: str) -> str:
    details = []
    if material:
        details.append(f"Material: {clean_space(material)}")
    if color:
        details.append(f"Color: {clean_space(color)}")
    if notes:
        details.append(clean_space(notes))
    body = ". ".join(details)
    return f"<p>{title}. {body}</p>" if body else f"<p>{title}.</p>"


def transform_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    output_rows = []
    notes = []
    seen_skus = Counter()

    for idx, row in enumerate(rows, start=1):
        title = smart_title(row["supplier_title"])
        vendor = clean_vendor(row["vendor"])
        sku, sku_note = normalize_sku(row.get("sku", ""), vendor, title, idx)
        seen_skus[sku] += 1
        price = parse_price(row.get("price", ""))
        inventory = parse_inventory(row.get("inventory", ""))
        category = infer_category(title, row.get("category", ""))
        handle = slugify(f"{vendor}-{title}")

        cleanup_notes = []
        if sku_note:
            cleanup_notes.append(sku_note)
        if seen_skus[sku] > 1:
            cleanup_notes.append("Possible duplicate SKU")
        if price is None:
            cleanup_notes.append("Price requires manual review")
        if inventory == 0:
            cleanup_notes.append("Inventory is zero")

        status = "active" if price is not None and inventory > 0 else "draft"
        price_text = f"{price:.2f}" if price is not None else ""
        material = clean_space(row.get("material", ""))
        color = clean_space(row.get("color", ""))
        notes_text = clean_space(row.get("notes", ""))

        output_rows.append(
            {
                "Handle": handle,
                "Title": title,
                "Body (HTML)": build_body(title, material, color, notes_text),
                "Vendor": vendor,
                "Product Category": category,
                "Type": category.split(">")[-1].strip(),
                "Tags": build_tags(category, material, color),
                "Published": "TRUE" if status == "active" else "FALSE",
                "Option1 Name": "Title",
                "Option1 Value": "Default Title",
                "Variant SKU": sku,
                "Variant Inventory Qty": str(inventory),
                "Variant Price": price_text,
                "SEO Title": f"{title} | {vendor}",
                "SEO Description": f"Shop {title} from {vendor}. Clean product data prepared for ecommerce import.",
                "Status": status,
                "Cleanup Notes": "; ".join(cleanup_notes),
            }
        )

        if cleanup_notes:
            notes.append(f"- Row {idx}: {title} -> {'; '.join(cleanup_notes)}")

    return output_rows, notes


def write_report(rows: list[dict[str, str]], notes: list[str]) -> None:
    active = sum(1 for row in rows if row["Status"] == "active")
    draft = len(rows) - active
    categories = Counter(row["Product Category"] for row in rows)

    lines = [
        "# Product Cleanup Report",
        "",
        "## Summary",
        "",
        f"- Input rows processed: {len(rows)}",
        f"- Active products ready for import: {active}",
        f"- Draft products needing review: {draft}",
        f"- Rows with cleanup notes: {len(notes)}",
        "",
        "## Category Split",
        "",
    ]
    lines.extend(f"- {category}: {count}" for category, count in categories.most_common())
    lines.extend(["", "## Manual Review Notes", ""])
    lines.extend(notes or ["- No manual review notes."])
    lines.extend(
        [
            "",
            "## Suggested Next Step",
            "",
            "Review draft products, confirm missing prices, then import `cleaned_shopify_products.csv` into Shopify.",
        ]
    )

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with INPUT_FILE.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    output_rows, notes = transform_rows(rows)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    write_report(output_rows, notes)
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {REPORT_FILE}")


if __name__ == "__main__":
    main()
