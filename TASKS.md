# Churchill Medical Clinic — Tasks

**Status:** PACKAGED for HostGator + live preview on GitHub Pages; awaiting domain, form mailbox and hours confirmation
**Live URL:** not live. Preview: https://vitalsigndigital.github.io/churchill-medical-preview/ (noindex)
**Repo:** https://github.com/vitalsigndigital/churchill-medical-preview
**Last worked:** 2026-09-22

## Open
- [ ] Swap the canonical domain once known: `python set_domain.py therealdomain.ca`. Rewrites canonicals, OG URLs, sitemap, llms.txt, JSON-LD and the `.htaccess` host, then rebuilds and repacks in one pass.
- [ ] After DNS + AutoSSL are live, enable the redirects: `python set_domain.py therealdomain.ca --enable-redirects`, then flip both `[R=302,L]` to `[R=301,L]` once a clean single-hop redirect is confirmed.
- [ ] Set the enquiry recipient: `S["form_to"]` in `build.py` (currently the `example.com` placeholder), then `python pages.py && python package.py`. Also create `noreply@<domain>` in cPanel and run Email Deliverability so SPF/DKIM align — see §7 of the upload guide, including the Email Routing trap if the clinic is on Google Workspace or Microsoft 365.
- [ ] Replace the licensed stock photography with the clinic's own photos when supplied — shot list is in `PLACEHOLDERS.md`. Drop new files into `assets/img/`, re-run `python make_images.py` if the hero changes.
- [ ] After launch: submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools; ping IndexNow.
- [ ] After launch: re-run the W3C validator and a Lighthouse pass against the live origin (both were run against the local build only).

## Waiting on client
- [ ] **Opening hours — blocking for accuracy.** Three public sources disagree: Peel 211 says Mon–Fri 9am–7pm / Sat 9am–3pm (used in the build); Medimap says Mon–Fri 9am–8pm; Doctr says Mon–Fri 10am–8pm and Sat–Sun 10am–4pm. Confirm the real hours. They appear in `build.py` (`HOURS_ROWS`), `assets/js/site.js` (`HOURS`) and the JSON-LD — all three must match.
- [ ] Confirm the services list on `services.html` is accurate and complete, and whether anything listed is not actually offered.
- [ ] **Psychiatry** — Cortico lists the clinic as offering psychiatrist as well as family doctor services. Single source, so it was deliberately left off the site. Confirm before adding.
- [ ] Confirm whether the practice is accepting new family practice patients (the site currently tells people to phone and ask, which is safe either way).
- [ ] Confirm uninsured-service fees exist and whether the clinic wants them published. No amounts are stated anywhere on the site.
- [ ] Confirm parking arrangements — nothing is claimed on the site because no source confirmed it.
- [ ] Confirm the adjacent pharmacy's relationship to the clinic (site says only that there is a pharmacy next to the clinic; it does not imply common ownership).
- [ ] Client/physician sign-off on all medical-adjacent copy, and legal review of `privacy.html`.
- [ ] Google Business Profile: confirm NAP matches the site exactly, add the website URL once live.
- [ ] Confirm French is or is not spoken (Cortico lists it; CPSO records only English + Arabic + Burmese, so French was excluded).

