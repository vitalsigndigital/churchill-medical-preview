#!/usr/bin/env python3
"""
Churchill Medical Clinic — static site builder.

Produces plain .html files. Nothing is rendered client-side: every heading,
paragraph, FAQ answer, NAP detail and JSON-LD block below is written into the
served HTML, so AI crawlers that do not execute JavaScript still read the page
in full.

Run:  python build.py
"""

import os
import re
import html
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))


def _asset_version():
    """Content hash of the CSS+JS, stamped onto their URLs.

    Without this, site.js can outlive the HTML in a browser cache — and site.js
    carries the opening-hours table that drives the live open/closed badge, so a
    stale copy shows a patient the wrong hours. Fingerprinting lets the server
    cache these files hard while guaranteeing a changed file is a changed URL.
    """
    import hashlib
    h = hashlib.sha256()
    for rel in ("assets/css/site.css", "assets/js/site.js"):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            h.update(open(p, "rb").read())
    return h.hexdigest()[:10]


ASSET_V = _asset_version()

# Where generated files are written. Defaults to the project root (the
# production build that package.py zips for HostGator). preview.py points it
# at docs/ to produce the GitHub Pages copy instead.
OUT = ROOT

# Preview mode marks every page noindex and disables the PHP contact form,
# because GitHub Pages cannot execute PHP and a preview must never compete
# with the real site in search.
PREVIEW = False


def set_output(directory, preview=False):
    global OUT, PREVIEW
    OUT = directory
    PREVIEW = preview
    os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# Single source of truth for every business fact on the site.
# Sources are recorded in PLACEHOLDERS.md. Change a fact here, rebuild, and it
# updates on every page and in every schema block at once.
# ---------------------------------------------------------------------------
S = {
    "name": "Churchill Medical Clinic",
    "domain": "https://www.churchillmedicalclinic.ca",  # PLACEHOLDER — confirm
    "street": "3050 Artesian Drive, Unit 6",
    "street_short": "3050 Artesian Drive",
    "unit": "Unit 6",
    "city": "Mississauga",
    "region": "ON",
    "region_long": "Ontario",
    "postal": "L5M 7P5",
    "country": "CA",
    "phone_display": "(905) 607-6495",
    "phone_tel": "+19056076495",
    "fax_display": "(905) 607-0881",
    "neighbourhood": "Churchill Meadows",
    "languages": ["English", "Arabic", "Burmese"],
    "maps_query": "Churchill+Medical+Clinic+3050+Artesian+Drive+Unit+6+Mississauga+ON+L5M+7P5",
    # Where the website enquiry form delivers. PLACEHOLDER — qa.py fails while
    # this is unset, because a form that posts into a void is worse than no form.
    "form_to": "REPLACE-WITH-CLINIC-EMAIL@example.com",
    "form_from_local": "noreply",
}
S["address_one_line"] = f'{S["street"]}, {S["city"]}, {S["region"]} {S["postal"]}'
S["maps_url"] = f'https://www.google.com/maps/search/?api=1&query={S["maps_query"]}'
S["apple_maps_url"] = f'https://maps.apple.com/?q={S["maps_query"]}'

# Hours — Peel Region 211 record MHL0405. Mirrored in assets/js/site.js.
HOURS_ROWS = [
    (1, "Monday", "9:00am – 7:00pm"),
    (2, "Tuesday", "9:00am – 7:00pm"),
    (3, "Wednesday", "9:00am – 7:00pm"),
    (4, "Thursday", "9:00am – 7:00pm"),
    (5, "Friday", "9:00am – 7:00pm"),
    (6, "Saturday", "9:00am – 3:00pm"),
    (0, "Sunday", "Closed"),
]

DOCTORS = [
    {
        "name": "Dr. Khin Maung Myint",
        "role": "Family Physician",
        "cpso": "80153",
        "school": "Mandalay Institute of Medicine, 1983",
        "cert": "Certificant, College of Family Physicians of Canada (2003)",
        "since": "Independent practice in Ontario since September 2003",
        "langs": "English, Burmese",
    },
    {
        "name": "Dr. Samira Wahba Azer Girgis",
        "role": "Family Physician",
        "cpso": "82475",
        "school": "Alexandria University Faculty of Medicine, 1979",
        "cert": "Certificant, College of Family Physicians of Canada (2004)",
        "since": "Independent practice in Ontario since May 2005",
        "langs": "English, Arabic",
    },
]

