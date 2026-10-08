# IndexNow

Staleaway notifies https://api.indexnow.org/indexnow of its own public URLs.
The public `/indexnow-key.txt` ownership file is stable; no provider credential is required.
`/deployment.txt` identifies the server image revision and prevents notifications before rollout.

GitHub Actions runs after successful **Deploy Prod Server** and hourly at :19 UTC.
It reads `/sitemap.xml`, including published blog posts with full `updated_at` timestamps.
The public homepage, uses page, and blog listing are included; customer-imported sitemaps,
review links, account pages, and drafts are not submitted.
Deployments refresh all public URLs. Hourly runs notify observed additions, modifications,
and removals using a cached checkpoint; unchanged URLs are skipped. Failed batches leave
that checkpoint unchanged and retry at the next run. Requests have bounded timeouts,
retry transient failures, and respect short numeric Retry-After values; longer or unspecified
rate limits fail the run for later retry. Batches are limited to 10,000 URLs.

Manual run: Actions → IndexNow public URL changes → Run workflow.
Read-only preview (Python standard library only):

```
python3 scripts/indexnow.py --site-url https://staleaway.com --dry-run
```

The workflow's cache can be evicted: the next run resubmits current URLs but cannot
recover historical removals. Changes created and removed between scans are unobserved.
Bulk database edits that bypass `updated_at` need a deployment or manual CLI submission.
Blog list changes are refreshed at deployment; individual published articles are tracked hourly.
HTTP 200 means received, HTTP 202 means key validation pending—not confirmed indexing.
See https://www.indexnow.org/documentation for the protocol.

Validation: `docker compose -f docker-compose-test.yml build` then `make test`.
The Tests workflow performs both commands. No database migrations are introduced.
