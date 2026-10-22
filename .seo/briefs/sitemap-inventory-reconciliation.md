# Sitemap guide: inventory reconciliation

## Purpose and scope

Improve the existing sitemap guide, not create another inventory or checklist URL.
Keep its title, description, original publication date and five-step structure.
This is a useful setup handoff, not a title experiment or an asserted ranking win.

Information gain: distinguish a person's intended inventory, the selected XML
entries and actual imported records, then give each mismatch a responsible person,
next action and unresolved/verified result. Replace the earlier generic example
with two clearly fictional cases that require different actions.

## Checked sources — October 22, 2026

- [Tulane: Conduct a Website Content Audit](https://communications.tulane.edu/drupal-guide/web-content-management/content-audit): combine CMS/navigation/sitemap inputs; an inventory may include unpublished content. Owner and follow-up fields support an actionable record.
- [University of Oregon: Content Audit](https://digital.uoregon.edu/project-kickoff/content-audit): collect addresses from an XML export or manual discovery, then evaluate the content. Inventory is not evaluation.
- [Google: Sitemaps overview](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview): sitemap inclusion does not guarantee crawling or indexing.
- Product source: `core/tasks.py` sitemap traversal and exact-URL record creation; `core/views.py` owned sitemap page listing; `PRODUCT.md` and the existing guide. Background import, traversal limits and fetch/XML failures do not establish complete membership. No manual-page-import, automatic reconciliation, section-filtering or synchronization claim.

The mismatch record is Staleaway's suggested manual framework, not terminology
attributed to the universities and not an application feature. Fictional cases
are not customer experience or a measured benchmark. Existing analytics cannot
support a public first-party statistic about inventory mismatches; no private
customer records or production aggregate were accessed to manufacture one.

## Counter-evidence and boundaries

The existing page already explained omissions and partial imports. Another
generic checklist would add little. Only the per-item next-action record and
different-cause examples justify this expansion. A separate comparison tool is
not yet supported by evidence of repeated need. Do not infer keyword volume,
import success, indexing failure or growth lift from this research.

Private research/measurement/reservations remain in the existing Rowset history
dataset identified by `.seo/config.json`; run `staleaway:daily-seo:2026-10-22`.
Keep private references restricted; do not expose credential-bearing URLs to
public sitemaps, shared notes, analytics or replay. No new event capture or form.

## Verification and publishing contract

Use the existing exact-publication-digest transition, PR review and Docker-backed
CI. Before merge, inspect the CI-rendered guide, jump links, existing diagram,
manual record and fictional cases at mobile/desktop widths under both OS color
preferences. Check server-rendered text, schema, two existing inbound sources
(homepage and blog), outbound links and no overflow. After deployment, verify
the exact revision, actual body, original publication date, modification date,
canonical, indexability and sitemap lastmod. Do not resubmit healthy URLs.

Keep earlier outcome windows; later diagnostic reads overlap the original
guide and October 16 planner-discovery change, so they are not causal proof.
