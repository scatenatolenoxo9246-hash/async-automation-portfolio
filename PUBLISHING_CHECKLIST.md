# Publishing Checklist

This repository is ready to publish after the user provides the account and identity details below.

## Information needed from user

Required:

- GitHub username
- Repository name
- Repository visibility: public or private
- English display name for the portfolio
- Contact email shown on the portfolio

Optional but recommended:

- GitHub profile URL
- LinkedIn profile URL
- Whether GitHub Pages should be enabled
- Preferred portfolio URL style:
  - GitHub Pages repo site: `https://USERNAME.github.io/REPO_NAME/`
  - Custom domain later

## Local Git setup needed

Current machine status before publishing:

- GitHub CLI `gh` is not installed.
- Git user name is not configured in this repository yet.
- Git user email is not configured in this repository yet.
- No remote origin is configured yet.

Recommended path:

1. Install GitHub CLI.
2. Run `gh auth login`.
3. Provide the GitHub username, repo name, and visibility.
4. Set local Git identity:

```bash
git config user.name "YOUR_NAME"
git config user.email "YOUR_EMAIL"
```

5. Commit this clean repo.
6. Create/push the GitHub repository.
7. Enable GitHub Pages from the `main` branch root.

## Files to customize before publishing

Edit `index.html`:

- `Your Name`
- `your.email@gmail.com`
- `https://github.com/your-github-username`
- `https://www.linkedin.com/in/your-linkedin-slug/`

Edit `client-acquisition-pipeline/user_profile.md`:

- display name
- Gmail
- time zone
- technical stack
- availability
- portfolio/GitHub/LinkedIn links
- first-task pricing

## Validation already performed

- Homepage local asset and case-study links exist.
- Shopify product feed cleaner script runs.
- Sales lead follow-up script runs.
- Outreach draft generator runs.
