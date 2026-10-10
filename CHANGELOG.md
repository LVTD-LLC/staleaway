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
