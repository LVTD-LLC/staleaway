# Content inventory comparison: UI verification

Sanitized screenshots from isolated public fixtures for PR #48. All addresses and examples are fictional; no customer records, production accounts, imports or email sends were used. The screenshot artifact implements `5efc0d2`; independent review also checks the responsive flow separately. The site is light-only: OS light/dark preference checks are not a claim of a dark theme or cross-engine coverage.

## Tool states

- Default: [320px/light](default-320-light.png), [390px/dark preference](default-390-dark.png), [1280px/light](default-1280-light.png), [1280px/dark preference](default-1280-dark.png).
- [All seven membership groups](valid-seven-groups.png).
- [Empty required input](empty-required.png), [malformed input and neutral recovery](malformed-neutral.png).
- [2,048-character URL boundary](boundary-url-2048.png), [2,000-line boundary with explicit displayed/export scope](boundary-2000.png), [2,001-line rejection](over-limit-neutral.png).
- [JavaScript-disabled manual worksheet](javascript-disabled-manual.png).

Native download events and filenames were observed and the actual generated CSV Blob bytes independently checked for 7, 2,000 and 6,000 result rows. Browserless's cross-container download-artifact path cannot be copied by the client, so OS-level file persistence is not claimed. No live fetch, timeout or kill-switch states exist: comparison is entirely local.

Functional verification includes equal totals with different URLs, seven combinations, exact string distinctions, Unicode, duplicates/blanks, editing/clearing invalidation, line-number-only errors and safe text output. The independent source, code, editorial and rendered-UX reviews are retained privately with the existing project research history; they are not customer or acquisition outcomes.

## Responsive flow

Independent calibrated render checks: [320px/light](responsive-diagram-320-light.png), [390px/dark preference](responsive-diagram-390-dark.png), [desktop/light](responsive-diagram-1280-light.png), [desktop/dark preference](responsive-diagram-1280-dark.png). Stacked input boxes preserve legible labels on narrow screens; comparison logic is unchanged.
