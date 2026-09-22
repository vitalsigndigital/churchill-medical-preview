#!/usr/bin/env python3
"""
Churchill Medical Clinic — page content.

Run this to build the site:   python pages.py
Shared facts, chrome and components live in build.py.
"""

from build import *   # noqa: F401,F403


# ===========================================================================
# Home
# ===========================================================================
def build_home():
    body = f"""
<section class="hero">
  <div class="hero__media">
    <img src="assets/img/hero-consultation-1280.webp"
         srcset="assets/img/hero-consultation-480.webp 480w,
                 assets/img/hero-consultation-800.webp 800w,
                 assets/img/hero-consultation-1280.webp 1280w,
                 assets/img/hero-consultation-1920.webp 1920w"
         sizes="100vw" width="1920" height="1080"
         alt="A family physician talking with a parent and child across a consulting room desk"
         fetchpriority="high" decoding="async">
  </div>
  <div class="hero__scrim"></div>
  <div class="container">
    <div class="hero__inner">
      {status_pill(on_dark=True)}
      <h1 style="margin-top:24px">Your walk-in clinic in Churchill Meadows</h1>
      <p class="hero__lede">No appointment needed. Two family physicians see patients six days a week
      for everyday illness and minor injuries &mdash; covered by OHIP, on Artesian Drive.</p>
      <div class="hero__actions">
        <a class="btn btn--onDark btn--lg" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
        <a class="btn btn--ghostOnDark btn--lg" href="walk-in-clinic.html"><span>How a visit works</span>{icon("arrow-right")}</a>
      </div>
      <div class="hero__meta">
        <span>{icon("map-pin")}{S['street']}, {S['city']}</span>
        <span>{icon("card")}Covered by OHIP</span>
        <span>{icon("languages")}English &middot; Arabic &middot; Burmese</span>
      </div>
    </div>
  </div>
</section>

<div class="container">
  <div class="infocard">
    <h2 class="sr-only">Clinic address, hours and telephone</h2>
    <div class="infocard__grid">
      <div class="infocard__item">
        <span class="icon-tile">{icon("map-pin")}</span>
        <div>
          <h3>Find us</h3>
          <p>{S['street']}<br>{S['city']}, {S['region']} {S['postal']}<br>
          <a href="{S['maps_url']}" rel="noopener">Get directions</a></p>
        </div>
      </div>
      <div class="infocard__item">
        <span class="icon-tile">{icon("clock")}</span>
        <div>
          <h3>Opening hours</h3>
          <p>Monday to Friday, 9am&ndash;7pm<br>Saturday, 9am&ndash;3pm<br>Closed Sunday</p>
        </div>
      </div>
      <div class="infocard__item">
        <span class="icon-tile">{icon("phone")}</span>
        <div>
          <h3>Speak to the clinic</h3>
          <p><a href="tel:{S['phone_tel']}">{S['phone_display']}</a><br>
          Fax {S['fax_display']}<br>
          Call ahead to check how busy we are.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">Walk in, don't wait weeks</span>
      <h2>Seen today, not next month</h2>
      <p class="lede">You do not need to be a registered patient and you do not need to book.
      Come in during opening hours, bring your health card, and one of our physicians will see you.</p>
    </div>
    <ol class="steps reveal">
      <li>
        <h3>Come in during opening hours</h3>
        <p>Arrive any time the clinic is open. Earlier in the day and earlier in the week are usually quieter.</p>
      </li>
      <li>
        <h3>Register at the front desk</h3>
        <p>Hand over your Ontario health card. The front desk will take a few details and explain the wait.</p>
      </li>
      <li>
        <h3>See a physician</h3>
        <p>You will be seen by Dr. Myint or Dr. Girgis, who will examine you, treat you, and arrange any
        prescription, test or referral you need.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">What we treat</span>
      <h2>Everyday medical care, close to home</h2>
      <p class="lede">The kinds of problems our physicians see most often. If you are not sure whether we can
      help with something, call the clinic first &mdash; we would rather tell you on the phone than have you
      make the journey for nothing.</p>
    </div>
    {services_grid()}
    <p style="margin-top:32px"><a class="btn btn--ghost" href="services.html"><span>See all services</span>{icon("arrow-right")}</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="split__media figure-frame">
        {picture("doctor-family", "A physician in discussion with a parent and their child during an appointment", "4x3")}
      </div>
      <div class="split__body">
        <span class="eyebrow">Family practice</span>
        <h2>Care that carries on after today</h2>
        <p>A walk-in visit solves the immediate problem. Some things need following up &mdash; blood pressure that
        needs watching, a result to go over, a referral to chase, a long-term condition to keep steady.</p>
        <p>Churchill Medical Clinic is a family practice as well as a walk-in clinic, so the same physicians can
        look after that continuing care. Whether the clinic is taking new family practice patients changes from
        time to time, so please call and ask.</p>
        <p style="margin-top:32px"><a class="btn btn--ghost" href="family-practice.html"><span>About our family practice</span>{icon("arrow-right")}</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container container--mid">
    {emergency_notice()}
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Your physicians</span>
      <h2>Two family doctors, both on the public register</h2>
      <p class="lede">Every credential below can be checked against the College of Physicians and Surgeons of
      Ontario public register, which lists both physicians at this address.</p>
    </div>
    {doctors_cards()}
    <p style="margin-top:32px"><a class="btn btn--ghost" href="our-doctors.html"><span>More about our doctors</span>{icon("arrow-right")}</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--reverse">
      <div class="split__media figure-frame figure-frame--right">
        {picture("reception", "A patient checking in with a receptionist at a clinic front desk", "4x3")}
      </div>
      <div class="split__body">
        <span class="eyebrow">Before you come</span>
        <h2>What to bring with you</h2>
        <ul class="ticklist" style="margin-bottom:24px">
          <li>{icon("check")}<span>Your Ontario health card &mdash; this is what makes the visit free</span></li>
          <li>{icon("check")}<span>A list of every medication you take, including anything bought over the counter</span></li>
          <li>{icon("check")}<span>Details of any allergies, especially to medication</span></li>
          <li>{icon("check")}<span>Any results, letters or paperwork relating to the problem</span></li>
          <li>{icon("check")}<span>For a child, their health card and immunisation record if you have it</span></li>
        </ul>
        <p>If you have lost your health card or it has expired, come in anyway and speak to the front desk.
        They will tell you where you stand before you are seen.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container container--mid">
    <div class="section-head section-head--center">
      <span class="eyebrow">Common questions</span>
      <h2>Before you visit</h2>
    </div>
    {faq_items(limit=5)}
    <p style="margin-top:32px;text-align:center"><a class="btn btn--ghost" href="faq.html"><span>All questions</span>{icon("arrow-right")}</a></p>
  </div>
</section>

{cta_band("Feeling unwell today?",
          "Walk in during opening hours, or call the front desk first to check how busy the clinic is.",
          "Hours can change at short notice. A quick call before you travel is always worth it.")}
"""
    page("index.html",
         "Walk-In Clinic in Mississauga | Churchill Medical Clinic",
         "Walk-in clinic in Churchill Meadows, Mississauga. No appointment needed for everyday illness and "
         "minor injuries. Open six days a week and covered by OHIP.",
         body, schema=schema_block("index.html", extra=faq_schema(limit=5)))


