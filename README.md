# Kings of Kings Website

This shared folder is the authoritative development project. Open this folder on the Mac or another device; open `website/` in Pinegrow.

## Start the preview

Run `./preview.sh`, then open http://localhost:8090/ on that same computer. Python 3 is required. The preview listens only on that device; sharing files does not expose the preview to the network. Do not run competing previews on the same port.

## Project layout

- **website/** — editable HTML, CSS, JavaScript, content collections, generator and KOKI instructions. All assets used by the pages are local to this folder.
- **originals/** — preserved copies of supplied artwork, Photoshop sources, PDFs, Numbers discography and merchandise mockups. Originals on the user's media volumes were left intact.
- **reference/wordpress/** — legacy uploaded assets and fonts required by the generator. No WordPress installation, passwords or database is included here.
- **research/** — live-site captures, Discogs evidence, provenance manifests and earlier build/research scripts. Historical acquisition scripts may retain original library paths; they are not required to build or preview the site.
- **reviews/** — screenshots of the site and previous visual checks.
- **private/** — prepared mail setup and private catalogue research. Never publish this directory.
- **migration/** — file-transfer verification and source maps.

## Rebuild and check

Run `./rebuild.sh`. Rebuilding needs Python 3 with Pillow installed (`requirements.txt`). The Mac's existing Pillow environment can be used; another computer needs its own environment. No local LLM, paid build service, WordPress or Docker is required.

Read AGENTS.md and website/KOKI.md before editing. Update generator sources and content collections rather than generated pages. Existing page paths, supplied artwork and Kings identity must be preserved.

## Current state

The site is a local preview, not a published replacement. Email delivery, no-reply confirmations, mailing-list registration, contest entries, agent responses and forwarding are not active. Private setup notes explain the remaining mail work. No credentials are stored in the website.

The original local WordPress clone, its database and passwords remain outside this share in the previous local workspace. Original project copies are retained there as a migration rollback; compatibility links point the old working paths to this shared project. This folder does not depend on those links.

On other devices, the share may mount at a different path. The active website build resolves paths relative to this project root. Preview and rebuild scripts also use their own location. Only one person or agent should edit the shared files at a time; concurrent edits are not automatically merged.
