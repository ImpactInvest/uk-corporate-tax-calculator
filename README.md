# UK Company Tax Calculator

A single-file, browser-based planning tool for a UK owner-managed limited company with a sole director. Model salary and dividend splits, see where every pound goes, and check when each liability falls due.

Open `UK Company Tax Calculator.dc.html` in a browser. No build step, no server, no dependencies beyond the bundled runtime.

## What it does

**Model** — Set revenue, expenses, employer pension, other personal income and a Plan 2 student loan toggle, then either solve for a target net take-home or fix the salary and dividends yourself. Outputs corporation tax, employer and employee NI, income tax, dividend tax and student loan, with a Sankey flow, a waterfall, bucket breakdowns and a payment calendar.

**Sensitivity** — A tornado chart ranking which inputs move take-home and effective tax rate most, a single-variable response curve, and a salary × pension heat map you can click to load into the model.

**Assumptions & sources** — Calculation order, 2025/26 and 2026/27 rate tables linked to gov.uk, timing rules, and what is deliberately out of scope.

## Rates

Covers 2025/26 and 2026/27. Corporation tax 19% to £50,000 with marginal relief to £250,000, 25% above. Plan 2 student loan 9% above £28,470 (2025/26) / £29,385 (2026/27), with dividends counted in full as unearned income once they exceed £2,000.

## Out of scope

Salary sacrifice, benefits in kind, the employment allowance, VAT, IR35 and off-payroll rules, the high income child benefit charge, Plan 1/4/5 and postgraduate loans, and reserves brought forward.

## Not advice

This is a planning aid, not tax advice. Check the figures against current HMRC guidance and your accountant before acting on them.
