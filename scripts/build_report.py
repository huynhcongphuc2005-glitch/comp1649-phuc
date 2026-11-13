"""Build report/COMP1649_Coursework_Report.docx with python-docx.

Run after scripts/capture.sh, scripts/build_figures.py and scripts/build_sketches.sh:
    python3 scripts/build_report.py
Two passes: the first is rendered with LibreOffice to find page numbers for
the contents, list of figures and list of tables; the second writes them in.
Prints the Introduction-to-Conclusion word count and checks citations.
Fill STUDENT below before submission.
"""
import re
import subprocess
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "report" / "figures"
SK = FIG / "sketches"
OUT = ROOT / "report" / "COMP1649_Coursework_Report.docx"

STUDENT = {"name": "[Student name]", "id": "[Student ID]", "tutor": "[Tutor name]", "date": "November 2026"}

ACCENT = RGBColor(0x34, 0x50, 0x3F)
LINK = "0563C1"
JUSTIFY = WD_ALIGN_PARAGRAPH.JUSTIFY

# =====================================================================
# Figures and tables (numbered in this order)
# =====================================================================
FIGURES = [
    ("idea_flow", SK / "idea_flow.png", "First paper sketch of the main idea as a flow"),
    ("focus_v1", SK / "focus_v1.png", "First sketch of the focus screen"),
    ("settings_v1", SK / "settings_v1.png", "First sketches of the reading and sensory screens"),
    ("storyboard", SK / "storyboard.png", "Storyboard of the planning journey"),
    ("cards", SK / "cards.png", "Card-based prototype of the three journeys"),
    ("visibility", FIG / "norman-visibility.png", "Visibility on the Today screen"),
    ("feedback", FIG / "norman-feedback.png", "Feedback on the Focus screen"),
    ("constraints", FIG / "norman-constraints.png", "Constraints on the Step screen"),
    ("consistency", FIG / "norman-consistency.png", "Consistency on the Settings screen"),
    ("affordance", FIG / "norman-affordance.png", "Affordances and signifiers on the Calm screen"),
    ("flow_planning", FIG / "flow-planning.png", "Screen flow of the planning journey"),
    ("flow_overload", FIG / "flow-overload.png", "Screen flow of the overload journey"),
    ("flow_personalise", FIG / "flow-personalise.png", "Screen flow of the personalisation journey"),
    ("control", FIG / "screen-00-today-dashboard.png", "Dashboard home screen used as the control condition"),
]
APPENDIX_FIGURES = [
    ("sk_today", SK / "today.png", "D1", "Sketch of the Today screen"),
    ("sk_plan", SK / "plan.png", "D2", "Sketch of the Plan screen"),
    ("sk_step", SK / "step.png", "D3", "Sketch of the Step screen"),
    ("sk_focus", SK / "focus.png", "D4", "Sketch of the Focus screen"),
    ("sk_rest", SK / "rest.png", "D5", "Sketch of the Rest screen"),
    ("sk_calm", SK / "calm.png", "D6", "Sketch of the Calm screen"),
    ("sk_settings", SK / "settings.png", "D7", "Sketch of the Settings screen"),
    ("sk_progress", SK / "progress.png", "D8", "Sketch of the Progress screen"),
    ("e_today", FIG / "screen-01-today.png", "E1", "Today screen"),
    ("e_plan", FIG / "screen-02-plan.png", "E2", "Plan screen"),
    ("e_step", FIG / "screen-03-step.png", "E3", "Step screen"),
    ("e_focus", FIG / "screen-04-focus.png", "E4", "Focus screen"),
    ("e_paused", FIG / "screen-04b-focus-paused.png", "E5", "Focus screen, paused state"),
    ("e_rest", FIG / "screen-05-rest.png", "E6", "Rest screen"),
    ("e_calm", FIG / "screen-06-calm.png", "E7", "Calm screen"),
    ("e_quiet", FIG / "screen-06b-calm-muted.png", "E8", "Calm screen, quiet mode on"),
    ("e_settings", FIG / "screen-07-settings.png", "E9", "Settings screen"),
    ("e_applied", FIG / "screen-07b-settings-applied.png", "E10", "Settings screen after changes are applied"),
    ("e_progress", FIG / "screen-08-progress.png", "E11", "Progress screen"),
    ("e_control", FIG / "screen-00-today-dashboard.png", "E12", "Dashboard home screen (study control condition)"),
]
FNUM = {k: str(i) for i, (k, _, _) in enumerate(FIGURES, 1)}
FNUM.update({k: n for k, _, n, _ in APPENDIX_FIGURES})
FPATH = {k: p for k, p, *_ in FIGURES + [(a, b) for a, b, *_ in APPENDIX_FIGURES]}
FCAP = {k: c for k, _, c in FIGURES}
FCAP.update({k: c for k, _, _, c in APPENDIX_FIGURES})
TABLES = [("req", "Requirements taken from the literature"),
          ("search", "Search strings, databases and sources retained"),
          ("map", "Interactions connected in Figma")]
TNUM = {k: str(i) for i, (k, _) in enumerate(TABLES, 1)}


def F(k):
    return f"Figure {FNUM[k]}"


def T(k):
    return f"Table {TNUM[k]}"


# =====================================================================
# Citations: author string, year, bookmark
# =====================================================================
CITES = [
    ("Clouder et al.", "2020", "ref_clouder"), ("McDowall and Kiseleva", "2024", "ref_mcdowall"),
    ("Van Hees, Moyson and Roeyers", "2015", "ref_vanhees"), ("Sonne et al.", "2016", "ref_sonne"),
    ("Spiel et al.", "2022", "ref_spiel"), ("Rello and Baeza-Yates", "2013", "ref_rello"),
    ("Zervogianni et al.", "2020", "ref_zervogianni"), ("Morris, Begel and Wiedermann", "2015", "ref_morris"),
    ("Norman", "2013", "ref_norman"), ("Rogers, Sharp and Preece", "2023", "ref_rogers"),
    ("Brooke", "1996", "ref_brooke"), ("Braun and Clarke", "2006", "ref_braun"),
]
CITE_RE = re.compile("|".join(
    rf"(?P<c{i}>{re.escape(a)}(?:'s)? \({y}\)?|{re.escape(a)}, {y})" for i, (a, y, _) in enumerate(CITES)))
XREF = r"\b(?:Figure [DE]?\d+|Table \d+|Appendix [A-F])\b"
LINK_RE = re.compile(f"(?P<x>{XREF})|" + CITE_RE.pattern)


