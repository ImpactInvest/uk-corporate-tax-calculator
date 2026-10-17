# Sole Trader Income Calculator

A browser-based planning tool that shows how much a one-person UK business owner actually takes home, where every pound of tax goes, and when each bill falls due.

The tax model treats the business as an owner-managed **limited company with a sole director**: profit pays corporation tax, and the owner draws a mix of salary and dividends.

**Live site:** [impactinvest.github.io/uk-corporate-tax-calculator](https://impactinvest.github.io/uk-corporate-tax-calculator/)

> **Not advice.** This is a planning tool for general information only. See [Disclaimer](#disclaimer).

---

## At a glance

| | |
|---|---|
| **What it is** | A single-page tax and take-home calculator |
| **Who it is for** | Owners of one-person UK businesses, and their accountants |
| **Tax years** | 2025/26 and 2026/27 |
| **Tech** | One static HTML file plus a bundled runtime (`support.js`). React 18 and Babel load from unpkg at runtime |
| **Build step** | None |
| **Backend** | None. Inputs are saved in the visitor's browser (`localStorage`) |
| **Hosting** | GitHub Pages, deployed from `main` only |

## Quick start

**Use it online:** open the [live site](https://impactinvest.github.io/uk-corporate-tax-calculator/).

**Run it locally:**

```bash
git clone https://github.com/ImpactInvest/uk-corporate-tax-calculator.git
cd uk-corporate-tax-calculator
python3 -m http.server 8000
```

Then open <http://localhost:8000>. The root page redirects to the calculator. You can also open `Sole Trader Income Calculator.dc.html` directly in a browser. An internet connection is needed either way, because React, Babel and the fonts load from CDNs.

## What it does

The app has three tabs.

**Model.** Enter revenue, expenses, employer pension contributions, other personal income, and whether you repay a Plan 2 student loan. Then either:

- set a **target net take-home** and let the calculator find the dividends needed, or
- **fix salary and dividends** yourself.

It shows corporation tax, employer and employee National Insurance, income tax, dividend tax and student loan repayments, as a Sankey flow, a waterfall chart, bucket breakdowns, and a payment calendar based on your chosen accounting year-end.

**Sensitivity.** A tornado chart ranks which inputs move take-home and effective tax rate the most. A response curve shows one input at a time, and a salary × pension heat map lets you click any cell to load it into the model.

**Assumptions & sources.** The calculation order, the rate tables for both tax years (linked to gov.uk), the timing rules, and what is deliberately left out.

There is also a **Request a feature** button on every page. See [Feature requests](#feature-requests).

## Tax rules covered

| Item | 2025/26 | 2026/27 |
|---|---|---|
| Corporation tax | 19% up to £50,000, marginal relief to £250,000, 25% above | Unchanged |
| Associated companies | The £50,000 and £250,000 limits are divided between associated companies | Same |
| Dividend tax (basic / higher / additional) | 8.75% / 33.75% / 39.35% | 10.75% / 35.75% / 39.35% |
| Dividend allowance | £500 | £500 |
| Personal allowance | £12,570 | £12,570 |
| Employer NI | 15% above £5,000 | Same |
| Plan 2 student loan | 9% above £28,470 | 9% above £29,385 |

Unearned income counts in full towards the student loan once it exceeds £2,000. The source of truth for every rate is the `R` object near the top of the logic script in the calculator file.

## Out of scope

Salary sacrifice, benefits in kind, the employment allowance, VAT, IR35 and off-payroll rules, the high income child benefit charge, Plan 1, 4 and 5 and postgraduate loans, and reserves brought forward.

## Project structure

```text
.
├── Sole Trader Income Calculator.dc.html   # The whole app: markup, styles, logic, rate tables
├── support.js                              # Generated runtime that renders the .dc.html file. Do not edit
├── index.html                              # Redirects the site root to the calculator
├── favicon.svg / favicon.png               # Site icon
├── .nojekyll                               # Tells GitHub Pages to serve files as-is
├── .cursor/environment.json                # Cloud-agent dev server config (port 8000)
└── .github/
    ├── workflows/pages.yml                 # Deploys to GitHub Pages on push to main
    ├── workflows/main-from-dev.yml         # Blocks pull requests into main unless they come from dev
    ├── workflows/issue-bot.yml             # Triages new issues with a Cursor cloud agent
    ├── scripts/launch-issue-agent.py       # Starts that agent. It may open PRs but never merges
    └── ISSUE_TEMPLATE/feature_request.md   # Template for feature requests
```

### How the calculator file is organised

`Sole Trader Income Calculator.dc.html` is a self-contained component file read by `support.js`:

| Part | Where | What it holds |
|---|---|---|
| Page shell | `<head>` | Title, favicon, feature-request dialog styles |
| Template | `<x-dc>` … `</x-dc>` | The UI markup, with `{{ … }}` bindings to values and handlers |
| Logic | `<script type="text/x-dc" data-dc-script>` | Rate tables (`R`), palette, and a `Component` class with the tax maths (`ct`, `eeNI`, `erNI`, `sl`, `income`, `model`, `solveDividends`) and chart builders (`sankey`, `waterfall`, tornado, sweep, heat map) |
| Feature requests | Last plain `<script>` | Opens a pre-filled GitHub issue |

## Making changes

1. Branch from `dev`.
2. Edit `Sole Trader Income Calculator.dc.html`. Rates live in `R`, defaults in `Component.state`.
3. Run the local server and check the change in the browser, for both tax years.
4. Open a pull request into `dev`.
5. To release, open a pull request from `dev` into `main`. Merging it deploys the site.

**Rules**

- Work lands on `dev` first. Only `dev` may be merged into `main`, and a check enforces this.
- GitHub Pages deploys **only** from `main`.
- Do not edit `support.js` by hand. It is generated.
- Keep the `localStorage` key `uk-company-tax-v2` as it is. Changing it wipes every visitor's saved inputs.
- If you add a file the site needs, add it to the copy step in `.github/workflows/pages.yml`, or it will not be deployed.
- When a rate changes, update the `R` table, the **Assumptions & sources** tab, and the [Tax rules covered](#tax-rules-covered) table above.

## For AI agents

- **Entry point:** `Sole Trader Income Calculator.dc.html`. Nearly every change happens in this one file.
- **No build, no tests, no package manager.** Verify by serving the folder with `python3 -m http.server 8000` and loading the page.
- **Base branch:** `dev`. Never push to or open pull requests against `main`. Never merge, force-push or deploy.
- **Do not touch** `support.js` (generated) or the `localStorage` key.
- **Keep scope tight.** Change only what the task asks for, and keep the calculator's existing behaviour otherwise.
- **Issue bot:** new issues trigger `.github/workflows/issue-bot.yml`, which starts a Cursor agent with the rules in `.github/scripts/launch-issue-agent.py`.

## Feature requests

Use **Request a feature** on the site. Each request opens a GitHub issue with the `feature-request` label, so it is tracked in this repository. [Watch issues](https://github.com/ImpactInvest/uk-corporate-tax-calculator/subscription) to get an email when one comes in.

Requesters can cancel before sending, or withdraw a filed request by closing the issue.

### Issue bot

When an issue is opened, GitHub Actions comments on it and launches a Cursor cloud agent to triage it. If the issue is a concrete code change, the agent opens a **pull request against `dev` and stops**. Nothing is merged automatically, and nothing deploys until `dev` is merged into `main`.

To turn the bot on:

1. [Watch issues](https://github.com/ImpactInvest/uk-corporate-tax-calculator/subscription) on this repository.
2. Create a [Cursor API key](https://cursor.com/dashboard/api) and add it as the `CURSOR_API_KEY` repository secret.
3. Connect this repository in [Cursor Integrations](https://cursor.com/dashboard/integrations).
4. Optional: if the agent can push a branch but cannot open a pull request, add a GitHub token with `issues` and `pull_requests` access as `BOT_GH_TOKEN`.

Add the `bot-skip` label to keep an issue human-only. To retry, re-run **Issue bot** from the Actions tab.

## Disclaimer

This website is a planning tool for general information only. It is not tax, legal or accounting advice, and it is not a substitute for advice from a suitably qualified professional. Do not rely on the figures, or take or refrain from any action, without first consulting your own tax adviser, accountant or solicitor. Use of the site does not create a professional relationship, and no liability is accepted for loss arising from reliance on it.
