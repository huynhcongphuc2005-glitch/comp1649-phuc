"""Generate the NeuroPulse HE screens as static HTML for html.to.design.

Each output file in figma/ is one 430 x 932 artboard with no device frame,
no JavaScript and no pseudo-element decoration, so it imports into Figma as
clean auto-layout frames. Shared chrome (status bar, app bar, tab bar) comes
from the helpers below so every frame is identical.

Run:  python3 scripts/build_screens.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figma"

# ---------------------------------------------------------------- icons
def icon(name, size=20, stroke=2):
    paths = {
        "today": '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
        "plan": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3.5 6 1.5 1.5L7.5 5M3.5 12l1.5 1.5 2.5-2.5M3.5 18l1.5 1.5 2.5-2.5"/>',
        "progress": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "settings": '<path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/>',
        "calm": '<path d="M2 12c2.5-3 5-3 7.5 0s5 3 7.5 0 3.5-2 5-1"/><path d="M2 17c2.5-3 5-3 7.5 0s5 3 7.5 0 3.5-2 5-1" opacity=".5"/>',
        "back": '<path d="m15 18-6-6 6-6"/>',
        "play": '<path d="M7 4.5v15l12-7.5z" fill="currentColor" stroke="none"/>',
        "pause": '<path d="M8 5v14M16 5v14"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
        "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        "share": '<path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
        "chevron": '<path d="m9 6 6 6-6 6"/>',
        "split": '<path d="M12 3v6M12 9 6 15v6M12 9l6 6v6"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


# ---------------------------------------------------------------- chrome
STATUS = (
    '<div class="status-bar"><span>9:41</span>'
    '<div class="status-bar-icons">'
    '<svg width="18" height="12" viewBox="0 0 18 12" aria-hidden="true"><rect x="0" y="8" width="3" height="4" rx="1" fill="currentColor"/>'
    '<rect x="5" y="5" width="3" height="7" rx="1" fill="currentColor"/><rect x="10" y="2.5" width="3" height="9.5" rx="1" fill="currentColor"/>'
    '<rect x="15" y="0" width="3" height="12" rx="1" fill="currentColor"/></svg>'
    '<svg width="27" height="13" viewBox="0 0 27 13" aria-hidden="true"><rect x=".5" y=".5" width="23" height="12" rx="3.5" fill="none" stroke="currentColor" opacity=".4"/>'
    '<rect x="2" y="2" width="17" height="9" rx="2" fill="currentColor"/><rect x="25" y="4.5" width="2" height="4" rx="1" fill="currentColor" opacity=".4"/></svg>'
    '</div></div>'
)

CALM_PILL = f'<a class="calm-pill" href="06-calm.html" data-figma-link="06 Calm">{icon("calm", 16)}Calm</a>'


def app_bar(title, back=None, calm=True, lead_title=False):
    left = (f'<a class="icon-btn" href="{back}" aria-label="Back">{icon("back", 20)}</a>'
            if back else '')
    right = CALM_PILL if calm else ''
    return (f'<header class="app-bar"><div class="app-bar-side">{left}'
            f'{"<span class=app-bar-title>" + title + "</span>" if lead_title else ""}</div>'
            f'{"" if lead_title else "<span class=app-bar-title>" + title + "</span>"}'
            f'<div class="app-bar-side app-bar-side-end">{right}</div></header>')


TABS = [("today", "Today", "01-today.html"), ("plan", "Plan", "02-plan.html"),
        ("progress", "Progress", "08-progress.html"), ("settings", "Settings", "07-settings.html")]


def tab_bar(active):
    items = ''.join(
        f'<a class="tab{" tab-active" if key == active else ""}" href="{href}">{icon(key, 24)}<span>{label}</span></a>'
        for key, label, href in TABS)
    return f'<nav class="tab-bar" aria-label="Main">{items}</nav>'


def page(file, title, body, theme=""):
    cls = f' class="{theme}"' if theme else ''
    html = f"""<!DOCTYPE html>
