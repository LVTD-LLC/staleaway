# Product truth — verified 2026-10-09

- Free access, no checkout or paid plans: PRODUCT.md, VISION.md and restored routes.
- Sitemap import, scheduled email reminders and human review links: core/forms.py, core/tasks.py, core/views.py.
- Daily, weekly and monthly cadence: core/choices.py ReviewCadence; per-sitemap page count and delivery settings in core/forms.py.
- Review links mark a page reviewed and redirect to its URL; this is not proof the person completed a substantive audit: core/views.py review_page_redirect.
- No claim of automatic content auditing, rewriting, broken-link detection, SEO ranking gains or AI product integrations is supported.
- Blog records have draft/published states. Public listing and detail must match the published-only sitemap contract.
- Legacy cleanapp database, queue, storage and migration names are compatibility identifiers, not stale public branding. Preserve them.
- Reminder delivery success was not end-to-end tested during this SEO run.

## Review email recipients — checked 2026-11-04

- Review emails use the owning profile's enabled `EmailPreference` addresses. When at least one is enabled, the account address is not automatically added; with none enabled, delivery falls back to `profile.user.email`. Disabling or removing every listed address is not a pause control. Source: `core/tasks.py:send_page_email_to_profile`.
- Recipient choices remain separate from inbox receipt or completed human review. The settings clarification changes no recipient selection, scheduling, PR8 review behavior or analytics. Verify the protected template using isolated synthetic fixtures, never a customer account or a real email send.

## Sitemap-start guidance — checked 2026-10-13

- The initial importer fetches the supplied XML URL and follows sitemap indexes with bounded recursion; it does not discover sitemap URLs from a homepage or robots.txt. Source: core/tasks.py process_sitemap_pages.
- Sitemap creation queues background import. A successful add does not establish complete import or a duration guarantee. Child fetch/parse errors and traversal guards can leave a partial list. Source: core/signals.py and core/tasks.py.
- Use an uncompressed XML sitemap input; raw gzip-file decoding is not implemented. Do not confuse HTTP transport decompression with file-format support.
- Reminder selection uses random unreviewed pages. Cadence is not a guarantee that every page is reviewed or re-reviewed at that interval. Source: core/tasks.py.
- These are code-verified boundaries, not a claim of live customer import or email-delivery testing.
