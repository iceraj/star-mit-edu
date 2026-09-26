# Archive provenance and capture notes

- **Source:** `http://star.mit.edu/` and same-host pages/assets reachable from its links.
- **Capture date:** 2026-09-26 UTC.
- **Capture status:** Mirror and supplemental linked-resource pass completed. The publishable tree contains 5,131 files and 152,770,490 bytes (145.69 MiB), with a largest asset of 8,413,616 bytes. No file exceeds Cloudflare Pages' documented 25 MiB per-asset limit.
- **Permission:** The project owner confirmed in this task that written permission for full-site republication is available. Keep the written authorization in the project records; this note is not itself that authorization.
- **Crawler guidance:** `robots.txt` returned `User-agent: * / Allow: /` at capture time.
- **Source freshness:** The homepage response reported `Last-Modified: Tue, 01 Dec 2015`; the capture records what the host served on the capture date, not necessarily recently edited material.
- **Transport limitation:** HTTPS currently presents a `*.cloudfront.net` certificate that fails hostname validation for `star.mit.edu`. The capture therefore used the same-host HTTP endpoint rather than disabling TLS certificate validation. HTTP does not provide transport encryption or server identity verification; this limitation is recorded for provenance.
- **Included:** Same-host HTML and static assets/documents (CSS, JavaScript, images, fonts, PDF, XML/text, JNLP, spreadsheets, and linked resources such as StarCluster source archives and mailing-list attachments), with local links converted for static browsing. Four explanatory HTML stubs mark 0.92rc1 pages that returned 403.
- **Excluded:** CMS/admin routes (`/star/`, `/admin/`), external services/pages, and file types outside the crawler allowlist, including most application installers and compressed software packages.
- **Interactions:** The archive does not reproduce hosted applications, authentication, forms, or backend behavior.
- **Unavailable source paths:** The main crawl, targeted resource fetch, and legacy documentation recrawl received 29, 8, and 8 HTTP errors respectively; source responses included 403 denials, primarily legacy font files and older documentation routes. The unavailable 0.92rc1 examples, support, version, and license pages have clearly labeled archive notes; `/cluster/download.html` links to the available `/cluster/downloads.html` page instead. Decorative font assets unavailable from the source may use browser fallback fonts.
- **Static link review:** 3,967 HTML pages were checked; the audit found zero unresolved local HTML links and zero remaining absolute links to `star.mit.edu`. 84 CSS files were checked; 92 unresolved CSS references are blocked font variants (mainly old EOT files and the 0.92rc1 font set).
- **Crawler artifacts:** Wget's literal filenames for query-string variants are ignored by `.gitignore` and stored outside the publishable tree; query links resolve to canonical static pages.

Original source pages and assets may retain their own separate credits and terms. This README does not replace the authorization or license terms that apply to individual materials.