<html lang="en"{cls}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=430, initial-scale=1">
<title>{title} · NeuroPulse HE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css">
</head>
<body>
<main class="screen" data-frame="{title}">
{STATUS}
{body}
</main>
</body>
</html>
"""
    (OUT / file).write_text(html, encoding="utf-8")


def step_row(title, meta, state="todo", last=False, go=False):
    done = state == "done"
    cls = "step-row" + (" step-row-current" if state == "current" else "") + (" step-row-last" if last else "")
    check = f'<span class="check{" check-done" if done else ""}">{icon("check", 14, 3)}</span>'
    title_cls = "step-title step-title-done" if done else "step-title"
    go_btn = f'<a class="step-go" href="03-step.html">{icon("play", 14)}</a>' if go else ''
    return (f'<li class="{cls}">{check}<div class="step-body"><span class="{title_cls}">{title}</span>'
            f'<span class="step-meta">{meta}</span></div>{go_btn}</li>')


def toggle(on):
    return f'<span class="toggle{" toggle-on" if on else ""}"><span class="toggle-knob"></span></span>'


def setting(title, desc, on, last=False):
    return (f'<div class="setting-row{" setting-row-last" if last else ""}"><div class="setting-text">'
            f'<span class="setting-title">{title}</span><span class="setting-desc">{desc}</span></div>{toggle(on)}</div>')


def segmented(options, active):
    return '<div class="segmented">' + ''.join(
        f'<span class="segment{" segment-active" if o == active else ""}">{o}</span>' for o in options) + '</div>'


def bar(pct):
    return f'<div class="bar"><div class="bar-fill" style="width:{pct}%"></div></div>'


PLAN_STEPS = [
    ("Read the brief and the marking rubric", "12 min · Done yesterday", "done"),
    ("List the three features you will build", "10 min · Done this morning", "done"),
    ("Find three peer-reviewed papers on neurodiverse learners", "15 min · Reading · next", "current"),
    ("Skim each paper and note one design implication", "15 min · Reading", "todo"),
    ("Sketch the five Norman principles for your interface", "12 min · Design", "todo"),
    ("Draft 300 words of the design section", "15 min · Writing", "todo"),
]

# ================================================================ screens

def today():
    body = f"""{app_bar("Today", lead_title=True)}
<section class="content">
  <div class="page-head">
    <span class="eyebrow">Friday 13 November</span>
    <h1 class="display">One thing<br>at a time.</h1>
  </div>
  <div class="card card-quiet" style="gap:10px">
    <div class="section-label"><span class="section-label-title">How full is your head?</span><span class="section-label-hint">optional</span></div>
    {segmented(["Clear", "Frayed", "Overloaded"], "Clear")}
  </div>
  <article class="card" style="gap:14px">
    <span class="tag">{icon("clock", 13, 2.4)}Next step · 15 min</span>
    <h2 class="card-title">Find three peer-reviewed papers on neurodiverse learners</h2>
    <span class="card-meta">COMP1649 · Step 3 of 6</span>
    <div class="btn-row">
      <a class="btn-primary btn-grow" href="04-focus.html">{icon("play", 16)}Start focus</a>
      <a class="btn-secondary" href="03-step.html">Details</a>
    </div>
  </article>
  <div class="note">{icon("info", 16)}<span><b>Why only this?</b> The rest of today's steps wait in Plan.</span></div>
  <a class="card card-quiet" href="02-plan.html" style="flex-direction:row;align-items:center;justify-content:space-between;padding:14px 18px">
    <span class="small"><b style="color:var(--ink)">2 more steps today</b> · saved in Plan</span>{icon("chevron", 18)}
  </a>
</section>
{tab_bar("today")}"""
    page("01-today.html", "01 Today", body)


def today_dashboard():
    """Control condition for the study: same visual system, full information load."""
    rows = ''.join(step_row(t, m, s if s != "current" else "todo", last=(i == 5), go=False)
                   for i, (t, m, s) in enumerate(PLAN_STEPS))
    rows2 = ''.join(step_row(t, m, "todo", last=(i == 2)) for i, (t, m) in enumerate([
        ("Clean the housing dataset", "20 min · Data"),
        ("Fit a baseline linear model", "25 min · Analysis"),
        ("Write up residual checks", "20 min · Writing")]))
    body = f"""{app_bar("Today", lead_title=True)}
