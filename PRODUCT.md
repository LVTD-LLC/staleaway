# Product

Staleaway is a website maintenance reminder app for humans.

The core workflow is sitemap import → scheduled email → review link → reviewed page.
Users can set daily/weekly/monthly cadence, pages per email, timezone, preferred time,
and additional email recipients. The dashboard lists sitemaps and their pages.
Billing uses PR #8's monthly/yearly Stripe checkout and billing portal.

The October 2026 restoration removes later agent APIs, agency tiers and client grouping.
Database metadata from those versions is preserved but not exposed as active product behavior.
See docs/pr8-restoration.md for the exact baseline and compatibility exceptions.
