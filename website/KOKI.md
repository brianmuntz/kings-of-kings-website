# KOKI — Kings of Kings International website editor

This project is the shared source for prompt-directed changes. KOKI is the editing workflow and project role, not a separately running service. No background schedule, remote Orange connection or publishing account is configured.

## Use through chat

Ask the agent working in this project, for example:
- “KOKI, add this flyer as an upcoming event. The confirmed date is …, the venue is …, the official ticket link is …”
- “KOKI, add this record sleeve and these verified credits to Kings of Kings Records.”
- “KOKI, move this completed show into event history.”

The agent reads this file and AGENTS.md, preserves originals, adds suitable web copies, updates the appropriate collection, rebuilds, checks links/metadata, and shows the changed preview. Publishing is a separate final action after Brian authorizes it. When the event date passes, the events hub automatically treats it as history on the next build.

## Editable collections

- content/current-releases.json — current homepage/label releases, displayed as a fluid swipeable shelf. Keep historical releases in featured-releases.json. Preserve full artwork; no inferred artist identities or invented streaming links.

- content/events.json — dated shows, performers, venue, image and source. Never invent a date or ticket availability. `venue_verified: false` suppresses Event structured data when the venue is unknown.
- content/featured-releases.json — curated visual release stories.
- content/releases.json — public release metadata with source links. No private legal fields.
- content/archive-stories.json — source-grounded concert and campaign stories.

For a durable change, edit a collection or pass one complete record to:
`python3 tools/koki.py update --collection events --file /path/to/record.json`
This previews validation without writing. Add `--apply` to save with a recoverable backup in .koki/backups. Other collections use their names above, without .json.

Validate with `python3 tools/koki.py validate`. Build using a Python environment with Pillow: `python3 tools/build.py`. Check with `python3 tools/check.py` and `node --check assets/site.js`. Inspect desktop/mobile, search filters, original-image enlargement and changed routes. Preview: `python3 tools/preview.py`, then http://localhost:8090/.

## Provenance and standards

A release credit does not prove an exclusive artist contract. A performer on a concert poster is an event appearance, not necessarily a label artist. Preserve this distinction. Private source paths, legal research notes and contract conclusions must not appear publicly. Unknown years stay unknown. Promotional claims in old artwork are historical quotations, not new factual claims.

Keep the original artworks unchanged. Use full-aspect web derivatives and accurate alt descriptions. Do not invent artist portraits or use generated artwork to replace exact logos. Keep release/event titles, unique descriptions, canonical URLs, social metadata, breadcrumbs and source-appropriate structured data synchronized.

## Mac / Orange handoff

Orange can follow this workflow once the same project files are transferred or shared and an agent there is explicitly opened on this folder. An OpenAI account by itself does not share the local disk. Never claim a transfer or remote service works until tested. Use source control or a private shared folder when hosting is selected; credentials belong outside this project.

## Hosting later

Prepare a public-only deployable folder excluding tools, content, project instructions, private reports and backups. Remove preview noindex only in the approved deployment copy. Confirm TLS, domain redirects, real 404 responses, security headers and rollback. Content can remain file-based; choose a database only if an actual authenticated admin/multi-user feature requires it. No public write endpoint exists in this preview.


## Enquiries and promotions
Enquiry UI: tools/enquiry_pages.py, tools/enquiry_form.fragment and assets/site.js. All production forms target /api/enquiries; localhost validates without sending or storing. Private mail setup is in private/mail-setup at the project root, outside the website. Routing destination and no-reply configuration belong there, never in public page text. Do not claim delivery, mailing-list registration, mailbox-agent replies or forwarding works until configured and tested. Giveaway announcement is at /contests/; entries are closed pending eligibility and official rules. No automated forwarding to Colin is enabled.


## Shared project location
The authoritative project root is /Volumes/AI/OpenAI_projects/Kings of Kings Website on this Mac. The website is website/; private mail setup is ../private/mail-setup from the website folder. Other devices may mount the share elsewhere. Use root-relative project paths and read ../README.md.