<section class="content" style="gap:12px">
  <div class="page-head">
    <span class="eyebrow">Friday 13 November</span>
    <h1 class="display" style="font-size:26px">Your tasks</h1>
  </div>
  <div class="btn-row">
    <div class="card card-quiet btn-grow" style="padding:12px;gap:2px"><span class="eyebrow">Due</span><b>14 days</b><span class="step-meta">COMP1649</span></div>
    <div class="card card-quiet btn-grow" style="padding:12px;gap:2px"><span class="eyebrow">Due</span><b>21 days</b><span class="step-meta">COMP1648</span></div>
    <div class="card card-quiet btn-grow" style="padding:12px;gap:2px"><span class="eyebrow">Open</span><b>9 steps</b><span class="step-meta">this week</span></div>
  </div>
  <div class="section-label"><span class="section-label-title">COMP1649 · HCI</span><span class="section-label-hint">2 of 6 done</span></div>
  <ul class="step-list">{rows}</ul>
  <div class="section-label"><span class="section-label-title">COMP1648 · Data Science</span><span class="section-label-hint">0 of 3 done</span></div>
  <ul class="step-list">{rows2}</ul>
</section>
{tab_bar("today")}"""
    page("00-today-dashboard.html", "00 Today (control)", body)


def plan():
    rows = ''.join(step_row(t, m, s, last=(i == len(PLAN_STEPS) - 1), go=(s == "current"))
                   for i, (t, m, s) in enumerate(PLAN_STEPS))
    body = f"""{app_bar("Plan", lead_title=True)}
<section class="content">
  <div class="page-head">
    <span class="eyebrow">COMP1649 · Coursework</span>
    <h1 class="display" style="font-size:27px">Six steps. No mountain.</h1>
  </div>
  <div class="chip-row"><span class="chip chip-active">COMP1649</span><span class="chip">COMP1648</span><span class="chip">+ Add work</span></div>
  <div class="card" style="gap:10px;padding:16px 18px">
    <div class="section-label"><span class="section-label-title">Report and prototype</span><span class="section-label-hint">Due 27 Nov</span></div>
    {bar(33)}
    <span class="step-meta">2 of 6 steps · each step 15 min or less</span>
  </div>
  <ul class="step-list">{rows}</ul>
</section>
{tab_bar("plan")}"""
    page("02-plan.html", "02 Plan", body)


def step():
    def item(text):
        return (f'<li class="step-row"><span class="check">{icon("check", 14, 3)}</span>'
                f'<div class="step-body"><span class="step-title">{text}</span></div></li>')
    body = f"""{app_bar("Step 3 of 6", back="02-plan.html")}
<section class="content">
  <div class="chip-row"><span class="tag">{icon("clock", 13, 2.4)}15 min</span><span class="tag tag-sky">Reading</span><span class="tag tag-clay">No writing needed</span></div>
  <div class="page-head">
    <h1 class="display" style="font-size:27px">Find three peer-reviewed papers</h1>
  </div>
  <div class="card" style="gap:4px;padding:14px 18px">
    <div class="section-label"><span class="section-label-title">Finished looks like</span><span class="section-label-hint">0 / 3</span></div>
    <ul class="step-list">
      {item("One paper saved, with a sentence on why it matters")}
      {item("A second paper that disagrees with the first")}
      <li class="step-row step-row-last"><span class="check">{icon("check", 14, 3)}</span><div class="step-body"><span class="step-title">A third paper you can cite in the bibliography</span></div></li>
    </ul>
  </div>
  <div class="card card-quiet" style="gap:10px">
    <div class="section-label"><span class="section-label-title">Search terms</span><span class="section-label-hint">tap to copy</span></div>
    <div class="chip-row"><span class="chip">neurodiversity + HE</span><span class="chip">ADHD + university</span><span class="chip">autism + co-design</span></div>
  </div>
  <a class="btn-quiet" href="02-plan.html">{icon("split", 18)}Still too big? Split into 5-minute steps</a>
  <a class="btn-primary" href="04-focus.html">{icon("play", 16)}Start 15-minute focus</a>
</section>
{tab_bar("plan")}"""
    page("03-step.html", "03 Step", body)


def focus_ring(fraction, label, sub):
    r, c = 108, 2 * 3.14159 * 108
    dash = c * fraction
    return f"""<div style="display:flex;justify-content:center;padding:6px 0">
  <div style="width:250px;height:250px;display:flex;align-items:center;justify-content:center">
    <svg width="250" height="250" viewBox="0 0 250 250" aria-hidden="true" style="margin-right:-250px">
      <circle cx="125" cy="125" r="{r}" fill="none" stroke="var(--surface-2)" stroke-width="14"/>
      <circle cx="125" cy="125" r="{r}" fill="none" stroke="var(--sage)" stroke-width="14" stroke-linecap="round"
        stroke-dasharray="{dash:.1f} {c:.1f}" transform="rotate(-90 125 125)"/>
    </svg>
    <div style="width:250px;display:flex;flex-direction:column;align-items:center;gap:2px">
      <span style="font-size:52px;font-weight:600;letter-spacing:-.03em;font-variant-numeric:tabular-nums">{label}</span>
      <span class="small">{sub}</span>
    </div>
  </div>