def xref_anchor(label):
    kind, num = label.split(" ")
    return {"Figure": "fig_", "Table": "tab_", "Appendix": "app_"}[kind] + num

# =====================================================================
# Text (everything from Introduction to Conclusion is counted)
# =====================================================================
INTRO = [
    "This report covers Option A of the COMP1649 brief, a digital application for neurodiverse learners in higher education. The product, NeuroPulse HE, is a phone app for undergraduates with ADHD, autism or dyslexia. Many of these students have the ability to do well but struggle with how university work is organised and with getting started on it (Clouder et al., 2020). The app aims to make starting easier, to give rest a proper place in the study day, and to let students change the interface without having to explain why.",
    "The prototype supports three core journeys. In the first, a student works through a plan of short steps, completes one step with a focus timer and then rests. In the second, a student who feels overloaded moves to a calm, low-demand screen. In the third, a student adjusts text and colour to suit them. Section 2 reviews the literature, Section 3 covers the concept, the design process and Norman's (2013) principles, Section 4 presents the Figma prototype, Section 5 proposes a study and Section 6 reflects on what I learned.",
]

BIB_INTRO = "The search strategy is given in Appendix A. Each source below added a different requirement to the design."

BIB = [
    "**Clouder et al. (2020)** carried out a systematic review of international research on how neurodiverse students experience higher education. They found that support services and technologies exist but often do not match what students need, and that fear of stigma and labels makes this gap wider. I chose this review because it treats the problem as an institutional one rather than a problem with the student. For my design it meant that no feature should depend on disclosing a diagnosis, which became requirement R3.",
    "**McDowall and Kiseleva (2024)** brought together earlier reviews of support for neurodivergent students. The evidence they found was modest, mostly from the United States and based on small samples, and technology was only one type of support among several. I picked this review because it is recent and it stopped me from claiming too much for an app. It led to requirement R5, that the app points students to human advisers, and to treating the prototype as something to be tested in Section 5.",
    "**Van Hees, Moyson and Roeyers (2015)** interviewed 23 autistic students in higher education. The students described problems with new situations and sudden changes, social relationships, processing information and managing time, and many were unsure whether to disclose. I chose the paper because the evidence comes from students themselves. It supports screens that behave predictably, a plan that only changes when the student changes it, and a rest screen that treats recovery as part of studying (R2).",
    "**Sonne et al. (2016)** present a design framework for ADHD assistive technology that links the challenges people with ADHD face to opportunities for technology, with practical design strategies. I selected it because it changed my first idea of a planner with many features. Following its approach of targeting one challenge at a time, the Today screen focuses on starting and shows only the next step, its length and one Start button (R1).",
    "**Spiel et al. (2022)** review technology research on ADHD from the position of neurodivergent researchers. They found that most systems try to reduce behaviour that does not fit neurotypical norms, and that people with ADHD are rarely involved in setting research goals. I chose this paper because it questioned the productivity apps I had been using as references. As a result I removed streaks, scores and badges (R4), and the study in Section 5 recruits neurodivergent students to judge the design.",
    "**Rello and Baeza-Yates (2013)** used eye-tracking with 48 readers with dyslexia to compare twelve fonts. Sans serif, monospaced and roman styles were read faster than serif, proportional and italic styles. I selected it because it gives evidence for a choice that is often made on looks alone. The prototype therefore uses the sans serif roman typefaces Inter and Atkinson Hyperlegible and avoids italic text. OpenDyslexic is offered as a personal choice but is not the default.",
    "**Zervogianni et al. (2020)** ran a Delphi study in which 27 autistic people, family members, practitioners and researchers agreed what counts as good evidence for digital support. The panel agreed on reliability, engagement and effectiveness. It shaped what my study measures: whether students start and keep going, and how quickly they start, not only whether they like the app.",
    "**Morris, Begel and Wiedermann (2015)** interviewed ten neurodiverse technology workers and then surveyed 846 engineers. They show that skilled people are held back by their working environment rather than their ability. I chose it as an HCI study of adults close in age to my users, and my study copies its mix of interviews with a structured measure.",
]

USERS = "The main persona is Alex, a second-year computing student with ADHD. Alex works well once started but loses a lot of time deciding where to begin, and notifications and noise quickly become too much. Other users include autistic students, who value predictability, and dyslexic students, who need control over text. The app is used on a phone in short sessions at home, in the library or between lectures."

CONCEPT = [
    "The concept is a calm companion that hands the student one card at a time. The whole plan is stored, but the home screen only shows the top card. The main tasks are to break work into steps, to start, pause and finish a step, to rest, to calm down when overloaded and to adjust the interface. Of the interaction types described by Rogers, Sharp and Preece (2023), the app relies mostly on instructing, such as tapping Start or Pause, and on manipulating, where sliders and switches change the interface straight away.",
    "Four main areas are reached from a tab bar: Today, Plan, Progress and Settings. A Calm button sits at the top right of every screen, so a quiet space is always one tap away. Calm uses a wave icon and a blue tint so that it stands out from the green used for actions.",
]

REQ_INTRO = f"{T('req')} shows the five requirements taken from Section 2 and where each one appears in the prototype. They also explain what was left out, such as a social feed, a leaderboard and deadline countdowns."

REQS = [
    ("R1 One next action", "Only the next step is shown, with its length and one Start button.", "Today, Step", "Sonne et al. (2016)"),
    ("R2 Rest as a state", "Every focus session ends with a rest screen; stopping is never marked as missed.", "Rest", "Van Hees, Moyson and Roeyers (2015)"),
    ("R3 Adjustment without disclosure", "Reading and sensory settings are in the main navigation and ask for no diagnosis.", "Settings, Calm", "Clouder et al. (2020)"),
    ("R4 No normative scoring", "Progress shows steps, time and rest days separately, with no streaks or badges.", "Progress", "Spiel et al. (2022)"),
    ("R5 Route to people", "Calm and Progress link to an adviser, adjustments and the tutor.", "Calm, Progress", "McDowall and Kiseleva (2024)"),
]

ASSUMPTIONS = "Some details do not come from the sources above and are treated as assumptions for the study to check. Steps are capped at 15 minutes, the Calm screen uses 4-4-4-4 paced breathing, the home screen offers an optional check-in on how full the student's head feels, and the palette is muted with one accent colour for actions. The size and spacing controls are also an assumption, because Rello and Baeza-Yates (2013) only compared typefaces. The interview in Appendix B asks about each of these."

PROCESS_INTRO = "I followed the move from low-fidelity paper prototypes to a mid-fidelity digital prototype described by Rogers, Sharp and Preece (2023, ch. 12)."

