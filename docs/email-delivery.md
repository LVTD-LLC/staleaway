# Staleaway email delivery

The Mailgun sending domain is `staleaway.com`. Web and worker use
`MAILGUN_SENDER_DOMAIN=staleaway.com` and
`DEFAULT_FROM_EMAIL=Rasul from Staleaway <rasul@staleaway.com>`.
Use a domain-scoped Mailgun sending key, never a shared account-admin key.
The production credential and sender configuration are stored in Infisical:
`Openclaw` / `prod` / `/services/mailgun-staleaway`.

Account confirmation/password-reset emails and scheduled page-review emails use
this global sender for existing and newly created accounts. User email preferences,
review cadence and stored content are not changed by sender configuration.

Cloudflare hosts SPF, 2048-bit DKIM, Mailgun MX/tracking, and monitoring-mode DMARC.
The exact address `rasul@staleaway.com` forwards through Mailgun to Rasul's existing
`rasul@lvtd.dev` inbox, including user replies and app feedback.

Keep Mailgun domain suppression entries for existing app recipients when moving
from an old domain. Never clear bounces, complaints or unsubscribe records to make
a delivery test pass. A domain verification/accepted API response alone does not
prove delivery; verify a controlled message through the production Django backend.