</div>"""


def focus(paused=False):
    if paused:
        ring = focus_ring(0.76, "11:24", "paused · no time lost")
        controls = f"""<a class="btn-primary" href="04-focus.html">{icon("play", 16)}Resume</a>
  <a class="btn-quiet" href="05-rest.html">I finished early, end this step</a>"""
        sound = ""
    else:
        ring = focus_ring(0.76, "11:24", "minutes left")
        controls = f"""<a class="btn-primary" href="04b-focus-paused.html">{icon("pause", 18, 2.6)}Pause</a>
  <a class="btn-quiet" href="05-rest.html">I finished early, end this step</a>"""
        sound = f"""<div class="card card-quiet" style="gap:10px;padding:14px 16px">
    <div class="section-label"><span class="section-label-title">Sound</span><span class="section-label-hint">optional</span></div>
    {segmented(["Low hum", "Soft rain", "Off"], "Off")}
  </div>"""
    body = f"""{app_bar("Focus", back="03-step.html")}
<section class="content">
  <div class="page-head" style="align-items:center;text-align:center">
    <span class="eyebrow">Step 3 of 6 · Reading</span>
    <h1 class="card-title">Find three peer-reviewed papers on neurodiverse learners</h1>
    <span class="small">Nothing else is due right now.</span>
  </div>
  {ring}
  {controls}
  {sound}
</section>
{tab_bar("today")}"""
    page("04b-focus-paused.html" if paused else "04-focus.html",
         "04b Focus paused" if paused else "04 Focus", body)


def rest():
    body = f"""{app_bar("Step complete", calm=True)}
<section class="content">
  <div class="page-head">
    <span class="tag">{icon("check", 13, 3)}Done</span>
    <h1 class="display">That step is done.</h1>
    <p class="lede">You found three papers.</p>
  </div>
  <div class="btn-row">
    <div class="card btn-grow" style="gap:2px;padding:14px 16px"><span class="step-meta">Time focused</span><b style="font-size:20px">15 min</b></div>
    <div class="card btn-grow" style="gap:2px;padding:14px 16px"><span class="step-meta">Coursework</span><b style="font-size:20px">3 of 6 steps</b></div>
  </div>
  <article class="card card-sage" style="align-items:center;text-align:center;gap:8px">
    <span class="eyebrow" style="color:var(--sage-deep)">Rest</span>
    <span style="font-size:44px;font-weight:600;letter-spacing:-.02em;font-variant-numeric:tabular-nums">3:00</span>
    <span class="card-title" style="font-size:17px">Step away for three minutes</span>
    <span class="small">Stand up, look out of a window, drink some water.</span>
    <a class="btn-primary" href="01-today.html" style="width:100%;margin-top:6px">Start rest</a>
  </article>
  <div class="card card-quiet" style="gap:4px;padding:14px 18px">
    <span class="step-meta">Next step · not now</span>
    <span class="step-title">Skim each paper and note one design implication</span>
  </div>
  <a class="btn-secondary" href="01-today.html">Stop here for today</a>
</section>
{tab_bar("today")}"""
    page("05-rest.html", "05 Rest", body)


def calm(muted=False):
    phase, count = ("Breathe out", "3") if muted else ("Breathe in", "4")
    banner = (f'<div class="note" style="background:var(--sky-wash);color:var(--sky)">{icon("moon", 16)}'
              f'<span><b>Quiet mode is on until 8:00 tomorrow.</b> No reminders, badges or counts.</span></div>') if muted else ''
    action = ('<a class="btn-secondary" href="06-calm.html">Stop breathing guide</a>' if muted
              else f'<a class="btn-primary" href="06b-calm-muted.html">Start breathing</a>')
    body = f"""{app_bar("Calm", back="01-today.html", calm=False)}