IDEA = f"I started by drawing the main idea as a rough flow on paper ({F('idea_flow')}). Opening the app leads straight to one step on Today. Starting it runs a short focus session, and a finished step leads to a rest before the next step or stopping for the day. Plan feeds steps into Today, while Calm and Settings can be reached from any screen."

SKETCHING = "From this flow I sketched each screen in pencil, wrote notes in red and changed the sketches after checking them against the requirements. The final sketch of every screen is in Appendix D. The two largest changes follow."

PROCESS = {
    "focus_v1": f"The first focus screen ({F('focus_v1')}) had Pause and Stop buttons of the same size, and a pop-up with points and a streak at the end. Equal buttons make it easy to end a session by mistake, and the points and streak are the kind of measure Spiel et al. (2022) criticise. Pause became the main button, Stop became a small text link and the pop-up was replaced by a full Rest screen.",
    "settings_v1": f"Reading and sensory settings began as two screens ({F('settings_v1')}). Both served one purpose, and the Sensory screen linked back to Reading. I merged them into one Settings screen where every change is shown immediately.",
}

STORY = f"Next I drew a storyboard of the planning journey ({F('storyboard')}). Drawing the scenes in order showed that the moment after a step is finished matters as much as the start, which supported giving rest its own screen."

CARDS = f"Finally, I made a card-based prototype with one paper card per screen, arranged by journey ({F('cards')}). Walking through the cards confirmed that each journey could be completed with no dead ends."

NORMAN_INTRO = "Five of Norman's (2013) principles were applied as shown below. The numbers in each figure match the numbers in the text."

NORMAN = [
    ("visibility", "Visibility", f"On the Today screen ({F('visibility')}) the next step is the largest element (1), so the student does not have to search for what to do. The Calm button (2) stays in the same place on every screen, so the way out of an overwhelming moment can always be seen."),
    ("feedback", "Feedback", f"On the Focus screen ({F('feedback')}) the ring shortens as time passes and the remaining minutes are shown as a number (1), so progress is clear without an alarm. Tapping Pause (2) changes the screen to a paused state with a Resume button and a message that no time has been lost."),
    ("constraints", "Constraints", f"On the Step screen ({F('constraints')}) the tags limit the step to 15 minutes and state the type of work (1). The checklist (2) defines when the step is finished, so the task has a clear end. If the step still feels too big, the student can split it (3) instead of giving up."),
    ("consistency", "Consistency", f"The Settings screen ({F('consistency')}) uses the same segmented control for typeface (1) and colour (2). The tab bar (3) and the Calm button (4) look the same and sit in the same place on every screen. This supports the predictability that autistic students value."),
    ("affordance", "Affordance and signifiers", f"On the Calm screen ({F('affordance')}) the main action is a wide filled button with a clear label (1). The switches (2) use the familiar mobile toggle shape, and the arrow on the support row (3) shows that it opens another page. Norman (2013) separates what an object allows from the signifiers that show it, so each label names its action."),
]

PROTO_INTRO = "The prototype has eight main screens, three extra states and one control screen for the study. I built the screens in HTML and CSS at 430 by 932 pixels, one file per screen. Each screen was then imported into Figma Design with the html.to.design plug-in, and the interactions were connected in Figma's prototype mode (Appendix F), so a participant can complete all three journeys by tapping through the screens. Full-size screenshots of every screen and state are in Appendix E."

FLOW_TEXT = {
    "flow_planning": [
        f"**Today** ({F('e_today')}) shows one step, how long it takes and a Start focus button. An optional check-in asks how full the student's head is.",
        f"**Step** ({F('e_step')}) shows the step's length and type, a checklist that defines 'finished' and suggested search terms, with one button to start.",
        f"**Focus** ({F('e_focus')}) shows the remaining time as a shrinking ring and a number. Pause is the main control and leads to a paused state ({F('e_paused')}); ending early uses a small text link.",
        f"**Rest** ({F('e_rest')}) says what was done, offers a three-minute break as the next task and shows the next step without pressure.",
    ],
    "flow_overload": [
        f"**Calm** ({F('e_calm')}) is reached from any screen. It offers paced breathing and switches that dim the colours, silence reminders and hide numbers ({F('e_quiet')}). It has no tab bar, which means fewer decisions.",
        f"**Progress** ({F('e_progress')}) shows steps, focused time and rest days as separate counts rather than a score, and links to an adviser, the extension process and a summary the student can share.",
    ],
    "flow_personalise": [
        f"**Plan** ({F('e_plan')}) holds all the steps for a module. Every step takes 15 minutes or less, and the current step is shaded with a play button.",
        f"**Settings** ({F('e_settings')}) lets the student change text size, letter spacing, typeface, colour and motion, with a live preview ({F('e_applied')}). No reason or diagnosis is asked for.",
    ],
}

PURPOSE = f"The prototype is mid-fidelity in the sense used by Rogers, Sharp and Preece (2023): layout, content, navigation and states are fixed, but accounts, notifications and data storage are not built. It is meant to communicate the concept and to serve as the study instrument. Each journey tests an assumption: that one step with a clear end makes starting easier, that a visible low-demand exit gets used, and that students adjust the interface when no disclosure is needed. For the study the prototype also includes a control version of the home screen that lists every task ({F('control')}; full size in {F('e_control')})."

STUDY_INTRO = "The main assumption behind the design is that showing one next action, instead of the whole plan, helps neurodivergent students start work. This study tests that assumption with the Figma prototype and also collects evidence of engagement and effectiveness, as recommended by Zervogianni et al. (2020)."

