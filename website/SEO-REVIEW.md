# Webmaster review — development build

## Implemented and checked

- Static, crawlable HTML with local CSS, JavaScript, images and fonts; essential content does not require JavaScript.
- Unique page titles and descriptions, document language, viewport tags, production canonical URLs and social metadata.
- One H1 per page; clear sections, internal navigation, footer navigation and a visitor site map.
- Organization and breadcrumb JSON-LD; three dated event detail pages with JSON-LD and explicit past-event labeling. No invented prices or future events.
- Existing /studio/, /reggae-events/, /canada/, /blog/, /gallery/, /programs/, /tickets/ and /contact/ paths preserved. Legacy home slug has a redirect document and an Apache 301 rule.
- Corrected displayed info email spelling and removed the invisible character from the contest email destination.
- Duplicate news paragraphs deduplicated; old announcements clearly identified as archives. Replaced broken merchandise call-to-action with direct enquiries.
- Optimized WebP copies of source artwork; originals unchanged. Explicit image dimensions, lazy loading below the hero, eager hero image, self-hosted font with swap.
- Responsive navigation with expanded state, keyboard escape handling, visible focus, skip link, reduced-motion support and native gallery dialog.
- Preview noindex meta and HTTP headers, disallow-all robots.txt, valid production-domain sitemap prepared for launch.

## Verification performed

Static checks passed for 16 HTML documents (including the duplicated root 404): metadata presence, one H1, local file references, internal anchor destinations, image attributes and JSON-LD syntax. Sitemap XML parses correctly. JavaScript syntax check passed.

Browser checks passed: homepage at 1440 px and 390 px, no horizontal overflow or broken loaded images, mobile menu expansion, Toronto city filtering and gallery dialog opening/closing. These checks do not constitute a full accessibility audit, measured Core Web Vitals, schema eligibility validation or verification of every external destination.

## Must resolve before production

1. Confirm future event schedule and ticket links; existing October 9–11 shows have passed. Confirm the published contact addresses are monitored; email deliverability was not tested.
2. Confirm content migration completeness against all media/posts and external links. Original backup remains the full reference. This build deliberately does not re-create registration forms or commerce without real service connections.
3. Review visual design and source rights with owner. Artwork is reused from supplied backup; its licensing and real-world identity claims are not independently verified.
4. Set up deployment credentials and rollback, then deploy the approved build. Existing aliases and host settings need inspection. No live server changes have been made.
5. In approved production copy: remove noindex meta, do not use preview server, replace robots.txt with public crawl rules and sitemap location, exclude tools/content/reports/project metadata.
6. Verify HTTPS and preferred-domain redirects, trailing slash behavior, 301s, true 404 status, compression and browser caching on HostPapa. Domain aliases are currently unknown beyond the owner's description.
7. Validate live structured data with Google's Rich Results Test, connect Search Console, submit sitemap and inspect representative URLs. Obtain prior URL/traffic inventory to catch unlisted inbound landing pages.
8. Measure mobile Lighthouse/PageSpeed and Core Web Vitals after production deployment. Lab/browser checks here do not guarantee rankings or field performance.
9. Verify Orange access and define any unattended update workflow before saying agents update the site automatically. Nothing scheduled yet.

No statement of “all SEO fixed” or production readiness is justified until these checks are complete.
