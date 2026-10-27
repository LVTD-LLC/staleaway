# Acquisition measurement boundary

As of 2026-10-10, browser measurement includes an explicit PostHog `$pageview` on
successful anonymous public pages only: homepage, blog index, technology page,
published articles, and (from 2026-10-15) the free tools hub and content review
planner. Planner inputs and outputs stay in the browser; no tool-use events or
values are collected, saved or added to URLs. Account, review, dashboard, sitemap,
authenticated and error pages have no browser analytics configuration. Missing configuration,
blocked storage, DNT/GPC, or a failed request means **unobserved**, not zero traffic.

The collector sends only the canonical public URL/path/host, a new random UUID,
a coarse allowlisted acquisition source, QA/known-bot flags and a measurement
version. Queries, fragments, arbitrary referrer domains, referrer paths, DOM,
form values, document titles, account identifiers and old PostHog cookies are
not sent. The new UUID namespace is intentionally not joined to old email-based
identities. Fetch omits credentials and sends no HTTP referrer.

This uses the official [PostHog capture endpoint](https://posthog.com/docs/api/capture),
rechecked 2026-10-27. It does not load the browser SDK or Plausible outbound-link
script. There is no browser replay, autocapture, pageleave or Web Vitals collection.
Those signals cannot be treated as measured after this boundary change.

## Public signup intent (2026-10-27)

Anonymous public pages also emit `public_signup_cta_clicked` with
`measurement_version = 'public-cta-v1'` for trusted primary-button or keyboard
clicks on the same-origin `/accounts/signup/` link, including nested icons and
modified primary clicks. It uses the same anonymous UUID and bounded properties
as public pageviews. Only the canonical **source page** is sent: no destination,
link text, placement, DOM attributes, query, fragment or form/tool values.
Links with destination parameters/fragments or credentials are ignored.
There is no listener on private/authenticated/error pages; DNT/GPC and route
configuration are rechecked on each click. Navigation is never blocked or delayed
for analytics, and missing/failed requests remain unobserved.

Filter the production host, exact event/version and exclude `is_qa = true` and
`is_known_bot = true`. Remaining events are not guaranteed human. Counts are
clicks, not signups or unique people; use distinct anonymous IDs for visitor
counts. Same-page pageview/click IDs support public discovery diagnostics, but
are deliberately **not joined to account identities**. A click does not prove
that signup loaded, an account was created, a reminder was accepted, or a human
review happened. Do not call this an organic activation funnel or infer lift.
Browser QA intercepts capture requests; it does not create production accounts
or send reminders. Actual eligible click ingestion remains a separate readback.

## Server activation measurement (2026-10-12)

The real allauth `user_signed_up` signal queues `user_signed_up` after the database
transaction commits, for password and social account creation. It is not a form
submission, login or email-verification event. The retained custom signup view
has no second measurement hook.

`first_review_reminder_accepted` is eligible only after `email.send()` returns one
accepted message and the existing `EmailSent` record is saved. The task verifies
that this is the account's earliest recorded send, including pre-rollout history.
A zero return or provider exception creates neither a send record nor an event.
This is **email-backend acceptance, not inbox delivery, an open, or a completed
human review**. Existing historical records are not rewritten or backfilled;
old records may include the previous implementation's unchecked send result.

Both events use `measurement_version = 'activation-v1'`, the same stable keyed
HMAC account identity, fixed non-identifying properties, the original event time,
and a deterministic keyed event UUID. Queue retries therefore reuse the event
identity rather than inventing another milestone. Signup uses account creation
time; the reminder uses the first send record's time. No email, raw profile/send
ID, private page URL, review-link token, cookie, DOM or provider payload is sent.
Legacy queued `properties` and `source_function` arguments are ignored. Anonymous
public visitors are deliberately not joined to these account identities.

Analytics is optional: missing configuration disables it. Enqueue failures are
logged without payloads and do not fail signup or retry an already accepted email.
The PostHog SDK has bounded transport retries; failed SDK enqueue raises in the
analytics job. There is no durable analytics outbox, so an outage or process loss
can leave outcomes unobserved. A successful queue call is not ingestion proof.
SDK runtime metadata may accompany these events; no request scope is supplied.

`try_create_posthog_alias` remains a no-op for compatibility with queued jobs.
Logfire retains default cookie scrubbing. Historical analytics is not deleted.

Contracts checked against [allauth signals](https://docs.allauth.org/en/latest/account/signals.html)
(installed allauth 64.2.1), [Django email](https://docs.djangoproject.com/en/5.1/topics/email/),
and [PostHog 5.4.0 capture source](https://github.com/PostHog/posthog-python/blob/v5.4.0/posthog/client.py).

## Reading outcomes

- Filter `properties.$host = 'staleaway.com'` and
  `properties.measurement_version = 'public-v1'` for the new population.
- Exclude `is_qa = true` and `is_known_bot = true`; remaining traffic is not
  guaranteed human. Browser tests can also use `?staleaway_qa=1`.
- Treat the rollout as a measurement discontinuity. Do not compare old SDK
  autocapture/replay/session counts to the new pageview-only population.
- Read server outcomes separately with the same production host and
  `measurement_version = 'activation-v1'`. Count distinct pseudonymous accounts;
  cohort signups on or after deployment and pair their later first-reminder events.
  Use an explicit observation window and allow for each user's chosen cadence.
  Do not divide all reminders by unrelated signups or combine this with the old
  `public-v1` or `public-cta-v1` population. Compare only mature cohorts.
- This does **not** join anonymous visits to account signups or attribute activation
  to organic search, an article or an AI referrer. A real production event readback
  is still needed before declaring live coverage. Do not create customer signups
  or send test email merely to manufacture an analytics observation.
- No server event identifies QA or known bots yet. Report that limitation for
  account cohorts; browser QA/bot flags apply only to public pageviews. A successful
  signup is not proof of a human, a verified email address or a qualified user.
- General diagnostic logging/error reporting is outside this bounded analytics
  repair; do not claim all telemetry has been audited.

## Verification

`npm run test:analytics` exercises collector privacy, stable IDs, malformed legacy
storage, known-referrer boundaries, QA flags, opt-outs and failed requests with
mocked network. Docker-backed `make test` covers rendered route exclusions,
published-only articles, legacy queued jobs, the real signup route, transaction
rollback, first-send ownership, backend rejection, analytics outages and retry
identities. All test email/provider/analytics calls are mocked or local-only.
Inspect actual browser requests after deployment using synthetic markers only.
