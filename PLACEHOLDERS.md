# Placeholder register — Churchill Medical Clinic

Everything on the site that is **not** confirmed by a primary source, and every
source behind the things that are. Nothing here is guesswork presented as fact;
each row says exactly how strong the evidence is.

Last updated 2026-09-17.

---

## 1. Confirmed — multiple independent sources

| Fact | Value | Sources |
|---|---|---|
| Clinic name | Churchill Medical Clinic | Peel 211, Cortico, Medimap, Doctr, CPSO |
| Address | 3050 Artesian Drive, Unit 6, Mississauga, ON L5M 7P5 | Peel 211, Doctr, **CPSO register (both physicians)** |
| Telephone | (905) 607-6495 | Peel 211, Cortico, Medimap, Doctr, CPSO |
| Fax | (905) 607-0881 | Peel 211, CPSO (both physician records) |
| Walk-in, no appointment | Yes | Peel 211, Medimap, Doctr |
| OHIP covered, no fee | Yes | Peel 211 |
| Wheelchair-accessible entrance | Yes | Peel 211 ("partially accessible; wheelchair accessible"), Doctr |
| Pharmacy adjacent | Yes | Peel 211 ("adjacent pharmacy available") |
| Neighbourhood | Churchill Meadows, near Winston Churchill Blvd & Hwy 403 | Peel 211 |

## 2. Confirmed — CPSO public register (authoritative)

Both physicians are listed on the College of Physicians and Surgeons of Ontario
register **at the clinic's exact address**, which is the strongest confirmation
available for a medical practice.

| | Dr. Khin Maung Myint | Dr. Samira Wahba Azer Girgis |
|---|---|---|
| CPSO number | 80153 | 82475 |
| Class | Independent Practice | Independent Practice |
| Registered since | 2 September 2003 | 25 May 2005 |
| Certification | CCFP, 6 June 2003 | CCFP, 8 December 2004 |
| Medical school | Mandalay Institute of Medicine, 1983 | Alexandria University Faculty of Medicine, 1979 |
| Languages | English, Burmese | English, Arabic |

Verify at `register.cpso.on.ca/physician-info/?cpsonum=80153` and `…=82475`.

## 3. PLACEHOLDER — must be confirmed before launch

| Item | Currently on the site | What is needed |
|---|---|---|
| **Domain** | `https://www.churchillmedicalclinic.ca` in canonicals, OG tags, sitemap, llms.txt | The real domain. One edit: `S["domain"]` in `build.py`, then `python pages.py`. |
| **Opening hours** | Mon–Fri 9am–7pm, Sat 9am–3pm, closed Sunday | **Sources conflict — see below.** Confirm with the clinic. |
| **Form recipient** | `REPLACE-WITH-CLINIC-EMAIL@example.com` in `contact.php` | A real monitored mailbox, and confirmation the host runs PHP. |
| **Services list** | Six categories on `services.html` | Client confirmation that each is offered and nothing important is missing. |
| **Photography** | Licensed stock (see `assets/img/CREDITS.md`) | The clinic's own photos. Shot list below. |
| **Uninsured fees** | Site says some services are not OHIP-insured and the desk quotes the fee first. No amounts given. | Confirm this is accurate; supply amounts only if the clinic wants them published. |
| **Privacy notice** | Plain-language PHIPA notice, flagged in-page as needing review | Clinic and legal sign-off. |

### The hours conflict, in full

| Source | Mon–Fri | Sat | Sun |
|---|---|---|---|
| **Peel Region 211** (record MHL0405) — *used in the build* | 9am–7pm | 9am–3pm | Closed |
| Medimap | 9am–8pm | 9am–3pm | Closed |
| Doctr | 10am–8pm | 10am–4pm | 10am–4pm |

Peel 211 was chosen because it is the municipal record and its Saturday and
Sunday agree with Medimap. Peel 211 also notes the clinic may close up to
30 minutes before the posted time, which is why every page carries "hours can
change, please call before you travel" and the walk-in page says the clinic may
stop registering patients shortly before closing.

**Hours are stored in three places and all three must be changed together:**
`build.py` → `HOURS_ROWS`, `assets/js/site.js` → `HOURS`, and the
`openingHoursSpecification` in `build.py` → `schema_clinic()`.

## 4. Deliberately excluded — do not add without confirmation

| Item | Why it was left out |
|---|---|
| **Psychiatry services** | Cortico lists "Psychiatrist and Family Doctor services". Single source, not corroborated by Peel 211, Medimap, Doctr or either CPSO record (both are family medicine). Publishing an unoffered specialty on a medical site is a real harm. |
| **French language** | Cortico lists French. CPSO records show English + Burmese (Myint) and English + Arabic (Girgis). Only the three CPSO-confirmed languages are claimed. |
| **Geo coordinates in schema** | No verified lat/long. Fabricated coordinates can misroute a patient, so `geo` is omitted and `hasMap` points to a Google Maps search for the full address instead. |
| **Accepting new patients** | Unknown and changeable. Schema omits `isAcceptingNewPatients`; the site tells people to phone and ask. |
| **Parking** | No source confirmed it. Nothing is claimed. |
| **Wait times** | Never claimed, and prohibited by the constraints in `TASKS.md`. |
| **Founding year / "serving since"** | Dr. Myint has practised in Ontario since 2003, but that is not the clinic's founding date. No date is claimed. |
| **Winston Churchill Medical Centre data** | A supplied source URL (`mississaugahaltonhealthline.ca/…id=163313`) is a **different clinic** — 6975 Meadowvale Town Centre Circle, 905-812-4874. None of its data was used. |
| **Nearest emergency department by name** | Not verified as nearest. The site says "your nearest hospital emergency department" and signposts 911 and Health811. |

## 5. Photo shot list — to replace the stock

When the clinic supplies its own photography, these are the slots, in priority
order. Filenames are the base names in `assets/img/`; `make_images.py`
regenerates the responsive WebP sizes.

| Slot | Base name | Ratio | What to shoot |
|---|---|---|---|
| 1. Hero | `hero-consultation` | 16:9 | A physician with a patient, room to the left for the headline. Landscape, well lit. |
| 2. Reception | `reception` | 4:3 | The real front desk, ideally with someone checking in. |
| 3. Waiting area | `waiting-room` | 16:9 | The actual waiting room, tidy, no identifiable patients. |
| 4. Consulting room | `walk-in-consult` | 4:3 | An exam room, either empty or with a consented model. |
| 5. Exterior | *(new slot)* | 16:9 | The unit frontage including the Churchill sign — genuinely useful for patients finding Unit 6. |
| 6–10 | `doctor-family`, `family-practice`, `chronic-care`, `senior-care`, `doctor-writing`, `vaccination` | 4:3 | Care situations. |

**Consent:** any identifiable patient needs written consent before publication.
Staff photos need staff consent. Empty rooms avoid the issue entirely and often
look better.
