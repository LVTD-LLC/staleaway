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
