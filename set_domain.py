#!/usr/bin/env python3
"""
Point the whole site at the real domain, then rebuild and repackage.

    python set_domain.py churchillmedicalclinic.ca
    python set_domain.py www.churchillmedicalclinic.ca

This is the one command that has to be run before the site goes live. It
rewrites the canonical host in build.py and regenerates every page, which
updates:

  - <link rel="canonical"> on all 12 pages
  - og:url and og:image on all 12 pages
  - every <loc> in sitemap.xml
  - the page list and URLs in llms.txt
  - the @id / url fields in the JSON-LD
  - the host rules in .htaccess

Shipping with the wrong canonical host is not a cosmetic problem: canonical
tags pointing at a domain the clinic does not own can cause Google to drop
the real site from its index.
"""

import os
import re
import sys
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))


def fail(msg):
    print("ERROR: " + msg)
    raise SystemExit(1)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(1)

    raw = sys.argv[1].strip().rstrip("/")
    raw = re.sub(r"^https?://", "", raw)
    if not re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw):
        fail(f"{raw!r} does not look like a domain (expected e.g. churchillmedicalclinic.ca)")

    host = raw.lower()
    bare = host[4:] if host.startswith("www.") else host
    use_www = host.startswith("www.")
    canonical = f"https://{host}"

    # --- 1. build.py: the canonical host every page is generated from -------
    bp = os.path.join(ROOT, "build.py")
    src = open(bp, encoding="utf-8").read()
    new, n = re.subn(
        r'("domain":\s*")[^"]+(")(,\s*#[^\n]*)?',
        lambda m: m.group(1) + canonical + m.group(2) + ",",
        src,
        count=1,
    )
    if not n:
        fail("could not find the domain entry in build.py")
    open(bp, "w", encoding="utf-8", newline="\n").write(new)
    print(f"build.py       canonical host -> {canonical}")

    # --- 2. .htaccess: fill in the host and switch the canonical block on ---
    #
    # The block ships commented out so the site stays testable on HostGator's
    # temporary URL and so no visitor is redirected to https before the
    # certificate exists. Enabling it is a deliberate step, not a default.
    hp = os.path.join(ROOT, ".htaccess")
    if os.path.exists(hp):
        h = open(hp, encoding="utf-8").read()

        if "--enable-redirects" in sys.argv or os.environ.get("CMC_ENABLE_REDIRECTS"):
            def uncomment(m):
                body = m.group(2)
                out = []
                for line in body.split("\n"):
                    st = line.lstrip()
                    if st.startswith("# "):
                        out.append(line.replace("# ", "", 1))
                    elif st == "#":
                        out.append(line.replace("#", "", 1))
                    else:
                        out.append(line)
                return m.group(1) + "\n".join(out) + m.group(3)

            h, n = re.subn(r"(--- START canonical block ---\n)(.*?)(#? ?--- END canonical block ---)",
                           uncomment, h, flags=re.S)
            state = "ENABLED" if n else "block markers not found"
        else:
            state = "left disabled (pass --enable-redirects once DNS and SSL are live)"

        h = h.replace("REPLACE-WITH-YOUR-DOMAIN", host)
        open(hp, "w", encoding="utf-8", newline="\n").write(h)

        # The negation is load-bearing: without the leading "!" the condition
        # matches the canonical host and redirects it to itself forever.
        active = [l for l in h.split("\n")
                  if "RewriteCond %{HTTP_HOST}" in l and not l.lstrip().startswith("#")]
        for line in active:
            if "!" not in line:
                fail("the .htaccess host condition lost its negation — this would "
                     "cause an infinite redirect loop. Restore the leading '!' before uploading.")
        if "REPLACE-WITH-YOUR-DOMAIN" in h:
            fail("a REPLACE-WITH-YOUR-DOMAIN placeholder survived in .htaccess")

        print(f".htaccess      host -> {host}; redirects {state}")
    else:
        print(".htaccess      not found — skipped")

    # --- 3. rebuild + repackage -------------------------------------------
    for step, script in (("rebuild", "pages.py"), ("verify", "qa.py"), ("repackage", "package.py")):
        p = os.path.join(ROOT, script)
        if not os.path.exists(p):
            continue
        r = subprocess.run([sys.executable, p], cwd=ROOT, capture_output=True, text=True)
        tail = (r.stdout or r.stderr).strip().splitlines()
        print(f"\n--- {step} ({script}) ---")
        for line in tail[-12:]:
            print("  " + line)
        if r.returncode != 0:
            fail(f"{script} exited {r.returncode}")

    print(f"\nDone. The site now canonicalises to {canonical}")
    print("Re-upload the regenerated zip, and make sure the domain's DNS points at HostGator.")


if __name__ == "__main__":
    main()