# ===========================================================================
# Walk-in clinic
# ===========================================================================
def build_walkin():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Walk-in clinic</span>
    <h1>Walk-in clinic in Mississauga &mdash; no appointment needed</h1>
    <p class="lede">Churchill Medical Clinic treats everyday illnesses and minor injuries on a walk-in basis,
    six days a week, at {S['street']} in {S['neighbourhood']}. You do not need to be a registered patient.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:32px;align-items:center">
      <a class="btn" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
      <a class="btn btn--ghost" href="{S['maps_url']}" rel="noopener">{icon("map-pin")}<span>Get directions</span></a>
      {status_pill()}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="split__body">
        <span class="eyebrow">What we can help with</span>
        <h2>Problems we see every day</h2>
        <p>Most walk-in visits are for something that has come on in the last few days and cannot wait for a
        scheduled appointment. Our physicians will examine you, treat what they can on the spot, and arrange a
        prescription, a laboratory requisition or a referral where one is needed.</p>
        <ul class="ticklist ticklist--2">
          <li>{icon("check")}<span>Coughs, colds and flu symptoms</span></li>
          <li>{icon("check")}<span>Sore throats and fevers</span></li>
          <li>{icon("check")}<span>Ear and eye infections</span></li>
          <li>{icon("check")}<span>Urinary tract infections</span></li>
          <li>{icon("check")}<span>Skin rashes and minor infections</span></li>
          <li>{icon("check")}<span>Sprains, strains and minor injuries</span></li>
          <li>{icon("check")}<span>Minor cuts, grazes and burns</span></li>
          <li>{icon("check")}<span>Wound care and dressing changes</span></li>
          <li>{icon("check")}<span>Prescription refills</span></li>
          <li>{icon("check")}<span>Flu shots and routine immunisations</span></li>
        </ul>
      </div>
      <div class="split__media figure-frame">
        {picture("walk-in-consult", "A physician listening to a patient during a walk-in consultation", "4x3")}
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container container--mid">
    {emergency_notice()}
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">How it works</span>
      <h2>A walk-in visit, start to finish</h2>
    </div>
    <ol class="steps reveal">
      <li><h3>Arrive during opening hours</h3>
        <p>There is no booking system to work around. The clinic is generally quietest earlier in the day and
        earlier in the week; late afternoons and Saturdays tend to be busier.</p></li>
      <li><h3>Register and wait</h3>
        <p>Give your Ontario health card to the front desk. They will register you and let you know roughly how
        long the wait is likely to be, so you can decide whether to stay.</p></li>
      <li><h3>See the physician</h3>
        <p>You will be seen by Dr. Myint or Dr. Girgis. If you need a prescription, a test or a referral to a
        specialist, that is arranged during the visit.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--2">
      <div>
        <h2>Opening hours</h2>
        <p>The clinic is open six days a week and closed on Sundays.</p>
        {hours_table()}
        <p style="margin-top:24px;font-size:.9375rem;color:var(--ink-3)">Hours can change, and the clinic may
        stop registering new walk-in patients shortly before closing so that everyone waiting can be seen.
        Please call {S['phone_display']} before you travel, particularly late in the day.</p>
      </div>
      <div>
        <h2>What a visit costs</h2>
        <p>If you have a valid Ontario health card, your walk-in visit is <strong>covered by OHIP</strong> and
        there is nothing to pay.</p>
        <p>A small number of services are not insured by OHIP &mdash; certain notes, letters and third-party
        forms, for example. Where that applies, the front desk will tell you the fee <em>before</em> anything is
        done, so there are no surprises.</p>
        <div class="notice" style="margin-top:24px">
          {icon("info")}
          <p><strong>No health card?</strong> Come in and speak to the front desk. They will explain your options
          before you are seen rather than after.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container container--mid">
    <div class="section-head section-head--center">
      <span class="eyebrow">Common questions</span>
      <h2>Walk-in questions</h2>
    </div>
    {faq_items(limit=4)}
  </div>
</section>

{cta_band("Walk in when you need to be seen",
          "Open Monday to Friday 9am to 7pm and Saturday 9am to 3pm, at 3050 Artesian Drive, Unit 6.")}
