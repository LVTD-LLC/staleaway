# Structure

- `staleaway/`: Django settings, routing, canonical-host middleware, storage/logging helpers.
- `core/models.py`: profiles, sitemaps, pages, email preferences, feedback and blog models.
- `core/migrations/`: complete historical schema; retained unchanged during restoration.
- `core/views.py`, `forms.py`: PR #8 dashboard, settings, page review and monthly/yearly checkout.
- `core/tasks.py`, `utils.py`: sitemap parsing, review email selection and scheduling.
- `core/stripe_webhooks.py`: subscription lifecycle handling.
- `core/api/`: session-authenticated UI helpers and the original admin blog endpoint.
- `core/tests/`: baseline behavior plus restoration, branding and compatibility regression tests.
- `frontend/templates/`: landing, app, account and email templates.
- `frontend/src/`: Stimulus controllers and shared `sa-*` styles.
- `frontend/vendors/`: original Staleaway mark and self-hosted licensed font.
- `deployment/`, `.github/workflows/`: existing web/worker builds and deploy entrypoints.
- `docs/pr8-restoration.md`: approved baseline, exact exceptions and rollback.

Additive model metadata from the later agent/agency versions remains dormant to
preserve data. The corresponding API/domain modules are intentionally removed.
