# Launch Checklist

This is the exact order to launch the outbound pipeline.

## Step 1: User fills profile basics

Open `user_profile.md` and replace:

- `[Your English display name]`
- `[your Gmail]`
- `[your time zone]`
- technical stack levels
- GitHub URL if available
- LinkedIn URL if available
- minimum small paid test price

If LinkedIn or GitHub does not exist yet, leave it as `not ready`.

## Step 2: Portfolio status

Portfolio is already published:

- Portfolio page: `https://scatenatolenoxo9246-hash.github.io/async-automation-portfolio/`
- GitHub repo: `https://github.com/scatenatolenoxo9246-hash/async-automation-portfolio`
- Contact email: `scatenatolenoxo9246@gmail.com`

## Step 3: First lead batch

Start with 30 leads:

- 10 Shopify agencies
- 10 Zapier/Make/Airtable automation consultants
- 10 small marketing/website agencies

For each lead, fill at least:

- `lead_id`
- `company`
- `segment`
- `country`
- `website`
- `source_url`
- `contact_page`
- `public_signal`
- `pain_guess`
- `service_angle`
- `score`
- `status`
- `custom_opening_line`

Set `status` to `not_contacted`.

## Step 4: Generate message drafts

Run:

```bash
cd "/Users/apple/Documents/New project/overseas_client_acquisition_pipeline"
python3 scripts/generate_outreach_drafts.py
```

Open:

`output/outreach_drafts.md`

Review each draft before sending.

## Step 5: Send only 5-10 messages per day

Use:

- Gmail
- LinkedIn
- Contact forms
- Upwork only if the lead is already on Upwork

Do not send hundreds of messages.

## Step 6: Paste replies back to Codex

Use this format:

```text
Lead:
[company, website, segment, service angle, message sent]

Customer reply:
[paste reply]

Please help me:
1. Translate and summarize.
2. Judge intent and risk.
3. Write the next English reply.
4. Suggest scope questions.
5. Suggest price if possible.
```

## Step 7: Convert to paid test task

Do not jump into a big project.

Push toward:

- 1 clear input
- 1 clear output
- 1-3 day timeline
- fixed price
- one revision

Use `pricing_and_offers.md` and `delivery_handoff_sop.md`.

## What the user should send Codex now

Send these six items:

1. English display name
2. Gmail address to show clients
3. Development stack and comfort level
4. Weekly available hours
5. Whether written English chat is acceptable with Codex help
6. Preferred first service: Shopify data cleanup, CRM/lead automation, scripts/API automation, or FAQ assistant prototype

After that, Codex can personalize the profile, portfolio text, offer wording, and first-batch lead strategy.