"""
    page("walk-in-clinic.html",
         "Walk-In Clinic Mississauga, No Appointment | Churchill",
         "Walk-in clinic at 3050 Artesian Drive, Mississauga. Colds, infections, minor injuries and "
         "prescriptions, no appointment needed. OHIP covered.",
         body, crumb_label="Walk-In Clinic",
         schema=schema_block("walk-in-clinic.html", extra=faq_schema(limit=4)))


# ===========================================================================
# Family practice
# ===========================================================================
def build_family():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Family practice</span>
    <h1>Family practice care in Churchill Meadows</h1>
    <p class="lede">Alongside the walk-in clinic, Dr. Myint and Dr. Girgis provide continuing family practice
    care &mdash; the kind that follows a problem through rather than closing the file at the end of the visit.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="split__media figure-frame">
        {picture("doctor-writing", "A family physician making notes while two patients sit across the desk", "4x3")}
      </div>
      <div class="split__body">
        <h2>Why continuity matters</h2>
        <p>A physician who already knows your history does not have to start from the beginning. They know which
        medications you have tried, what your blood pressure has been doing over the last year, and what
        &ldquo;normal&rdquo; looks like for you.</p>
        <p>That context is what turns a series of separate appointments into actual care. It is also what makes
        it easier to catch the thing that has quietly changed.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Ongoing care</span>
      <h2>What family practice covers</h2>
      <p class="lede">The continuing side of general practice, provided by the same two physicians who staff
      the walk-in clinic.</p>
    </div>
    <div class="grid grid--3">
      <div class="service reveal"><span class="service__icon">{icon("heart-pulse")}</span>
        <div><h3>Long-term conditions</h3><p>Routine review and monitoring of ongoing conditions, including
        blood pressure checks and regular follow-up.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("file-text")}</span>
        <div><h3>Results and follow-up</h3><p>Going through laboratory results with you, explaining what they
        mean, and deciding together what happens next.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("route")}</span>
        <div><h3>Referrals to specialists</h3><p>Referral to a specialist or hospital service when your care
        needs to go beyond what a family practice can provide.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("pill")}</span>
        <div><h3>Medication review</h3><p>Reviewing what you are taking, why, and whether it is still the right
        thing &mdash; then issuing repeat prescriptions.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("syringe")}</span>
        <div><h3>Immunisations</h3><p>Seasonal flu shots and routine publicly funded immunisations for adults
        and children, subject to availability.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("baby")}</span>
        <div><h3>Care for the whole family</h3><p>Both physicians are certificants in family medicine and see
        patients of all ages, from children through to older adults.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--reverse">
      <div class="split__media figure-frame figure-frame--right">
        {picture("senior-care", "A physician reviewing notes at a computer with an older patient", "4x3")}
      </div>
      <div class="split__body">
        <h2>Are you taking new patients?</h2>
        <p>This is the question we are asked most, and the honest answer is that it changes. Rather than publish
        something here that may be out of date by the time you read it, please call the clinic on
        <a href="tel:{S['phone_tel']}">{S['phone_display']}</a> and ask the front desk directly.</p>
        <p>If the practice is full at the time you call, Health Care Connect &mdash; the Ontario government's
        service for finding a family doctor or nurse practitioner &mdash; is the next place to try.</p>
        <p style="margin-top:32px"><a class="btn" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call and ask</span></a></p>
      </div>
    </div>
  </div>
</section>

{cta_band("Looking for continuing care?",
          "Call the clinic to ask about family practice availability, or walk in for something that needs seeing to today.")}
"""
    page("family-practice.html",
         "Family Practice in Mississauga | Churchill Medical Clinic",
         "Family practice care in Churchill Meadows, Mississauga. Long-term condition reviews, results, "
         "referrals and medication reviews from two family physicians.",
         body, crumb_label="Family Practice", schema=schema_block("family-practice.html"))


# ===========================================================================
# Services
# ===========================================================================
def build_services():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Services</span>
    <h1>Services at Churchill Medical Clinic</h1>
    <p class="lede">Primary care for everyday problems, provided on a walk-in basis and through our family
    practice. Most of what follows is covered by OHIP when you present a valid Ontario health card.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="sr-only">Services offered</h2>
    {services_grid()}
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="split">
      <div class="split__body">
        <span class="eyebrow">Immunisation</span>
        <h2>Flu shots and routine vaccinations</h2>
        <p>Seasonal influenza vaccination is available at the clinic each autumn, along with routine publicly
        funded immunisations, subject to supply.</p>
        <p>Availability changes through the season, so call {S['phone_display']} to check before you travel.</p>
        <p style="margin-top:32px"><a class="btn btn--ghost" href="flu-shots-mississauga.html"><span>About flu shots</span>{icon("arrow-right")}</a></p>
      </div>
      <div class="split__media figure-frame">
        {picture("vaccination", "A nurse giving a vaccination in a patient's upper arm", "4x3")}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--mid">
    <h2>What we cannot do here</h2>
    <p>Being straight about the limits of a walk-in clinic saves people a wasted journey. Churchill Medical
    Clinic is a primary care practice, not a hospital or an urgent care centre.</p>
    <ul>
      <li><strong>Emergencies.</strong> Chest pain, difficulty breathing, severe bleeding, signs of a stroke,
      serious injury &mdash; call 911 or go to a hospital emergency department.</li>
      <li><strong>On-site imaging or laboratory testing.</strong> We can issue a requisition so you can have
      bloodwork or imaging done at a laboratory or imaging centre, but it is not carried out at the clinic.</li>
      <li><strong>Specialist treatment.</strong> Where a problem needs a specialist, our physicians will refer
      you rather than treat it here.</li>
    </ul>
    <p>If you are not certain whether we are the right place, call the clinic on
    <a href="tel:{S['phone_tel']}">{S['phone_display']}</a> and describe the problem. The front desk will tell
    you honestly whether to come in.</p>
    <div style="margin-top:32px">{emergency_notice()}</div>
  </div>
</section>

{cta_band("Not sure if we can help?",
          "One phone call will tell you. The front desk would rather redirect you than have you wait for nothing.")}
"""
    page("services.html",
         "Medical Services in Mississauga | Churchill Medical Clinic",
         "Services at Churchill Medical Clinic, Mississauga: walk-in care for illness and minor injury, "
         "prescriptions, vaccinations, forms and family practice.",
         body, crumb_label="Services", schema=schema_block("services.html"))


# ===========================================================================
# Our doctors
# ===========================================================================
def build_doctors():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Our doctors</span>
    <h1>The physicians at Churchill Medical Clinic</h1>
    <p class="lede">Two family physicians, both certificants of the College of Family Physicians of Canada and
    both listed at this address on the CPSO public register. Every detail below can be independently verified.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="sr-only">Our physicians</h2>
    {doctors_cards()}
    <div class="notice" style="margin-top:40px">
      {icon("shield-check")}
      <p><strong>Check us yourself.</strong> Every physician licensed in Ontario appears on the College of
      Physicians and Surgeons of Ontario public register, searchable by name or CPSO number at
      <a href="https://register.cpso.on.ca" rel="noopener">register.cpso.on.ca</a>. We publish our CPSO numbers
      so you can look us up in a few seconds.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="split">
      <div class="split__media figure-frame">
        {picture("family-practice", "A physician examining a child with a stethoscope while a parent watches", "4x3")}
      </div>
      <div class="split__body">
        <h2>Care in more than one language</h2>
        <p>Explaining a symptom is hard enough in your first language. Between them, our physicians consult in
        <strong>English, Arabic and Burmese</strong> &mdash; Dr. Girgis in Arabic, Dr. Myint in Burmese.</p>
        <p>If you would prefer to be seen by a particular physician, say so when you register at the front desk.
        They will tell you whether that doctor is in and what the wait looks like.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("Come and see us",
          "Walk in during opening hours, or call the clinic to ask about family practice availability.")}
"""
    page("our-doctors.html",
         "Our Doctors | Churchill Medical Clinic, Mississauga",
         "The family physicians at Churchill Medical Clinic, Mississauga: Dr. Khin Maung Myint and "
         "Dr. Samira Girgis. Consultations in English, Arabic and Burmese.",
         body, crumb_label="Our Doctors", schema=schema_block("our-doctors.html"))


