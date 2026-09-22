#!/usr/bin/env python3
"""
Static QA for the built site. Checks the things that are cheap to get wrong and
expensive to ship: broken links, missing assets, missing alt text, heading
order, title/meta lengths, and malformed JSON-LD.

Run:  python qa.py
"""

import os
import re
import sys
import json
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = sorted(glob.glob(os.path.join(ROOT, "*.html")))

fails, warns = [], []


def fail(p, m):
    fails.append(f"{os.path.basename(p)}: {m}")


def warn(p, m):
    warns.append(f"{os.path.basename(p)}: {m}")


for path in PAGES:
    src = open(path, encoding="utf-8").read()
    name = os.path.basename(path)

    # --- title / meta description ---------------------------------------
    t = re.search(r"<title>(.*?)</title>", src, re.S)
    if not t:
        fail(path, "no <title>")
    else:
        n = len(t.group(1))
        if n > 65:
            warn(path, f"title {n} chars (>65, Google truncates)")
    d = re.search(r'<meta name="description" content="(.*?)">', src, re.S)
    if not d:
        fail(path, "no meta description")
    else:
        n = len(d.group(1))
        if not (120 <= n <= 165):
            warn(path, f"meta description {n} chars (target 120-165)")

    # --- headings --------------------------------------------------------
    h1s = re.findall(r"<h1[^>]*>", src)
    if len(h1s) != 1:
        fail(path, f"{len(h1s)} <h1> elements (want exactly 1)")
    levels = [int(m) for m in re.findall(r"<h([1-4])[ >]", src)]
    prev = 0
    for lv in levels:
        if prev and lv > prev + 1:
            warn(path, f"heading jumps h{prev} -> h{lv}")
        prev = lv

    # --- images ----------------------------------------------------------
    for tag in re.findall(r"<img\b[^>]*>", src):
        if 'alt="' not in tag:
            fail(path, "img without alt: " + tag[:90])
        elif re.search(r'alt=""', tag):
            warn(path, "img with empty alt: " + tag[:90])
        if "width=" not in tag or "height=" not in tag:
            warn(path, "img without width/height (CLS risk): " + tag[:90])
        m = re.search(r'src="([^"]+)"', tag)
        if m and not m.group(1).startswith(("http", "data:")):
            if not os.path.exists(os.path.join(ROOT, m.group(1))):
                fail(path, "missing image file: " + m.group(1))
        for ss in re.findall(r'srcset="([^"]+)"', tag):
            for cand in ss.split(","):
                f = cand.strip().split(" ")[0]
                if f and not os.path.exists(os.path.join(ROOT, f)):
                    fail(path, "missing srcset file: " + f)

    # --- internal links --------------------------------------------------
    for href in re.findall(r'href="([^"]+)"', src):
        if href.startswith(("http", "tel:", "mailto:", "#", "data:")):
            continue
        target = href.split("#")[0].split("?")[0]
        if target and not os.path.exists(os.path.join(ROOT, target)):
            fail(path, f"broken internal link: {href}")

    # --- JSON-LD ---------------------------------------------------------
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            fail(path, f"invalid JSON-LD: {e}")
            continue
        for node in data.get("@graph", [data]):
            if "@type" not in node:
                fail(path, "JSON-LD node without @type")

    # --- accessibility basics -------------------------------------------
    if 'class="skip-link"' not in src:
        fail(path, "no skip link")
    if 'lang="en-CA"' not in src:
        fail(path, "no lang attribute")
    if "user-scalable=no" in src or "maximum-scale=1" in src:
        fail(path, "viewport disables zoom")
    # A button only needs aria-label when it has no readable text of its own.
    for tag, inner in re.findall(r"(<button\b[^>]*>)(.*?)</button>", src, re.S):
        text = re.sub(r"<[^>]+>", "", inner).strip()
        if not text and "aria-label" not in tag and "aria-labelledby" not in tag:
            fail(path, "icon-only button with no accessible name: " + tag[:70])

    # --- claim constraints (client hard rules) ---------------------------
    lowered = src.lower()
    for banned, why in [
        ("private insurance", "must never imply private insurance is billed"),
        ("we accept insurance", "must never imply private insurance is billed"),
        ("best clinic", "no superlatives (CPSO advertising)"),
        ("guarantee", "no guarantees (CPSO advertising)"),
        ("no wait", "cannot promise wait times"),
        ("walk in without waiting", "cannot promise wait times"),
    ]:
        if banned in lowered:
            fail(path, f'banned phrase "{banned}" — {why}')

# --- launch blockers that live outside the HTML -----------------------------
_php = os.path.join(ROOT, "contact.php")
if os.path.exists(_php):
    _src = open(_php, encoding="utf-8").read()
    if "REPLACE-WITH" in _src or "example.com" in _src:
        warns.append("contact.php: enquiry recipient is still a PLACEHOLDER — every "
                     "submission will be lost. Set S['form_to'] in build.py.")

_ht = os.path.join(ROOT, ".htaccess")
if not os.path.exists(_ht):
    fails.append(".htaccess: missing — no custom 404, no HTTPS or canonical host redirect")
else:
    _h = open(_ht, encoding="utf-8").read()
    if "REPLACE-WITH-YOUR-DOMAIN" in _h:
        warns.append(".htaccess: canonical host still a placeholder (expected until the "
                     "domain is confirmed; run set_domain.py)")
    # A live host condition without its negation is an infinite redirect loop.
    for _l in _h.split("\n"):
        if "RewriteCond %{HTTP_HOST}" in _l and not _l.lstrip().startswith("#") and "!" not in _l:
            fails.append(".htaccess: a live RewriteCond on HTTP_HOST lost its negation — "
                         "this would redirect the canonical host to itself forever")

for _p in PAGES:
    if "churchillmedicalclinic.ca" in open(_p, encoding="utf-8").read():
        warns.append("canonical domain is still the placeholder churchillmedicalclinic.ca — "
                     "run set_domain.py with the real domain before launch")
        break

print(f"Checked {len(PAGES)} pages\n")
if fails:
    print("FAIL (%d)" % len(fails))
    for f in fails:
        print("  x " + f)
else:
    print("FAIL (0) — none")
print()
if warns:
    print("WARN (%d)" % len(warns))
    for w in warns:
        print("  ! " + w)
else:
    print("WARN (0) — none")

sys.exit(1 if fails else 0)
