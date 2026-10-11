# Repository-reviewed blog publishing

The existing `BlogPost` database model, published-only routes, Markdown renderer,
sitemap and admin workflow remain in place. Repository content adds a reviewed
publishing path, not an unauthenticated API or replacement CMS.

## Create a guide

Add matching `content/blog/<slug>.md` and `<slug>.json` files on a branch. The
Markdown starts below the H1: the template renders the title. These are trusted,
code-reviewed files; embedded HTML follows the existing Markdown renderer. Do not
put customer data, private links, tracking tokens or external scripts in them.

The JSON must contain exactly these fields:

```json
{
  "schema_version": 1,
  "slug": "website-content-review-checklist",
  "title": "Website content review checklist",
  "description": "A useful, accurate search description.",
  "tags": "content review, website maintenance",
  "author": "Staleaway",
  "content_sha256": "<lowercase SHA256 of the exact UTF-8 Markdown bytes>",
  "expected_previous_sha256": null
}
```

Compute the content hash with `sha256sum content/blog/<slug>.md`. Publishing
requires a reviewed PR, appropriate tests and the normal merge/deploy path. No
new publishing credential is needed. Run `make test` (Docker only). CI also
renders public fixtures into the `public-blog-preview` artifact after tests;
serve its directory locally and inspect the homepage, blog and guide on desktop
and mobile before merging. The preview uses an in-memory test database, not any
production or customer data. It validates manifests, then seeds the desired
publications as fixtures even when a revision names a previous digest. This
checks desired rendering, **not** production history or whether an update can
apply to existing rows; the production publisher retains that guard. Its
publication timestamp is a preview timestamp.

## Deployment and verification

The web entrypoint runs `publish_repository_blog` after migrations and before
Gunicorn. Workers do not run it. A publication error prevents the **new** web
container from starting; inspect logs and correct the branch rather than bypass
these checks. Existing CapRover deployment behavior determines whether the prior
healthy container continues serving; verify it rather than assume. A successful
CI preview is not proof of a successful production publication.

The command validates all manifests before applying changes atomically. It
serializes blog writes in PostgreSQL during the brief transaction, because the
legacy schema does not enforce unique slugs. It assigns a stable repository-owned
UUID, rejects unrelated same-slug or UUID collisions (including drafts), and
requires the full existing public-record digest for changes. Identical content
is a no-op: neither `created_at` nor `updated_at` is reset. Actual publication
dates come from database creation, not a planned date in a content file.

Only repository-owned posts receive the Staleaway organization byline. Existing
articles retain their existing author attribution. BlogPosting and breadcrumbs
are rendered for posts; the five-step HowTo is scoped to the approved repository
checklist and must stay consistent with its visible instructions.

After deploy, verify HTTP 200, canonical, body, links, dates, article/schema
rendering and sitemap inclusion, plus desktop/mobile screenshots. The homepage
checklist link appears only while that slug is published. The existing postdeploy
IndexNow workflow handles changed public URLs; do not add daily resubmissions.

## Update an existing repository post

1. Use the prior successful `publication_sha256` from deployment output as
   `expected_previous_sha256`. It is a SHA256 of the exact JSON serialization of
   all public fields, as defined in `core.blog_publishing.publication_digest`.
   It is not the Markdown-only hash. No private customer data is printed.
2. Edit the Markdown/metadata and update `content_sha256`.
3. Review, test, merge and verify the resulting deployment as above.

The previous digest is a single approved transition, not a wildcard or a history
of acceptable states. A manual editorial modification, image change, slug move,
unrelated collision or withdrawal to draft stops automated updates. Investigate
and reconcile explicitly; do not copy a digest blindly to force an overwrite.
`make manage publish_repository_blog --dry-run` can validate on a local stack
without writes. Read deployment state through approved operator access when
production diagnosis is needed; do not expose an admin key in a URL.

## Withdrawal and rollback

Removing a manifest does **not** delete or unpublish the database row. A missing
or empty `content/blog` directory is an explicit no-op and does not block web
startup, including after the last manifest is removed. Present malformed
manifests still fail closed. A code rollback does not undo a publication. If a post needs withdrawal, explicitly use
the existing admin workflow to set it to draft, then remove or reconcile its
manifest in the same authorized change. The publisher refuses to auto-republish
a repository post that has been moved to draft, even with a matching prior hash.
An older code image containing a different manifest will fail the digest guard
instead of silently undoing newer editorial content. Coordinate corrective
publication through a new reviewed commit; never restore a database backup over
current customer data.