# ===========================================================================
# About
# ===========================================================================
def build_about():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">About the clinic</span>
    <h1>A neighbourhood clinic in Churchill Meadows</h1>
    <p class="lede">Churchill Medical Clinic is a walk-in and family practice on Artesian Drive, near the corner
    of Winston Churchill Boulevard and Highway 403, serving the western side of Mississauga.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="split__body">
        <h2>Primary care without the wait for an appointment</h2>
        <p>Most medical problems are not emergencies, but they are not things that can wait three weeks either.
        A child with an ear infection, a chest infection that is not shifting, a sprained ankle, a prescription
        that has run out &mdash; these need seeing to within a day or two.</p>
        <p>That is the gap a walk-in clinic fills. You come in when you need to be seen, a family physician
        examines you, and the problem gets dealt with. Because the clinic is also a family practice, anything
        that needs following up can be followed up here too.</p>
      </div>
      <div class="split__media figure-frame figure-frame--right">
        {picture("waiting-room", "A bright, clean clinic waiting area with seating", "16x9")}
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="grid grid--3">
      <div class="service reveal"><span class="service__icon">{icon("card")}</span>
        <div><h3>Covered by OHIP</h3><p>With a valid Ontario health card there is nothing to pay for an insured
        visit. Where a service is not insured, you will be told the fee before it is provided.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("languages")}</span>
        <div><h3>Three languages</h3><p>Consultations in English, Arabic and Burmese, which matters in a
        neighbourhood as mixed as this one.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("accessibility")}</span>
        <div><h3>Accessible entrance</h3><p>The clinic has a wheelchair-accessible entrance. Call ahead if you
        have a specific access need and the front desk will help.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("pill")}</span>
        <div><h3>Pharmacy next door</h3><p>There is a pharmacy beside the clinic, so a prescription can usually
        be filled without a second journey.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("users")}</span>
        <div><h3>All ages</h3><p>Both physicians are certificants in family medicine and see patients of every
        age, from young children to older adults.</p></div></div>
      <div class="service reveal"><span class="service__icon">{icon("clock")}</span>
        <div><h3>Six days a week</h3><p>Open Monday to Friday until 7pm, and Saturday mornings and early
        afternoons. Closed on Sundays.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--2">
      <div>
        <h2>Where to find us</h2>
        <p>{S['street']}<br>{S['city']}, {S['region_long']} {S['postal']}</p>
        <p>The clinic sits in {S['neighbourhood']}, on the western edge of Mississauga near the Winston Churchill
        Boulevard and Highway 403 interchange, close to the Halton boundary.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px">
          <a class="btn btn--ghost" href="{S['maps_url']}" rel="noopener">{icon("map-pin")}<span>Google Maps</span></a>
          <a class="btn btn--ghost" href="{S['apple_maps_url']}" rel="noopener">{icon("route")}<span>Apple Maps</span></a>
        </div>
      </div>
      <div>
        <h2>Opening hours</h2>
        {hours_table()}
        <p style="margin-top:24px;font-size:.9375rem;color:var(--ink-3)">Hours can change. Please call
        {S['phone_display']} before you travel.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("We are on Artesian Drive",
          "Walk in during opening hours, or call the front desk if you would like to check something first.")}
"""
    page("about.html",
         "About Churchill Medical Clinic | Mississauga Walk-In",
         "A walk-in and family practice on Artesian Drive in Churchill Meadows, Mississauga. OHIP "
         "covered, wheelchair-accessible entrance, open six days a week.",
         body, crumb_label="About", schema=schema_block("about.html"))


# ===========================================================================
# FAQ
# ===========================================================================
def build_faq():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Questions</span>
    <h1>Frequently asked questions</h1>
    <p class="lede">The things patients ask the front desk most often. If your question is not here,
    call the clinic on <a href="tel:{S['phone_tel']}">{S['phone_display']}</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container container--mid">
    <h2 class="sr-only">Questions and answers</h2>
    {faq_items()}
  </div>
</section>

<section class="section section--tight">
  <div class="container container--mid">
    {emergency_notice()}
  </div>
</section>

{cta_band("Still not sure?",
          "The front desk answers these questions all day. Give them a call and ask.")}
"""
    page("faq.html",
         "FAQ | Churchill Medical Clinic, Mississauga Walk-In",
         "Answers about visiting Churchill Medical Clinic in Mississauga: appointments, OHIP coverage, "
         "what to bring, languages, accessibility and prescriptions.",
         body, crumb_label="FAQ", schema=schema_block("faq.html", extra=faq_schema()))