## Done
- [x] 2026-09-22 — **Published a client preview** at https://vitalsigndigital.github.io/churchill-medical-preview/ and put the project in its own public repo (matching the `deca-health-preview` / `rahat-foundation` convention). All 13 pages verified live, custom 404 serving a real 404 status, WebP served as `image/webp`, no console errors.
- [x] 2026-09-22 — Added `preview.py`: builds a separate `docs/` copy that is `noindex` on every page with the PHP form rendered inert, and omits `contact.php`/`.htaccess`/`sitemap.xml`/`llms.txt`. The preview's robots.txt deliberately *allows* crawling, since Disallow would stop crawlers reading the noindex and achieve the opposite.
- [x] 2026-09-22 — **`TASKS.md` is excluded from the public repo** (it records engagement status) but stays tracked in the private workspace repo via a gitignore negation, so the internal record survives without being published.
- [x] 2026-09-22 — Caught two packaging faults before they shipped: `page()` had not picked up the new output directory, so a preview build silently overwrote 11 production pages with `noindex`; and `package.py` would have bundled the whole `docs/` preview into the HostGator zip. Both fixed and verified.
- [x] 2026-09-22 — Pinned LF line endings with `.gitattributes` so the Windows checkout cannot hand Apache CRLF files.
- [x] 2026-09-17 — **Packaged for HostGator.** `Churchill-Medical-Clinic-Website.zip` (60 files, 1.6 MB, flat at the zip root so cPanel Extract lands it in `public_html`) plus `Churchill-Medical-HostGator-Upload-Guide.md`, both in the agency root. `package.py` builds it, refuses to run if `qa.py` fails, excludes all build scripts and internal docs, and prints the outstanding launch blockers.
- [x] 2026-09-17 — Wrote `.htaccess`: custom 404, WebP/SVG MIME types, guarded compression, caching, security headers, no-store on the form handler, deny rules for `*.py`/`*.md`. **Canonical/HTTPS redirects ship commented out on purpose** so the site stays testable on HostGator's temporary URL and nobody hits https before AutoSSL issues; they also ship as 302 rather than 301 while the domain is unsettled.
- [x] 2026-09-17 — Ran a 6-agent audit (portability, .htaccess authoring, mail deliverability, then three adversarial lenses on the .htaccess). **Portability came back clean: 0 case mismatches across 427 resolved asset paths**, 0 absolute paths, 0 BOMs, all LF, and the detector was self-tested against planted fixtures (3/3 caught) so the pass is real rather than a silent regex failure.
- [x] 2026-09-17 — **Found and fixed a bug in my own `set_domain.py`**: its `.htaccess` regex dropped the leading `!` from the host condition, which would have inverted the rule into an infinite redirect loop. Rewritten, and `qa.py` now fails the build if any live `RewriteCond %{HTTP_HOST}` loses its negation.
- [x] 2026-09-17 — Fixed a real UX defect: `contact.php` redirected to `contact.html?sent=1` but nothing ever read that flag, so a patient submitted the form and saw no acknowledgement at all. Added a proper `thank-you.html` (works with JavaScript disabled) and an inline error banner that tells people to phone instead.
- [x] 2026-09-17 — Hardened the mail path: `From` is now a build-time constant instead of the client-controlled `HTTP_HOST`; added the `-f` envelope sender so SPF and DMARC align rather than authenticating a hostgator.com hostname; added `MIME-Version`; removed `novalidate` so browsers still validate the form without JavaScript.
- [x] 2026-09-17 — Added content-hash fingerprinting (`site.css?v=…`, `site.js?v=…`). This mattered: `site.js` carries the opening-hours table that drives the live open/closed badge, and it was cacheable for longer than the HTML, so a stale copy could have shown a patient the wrong hours.
- [x] 2026-09-17 — Built the full site: 12 pages (home, walk-in clinic, family practice, services, our doctors, about, FAQ, contact, Churchill Meadows local page, flu shots, privacy, 404), plus `sitemap.xml`, `robots.txt`, `llms.txt` and `contact.php`.
- [x] 2026-09-17 — Verified both physicians against the CPSO public register, which lists **both at 3050 Artesian Drive, Unit 6**: Dr. Khin Maung Myint (CPSO 80153, CCFP 2003, Mandalay Institute of Medicine 1983, independent practice since Sept 2003, English + Burmese) and Dr. Samira Wahba Azer Girgis (CPSO 82475, CCFP 2004, Alexandria University 1979, independent practice since May 2005, English + Arabic). No credential on the site is inferred.
- [x] 2026-09-17 — **Caught that one of the supplied source URLs is a different clinic.** `mississaugahaltonhealthline.ca/displayservice.aspx?id=163313` is Winston Churchill Medical Centre, 6975 Meadowvale Town Centre Circle, 905-812-4874 — different business, address and phone. Excluded entirely; none of its data reached the build.
- [x] 2026-09-17 — Rebuilt the logo from the exterior-sign photograph as clean SVG: `caduceus.svg` (full mark), `caduceus-compact.svg` (holds legibility at 16–32px where the full mark dissolves), `favicon.svg`, `logo-badge.svg` (sign lockup). Rendered and visually checked at 16/24/32/48px before accepting.
- [x] 2026-09-17 — Design system in `assets/css/site.css`: tokens derived from the signage blue, Newsreader + Inter, 4/8px spacing, one elevation scale, house image treatment (aspect-locked figures, editorial offset frame, transform-only hover).
- [x] 2026-09-17 — Live "Open now / Closed" status computed at view time in `America/Toronto`, so it is correct for a visitor in any timezone and never stale. Unit-tested against 13 boundary cases including Saturday 3pm correctly reporting "opens Monday" rather than "tomorrow".
- [x] 2026-09-17 — Licensed 10 photographs (Pexels, free commercial licence) and generated 34 responsive WebP files, 1.47 MB total, largest hero 92 KB. Reviewed every candidate visually first and rejected two that would have shipped brand damage: one carried Russian signage, another showed a different clinic's logo.
- [x] 2026-09-17 — **W3C Nu validator: 0 errors and 0 warnings across all 12 pages.** Fixed a real duplicate-ID error (the brand mark's `<g id>`/`<use>` pair collided when rendered twice per page) and added headings to three headingless sections.
- [x] 2026-09-17 — Accessibility verified in-browser: 0 contrast failures at desktop and 375px, no targets below the WCAG 2.2 AA 24px minimum, no horizontal overflow, skip links, visible focus rings, form errors bound to their fields with focus moved to the first invalid one.
- [x] 2026-09-17 — Fixed three defects found by rendering rather than by reading code: the hero scrim was opaque enough to flatten the photograph entirely; unconstrained icon SVGs rendered enormous in the mobile drawer; and an unscoped `.drawer a` rule hijacked the drawer's call button, giving it dark text on a blue field.
- [x] 2026-09-17 — Made scroll-reveal fail safe: `.reveal` is scoped to `html.js`, so with scripting off the page renders in full instead of leaving sections invisible.
- [x] 2026-09-17 — `qa.py` static checker added (links, assets, alt text, heading order, title/meta length, JSON-LD validity, and the banned-claims list). Passes with 0 failures and 0 warnings.

## Notes
**Hard constraints (re-check these in QA before every deploy):**
- **OHIP only.** Never imply private insurance is billed or accepted. `paymentAccepted` in the schema is `OHIP` and nothing else.
- **No superlatives, no guarantees, no patient testimonials** — CPSO advertising rules apply to physician marketing in Ontario.
- **Never promise a wait time**, or imply walk-in means no waiting.
- **No invented credentials.** Everything on `our-doctors.html` is traceable to the CPSO public register.
- Emergency signposting (911 + Health811) must stay on the home, walk-in, services, FAQ, flu-shot and Churchill Meadows pages.
- `qa.py` enforces the banned-phrase list automatically — run it after any copy change.

**Build:** `python pages.py` regenerates every page. Never hand-edit the `.html` files; they are generated and edits will be overwritten. Facts live in `build.py` (`S`, `HOURS_ROWS`, `DOCTORS`); copy lives in `pages.py`.
