To find your website sitemap, try your domain followed by `/sitemap.xml`, check `/robots.txt` for a `Sitemap:` address, or open your CMS’s sitemap settings. Then check whether that address lists pages or links to other sitemap files. Choose the public pages you want to review before importing the list into Staleaway.

You can follow these steps without a Staleaway account. You need a browser and a website you manage; CMS access helps if the common locations do not work. The goal is a usable list for human content reviews.

**The short version:**

1. Find the sitemap address.
2. Identify an XML page list or index.
3. Choose the review scope.
4. Check import readiness with the worksheet below.
5. Import and verify listed pages.

**Jump to:** [Find the address](#find-sitemap-address) · [Read the XML](#read-sitemap-xml) · [Choose the scope](#choose-review-scope) · [Reconcile your inventory](#reconcile-review-inventory) · [Check readiness](#check-import-readiness) · [Verify the import](#verify-imported-pages)

<h2 id="find-sitemap-address">1. Find the sitemap address</h2>

Start with the public domain visitors actually use. Add `/sitemap.xml` to it: for the illustrative domain `example.com`, that would be `https://example.com/sitemap.xml`. If it opens, keep the full address, including any final destination after a redirect. A familiar filename is a starting point, not proof that the response is a sitemap.

If you get a missing-page message, open `/robots.txt` on the same domain. Look for a line beginning `Sitemap:` and open the address after it. There may be more than one. This declaration is part of the [Sitemaps protocol](https://www.sitemaps.org/protocol.html); its absence does not prove that the site has no sitemap.

Still nothing? Use the CMS or SEO plugin’s own settings. They are a better source than trying a long list of guessed filenames.

### Common sitemap locations by platform

**WordPress core:** try `/wp-sitemap.xml`. WordPress introduced that default index in [WordPress 5.5](https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/). An SEO plugin or site setting can change what is available, so this is not a universal address for every WordPress installation.

**WordPress with Yoast SEO:** open Yoast SEO → Settings → Site features. Under Technical SEO, find XML sitemaps and use **View the XML sitemap**. [Yoast’s instructions](https://yoast.com/help/xml-sitemaps-in-the-wordpress-seo-plugin/) show that route. Its usual index is `/sitemap_index.xml`; following the settings link avoids confusion when another address redirects there.

**Shopify:** open `/sitemap.xml` at your store’s domain. [Shopify generates this file](https://help.shopify.com/en/manual/promoting-marketing/seo/find-site-map) and links separate sitemaps for content such as products, collections, pages and blog posts. A password-protected or private store may prevent access. Do not remove privacy controls merely to make an import work.

**Webflow:** check `/sitemap.xml`. If it is missing, inspect Site settings → SEO → Sitemap. [Webflow’s auto-generation instructions](https://help.webflow.com/hc/en-us/articles/33961355371667-Create-a-sitemap-in-Webflow) require enabling the setting, saving and publishing; a project may instead use a custom sitemap. Check with whoever maintains the site before changing that configuration.

Platform documentation checked October 13, 2026. Confirm the address on your own site. If you do not manage its settings, ask the maintainer for the public XML sitemap URL rather than changing plugins or search-visibility settings to experiment.

<h2 id="read-sitemap-xml">2. Identify an XML page list or index</h2>

A browser may show raw XML, a styled table, or a notice that the XML has no style information. None of those appearances alone tells you whether the file is usable. Look at what its entries point to.

A **page sitemap** has a `urlset` containing `url` entries. Each entry’s `loc` gives a page address. A **sitemap index** has a `sitemapindex` containing `sitemap` entries; those `loc` values point to other sitemap files. The [Sitemaps XML protocol 0.9](https://www.sitemaps.org/protocol.html) defines both structures. These small examples follow that specification; `example.com` is an illustrative domain, not an import target.

**An index points to a sitemap file:**

    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <sitemap>
        <loc>https://example.com/help-sitemap.xml</loc>
      </sitemap>
    </sitemapindex>

**A page list points to a content page:**

    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>https://example.com/help/change-address</loc>
      </url>
    </urlset>

The outer element is the quick clue. In the first example, open the linked XML file to see the next level. In the second, the link already identifies a page to review.

<figure>
<svg viewBox="0 0 400 370" width="100%" role="img" aria-labelledby="find-your-website-sitemap-flow-title find-your-website-sitemap-flow-desc" style="max-width:400px;height:auto;display:block;margin:auto;color:var(--sa-ink)">
<title id="find-your-website-sitemap-flow-title">Follow the index to the pages you want to review</title>
<desc id="find-your-website-sitemap-flow-desc">An optional sitemap index links to child sitemap files. A selected child page list contains public page addresses. Check those addresses against the records that actually appear after import.</desc>
<rect x="12" y="10" width="376" height="66" rx="16" fill="var(--sa-night)" />
<text x="200" y="37" text-anchor="middle" fill="white" font-size="19" font-weight="bold">Sitemap index</text>
<text x="200" y="60" text-anchor="middle" fill="white" font-size="16">Links to sitemap files, not page records</text>
<path d="M200 76V106 M193 98L200 106L207 98" stroke="var(--sa-purple)" stroke-width="2" fill="none" />
<rect x="12" y="108" width="376" height="66" rx="16" fill="var(--sa-lavender)" />
<text x="200" y="135" text-anchor="middle" fill="currentColor" font-size="19" font-weight="bold">Selected page sitemap</text>
<text x="200" y="158" text-anchor="middle" fill="currentColor" font-size="16">Lists the public pages in your review scope</text>
<path d="M200 174V204 M193 196L200 204L207 196" stroke="var(--sa-purple)" stroke-width="2" fill="none" />
<rect x="12" y="206" width="376" height="66" rx="16" fill="var(--sa-lavender)" />
<text x="200" y="233" text-anchor="middle" fill="currentColor" font-size="19" font-weight="bold">Background import</text>
<text x="200" y="256" text-anchor="middle" fill="currentColor" font-size="16">Check which page records actually appeared</text>
<path d="M200 272V302 M193 294L200 302L207 294" stroke="var(--sa-purple)" stroke-width="2" fill="none" />
<text x="200" y="327" text-anchor="middle" fill="currentColor" font-size="18" font-weight="bold">A human still needs to review the content.</text>
<text x="200" y="354" text-anchor="middle" fill="currentColor" font-size="14">Staleaway · October 2026</text>
</svg>
<figcaption>An index leads to a page list. If your address already opens a page list, start at the second box.</figcaption>
</figure>

For a public example, open [Staleaway’s sitemap](/sitemap.xml). At this guide’s publication it uses `urlset`, with `loc` entries for public pages such as the blog. Look for the page addresses inside its `loc` entries.

An index is not an error. Staleaway’s importer follows XML sitemap indexes, but large, deeply nested or partly unavailable indexes can produce an incomplete list. Start with a relevant child if that makes your list easier to inspect.

<h2 id="choose-review-scope">3. Choose the review scope</h2>

Before copying the address into an app, decide what you want to maintain. “Our public help articles” is a useful scope. “Every URL that exists” may include archives, product variants or other pages you do not intend to review in this pass.

Open a few representative entries. Do they reach the live pages you expected? If an index separates blog posts from products, inspect the child file for the section you need. Choosing that child is a manual choice of input, not a filtering feature inside Staleaway.

Shopify’s separate content sitemaps illustrate why this matters: a shop owner reviewing buying guides might start with the blog list rather than the full store index. A WordPress editor should likewise check the entries, rather than assume a file with “post” in its name contains every page they care about.

<h3 id="reconcile-review-inventory">Reconcile the sitemap with your review inventory</h3>

A **content inventory** is your own record of content you intend to maintain. It can be broader than a public sitemap. [Tulane’s content-audit guidance](https://communications.tulane.edu/drupal-guide/web-content-management/content-audit) recommends checking CMS content and navigation alongside the sitemap. The [University of Oregon’s audit guide](https://digital.uoregon.edu/project-kickoff/content-audit) also separates collecting page addresses from evaluating their content. Sources checked October 22, 2026.

Keep three lists distinct: your intended review inventory, the page addresses in the XML you selected, and the records that actually appear after import. Compare addresses, not just totals. Equal counts can hide different pages. Start with a manageable section; a sample check is not evidence that the whole inventory matches.

**Use the difference to choose the next action:**

- An intended public page is missing from the selected XML: check another relevant child sitemap, then ask the maintainer whether the omission is intentional. Absence alone does not mean the page is broken or unindexed.
- A draft or private page belongs in your review inventory but not in public XML: keep its record in a restricted system and review it there. Do not publish private addresses or credential-bearing links to make an import look complete.
- A public address is in the selected XML but absent from imported records: note the exact input and check time, then investigate with the maintainer. A child fetch failure or traversal limit can leave a partial import. Repeatedly adding the same sitemap does not establish coverage.
- The XML includes sections outside this review: choose a more relevant child before adding it. If you already imported it, inspect what appeared before changing anything. Choosing a different input does not automatically remove existing records or keep them synchronized with the new list.

### Copyable mismatch record

Use this in your own notes, **not as a Staleaway form or automatic report**. Keep restricted identifiers and access details out of public or broadly shared records.

> **Public page address, or a restricted internal reference:**<br>
> **In my intended inventory: yes / no / uncertain:**<br>
> **In the selected XML: yes / no / not checked:**<br>
> **In imported records: yes / no / not checked:**<br>
> **Exact XML input and checked date:**<br>
> **Intended visibility and difference found:**<br>
> **Person responsible for the next action:**<br>
> **Next action and next check date:**<br>
> **Result verified, or still unresolved:**

**Fictional example:** a help editor includes a draft refund policy in a restricted inventory. It is intentionally unpublished, so its absence from public XML needs no sitemap repair. The editor keeps its review in the existing CMS workflow.

The same editor finds a published delivery guide in the selected help XML but cannot find its address in Staleaway’s imported list. They record the input, missing public address and check date, assign a maintainer to investigate, and set a follow-up date. They check the actual records again before marking the missing-page issue resolved. Opening an XML file is not that verification.

<h2 id="check-import-readiness">4. Check import readiness</h2>

Staleaway needs the full address of an XML sitemap. A homepage, an HTML directory of links, and a `robots.txt` file are not interchangeable with that input. Use an uncompressed XML sitemap URL; do not assume a downloadable `.gz` file is supported.

Open the chosen address without relying on your CMS login. A sign-in screen, password prompt, access-denied response or HTML error page means you have not yet confirmed a usable public XML input. If you are unsure what the response contains, ask the maintainer rather than sharing access tokens or disabling protection.

### Copyable import-readiness worksheet

This is a **manual worksheet for your notes**, not a Staleaway feature or an automatic validation report.

> **Website I manage:**<br>
> **Full sitemap URL and where I found it:**<br>
> **Checked on:**<br>
> **Public XML without signing in: yes / no / uncertain:**<br>
> **File type: page list / index / uncertain:**<br>
> **Child sitemap checked, if applicable:**<br>
> **Content I intend to review:**<br>
> **Representative public page addresses found:**<br>
> **Important omissions or unwanted sections:**<br>
> **Decision: try this input / choose a narrower child / ask the maintainer:**<br>
> **After importing: which expected pages actually appeared?**<br>
> **Unresolved issue and next action:**

If you cannot tell whether the address opens XML, ask your site maintainer before importing. Check that a narrower list still contains the pages you need.

After importing, use the [mismatch record](#reconcile-review-inventory) for expected pages that did not appear. Keep the readiness check separate from the later content review: opening a sitemap does not check the facts on its pages.

<h2 id="verify-imported-pages">5. Import and verify listed pages</h2>

To use the list for reminders, [create a free Staleaway account](/accounts/signup/) or sign in to your existing account. In the dashboard, enter the full XML address in **Sitemap URL** and choose **Add Sitemap**. Import runs in the background. Open the sitemap entry and check which intended pages appeared.

**A successful add is not proof that every page was imported.** A fetch or XML error in one child can leave a partial list, and traversal limits can stop a broad index. There is no promised completion time. If the list stays empty or differs from the input, recheck the public XML and the selected child with your site maintainer; do not keep adding duplicate entries to test whether waiting helped.

Then choose the pages per review email and a daily, weekly or monthly cadence. The [Staleaway workflow](/#how-it-works) brings pages to your attention; it does not certify them as accurate. Reminders select unreviewed pages rather than guaranteeing that every page is covered within a particular interval.

Not sure how much review time to set aside? Use the free [content review workload planner](/tools/content-review-planner) with the number of pages you intend to check. You can compare a smaller batch with more review sessions before choosing your own plan. The estimate stays separate from your reminder settings.

When a reminder arrives, opening **Review This Page** marks the page reviewed before redirecting you to it. That recorded action is not proof that you checked its claims or finished an edit. Use the [website content review checklist](/blog/website-content-review-checklist) to inspect the content, record a decision and verify any fix in your own publishing system.

### Common mistakes to avoid

- **Pasting a page’s address instead of its sitemap address.** A page address belongs inside the inventory; the import field needs the XML file that lists it.
- **Treating `lastmod` as a review date.** The protocol uses it for modification metadata. It does not establish that someone checked the facts.
- **Assuming a healthy XML response means a complete import.** Check the actual page list afterward; file discovery and application processing are different steps.
- **Changing search or privacy settings to force an import.** Resolve the intended public input with the maintainer. Content review is not a reason to expose private material.

## Questions before you start

### Does having a sitemap mean my pages are indexed?

No. Google says a sitemap does not guarantee crawling or indexing. A content review also needs a human check of the page itself.

Google’s [sitemap overview](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) explains the distinction. This guide helps you find a review input, not diagnose an indexing failure.

### Can I use my homepage or robots.txt URL instead?

No. Find the XML sitemap address first. Staleaway imports the supplied sitemap; it does not discover it from a homepage or a robots.txt file.

### Will Staleaway review or rewrite the pages for me?

No. Staleaway sends review reminders. You check the content and make changes in your own publishing system.

Find the right list, verify what arrived, and start with a page you can review carefully.
