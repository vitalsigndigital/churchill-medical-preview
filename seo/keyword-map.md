# Keyword map — Churchill Medical Clinic

One page owns one primary intent; no two pages compete for the same query.

Judgements below are **based on SERP inspection and local-intent reasoning, not
volume data** — no keyword tool was used, and the client supplied no Google Ads
or Search Console exports. If those exports become available, rebuild this table
around real converting terms before adding any further pages.

| URL | Primary keyword | Secondary | Intent | Title (chars) | Primary CTA | Schema |
|---|---|---|---|---|---|---|
| `/` | walk-in clinic Mississauga | walk-in clinic Churchill Meadows, no appointment doctor Mississauga | Commercial / local | 55 | Call | MedicalClinic, WebSite, FAQPage |
| `/walk-in-clinic.html` | walk-in clinic Mississauga no appointment | walk-in clinic Artesian Drive, walk-in doctor near me | Commercial / local | 54 | Call | MedicalClinic, BreadcrumbList, FAQPage |
| `/walk-in-clinic-churchill-meadows.html` | walk-in clinic Churchill Meadows | walk-in clinic L5M, clinic near Winston Churchill and 403 | Local | 56 | Call | MedicalClinic, BreadcrumbList |
| `/family-practice.html` | family doctor Mississauga | family practice Churchill Meadows, accepting new patients Mississauga | Commercial | 56 | Call | MedicalClinic, BreadcrumbList |
| `/services.html` | walk-in clinic services Mississauga | prescription refill, medical forms, lab requisition | Informational → commercial | 57 | Call | MedicalClinic, BreadcrumbList |
| `/our-doctors.html` | Dr Khin Maung Myint / Dr Samira Girgis | family physician Mississauga CPSO | Navigational / trust | 51 | Call | MedicalClinic + Physician, BreadcrumbList |
| `/flu-shots-mississauga.html` | flu shot Mississauga | flu vaccine Churchill Meadows, free flu shot Ontario | Seasonal commercial | 50 | Call | MedicalClinic, BreadcrumbList |
| `/about.html` | Churchill Medical Clinic | clinic Artesian Drive Mississauga | Brand | 52 | Call | MedicalClinic, BreadcrumbList |
| `/faq.html` | walk-in clinic questions Mississauga | do I need an appointment, is it covered by OHIP | Informational | 51 | Call | MedicalClinic, BreadcrumbList, FAQPage |
| `/contact.html` | Churchill Medical Clinic phone / address | directions, opening hours | Navigational | 46 | Call | MedicalClinic, BreadcrumbList |
| `/privacy.html` | — | — | Legal | 50 | — | MedicalClinic, BreadcrumbList |

## Internal linking

Hub: `/walk-in-clinic.html` is the money page. `/` and every spoke link into it.

- `/` → walk-in clinic, family practice, services, our doctors, FAQ
- `/services.html` → flu shots, walk-in clinic
- `/walk-in-clinic-churchill-meadows.html` → walk-in clinic (hub), contact
- `/flu-shots-mississauga.html` → services
- Every page → contact, and a tap-to-call CTA in the header, body and sticky mobile bar

## GEO / AI-visibility notes

- Every fact — hours, address, coverage, languages, physician credentials — is in
  the raw server-delivered HTML. No content is injected by JavaScript, so
  retrieval systems that do not execute JS still read the page in full.
- `llms.txt` restates the clinic's key facts in plain prose, including an explicit
  "Not available at this clinic" section, so an assistant answering "can I get an
  X-ray at Churchill Medical Clinic" has a correct answer to cite.
- FAQ content is marked up as `FAQPage` and phrased as direct answers to the
  questions patients actually ask.
- Physician `identifier` values carry CPSO numbers, which ties the entities to a
  public register an assistant can corroborate against.

## Deliberately not built

- No location pages for neighbourhoods the clinic does not serve. A single
  Churchill Meadows page is legitimate because the clinic is physically in it;
  spinning up "walk-in clinic Oakville" pages for a clinic on Artesian Drive
  would be doorway content and would eventually be penalised.
- No page targets "urgent care" or "emergency" — the clinic is neither, and
  ranking for those terms would bring the wrong patients through the door.