STUDY = [
    ("5.1 Research questions and hypothesis",
     "The first research question asks whether a home screen showing one next action reduces the time neurodivergent students take to start a task compared with a dashboard. The hypothesis is that time to first action will be shorter with the one-step screen (condition A) than with the dashboard (condition B). The second research question asks how usable students find the three journeys and how they experience the rest and calm features."),
    ("5.2 Participants and recruitment",
     "Twelve undergraduates who describe themselves as neurodivergent will take part. A diagnosis is not required, in line with Clouder et al. (2020). Participants will be recruited through the Disability and Dyslexia Service mailing list, student societies and posters, and will receive a £10 voucher. Two pilot sessions will check timing and wording first."),
    ("5.3 Design and procedure",
     "The study uses a within-subjects design, so every participant uses both home screens. Half will see condition A first and half condition B, to balance learning effects. Each 45-minute session follows the script in Appendix B. After consent and a background questionnaire, the participant completes three tasks on the prototype while thinking aloud. In the first task they start the next piece of work in each condition, in the second they pause a focus session and find somewhere quieter, and in the third they make the text larger and the screen darker. The session ends with the System Usability Scale (Brooke, 1996) and a short interview. Breaks are allowed at any time."),
    ("5.4 Data collection",
     "Screen and audio recordings give the time to first action, measured from the screen appearing to the first tap on a start control, together with task success, errors and think-aloud comments. The questionnaires give SUS scores and a preference between the two home screens."),
    ("5.5 Analysis",
     "Time to first action in the two conditions will be compared with a Wilcoxon signed-rank test, because the sample is small and timing data are usually skewed. SUS scores and task success will be reported descriptively. Think-aloud and interview data will be analysed with thematic analysis (Braun and Clarke, 2006), and the themes will be compared with the requirements in Table 1."),
    ("5.6 Justification and limitations",
     "A within-subjects design suits this group because individual differences are large and each participant acts as their own control. The tasks are simulated, twelve participants only allow exploratory statistics, and being observed may change behaviour, so a later two-week field study would show whether any effect lasts."),
    ("5.7 Ethics",
     "The study needs approval from the university ethics committee. Data will be pseudonymised, stored on university systems in line with UK GDPR and deleted at the end of the project. No health information is collected beyond how participants describe themselves."),
]

CONCLUSION = [
    "The most important thing I learned is that designing for this group often means taking features away. My first sketches looked like the productivity apps I already used, with a dashboard, countdowns, streaks and points. Reading Spiel et al. (2022) made me see that these features reward one particular way of working, and the storyboard showed me how much a single pop-up can interrupt someone who has just managed to start. Removing features was harder than adding them, because I had to justify every element that stayed.",
    "I was also surprised by how much Norman's (2013) principles matter for accessibility. I had thought of visibility, feedback and constraints as general usability rules, but for a student who is already overloaded they decide whether the student can act at all. In future projects I want to start from what users say about their own experience, write requirements from research before designing screens, and test with the people a product is meant for rather than relying on my own sense of what is easy.",
]

REFERENCES = [
    ("ref_braun", "Braun, V. and Clarke, V. (2006) 'Using thematic analysis in psychology', *Qualitative Research in Psychology*, 3(2), pp. 77–101.", "https://doi.org/10.1191/1478088706qp063oa"),
    ("ref_brooke", "Brooke, J. (1996) 'SUS: a \"quick and dirty\" usability scale', in Jordan, P.W., Thomas, B., Weerdmeester, B.A. and McClelland, I.L. (eds) *Usability evaluation in industry*. London: Taylor & Francis, pp. 189–194.", None),
    ("ref_clouder", "Clouder, L., Karakus, M., Cinotti, A., Ferreyra, M.V., Fierros, G.A. and Rojo, P. (2020) 'Neurodiversity in higher education: a narrative synthesis', *Higher Education*, 80(4), pp. 757–778.", "https://doi.org/10.1007/s10734-020-00513-6"),
    ("ref_mcdowall", "McDowall, A. and Kiseleva, M. (2024) 'A rapid review of supports for neurodivergent students in higher education. Implications for research and practice', *Neurodiversity*, 2.", "https://doi.org/10.1177/27546330241291769"),
    ("ref_morris", "Morris, M.R., Begel, A. and Wiedermann, B. (2015) 'Understanding the challenges faced by neurodiverse software engineering employees: towards a more inclusive and productive technical workforce', in *Proceedings of the 17th International ACM SIGACCESS Conference on Computers & Accessibility (ASSETS '15)*. New York: ACM, pp. 173–184.", "https://doi.org/10.1145/2700648.2809841"),
    ("ref_norman", "Norman, D.A. (2013) *The design of everyday things*. Revised and expanded edn. New York: Basic Books.", None),
    ("ref_rello", "Rello, L. and Baeza-Yates, R. (2013) 'Good fonts for dyslexia', in *Proceedings of the 15th International ACM SIGACCESS Conference on Computers and Accessibility (ASSETS '13)*. New York: ACM, pp. 1–8.", "https://doi.org/10.1145/2513383.2513447"),
    ("ref_rogers", "Rogers, Y., Sharp, H. and Preece, J. (2023) *Interaction design: beyond human-computer interaction*. 6th edn. Hoboken, NJ: Wiley.", None),
    ("ref_sonne", "Sonne, T., Marshall, P., Obel, C., Thomsen, P.H. and Grønbæk, K. (2016) 'An assistive technology design framework for ADHD', in *Proceedings of the 28th Australian Conference on Computer-Human Interaction (OzCHI '16)*. New York: ACM, pp. 60–70.", "https://doi.org/10.1145/3010915.3010925"),
    ("ref_spiel", "Spiel, K., Hornecker, E., Williams, R.M. and Good, J. (2022) 'ADHD and technology research – investigated by neurodivergent readers', in *Proceedings of the 2022 CHI Conference on Human Factors in Computing Systems (CHI '22)*. New York: ACM, pp. 1–21.", "https://doi.org/10.1145/3491102.3517592"),
    ("ref_vanhees", "Van Hees, V., Moyson, T. and Roeyers, H. (2015) 'Higher education experiences of students with autism spectrum disorder: challenges, benefits and support needs', *Journal of Autism and Developmental Disorders*, 45(6), pp. 1673–1688.", "https://doi.org/10.1007/s10803-014-2324-2"),
    ("ref_zervogianni", "Zervogianni, V., Fletcher-Watson, S., Herrera, G., Goodwin, M., Pérez-Fuster, P., Brosnan, M. and Grynszpan, O. (2020) 'A framework of evidence-based practice for digital support, co-developed with and for the autism community', *Autism*, 24(6), pp. 1411–1422.", "https://doi.org/10.1177/1362361319898331"),
]

SEARCH = [
    ("\"neurodivergent\" OR \"neurodiverse\" AND \"higher education\"", "Scopus, Google Scholar", "Clouder et al. (2020); McDowall and Kiseleva (2024)"),
    ("\"autism\" AND (\"university\" OR \"college\") AND \"support needs\"", "PubMed, Scopus", "Van Hees, Moyson and Roeyers (2015)"),
    ("\"ADHD\" AND (\"assistive technology\" OR \"design framework\")", "ACM Digital Library", "Sonne et al. (2016); Spiel et al. (2022)"),
    ("\"dyslexia\" AND (\"font\" OR \"typography\") AND \"reading\"", "ACM Digital Library", "Rello and Baeza-Yates (2013)"),
    ("\"autism\" AND \"digital support\" AND \"evidence\"", "PubMed, Google Scholar", "Zervogianni et al. (2020)"),
    ("\"neurodiverse\" AND (\"software engineers\" OR \"workplace\")", "ACM Digital Library", "Morris, Begel and Wiedermann (2015)"),
]

