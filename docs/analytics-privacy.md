# Acquisition measurement boundary

As of 2026-10-10, browser measurement is an explicit PostHog `$pageview` on
successful anonymous public pages only: homepage, blog index, technology page,
and published articles. Account, review, dashboard, sitemap, authenticated and
error pages have no browser analytics configuration. Missing configuration,
blocked storage, DNT/GPC, or a failed request means **unobserved**, not zero traffic.

The collector sends only the canonical public URL/path/host, a new random UUID,
a coarse allowlisted acquisition source, QA/known-bot flags and a measurement
version. Queries, fragments, arbitrary referrer domains, referrer paths, DOM,
form values, document titles, account identifiers and old PostHog cookies are
not sent. The new UUID namespace is intentionally not joined to old email-based
identities. Fetch omits credentials and sends no HTTP referrer.

This uses the official [PostHog capture endpoint](https://posthog.com/docs/api/capture),
checked 2026-10-10. It does not load the browser SDK or Plausible outbound-link
script. There is no browser replay, autocapture, pageleave or Web Vitals collection.
Those signals cannot be treated as measured after this boundary change.

`user_signed_up` is the only accepted event in the retained server task. It
uses a stable keyed HMAC rather than email/raw profile ID and a fixed property
set. The custom `AccountSignupView` is not wired into the current allauth URL
configuration; this repair does not establish live signup-event coverage.
Legacy queued payload properties are ignored;
`try_create_posthog_alias` remains a no-op for compatibility with queued jobs.
New jobs never queue the request cookie collection. Logfire no longer bypasses
its default cookie scrubbing. Existing historical data is not deleted or rewritten.

## Reading outcomes

- Filter `properties.$host = 'staleaway.com'` and
  `properties.measurement_version = 'public-v1'` for the new population.
- Exclude `is_qa = true` and `is_known_bot = true`; remaining traffic is not
  guaranteed human. Browser tests can also use `?staleaway_qa=1`.
- Treat the rollout as a measurement discontinuity. Do not compare old SDK
  autocapture/replay/session counts to the new pageview-only population.
- This does **not** join anonymous visits to account signups, verify live signup
  delivery, or establish first-reminder delivery or completed human reviews.
  Those activation measurements remain separate work.
- General diagnostic logging/error reporting is outside this bounded analytics
  repair; do not claim all telemetry has been audited.

## Verification

`npm run test:analytics` exercises collector privacy, stable IDs, malformed legacy
storage, known-referrer boundaries, QA flags, opt-outs and failed requests with
mocked network. Docker-backed `make test` covers rendered route exclusions,
published-only articles, legacy queued jobs and server signup properties.
Inspect actual browser requests after deployment using synthetic markers only.
