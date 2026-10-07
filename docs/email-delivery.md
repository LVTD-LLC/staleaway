# Staleaway email delivery

The Mailgun sending domain is `mg.staleaway.com`. Web and worker use
`MAILGUN_SENDER_DOMAIN=mg.staleaway.com` and
`DEFAULT_FROM_EMAIL=Rasul from Staleaway <rasul@staleaway.com>`.
Use a domain-scoped Mailgun sending key, never a shared account-admin key.
The production credential and sender configuration are stored in Infisical:
`Openclaw` / `prod` / `/services/mailgun-staleaway`.

Account confirmation/password-reset emails and scheduled page-review emails use
this global sender for existing and newly created accounts. User email preferences,
review cadence and stored content are not changed by sender configuration.

Cloudflare hosts SPF, 2048-bit DKIM and Mailgun MX/tracking for `mg.staleaway.com`.
Root DMARC retains monitoring mode with relaxed SPF/DKIM alignment so the
root-domain From address aligns with the authenticated sending subdomain.
Open/click tracking remains disabled.
The exact address `rasul@staleaway.com` forwards through Mailgun to Rasul's existing
`rasul@lvtd.dev` inbox, including user replies and app feedback.

Keep Mailgun domain suppression entries for existing app recipients when moving
from an old domain. Never clear bounces, complaints or unsubscribe records to make
a delivery test pass. A domain verification/accepted API response alone does not
prove delivery; verify a controlled message through the production Django backend.

## Sending-subdomain cutover (2026-10-07)

Both CapRover apps (`staleaway` and `staleaway-workers`) must use the subdomain
and its own domain-scoped sending key; changing only the domain with the old
root-domain key will fail. Update the corresponding Infisical values together.
Keep the root Mailgun domain and MX records for incoming reply forwarding and
legacy event history; new application mail must use `mg.staleaway.com`.
The existing 76 bounce and 2 complaint suppressions were copied and verified
on the new domain; there were no unsubscribe entries at cutover.

Verify a controlled email from each running Django service and check delivery,
SPF, DKIM and DMARC at the receiving mailbox. Do not call the reminder task for
this smoke test: it writes `EmailSent` and changes the next reminder's eligibility.
Rollback requires restoring the previous domain and its matching sending key
together on both services and in Infisical. Do not delete the old domain, keys,
or DNS records during the cutover.
