# Staleaway

Scheduled page review reminders for your website. Add a sitemap, choose a cadence,
and receive pages to revisit in your inbox.

- Site: https://staleaway.com
- Repository: https://github.com/LVTD-LLC/staleaway

## Development

Copy `.env.example` to `.env` and configure local settings. Never commit secrets.
Run `make serve` for the local Docker stack, `make migrate` for a new development
database, and `make shell` for Django's shell. Frontend watch mode is `npm run watch`.

## Tests

```sh
npm ci --include=dev
npm run build
docker compose -f docker-compose-test.yml build
make test
```

Tests run in a network-isolated container. External providers are mocked.

## Deployment

Main-branch GitHub workflows deploy the existing `staleaway` and `staleaway-workers`
CapRover apps. Production keeps its existing database, media bucket, Redis queue,
credentials and volumes. Do not recreate storage during a branding/code change.

Email uses configurable `DEFAULT_FROM_EMAIL`, `MAILGUN_SENDER_DOMAIN`, and `MJML_URL`.
All features are free. No payment-provider credentials or webhook setup are needed.
Historical billing columns remain inert to preserve existing records; there is no runtime integration.

## Product baseline

The app restores the behavior shipped in PR #8, with Staleaway branding and a
Firefox-inspired presentation. It does not include the subsequent agency/agent
features. Existing database fields and migrations remain intact to preserve data.

- [Restoration and rollback](docs/pr8-restoration.md)
- [Domain cutover](docs/staleaway-cutover.md)
- [Design](DESIGN.md)
- [Technology](TECH.md)