# ===========================================================================
# Contact
# ===========================================================================
def build_contact():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Contact</span>
    <h1>Contact and directions</h1>
    <p class="lede">The fastest way to reach the clinic is by telephone during opening hours. The front desk can
    answer questions about hours, availability and whether we are the right place for your problem.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:32px;align-items:center">
      <a class="btn btn--lg" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
      {status_pill()}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="sr-only">Contact details</h2>
    <div class="grid grid--3">
      <div class="card">
        <span class="icon-tile" style="margin-bottom:16px">{icon("map-pin")}</span>
        <h3>Address</h3>
        <p>{S['street']}<br>{S['city']}, {S['region_long']} {S['postal']}<br>Canada</p>
        <p style="margin-top:16px">
          <a href="{S['maps_url']}" rel="noopener">Google Maps</a> &middot;
          <a href="{S['apple_maps_url']}" rel="noopener">Apple Maps</a>
        </p>
      </div>
      <div class="card">
        <span class="icon-tile" style="margin-bottom:16px">{icon("phone")}</span>
        <h3>Telephone and fax</h3>
        <p>Telephone <a href="tel:{S['phone_tel']}">{S['phone_display']}</a><br>
        Fax {S['fax_display']}</p>
        <p style="margin-top:16px">Please do not send personal health information by fax without calling first.</p>
      </div>
      <div class="card">
        <span class="icon-tile" style="margin-bottom:16px">{icon("clock")}</span>
        <h3>Opening hours</h3>
        {hours_table()}
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="split">
      <div class="split__body">
        <h2>Getting here</h2>
        <p>Churchill Medical Clinic is on Artesian Drive in {S['neighbourhood']}, on the western side of
        {S['city']} near the Winston Churchill Boulevard and Highway 403 interchange.</p>
        <p>The clinic is <strong>Unit 6</strong> &mdash; check the unit number before you set off, since the
        address covers more than one business.</p>
        <p>There is a pharmacy next to the clinic, so a prescription can usually be filled in the same trip.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px">
          <a class="btn btn--ghost" href="{S['maps_url']}" rel="noopener">{icon("map-pin")}<span>Open in Google Maps</span></a>
          <a class="btn btn--ghost" href="{S['apple_maps_url']}" rel="noopener">{icon("route")}<span>Open in Apple Maps</span></a>
        </div>
      </div>
      <div class="split__media figure-frame figure-frame--right">
        {picture("waiting-room", "The clinic waiting area, with seating and a reception desk", "16x9")}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--mid">
    <div class="section-head">
      <span class="eyebrow">Send a message</span>
      <h2>General enquiries</h2>
      <p class="lede">For general questions only. This form is not monitored continuously and must never be used
      for anything urgent.</p>
    </div>

    <div class="notice notice--warn" style="margin-bottom:32px">
      {icon("alert")}
      <p><strong>Do not use this form for medical advice, test results, or anything urgent.</strong>
      Please do not include personal health information. For a medical emergency call <strong>911</strong>.
      To discuss your care, call the clinic on <a href="tel:{S['phone_tel']}">{S['phone_display']}</a>.</p>
    </div>
{preview_form_notice()}
    <form action="contact.php" method="post" data-validate{' inert aria-disabled="true"' if PREVIEW else ''}>
      <div class="formstatus" role="status" aria-live="polite"></div>

      <div class="field">
        <label for="name">Your name <span class="req" aria-hidden="true">*</span></label>
        <input type="text" id="name" name="name" autocomplete="name" required>
        <span class="error" role="alert"></span>
      </div>

      <div class="field">
        <label for="phone">Telephone <span class="req" aria-hidden="true">*</span></label>
        <input type="tel" id="phone" name="phone" autocomplete="tel" inputmode="tel" required>
        <span class="help">The quickest way for us to get back to you.</span>
        <span class="error" role="alert"></span>
      </div>

      <div class="field">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" autocomplete="email" inputmode="email">
        <span class="help">Optional. Email is not a secure way to send health information.</span>
        <span class="error" role="alert"></span>
      </div>

      <div class="field">
        <label for="reason">What is this about? <span class="req" aria-hidden="true">*</span></label>
        <select id="reason" name="reason" required>
          <option value="">Please choose&hellip;</option>
          <option>Opening hours or availability</option>
          <option>Family practice enquiry</option>
          <option>Forms, notes or paperwork</option>
          <option>Accessibility or language support</option>
          <option>Something else</option>
        </select>
        <span class="error" role="alert"></span>
      </div>

      <div class="field">
        <label for="message">Your message <span class="req" aria-hidden="true">*</span></label>
        <textarea id="message" name="message" required></textarea>
        <span class="help">Please keep this general &mdash; no symptoms, diagnoses or health details.</span>
        <span class="error" role="alert"></span>
      </div>

      <p style="position:absolute;left:-9999px" aria-hidden="true">
        <label for="website">Leave this field empty</label>
        <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
      </p>

      <button class="btn btn--lg" type="submit">{icon("mail")}<span>Send message</span></button>
      <p class="formnote" style="margin-top:24px">By sending this form you agree that we may contact you using
      the details above. See our <a href="privacy.html">privacy notice</a> for how your information is handled.</p>
    </form>
  </div>
</section>

{cta_band("The phone is the fastest route",
          "During opening hours, a call to the front desk will get you an answer straight away.")}
"""
    page("contact.html",
         "Contact Churchill Medical Clinic | Mississauga",
         "Churchill Medical Clinic, 3050 Artesian Drive, Unit 6, Mississauga ON L5M 7P5. Telephone "
         "(905) 607-6495. Opening hours, directions and enquiries.",
         body, crumb_label="Contact", schema=schema_block("contact.html"))


# ===========================================================================
# Local SEO spoke — Churchill Meadows
# ===========================================================================
def build_local():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Churchill Meadows</span>
    <h1>Walk-in clinic in Churchill Meadows, Mississauga</h1>
    <p class="lede">Churchill Medical Clinic is on Artesian Drive, inside Churchill Meadows itself &mdash; no
    drive across the city when someone in the house needs seeing to today.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:32px;align-items:center">
      <a class="btn" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
      <a class="btn btn--ghost" href="{S['maps_url']}" rel="noopener">{icon("map-pin")}<span>Get directions</span></a>
      {status_pill()}
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--mid prose">
    <h2>A clinic inside the neighbourhood</h2>
    <p>Churchill Meadows sits on the western edge of Mississauga, bounded roughly by Winston Churchill Boulevard,
    Highway 403, Britannia Road and Erin Mills Parkway. It is a young, family-heavy part of the city &mdash; which
    means a steady need for the ordinary medical care that families actually use: ear infections, fevers, sprained
    wrists, prescriptions that have run out, a cough that has gone on too long.</p>
    <p>Churchill Medical Clinic is at {S['street']}, near the Winston Churchill and Highway 403 interchange.
    It is a walk-in clinic, so there is no appointment to book and no need to be a registered patient.</p>

    <h2>Who we see</h2>
    <p>Anyone who walks in during opening hours with a valid Ontario health card. In practice most of our patients
    come from Churchill Meadows and the surrounding western Mississauga neighbourhoods, along with people who work
    nearby and would rather be seen close to work than take a day off.</p>

    <h2>Opening hours</h2>
    {hours_table()}
    <p style="margin-top:24px">Hours can change and the clinic may stop registering walk-in patients shortly
    before closing. Call <a href="tel:{S['phone_tel']}">{S['phone_display']}</a> before travelling, especially
    late in the day.</p>

    <h2>What it costs</h2>
    <p>With a valid Ontario health card, an insured visit is covered by OHIP and there is nothing to pay. A few
    services &mdash; certain notes, letters and third-party forms &mdash; are not insured; the front desk will
    quote the fee before the work is done.</p>

    <h2>What to bring</h2>
    <ul>
      <li>Your Ontario health card</li>
      <li>A list of your current medications, including anything bought over the counter</li>
      <li>Details of any allergies</li>
      <li>Any relevant results or letters</li>
    </ul>

    <div style="margin-top:40px">{emergency_notice()}</div>
  </div>
</section>

{cta_band("A walk-in clinic in your own neighbourhood",
          "3050 Artesian Drive, Unit 6 — open six days a week, no appointment needed.")}
"""
    page("walk-in-clinic-churchill-meadows.html",
         "Walk-In Clinic, Churchill Meadows Mississauga | Churchill",
         "Walk-in clinic in Churchill Meadows, Mississauga, at 3050 Artesian Drive. No appointment "
         "needed, OHIP covered, open Monday to Saturday.",
         body, crumb_label="Churchill Meadows", schema=schema_block("walk-in-clinic-churchill-meadows.html"))


