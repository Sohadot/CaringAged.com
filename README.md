# CaringAged.com

**A clearer path through later-life care.** A concept-first, static editorial website created for the CaringAged.com digital asset and owned by Sohadot.

## Positioning

CaringAged is **an independent educational concept**, not a care provider, a health adviser, a directory of verified services or a referral marketplace. Its first release helps readers distinguish care pathways and frame more useful questions. It does not collect health information, recommend individual services or score providers.

- `/`: Public educational landing page and accessible interactive *care lens*.
- `/sources/`: Primary-source bibliography, editorial approach, geographic limitations and disclaimers.
- `/acquire/`: Separate, non-indexable strategic acquisition page. **Do not put this URL in a sitemap.**
- `/robots.txt` and `/sitemap.xml`: crawl discovery and indexation scope.
- `/og/caringaged-share.png`: 1200 × 630 PNG social-preview artwork; generated from `scripts/generate_og.py` and referenced by Open Graph/Twitter metadata.

## Evidence and accuracy

Initial evidence review: **2026-11-03**. The facts and country-specific caveats are supported with direct links to WHO, NIH/NIA, My Aged Care, NHS, Medicare and CDC. The WHO projection of 2.1 billion people aged 60+ by 2050 is a **demographic projection**, never an estimate of domain value, market revenue or paying customers.

Country-specific eligibility, funding and professional licensing must never be presented as universal. Do not invent provider ratings, care facility listings, verified staff, testimonials, endorsements, revenue, traffic or partnerships.

## Design and technology

Single-file static pages using semantic HTML, responsive CSS and a small local JavaScript enhancement. No front-end framework, external JavaScript, user tracking, cookies or form data collection. Web fonts may load from Google Fonts; Georgia/system fonts are the fallback.

Accessible features include skip link, focus-visible indicators, semantic headings, accessible button state in the care lens, and reduced-motion support.

## Deployment notes

This repository contains **source code only**. Domain/DNS/TLS, hosting and any deployment have not been configured or verified by this PR. Deploy as a static site from the repository root; confirm hosting resolves directory-style links `/sources/` and `/acquire/` to their respective `index.html` files. Enforce HTTPS and verify the canonical URL matches the eventual production domain.

Before making the public site live:
1. Confirm Sohadot ownership of the domain, DNS, TLS and selected hosting.
2. Confirm `agent@sohadot.com` is the intended acquisition contact.
3. Review medical-context disclaimers and any relevant trademarks for the chosen operating markets.
4. Verify `/acquire/` returns `noindex,follow` and is excluded from the sitemap.
5. Verify the current Dynadot listing URL resolves and is purchasable; escrow is only an option by agreement.
6. Confirm `/og/caringaged-share.png` resolves as a public `image/png` over HTTPS and renders in share debuggers.
7. Open all internal links, run responsive and keyboard checks, and update evidence dates when content is substantively re-reviewed.

## Review boundary

This work is intended for a **draft pull request**. No merge, hosting configuration, production mutation or live deployment is implied or authorized by the existence of the code.

(c) 2026 Sohadot.
