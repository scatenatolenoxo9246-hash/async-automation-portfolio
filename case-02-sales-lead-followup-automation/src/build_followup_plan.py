#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
PLAN_FILE = OUTPUT_DIR / "followup_plan.csv"
DRAFT_FILE = OUTPUT_DIR / "email_drafts.md"
TODAY = date(2026, 5, 31)


HIGH_FIT_INDUSTRIES = {
    "shopify agency",
    "automation agency",
    "ecommerce",
    "consulting",
    "real estate",
}

STAGE_POINTS = {
    "new": 10,
    "qualified": 24,
    "proposal": 32,
    "won": 0,
    "lost": 0,
}

SENTIMENT_POINTS = {
    "positive": 24,
    "neutral": 12,
    "cold": -4,
    "negative": -20,
}


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def parse_date(value: str) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def budget_points(value: str) -> int:
    if "1000-5000" in value or "1000-3000" in value:
        return 18
    if "500-2000" in value:
        return 14
    if "300-1000" in value:
        return 8
    return 4


def team_points(value: str) -> int:
    try:
        team_size = int(value)
    except ValueError:
        return 4
    if 5 <= team_size <= 20:
        return 12
    if team_size < 5:
        return 7
    return 8


def urgency_points(days_since_touch: int) -> int:
    if days_since_touch <= 2:
        return 18
    if days_since_touch <= 7:
        return 12
    if days_since_touch <= 14:
        return 6
    return -8


def next_action(stage: str, sentiment: str, days_since_touch: int, meeting_date: str) -> str:
    if meeting_date:
        return "Prepare meeting notes and confirm agenda"
    if stage == "proposal":
        return "Send concise proposal recap and ask for decision timeline"
    if sentiment == "positive" and days_since_touch <= 7:
        return "Send paid test task suggestion"
    if sentiment == "cold" or days_since_touch > 14:
        return "Send value-based reactivation follow-up"
    return "Send short diagnostic question"


def priority(score: int) -> str:
    if score >= 78:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"


def offer_angle(industry: str, pain_point: str) -> str:
    text = f"{industry} {pain_point}".lower()
    if "shopify" in text or "product" in text or "csv" in text:
        return "Shopify/product data cleanup"
    if "report" in text or "dashboard" in text:
        return "automated reporting workflow"
    if "faq" in text or "appointment" in text:
        return "support FAQ assistant prototype"
    if "lead" in text or "follow" in text:
        return "lead follow-up workflow"
    if "developer" in text or "capacity" in text:
        return "async implementation support"
    return "small workflow automation"


def email_draft(lead: dict[str, str], interaction: dict[str, str], action: str) -> str:
    first_name = lead["contact_name"].split()[0]
    angle = offer_angle(lead["industry"], lead["pain_point"])
    summary = interaction["last_message_summary"]

    return f"""Subject: Quick next step for {angle}

Hi {first_name},

Thanks again for sharing the context around {lead["pain_point"]}.

Based on your note about "{summary}", I think the fastest low-risk next step is a small paid test task around {angle}. That would let you check output quality, communication, and turnaround before committing to a larger workflow.

I can keep the first version very focused:
- confirm the input data or workflow
- clean/build one useful output
- send a short handoff note so your team can review it

Would you like me to suggest a small test scope for this?

Best,
"""


def build_plan() -> tuple[list[dict[str, str]], str]:
    leads = parse_csv(DATA_DIR / "leads.csv")
    interactions = {row["lead_id"]: row for row in parse_csv(DATA_DIR / "interactions.csv")}
    plan_rows = []
    draft_sections = ["# Follow-up Email Drafts", ""]

    for lead in leads:
        interaction = interactions.get(lead["lead_id"], {})
        last_touch = parse_date(interaction.get("last_touch_date", ""))
        days_since_touch = (TODAY - last_touch).days if last_touch else 999

        score = 0
        score += 18 if lead["industry"].lower() in HIGH_FIT_INDUSTRIES else 8
        score += STAGE_POINTS.get(lead["stage"].lower(), 6)
        score += SENTIMENT_POINTS.get(interaction.get("reply_sentiment", "").lower(), 0)
        score += budget_points(lead["budget_range"])
        score += team_points(lead["team_size"])
        score += urgency_points(days_since_touch)
        score = max(0, min(100, score))

        action = next_action(
            lead["stage"].lower(),
            interaction.get("reply_sentiment", "").lower(),
            days_since_touch,
            interaction.get("next_meeting_date", ""),
        )
        angle = offer_angle(lead["industry"], lead["pain_point"])

        plan_rows.append(
            {
                "priority": priority(score),
                "score": str(score),
                "lead_id": lead["lead_id"],
                "company": lead["company"],
                "contact_name": lead["contact_name"],
                "email": lead["email"],
                "country": lead["country"],
                "industry": lead["industry"],
                "pain_point": lead["pain_point"],
                "offer_angle": angle,
                "days_since_last_touch": str(days_since_touch),
                "recommended_next_action": action,
                "last_message_summary": interaction.get("last_message_summary", ""),
            }
        )

        draft_sections.extend(
            [
                f"## {lead['company']} ({priority(score)}, score {score})",
                "",
                email_draft(lead, interaction, action),
                "",
            ]
        )

    plan_rows.sort(key=lambda row: int(row["score"]), reverse=True)
    return plan_rows, "\n".join(draft_sections)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plan_rows, draft_text = build_plan()

    with PLAN_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(plan_rows[0].keys()))
        writer.writeheader()
        writer.writerows(plan_rows)

    DRAFT_FILE.write_text(draft_text, encoding="utf-8")
    print(f"Wrote {PLAN_FILE}")
    print(f"Wrote {DRAFT_FILE}")


if __name__ == "__main__":
    main()
