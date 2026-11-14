# Kings of Kings website project

This is the independent HTML/CSS/JavaScript replacement for kingsofkingsinternational.com. It does not require WordPress, Elementor, a local LLM, or Docker.

Use the current project and preview; do not start another redesign or substitute a different platform. Preserve the existing Kings identity and supplied assets. User directs changes through chat. Keep live hosting untouched until the user authorizes publishing.

Preview: python3 tools/preview.py (localhost port 8090). Preview is loopback-only and noindex. It automatically refreshes after file changes. Stop with Ctrl+C. No paid dependency or build service is needed.

Verify: python3 tools/check.py and node --check assets/site.js. Test visible desktop/mobile behavior through the available browser tools. tools/build.py regenerates pages from its templates and content/legacy-pages.json; update that source when making durable page changes. Do not regenerate over manual Pinegrow edits without incorporating them first.

Pinegrow project root is this folder. Root page is index.html. Project has no CSS framework. Do not add dependencies without a clear requirement. Read Pinegrow's current project context before using its editing API.

content/events.json records the initial event archive, currently mirrored in tools/build.py. Keep both synchronized when changing event information. Never invent upcoming dates, ticket availability, testimonials, attendance figures, or payment functionality. Existing October 9–11, 2026 events are past events. Store no credentials in the project.

Deployment is NOT connected. Preserve old page paths; use production redirects for changed paths. Before launch prepare a clean deployable copy excluding tools/, content/, AGENTS.md, reports, project metadata and snapshots; remove preview noindex directives only from that approved production copy, generate public robots.txt and sitemap.xml, test domain redirects, TLS, real 404 responses, caching and Search Console. Do not publish raw project source files.

Orange coordination is NOT verified. Same account does not establish remote machine access. Do not claim agents, scheduled updates, or deployment are running unless demonstrated.

## Current archive extension and KOKI
Read KOKI.md before content updates. content/events.json is now the single event source; tools/build.py no longer mirrors hardcoded events. tools/archive_pages.py generates the brand home, Record Label, release stories, artist archive, gallery, and events hub. Update generator sources rather than generated HTML. tools/koki.py validates all four content collections and supports backed-up local updates. No autonomous service is installed. Original artwork is preserved; web copies are in assets/archive. Keep private source manifests and legal research outside the website folder.


Shared-root migration: the editable website is now website/ under the shared project. Generator reference files are ../reference/wordpress. Use ../preview.sh or tools/preview.py. All active build paths resolve relative to this root; do not restore old local workspace dependencies. Mail setup is ../private/mail-setup.
