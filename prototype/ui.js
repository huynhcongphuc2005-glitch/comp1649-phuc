/* ==========================================================================
   NeuroPulse HE — shared micro-interactions
   Each screen is a standalone artboard; these behaviours only operate
   within the current file (no cross-screen routing by design).
   ========================================================================== */
(function () {
  "use strict";

  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---------- Embedded preview mode ---------- */
  if (window.location.hash === "#embed") document.body.classList.add("is-embed");

  /* ---------- Status bar clock ---------- */
  const clock = $("[data-clock]");
  if (clock) {
    const tick = () => {
      const now = new Date();
      clock.textContent = String(now.getHours()).padStart(2, "0") + ":" + String(now.getMinutes()).padStart(2, "0");
    };
    tick();
    setInterval(tick, 20000);
  }

  /* ---------- Toast ---------- */
  let toastEl = $(".toast");
  let toastTimer;
  function toast(message) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      (document.querySelector(".artboard") || document.body).appendChild(toastEl);
    }
    toastEl.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg><span></span>';
    toastEl.querySelector("span").textContent = message;
    toastEl.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("is-visible"), 2600);
  }
  window.npToast = toast;

  /* ---------- Theme ---------- */
  const root = document.documentElement;
  $$("[data-set-theme]").forEach((btn) => {
    btn.addEventListener("click", () => {
      root.setAttribute("data-theme", btn.dataset.setTheme);
      const group = btn.closest("[data-theme-group]");
      if (group) $$("[data-set-theme]", group).forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      const label = btn.dataset.themeLabel || btn.dataset.setTheme;
      toast("Theme: " + label);
    });
  });

  /* ---------- Single-select chip / segmented groups ---------- */
  $$("[data-select-group]").forEach((group) => {
    const items = $$("[data-select]", group);
    items.forEach((item) => {
      item.addEventListener("click", () => {
        items.forEach((i) => {
          const on = i === item;
          if (i.hasAttribute("aria-pressed")) i.setAttribute("aria-pressed", String(on));
          if (i.hasAttribute("aria-selected")) i.setAttribute("aria-selected", String(on));
          i.classList.toggle("is-active", on);
        });
        toast(item.dataset.toast || item.textContent.trim());
      });
    });
  });

  /* ---------- Switches ---------- */
  $$('[role="switch"]').forEach((sw) => {
    sw.addEventListener("click", () => {
      const next = sw.getAttribute("aria-checked") !== "true";
      sw.setAttribute("aria-checked", String(next));
      toast((sw.dataset.label || "Setting") + (next ? " on" : " off"));
    });
  });

  /* ---------- Checklist ---------- */
  $$("[data-step]").forEach((step) => {
    const toggle = () => {
      step.classList.toggle("is-done");
      const list = step.closest("[data-step-list]");
      if (list) updateProgress(list);
      toast(step.classList.contains("is-done") ? "Step done. That counts." : "Step reopened");
    };
    step.addEventListener("click", (e) => {
      if (e.target.closest("button, a")) return;
      toggle();
    });
    step.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
    });
    step.setAttribute("tabindex", "0");
    step.setAttribute("role", "checkbox");
    step.setAttribute("aria-checked", "false");
  });

  function updateProgress(list) {
    const all = $$("[data-step]", list);
    const done = all.filter((s) => s.classList.contains("is-done")).length;
    all.forEach((s) => s.setAttribute("aria-checked", String(s.classList.contains("is-done"))));
    const counter = $("[data-progress-count]", list.closest(".content") || document);
    if (counter) counter.textContent = done + " of " + all.length + " steps";
    const bar = $("[data-progress-bar]", list.closest(".content") || document);
    if (bar) bar.style.width = Math.round((done / all.length) * 100) + "%";
  }

  /* ---------- Reading controls ---------- */
  const fontSize = $("[data-font-size]");
  if (fontSize) {
    const preview = $("[data-reading-preview]");
    const apply = () => {
      const v = fontSize.value;
      if (preview) preview.style.fontSize = v + "px";
      $("[data-font-size-value]").textContent = v + "px";
    };
    fontSize.addEventListener("input", apply);
    apply();
  }

  const tracking = $("[data-tracking]");
  if (tracking) {
    const preview = $("[data-reading-preview]");
    const apply = () => {
      if (preview) preview.style.letterSpacing = (tracking.value / 100) + "em";
      $("[data-tracking-value]").textContent = (tracking.value / 100).toFixed(2) + "em";
    };
    tracking.addEventListener("input", apply);
    apply();
  }

  $$("[data-reading-font]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const preview = $("[data-reading-preview]");
      if (preview) preview.style.fontFamily = btn.dataset.readingFont;
      $$("[data-reading-font]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      toast("Reading font: " + btn.dataset.fontLabel);
    });
  });

  /* ---------- Focus timer ---------- */
  const timer = $("[data-timer]");
  if (timer) {
    const minutes = Number(timer.dataset.timer);
    const total = minutes * 60;
    let left = total;
    let running = false;
    let handle = null;

    const clockEl = $("[data-timer-clock]");
    const ring = $("[data-timer-ring]");
    const startBtn = $("[data-timer-start]");
    const caption = $("[data-timer-caption]");
    const circumference = 2 * Math.PI * 104;

    ring.style.strokeDasharray = circumference;

    const minutesOnly = timer.dataset.display === "minutes";

    const render = () => {
      const m = Math.floor(left / 60);
      const s = left % 60;
      clockEl.textContent = minutesOnly
        ? String(Math.ceil(left / 60))
        : String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
      ring.style.strokeDashoffset = circumference * (1 - left / total);
    };

    const stop = () => {
      running = false;
      clearInterval(handle);
      startBtn.innerHTML = '<svg class="btn__icon" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>Resume';
      caption.textContent = "Paused — the ring is still where you left it";
    };

    startBtn.addEventListener("click", () => {
      if (running) { stop(); return; }
      running = true;
      startBtn.innerHTML = '<svg class="btn__icon" viewBox="0 0 24 24" fill="currentColor"><rect x="7" y="5" width="3.4" height="14" rx="1"/><rect x="13.6" y="5" width="3.4" height="14" rx="1"/></svg>Pause';
      caption.textContent = "Focusing — you can leave this screen open";
      handle = setInterval(() => {
        left -= 1;
        if (left <= 0) {
          left = 0; render(); clearInterval(handle); running = false;
          startBtn.innerHTML = "Start again";
          caption.textContent = "Finished. Nothing is flashing or buzzing.";
          toast("Step finished — take the next minute slowly.");
          return;
        }
        render();
      }, 1000);
    });

    $("[data-timer-reset]")?.addEventListener("click", () => {
      clearInterval(handle);
      left = total; running = false; render();
      startBtn.innerHTML = '<svg class="btn__icon" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>Start focus';
      caption.textContent = "Ready when you are";
    });

    render();
  }

  /* ---------- Breathing pacer ---------- */
  const breath = $("[data-breath]");
  if (breath) {
    const phase = $("[data-breath-phase]");
    const count = $("[data-breath-count]");
    const phases = [["Breathe in", 4], ["Hold", 4], ["Breathe out", 4], ["Rest", 4]];
    let i = 0, t = 0, active = false, tick;

    const step = () => {
      phase.textContent = phases[i][0];
      t = phases[i][1];
      count.textContent = t;
      breath.dataset.phase = String(i);
    };

    $("[data-breath-toggle]").addEventListener("click", (e) => {
      active = !active;
      e.currentTarget.textContent = active ? "Pause" : "Start breathing";
      if (!active) { clearInterval(tick); return; }
      step();
      tick = setInterval(() => {
        t -= 1;
        if (t < 0) { i = (i + 1) % phases.length; step(); return; }
        count.textContent = t;
      }, 1000);
    });
    step();
  }
})();