# ===========================================================================
# Seasonal spoke — flu shots
# ===========================================================================
def build_flu():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Immunisation</span>
    <h1>Flu shots in Mississauga</h1>
    <p class="lede">Seasonal influenza vaccination is available at Churchill Medical Clinic each autumn, subject
    to supply. Call the clinic to check availability before you travel.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:32px;align-items:center">
      <a class="btn" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Check availability</span></a>
      {status_pill()}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="split__body prose">
        <h2>Why the flu shot is worth the trip</h2>
        <p>Influenza is not a heavy cold. For most healthy adults it means a rough week; for young children,
        older adults, pregnant people and anyone with a long-term heart, lung or immune condition, it can mean
        pneumonia and a hospital admission.</p>
        <p>The vaccine is reformulated every year to match the strains expected to circulate, which is why last
        year's shot does not carry over. It takes roughly two weeks after the injection to reach full effect.</p>

        <h2>Who can have it</h2>
        <p>In Ontario, the seasonal influenza vaccine is publicly funded for everyone six months of age and older
        who lives, works or attends school in the province. There is no charge with a valid Ontario health card.</p>

        <h2>When to come</h2>
        <p>The vaccine is usually available from the autumn and the campaign runs through the winter. Ontario
        confirms the start date and eligibility each year, so <strong>call the clinic on
        <a href="tel:{S['phone_tel']}">{S['phone_display']}</a></strong> to confirm we have supply before
        you make the journey.</p>
      </div>
      <div class="split__media figure-frame figure-frame--right">
        {picture("vaccination", "A nurse administering a vaccination into a patient's upper arm", "4x3")}
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container container--mid">
    <div class="notice">
      {icon("info")}
      <p><strong>Dates change every year.</strong> Rather than publish a date here that may be wrong by the time
      you read it, please call the clinic to confirm current availability. Ontario publishes the season's
      eligibility and start dates on the provincial health website.</p>
    </div>
    <div style="margin-top:32px">{emergency_notice()}</div>
  </div>
</section>

{cta_band("Call before you come",
          "Vaccine supply moves through the season. A quick call confirms we can do it today.")}
"""
    page("flu-shots-mississauga.html",
         "Flu Shots in Mississauga | Churchill Medical Clinic",
         "Seasonal flu shots at Churchill Medical Clinic, Churchill Meadows, Mississauga. Publicly funded "
         "in Ontario with a valid health card. Call to check supply.",
         body, crumb_label="Flu Shots", schema=schema_block("flu-shots-mississauga.html"))


# ===========================================================================
# Privacy
# ===========================================================================
def build_privacy():
    body = f"""
<section class="pagehead">
  <div class="container">
    <span class="eyebrow">Legal</span>
    <h1>Privacy notice</h1>
    <p class="lede">How Churchill Medical Clinic handles personal information and personal health information.</p>
  </div>
</section>

<section class="section">
  <div class="container container--mid prose">
    <h2>Your health information</h2>
    <p>Churchill Medical Clinic is a health information custodian under Ontario's
    <em>Personal Health Information Protection Act, 2004</em> (PHIPA). We collect personal health information
    in order to provide you with care, and we use and disclose it only as PHIPA permits or requires.</p>

    <h2>This website</h2>
    <p>This site does not require you to create an account and does not ask for health information. If you send
    a message through the enquiry form on our contact page, we receive the name, telephone number, email address
    and message you provide, and use them solely to respond to your enquiry.</p>
    <p>Please do not send symptoms, diagnoses, test results or other health details through the website form or
    by email. Neither is a secure channel. Telephone the clinic instead.</p>

    <h2>Cookies and analytics</h2>
    <p>This website sets no advertising or tracking cookies of its own. Web fonts are loaded from Google Fonts,
    which means your browser makes a request to Google's servers to fetch them.</p>

    <h2>Access to your record</h2>
    <p>Under PHIPA you have the right to ask for access to your own health record and to ask for a correction if
    something in it is inaccurate. To make a request, contact the clinic at
    <a href="tel:{S['phone_tel']}">{S['phone_display']}</a> or write to us at {S['street']}, {S['city']},
    {S['region']} {S['postal']}.</p>

    <h2>Concerns</h2>
    <p>If you have a concern about how your information has been handled, please raise it with the clinic first.
    You also have the right to complain to the Information and Privacy Commissioner of Ontario.</p>

    <div class="notice" style="margin-top:40px">
      {icon("info")}
      <p><strong>Note for the clinic:</strong> this notice is a plain-language starting point and is not legal
      advice. It should be reviewed and approved by the clinic before launch, and checked against your existing
      privacy policy and any hospital or network agreements.</p>
    </div>
  </div>
</section>
"""
    page("privacy.html",
         "Privacy Notice | Churchill Medical Clinic, Mississauga",
         "How Churchill Medical Clinic collects, uses and protects personal health information under Ontario's "
         "Personal Health Information Protection Act (PHIPA).",
         body, crumb_label="Privacy", schema=schema_block("privacy.html"))


# ===========================================================================
# 404
# ===========================================================================
def build_404():
    body = f"""
