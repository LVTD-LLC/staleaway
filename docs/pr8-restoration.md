# PR #8 restoration (2026-10-04)

Requested baseline: merge `37c7e3b9b323330bc1c5e14f68139c3a52053e18`.

Restore PR #8's sitemap setup, dashboard, settings, random unreviewed-page email selection, review links, session API, and monthly/yearly Stripe checkout. Remove the later agent review API, agency tiers, client grouping and deterministic queue modules. This is a forward commit, not a history rewrite.

## Deliberate compatibility exceptions

- Keep the `staleaway` package, deployment targets, canonical host middleware, environment-based email sender and existing media/queue names from the domain cutover.
- Retain models' additive fields and migrations 0014–0017 unchanged. These fields are dormant in the restored workflows; they preserve existing data and provide defaults for inserts into the current database. Never reverse migrations or drop those columns to make the source look older.
- Keep the Docker-isolated test harness and canonical-domain/sender tests.
- Do not restore API-key logging from the old code. Keep the subscription-deletion empty-string fix required by the existing non-null schema.
- Branding, templates and styles use Staleaway. Pricing copy describes this product, not the unrelated image-service boilerplate present in PR #8.
- New Firefox-inspired presentation does not introduce new product features.

## Verification / deployment

Build frontend assets, run `make test` in an isolated Docker environment, check `makemigrations --check --dry-run` with migrations enabled, and test on a disposable restored database. No new migration is expected. Deployment uses the existing GitHub workflows and Staleaway services. Existing database, media, queue and secrets must not change.

Rollback is redeploying image tag `cfd34068941da44ef810824b9597bfd6b6c0e3b8` for web and worker. No database rollback is necessary. Do not restore an old database over current users.
