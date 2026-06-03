# Lead Research Notes - 2026-06-03

This batch is intentionally small and manual. The purpose is to validate outreach quality before scaling.

## Source pools used

- Shopify Partner Directory
- Make Partner Directory
- Zapier Solution Partner Directory
- Webflow profiles and Made in Webflow pages

## Why these leads were selected

The first batch prioritizes public signals that match our delivery examples:

- Shopify migration and product/catalog setup
- Product and collection setup
- Large SKU or data migration language
- API, webhook, Make/Zapier/Airtable/Google Sheets implementation
- CRM and form-to-database automation
- FAQ/support assistant or AI-agent language

## First outreach hypothesis

Do not pitch broad "AI consulting."

Pitch one of these low-risk implementation angles:

1. Product CSV cleanup and Shopify import-ready files
2. Migration data cleanup/QA support
3. Webhook/API helper scripts
4. Google Sheets/Airtable data cleanup before automation
5. CRM/form-to-lead workflow cleanup
6. FAQ/support assistant prototype

## Rejected or lower-priority lead patterns

- Large agencies that explicitly say "fully in-house" or "never outsourced"
- Broad enterprise consultancies with procurement-heavy positioning
- Leads without any clear contact route
- Leads where the opening line would be generic

## Daily usage

1. Open `lead_tracker.csv`.
2. Pick 5 leads with score 78+.
3. Run `python3 scripts/generate_outreach_drafts.py`.
4. Review `output/outreach_drafts.md`.
5. Manually send from the user's real Gmail/LinkedIn/contact form.
6. Update `status`, `last_touch_date`, and `next_followup_date`.

## Important

No message has been sent. This file only supports manual review and user-controlled outreach.

## Batch 02 update

Added 16 more leads, bringing the tracker to 31 total leads.

Batch 02 focus:

- Shopify agencies with direct public emails and product/collection/migration signals.
- Make automation consultants with API, webhook, CRM, data migration, Airtable, Shopify, Google Sheets, or custom app signals.
- Lower priority given to large enterprise-heavy agencies unless the data/API overlap was strong.

Best new leads by fit:

- Fifty Tech Solutions: strong CRM, data migration, contact enrichment, custom API, Shopify/Airtable/Clay overlap.
- NEODELTA SAS: freelancer collective working on automation, SaaS products, API connections and Make scenario fixes.
- Meghbalika Tech: direct overlap with Shopify product/collection setup and product data transfer.
- ThePlanetSoft: Shopify migrations involving products, customers, orders, pages, and SEO data.
- Codify Infotech: product/collection setup, app setup, third-party code, landing pages, and troubleshooting.
- Rounders: boutique Shopify team with product setup, custom integrations, and WooCommerce data transfer experience.

Batch 02 send queue:

- `send_batch_02_20260603.md`