<section class="section">
  <div class="container container--mid" style="text-align:center;padding-block:40px">
    <span class="eyebrow" style="justify-content:center">Page not found</span>
    <h1>We could not find that page</h1>
    <p class="lede" style="margin-inline:auto;max-width:52ch">The link may be out of date, or the address may
    have been mistyped. Everything on the site is reachable from the pages below.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:32px">
      <a class="btn" href="index.html">{icon("arrow-right")}<span>Go to the home page</span></a>
      <a class="btn btn--ghost" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
    </div>
    <h2 class="sr-only">Popular pages</h2>
    <div class="grid grid--3" style="margin-top:64px;text-align:left">
      <a class="card card--link" href="walk-in-clinic.html"><h3>Walk-in clinic</h3>
        <p>Hours, what we treat, and how a visit works.</p>
        <span class="card__more">Open{icon("arrow-right")}</span></a>
      <a class="card card--link" href="services.html"><h3>Services</h3>
        <p>What the clinic can and cannot help with.</p>
        <span class="card__more">Open{icon("arrow-right")}</span></a>
      <a class="card card--link" href="contact.html"><h3>Contact</h3>
        <p>Address, telephone, hours and directions.</p>
        <span class="card__more">Open{icon("arrow-right")}</span></a>
    </div>
  </div>
</section>
"""
    out = head("404.html", "Page not found | Churchill Medical Clinic",
               "That page could not be found. Find the walk-in clinic hours, services and contact details for "
               "Churchill Medical Clinic in Mississauga.")
    out = out.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
                      '<meta name="robots" content="noindex, follow">')
    out += header("404.html") + f'<main id="main">\n{body}\n</main>\n' + footer()
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


# ===========================================================================
# Thank you — the destination contact.php redirects to on success.
# A real page rather than a query-string flag, so a patient with JavaScript
# disabled still gets a clear confirmation that the message was sent.
# ===========================================================================
def build_thankyou():
    body = f"""
