#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAD_TRACKER = ROOT / "lead_tracker.csv"

BATCHES = {
    "send_batch_01_20260603.md": ["L0101", "L0109", "L0102", "L0104", "L0110"],
    "send_batch_02_20260603.md": [
        "L0131",
        "L0129",
        "L0125",
        "L0124",
        "L0116",
        "L0121",
        "L0128",
        "L0118",
        "L0126",
        "L0130",
    ],
}


def load_draft_module():
    module_path = ROOT / "scripts" / "generate_outreach_drafts.py"
    spec = importlib.util.spec_from_file_location("generate_outreach_drafts", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load draft generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_leads() -> dict[str, dict[str, str]]:
    with LEAD_TRACKER.open(newline="", encoding="utf-8") as file:
        return {row["lead_id"]: row for row in csv.DictReader(file)}


def contact_route(row: dict[str, str]) -> str:
    return row.get("contact_email") or row.get("contact_page") or row.get("website") or "Needs research"


def send_method(row: dict[str, str]) -> str:
    if row.get("contact_email"):
        return "Gmail"
    return "Website/contact form"


def signed_message(message: str) -> str:
    signature = """Best,
scatenatolenoxo9246-hash
Async Automation Developer
Portfolio: https://scatenatolenoxo9246-hash.github.io/async-automation-portfolio/"""
    if "Portfolio: https://scatenatolenoxo9246-hash.github.io/async-automation-portfolio/" in message:
        return message
    return f"{message.rstrip()}\n\n{signature}"


def write_batch(filename: str, lead_ids: list[str]) -> None:
    drafts = load_draft_module()
    leads = load_leads()
    lines = [
        f"# {filename.replace('_', ' ').replace('.md', '').title()}",
        "",
        "No messages have been sent. This is a copy/paste-ready queue for the user's real Gmail, LinkedIn, or website contact forms.",
        "",
        "Recommended use: send 5 messages per day at most. Keep the rest for tomorrow or after replies.",
        "",
        "After sending any lead, update `lead_tracker.csv`:",
        "",
        "- `status`: `contacted`",
        "- `last_touch_date`: `2026-06-03`",
        "- `next_followup_date`: `2026-06-06`",
        "- `next_action`: `Follow up if no reply`",
        "",
    ]

    for index, lead_id in enumerate(lead_ids, start=1):
        row = leads[lead_id]
        subject = row.get("outreach_subject") or drafts.subject_for(
            row.get("segment", ""),
            row.get("service_angle", ""),
        )
        message = signed_message(row.get("outreach_message") or drafts.message_for(row))
        route = contact_route(row)
        lines.extend(
            [
                f"## {index}. {row['company']}",
                "",
                f"- Lead ID: {lead_id}",
                f"- Score: {row['score']}",
                f"- Send method: {send_method(row)}",
                f"- Contact route: `{route}`",
                f"- Source: `{row['source_url']}`",
                f"- Angle: {row['service_angle']}",
                "",
                "Copy this email:",
                "",
                "```text",
                f"To: {route}",
                f"Subject: {subject}",
                "",
                "Body:",
                "",
                message,
                "```",
                "",
                "Subject only:",
                "",
                "```text",
                subject,
                "```",
                "",
                "Body only:",
                "",
                "```text",
                message,
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## If They Reply \"Send Examples\"",
            "",
            "Use:",
            "",
            "```text",
            "Sure. Here are three short examples:",
            "",
            "1. Shopify product feed cleaner: messy supplier CSV to Shopify-ready output with review notes.",
            "2. Sales lead follow-up automation: lead scoring, next actions, and email draft generation.",
            "3. Support FAQ assistant prototype: searchable FAQ answers with handoff notes.",
            "",
            "Portfolio: https://scatenatolenoxo9246-hash.github.io/async-automation-portfolio/",
            "",
            "If helpful, I can also suggest a small paid test scope based on one workflow from your current client work.",
            "```",
            "",
        ]
    )

    (ROOT / filename).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {ROOT / filename}")


def main() -> None:
    for filename, lead_ids in BATCHES.items():
        write_batch(filename, lead_ids)


if __name__ == "__main__":
    main()
