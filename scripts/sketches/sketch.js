/* Low-fidelity, hand-drawn style sketches for the design-process figures.
   Rendered by sketch.html?fig=<name> in headless Chrome (scripts/build_sketches.sh).
   Deliberately rough: boxes, scribbles and short handwritten labels, not the
   final interface. Screens use a 300 x 600 phone space so the same sketch can
   be reused at small scale in the storyboard and the paper cards.
   These are references to redraw by hand on paper. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const PEN = "#2a2a2a", RED = "#c0392b", SOFT = "#909090";
  const svg = document.getElementById("sheet");
  const rc = rough.svg(svg);
  let seed = 11;

  function opts(o) {
    return Object.assign({ stroke: PEN, strokeWidth: 1.6, roughness: 1.9, bowing: 1.8, seed: seed++ }, o || {});
  }

  function ctx(g) {
    const add = (el) => { g.appendChild(el); return el; };
    const c = {
      g,
      rect: (x, y, w, h, o) => add(rc.rectangle(x, y, w, h, opts(o))),
      line: (x1, y1, x2, y2, o) => add(rc.line(x1, y1, x2, y2, opts(o))),
      circle: (cx, cy, d, o) => add(rc.circle(cx, cy, d, opts(o))),
      ellipse: (cx, cy, w, h, o) => add(rc.ellipse(cx, cy, w, h, opts(o))),
      arc: (cx, cy, d, a1, a2, o) => add(rc.arc(cx, cy, d, d, a1, a2, false, opts(o))),
      path: (d, o) => add(rc.path(d, opts(o))),
      text: (x, y, s, o) => {
        o = o || {};
        const t = document.createElementNS(NS, "text");
        t.setAttribute("x", x); t.setAttribute("y", y);
        t.setAttribute("font-family", o.font || "Kalam");
        t.setAttribute("font-size", o.size || 15);
        t.setAttribute("font-weight", o.bold ? 700 : 400);
        t.setAttribute("fill", o.color || PEN);
        if (o.anchor) t.setAttribute("text-anchor", o.anchor);
        t.textContent = s;
        return add(t);
      },
    };
    /* wavy lines standing in for text */
    c.scribble = (x, y, w, rows, gap, bold) => {
      gap = gap || 13;
      for (let i = 0; i < rows; i++) {
        const ww = rows > 1 && i === rows - 1 ? w * 0.55 : w;
        c.line(x, y + i * gap, x + ww, y + i * gap, { stroke: bold ? PEN : SOFT, strokeWidth: bold ? 2.4 : 1.2, roughness: 2.4 });
      }
    };
    c.button = (x, y, w, h, label, filled) => {
      c.rect(x, y, w, h, filled ? { fill: "#b8b8b8", fillStyle: "hachure", hachureGap: 7, fillWeight: 1.2 } : {});
      if (label) c.text(x + w / 2, y + h / 2 + 6, label, { size: 16, anchor: "middle", bold: !!filled });
    };
    c.check = (x, y, done) => {
      c.rect(x, y, 16, 16, { strokeWidth: 1.3 });
      if (done) c.path(`M${x + 2} ${y + 8} L${x + 7} ${y + 14} L${x + 16} ${y}`, { strokeWidth: 2 });
    };
    c.toggle = (x, y, on) => { c.ellipse(x + 20, y + 11, 42, 22, on ? { fill: "#b8b8b8", fillStyle: "hachure", hachureGap: 5 } : {}); c.circle(on ? x + 30 : x + 10, y + 11, 14); };
    c.calm = () => { c.ellipse(250, 42, 62, 26); c.text(250, 48, "~ calm", { size: 13, anchor: "middle" }); };
    c.back = () => c.text(18, 50, "<", { size: 22, bold: true });
    c.title = (s, x) => c.text(x || 16, 50, s, { size: 19, bold: true });
    c.tabbar = (active) => {
      c.line(4, 538, 296, 534, { strokeWidth: 1.2 });
      for (let i = 0; i < 4; i++) {
        const x = 38 + i * 75;
        c.rect(x - 10, 552, 20, 18, { strokeWidth: i === active ? 2.6 : 1.1, fill: i === active ? "#cfcfcf" : undefined, fillStyle: "solid" });
      }
    };
    c.phone = () => { c.rect(0, 0, 300, 600, { strokeWidth: 2.2, roughness: 1.4 }); };
    return c;
  }

  function group(x, y, s, parent) {
    const g = document.createElementNS(NS, "g");
    g.setAttribute("transform", `translate(${x},${y}) scale(${s || 1})`);
    (parent || svg).appendChild(g);
    return g;
  }

  /* ---------------------------------------------------------------- screens (lo-fi) */
  const SCREENS = {
    today(c) {
      c.phone(); c.title("Today"); c.calm();
      c.text(16, 96, "one thing at a time", { size: 18 });
      c.rect(16, 112, 268, 44); c.text(26, 139, "how's your head?", { size: 13 });
      [176, 210, 244].forEach((x) => c.circle(x, 134, 22));
      c.rect(16, 172, 268, 196, { strokeWidth: 2.6 });
      c.rect(28, 184, 90, 20); c.text(73, 199, "15 min", { size: 12, anchor: "middle" });
      c.scribble(28, 232, 230, 2, 18, true);
      c.scribble(28, 278, 120, 1);
      c.button(28, 300, 150, 46, "START", true);
      c.button(190, 300, 80, 46, "info");
      c.rect(16, 384, 268, 36); c.text(28, 408, "why only this? (?)", { size: 13 });
      c.rect(16, 432, 268, 36); c.text(28, 456, "+ 2 more steps  >", { size: 13 });
      c.tabbar(0);
    },
    plan(c) {
      c.phone(); c.title("Plan"); c.calm();
      [[16, 70], [104, 70], [192, 50]].forEach(([x, w], i) => c.rect(x, 72, w, 24, { strokeWidth: i === 0 ? 2.4 : 1.2 }));
      c.rect(16, 112, 268, 14); c.rect(16, 112, 92, 14, { fill: PEN, fillStyle: "hachure", hachureGap: 4 });
      for (let i = 0; i < 6; i++) {
        const y = 150 + i * 60;
        if (i === 2) c.rect(10, y - 10, 280, 50, { fill: "#d6d6d6", fillStyle: "hachure", hachureGap: 9, stroke: SOFT });
        c.check(22, y, i < 2);
        c.scribble(50, y + 8, i === 2 ? 170 : 190 - (i % 2) * 40, 1, 0, i === 2);
        if (i < 2) c.line(48, y + 8, 220, y + 7, { strokeWidth: 1.4 });
        c.scribble(50, y + 26, 60, 1);
        if (i === 2) { c.circle(268, y + 12, 26); c.text(268, y + 17, ">", { size: 13, anchor: "middle", bold: true }); }
      }
      c.tabbar(1);
    },
    step(c) {
      c.phone(); c.back(); c.title("step 3/6", 40); c.calm();
      [[16, 60], [84, 66], [158, 84]].forEach(([x, w]) => c.rect(x, 72, w, 22));
      c.text(46, 88, "15m", { size: 11, anchor: "middle" });
      c.scribble(16, 128, 240, 2, 20, true);
      c.rect(16, 172, 268, 150, { strokeWidth: 2.4 });
      c.text(28, 196, "DONE =", { size: 15, bold: true });
      [0, 1, 2].forEach((i) => { c.check(30, 214 + i * 34, false); c.scribble(56, 222 + i * 34, 190, 1); });
      c.rect(16, 338, 268, 70); c.text(28, 360, "search terms", { size: 13 });
      c.rect(28, 372, 100, 22); c.rect(138, 372, 80, 22);
      c.text(150, 440, "too big? -> split", { size: 14, anchor: "middle" });
      c.button(16, 462, 268, 48, "START", true);
      c.tabbar(1);
    },
    focus(c) {
      c.phone(); c.back(); c.title("Focus", 120); c.calm();
      c.scribble(60, 92, 180, 1, 0, true);
      c.circle(150, 222, 176, { strokeWidth: 1.2 });
      c.arc(150, 222, 176, -Math.PI / 2, Math.PI * 0.95, { strokeWidth: 5 });
      c.text(150, 234, "12:00", { size: 36, anchor: "middle", bold: true });
      c.button(16, 340, 268, 52, "PAUSE", true);
      c.text(150, 424, "end early (small)", { size: 13, anchor: "middle" });
      c.rect(16, 452, 268, 50); c.text(28, 482, "sound: off / rain", { size: 13 });
      c.tabbar(0);
    },
    rest(c) {
      c.phone(); c.title("Done!", 120); c.calm();
      c.scribble(16, 92, 210, 1, 0, true);
      c.rect(16, 112, 126, 48); c.rect(158, 112, 126, 48);
      c.text(26, 142, "15 min", { size: 14 }); c.text(168, 142, "3 / 6", { size: 14 });
      c.rect(16, 180, 268, 160, { fill: "#dedede", fillStyle: "hachure", hachureGap: 11, strokeWidth: 2.4 });
      c.text(150, 210, "REST", { size: 16, anchor: "middle", bold: true });
      c.text(150, 258, "3:00", { size: 34, anchor: "middle", bold: true });
      c.button(40, 278, 220, 42, "start", true);
      c.rect(16, 360, 268, 50); c.text(28, 390, "next: ...  (not now)", { size: 13 });
      c.button(16, 428, 268, 44, "stop for today");
      c.tabbar(0);
    },
    calm(c) {
      c.phone(); c.back(); c.title("Calm", 120);
      c.scribble(16, 92, 230, 1, 0, true);
      c.circle(150, 166, 120, { fill: "#e2e2e2", fillStyle: "hachure", hachureGap: 10 });
      c.text(150, 172, "breathe", { size: 16, anchor: "middle" });
      c.button(16, 244, 268, 44, "START", true);
      ["dim", "silence", "hide numbers"].forEach((l, i) => {
        const y = 308 + i * 50;
        c.text(24, y + 26, l, { size: 15 }); c.toggle(228, y + 10, false);
        c.line(16, y + 46, 284, y + 47, { stroke: SOFT, strokeWidth: 0.9 });
      });
      c.rect(16, 470, 268, 42); c.text(28, 497, "talk to someone  >", { size: 14 });
      c.text(150, 560, "I'm ok, back", { size: 14, anchor: "middle" });
    },
    settings(c) {
      c.phone(); c.title("Settings"); c.calm();
      c.rect(16, 72, 268, 66); c.text(30, 112, "Aa preview text", { size: 17 });
      [["size", 164, 0.3], ["spacing", 218, 0.1]].forEach(([l, y, p]) => {
        c.text(16, y, l, { size: 15, bold: true }); c.line(16, y + 20, 284, y + 21, { strokeWidth: 1.3 });
        c.circle(16 + 268 * p, y + 20, 18);
      });
      c.text(16, 282, "font", { size: 15, bold: true });
      [0, 1, 2].forEach((i) => { c.rect(16 + i * 92, 294, 80, 40, { strokeWidth: i === 0 ? 2.6 : 1.2 }); c.text(56 + i * 92, 320, "Aa", { size: 16, anchor: "middle" }); });
      c.text(16, 366, "colour", { size: 15, bold: true });
      [0, 1, 2].forEach((i) => c.rect(16 + i * 92, 378, 80, 40, i === 2 ? { fill: PEN, fillStyle: "hachure", hachureGap: 5 } : { strokeWidth: i === 0 ? 2.6 : 1.2 }));
      c.text(16, 458, "less motion", { size: 15, bold: true }); c.toggle(228, 442, false);
      c.tabbar(3);
    },
    progress(c) {
      c.phone(); c.title("Progress"); c.calm();
      [0, 1, 2].forEach((i) => { const x = 16 + i * 92; c.rect(x, 72, 82, 54); c.text(x + 12, 104, ["4", "1h55", "2"][i], { size: 18, bold: true }); });
      c.rect(16, 142, 268, 128);
      [45, 30, 0, 55, 25, 0, 0].forEach((h, i) => {
        const x = 34 + i * 36;
        if (h) c.rect(x, 252 - h * 1.5, 16, h * 1.5, { fill: "#9a9a9a", fillStyle: "hachure", hachureGap: 4 });
        else c.line(x, 252, x + 16, 252, { stroke: SOFT, strokeWidth: 2.4 });
      });
      c.text(16, 300, "help", { size: 15, bold: true });
      [0, 1, 2].forEach((i) => { const y = 312 + i * 46; c.rect(16, y, 268, 40); c.circle(36, y + 20, 18); c.scribble(56, y + 20, 160, 1); c.text(268, y + 26, ">", { size: 14 }); });
      c.rect(16, 466, 268, 36); c.text(28, 490, "NO streaks", { size: 14, bold: true });
      c.tabbar(2);
    },

    /* ---- early ideas and first versions ---- */
    home_a(c) {
      c.phone(); c.title("Home");
      [16, 108, 200].forEach((x) => { c.rect(x, 70, 84, 46); c.text(x + 42, 99, "14d!", { size: 15, anchor: "middle", bold: true }); });
      for (let i = 0; i < 11; i++) { c.check(16, 140 + i * 34, i < 2); c.scribble(42, 148 + i * 34, 200 - (i % 3) * 35, 1); }
      c.tabbar(0);
    },
    focus_v1(c) {
      c.phone(); c.title("Focus", 120);
      c.circle(150, 180, 160);
      c.text(150, 192, "12:00", { size: 32, anchor: "middle", bold: true });
      c.button(16, 286, 128, 48, "pause", true); c.button(156, 286, 128, 48, "stop", true);
      c.rect(36, 360, 228, 150, { strokeWidth: 2.6, fill: "#ffffff", fillStyle: "solid" });
      c.text(150, 396, "Well done! +10", { size: 18, anchor: "middle", bold: true });
      c.text(150, 426, "streak 3", { size: 15, anchor: "middle" });
      c.button(60, 446, 180, 34, "next task");
      c.text(150, 500, "break? x", { size: 12, anchor: "middle" });
      c.tabbar(0);
    },
    reading_v1(c) {
      c.phone(); c.title("Reading");
      c.rect(16, 72, 268, 60); c.scribble(28, 98, 230, 2);
      ["size", "spacing", "font"].forEach((l, i) => { c.text(16, 172 + i * 62, l, { size: 15, bold: true }); c.line(16, 190 + i * 62, 284, 191 + i * 62); });
      c.tabbar(3);
    },
    sensory_v1(c) {
      c.phone(); c.title("Sensory");
      ["colour", "motion", "sound", "haptics"].forEach((l, i) => { c.text(16, 104 + i * 62, l, { size: 15, bold: true }); c.toggle(228, 88 + i * 62, i === 1); });
      c.text(16, 370, "reading >", { size: 14 });
      c.tabbar(3);
    },
  };

  /* ---------------------------------------------------------------- annotations */
  function note(c, x, y, lines, tx, ty) {
    lines.forEach((l, i) => c.text(x, y + i * 22, l, { size: 18, color: RED, font: "Caveat" }));
    if (tx !== undefined && tx !== null) {
      const sx = x - 6, sy = y - 6;
      c.line(sx, sy, tx, ty, { stroke: RED, strokeWidth: 1.6, roughness: 1 });
      const a = Math.atan2(ty - sy, tx - sx), h = 10;
      c.line(tx, ty, tx - h * Math.cos(a - 0.45), ty - h * Math.sin(a - 0.45), { stroke: RED, strokeWidth: 1.6, roughness: 0.6 });
      c.line(tx, ty, tx - h * Math.cos(a + 0.45), ty - h * Math.sin(a + 0.45), { stroke: RED, strokeWidth: 1.6, roughness: 0.6 });
    }
  }

  /* phone at (30, 50) on a 660 x 700 sheet; arrow targets in sheet coordinates */
  const NOTES = {
    today: [[[360, 100], ["calm always here"], 312, 92],
            [[360, 290], ["ONE step only,", "big start button"], 316, 300],
            [[360, 440], ["explain why", "the rest is hidden"], 316, 452],
            [[360, 600], ["same tabs everywhere"], 316, 605]],
    plan: [[[360, 170], ["one module", "at a time"], 316, 135],
           [[360, 330], ["current step", "shaded + play"], 316, 320],
           [[360, 470], ["max 15 min", "per step?"], 316, 470]],
    step: [[[360, 130], ["how long / what kind"], 316, 132],
           [[360, 290], ["say what DONE means"], 316, 300],
           [[360, 500], ["escape if too big"], 316, 490]],
    focus: [[[360, 250], ["time left, no alarm"], 316, 270],
            [[360, 420], ["PAUSE = biggest"], 316, 418],
            [[360, 490], ["end early small,", "avoid mis-tap"], 316, 474]],
    rest: [[[360, 300], ["rest = its own screen,", "not a reward"], 316, 320],
           [[360, 520], ["stopping is ok"], 316, 500]],
    calm: [[[360, 140], ["no tabs here"], 316, 100],
           [[360, 420], ["one tap each"], 316, 410],
           [[360, 560], ["real people"], 316, 542]],
    settings: [[[360, 160], ["see change live"], 316, 155],
               [[360, 330], ["size + spacing,", "font choice"], 316, 300],
               [[360, 520], ["no diagnosis asked"], 316, 500]],
    progress: [[[360, 160], ["counts, not a score"], 316, 150],
                [[360, 290], ["grey = rest day"], 316, 300],
                [[360, 560], ["no streaks!"], 316, 538]],
    focus_v1: [[[360, 360], ["same size ->", "mis-taps"], 316, 362],
               [[360, 470], ["points + streak:", "Spiel et al. -> remove"], 296, 470],
               [[360, 600], ["break hidden ->", "make Rest a screen"], 290, 560]],
  };

  function sheetFor(name, label) {
    size(660, 700);
    const c = ctx(group(0, 0, 1));
    c.text(30, 34, label, { size: 21, bold: true });
    SCREENS[name](ctx(group(30, 50, 1)));
    (NOTES[name] || []).forEach(([[x, y], lines, tx, ty]) => note(c, x, y, lines, tx, ty));
  }

  function size(w, h) {
    svg.setAttribute("width", w); svg.setAttribute("height", h); svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
  }

  /* ---------------------------------------------------------------- composite figures */
  function arrow(c, x1, y1, x2, y2, o) {
    o = Object.assign({ strokeWidth: 1.8, roughness: 1 }, o || {});
    c.line(x1, y1, x2, y2, o);
    const a = Math.atan2(y2 - y1, x2 - x1), h = 12;
    c.line(x2, y2, x2 - h * Math.cos(a - 0.45), y2 - h * Math.sin(a - 0.45), o);
    c.line(x2, y2, x2 - h * Math.cos(a + 0.45), y2 - h * Math.sin(a + 0.45), o);
  }

  function box(c, x, y, w, h, lines, o) {
    c.rect(x, y, w, h, Object.assign({ strokeWidth: 2 }, o || {}));
    lines.forEach((l, i) => c.text(x + w / 2, y + h / 2 + 6 + (i - (lines.length - 1) / 2) * 22, l, { size: 18, anchor: "middle", bold: i === 0 }));
  }

  /* the main idea as a rough flow, drawn before any screen */
  function ideaFlow() {
    size(1400, 720);
    const c = ctx(group(0, 0, 1));
    c.text(30, 40, "NeuroPulse: main idea", { size: 24, bold: true });
    const W = 150, H = 76, Y = 320;
    const xs = [30, 225, 420, 615, 810, 1005, 1200];
    const main = [["open app"], ["Today", "one step"], ["start", "15 min"], ["Focus", "timer"], ["step", "done"], ["Rest", "3 min"], ["next step", "or stop"]];
    main.forEach((l, i) => {
      box(c, xs[i], Y, W, H, l, i === 1 ? { strokeWidth: 3 } : {});
      if (i < main.length - 1) arrow(c, xs[i] + W + 6, Y + H / 2, xs[i + 1] - 6, Y + H / 2);
    });
    box(c, 225, 120, W, H, ["Plan", "split work"]);
    arrow(c, 300, 200, 300, Y - 8);
    c.text(312, 260, "steps <= 15 min", { size: 15 });
    box(c, 810, 120, W + 20, H, ["Settings", "text, colour"]);
    c.text(992, 150, "from any screen,", { size: 15 }); c.text(992, 170, "no diagnosis", { size: 15 });
    c.path(`M${xs[6] + W / 2} ${Y + H + 6} Q ${700} ${Y + H + 130} ${300} ${Y + H + 8}`, { strokeWidth: 1.8, roughness: 1.2 });
    arrow(c, 312, Y + H + 20, 300, Y + H + 8);
    c.text(700, Y + H + 90, "next step: back to Today", { size: 15, anchor: "middle" });
    box(c, 615, 560, W + 20, H, ["Calm", "breathe, quiet"]);
    box(c, 900, 560, W + 40, H, ["talk to", "someone"]);
    arrow(c, 790, 598, 894, 598);
    c.text(420, 600, "overloaded?", { size: 17, bold: true }); c.text(420, 622, "(any screen)", { size: 15 });
    arrow(c, 530, 598, 609, 598);
    note(c, 30, 470, ["ONE thing at a time,", "the rest waits in Plan"], 282, 404);
    note(c, 1130, 470, ["rest is a step,", "not a prize.", "no streaks"], 1080, 404);
  }

  function bubble(c, x, y, w, lines) {
    c.ellipse(x + w / 2, y + lines.length * 11, w + 30, lines.length * 24 + 28);
    lines.forEach((l, i) => c.text(x + w / 2, y + 16 + i * 22, l, { size: 17, anchor: "middle" }));
  }

  function storyboard() {
    size(1500, 900);
    const c = ctx(group(0, 0, 1));
    const panels = [
      (p) => { SCREENS.home_a(ctx(group(40, 20, 0.42, p.g))); bubble(p, 230, 90, 180, ["six deadlines...", "where do I", "start?"]); },
      (p) => { SCREENS.today(ctx(group(40, 20, 0.42, p.g))); bubble(p, 230, 100, 180, ["just this one,", "15 minutes"]); },
      (p) => { SCREENS.step(ctx(group(40, 20, 0.42, p.g))); bubble(p, 230, 90, 180, ["so 'done' means", "three papers.", "I can do that"]); },
      (p) => { SCREENS.focus(ctx(group(40, 20, 0.42, p.g))); bubble(p, 230, 100, 180, ["no alarm,", "I can pause"]); },
      (p) => { SCREENS.rest(ctx(group(40, 20, 0.42, p.g))); bubble(p, 230, 100, 180, ["a break is", "the next task"]); },
      (p) => { SCREENS.progress(ctx(group(40, 20, 0.42, p.g))); bubble(p, 230, 100, 180, ["stopping here", "still counts"]); },
    ];
    const caps = [
      ["1. Every deadline is on screen at once.", "Alex (ADHD) can't decide where to start."],
      ["2. The app shows one step, how long", "it takes, and one Start button."],
      ["3. Alex checks what 'done' means.", "The step has an end."],
      ["4. Quiet timer. Time left visible.", "Pause is the biggest button."],
      ["5. Step done. 3 min rest comes next,", "as a task, not a prize."],
      ["6. Alex stops for the day. Progress shows", "what was done, no streak to lose."],
    ];
    panels.forEach((draw, i) => {
      const x = 20 + (i % 3) * 490, y = 20 + Math.floor(i / 3) * 440;
      c.rect(x, y, 470, 420, { strokeWidth: 2, roughness: 1.2 });
      c.line(x, y + 330, x + 470, y + 330, { strokeWidth: 1.6 });
      draw(ctx(group(x, y, 1)));
      caps[i].forEach((l, k) => c.text(x + 16, y + 362 + k * 26, l, { size: 19 }));
    });
  }

  function cards() {
    size(1500, 1130);
    const c = ctx(group(0, 0, 1));
    const lanes = [
      ["Plan to rest", [["today", "Today"], ["step", "Step"], ["focus", "Focus"], ["rest", "Rest"]]],
      ["Overload to calm", [["today", "any screen"], ["calm", "Calm"], ["progress", "Talk to someone"]]],
      ["Personalise", [["plan", "Plan"], ["settings", "Settings"], ["progress", "Progress"]]],
    ];
    lanes.forEach(([title, items], li) => {
      const y = 20 + li * 345;
      c.text(20, y + 150, title, { size: 27, bold: true });
      items.forEach(([s, label], i) => {
        const x = 260 + i * 300;
        c.rect(x, y, 190, 320, { strokeWidth: 1.8, roughness: 1.2 });
        SCREENS[s](ctx(group(x + 25, y + 12, 0.47, c.g)));
        c.text(x + 95, y + 310, label, { size: 19, anchor: "middle", bold: true });
        if (i < items.length - 1) note(c, x + 210, y + 150, [""], x + 290, y + 156);
      });
    });
    note(c, 820, 1110, ["Reading + Sensory merged into this one card"], 690, 1050);
  }

  function settingsV1() {
    size(1000, 700);
    const c = ctx(group(0, 0, 1));
    c.text(30, 34, "Reading + Sensory, first version", { size: 21, bold: true });
    SCREENS.reading_v1(ctx(group(30, 50, 1)));
    SCREENS.sensory_v1(ctx(group(360, 50, 1)));
    note(c, 690, 200, ["two places for", "one job"], 640, 160);
    note(c, 690, 400, ["links back", "to reading = loop"], 470, 420);
    note(c, 690, 540, ["-> merge into one", "Settings screen"]);
  }

  const FIGS = {
    storyboard, cards, settings_v1: settingsV1, idea_flow: ideaFlow,
    today: () => sheetFor("today", "Today"), plan: () => sheetFor("plan", "Plan"),
    step: () => sheetFor("step", "Step"), focus: () => sheetFor("focus", "Focus"),
    rest: () => sheetFor("rest", "Rest"), calm: () => sheetFor("calm", "Calm"),
    settings: () => sheetFor("settings", "Settings"), progress: () => sheetFor("progress", "Progress"),
    focus_v1: () => sheetFor("focus_v1", "Focus, first version"),
  };

  const fig = new URLSearchParams(location.search).get("fig") || "today";
  document.fonts.ready.then(() => { FIGS[fig](); document.title = "ready"; });
})();
