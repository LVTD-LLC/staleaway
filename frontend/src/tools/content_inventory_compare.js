// Compare pasted strings only. URL parsing validates syntax; it never supplies a match key.
const LIMITS = { bytes: 250000, lines: 2000, url: 2048, displayed: 100 };
const FIELDS = [
  { key: "inventory", label: "Intended inventory", example: "https://example.com/about\nhttps://example.com/services\nhttps://example.com/contact" },
  { key: "sitemap", label: "Selected sitemap page URLs", example: "https://example.com/about\nhttps://example.com/services\nhttps://example.com/news" },
  { key: "imported", label: "Actual imported records", example: "https://example.com/about\nhttps://example.com/news\nhttps://example.com/archive" },
];
const GROUPS = [
  { key: "111", label: "In all three lists", action: "Confirm scope; continue human review" },
  { key: "110", label: "Inventory + sitemap; not imported", action: "Check import status and selected sitemap" },
  { key: "101", label: "Inventory + imported; not in sitemap", action: "Check selected sitemap scope and record source" },
  { key: "100", label: "Inventory only", action: "Confirm intended scope and page URL" },
  { key: "011", label: "Sitemap + imported; not in inventory", action: "Confirm inventory scope with its owner" },
  { key: "010", label: "Sitemap only", action: "Check inventory scope and import status" },
  { key: "001", label: "Imported only", action: "Check record source and current review scope" },
];

function publicHost(hostname) {
  const host = hostname.toLowerCase().replace(/\.$/, "");
  if (host.startsWith("[")) {
    // Conservative scope: pasted IPv6 literals are not supported, including local/mapped forms.
    return false;
  }
  if (/^[0-9.]+$/.test(host)) {
    const parts = host.split(".").map(Number);
    const [a, b] = parts;
    return parts.length === 4 && parts.every(n => n >= 0 && n <= 255) &&
      a !== 0 && a !== 10 && a !== 127 && a < 224 &&
      !(a === 100 && b >= 64 && b <= 127) && !(a === 169 && b === 254) &&
      !(a === 172 && b >= 16 && b <= 31) && !(a === 192 && (b === 168 || b === 0)) &&
      !(a === 198 && (b === 18 || b === 19));
  }
  return host.includes(".") && !/(^|\.)(localhost|local|internal|lan|home|invalid|test|onion)$/.test(host) &&
    host.split(".").every(label => /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(label));
}

function validUrl(text) {
  if (text.length > LIMITS.url || /[\u0000-\u0020\u007f-\u009f\s\\?#]/u.test(text) || !/^https?:\/\//i.test(text)) return false;
  try {
    const url = new URL(text);
    const authority = text.slice(text.indexOf("://") + 3).split("/")[0];
    return Boolean(authority) && !authority.includes("@") && !url.username && !url.password && publicHost(url.hostname);
  } catch {
    return false;
  }
}

function parseList(raw) {
  const text = typeof raw === "string" ? raw : "";
  if (new TextEncoder().encode(text).length > LIMITS.bytes) return { error: "Exceeds 250,000 bytes. Shorten this list and compare again." };
  const lines = text.split(/\r\n|\n|\r/);
  const urls = new Set();
  const invalidLines = [];
  let nonblank = 0, blanks = 0, duplicates = 0;
  lines.forEach((line, index) => {
    const value = line.trim();
    if (!value) { blanks++; return; }
    nonblank++;
    // Reject control characters even at line boundaries; ordinary outer spaces are trimmed.
    if (/[\u0000-\u001f\u007f-\u009f]/u.test(line) || !validUrl(value)) {
      invalidLines.push(index + 1);
      return;
    }
    if (urls.has(value)) duplicates++;
    urls.add(value);
  });
  if (!nonblank) return { error: "Paste at least one public page URL. All three lists are required." };
  if (nonblank > LIMITS.lines) return { error: "Exceeds 2,000 nonblank lines. Shorten this list and compare again." };
  if (invalidLines.length) {
    const shown = invalidLines.slice(0, 20).join(", ");
    return { error: `Check line numbers ${shown}${invalidLines.length > 20 ? ` (and ${invalidLines.length - 20} more)` : ""}. Use public http/https page URLs only, without credentials, query strings or fragments. IPv6 literals are unsupported.` };
  }
  return { urls, duplicates, blanks, nonblank };
}

function compare(raw) {
  const lists = {}, errors = {};
  FIELDS.forEach(({key}) => {
    lists[key] = parseList(raw[key]);
    if (lists[key].error) errors[key] = lists[key].error;
  });
  if (Object.keys(errors).length) return { status: "invalid", errors };
  const union = new Set(FIELDS.flatMap(({key}) => [...lists[key].urls]));
  const counts = Object.fromEntries(GROUPS.map(group => [group.key, 0]));
  const rows = [...union].map(url => {
    const flags = FIELDS.map(({key}) => lists[key].urls.has(url));
    const key = flags.map(present => present ? "1" : "0").join("");
    const group = GROUPS.find(group => group.key === key);
    counts[key]++;
    return { url, flags, key, label: group.label, action: group.action };
  });
  return { status: "ready", lists, rows, counts };
}

function csv(result) {
  if (result.status !== "ready") return "";
  // Every URL starts with validated http(s); other cells are fixed labels, never formulas.
  const quote = value => `"${String(value).replace(/"/g, '""')}"`;
  const rows = [["URL", "In intended inventory", "In selected sitemap", "In imported records", "Membership", "Manual next step"],
    ...result.rows.map(row => [row.url, ...row.flags.map(flag => flag ? "yes" : "no"), row.label, row.action])];
  return rows.map(row => row.map(quote).join(",")).join("\r\n") + "\r\n";
}

module.exports = { LIMITS, FIELDS, GROUPS, validUrl, parseList, compare, csv };
