# 2026-10-16 — Connect review guides to the workload planner

- Add contextual planner links at the scheduling step of the review checklist and after sitemap-import guidance, so readers can choose a manageable manual review batch without creating an account.
- Keep both guides’ intent, titles, existing review workflow and planner calculations unchanged. Use exact previous-publication digests to preserve editorial safeguards; publication updates modification dates while retaining original publication dates.

# 2026-10-15 — Free content review workload planner

- Add a client-only whole-page review planner and a free tools hub, with homepage, blog and footer discovery. Calculate workload and target capacity without promising app coverage or completion dates.
- Keep planner inputs local: no upload, persistence, URL parameters, tool-use events or customer data. Add accessible validation, plain-text copy/download, reset, and a manual fallback for unavailable JavaScript.
- Add public canonical/schema/sitemap coverage, arithmetic and boundary regression tests, and planner preview artifacts. Preserve free access, existing privacy exclusions, reminder selection, storage and database behavior.

# 2026-10-14 — Sitemap setup help and visible validation

- Link the published sitemap-finding guide beside both sitemap inputs in a new tab without sending a referrer; clarify that saving a URL is not import confirmation.
- Keep invalid submissions visible for returning users and for first-time users who previously skipped onboarding; preserve entered values and associate help/errors with the input.
- Cover published-only help, ownership and validation recovery in isolated tests and render synthetic onboarding previews. No queue, billing, customer-data or analytics changes.

# 2026-10-13 — Find a sitemap and start a focused review list

- Publish a source-checked sitemap-finding guide with CMS starting points, an index-versus-page-list diagram, and a manual import-readiness worksheet. Explain import and reminder limits without indexing or completion promises.
- Add published-only homepage discovery, process/question structured data and publication regression coverage; retain the existing guarded blog publisher. Keep blog list markers inside the mobile column and wrap XML examples legibly.
- Replace the unsupported onboarding promise to process every page in under a minute with background-import guidance. No parser, queue, account, storage or billing behavior changes.

# 2026-10-12 — Measure real activation milestones safely

- Wire pseudonymous signup measurement to the active allauth signal, after commit, including social signups. Keep account and review pages free of browser analytics.
- Measure the first recorded reminder only after email-backend acceptance; a zero send result no longer creates a successful-send record. Preserve existing history, review selection, cadence and all-free access.
- Use fixed analytics properties and stable retry identities; analytics queue failure cannot fail signup or retry an accepted email. Document unobserved delivery, organic attribution and outage limits; add Docker-backed regression coverage.

# 2026-10-11 — Publish a practical content review checklist

- Add a repository-reviewed website content review guide and homepage discovery link, with an organization byline, visible publication date and article/process/breadcrumb structured data.
- Publish approved Markdown into the existing blog during web deployment. Guard against unrelated content, draft collisions and unapproved edits; preserve publication dates on repeat deployments. No database migration, worker, reminder or billing changes.
- Add Docker-backed publication/privacy-boundary checks and public-only preview artifacts for pre-merge visual review.

# 2026-10-10 — Bound acquisition analytics to public pages

- Replace browser SDK/autocapture/replay and duplicate outbound-link tracking with explicit anonymous public pageviews. Keep private/account/error pages out of browser analytics; never send URL queries, fragments, raw referrers or page contents.
- Keep signup outcome events with pseudonymous server IDs and fixed properties; stop cookie/email aliasing, including legacy queued jobs. Restore default cookie scrubbing in diagnostics.
- Add route, collector and queue regression checks. Document the measurement break and unverified activation attribution; preserve customer data, reminder behavior and all free features.

# 2026-10-09 — Preserve homepage hero spacing

- Shorten the SEO-refined hero sentence to preserve its original desktop line count and keep secondary links clear of decorative artwork. Search metadata is unchanged.

# 2026-10-09 — Public SEO foundations

- Add a sitemap-discovering robots.txt and descriptive homepage metadata.
- Link the blog and technology pages from public navigation; use the public layout for technology information and the current contact address. Remove unsupported AI-service descriptions.
- Enforce published-only blog listing/detail views; safely serialize article text in structured data and support posts without images.
- Use the configured site origin for public canonical URLs; add regression coverage and sanitized SEO foundations.

## 2026-10-08 — IndexNow
- Add public ownership proof and revision-verified post-deploy/hourly sitemap notifications with retries and success-only checkpoints.
- Correct public sitemap homepage (exclude login-only dashboard), include only published blog entries, and preserve full modification timestamps.
- Add Docker-backed CI coverage. No database, billing, review queue, or email changes.

# Changelog

## 2026-10-07

- Move the default and production Mailgun sending domain to `mg.staleaway.com`, preserving the Staleaway From address, reply forwarding and suppressions. Document paired domain/key configuration and safe delivery verification.

# 2026-10-04 — Staleaway email sender

- Default transactional and review-reminder emails to `Rasul from Staleaway <rasul@staleaway.com>`, using the dedicated Mailgun domain. Environment overrides remain supported.
- Existing accounts use the same global sender; no account or preference migration is required.

# Free access — 2026-10-04

- Make every feature free, with no pricing page, checkout, subscription controls or payment-status messaging.
- Remove Stripe SDK, webhook handling, billing settings, API/controller and local CLI service.
- Replace the admin billing metric with users who have sitemaps; retain all existing data and schema history.
- Verify sitemap import, scheduling settings, recipients and page reviews across all historical account states.

# 2026-10-04 — PR #8 restoration and Firefox-inspired design

- Restore the PR #8 sitemap/email review product and monthly/yearly billing; remove later agent/agency workflows.
- Use Staleaway branding with a purple, condensed-type, rounded-card visual system inspired by the supplied Firefox reference.
- Preserve existing users, additive database fields/migrations, media, queue and Staleaway hosting/email compatibility.

<!-- Types of changes -->
**Added** for new features.
**Changed** for changes in existing functionality.
**Deprecated** for soon-to-be removed features.
**Removed** for now removed features.
**Fixed** for any bug fixes.
**Security** in case of vulnerabilities.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2026-10-04]
### Changed
- Rebranded PageFresh / Cleanapp to Staleaway at https://staleaway.com across UI, email, API documentation, Python package, and deployment configuration.
- Made media bucket, queue name, and analytics site explicit environment settings so existing data and queued work survive the rename. Legacy billing-limit environment names remain supported.
- Added a data-preserving cutover and rollback runbook.

## [Unreleased]
### Added
- `Skip onboarding` option

### Changed
- Default PageFresh sender email now resolves from `DEFAULT_FROM_EMAIL` with a
  `rasul@lvtd.dev` fallback.

### Removed
- djstripe
