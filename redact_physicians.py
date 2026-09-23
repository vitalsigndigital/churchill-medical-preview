#!/usr/bin/env python3
"""
Strip both physicians from the published preview.

    python redact_physicians.py          # redact docs/ in place
    python redact_physicians.py --check   # report only, change nothing

Why this exists
---------------
The preview is a public URL under Vital Sign Digital's brand, and it names
Dr. Khin Maung Myint and Dr. Samira Wahba Azer Girgis together with their CPSO
registration numbers. Those details are on a public register, but publishing
them under someone else's brand, on a site the physicians did not commission,
is the clinic's decision to make and not ours.

So the clinic needs to be able to say "take their names off" and have it
happen immediately, not "next time I rebuild". This does that in one command
and then PROVES it: the script fails loudly if a single name or registration
number survives anywhere in docs/.

This touches the preview only. The production build in the project root is
untouched, and `python preview.py` regenerates the full version.
"""

import os
import re
import sys
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

NAMES = [
    "Dr. Khin Maung Myint", "Khin Maung Myint",
    "Dr. Samira Wahba Azer Girgis", "Samira Wahba Azer Girgis",
    "Dr. Samira Girgis", "Dr. Myint", "Dr. Girgis", "Myint", "Girgis",
]
CPSO = ["80153", "82475"]


def redact_html(src):
    # 1. Drop the Physician array from the JSON-LD, keeping the JSON valid.
    src = re.sub(r',\s*"physician":\s*\[.*?\n  \]', "", src, flags=re.S)

    # 2. Replace the two doctor cards with one neutral card.
    src = re.sub(
        r'<div class="grid grid--2">(?:\s*<div class="doctor reveal">.*?</div>\s*){1,2}</div>',
        '<div class="card"><h3>Our physicians</h3><p>The clinic is staffed by family '
        'physicians registered with the College of Physicians and Surgeons of Ontario. '
        'Their details are not shown on this preview.</p></div>',
        src, flags=re.S)

    # 3. Any remaining standalone doctor card.
    src = re.sub(r'<div class="doctor reveal">.*?</div>\s*(?=<div class="doctor|</div>)', "", src, flags=re.S)

    # 4. Prose mentions.
    src = src.replace("You will be seen by Dr. Myint or Dr. Girgis", "You will be seen by one of our physicians")
    src = src.replace("Dr. Myint or Dr. Girgis", "one of our physicians")
    src = src.replace("Dr. Myint and Dr. Girgis", "our physicians")
    src = src.replace("Dr. Girgis in Arabic, Dr. Myint in Burmese", "between them")
    src = src.replace("Dr. Girgis speaks Arabic and Dr. Myint speaks Burmese",
                      "our physicians speak Arabic and Burmese between them")
    src = src.replace("The family physicians at Churchill Medical Clinic, Mississauga: "
                      "Dr. Khin Maung Myint and Dr. Samira Girgis. ",
                      "The family physicians at Churchill Medical Clinic, Mississauga. ")

    # 5. Remove every link to the removed page — nav items and body buttons
    #    alike. href is not always the first attribute, which the first version
    #    of this pattern assumed.
    src = re.sub(r'<a[^>]*href="our-doctors\.html"[^>]*>.*?</a>', "", src, flags=re.S)
    #    ...and any paragraph left holding nothing but whitespace.
    src = re.sub(r'<p[^>]*>\s*</p>', "", src)

    # 6. Anything left that still names them.
    for n in sorted(NAMES, key=len, reverse=True):
        src = src.replace(n, "our physicians")
    for c in CPSO:
        src = re.sub(r"\b" + c + r"\b", "", src)
    return src


def main():
    check = "--check" in sys.argv
    if not os.path.isdir(DOCS):
        sys.exit("docs/ not found — run `python preview.py` first.")

    pages = sorted(f for f in os.listdir(DOCS) if f.endswith(".html"))
    hits_before = {}
    for f in pages:
        s = open(os.path.join(DOCS, f), encoding="utf-8").read()
        k = sum(s.count(n) for n in ("Myint", "Girgis")) + sum(s.count(c) for c in CPSO)
        if k:
            hits_before[f] = k

    print(f"docs/ currently names the physicians on {len(hits_before)} of {len(pages)} pages")
    if check:
        for f, k in hits_before.items():
            print(f"  {f:44} {k} mention(s)")
        return 0

    doc_page = os.path.join(DOCS, "our-doctors.html")
    if os.path.exists(doc_page):
        os.remove(doc_page)
        print("  removed our-doctors.html")

    for f in sorted(x for x in os.listdir(DOCS) if x.endswith(".html")):
        p = os.path.join(DOCS, f)
        s = open(p, encoding="utf-8").read()
        out = redact_html(s)
        if out != s:
            open(p, "w", encoding="utf-8", newline="\n").write(out)

    # --- prove it ----------------------------------------------------------
    remaining, bad_json = [], []
    for f in sorted(x for x in os.listdir(DOCS) if x.endswith(".html")):
        s = open(os.path.join(DOCS, f), encoding="utf-8").read()
        for t in ("Myint", "Girgis") + tuple(CPSO):
            if t in s:
                remaining.append(f"{f}: {t}")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                bad_json.append(f"{f}: {e}")
        if 'href="our-doctors.html"' in s:
            remaining.append(f"{f}: link to removed page")

    if remaining or bad_json:
        print("\nFAILED — redaction is incomplete:")
        for r in remaining + bad_json:
            print("  x " + r)
        return 1

    print(f"\nVerified: 0 names, 0 CPSO numbers and 0 dead links across "
          f"{len([x for x in os.listdir(DOCS) if x.endswith('.html')])} pages; all JSON-LD still parses.")
    print("Commit and push docs/ to publish the redacted preview.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
