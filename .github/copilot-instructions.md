<!-- Copied/created for clayweb.github.io (metaclay) -->
# Copilot / AI assistant instructions for this repo

Keep guidance short and actionable. This repository is a small static site used as an internal "CLAYSTUDIO" portal. Most pages are plain HTML, CSS and client-side JavaScript. The site serves static assets from the project root (for example `/claystudio/images/` and `/projects/`).

Key facts an AI helper must know
- This is a static site (no server-side code). Edit HTML, CSS and client-side JS only.
- Main entry files: `index.html`, `play.html`, and the `claystudio/` folder (notably `claystudio/device.html`).
- Assets live under `claystudio/images/` (device images) and `projects/` (video refs, thumbnails, turnover docs).

Primary patterns to follow
- Image naming: device images follow the pattern `<ID>_IMG01.jpg` through `<ID>_IMG16.jpg`. See `claystudio/device.html` which attempts to load up to 16 images and removes missing ones via `img.onerror`.
- Invoice mapping: an inventory id is derived from a device id by slicing and prefix replacement (example in `device.html`: `let inv = id.slice(0, -2).replace("DEV", "INV");`). Use this same logic when creating links or UI that references invoices.
- URL-driven views: pages like `play.html` and `claystudio/device.html` rely on query string parameters (e.g., `?id=DEV-211009-A01&path=/claystudio/images/device/&name=...`) — preserve parameter names and semantics when changing navigation.
- Parts list format: `device.html` expects the `parts` parameter to be delimited by `//` entries and uses ` -- ` and ` ** ` to split id, name, cost, notes. When parsing or generating parts data, follow that exact delimiter convention.

Developer workflows and