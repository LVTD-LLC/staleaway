const assert = require('assert').strict;
const { extractPageUrls } = require('../src/tools/sitemap_page_urls');
let parserCalls = 0;
class MustNotParse { constructor() { parserCalls++; throw Error('unsafe invocation'); } }
for (const raw of ['', ' '.repeat(250001), '<!DOCTYPE urlset [<!ENTITY x SYSTEM "https://example.com/">]><urlset/>', '<?xml-stylesheet href="https://example.com/style"?><urlset/>', '<!ENTITY x "a"><urlset/>']) {
  const r = extractPageUrls(raw, MustNotParse);
  assert.equal(r.status, 'invalid');
  assert.equal(r.text, undefined);
}
assert.equal(parserCalls, 0);
assert.match(extractPageUrls('<urlset/>', null).error, /unavailable/);
assert.equal(extractPageUrls('<urlset/>', MustNotParse).status, 'invalid');
assert.equal(parserCalls, 1);
console.log('XML preflight: empty/byte-limit/declarations/instructions/no-parser/exception passed; native DOM cases require separate browser verification');
