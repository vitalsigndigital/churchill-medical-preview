#!/usr/bin/env python3
"""
Build the GitHub Pages preview into docs/.

    python preview.py

This is NOT the production build. It differs in three deliberate ways:

1. Every page is marked `noindex, nofollow`. The preview must never compete
   with the clinic's real site in search — and Churchill's canonical tags still
   point at a placeholder domain, so a crawlable preview would be canonicalising
   to a host that may not exist.

2. The enquiry form is rendered inert, with a notice explaining why. GitHub
   Pages serves static files and cannot execute contact.php; without this the
   browser would offer to *download* the PHP file when someone pressed Send.

3. contact.php, .htaccess, sitemap.xml and llms.txt are not emitted. None of
   them do anything useful on Pages, and shipping a sitemap for a noindex
   preview sends mixed signals.

The production build in the project root is untouched — `python pages.py` and
`python package.py` still produce the HostGator package exactly as before.
"""

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

import build
import pages


def main():
    # Start clean so a renamed page cannot linger in the published preview.
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

    build.set_output(DOCS, preview=True)
    # pages.py did `from build import *`, so its module globals hold their own
    # copies of OUT/PREVIEW taken at import time. Re-point them.
    pages.OUT = DOCS
    pages.PREVIEW = True

    for fn in (pages.build_home, pages.build_walkin, pages.build_family,
               pages.build_services, pages.build_doctors, pages.build_about,
               pages.build_faq, pages.build_contact, pages.build_local,
               pages.build_flu, pages.build_privacy, pages.build_thankyou,
               pages.build_404):
        fn()

    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DOCS, "assets"),
                    ignore=shutil.ignore_patterns("*.md"))

    # Tell GitHub Pages not to run the files through Jekyll.
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    # Crawling is ALLOWED on purpose. Disallow would stop crawlers ever reading
    # the noindex tag, and a blocked URL can still be indexed from a bare link.
    # Allow + noindex is what actually keeps a staging site out of the index.
    open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8", newline="\n").write(
        "# Design preview of Churchill Medical Clinic — not the live site.\n"
        "# Crawling is permitted so that the noindex directive on every page is\n"
        "# actually seen. Disallow would hide the noindex and achieve the opposite.\n"
        "User-agent: *\n"
        "Allow: /\n"
    )

    html = sorted(f for f in os.listdir(DOCS) if f.endswith(".html"))
    total = sum(os.path.getsize(os.path.join(dp, f))
                for dp, _, fs in os.walk(DOCS) for f in fs)

    # Verify rather than assume: every page must carry noindex, and no page may
    # still point at the PHP handler as a live form target.
    bad_index, bad_form = [], []
    for f in html:
        src = open(os.path.join(DOCS, f), encoding="utf-8").read()
        if "noindex" not in src:
            bad_index.append(f)
        if 'action="contact.php"' in src and "inert" not in src:
            bad_form.append(f)

    print(f"preview -> {DOCS}")
    print(f"  {len(html)} pages, {total/1024:.0f} KB total")
    print(f"  noindex on all pages : {'yes' if not bad_index else 'NO -> ' + ', '.join(bad_index)}")
    print(f"  live PHP form refs   : {'none' if not bad_form else 'FOUND -> ' + ', '.join(bad_form)}")
    for gone in ("contact.php", ".htaccess", "sitemap.xml", "llms.txt"):
        assert not os.path.exists(os.path.join(DOCS, gone)), f"{gone} leaked into the preview"
    print("  excluded             : contact.php, .htaccess, sitemap.xml, llms.txt")

    if bad_index or bad_form:
        sys.exit(1)


if __name__ == "__main__":
    main()
