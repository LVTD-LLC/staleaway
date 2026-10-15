# Content review planner — pre-merge render proof

Captured October 15, 2026 from the isolated Django-rendered CI preview for revision `94a80bc73cc408bc4e49376267dc238e8d66666a`. Only fictional example inputs are shown; no customer data or analytics exports.

- [Desktop calculator](desktop-default.png): 1280px viewport; example result and local export.
- [Desktop guide](desktop-guide.png): worked example, two original diagrams, sources and product limits.
- [Mobile method diagram](mobile-figure.png): 320px viewport.
- [Maximum values on mobile](mobile-maximum-viewport.png): actual 320px viewport capture after the narrow-screen correction; no result-cell or document overflow.

Independent review: tool UX 5/5, visual clarity 4/5; input validation, stale-result hiding, Enter calculation and clipboard failure fallback passed with no JavaScript errors. Maximum input arithmetic and default arithmetic checked independently. Narrow-screen numeric overflow discovered during review was corrected before merge.

CI [38701946001](https://github.com/LVTD-LLC/staleaway/actions/runs/38701946001): 148 Docker-backed tests (`make test`), 2,062 planner assertions, 19 analytics assertions, frontend build and isolated preview rendering passed. These screenshots establish pre-merge rendering, not deployment, search indexing or acquisition lift.

The site has one light design; OS light/dark preference checks do not imply an alternate dark theme. Remote full-element captures can misplace an offscreen fixed skip link; the mobile maximum proof uses a viewport capture, with DOM geometry checked independently.
