// Deliberately use PostHog's capture API, not an auto-collecting remote SDK.
// Contract: https://posthog.com/docs/api/capture (verified 2026-10-27).
const INGEST_URL = "https://us.i.posthog.com/i/v0/e/";
const STORAGE_KEY = "staleaway_public_visitor_v1";
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const REFERRERS = [
  "google.com", "bing.com", "duckduckgo.com", "search.yahoo.com",
  "chatgpt.com", "chat.openai.com", "perplexity.ai", "claude.ai",
  "copilot.microsoft.com", "gemini.google.com",
];

function acquisitionReferrer(referrer, origin) {
  try {
    const url = new URL(referrer);
    if (!["https:", "http:"].includes(url.protocol) || url.origin === origin) {
      return "direct_or_internal";
    }
    // Preserve only a known acquisition domain, never a path/query/fragment or
    // arbitrary private hostname. Exact/dot-boundary matching avoids lookalikes.
    return REFERRERS.find(host => url.hostname === host || url.hostname.endsWith("." + host)) || "other_external";
  } catch (error) {
    return "direct_or_internal";
  }
}

function publicConfig(win, doc) {
  const element = doc.getElementById("public-analytics-config");
  if (!element || win.navigator.doNotTrack === "1" || win.doNotTrack === "1" || win.navigator.globalPrivacyControl) {
    return null;
  }
  try {
    const config = JSON.parse(element.textContent);
    const canonical = new URL(config.url);
    // Only the server's public route may be measured. Do not use location.href
    // or read any old PostHog cookie/superproperty/identity storage.
    if (!config.api_key || canonical.origin !== win.location.origin || canonical.pathname !== win.location.pathname || canonical.search || canonical.hash) {
      return null;
    }
    return { config, canonical };
  } catch (error) {
    return null;
  }
}

async function capturePublicEvent(event, version, win, doc) {
  const context = publicConfig(win, doc);
  if (!context) return false;
  try {
    const { config, canonical } = context;
    let visitorId = win.localStorage.getItem(STORAGE_KEY);
    if (!UUID.test(visitorId || "")) {
      visitorId = win.crypto.randomUUID();
      win.localStorage.setItem(STORAGE_KEY, visitorId);
    }
    const referrer = acquisitionReferrer(doc.referrer, canonical.origin);
    const isQa = Boolean(win.navigator.webdriver) || new URLSearchParams(win.location.search).get("staleaway_qa") === "1";
    const properties = {
      "$current_url": canonical.href,
      "$pathname": canonical.pathname,
      "$host": canonical.hostname,
      "$process_person_profile": false,
      "$geoip_disable": true,
      "acquisition_referrer": referrer,
      "measurement_version": version,
      "is_qa": isQa,
      "is_known_bot": /bot|crawler|spider|headless|playwright/i.test(win.navigator.userAgent || ""),
    };
    // No DOM, form values, document title, raw referrer, URL parameters,
    // account identifiers, session replay, or remotely configured collection.
    const response = await win.fetch(INGEST_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "omit",
      referrerPolicy: "no-referrer",
      keepalive: true,
      body: JSON.stringify({
        api_key: config.api_key,
        event,
        distinct_id: visitorId,
        properties,
      }),
    });
    return response.ok;
  } catch (error) {
    // Blocked storage, unavailable crypto, and failed measurement must not
    // affect the page. Do not log potentially sensitive request/error details.
    return false;
  }
}

function capturePublicPageview(win = window, doc = document) {
  return capturePublicEvent("$pageview", "public-v1", win, doc);
}

const listeningDocuments = new WeakSet();

function installPublicSignupClicks(win = window, doc = document) {
  const context = publicConfig(win, doc);
  if (!context || listeningDocuments.has(doc)) return false;
  const signupPath = context.config.signup_path;
  // The destination is server-owned, never an arbitrary data attribute or URL.
  if (signupPath !== "/accounts/signup/") return false;
  doc.addEventListener("click", event => {
    if (!event.isTrusted || event.defaultPrevented || event.button !== 0) return;
    try {
      const anchor = event.target.closest("a[href]");
      if (!anchor) return;
      const destination = new URL(anchor.href, win.location.origin);
      if (destination.origin !== win.location.origin || destination.pathname !== signupPath || destination.search || destination.hash || destination.username || destination.password) return;
      // No text, element attributes, destination URL, placement, or inputs sent.
      // Recheck opt-outs/config on every click; never delay or prevent navigation.
      capturePublicEvent("public_signup_cta_clicked", "public-cta-v1", win, doc);
    } catch (error) {
      // Invalid/non-element targets and analytics failures leave navigation alone.
    }
  });
  listeningDocuments.add(doc);
  return true;
}

module.exports = { acquisitionReferrer, capturePublicPageview, installPublicSignupClicks };
