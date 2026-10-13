To find your website sitemap, try your domain followed by `/sitemap.xml`, check `/robots.txt` for a `Sitemap:` address, or open your CMS’s sitemap settings. Then check whether that address lists pages or links to other sitemap files. Choose the public pages you want to review before importing the list into Staleaway.

You can follow these steps without a Staleaway account. You need a browser and a website you manage; CMS access helps if the common locations do not work. The goal is a usable list for human content reviews, not a promise that Google has indexed everything in it.

**The short version:**

1. Find the sitemap address.
2. Identify an XML page list or index.
3. Choose the review scope.
4. Check import readiness with the worksheet below.
5. Import and verify listed pages.

## 1. Find the sitemap address

Start with the public domain visitors actually use. Add `/sitemap.xml` to it: for the illustrative domain `example.com`, that would be `https://example.com/sitemap.xml`. If it opens, keep the full address, including any final destination after a redirect. A familiar filename is a starting point, not proof that the response is a sitemap.

If you get a missing-page message, open `/robots.txt` on the same domain. Look for a line beginning `Sitemap:` and open the address after it. There may be more than one. This declaration is part of the [Sitemaps protocol](https://www.sitemaps.org/protocol.html); its absence does not prove that the site has no sitemap.

Still nothing? Use the CMS or SEO plugin’s own settings. They are a better source than trying a long list of guessed filenames.

### Common sitemap locations by platform

**WordPress core:** try `/wp-sitemap.xml`. WordPress introduced that default index in [WordPress 5.5](https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/). An SEO plugin or site setting can change what is available, so this is not a universal address for every WordPress installation.

**WordPress with Yoast SEO:** open Yoast SEO → Settings → Site features. Under Technical SEO, find XML sitemaps and use **View the XML sitemap**. [Yoast’s instructions](https://yoast.com/help/xml-sitemaps-in-the-wordpress-seo-plugin/) show that route. Its usual index is `/sitemap_index.xml`; following the settings link avoids confusion when another address redirects there.

**Shopify:** open `/sitemap.xml` at your store’s domain. [Shopify generates this file](https://help.shopify.com/en/manual/promoting-marketing/seo/find-site-map) and links separate sitemaps for content such as products, collections, pages and blog posts. Private mode restricts access. Do not remove privacy controls merely to make an import work.

**Webflow:** check `/sitemap.xml`. If it is missing, inspect Site settings → SEO → Sitemap. [Webflow’s auto-generation instructions](https://help.webflow.com/hc/en-us/articles/33961355371667-Create-a-sitemap-in-Webflow) require enabling the setting, saving and publishing; a project may instead use a custom sitemap. Check with whoever maintains the site before changing that configuration.

These locations were checked against the linked platform documentation on October 13, 2026. Your site’s actual response is the final check. If you do not manage its settings, ask the maintainer for the public XML sitemap URL rather than changing plugins or search-visibility settings to experiment.

## 2. Identify an XML page list or index

A browser may show raw XML, a styled table, or a notice that the XML has no style information. None of those appearances alone tells you whether the file is usable. Look at what its entries point to.

A **page sitemap** has a `urlset` containing `url` entries. Each entry’s `loc` gives a page address. A **sitemap index** has a `sitemapindex` containing `sitemap` entries; those `loc` values point to other sitemap files. The [XML protocol](https://www.sitemaps.org/protocol.html) defines both structures.

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
<figcaption>A sitemap index is an extra layer of discovery. If your address already opens a page list, start there. Importing a list does not establish that the content was reviewed.</figcaption>
</figure>

For a public example, open [Staleaway’s sitemap](/sitemap.xml). At this guide’s publication it uses `urlset`, with `loc` entries for public pages such as the blog. This demonstrates the file’s shape; it is not evidence of a customer import or a complete inventory of every application route.

An index is not an error. Staleaway’s importer follows XML sitemap indexes, but large, deeply nested or partly unavailable indexes can produce an incomplete list. A relevant child sitemap can make your first review list easier to inspect.

## 3. Choose the review scope

Before copying the address into an app, decide what you want to maintain. “Our public help articles” is a useful scope. “Every URL that exists” may include archives, product variants or other pages you do not intend to review in this pass.

Open a few representative entries. Do they reach the live pages you expected? If an index separates blog posts from products, inspect the child file for the section you need. Choosing that child is a manual choice of input, not a filtering feature inside Staleaway.

Shopify’s separate content sitemaps illustrate why this matters: a shop owner reviewing buying guides might start with the blog list rather than the full store index. A WordPress editor should likewise check the entries, rather than assume a file with “post” in its name contains every page they care about.

Keep a separate note of important pages missing from the sitemap. Membership is not proof that a page is current, and absence does not by itself mean a page is broken. Ask the site maintainer whether an omission is intentional. Do not add private pages or credential-bearing links to a public sitemap to make a review list look complete.

## 4. Check import readiness

Staleaway needs the full address of an XML sitemap. A homepage, an HTML directory of links, and a `robots.txt` file are not interchangeable with that input. Use an uncompressed XML sitemap URL; do not assume a downloadable `.gz` file is supported. HTTP transport compression is a separate matter.

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

Stop at an uncertain input instead of recording it as a pass. A narrower list is useful only if it contains the pages you intend to review; a short empty file is not a better result.

**Worked example:** you manage public help articles and find an index through the CMS settings. One child lists help pages, while another lists the news archive. You open the help child, confirm that known public articles appear, and put that child’s full URL in the worksheet. After adding it to Staleaway, you compare the imported list with those same representative articles. If one is missing, record the mismatch and investigate before calling the setup complete. This is an illustrative workflow, not a customer result or a guarantee that checking a sample proves completeness.

## 5. Import and verify listed pages

To use the list for reminders, [create a free Staleaway account](/accounts/signup/) or sign in to your existing account. In the dashboard, enter the full XML address in **Sitemap URL** and choose **Add Sitemap**. Import runs in the background. Open the sitemap entry and check which intended pages appeared.

**A successful add is not proof that every page was imported.** A fetch or XML error in one child can leave a partial list, and traversal limits can stop a broad index. There is no promised completion time. If the list stays empty or differs from the input, recheck the public XML and the selected child with your site maintainer; do not keep adding duplicate entries to test whether waiting helped.

Then choose the pages per review email and a daily, weekly or monthly cadence. The [Staleaway workflow](/#how-it-works) brings pages to your attention; it does not certify them as accurate. Reminders select unreviewed pages rather than guaranteeing that every page is covered within a particular interval.

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