SUS_ITEMS = [
    "I think that I would like to use this system frequently.", "I found the system unnecessarily complex.",
    "I thought the system was easy to use.", "I think that I would need the support of a technical person to be able to use this system.",
    "I found the various functions in this system were well integrated.", "I thought there was too much inconsistency in this system.",
    "I would imagine that most people would learn to use this system very quickly.", "I found the system very cumbersome to use.",
    "I felt very confident using the system.", "I needed to learn a lot of things before I could get going with this system.",
]

FIGMA_LINKS = [
    ("Today", "Start focus", "Focus"), ("Today", "Details", "Step"), ("Today", "2 more steps today", "Plan"),
    ("Plan", "Play button on the current step", "Step"), ("Step", "Start 15-minute focus", "Focus"),
    ("Focus", "Pause", "Focus, paused"), ("Focus, paused", "Resume", "Focus"),
    ("Focus and Focus, paused", "I finished early, end this step", "Rest"), ("Rest", "Start rest; Stop here for today", "Today"),
    ("Every screen", "Calm button", "Calm"), ("Calm", "Start breathing", "Calm, quiet mode"),
    ("Calm and Calm, quiet mode", "I'm okay, back to Today", "Today"), ("Calm and Calm, quiet mode", "Talk to someone", "Progress"),
    ("Settings", "Night colour option", "Settings, applied"), ("Tab bar", "Today, Plan, Progress, Settings", "Matching screen"),
]

# =====================================================================
# docx helpers
# =====================================================================
COUNTED = []


def counted(text):
    COUNTED.append(text)
    return text


def _rpr(bold=False, italic=False, size=None, color=None, underline=False):
    rPr = OxmlElement("w:rPr")
    for flag, tag in ((bold, "w:b"), (italic, "w:i")):
        if flag:
            rPr.append(OxmlElement(tag))
    if color:
        c = OxmlElement("w:color"); c.set(qn("w:val"), color); rPr.append(c)
    if size:
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(int(size * 2))); rPr.append(s)
    if underline:
        u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    return rPr


def hyperlink(p, text, anchor=None, url=None, bold=False, italic=False, size=None):
    h = OxmlElement("w:hyperlink")
    if url:
        h.set(qn("r:id"), p.part.relate_to(url, RT.HYPERLINK, is_external=True))
    else:
        h.set(qn("w:anchor"), anchor)
    h.set(qn("w:history"), "1")
    r = OxmlElement("w:r")
    r.append(_rpr(bold, italic, size, color=LINK if url else None, underline=bool(url)))
    t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = text
    r.append(t); h.append(r); p._p.append(h)


def plain_run(p, text, bold=False, italic=False, size=None):
    r = p.add_run(text); r.bold = bold or None; r.italic = italic or None
    if size:
        r.font.size = Pt(size)


def add_runs(p, text, size=None, link_cites=True):
    """**bold**, *italic*, and author-year citations as internal links."""
    for part in re.split(r"(\*\*.+?\*\*|\*.+?\*)", text):
        if not part:
            continue
        bold, italic = part.startswith("**"), part.startswith("*") and not part.startswith("**")
        seg = part[2:-2] if bold else part[1:-1] if italic else part
        pos = 0
        if link_cites:
            for m in LINK_RE.finditer(seg):
                plain_run(p, seg[pos:m.start()], bold, italic, size)
                if m.lastgroup == "x":
                    anchor = xref_anchor(m.group(0))
                else:
                    anchor = CITES[int(m.lastgroup[1:])][2]
                hyperlink(p, m.group(0), anchor=anchor, bold=bold, italic=italic, size=size)
                pos = m.end()
        plain_run(p, seg[pos:], bold, italic, size)
    return p


def para(doc_or_cell, text, align=JUSTIFY, space_after=8, size=None, link_cites=True):
    p = doc_or_cell.add_paragraph()
    add_runs(p, text, size=size, link_cites=link_cites)
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    return p


BOOKMARK_ID = [1000]


def mark(p, name):
    BOOKMARK_ID[0] += 1
    bookmark(p, name, BOOKMARK_ID[0])


def h(doc, text, level=1, new_page=False):
    if new_page:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    p = doc.add_heading(text, level=level)
    m = re.match(r"Appendix ([A-F]):", text)
    if m:
        mark(p, f"app_{m.group(1)}")
    return p


def caption(container, text, align=WD_ALIGN_PARAGRAPH.CENTER, count=True):
    p = container.add_paragraph(style="Caption")
    add_runs(p, counted(text) if count else text, link_cites=False)
    m = re.match(r"(Figure [DE]?\d+|Table \d+)\.", text)
    if m:
        mark(p, xref_anchor(m.group(1)))
    p.alignment = align
    p.paragraph_format.space_after = Pt(10)
    return p


def picture(container, path, width_cm):
    p = container.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(str(path), width=Cm(width_cm))


def figure(doc, key, width_cm, count=True):
    picture(doc, FPATH[key], width_cm)
    caption(doc, f"Figure {FNUM[key]}. {FCAP[key]}.", count=count)


def no_borders(table):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "nil"); b.append(e)
    tblPr.append(b)


def keep_row(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hex_fill)
    tcPr.append(sh)


def table(doc, key, header, rows, widths, size=9.5, count=False):
    cap = f"Table {TNUM[key]}. {dict(TABLES)[key]}."
    p = caption(doc, cap, count=count)
    p.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=len(header)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, hd in enumerate(header):
        c = t.rows[0].cells[i]; c.text = ""
        r = c.paragraphs[0].add_run(hd); r.bold = True; r.font.size = Pt(size)
        shade(c, "E5EDE6")
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            add_runs(cells[i].paragraphs[0], counted(v) if count else v, size=size)
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
        for row in t.rows:
            row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


def bookmark(p, name, bid):
    s = OxmlElement("w:bookmarkStart"); s.set(qn("w:id"), str(bid)); s.set(qn("w:name"), name)
    e = OxmlElement("w:bookmarkEnd"); e.set(qn("w:id"), str(bid))
    p._p.insert(0, s); p._p.append(e)


def page_number_footer(section):
    p = section.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run()
    for tag, val in (("begin", None), ("instr", "PAGE"), ("end", None)):
        if tag == "instr":
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = val
        else:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag)
        r._r.append(el)
    r.font.size = Pt(9)


