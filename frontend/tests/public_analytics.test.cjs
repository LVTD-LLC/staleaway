const assert = require("assert").strict;
const { capturePublicPageview, acquisitionReferrer } = require("../src/analytics/public");
const UUID = "638b0b5b-6d96-4d65-b3e7-7c4668665620";
const PRIVATE = "private-synthetic-marker@example.invalid";

function fixture(overrides = {}) {
  const calls = [];
  const stored = new Map([
    ["ph_old_posthog", JSON.stringify({distinct_id: PRIVATE, $initial_current_url: PRIVATE})],
  ]);
  const win = {
    navigator: { userAgent: "ordinary-test-browser", webdriver: false },
    location: { origin: "https://staleaway.com", pathname: "/blog", search: "?next=" + PRIVATE, hash: "#" + PRIVATE },
    localStorage: { getItem: key => stored.get(key), setItem: (key, value) => stored.set(key, value) },
    crypto: { randomUUID: () => UUID },
    fetch: async (url, options) => { calls.push({url, options}); return {ok: true}; },
    ...overrides,
  };
  const doc = {
    cookie: "session=" + PRIVATE,
    referrer: "https://staleaway.com/accounts/password/reset/key/" + PRIVATE,
    title: PRIVATE,
    getElementById: () => ({textContent: JSON.stringify({api_key: "synthetic-project-key", url: "https://staleaway.com/blog"})}),
  };
  return {win, doc, calls, stored};
}

(async () => {
  let checks = 0;
  const f = fixture();
  assert.equal(await capturePublicPageview(f.win, f.doc), true);
  const event = JSON.parse(f.calls[0].options.body);
  assert.equal(event.event, "$pageview");
  assert.equal(event.distinct_id, UUID);
  assert.equal(event.properties.$current_url, "https://staleaway.com/blog");
  assert.equal(event.properties.acquisition_referrer, "direct_or_internal");
  assert.equal(JSON.stringify(f.calls).includes(PRIVATE), false);
  assert.equal(f.calls[0].options.credentials, "omit");
  assert.equal(f.calls[0].options.referrerPolicy, "no-referrer");
  assert.deepEqual(Object.keys(event.properties).sort(), [
    "$current_url", "$geoip_disable", "$host", "$pathname", "$process_person_profile",
    "acquisition_referrer", "is_known_bot", "is_qa", "measurement_version",
  ].sort());
  checks++;

  await capturePublicPageview(f.win, f.doc);
  assert.equal(JSON.parse(f.calls[1].options.body).distinct_id, event.distinct_id);
  f.stored.set("staleaway_public_visitor_v1", PRIVATE);
  await capturePublicPageview(f.win, f.doc);
  assert.equal(JSON.parse(f.calls[2].options.body).distinct_id, UUID);
  checks++;

  for (const url of ["https://staleaway.com/accounts/login/", "https://staleaway.com/blog?token=" + PRIVATE, "https://staleaway.com/blog#" + PRIVATE, "https://elsewhere.invalid/blog"]) {
    const x = fixture();
    x.doc.getElementById = () => ({textContent: JSON.stringify({api_key: "test", url})});
    assert.equal(await capturePublicPageview(x.win, x.doc), false);
    assert.equal(x.calls.length, 0);
    checks++;
  }
  for (const mutate of [
    x => { x.doc.getElementById = () => null; },
    x => { x.doc.getElementById = () => ({textContent: "invalid-json"}); },
    x => { x.win.navigator.globalPrivacyControl = true; },
    x => { x.win.navigator.doNotTrack = "1"; },
    x => { x.win.localStorage.getItem = () => { throw Error("blocked"); }; },
    x => { x.win.crypto.randomUUID = undefined; },
  ]) {
    const x = fixture(); mutate(x);
    assert.equal(await capturePublicPageview(x.win, x.doc), false);
    assert.equal(x.calls.length, 0);
    checks++;
  }
  for (const ref of ["https://google.com/" + PRIVATE, "https://www.google.com/?q=" + PRIVATE]) {
    assert.equal(acquisitionReferrer(ref, "https://staleaway.com"), "google.com");
    checks++;
  }
  for (const ref of ["https://evilgoogle.com/", "https://google.com.evil.invalid/", "https://private-intranet.invalid/" + PRIVATE]) {
    assert.equal(acquisitionReferrer(ref, "https://staleaway.com"), "other_external");
    checks++;
  }
  const qa = fixture(); qa.win.navigator.webdriver = true; qa.win.navigator.userAgent = "HeadlessChrome";
  await capturePublicPageview(qa.win, qa.doc);
  assert.equal(JSON.parse(qa.calls[0].options.body).properties.is_qa, true);
  assert.equal(JSON.parse(qa.calls[0].options.body).properties.is_known_bot, true);
  const failure = fixture({fetch: async () => { throw Error("offline"); }});
  assert.equal(await capturePublicPageview(failure.win, failure.doc), false);
  checks += 2;
  console.log(`${checks} public analytics regression cases passed (mocked network).`);
})().catch(error => { console.error(error); process.exitCode = 1; });
