# Async Automation Developer Portfolio

This repository is a publish-ready portfolio and client acquisition kit for overseas small-business automation services.

## Live Portfolio

The portfolio homepage is `index.html`. It can be published directly with GitHub Pages from the repository root.

Before publishing, replace placeholders in `index.html`:

- `Your Name`
- `your.email@gmail.com`
- `https://github.com/your-github-username`
- `https://www.linkedin.com/in/your-linkedin-slug/`

## Case Studies

- `case-01-shopify-product-feed-cleaner`: Shopify-ready product data cleanup example.
- `case-02-sales-lead-followup-automation`: CRM lead scoring and follow-up draft generation example.
- `case-03-support-faq-assistant`: static support FAQ assistant prototype.

## Client Acquisition Pipeline

The `client-acquisition-pipeline` folder contains:

- lead sourcing playbook
- lead tracker CSV
- ICP scorecard
- outreach templates
- reply handling SOP
- pricing and offer structure
- delivery handoff SOP

## Local Checks

Run the Python examples:

```bash
cd case-01-shopify-product-feed-cleaner
python3 src/clean_product_feed.py

cd ../case-02-sales-lead-followup-automation
python3 src/build_followup_plan.py
```

Generate outreach drafts:

```bash
cd client-acquisition-pipeline
python3 scripts/generate_outreach_drafts.py
```
