# UK Company Tax Calculator

A browser-based planning tool for a UK owner-managed limited company with a sole director. Model salary and dividend splits, see where every pound goes, and check when each liability falls due.

**Live:** [impactinvest.github.io/uk-corporate-tax-calculator](https://impactinvest.github.io/uk-corporate-tax-calculator/)

Open `UK Company Tax Calculator.dc.html` in a browser to run it locally. No build step, no server, no dependencies beyond the bundled runtime.

## Feature requests

Use **Request a feature** on the site. Each request opens a GitHub issue with the `feature-request` label, so it is tracked in this repo and emailed to you if you [watch issues](https://github.com/ImpactInvest/uk-corporate-tax-calculator/subscription) on the repository.

Requesters can cancel before sending, or withdraw a filed request by closing the GitHub issue.

Work lands on `dev` first. Merge `dev` into `main` when you want a release; GitHub Pages deploys **only** from `main`.

When an issue is opened, GitHub Actions comments immediately and launches a Cursor cloud agent to triage it. If it is a concrete code change, the agent opens a **pull request against `dev` and stops**. Nothing is auto-merged, and nothing deploys until `dev` is merged into `main`.

To turn the bot on:

1. [Watch issues](https://github.com/ImpactInvest/uk-corporate-tax-calculator/subscription) on this repository (GitHub email as soon as something comes in).
2. Create a [Cursor API key](https://cursor.com/dashboard/api) and add it as the `CURSOR_API_KEY` repository secret.
3. Connect this repository in [Cursor Integrations](https://cursor.com/dashboard/integrations).
4. Optional: if the agent can push a branch but cannot open a PR, add a GitHub PAT with `issues` and `pull_requests` as `BOT_GH_TOKEN`.

Add the `bot-skip` label to keep an issue human-only. Re-run **Issue bot** from the Actions tab to retry.

## What it does

**Model** — Set revenue, expenses, employer pension, other personal income and a Plan 2 student loan toggle, then either solve for a target net take-home or fix the salary and dividends yourself. Outputs corporation tax, employer and employee NI, income tax, dividend tax and student loan, with a Sankey flow, a waterfall, bucket breakdowns and a payment calendar.

**Sensitivity** — A tornado chart ranking which inputs move take-home and effective tax rate most, a single-variable response curve, and a salary × pension heat map you can click to load into the model.

**Assumptions & sources** — Calculation order, 2025/26 and 2026/27 rate tables linked to gov.uk, timing rules, and what is deliberately out of scope.

## Rates

Covers 2025/26 and 2026/27. Corporation tax 19% to £50,000 with marginal relief to £250,000, 25% above — limits divided if you have associated companies. Plan 2 student loan 9% above £28,470 (2025/26) / £29,385 (2026/27), with unearned income counted in full once it exceeds £2,000.

## Out of scope

Salary sacrifice, benefits in kind, the employment allowance, VAT, IR35 and off-payroll rules, the high income child benefit charge, Plan 1/4/5 and postgraduate loans, and reserves brought forward.

## Disclaimer

This website is a planning tool for general information only. It is not tax, legal or accounting advice, and it is not a substitute for advice from a suitably qualified professional. Do not rely on the figures, or take or refrain from any action, without first consulting your own tax adviser, accountant or solicitor. Use of the site does not create a professional relationship, and no liability is accepted for loss arising from reliance on it.