<section class="content" style="gap:14px">
  <div class="page-head">
    <span class="eyebrow">Overload reset</span>
    <h1 class="display" style="font-size:27px">Let's make things quieter.</h1>
    <p class="lede">Nothing here needs a decision. Stay as long as you like.</p>
  </div>
  {banner}
  <div style="display:flex;justify-content:center">
    <div style="width:{'188' if muted else '210'}px;height:{'188' if muted else '210'}px;border-radius:999px;background:var(--sky-wash);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px">
      <span style="font-size:15px;font-weight:600;color:var(--sky)">{phase}</span>
      <span style="font-size:44px;font-weight:600;color:var(--sky)">{count}</span>
      <span class="step-meta">4-4-4-4 box breathing</span>
    </div>
  </div>
  {action}
  <div class="setting-group">
    {setting("Dim the colours", "Night palette, lower contrast", muted)}
    {setting("Silence everything", "No reminders or badges until tomorrow", muted)}
    {setting("Hide all numbers", "Removes counts and timers", muted, last=True)}
  </div>
  <a class="card card-quiet" href="08-progress.html" style="flex-direction:row;align-items:center;gap:12px;padding:14px 16px">
    {icon("person", 20)}<span class="small" style="flex:1"><b style="color:var(--ink)">Talk to someone</b><br>Adviser, wellbeing team or your tutor</span>{icon("chevron", 18)}
  </a>
  <a class="btn-quiet" href="01-today.html">I'm okay, back to Today</a>
</section>"""
    page("06b-calm-muted.html" if muted else "06-calm.html",
         "06b Calm quiet mode" if muted else "06 Calm", body, theme="theme-night" if muted else "")


def settings(applied=False):
    size, size_pct = ("19 px", 64) if applied else ("16 px", 28)
    spacing, sp_pct = ("0.04 em", 50) if applied else ("0.00 em", 6)
    face = "Atkinson" if applied else "Inter"
    colour = "Night" if applied else "Paper"
    def slider(title, value, pct, lo, hi):
        return (f'<div class="slider-row"><div class="slider-head"><span class="setting-title">{title}</span>'
                f'<span class="slider-value">{value}</span></div><div class="slider-track">'
                f'<div class="slider-fill" style="width:{pct}%"></div><div class="slider-thumb"></div></div>'
                f'</div>')
    applied_note = (f'<div class="note" style="background:var(--sage-wash);color:var(--sage-deep)">{icon("check", 16, 2.6)}'
                    f'<span><b>Applied everywhere.</b> Undo from this screen at any time.</span></div>') if applied else ''
    body = f"""{app_bar("Settings", lead_title=True)}
<section class="content" style="gap:12px">
  <p class="lede">Changes apply live, everywhere. No diagnosis or explanation needed.</p>
  {applied_note}
  <div class="card" style="gap:6px;padding:14px 16px">
    <span class="step-meta">Preview</span>
    <span style="font-family:{'var(--font-read)' if applied else 'var(--font-ui)'};font-size:{19 if applied else 16}px;letter-spacing:{'.04em' if applied else '0'};line-height:1.55">Find three peer-reviewed papers on neurodiverse learners.</span>
  </div>
  <div class="setting-group">
    {slider("Text size", size, size_pct, "A 14", "A 24")}
    {slider("Letter spacing", spacing, sp_pct, "tight", "wide")}
    <div class="slider-row setting-row-last" style="border-bottom:0"><span class="setting-title">Typeface</span>
      {segmented(["Inter", "Atkinson", "OpenDyslexic"], face)}</div>
  </div>
  <div class="setting-group">
    <div class="slider-row"><span class="setting-title">Colour</span>{segmented(["Paper", "Warm", "Night"], colour)}</div>
    {setting("Reduce motion", "No transitions or moving content", applied, last=True)}
  </div>
</section>
{tab_bar("settings")}"""
    page("07b-settings-applied.html" if applied else "07-settings.html",
         "07b Settings applied" if applied else "07 Settings", body,
         theme="theme-night text-large" if applied else "")


def progress():
    days = [("M", 45, False), ("T", 30, False), ("W", 0, True), ("T", 55, False), ("F", 25, False), ("S", 0, True), ("S", 0, False)]
    bars = ''.join(
        f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">'
        f'<div style="height:72px;width:100%;display:flex;align-items:flex-end;justify-content:center">'
        f'<div style="width:22px;height:{max(h * 1.2, 6)}px;border-radius:6px;background:{"var(--line)" if (rest or h == 0) else "var(--sage)"}"></div></div>'
        f'<span class="step-meta">{d}</span></div>' for d, h, rest in days)
    def help_row(ic, title, desc, last=False):
        return (f'<div class="setting-row{" setting-row-last" if last else ""}"><span style="color:var(--sage)">{icon(ic, 20)}</span>'
                f'<div class="setting-text"><span class="setting-title">{title}</span></div>{icon("chevron", 18)}</div>')
    body = f"""{app_bar("Progress", lead_title=True)}
