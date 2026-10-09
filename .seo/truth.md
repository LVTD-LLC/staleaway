# Product truth — verified 2026-10-09

- Free access, no checkout or paid plans: PRODUCT.md, VISION.md and restored routes.
- Sitemap import, scheduled email reminders and human review links: core/forms.py, core/tasks.py, core/views.py.
- Daily, weekly and monthly cadence: core/choices.py ReviewCadence; per-sitemap page count and delivery settings in core/forms.py.
- Review links mark a page reviewed and redirect to its URL; this is not proof the person completed a substantive audit: core/views.py review_page_redirect.
- No claim of automatic content auditing, rewriting, broken-link detection, SEO ranking gains or AI product integrations is supported.
- Blog records have draft/published states. Public listing and detail must match the published-only sitemap contract.
- Legacy cleanapp database, queue, storage and migration names are compatibility identifiers, not stale public branding. Preserve them.
- Reminder delivery success was not end-to-end tested during this SEO run.