def setup_styles(doc):
    st = doc.styles
    normal = st["Normal"]
    normal.font.name = "Arial"; normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    normal.paragraph_format.line_spacing = 1.15
    for name, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5)):
        s = st[name]
        s.font.name = "Arial"; s.font.size = Pt(size); s.font.bold = True; s.font.color.rgb = ACCENT
        rf = s.element.rPr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); s.element.rPr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rf.set(qn(a), "Arial")
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        s.paragraph_format.space_before = Pt(14 if name == "Heading 1" else 10)
        s.paragraph_format.space_after = Pt(6)
        s.paragraph_format.keep_with_next = True
    cap = st["Caption"]
    cap.font.name = "Arial"; cap.font.size = Pt(9); cap.font.italic = False; cap.font.bold = False
    cap.font.color.rgb = RGBColor(0x40, 0x48, 0x42)


# =====================================================================
# Front-matter lists
# =====================================================================
TOC_ENTRIES = [
    ("List of figures and tables", 1),
    ("1 Introduction", 1), ("2 Annotated bibliography", 1), ("3 Product design", 1),
    ("3.1 Conceptual design", 2), ("3.2 Design process", 2), ("3.3 Design principles", 2),
    ("4 Mid-fidelity prototype", 1), ("4.1 Overview", 2), ("4.2 Screens", 2), ("4.3 Purpose and fidelity", 2),
    ("5 Proposed empirical research study", 1), ("6 Conclusion and reflection", 1), ("References", 1),
    ("Appendix A: Literature search strategy", 1), ("Appendix B: Study materials", 1),
    ("Appendix C: Declaration of AI use", 1), ("Appendix D: Hand-drawn sketches", 1),
    ("Appendix E: Prototype screenshots", 1), ("Appendix F: Figma interaction map", 1),
]
LOF = [f"Figure {FNUM[k]}. {c}" for k, _, c in FIGURES] + [f"Figure {n}. {c}" for _, _, n, c in APPENDIX_FIGURES]
LOT = [f"Table {TNUM[k]}. {c}" for k, c in TABLES]


def toc_line(doc, text, page, indent=0.0, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16.4), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f"{text}\t{page}"); r.bold = bold


# =====================================================================
# Build
# =====================================================================

