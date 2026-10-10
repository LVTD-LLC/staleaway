# Technology

Staleaway uses Django 5, PostgreSQL, Django Q2/Redis, Django Allauth,
Anymail/Mailgun and a configured MJML HTTP renderer. The frontend is Django templates,
Stimulus, Tailwind and webpack. Production uses the existing CapRover web and worker
services and main-branch GitHub deployment workflows.

## Verification

- `npm ci --include=dev && npm run build`
- `docker compose -f docker-compose-test.yml build`
- `make test` (network-isolated Docker tests; SQLite test database)
- `make test core/tests/test_restoration.py`
- Check current PostgreSQL schema separately when restoring older code; unit tests skip core migrations.

Python requirements are exported from Poetry into requirements.txt for Docker builds.
No dependency/runtime upgrade is part of the restoration.

## Configuration

Use `.env.example`. Keep all credentials server-side. `SITE_URL` is the canonical
origin; `LEGACY_HOSTS` preserves old links. Email sender and Mailgun domain are
configurable. No payment-provider configuration is required.
Optional analytics/error-reporting integrations should remain optional.

Never rename existing database volumes, media buckets or queue identifiers to match
branding. The Django package is `staleaway`; the database app label stays `core`.
See docs/staleaway-cutover.md and docs/pr8-restoration.md.

Public acquisition analytics use a bounded capture-only PostHog collector; see
`docs/analytics-privacy.md` for exclusions and measurement limits. Run
`npm run test:analytics` for the network-mocked collector checks.
