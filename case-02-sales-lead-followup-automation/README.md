# Case Study 02: Sales Lead Follow-up Automation

## Client scenario

A small agency or B2B service business has leads in spreadsheets, forms, and CRM exports. The team does not know who to follow up with first, what to say, or which leads are going cold.

## What this automation does

The script creates a simple follow-up command center.

It automatically:

- Scores leads by fit, urgency, and engagement
- Detects stale conversations
- Recommends the next action
- Writes personalized first-draft follow-up emails
- Exports a prioritized CSV and a markdown file with email drafts

## Files

- `data/leads.csv`: sample CRM-style lead export
- `data/interactions.csv`: sample recent touch history
- `src/build_followup_plan.py`: automation script
- `output/followup_plan.csv`: generated action plan
- `output/email_drafts.md`: generated email drafts

## Run

```bash
python3 src/build_followup_plan.py
```

Run this command from this case folder.

## Client value

This is useful for small agencies, consultants, local service companies, B2B SaaS teams, and founders who collect leads but lose revenue because follow-up is manual and inconsistent.