def build(pages):
    COUNTED.clear()
    doc = Document()
    setup_styles(doc)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin = sec.bottom_margin = Cm(2.2)

    # ---- Title page
    for _ in range(5):
        doc.add_paragraph()
    para(doc, "COMP1649 Human–Computer Interaction and Design", align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("NeuroPulse HE"); r.bold = True; r.font.size = Pt(30); r.font.color.rgb = ACCENT
    para(doc, "A mobile companion for neurodiverse learners in higher education", align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    para(doc, "Coursework report, Option A", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=60)
    for label, key in (("Student", "name"), ("Student ID", "id"), ("Tutor", "tutor"), ("Date", "date")):
        para(doc, f"**{label}:** {STUDENT[key]}", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "University of Greenwich, School of Computing and Mathematical Sciences", align=WD_ALIGN_PARAGRAPH.CENTER, size=10, space_after=4)
    para(doc, "Word count (Introduction to Conclusion): {WORDS}", align=WD_ALIGN_PARAGRAPH.CENTER, size=10)

    # ---- Contents
    h(doc, "Contents", 1, new_page=True)
    for title, level in TOC_ENTRIES:
        toc_line(doc, title, pages.get(title, ""), indent=0.6 if level == 2 else 0, bold=level == 1)

    h(doc, "List of figures and tables", 1, new_page=True)
    for line in LOF:
        toc_line(doc, line, pages.get(line.split(".")[0] + ".", ""))
    doc.add_paragraph()
    for line in LOT:
        toc_line(doc, line, pages.get(line.split(".")[0] + ".", ""))

    # ---- 1 Introduction
    h(doc, "1 Introduction", 1, new_page=True)
    for t in INTRO:
        para(doc, counted(t))

    # ---- 2 Annotated bibliography
    h(doc, "2 Annotated bibliography", 1)
    para(doc, counted(BIB_INTRO))
    for t in BIB:
        para(doc, counted(t))

    # ---- 3 Product design
    h(doc, "3 Product design", 1)
    h(doc, "3.1 Conceptual design", 2)
    h(doc, "3.1.1 Users and context", 3)
    para(doc, counted(USERS))
    h(doc, "3.1.2 Concept, tasks and interaction", 3)
    for t in CONCEPT:
        para(doc, counted(t))
    h(doc, "3.1.3 Requirements", 3)
    para(doc, counted(REQ_INTRO))
    table(doc, "req", ["Requirement", "Design response", "Screens", "Source"], REQS, [3.4, 6.6, 2.4, 4.0], count=True)
    h(doc, "3.1.4 Design assumptions", 3)
    para(doc, counted(ASSUMPTIONS))

    h(doc, "3.2 Design process", 2)
    para(doc, counted(PROCESS_INTRO))
    figure(doc, "idea_flow", 15.5)
    para(doc, counted(IDEA))
    para(doc, counted(SKETCHING))
    figure(doc, "focus_v1", 7.0)
    para(doc, counted(PROCESS["focus_v1"]))
    figure(doc, "settings_v1", 10.0)
    para(doc, counted(PROCESS["settings_v1"]))
    para(doc, counted(STORY))
    figure(doc, "storyboard", 16.0)
    para(doc, counted(CARDS))
    figure(doc, "cards", 15.0)

    h(doc, "3.3 Design principles", 2)
    para(doc, counted(NORMAN_INTRO))
    for i, (key, name, text) in enumerate(NORMAN, 1):
        h(doc, f"3.3.{i} {name}", 3)
        para(doc, counted(text))
        figure(doc, key, 4.0)

    # ---- 4 Prototype
    h(doc, "4 Mid-fidelity prototype", 1)
    h(doc, "4.1 Overview", 2)
    para(doc, counted(PROTO_INTRO))
    h(doc, "4.2 Screens", 2)
    for key, texts in FLOW_TEXT.items():
        figure(doc, key, 16.0 if key == "flow_planning" else 13.0 if key == "flow_overload" else 9.8)
        for t in texts:
            para(doc, counted(t))
    h(doc, "4.3 Purpose and fidelity", 2)
    para(doc, counted(PURPOSE))
    figure(doc, "control", 4.4)

    # ---- 5 Study
    h(doc, "5 Proposed empirical research study", 1)
    para(doc, counted(STUDY_INTRO))
    for title, body in STUDY:
        h(doc, title, 3)
        para(doc, counted(body))

    # ---- 6 Conclusion
    h(doc, "6 Conclusion and reflection", 1)
    for t in CONCLUSION:
        para(doc, counted(t))

    # ---- References
    h(doc, "References", 1, new_page=True)
    for i, (bm, text, url) in enumerate(REFERENCES):
        p = doc.add_paragraph()
        add_runs(p, text + (" Available at: " if url else ""), link_cites=False)
        if url:
            hyperlink(p, url, url=url)
            p.add_run(".")
        p.paragraph_format.left_indent = Cm(1); p.paragraph_format.first_line_indent = Cm(-1)
        p.paragraph_format.space_after = Pt(6)
        bookmark(p, bm, 100 + i)

    # ---- Appendices
    h(doc, "Appendix A: Literature search strategy", 1, new_page=True)
    para(doc, "The ACM Digital Library, Scopus, PubMed and Google Scholar were searched in October 2026. Further sources were found by checking the reference lists of, and later citations to, the two reviews (Clouder et al., 2020; McDowall and Kiseleva, 2024).")
    para(doc, "Sources were included if they were peer-reviewed journal articles, conference papers or academic books in English that dealt with neurodivergent adults or students, or with HCI design and evaluation methods relevant to them. Blogs, product websites, opinion pieces and studies of children only were excluded, unless the design finding applied to adults, as with typography. Every reference was checked against its publisher record through Crossref before it was included.")
    table(doc, "search", ["Search string (title, abstract, keywords)", "Database", "Sources retained"], SEARCH, [7.4, 3.6, 5.4], size=9)

    h(doc, "Appendix B: Study materials", 1, new_page=True)
    h(doc, "B1 Participant information sheet", 2)
    for t in [
        "**Study title:** Evaluating NeuroPulse HE, a study companion for neurodivergent students.",
        "**What is the study about?** We are testing a prototype phone app that helps students start and finish study tasks. We want to find out whether it is easy to use and whether it helps people start work.",
        "**What will I do?** In one 45-minute session you will try three short tasks on a phone prototype while saying what you are thinking, fill in two short questionnaires and answer a few questions. The screen and your voice will be recorded. You can take a break at any time.",
        "**Do I have to take part?** No. You can stop at any point without giving a reason, and you can withdraw your data up to two weeks after the session. You do not need a diagnosis to take part.",
        "**What happens to my data?** Recordings are stored on university systems under a participant number and deleted at the end of the project. Quotes in reports will not identify you.",
        "**Contact:** [Researcher name and university email]; supervisor: [Supervisor name and email].",
    ]:
        para(doc, t, space_after=4)
    h(doc, "B2 Consent form", 2)
    t = doc.add_table(rows=1, cols=2); t.style = "Table Grid"; t.autofit = False
    for i, hd in enumerate(["Statement", "Initial"]):
        c = t.rows[0].cells[i]; c.text = ""; rr = c.paragraphs[0].add_run(hd); rr.bold = True; rr.font.size = Pt(9.5); shade(c, "E5EDE6")
    for s in ["I have read the information sheet and had the chance to ask questions.",
              "I understand that taking part is voluntary and that I can stop at any time without giving a reason.",
              "I agree to the session being screen- and audio-recorded.",
              "I understand that I can withdraw my data up to two weeks after the session.",
              "I agree that anonymised quotes may be used in reports.", "I agree to take part in this study."]:
        cells = t.add_row().cells; cells[0].text = ""; plain_run(cells[0].paragraphs[0], s, size=9.5)
    for i, w in enumerate([13.5, 2.9]):
        t.columns[i].width = Cm(w)
        for row in t.rows:
            row.cells[i].width = Cm(w)
    doc.add_paragraph()
    para(doc, "Participant name ______________  Signature ______________  Date ________", align=None)
    para(doc, "Researcher name ______________  Signature ______________  Date ________", align=None)
    h(doc, "B3 Background questionnaire", 2)
    for i, q in enumerate([
        "Participant number: P__   Year of study: ☐1 ☐2 ☐3 ☐4 ☐PG   Subject: __________",
        "How do you describe yourself? (tick any) ☐ADHD ☐Autistic ☐Dyslexic ☐Dyspraxic ☐Other: ______ ☐Prefer not to say",
        "Do you currently use any apps to plan or start study tasks? ☐No ☐Yes, which: __________",
        "How often do you find it hard to start a study task? ☐Never ☐Rarely ☐Sometimes ☐Often ☐Almost always",
        "Do you use any accessibility settings on your phone, such as larger text, dark mode or reduced motion? ☐No ☐Yes, which: ______",
    ], 1):
        para(doc, f"{i}. {q}", space_after=4, align=None)
    h(doc, "B4 Facilitator script and tasks", 2)
    for t_ in [
        "**Welcome (5 min).** \"Thank you for coming. We are testing the app, not you, so there are no wrong answers. Please think aloud as you go. You can take a break or stop at any time.\" Check the consent form and start recording.",
        "**Background (3 min).** The participant completes B3.",
        "**Task 1, conditions A and B in counterbalanced order (5 min each).** \"Imagine it is Friday afternoon and you have coursework due. Using the app, start the next piece of work.\" The task succeeds when the participant taps Start focus (A) or a start control for the correct task (B). Measure the time from the first screen to the first tap on a start control, then repeat with the other condition.",
        "**Task 2 (5 min).** \"You are in a focus session and start to feel overwhelmed. Pause, then find somewhere quieter in the app.\" The task succeeds when the participant reaches the Calm screen.",
        "**Task 3 (5 min).** \"Make the text easier for you to read and the screen darker.\" The task succeeds when the participant reaches the applied Settings state.",
        "**Questionnaires (5 min).** The SUS (B5) for the app as a whole, then: \"Which home screen would you rather use, the first or the second? Why?\"",
        "**Interview (10 min).** B6. **Debrief (2 min).** B7. Stop recording.",
        "**Facilitator rules.** Do not help unless the participant has been stuck for two minutes; then give one hint and record it as an assist. Offer a break between tasks.",
    ]:
        para(doc, t_, space_after=4)
    h(doc, "B5 System Usability Scale (Brooke, 1996)", 2)
    para(doc, "Ratings run from 1 (strongly disagree) to 5 (strongly agree). Odd items score the rating minus 1 and even items score 5 minus the rating; the sum multiplied by 2.5 gives a score from 0 to 100.", space_after=4)
    st = doc.add_table(rows=1, cols=7); st.style = "Table Grid"; st.autofit = False
    for i, hd in enumerate(["#", "Statement", "1", "2", "3", "4", "5"]):
        c = st.rows[0].cells[i]; c.text = ""; rr = c.paragraphs[0].add_run(hd); rr.bold = True; rr.font.size = Pt(9); shade(c, "E5EDE6")
    for i, s in enumerate(SUS_ITEMS, 1):
        cells = st.add_row().cells
        for j, v in enumerate([str(i), s, "☐", "☐", "☐", "☐", "☐"]):
            cells[j].text = ""; plain_run(cells[j].paragraphs[0], v, size=9)
    for i, w in enumerate([0.8, 10.6, 1, 1, 1, 1, 1]):
        st.columns[i].width = Cm(w)
        for row in st.rows:
            row.cells[i].width = Cm(w)
    h(doc, "B6 Semi-structured interview schedule", 2)
    for i, q in enumerate([
        "Tell me about the moment you had to start the work in each version. What did you notice?",
        "Was anything missing from the first home screen that you needed?",
        "How did the rest screen after the focus session feel to you?",
        "When you went to Calm, was it clear what would happen? Would you use it?",
        "Were the settings you changed the ones you would actually use? Did you want to change text size or spacing?",
        "Was 15 minutes a good length for a step? What length would suit you?",
        "Did the breathing guide on the Calm screen help, or would you prefer something else?",
        "Was the 'How full is your head?' question useful, annoying or neither?",
        "Were the colours comfortable to look at? Would you change them?",
        "Did anything in the app feel like pressure, or is there anything you would turn off?",
        "If you could change one thing, what would it be?",
    ], 1):
        para(doc, f"{i}. {q}", space_after=3, align=None)
    h(doc, "B7 Debrief", 2)
    para(doc, "\"Thank you. The study compares two home screens to see whether showing one task at a time helps people start. If anything today was uncomfortable, the university wellbeing service and the Disability and Dyslexia Service can help: [contact details]. You can withdraw your data within two weeks by emailing the researcher with your participant number.\"")
    h(doc, "B8 Data recording sheet", 2)
    rs = doc.add_table(rows=1, cols=9); rs.style = "Table Grid"
    for i, hd in enumerate(["P#", "Order", "Task 1 time A (s)", "Task 1 time B (s)", "Task 2 success", "Task 3 success", "Assists", "SUS", "Prefers"]):
        c = rs.rows[0].cells[i]; c.text = ""; rr = c.paragraphs[0].add_run(hd); rr.bold = True; rr.font.size = Pt(8.5); shade(c, "E5EDE6")
    for row in (["P01", "AB"], ["P02", "BA"], ["…", ""]):
        cells = rs.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = ""; plain_run(cells[j].paragraphs[0], v, size=8.5)

    h(doc, "Appendix C: Declaration of AI use", 1, new_page=True)
    p = doc.add_paragraph()
    plain_run(p, "Complete the University of Greenwich declaration of AI use form (")
    hyperlink(p, "https://www.gre.ac.uk/docs/rep/sas/declaration-of-ai-use", url="https://www.gre.ac.uk/docs/rep/sas/declaration-of-ai-use")
    plain_run(p, ") and insert it here. State which tools were used and for which tasks, and confirm that the design decisions, analysis and reflection are your own.")
    para(doc, "Tool(s) used: ______________________   Purpose: ______________________", align=None)
    para(doc, "Signature: ______________________   Date: __________", align=None)

    h(doc, "Appendix D: Hand-drawn sketches", 1, new_page=True)
    para(doc, "These are the final paper sketches of the eight main screens, drawn before the digital screens were built. Notes in red record design decisions.")
    for key in ["sk_today", "sk_plan", "sk_step", "sk_focus", "sk_rest", "sk_calm", "sk_settings", "sk_progress"]:
        figure(doc, key, 9.6, count=False)

    h(doc, "Appendix E: Prototype screenshots", 1, new_page=True)
    para(doc, "Full-size screenshots of the eight main screens, the three extra states and the control screen used in the study, as imported into Figma Design at 430 by 932 pixels.")
    e_keys = [k for k, _, n, _ in APPENDIX_FIGURES if n.startswith("E")]
    for i, key in enumerate(e_keys):
        if i:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        figure(doc, key, 8.6, count=False)

    h(doc, "Appendix F: Figma interaction map", 1, new_page=True)
    para(doc, "Each frame is one imported screen. All links use On tap and Navigate to, with Smart animate at 200 ms and ease out. The link to the applied Settings state uses an Instant transition because reduced motion is switched on in that state.")
    table(doc, "map", ["From frame", "Element", "To frame"], FIGMA_LINKS, [4.6, 7.0, 4.8], size=9)

    page_number_footer(doc.sections[0])
    words = word_count()
    for p in doc.paragraphs:
        if "{WORDS}" in p.text:
            for r in p.runs:
                r.text = r.text.replace("{WORDS}", f"{words:,}")
    doc.save(OUT)


# =====================================================================
# Page finding and checks
# =====================================================================

def find_pages():
    from pypdf import PdfReader
    tmp = Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(OUT)], check=True, capture_output=True)
    pages = [pg.extract_text() or "" for pg in PdfReader(tmp / (OUT.stem + ".pdf")).pages]
    found = {}
    keys = [t for t, _ in TOC_ENTRIES] + [l.split(".")[0] + "." for l in LOF + LOT]
    for key in keys:
        start = 4 if key.startswith(("Figure", "Table")) else 3
        for n, text in enumerate(pages[start - 1:], start=start):
            lines = [ln.strip() for ln in text.splitlines()]
            if any(ln == key or (key.endswith(".") and ln.startswith(key + " ")) for ln in lines):
                found[key] = n
                break
    return found


def word_count():
    return sum(len(re.sub(r"\*", "", t).split()) for t in COUNTED)


def check_citations():
    body = " ".join(COUNTED)
    used = {CITES[int(m.lastgroup[1:])][2] for m in CITE_RE.finditer(body)}
    listed = {bm for bm, _, _ in REFERENCES}
    return sorted(listed - used), sorted(used - listed)


if __name__ == "__main__":
    build({})
    pages = find_pages()
    build(pages)
    again = find_pages()
    if again != pages:
        build(again)
        pages = again
    keys = [t for t, _ in TOC_ENTRIES] + [l.split(".")[0] + "." for l in LOF + LOT]
    print("pages not found:", [k for k in keys if k not in pages] or "none")
    unused, unlisted = check_citations()
    print(f"saved {OUT}")
    print(f"word count (Introduction to Conclusion, incl. tables and captions): {word_count()}")
    print("references never cited in text:", unused or "none")
    print("cited but not in reference list:", unlisted or "none")
