# Staleaway cutover

Public origin: `https://staleaway.com`. Repository: `LVTD-LLC/staleaway`.
Services: `staleaway`, `staleaway-workers`, `staleaway-postgres`, `staleaway-redis`.

## Data invariants

This rebrand does not change models, the `core` app label, migrations, user IDs,
passwords, API keys, subscriptions, or review links. Keep the existing `SECRET_KEY`,
Postgres database/user/password, volume names, Redis password, and provider keys.
Do not initialize a new database or create new production volumes.

For existing production configure BOTH web and worker:

- `SITE_URL=https://staleaway.com`
- `POSTGRES_HOST=srv-captain--staleaway-postgres`
- `REDIS_HOST=srv-captain--staleaway-redis`
- `AWS_S3_BUCKET_NAME=cleanapp-prod` (the actual existing bucket, not a new name)
- `Q_CLUSTER_NAME=cleanapp-q` (preserves signed/queued Django Q jobs)
- `LEGACY_HOSTS=pagefresh.lvtd.dev,cleanapp.dev,www.staleaway.com`
- `DEFAULT_FROM_EMAIL=Rasul from Staleaway <rasul@lvtd.dev>`
- `MAILGUN_SENDER_DOMAIN`: preserve a verified sending domain; do not assume a new domain is verified.
- `PLAUSIBLE_SITE_DOMAIN=pagefresh.lvtd.dev` until that existing analytics site is renamed.

All features are now free; former billing limit settings are unused. Storage/queue
defaults deliberately preserve legacy installations; new installations should set them explicitly.

## Ordered production procedure

1. Save private CapRover app definitions, service specs, and pinned image digests.
2. Take a custom-format `pg_dump`; restore it into a separate verification database.
   Compare user/profile/sitemap/page counts. Never print user records or credentials.
3. Build and test the renamed package in an isolated Docker container, without
   production secrets, network integrations, or production database access.
4. Add apex and www DNS records to the existing main server; attach both domains
   through CapRover and obtain TLS certificates before changing the canonical host.
5. Pause the web and worker during stateful service renames. Use CapRover's supported
   rename API, one service at a time. Keep existing volumes and database names.
   Confirm the old Postgres process has stopped before starting its replacement.
6. Update connection hostnames in both apps, rename web/worker, deploy the tested
   images, and resume one web and one worker instance. Update GitHub deployment
   tokens if needed; preserve all unrelated environment/configuration values.
7. Update Django Site #1 to `staleaway.com` / `Staleaway` without recreating it.
   Keep legacy domains serving existing links. Redirect safe GET/HEAD requests only;
   preserve POST request semantics. Payment webhooks were subsequently removed.
8. Verify HTTPS, login/signup forms, assets, API docs, worker startup, database/Redis
   connections, identical record counts, and unchanged volume mounts. Check email
   configuration without sending user mail. Payment routes are no longer exposed.

Existing login cookies cannot cross domains; users may need to log in again.
Their accounts, password hashes, API keys, and data remain unchanged.

## Rollback

Keep the pre-cutover dump and service snapshots private on the main host. Roll back
application images/configuration first; do not restore the dump over a live database
unless data corruption is confirmed and a separately approved recovery is needed.
The previous image can use the renamed database/Redis services by keeping the updated
connection hostnames. Restore the former SITE_URL and canonical routing if needed.
Never delete volumes as part of rollback. Existing self-hosted Compose/Render users
must retain resource and volume names when applying updated example configurations.
