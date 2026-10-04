# Staleaway design

Reference: Firefox landing page, inspected through TastefulKit MCP:
https://tastefulkit.com/designs/8403ad70-8b33-4345-90cc-05d2c086848d/

Adapt its deep-purple opening/footer, tall condensed headlines, lavender feature cards,
warm illustration accents, rounded pills and alternating white editorial sections.
Do not copy Firefox branding, fox artwork, product claims or source code.

- Night: #210340; action: #7543e3; lavender: #f1e7f8; ink: #15141a.
- Warm yellow/orange/pink are decorative accents, not body-text colors.
- Headings: self-hosted Barlow Condensed Bold (OFL in vendors/fonts).
- Body: system Arial/Helvetica. Do not fetch remote fonts at runtime.
- Components use `sa-*` classes in frontend/src/styles/index.css.
- Landing: centered hero, four feature cards, three-step setup, explicitly illustrative email preview, asymmetric benefit grid, closing CTA.
- App: preserve PR #8's forms and controllers; use purple navigation/actions with light surfaces.
- Mobile: one-column cards, responsive navigation with Escape/outside-close, no document overflow.
- Preserve semantic labels, keyboard focus, reduced-motion preference and readable contrast.
- Public copy says Staleaway. No rename announcements or agent/agency promises.