<section class="section">
  <div class="container container--mid" style="text-align:center;padding-block:40px">
    <span class="icon-tile" style="width:76px;height:76px;border-radius:22px;margin:0 auto 28px;background:var(--open-soft);border-color:#BFE3D2;color:var(--open)">
      <span style="display:grid;place-items:center;width:38px;height:38px">{icon("check", "tick-lg")}</span>
    </span>
    <span class="eyebrow" style="justify-content:center">Message sent</span>
    <h1>Thank you &mdash; we have your message</h1>
    <p class="lede" style="margin-inline:auto;max-width:52ch">The clinic will get back to you using
    the contact details you gave us. Please allow a working day or so for a reply.</p>

    <div class="notice notice--warn" style="text-align:left;margin:40px auto 0;max-width:620px">
      {icon("alert")}
      <p><strong>If you need to be seen today, do not wait for a reply.</strong> Walk in during opening
      hours, or call the clinic on <a href="tel:{S['phone_tel']}">{S['phone_display']}</a>. For a medical
      emergency call <strong>911</strong>.</p>
    </div>

    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:40px">
      <a class="btn btn--lg" href="tel:{S['phone_tel']}" data-cta="call">{icon("phone")}<span>Call {S['phone_display']}</span></a>
      <a class="btn btn--ghost btn--lg" href="index.html"><span>Back to the home page</span>{icon("arrow-right")}</a>
    </div>

    <div style="margin-top:56px;text-align:left">
      <h2 class="sr-only">Clinic details</h2>
      <div class="infocard" style="margin-top:0">
        <div class="infocard__grid">
          <div class="infocard__item">
            <span class="icon-tile">{icon("map-pin")}</span>
            <div><h3>Find us</h3><p>{S['street']}<br>{S['city']}, {S['region']} {S['postal']}<br>
            <a href="{S['maps_url']}" rel="noopener">Get directions</a></p></div>
          </div>
          <div class="infocard__item">
            <span class="icon-tile">{icon("clock")}</span>
            <div><h3>Opening hours</h3><p>Monday to Friday, 9am&ndash;7pm<br>Saturday, 9am&ndash;3pm<br>Closed Sunday</p></div>
          </div>
          <div class="infocard__item">
            <span class="icon-tile">{icon("phone")}</span>
            <div><h3>Speak to the clinic</h3><p><a href="tel:{S['phone_tel']}">{S['phone_display']}</a><br>
            Fax {S['fax_display']}</p></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    out = head("thank-you.html", "Message sent | Churchill Medical Clinic",
               "Your message has been sent to Churchill Medical Clinic. If you need to be seen today, "
               "walk in during opening hours or call (905) 607-6495.")
    out = out.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
                      '<meta name="robots" content="noindex, follow">')
    out += header("thank-you.html") + f'<main id="main">\n{body}\n</main>\n' + footer()
    with open(os.path.join(OUT, "thank-you.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)

# ===========================================================================
# robots.txt / sitemap.xml / llms.txt
# ===========================================================================
PAGES_FOR_SITEMAP = [
    ("index.html", "1.0", "weekly"),
    ("walk-in-clinic.html", "0.9", "monthly"),
    ("walk-in-clinic-churchill-meadows.html", "0.8", "monthly"),
    ("family-practice.html", "0.8", "monthly"),
    ("services.html", "0.8", "monthly"),
    ("our-doctors.html", "0.7", "monthly"),
    ("flu-shots-mississauga.html", "0.7", "monthly"),
    ("about.html", "0.6", "monthly"),
    ("faq.html", "0.6", "monthly"),
    ("contact.html", "0.7", "monthly"),
    ("privacy.html", "0.3", "yearly"),
]


def build_seo_files():
    today = datetime.date.today().isoformat()

    urls = ""
    for p, prio, freq in PAGES_FOR_SITEMAP:
        loc = f"{S['domain']}/" if p == "index.html" else f"{S['domain']}/{p}"
        urls += (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
                 f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}</urlset>\n")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sitemap)

    robots = f"""# Churchill Medical Clinic
# Default-allow. AI crawlers are welcome: being read and cited accurately is
# the point of publishing clinic hours and services in plain HTML.

User-agent: *
Allow: /

Sitemap: {S['domain']}/sitemap.xml
"""
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(robots)

    hours_txt = "\n".join(f"- {d}: {h}" for _, d, h in HOURS_ROWS)
    llms = f"""# Churchill Medical Clinic

> A walk-in clinic and family practice in Churchill Meadows, Mississauga, Ontario.
> Treats everyday illness and minor injuries without an appointment. Insured
> services are covered by OHIP for patients with a valid Ontario health card.

## Key facts

- Name: {S['name']}
- Address: {S['street']}, {S['city']}, {S['region_long']} {S['postal']}, Canada
- Telephone: {S['phone_display']}
- Fax: {S['fax_display']}
- Neighbourhood: {S['neighbourhood']}, western Mississauga, near Winston Churchill Blvd and Highway 403
- Appointment required: No — walk-in
- Payment: OHIP. Some uninsured services carry a fee, quoted before the service is provided.
- Languages: English, Arabic, Burmese
- Accessibility: Wheelchair-accessible entrance
- Pharmacy: There is a pharmacy adjacent to the clinic

## Opening hours (America/Toronto)

{hours_txt}

Hours can change; callers are advised to telephone before travelling.

## Physicians

- Dr. Khin Maung Myint — Family Physician, CPSO 80153. Certificant, College of Family
  Physicians of Canada (2003). Mandalay Institute of Medicine, 1983. Independent
  practice in Ontario since September 2003. Speaks English and Burmese.
- Dr. Samira Wahba Azer Girgis — Family Physician, CPSO 82475. Certificant, College of
  Family Physicians of Canada (2004). Alexandria University Faculty of Medicine, 1979.
  Independent practice in Ontario since May 2005. Speaks English and Arabic.

## Services

- Walk-in care for everyday illness: coughs, colds, flu symptoms, sore throats, fevers,
  ear and eye infections, urinary tract infections, skin rashes, minor infections
- Minor injuries: sprains, strains, minor cuts and grazes, minor burns, wound care
- Prescriptions and refills
- Vaccinations, including seasonal flu shots, subject to supply
- Medical notes, routine forms and laboratory requisitions (some are not OHIP insured)
- Family practice: long-term condition review, results follow-up, medication review,
  referrals to specialists

## Not available at this clinic

- Emergency care. Patients with an emergency should call 911 or attend a hospital
  emergency department.
- On-site imaging or laboratory testing. Requisitions are issued for use elsewhere.
- Specialist treatment. Patients are referred instead.

## Pages

- {S['domain']}/ — Home
- {S['domain']}/walk-in-clinic.html — Walk-in clinic: hours, what is treated, how a visit works
- {S['domain']}/walk-in-clinic-churchill-meadows.html — Walk-in clinic for Churchill Meadows
- {S['domain']}/family-practice.html — Family practice and continuing care
- {S['domain']}/services.html — Full list of services
- {S['domain']}/our-doctors.html — Physicians and their credentials
- {S['domain']}/flu-shots-mississauga.html — Seasonal flu shots
- {S['domain']}/about.html — About the clinic
- {S['domain']}/faq.html — Frequently asked questions
- {S['domain']}/contact.html — Contact, directions and enquiry form
- {S['domain']}/privacy.html — Privacy notice (PHIPA)
"""
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8", newline="\n").write(llms)


def build_contact_php():
    php = r"""<?php
/**
 * Churchill Medical Clinic — contact form handler.
 *
 * Deliberately minimal. It does not store anything, and it is not a channel for
 * personal health information: the form itself tells patients to telephone for
 * anything clinical.
 *
 * BEFORE LAUNCH: set $to to the clinic's real monitored mailbox.
 */
declare(strict_types=1);

$to       = '__FORM_TO__';
$fromAddr = '__FROM_ADDR__';   // must be a domain this server is allowed to send as
$subject  = 'Website enquiry — Churchill Medical Clinic';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: contact.html');
    exit;
}

// Honeypot: a real person never fills this in.
if (!empty($_POST['website'] ?? '')) {
    header('Location: thank-you.html');
    exit;
}

$clean = static function (string $key, int $max = 500): string {
    $v = trim((string)($_POST[$key] ?? ''));
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);   // header-injection guard
    return mb_substr($v, 0, $max);
};

$name    = $clean('name', 120);
$phone   = $clean('phone', 40);
$email   = $clean('email', 160);
$reason  = $clean('reason', 120);
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 3000);

if ($name === '' || $phone === '' || $reason === '' || $message === '') {
    header('Location: contact.html?error=missing');
    exit;
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: contact.html?error=email');
    exit;
}

$body = "Website enquiry\n\n"
      . "Name:    {$name}\n"
      . "Phone:   {$phone}\n"
      . "Email:   " . ($email !== '' ? $email : '(not given)') . "\n"
      . "Subject: {$reason}\n\n"
      . "Message:\n{$message}\n\n"
      . '---'."\n"
      . 'Sent ' . date('Y-m-d H:i:s T') . ' from ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

// From is a build-time constant, never $_SERVER['HTTP_HOST']: that header is
// client-controlled, and it is the one value that would otherwise reach the
// mail headers without passing through the sanitiser above.
$headers  = 'From: Churchill Medical Clinic <' . $fromAddr . ">\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
if ($email !== '') {
    $headers .= 'Reply-To: ' . $email . "\r\n";
}

// The fifth argument sets the envelope sender. Without it, cPanel's Exim uses
// the hosting account default, so SPF authenticates a hostgator.com hostname
// while the From: header claims the clinic's domain. That misalignment is what
// puts the message in the spam folder, or gets it rejected outright.
$sent = @mail($to, $subject, $body, $headers, '-f ' . $fromAddr);
header('Location: ' . ($sent ? 'thank-you.html' : 'contact.html?error=send'));
exit;
"""
    from urllib.parse import urlparse
    host = urlparse(S["domain"]).netloc or "localhost"
    php = php.replace("__FORM_TO__", S["form_to"])
    php = php.replace("__FROM_ADDR__", S["form_from_local"] + "@" + host)
    open(os.path.join(OUT, "contact.php"), "w", encoding="utf-8", newline="\n").write(php)


# ===========================================================================
if __name__ == "__main__":
    build_home()
    build_walkin()
    build_family()
    build_services()
    build_doctors()
    build_about()
    build_faq()
    build_contact()
    build_local()
    build_flu()
    build_privacy()
    build_thankyou()
    build_404()
    build_seo_files()
    build_contact_php()

    built = [p for p, _, _ in PAGES_FOR_SITEMAP] + ["thank-you.html", "404.html"]
    print("Built %d pages:" % len(built))
    for b in built:
        size = os.path.getsize(os.path.join(OUT, b))
        print("  %-44s %6.1f KB" % (b, size / 1024))
    for extra in ("sitemap.xml", "robots.txt", "llms.txt", "contact.php"):
        print("  %-44s %6.1f KB" % (extra, os.path.getsize(os.path.join(OUT, extra)) / 1024))
