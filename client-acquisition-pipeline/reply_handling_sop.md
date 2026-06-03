# Reply Handling SOP

When a lead replies, paste the full reply into Codex with the lead row from `lead_tracker.csv`.

Use this format:

```text
Lead:
[paste lead row or company/context]

Customer reply:
[paste reply]

What I want:
Help me understand intent, risk, next reply, and whether to quote.
```

## Reply categories

### Category 1: asks for examples

Intent: interested but not ready.

Next action:

- Send portfolio link.
- Pick the most relevant case.
- Ask one diagnostic question.

Response goal:

> Move from curiosity to a concrete workflow or sample file.

### Category 2: asks for rate

Intent: budget check.

Next action:

- Avoid open-ended hourly quote at first.
- Suggest a small fixed-scope paid test.
- Ask for input file/workflow/deadline.

Response goal:

> Get enough context to propose a small paid first task.

### Category 3: shares a problem

Intent: strongest opportunity.

Next action:

- Restate the problem.
- Ask 3-5 scope questions.
- Suggest a small first deliverable.

Response goal:

> Create a paid test task proposal.

### Category 4: wants a call

Intent: possible opportunity, but risky if English speaking is weak.

Next action:

- Ask for written context before the call.
- Offer async-first process.
- If needed, keep call short and prepared.

Response goal:

> Move requirements into writing before committing.

### Category 5: asks for free sample work

Intent: possible free-work trap.

Next action:

- Offer to show existing samples.
- Offer a very small paid test.
- Do not complete custom production work for free.

Response goal:

> Keep trust-building without unpaid custom delivery.

### Category 6: not interested

Intent: close or nurture.

Next action:

- Reply politely once.
- Do not chase aggressively.
- Mark status as `closed_not_now`.

Response goal:

> Preserve reputation and move on.

## Clarifying questions by project type

### Data cleanup / CSV

Ask:

- What is the input file format?
- What should the final output look like?
- How many rows and columns?
- What are the rules for duplicates, missing fields, and manual review?
- Is this a one-time cleanup or recurring workflow?

### Shopify data workflow

Ask:

- Is this for a new import, migration, or bulk update?
- Do you already have a Shopify CSV template?
- How many products and variants?
- Which fields matter most: title, description, SKU, vendor, category, tags, images, SEO?
- What should be flagged for manual review?

### Zapier/Make/API automation

Ask:

- What tools are involved?
- What triggers the workflow?
- What data should move from tool A to tool B?
- Are API docs or sample payloads available?
- What should happen when an error occurs?

### FAQ/support prototype

Ask:

- Where are the current FAQs or support docs?
- What customer channels create repeated questions?
- Should the output be a website widget, internal tool, or knowledge-base draft?
- Is this just a prototype or a production integration?
- What topics should be escalated to a human?

## Output Codex should produce after each reply

For every meaningful customer reply, Codex should return:

- Chinese summary for the user
- Customer intent category
- Risk flags
- Recommended next move
- English reply draft
- Scope questions if needed
- Suggested price range if enough context exists
- Lead tracker update values

## Red flags

Stop and ask for caution if the customer:

- Requests fake reviews, spam, account creation, scraping private data, or bypassing platform limits.
- Wants access to sensitive systems without contract/payment clarity.
- Refuses written scope.
- Wants substantial custom work for free.
- Demands guaranteed revenue or SEO ranking outcomes.
- Pushes payment outside a safe channel before trust exists.
