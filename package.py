#!/usr/bin/env python3
"""
Build the upload package for HostGator.

    python package.py

Writes  ../Churchill-Medical-Clinic-Website.zip  (the agency root folder, per
the workspace convention that client deliverables never go to Downloads).

The archive contains the production files ONLY, at the ZIP ROOT — no wrapper
folder — so that cPanel's "Extract" drops them straight into public_html
rather than into public_html/churchill-medical/.

Excluded deliberately: the build scripts (build.py, pages.py, qa.py,
make_images.py, package.py, set_domain.py), all .md documentation, the seo/
folder and .gitignore. None of them belong on a public web server, and the
.htaccess denies them a second time in case one is ever uploaded by hand.
"""

import os
import sys
import zipfile
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(ROOT, "..", "Churchill-Medical-Clinic-Website.zip"))

# Files that must be present or the package is not shippable.
REQUIRED = [
    "index.html", "walk-in-clinic.html", "family-practice.html", "services.html",
    "our-doctors.html", "about.html", "faq.html", "contact.html",
    "walk-in-clinic-churchill-meadows.html", "flu-shots-mississauga.html",
    "privacy.html", "404.html", "thank-you.html",
    "contact.php", "robots.txt", "sitemap.xml", "llms.txt", ".htaccess",
    "assets/css/site.css", "assets/js/site.js",
    "assets/img/favicon.svg", "assets/img/apple-touch-icon.png",
    "assets/img/og-default.jpg",
]

EXCLUDE_EXT = {".py", ".md", ".pyc"}
EXCLUDE_NAMES = {".gitignore", ".DS_Store", "Thumbs.db"}
EXCLUDE_DIRS = {"__pycache__", "seo", ".git", ".claude"}


def collect():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXCLUDE_EXT or fn in EXCLUDE_NAMES:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            out.append((full, rel))
    return sorted(out, key=lambda t: t[1])


def main():
    # 1. Never package a build that fails its own checks.
    qa = os.path.join(ROOT, "qa.py")
    if os.path.exists(qa):
        r = subprocess.run([sys.executable, qa], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout)
            print("ABORTED: qa.py reported failures. Fix them before packaging.")
            raise SystemExit(1)
        print("qa.py ....... passed")

    files = collect()
    have = {rel for _, rel in files}
    missing = [r for r in REQUIRED if r not in have]
    if missing:
        print("ABORTED: required files are missing from the package:")
        for m in missing:
            print("   - " + m)
        if ".htaccess" in missing:
            print("\n   .htaccess is generated separately — see the project README.")
        raise SystemExit(1)

    # 2. Collect the things that are still placeholders, to shout about below.
    pending = []
    idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    if "churchillmedicalclinic.ca" in idx:
        pending.append(
            ("Canonical domain is still the placeholder",
             "www.churchillmedicalclinic.ca is written into every canonical tag, the\n"
             "  sitemap and the JSON-LD. Canonical tags pointing at a domain the clinic\n"
             "  does not own can cause Google to drop the real site from its index.",
             "python set_domain.py theirrealdomain.ca"))

    php = open(os.path.join(ROOT, "contact.php"), encoding="utf-8").read()
    if "REPLACE-WITH" in php or "example.com" in php:
        pending.append(
            ("Contact form recipient is still the placeholder",
             "example.com publishes a null MX record, so every enquiry a patient sends\n"
             "  is permanently undeliverable — and mail() reports success either way.",
             "set S['form_to'] in build.py, then: python pages.py && python package.py"))

    ht = open(os.path.join(ROOT, ".htaccess"), encoding="utf-8").read()
    live_block = any("RewriteRule" in l and not l.lstrip().startswith("#")
                     for l in ht.split("\n"))
    if not live_block:
        pending.append(
            ("HTTPS / canonical-host redirects are OFF (this is intentional)",
             "They are commented out so the site stays testable on HostGator's temporary\n"
             "  URL, and so nobody is redirected to https before the SSL certificate is\n"
             "  issued. Turn them on only after the real domain loads with a padlock.",
             "python set_domain.py theirrealdomain.ca --enable-redirects"))

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for full, rel in files:
            z.write(full, rel)

    raw = sum(os.path.getsize(f) for f, _ in files)
    print(f"\nPackaged {len(files)} files")
    print(f"  {'source':<28}{raw/1024:8.0f} KB")
    print(f"  {'compressed':<28}{os.path.getsize(OUT)/1024:8.0f} KB")
    print(f"  -> {OUT}")

    groups = {}
    for _, rel in files:
        key = rel.split("/")[0] if "/" in rel else os.path.splitext(rel)[1] or rel
        groups[key] = groups.get(key, 0) + 1
    print("\nContents:")
    for k in sorted(groups):
        print(f"  {k:<28}{groups[k]:4} file(s)")

    if pending:
        print("\n" + "=" * 72)
        print("BEFORE THIS GOES LIVE — %d item(s) still to settle" % len(pending))
        print("=" * 72)
        for i, (title, why, how) in enumerate(pending, 1):
            print(f"\n{i}. {title}")
            print("  " + why)
            print(f"  ->  {how}")
        print("\n" + "=" * 72)
        print("The zip is still valid and uploadable — you can put it on the server")
        print("and test it today. Just settle these before pointing the public at it.")
        print("=" * 72)


if __name__ == "__main__":
    main()
