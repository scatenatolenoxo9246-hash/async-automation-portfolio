#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAD_TRACKER = ROOT / "lead_tracker.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_FILE = OUTPUT_DIR / "outreach_drafts.md"


def clean(value: str | None) -> str:
    return (value or "").strip()


def first_name(contact_name: str) -> str:
    if not contact_name:
        return "[Name]"
    return contact_name.split()[0]


def subject_for(segment: str, service_angle: str) -> str:
    text = f"{segment} {service_angle}".lower()
    if "shopify" in text:
        return "Extra async help for Shopify product data cleanup"
    if "zapier" in text or "make" in text or "airtable" in text or "automation" in text:
        return "Async implementation support for automation projects"
    if "marketing" in text or "website" in text or "webflow" in text:
        return "Small automation support for agency client work"
    return "Extra async implementation support"


def message_for(row: dict[str, str]) -> str:
    name = first_name(clean(row.get("contact_name")))
    company = clean(row.get("company")) or "your team"
    segment = clean(row.get("segment"))
    signal = clean(row.get("public_signal")) or clean(row.get("custom_opening_line")) or "your client work"
    custom_opening = clean(row.get("custom_opening_line"))
    opening_line = custom_opening or f"I saw that {company} works on {signal}."
    angle = clean(row.get("service_angle")) or "data cleanup and automation support"
    text = f"{segment} {angle}".lower()

    if "shopify" in text:
        body = f"""Hi {name},

{opening_line}

I am a China-based developer helping small agencies with async implementation work: product CSV cleanup, supplier catalog normalization, Shopify import-ready files, bulk edit workflows, and small scripts.

If you ever have overflow work, I can start with a small paid test task so you can check quality, turnaround, and written communication before committing to anything larger.

Would it be useful if I sent 2-3 short examples of the kind of work I can support?"""
    elif any(word in text for word in ["zapier", "make", "airtable", "automation"]):
        body = f"""Hi {name},

{opening_line}

I am a China-based developer who can support automation consultants with async implementation tasks: API scripts, webhook helpers, CSV cleanup, Google Sheets workflows, and client handoff notes.

If you ever have implementation overflow, I can start with a small paid test task. Written requirements are best for me, and I can send clean files plus a short handoff note.

Would you like me to send a few short examples?"""
    else:
        body = f"""Hi {name},

{opening_line}

I am a China-based developer helping small agencies with async implementation work: form-to-sheet cleanup, CRM data preparation, recurring reports, small API scripts, and FAQ/support assistant prototypes.

If a client asks for small technical workflow work outside your main scope, I can help as a quiet implementation partner. I am happy to start with a small paid test task first.

Would it be useful if I sent over 2-3 relevant examples?"""

    return body


def load_rows() -> list[dict[str, str]]:
    with LEAD_TRACKER.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    sections = ["# Outreach Drafts", ""]
    count = 0

    for row in rows:
        status = clean(row.get("status"))
        if status not in {"not_contacted", "draft_ready", ""}:
            continue

        company = clean(row.get("company")) or "Unknown company"
        score = clean(row.get("score")) or "not scored"
        subject = clean(row.get("outreach_subject")) or subject_for(
            clean(row.get("segment")),
            clean(row.get("service_angle")),
        )
        message = clean(row.get("outreach_message")) or message_for(row)

        sections.extend(
            [
                f"## {company}",
                "",
                f"- Lead ID: {clean(row.get('lead_id'))}",
                f"- Segment: {clean(row.get('segment'))}",
                f"- Score: {score}",
                f"- Website: {clean(row.get('website'))}",
                f"- Contact route: {clean(row.get('contact_page')) or clean(row.get('contact_email')) or 'Needs research'}",
                "",
                f"Subject: {subject}",
                "",
                message,
                "",
                "---",
                "",
            ]
        )
        count += 1

    OUTPUT_FILE.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Drafts generated: {count}")


if __name__ == "__main__":
    main()
