# Content-review guide and repository publishing

- Target: https://staleaway.com/blog/website-content-review-checklist
- Growth purpose: help website owners turn a reminder into a concrete human review, then choose whether the free sitemap-reminder workflow fits.
- The guide uses explicitly fictional service/event/how-to cases, a manual review log, and code-verified reminder limitations. No customer data or outcome statistics are published.
- Publication path: reviewed Markdown and a checked manifest, slug/UUID ownership and previous-record digest guards, idempotent dates, no schema migration or customer-data changes.
- Homepage and published blog index provide discovery. Existing postdeploy IndexNow remains unchanged.
- Shipping requires independent editorial/code review, Docker-backed CI, rendered preview, normal merge/deploy and live verification. PR state is not deployed state.
- Private evidence, shortlist, baselines, run status and outcome dates remain in the existing Rowset observations dataset identified in config.json. Run key: staleaway:daily-seo:2026-10-11.
- Follow-up: privacy-safe signup-to-first-reminder success measurement, not pageview-based conversion claims.
