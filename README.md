# Churchill Medical Clinic — website

A static site for a walk-in clinic and family practice at 3050 Artesian Drive,
Unit 6, Mississauga. Twelve pages, no framework, no build toolchain beyond
Python and Pillow.

## Build

```
python pages.py
```

Regenerates every `.html` file, plus `sitemap.xml`, `robots.txt`, `llms.txt` and
`contact.php`.

**Do not hand-edit the generated `.html` files** — they are overwritten on every
build.

| File | What it holds |
|---|---|
| `build.py` | Business facts (`S`, `HOURS_ROWS`, `DOCTORS`), page chrome, icons, reusable components, JSON-LD |
| `pages.py` | The copy for each page, and the entry point |
| `make_images.py` | Generates `apple-touch-icon.png` and `og-default.jpg` from the logo geometry and hero photo |
| `qa.py` | Static checks — run before every deploy |
| `assets/css/site.css` | The whole design system |
| `assets/js/site.js` | Progressive enhancement only |

Change a fact once in `build.py` and it updates on every page, in the footer, in
the hours table and in the structured data simultaneously. That is the point of
the generator: NAP drift across pages is the most common defect on small
business sites, and here it is structurally impossible.

## Preview site

    python preview.py

Builds a separate copy into `docs/`, which GitHub Pages serves at
**https://vitalsigndigital.github.io/churchill-medical-preview/**

This is *not* the production build, and differs in three deliberate ways:

- **Every page is `noindex, nofollow`.** A preview must never compete with the
  clinic's real site in search. Churchill's canonical tags still point at a
  placeholder domain, so a crawlable preview would be canonicalising to a host
  that may not exist.
- **The enquiry form is rendered inert**, with a notice saying why. Pages serves
  static files and cannot execute `contact.php`; without this, pressing Send
  would offer to *download* the PHP file.
- **`contact.php`, `.htaccess`, `sitemap.xml` and `llms.txt` are omitted.** None
  of them do anything on Pages, and a sitemap for a noindex site is a mixed
  signal.

`robots.txt` in the preview deliberately **allows** crawling. `Disallow` would
stop crawlers ever reading the `noindex`, and a blocked URL can still be indexed
from a bare link — allow + noindex is what actually keeps a staging site out.

`package.py` excludes `docs/` from the HostGator zip, so the preview can never
be uploaded to production by accident.

## Checks

```
python qa.py
```

Verifies internal links resolve, image files exist, every image has alt text,
headings do not skip levels, titles and meta descriptions are in range, JSON-LD
parses, and no banned claim phrasing has crept into the copy (see the hard
constraints in `TASKS.md`).

HTML was additionally validated against the W3C Nu validator — all 12 pages
return 0 errors and 0 warnings:

```
curl -s -H "Content-Type: text/html; charset=utf-8" --data-binary "@index.html" \
  "https://validator.w3.org/nu/?out=json"
```

## Local preview

```
python -m http.server 4186
```

Then open `http://localhost:4186`. The contact form needs PHP, so it will not
submit against `http.server`; everything else works.

## Design

- **Type** — Newsreader (display) + Inter (UI). A serif headline reads
  established and authoritative, which suits a practice whose physicians have
  been registered in Ontario for twenty years; it also separates the site from
  the all-sans template look.
- **Colour** — derived from the clinic's own signage blue (`--brand-700 #0F4C9B`),
  with a navy ink and a single green reserved for the live "open" state. Every
  foreground/background pair was measured in-browser; there are no contrast
  failures at any breakpoint.
- **Images** — one house treatment: aspect-ratio-locked figures so nothing shifts
  while loading, a thin offset brand frame for editorial blocks, and hover
  effects that only ever touch `transform` and `opacity`.
- **Motion** — 200ms interface transitions, one scroll reveal. All of it is
  behind `html.js` and `prefers-reduced-motion`, so the page renders completely
  with scripting off.

## Things worth knowing before you change something

- **Opening hours live in three places** and must be changed together:
  `HOURS_ROWS` in `build.py`, `HOURS` in `assets/js/site.js`, and
  `openingHoursSpecification` in `schema_clinic()`. The hours themselves are not
  yet client-confirmed — see `PLACEHOLDERS.md`.
- **The open/closed badge is computed at view time** in `America/Toronto`, never
  at build time, so it is right for a visitor in any timezone and can never go
  stale. `window.clinicStatusFor({day, minutes})` exposes the logic for testing.
- **No content is injected by JavaScript.** Every heading, answer and NAP detail
  is in the served HTML so that AI crawlers, which mostly do not execute JS, read
  the page in full.
- **Claim constraints are enforced by `qa.py`.** OHIP only — never imply private
  insurance; no superlatives, guarantees, testimonials or wait-time promises.
  These are regulatory, not stylistic: CPSO advertising rules govern physician
  marketing in Ontario.

## Status

Built, not launched. `PLACEHOLDERS.md` lists everything still to be confirmed by
the client — the domain, the opening hours, the form recipient and the services
list are the four that block launch.