NAV = [
    ("index.html", "Home"),
    ("walk-in-clinic.html", "Walk-In Clinic"),
    ("family-practice.html", "Family Practice"),
    ("services.html", "Services"),
    ("our-doctors.html", "Our Doctors"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]

# ---------------------------------------------------------------------------
# Icons — Lucide (ISC licence). One family, 1.75 stroke, 24px grid throughout.
# ---------------------------------------------------------------------------
_I = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "map-pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "stethoscope": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
    "syringe": '<path d="m18 2 4 4"/><path d="m17 7 3-3"/><path d="M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5"/><path d="m9 11 4 4"/><path d="m5 19-3 3"/><path d="m14 4 6 6"/>',
    "baby": '<path d="M9 12h.01"/><path d="M15 12h.01"/><path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5"/><path d="M19 6.3a9 9 0 0 1 1.8 3.9 2 2 0 0 1 0 3.6 9 9 0 0 1-17.6 0 2 2 0 0 1 0-3.6A9 9 0 0 1 12 3c2 0 3.5.5 5 1.5"/>',
    "heart-pulse": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 13H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "pill": '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "menu": '<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "printer": '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect width="12" height="8" x="6" y="14" rx="1"/>',
    "accessibility": '<circle cx="16" cy="4" r="1"/><path d="m18 19 1-7-6 1"/><path d="m5 8 3-3 5.5 3-2.36 3.5"/><path d="M4.24 14.5a5 5 0 0 0 6.88 6"/><path d="M13.76 17.5a5 5 0 0 0-6.88-6"/>',
    "languages": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "bandage": '<path d="M10 10.01h.01"/><path d="M10 14.01h.01"/><path d="M14 10.01h.01"/><path d="M14 14.01h.01"/><path d="M18 6v11.5"/><path d="M6 6v12"/><rect width="20" height="12" x="2" y="6" rx="6"/>',
    "thermometer": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "card": '<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>',
}


def icon(name, cls=""):
    """Always emits class="ic" so every icon has a sane default size even where
    no component rule targets it (the mobile drawer taught us this)."""
    body = _I[name]
    c = ("ic " + cls).strip()
    return (
        f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>'
    )


def caduceus(height="32"):
    """Inline brand mark so it inherits currentColor and needs no extra request."""
    p = os.path.join(ROOT, "assets", "img", "caduceus.svg")
    raw = open(p, encoding="utf-8").read()
    inner = raw.split(">", 1)[1].rsplit("</svg>", 1)[0].strip()
    # The mark is rendered more than once per page (header and footer), so the
    # <g id>/<use> pair in the source file would produce duplicate IDs. Expand
    # the mirrored wing inline instead: no IDs, no collision.
    wing = re.search(r'<g id="wing">(.*?)</g>', inner, re.S)
    if wing:
        paths = wing.group(1)
        inner = inner.replace(wing.group(0), f"<g>{paths}</g>")
        inner = re.sub(r'<use href="#wing"[^/]*/>',
                       f'<g transform="translate(120,0) scale(-1,1)">{paths}</g>', inner)
    return (
        f'<svg viewBox="0 0 120 205" fill="none" style="height:{height}px" '
        f'aria-hidden="true" focusable="false">{inner}</svg>'
    )


# ---------------------------------------------------------------------------
# Shared chrome
# ---------------------------------------------------------------------------
TEL_BTN = (
    f'<a class="btn" href="tel:{S["phone_tel"]}" data-cta="call">'
    f'{icon("phone")}<span>Call {S["phone_display"]}</span></a>'
)


