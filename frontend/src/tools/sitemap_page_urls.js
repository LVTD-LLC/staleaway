// Sitemaps protocol 0.9: https://www.sitemaps.org/protocol.html
// XML DOM contract: https://developer.mozilla.org/en-US/docs/Web/API/DOMParser/parseFromString
// Checked 2026-11-18. No document nodes are inserted into the page; no fetch/storage.
const { LIMITS, parseList } = require("./content_inventory_compare");
const NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9";

function extractPageUrls(raw, Parser = globalThis.DOMParser) {
  const text = typeof raw === "string" ? raw.trim() : "";
  const fail = error => ({ status: "invalid", error });
  if (!text) return fail("Paste public page-sitemap XML first. No page list was extracted.");
  if (new TextEncoder().encode(raw).length > LIMITS.bytes) return fail("XML exceeds 250,000 bytes. Use a smaller page sitemap; no partial list was extracted.");
  if (/<!DOCTYPE|<!ENTITY|<\?(?!xml(?:\s|\?>))/i.test(text)) return fail("Document types, entity declarations and processing instructions are unsupported. No page list was extracted.");
  if (typeof Parser !== "function") return fail("XML parsing is unavailable in this browser. Prepare one public page URL per line manually.");
  let doc;
  try { doc = new Parser().parseFromString(text, "application/xml"); }
  catch { return fail("XML could not be parsed. No page list was extracted."); }
  if (doc.getElementsByTagNameNS("*", "parsererror").length) return fail("XML is malformed. Copy the complete source of one page sitemap; no partial list was extracted.");
  const root = doc.documentElement;
  if (root && root.localName === "sitemapindex" && root.namespaceURI === NAMESPACE) return fail("This is a sitemap index, not a page list. Open a relevant child sitemap yourself and paste its urlset XML. Child files have not been fetched.");
  if (!root || root.localName !== "urlset" || root.namespaceURI !== NAMESPACE) return fail("Use a urlset in the Sitemaps 0.9 namespace, not HTML, a URL or an index. No page list was extracted.");
  const entries = Array.from(root.children);
  if (!entries.length || entries.length > LIMITS.lines) return fail("Use a page sitemap with 1–2,000 URL entries. No partial list was extracted.");
  const urls = [];
  for (const entry of entries) {
    if (entry.localName !== "url" || entry.namespaceURI !== NAMESPACE) return fail("Unexpected entry in urlset. No partial list was extracted.");
    const locs = Array.from(entry.children).filter(child => child.localName === "loc" && child.namespaceURI === NAMESPACE);
    if (locs.length !== 1 || locs[0].children.length) return fail("Each URL entry needs exactly one text-only page loc. No partial list was extracted.");
    // XML decoding is deliberate. URL spelling/encoding is otherwise preserved.
    urls.push(locs[0].textContent.trim());
  }
  const list = parseList(urls.join("\n"));
  if (urls.some(url => !url || /[\r\n]/.test(url)) || list.error) return fail("A page loc is empty or outside this tool's public-URL limits. Check every entry; no partial list was extracted. Queries, fragments, credentials and local/private hosts are unsupported.");
  return { status: "ready", text: Array.from(list.urls).join("\n"), entries: entries.length, unique: list.urls.size, duplicates: list.duplicates };
}

module.exports = { extractPageUrls };