<section class="content" style="gap:14px">
  <div class="page-head">
    <span class="eyebrow">This week</span>
    <h1 class="display" style="font-size:27px">A week that fits.</h1>
  </div>
  <div class="btn-row">
    <div class="card btn-grow" style="gap:0;padding:12px 14px"><b style="font-size:22px">4</b><span class="step-meta">steps finished</span></div>
    <div class="card btn-grow" style="gap:0;padding:12px 14px"><b style="font-size:22px">1 h 55</b><span class="step-meta">focused time</span></div>
    <div class="card btn-grow" style="gap:0;padding:12px 14px"><b style="font-size:22px">2</b><span class="step-meta">rest days</span></div>
  </div>
  <div class="card" style="gap:10px;padding:14px 16px">
    <div class="section-label"><span class="section-label-title">Focused minutes</span><span class="section-label-hint">Mon–Sun</span></div>
    <div style="display:flex;gap:6px">{bars}</div>
    <span class="setting-desc">Grey days are rest days.</span>
  </div>
  <div class="section-label"><span class="section-label-title">Help, when you want it</span></div>
  <div class="setting-group">
    {help_row("person", "Disability and dyslexia adviser", "Book a 20-minute call")}
    {help_row("calendar", "Request an adjustment or extension", "Opens the university form")}
    {help_row("share", "Share a summary with your tutor", "You choose what is included", last=True)}
  </div>
  <div class="note">{icon("info", 16)}<span>No streaks. Skipping a day resets nothing.</span></div>
</section>
{tab_bar("progress")}"""
    page("08-progress.html", "08 Progress", body)


SCREENS = [
    ("01-today.html", "01 Today", "One next action"),
    ("02-plan.html", "02 Plan", "Work split into ≤15-minute steps"),
    ("03-step.html", "03 Step", "Definition of done and one start"),
    ("04-focus.html", "04 Focus", "Timer without time pressure"),
    ("04b-focus-paused.html", "04b Focus paused", "State variant"),
    ("05-rest.html", "05 Rest", "Rest as a legitimate next task"),
    ("06-calm.html", "06 Calm", "Low-demand overload reset"),
    ("06b-calm-muted.html", "06b Calm quiet mode", "State variant"),
    ("07-settings.html", "07 Settings", "Reading and sensory control"),
    ("07b-settings-applied.html", "07b Settings applied", "State variant"),
    ("08-progress.html", "08 Progress", "Progress without streaks, routes to people"),
    ("00-today-dashboard.html", "00 Today (control)", "Study control condition"),
]


def index():
    cards = ''.join(
        f'<figure><iframe src="{f}" width="430" height="932" loading="lazy" title="{t}"></iframe>'
        f'<figcaption><a href="{f}">{t}</a> — {d}</figcaption></figure>' for f, t, d in SCREENS)
    (OUT / "index.html").write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NeuroPulse HE screens</title>
<style>
body{{margin:0;padding:32px;background:#E9E6DC;font:14px/1.5 Inter,Arial,sans-serif;color:#171E19}}
h1{{font-size:20px;margin:0 0 4px}} p{{margin:0 0 24px;color:#4A544C}}
.grid{{display:flex;flex-wrap:wrap;gap:28px}}
figure{{margin:0;width:258px}} iframe{{border:0;border-radius:18px;background:#fff;transform:scale(.6);transform-origin:0 0;margin:0 0 -373px 0}}
figcaption{{margin-top:8px}} a{{color:#34503F;font-weight:600}}
</style></head><body>
<h1>NeuroPulse HE — screens for Figma</h1>
<p>Preview only. Import each screen file (not this page) with html.to.design at 430 × 932.</p>
<div class="grid">{cards}</div></body></html>
""", encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    today(); today_dashboard(); plan(); step(); focus(); focus(paused=True); rest()
    calm(); calm(muted=True); settings(); settings(applied=True); progress(); index()
    print("wrote", len(SCREENS), "screens + index to", OUT)
