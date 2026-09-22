/* Churchill Medical Clinic — progressive enhancement only.
   Every piece of content this file touches also exists in the served HTML.
   Nothing here supplies content that a crawler could not already read. */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     1. Mobile navigation drawer
     ------------------------------------------------------------------ */
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("mobile-drawer");

  if (toggle && drawer) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      drawer.setAttribute("data-open", String(!open));
    });

    // Escape closes the drawer and returns focus to the trigger
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        drawer.setAttribute("data-open", "false");
        toggle.focus();
      }
    });

    // Close when the viewport grows past the desktop breakpoint
    var mq = window.matchMedia("(min-width: 1024px)");
    var onChange = function (e) {
      if (e.matches) {
        toggle.setAttribute("aria-expanded", "false");
        drawer.setAttribute("data-open", "false");
      }
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* ------------------------------------------------------------------
     2. Live opening status — computed at view time in America/Toronto
        so it is never "true only at build time", and is correct for a
        visitor in any timezone.
        Hours source: Peel Region 211 record MHL0405.
     ------------------------------------------------------------------ */
  var HOURS = {
    0: null,              // Sunday — closed
    1: [540, 1140],       // Mon 09:00–19:00  (minutes from midnight)
    2: [540, 1140],
    3: [540, 1140],
    4: [540, 1140],
    5: [540, 1140],
    6: [540, 900]         // Sat 09:00–15:00
  };
  var DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function torontoNow() {
    // Read the wall clock in Toronto regardless of the visitor's own timezone.
    var parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/Toronto",
      weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false
    }).formatToParts(new Date());

    var get = function (t) {
      for (var i = 0; i < parts.length; i++) if (parts[i].type === t) return parts[i].value;
      return null;
    };
    var wk = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    var hour = parseInt(get("hour"), 10);
    if (hour === 24) hour = 0; // some engines report 24 for midnight
    return { day: wk[get("weekday")], minutes: hour * 60 + parseInt(get("minute"), 10) };
  }

  function fmt(mins) {
    var h = Math.floor(mins / 60), m = mins % 60;
    var ampm = h >= 12 ? "pm" : "am";
    var h12 = h % 12; if (h12 === 0) h12 = 12;
    return h12 + (m ? ":" + String(m).padStart(2, "0") : "") + ampm;
  }

  function nextOpening(fromDay) {
    for (var i = 1; i <= 7; i++) {
      var d = (fromDay + i) % 7;
      if (HOURS[d]) {
        return (i === 1 ? "tomorrow" : DAY_NAMES[d]) + " at " + fmt(HOURS[d][0]);
      }
    }
    return null;
  }

  function computeStatus(injected) {
    var now = injected || torontoNow();
    if (isNaN(now.day) || isNaN(now.minutes)) return null;
    var today = HOURS[now.day];

    if (today && now.minutes >= today[0] && now.minutes < today[1]) {
      var left = today[1] - now.minutes;
      if (left <= 60) return { state: "open", label: "Closing at " + fmt(today[1]) };
      return { state: "open", label: "Open now until " + fmt(today[1]) };
    }
    if (today && now.minutes < today[0]) {
      return { state: "closed", label: "Opens today at " + fmt(today[0]) };
    }
    var next = nextOpening(now.day);
    return { state: "closed", label: next ? "Closed — opens " + next : "Closed" };
  }

  // Exposed so the opening-hours logic can be exercised at day boundaries
  // without waiting for a Tuesday evening. Takes {day, minutes} in Toronto time.
  window.clinicStatusFor = computeStatus;

  var status = computeStatus();
  if (status) {
    var pills = document.querySelectorAll("[data-status-pill]");
    for (var i = 0; i < pills.length; i++) {
      pills[i].setAttribute("data-state", status.state);
      var text = pills[i].querySelector("[data-status-text]");
      if (text) text.textContent = status.label;
    }
  }

  // Mark today's row in any hours table
  var todayIndex = torontoNow().day;
  var rows = document.querySelectorAll("[data-day]");
  for (var r = 0; r < rows.length; r++) {
    if (parseInt(rows[r].getAttribute("data-day"), 10) === todayIndex) {
      rows[r].setAttribute("data-today", "true");
      var th = rows[r].querySelector("th");
      if (th && !th.querySelector(".hours__today")) {
        var badge = document.createElement("span");
        badge.className = "hours__today";
        badge.textContent = "Today";
        th.appendChild(badge);
      }
    }
  }

  /* ------------------------------------------------------------------
     3. Scroll reveal — decorative only, and skipped entirely when the
        visitor prefers reduced motion or IntersectionObserver is absent.
     ------------------------------------------------------------------ */
  var reveals = document.querySelectorAll(".reveal");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reveals.length && !reduced && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    for (var v = 0; v < reveals.length; v++) io.observe(reveals[v]);
  } else {
    // No observer, or motion is unwelcome: show everything immediately.
    for (var w = 0; w < reveals.length; w++) reveals[w].classList.add("is-in");
  }

  /* ------------------------------------------------------------------
     3b. Server-side form errors. Success lands on thank-you.html, a real
         page, so the confirmation works with scripting disabled; only the
         rarer error paths come back here as a query flag.
     ------------------------------------------------------------------ */
  var statusBox = document.querySelector(".formstatus");
  if (statusBox) {
    var err = null;
    var q = window.location.search;
    if (q.indexOf("error=send") > -1) {
      err = "Your message could not be sent just now. Please call the clinic on (905) 607-6495 instead.";
    } else if (q.indexOf("error=missing") > -1) {
      err = "Some required details were missing. Please check the form below and send it again.";
    } else if (q.indexOf("error=email") > -1) {
      err = "That email address was not recognised. Please check it, or leave it blank and give a phone number.";
    }
    if (err) {
      statusBox.className = "formstatus formstatus--error";
      statusBox.setAttribute("role", "alert");
      statusBox.textContent = err;
      statusBox.scrollIntoView({ block: "center" });
    }
  }

  /* ------------------------------------------------------------------
     4. Contact form — validate on blur, focus the first invalid field
        on submit. The form still posts normally without JS.
     ------------------------------------------------------------------ */
  var form = document.querySelector("[data-validate]");
  if (form) {
    var setFieldState = function (input) {
      var field = input.closest(".field");
      if (!field) return true;
      var ok = input.checkValidity();
      field.setAttribute("data-invalid", String(!ok));
      var err = field.querySelector(".error");
      if (err && !ok) err.textContent = input.validationMessage;
      return ok;
    };

    var inputs = form.querySelectorAll("input, select, textarea");
    for (var n = 0; n < inputs.length; n++) {
      (function (input) {
        input.addEventListener("blur", function () {
          if (input.value !== "") setFieldState(input);
        });
        input.addEventListener("input", function () {
          var field = input.closest(".field");
          if (field && field.getAttribute("data-invalid") === "true") setFieldState(input);
        });
      })(inputs[n]);
    }

    form.addEventListener("submit", function (e) {
      var firstInvalid = null;
      for (var k = 0; k < inputs.length; k++) {
        if (!setFieldState(inputs[k]) && !firstInvalid) firstInvalid = inputs[k];
      }
      if (firstInvalid) {
        e.preventDefault();
        firstInvalid.focus();
        firstInvalid.scrollIntoView({ block: "center", behavior: reduced ? "auto" : "smooth" });
      }
    });
  }
})();