def status_pill(on_dark=False):
    """Server-rendered fallback text; JS replaces it with the live state."""
    cls = "status status--onDark" if on_dark else "status"
    return (
        f'<span class="{cls}" data-status-pill>'
        f'<span class="status__dot"></span>'
        f'<span data-status-text>Mon&ndash;Fri 9am&ndash;7pm &middot; Sat 9am&ndash;3pm</span></span>'
    )


def head(page, title, desc, extra_schema=""):
    _robots = ("noindex, nofollow" if PREVIEW
               else "index, follow, max-image-preview:large, max-snippet:-1")
    canonical = f'{S["domain"]}/{page}' if page != "index.html" else f'{S["domain"]}/'
    og_img = f'{S["domain"]}/assets/img/og-default.jpg'
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{_robots}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{S['name']}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_CA">
<meta property="og:image" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<meta name="theme-color" content="#0F4C9B">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Mississauga">

<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap">
<link rel="stylesheet" href="assets/css/site.css?v={ASSET_V}">
<script>document.documentElement.classList.add("js");</script>
{extra_schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
""" + (preview_banner() if PREVIEW else "")


def preview_banner():
    """Shown only on the GitHub Pages preview.

    That URL is public and carries the clinic's name, address, telephone and
    both physicians' CPSO numbers, so it must never be mistakable for the
    clinic's own approved website.
    """
    return f"""<div class="previewbar" role="note">
  <div class="previewbar__in">
    <strong>Design preview</strong> by Vital Sign Digital &mdash; this is not the official website of
    {S['name']}, and the clinic has not approved it. Details shown here are unconfirmed.
    For hours and services, telephone <a href="tel:{S['phone_tel']}">{S['phone_display']}</a>.
  </div>
</div>
"""


def header(page):
    nav_links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a>'
        for h, t in NAV
    )
    drawer_links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}{icon("arrow-right")}</a>'
        for h, t in NAV
    )
    return f"""<header class="header">
  <div class="container">
    <div class="header__bar">
      <a class="brand" href="index.html" aria-label="{S['name']} — home">
        <span class="brand__mark">{caduceus(32)}</span>
        <span class="brand__text">
          <span class="brand__name">Churchill</span>
          <span class="brand__sub">Medical Clinic</span>
        </span>
      </a>
      <nav class="nav" aria-label="Primary">{nav_links}</nav>
      <a class="btn header__cta" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>{S['phone_display']}</span></a>
      <button class="nav-toggle" type="button" aria-expanded="false"
              aria-controls="mobile-drawer" aria-label="Open menu">
        <span class="icon-open">{icon("menu")}</span><span class="icon-close">{icon("x")}</span>
      </button>
    </div>
    <div class="drawer" id="mobile-drawer" data-open="false">
      <nav aria-label="Mobile">{drawer_links}</nav>
      <a class="btn btn--block" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
    </div>
  </div>
</header>
"""


def crumbs(page, label):
    if page == "index.html":
        return ""
    return f"""<div class="container"><nav class="crumbs" aria-label="Breadcrumb">
  <ol><li><a href="index.html">Home</a></li><li aria-current="page">{label}</li></ol>
</nav></div>
"""


def footer():
    hours_list = "".join(f"<li>{d} <span style='float:right'>{h}</span></li>" for _, d, h in HOURS_ROWS)
    quick = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[1:6])
    year = datetime.date.today().year
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <a class="footer__brand" href="index.html">
          <span class="brand__mark">{caduceus(32)}</span>
          <span class="brand__text">
            <span class="brand__name">Churchill</span>
            <span class="brand__sub">Medical Clinic</span>
          </span>
        </a>
        <p>A walk-in and family practice clinic in {S['neighbourhood']}, {S['city']}. Most visits are covered by OHIP &mdash; bring your health card.</p>
        <p><strong style="color:#fff">In an emergency, call 911</strong> or go to your nearest hospital emergency department.</p>
      </div>
      <div>
        <h3>Visit</h3>
        <ul>
          <li>{S['street']}<br>{S['city']}, {S['region']} {S['postal']}</li>
          <li><a href="{S['maps_url']}" rel="noopener">Get directions</a></li>
          <li><a href="tel:{S['phone_tel']}">{S['phone_display']}</a></li>
          <li>Fax {S['fax_display']}</li>
        </ul>
      </div>
      <div>
        <h3>Clinic</h3>
        <ul>{quick}</ul>
      </div>
      <div>
        <h3>Hours</h3>
        <ul>{hours_list}</ul>
        <p style="margin-top:16px;font-size:.8125rem">Hours can change. Please call before you travel.</p>
      </div>
    </div>
    <div class="footer__bottom">
      <p style="margin:0">&copy; {year} {S['name']}. All rights reserved.</p>
      <nav aria-label="Legal">
        <a href="privacy.html">Privacy &amp; PHIPA</a>
        <a href="contact.html">Contact</a>
        <a href="faq.html">FAQ</a>
      </nav>
    </div>
  </div>
</footer>

<div class="callbar">
  <a class="btn" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call clinic</span></a>
  <a class="btn btn--ghost" href="{S['maps_url']}" rel="noopener">{icon("map-pin")}<span>Directions</span></a>
</div>

<script src="assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def page(name, title, desc, body, crumb_label=None, schema=""):
    out = head(name, title, desc, schema)
    out += header(name)
    if crumb_label:
        out += crumbs(name, crumb_label)
    out += f'<main id="main">\n{body}\n</main>\n'
    out += footer()
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    return out


# ---------------------------------------------------------------------------
# Reusable content blocks
# ---------------------------------------------------------------------------
def picture(base, alt, ratio="4x3", widths=(480, 800, 1280), sizes="(min-width:900px) 50vw, 100vw",
            cls="", loading="lazy", zoom=False):
    srcset = ", ".join(f"assets/img/{base}-{w}.webp {w}w" for w in widths)
    w, h = (4, 3) if ratio == "4x3" else (16, 9) if ratio == "16x9" else (3, 2)
    zc = " figure--zoom" if zoom else ""
    return (
        f'<div class="figure figure--{ratio}{zc} {cls}">'
        f'<img src="assets/img/{base}-800.webp" srcset="{srcset}" sizes="{sizes}" '
        f'alt="{html.escape(alt)}" width="{w*200}" height="{h*200}" '
        f'loading="{loading}" decoding="async">'
        f"</div>"
    )


def hours_table():
    rows = "".join(
        f'<tr data-day="{i}"><th scope="row">{d}</th><td>{h}</td></tr>'
        for i, d, h in HOURS_ROWS
    )
    return f'<table class="hours"><caption class="sr-only">Opening hours</caption><tbody>{rows}</tbody></table>'


def emergency_notice():
    return f"""<h2 class="sr-only">Emergency and after-hours care</h2>
<div class="notice notice--warn">
  {icon("alert")}
  <p><strong>This clinic is not an emergency department.</strong> If you have chest pain, trouble breathing,
  severe bleeding, signs of a stroke, or any other emergency, call <strong>911</strong> or go to your nearest
  hospital emergency department. For free health advice any time of day, call Health811 by dialling <strong>811</strong>.</p>
</div>"""


def cta_band(heading, text, primary_note=""):
    return f"""<section class="section section--brand">
  <div class="container container--mid" style="text-align:center">
    <h2>{heading}</h2>
    <p class="lede" style="margin-inline:auto;max-width:56ch">{text}</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:32px">
      <a class="btn btn--onDark btn--lg" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
      <a class="btn btn--ghostOnDark btn--lg" href="{S['maps_url']}" rel="noopener">{icon("map-pin")}<span>Get directions</span></a>
    </div>
    {f'<p style="margin-top:24px;font-size:.9375rem">{primary_note}</p>' if primary_note else ''}
  </div>
</section>"""


def preview_form_notice():
    """Shown only on the GitHub Pages preview, where there is no PHP to run."""
    if not PREVIEW:
        return ""
    return f"""    <div class="notice" style="margin-bottom:32px">
      {icon("info")}
      <p><strong>This is a design preview.</strong> The enquiry form below is shown for layout only
      and is switched off here, because this preview is served as static files with no mail handling.
      It works normally on the live site. To reach the clinic now, call
      <a href="tel:{S['phone_tel']}">{S['phone_display']}</a>.</p>
    </div>
"""


SERVICES = [
    ("thermometer", "Everyday illness",
     "Coughs, colds, sore throats, fevers, flu symptoms, ear and eye infections, urinary tract infections, "
     "skin rashes and other common infections."),
    ("bandage", "Minor injuries",
     "Sprains and strains, minor cuts and grazes, minor burns, bruising, and wound care and dressing changes."),
    ("pill", "Prescriptions and refills",
     "New prescriptions where appropriate and refills of an existing medication. There is a pharmacy next to the clinic."),
    ("syringe", "Vaccinations and flu shots",
     "Seasonal flu shots and routine publicly funded immunisations, subject to availability."),
    ("file-text", "Forms, notes and requisitions",
     "Medical notes, routine forms and laboratory requisitions. Some of these are not covered by OHIP &mdash; "
     "please ask the front desk before your appointment."),
    ("heart-pulse", "Ongoing and follow-up care",
     "Blood pressure and routine monitoring, review of results, follow-up on an earlier visit, and referrals "
     "to a specialist when they are needed."),
]


def services_grid(limit=None):
    items = SERVICES[:limit] if limit else SERVICES
    cards = "".join(
        f'<div class="service reveal"><span class="service__icon">{icon(i)}</span>'
        f"<div><h3>{t}</h3><p>{d}</p></div></div>"
        for i, t, d in items
    )
    return f'<div class="grid grid--3">{cards}</div>'


def doctors_cards():
    out = []
    for d in DOCTORS:
        out.append(f"""<div class="doctor reveal">
  <h3 class="doctor__name">{d['name']}</h3>
  <p class="doctor__role">{d['role']}</p>
  <dl class="doctor__meta">
    <div class="doctor__row"><dt>CPSO number</dt><dd>{d['cpso']}</dd></div>
    <div class="doctor__row"><dt>Certification</dt><dd>{d['cert']}</dd></div>
    <div class="doctor__row"><dt>Medical school</dt><dd>{d['school']}</dd></div>
    <div class="doctor__row"><dt>In practice</dt><dd>{d['since']}</dd></div>
    <div class="doctor__row"><dt>Languages</dt><dd>{d['langs']}</dd></div>
  </dl>
</div>""")
    return f'<div class="grid grid--2">{"".join(out)}</div>'


# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
def schema_clinic():
    return """{
  "@type": "MedicalClinic",
  "@id": "%(domain)s/#clinic",
  "name": "%(name)s",
  "url": "%(domain)s/",
  "telephone": "%(phone)s",
  "faxNumber": "%(fax)s",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "%(street)s",
    "addressLocality": "%(city)s",
    "addressRegion": "%(region)s",
    "postalCode": "%(postal)s",
    "addressCountry": "CA"
  },
  "areaServed": [
    {"@type": "City", "name": "Mississauga"},
    {"@type": "Place", "name": "Churchill Meadows"}
  ],
  "hasMap": "%(maps)s",
  "medicalSpecialty": ["PrimaryCare", "FamilyPractice"],
  "availableService": [
    {"@type": "MedicalProcedure", "name": "Walk-in care for minor illness and injury"},
    {"@type": "MedicalProcedure", "name": "Family practice and follow-up care"},
    {"@type": "MedicalProcedure", "name": "Vaccinations and flu shots"},
    {"@type": "MedicalProcedure", "name": "Prescriptions and refills"}
  ],
  "paymentAccepted": "OHIP",
  "currenciesAccepted": "CAD",
  "knowsLanguage": ["en", "ar", "my"],
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
     "opens": "09:00", "closes": "19:00"},
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": "Saturday", "opens": "09:00", "closes": "15:00"}
  ],
  "physician": [
    {"@type": "Physician", "name": "Dr. Khin Maung Myint",
     "medicalSpecialty": "FamilyPractice",
     "identifier": {"@type": "PropertyValue", "propertyID": "CPSO", "value": "80153"},
     "knowsLanguage": ["en","my"]},
    {"@type": "Physician", "name": "Dr. Samira Wahba Azer Girgis",
     "medicalSpecialty": "FamilyPractice",
     "identifier": {"@type": "PropertyValue", "propertyID": "CPSO", "value": "82475"},
     "knowsLanguage": ["en","ar"]}
  ]
}""" % {
        "domain": S["domain"], "name": S["name"], "phone": S["phone_display"],
        "fax": S["fax_display"], "street": S["street"], "city": S["city"],
        "region": S["region"], "postal": S["postal"], "maps": S["maps_url"],
    }


def schema_block(page, extra=None):
    """One @graph per page: the clinic entity, the page, and breadcrumbs."""
    nodes = [schema_clinic()]
    nodes.append("""{
  "@type": "WebSite",
  "@id": "%(d)s/#website",
  "url": "%(d)s/",
  "name": "%(n)s",
  "publisher": {"@id": "%(d)s/#clinic"},
  "inLanguage": "en-CA"
}""" % {"d": S["domain"], "n": S["name"]})

    if page != "index.html":
        label = dict(NAV).get(page, "")
        nodes.append("""{
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "%(d)s/"},
    {"@type": "ListItem", "position": 2, "name": "%(l)s", "item": "%(d)s/%(p)s"}
  ]
}""" % {"d": S["domain"], "l": label, "p": page})

    if extra:
        nodes.append(extra)

    graph = ",\n".join(nodes)
    return f'<script type="application/ld+json">\n{{\n"@context": "https://schema.org",\n"@graph": [\n{graph}\n]\n}}\n</script>'


FAQS = [
    ("Do I need an appointment?",
     "No. Churchill Medical Clinic is a walk-in clinic, so you can come in during opening hours without booking. "
     "Calling ahead on {phone} is still worth doing &mdash; the front desk can tell you how busy the clinic is and "
     "confirm that a physician is in."),
    ("What does a visit cost?",
     "If you have a valid Ontario health card, your visit is covered by OHIP and there is nothing to pay. "
     "A small number of services are not insured by OHIP &mdash; certain notes, forms and letters, for example. "
     "The front desk will tell you the fee before anything is done."),
    ("What should I bring?",
     "Your Ontario health card, a list of the medications you take (including anything you buy over the counter), "
     "and details of any allergies. If you are following up on an earlier problem, bring any results or letters you have."),
    ("Is the clinic taking new family practice patients?",
     "This changes from time to time, so please call the clinic on {phone} and ask. We would rather tell you honestly "
     "on the phone than have you travel in and be turned away."),
    ("What languages are spoken at the clinic?",
     "English, Arabic and Burmese. Dr. Girgis speaks Arabic and Dr. Myint speaks Burmese."),
    ("Is the clinic wheelchair accessible?",
     "The clinic has a wheelchair-accessible entrance. If you have a specific access need, please call ahead "
     "on {phone} so the front desk can help."),
    ("Can you prescribe or refill my medication?",
     "A physician can issue a new prescription where it is clinically appropriate, and can refill an existing "
     "medication after reviewing it with you. Bring the medication or its packaging with you if you can. "
     "There is a pharmacy next to the clinic."),
    ("What if I need care when the clinic is closed?",
     "For anything urgent or life-threatening, call 911 or go to your nearest hospital emergency department. "
     "For health advice at any hour, you can call Health811 free by dialling 811."),
]


def faq_items(limit=None):
    items = FAQS[:limit] if limit else FAQS
    out = []
    for q, a in items:
        a = a.format(phone=f'<a href="tel:{S["phone_tel"]}">{S["phone_display"]}</a>')
        out.append(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>")
    return f'<div class="faq">{"".join(out)}</div>'


def faq_schema(limit=None):
    items = FAQS[:limit] if limit else FAQS
    entries = []
    for q, a in items:
        plain = a.format(phone=S["phone_display"])
        plain = re.sub(r"<[^>]+>", "", plain).replace("&mdash;", "—").replace('"', "'")
        entries.append(
            '{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}'
            % (q.replace('"', "'"), plain)
        )
    return '{\n"@type": "FAQPage",\n"mainEntity": [\n%s\n]\n}' % ",\n".join(entries)
