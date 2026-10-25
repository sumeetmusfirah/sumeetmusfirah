#!/usr/bin/env python3
"""Generate the profile's SVG visual system (light + dark variants).

Stdlib only. Every asset is a pure function of the tokens below, so the
output is deterministic: edit a token or a layout, re-run, commit the diff.

    python3 assets/build.py

Design rules (see assets/README.md): warm paper ground, charcoal ink,
olive + clay + signature orange accents used sparingly, editorial serif for
words, monospace for labels and numbers, hairline strokes, no gradients.
Numbers in figures must come from a public, cited source.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- tokens ---
PALETTES = {
    "light": {
        "bg": "#FAF9F5",      # warm off-white
        "rule": "#E3E0D6",    # hairline on paper
        "ink": "#141413",     # near-black text
        "muted": "#5E5D59",   # secondary text (6.3:1)
        "sage": "#788C5D",    # olive: strokes, motifs
        "moss": "#556640",    # olive labels (5.9:1)
        "clay": "#B4532F",    # deep clay for text (4.7:1)
        "wine": "#B4532F",    # accent labels share deep clay
        "sig": "#D97757",     # signature orange: dots, pulses, nodes (graphics only)
        "panel": "#F0EEE6",   # box fill
    },
    "dark": {
        "bg": "#1A1915",
        "rule": "#3A3934",
        "ink": "#FAF9F5",
        "muted": "#B0AEA5",
        "sage": "#95A876",
        "moss": "#A9BC8A",
        "clay": "#E08A6D",
        "wine": "#E08A6D",
        "sig": "#D97757",
        "panel": "#24231F",
    },
}

SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def style(p: dict) -> str:
    return f"""<style>
.serif{{font-family:{SERIF}}}
.mono{{font-family:{MONO}}}
.ink{{fill:{p['ink']}}} .muted{{fill:{p['muted']}}} .moss{{fill:{p['moss']}}}
.wine{{fill:{p['wine']}}} .clay{{fill:{p['clay']}}} .sig{{fill:{p['sig']}}}
.hair{{stroke:{p['rule']};stroke-width:1;fill:none}}
.line{{stroke:{p['muted']};stroke-width:0.9;fill:none}}
.motif{{stroke:{p['sage']};stroke-width:1.1;fill:none;stroke-linecap:round}}
.box{{fill:{p['panel']};stroke:{p['rule']};stroke-width:1}}
.label{{font-size:11px;letter-spacing:1.8px}}
@keyframes draw{{from{{stroke-dashoffset:260}}to{{stroke-dashoffset:0}}}}
@keyframes fadein{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes travel{{0%{{offset-distance:0%;opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{offset-distance:100%;opacity:0}}}}
@keyframes glow{{0%,62%,100%{{r:4.2px;opacity:1}}70%{{r:6.5px;opacity:.55}}}}
@keyframes sway{{0%,100%{{transform:rotate(-3deg)}}50%{{transform:rotate(3deg)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.draw{{stroke-dasharray:260;animation:draw 2.4s cubic-bezier(.4,0,.2,1) both}}
.late{{animation:fadein 1.2s ease-out 1.6s both}}
.pulse{{opacity:0;offset-path:path('M900,185 L980,185 L1040,140 L1100,172');animation:travel 3.2s ease-in-out 2.6s infinite}}
.glow{{animation:glow 3.2s ease-in-out 2.6s infinite}}
.sway{{transform-box:fill-box;transform-origin:50% 100%;animation:sway 6s ease-in-out infinite}}
.cursor{{animation:blink 1.1s steps(1) infinite}}
</style>"""


def svg(w: int, h: int, title: str, desc: str, body: str, p: dict) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-labelledby="t d">\n'
        f'<title id="t">{escape(title)}</title>\n<desc id="d">{escape(desc)}</desc>\n'
        f"{style(p)}\n"
        f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,1 L9,5 L0,9" fill="none" stroke="{p["muted"]}" stroke-width="1.3"/>'
        f"</marker></defs>\n"
        f'<rect width="{w}" height="{h}" rx="6" fill="{p["bg"]}"/>\n'
        f"{body}\n</svg>\n"
    )


def text(x, y, s, cls, size=None, anchor="start", extra=""):
    sz = f' font-size="{size}"' if size else ""
    return (f'<text x="{x}" y="{y}" class="{cls}"{sz} text-anchor="{anchor}"{extra}>'
            f"{escape(s)}</text>")


def box(x, y, w, h, title, lines=(), title_size=17, title_cls="serif ink"):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" class="box"/>',
           text(x + 16, y + 30, title, title_cls, title_size)]
    for i, (s, cls) in enumerate(lines):
        out.append(text(x + 16, y + 54 + i * 19, s, cls, 12))
    return "\n".join(out)


def caption(y, label, lines, p):
    out = [f'<line x1="48" y1="{y - 26}" x2="1152" y2="{y - 26}" class="hair"/>',
           text(48, y, label, "mono wine label")]
    for i, s in enumerate(lines):
        out.append(text(140, y + i * 20, s, "serif muted", 14))
    return "\n".join(out)


# ---------------------------------------------------------------- motifs ---
def neuron_to_graph(ox=0, oy=0):
    """Fine-line dendritic arbor whose axon resolves into an agent graph."""
    dend = [
        "M900,185 C870,170 850,150 820,128", "M820,128 C810,118 800,114 786,112",
        "M820,128 C815,115 816,104 812,94", "M900,185 C868,188 840,196 806,204",
        "M806,204 C795,200 784,201 772,206", "M806,204 C796,214 790,224 786,236",
        "M900,185 C885,160 878,140 874,112", "M874,112 C866,104 860,100 852,98",
        "M874,112 C878,104 882,100 890,96", "M900,185 C890,210 880,232 860,252",
        "M860,252 C850,256 842,256 830,254", "M905,185 L974,185",
    ]
    nodes = {"A": (980, 185), "B": (1040, 140), "C": (1050, 226), "D": (1100, 172),
             "E": (1122, 242), "F": (1112, 112)}
    edges = ["AB", "AC", "BD", "CD", "BF", "DE", "CE", "DF"]
    g = [f'<g transform="translate({ox},{oy})">']
    g += [f'<path d="{d}" class="motif draw" style="animation-delay:{i * 0.08:.2f}s"/>'
          for i, d in enumerate(dend)]
    g.append('<circle cx="900" cy="185" r="5" class="motif"/>')
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="motif late" stroke-opacity="0.75"/>')
    for k, (x, y) in nodes.items():
        cls = "sig glow" if k == "D" else "motif late"
        fill = "" if k == "D" else ' style="fill:var(--bg)"'
        g.append(f'<circle cx="{x}" cy="{y}" r="4.2" class="{cls}"{fill}/>')
    g.append('<circle r="2.6" class="sig pulse"/>')  # signal travelling soma -> graph
    g.append("</g>")
    return "\n".join(g)


def static_motif():
    """Motif with animation hooks removed (for raster exports like the avatar)."""
    m = neuron_to_graph()
    for cls in (" draw", " late", " glow"):
        m = m.replace(cls, "")
    return "\n".join(l for l in m.splitlines() if "pulse" not in l)


def sprig(cx, cy):
    """Very small fine-line botanical sprig (used once, in the footer)."""
    leaves = []
    for i, dy in enumerate((-10, -2, 6)):
        s = 1 - i * 0.18
        leaves.append(f'<path d="M{cx},{cy + dy} q{-9 * s},{-7 * s} {-17 * s},{-4 * s} '
                      f'q{7 * s},{6 * s} {17 * s},{4 * s}" class="motif"/>')
        leaves.append(f'<path d="M{cx},{cy + dy - 3} q{9 * s},{-7 * s} {17 * s},{-4 * s} '
                      f'q{-7 * s},{6 * s} {-17 * s},{4 * s}" class="motif"/>')
    stem = f'<path d="M{cx},{cy + 14} C{cx + 1},{cy} {cx - 1},{cy - 10} {cx},{cy - 20}" class="motif"/>'
    return stem + "\n" + "\n".join(leaves)


# ---------------------------------------------------------------- assets ---
def header(p):
    body = "\n".join([
        text(56, 64, "RESEARCH NOTEBOOK  ·  AI × COGNITION × NEURO", "mono muted label"),
        f'<rect x="436" y="54" width="7" height="12" class="sig cursor"/>',
        f'<line x1="56" y1="84" x2="1144" y2="84" stroke="{p["ink"]}" stroke-width="0.8"/>',
        text(56, 162, "Sumeet Musfirah", "serif ink", 58, extra=' letter-spacing="0.4"'),
        text(56, 206, "Studying intelligence across biological and artificial systems.",
             "serif muted", 23, extra=' font-style="italic"'),
        text(56, 246, "AI SAFETY · MODEL BEHAVIOR · LLM EVALUATION · SOCIAL INFLUENCE",
             "mono moss label"),
        text(56, 266, "BELIEF UPDATING · NEUROAI · COGNITIVE SCIENCE · MULTIMODAL AI",
             "mono moss label"),
        neuron_to_graph(0, 4),
        text(1144, 280, "fig. 0 — dendritic arbor → agent graph", "mono muted", 10, "end"),
        f'<line x1="56" y1="294" x2="1144" y2="294" stroke="{p["ink"]}" stroke-width="0.8"/>',
    ])
    return svg(1200, 320, "Sumeet Musfirah — Studying intelligence across biological and artificial systems",
               "Masthead with name, tagline, research areas, and a fine-line drawing of a neuron "
               "whose axon becomes a small network graph.", body, p)


def footer(p):
    body = "\n".join([
        f'<line x1="380" y1="40" x2="570" y2="40" class="hair"/>',
        '<g class="sway">', sprig(600, 40), "</g>",
        f'<line x1="630" y1="40" x2="820" y2="40" class="hair"/>',
        text(600, 92, "AI × Cognition × Neuro", "serif muted", 19, "middle",
             ' font-style="italic" letter-spacing="0.5"'),
    ])
    return svg(1200, 116, "AI × Cognition × Neuro", "Footer rule with a small botanical sprig.", body, p)


def research_map(p):
    L, C, R = 48, 400, 872  # column x
    out = [
        text(L, 56, "BIOLOGICAL & HUMAN SYSTEMS", "mono moss label"),
        text(C + 200, 56, "SHARED QUESTIONS", "mono wine label", anchor="middle"),
        text(1152, 56, "ARTIFICIAL SYSTEMS", "mono clay label", anchor="end"),
    ]
    left = [("Cognitive control", "EEG · neuromodulation · ML"),
            ("Social cognition", "theory of mind · persuasion · trust"),
            ("Neuroethics", "neurorights · cognitive sovereignty")]
    right = [("Interacting LLMs", "source attribution · cascades"),
             ("Model behavior", "persuasion · pressure · drift"),
             ("Evaluation", "LLM-as-judge · clinical AI")]
    qs = ["When should an agent update on another's claim?",
          "Can confidence spread independently of evidence?",
          "What does social pressure do to model behavior?",
          "Do our evaluations measure what we think they do?"]
    ys = [84, 176, 268]
    for (t, s), y in zip(left, ys):
        out.append(box(L, y, 280, 72, t, [(s, "mono muted")]))
        out.append(f'<path d="M{L + 280},{y + 36} H{L + 316}" class="line"/>')
    for (t, s), y in zip(right, ys):
        out.append(box(R, y, 280, 72, t, [(s, "mono muted")]))
        out.append(f'<path d="M{R},{y + 36} H{R - 36}" class="line"/>')
    # buses
    out.append(f'<path d="M{L + 316},{ys[0] + 36} V{ys[-1] + 36}" class="line"/>')
    out.append(f'<path d="M{R - 36},{ys[0] + 36} V{ys[-1] + 36}" class="line"/>')
    qy = [96, 160, 224, 288]
    for q, y in zip(qs, qy):
        out.append(f'<rect x="{C}" y="{y}" width="400" height="44" rx="22" class="box"/>')
        out.append(text(C + 200, y + 28, q, "serif ink", 15.5, "middle", ' font-style="italic"'))
        out.append(f'<path d="M{L + 316},{y + 22} H{C}" class="line" marker-end="url(#arr)"/>')
        out.append(f'<path d="M{R - 36},{y + 22} H{C + 400}" class="line" marker-end="url(#arr)"/>')
    # project axis
    ay = 430
    out += [
        text(L, ay - 46, "WHERE EACH PROJECT SITS", "mono muted label"),
        f'<line x1="{L}" y1="{ay}" x2="1152" y2="{ay}" stroke="{p["ink"]}" stroke-width="0.8"/>',
        text(L, ay + 44, "biological", "mono moss", 11),
        text(1152, ay + 44, "artificial", "mono clay", 11, "end"),
    ]
    projects = [(190, "CogNeW · EEG & neuromodulation", -1), (380, "Neurorights poster", 1),
                (640, "Aletheia · Exp 001", -1), (820, "Persuasion Topography", 1),
                (960, "Pressure evals v0.1", -1), (1100, "ABIM · clinical AI eval", 1)]
    for x, name, side in projects:
        ty = ay - 14 if side < 0 else ay + 24
        anchor = "end" if x > 1050 else "middle"
        out.append(f'<circle cx="{x}" cy="{ay}" r="4" class="sig"/>')
        out.append(text(x, ty, name, "mono ink", 11.5, anchor))
    out.append(caption(540, "FIGURE 1", [
        "Research program. Questions about belief updating and influence, studied in brains and",
        "people (left) and in interacting artificial agents (right).",
    ], p))
    return svg(1200, 590, "Figure 1: Research program map",
               "Three columns. Biological and human systems: cognitive control, social cognition, "
               "neuroethics. Shared questions: when should an agent update on another's claim; can "
               "confidence spread independently of evidence; what does social pressure do to model "
               "behavior; do our evaluations measure what we think. Artificial systems: interacting "
               "LLMs, model behavior, evaluation. Below, an axis from biological to artificial places "
               "CogNeW EEG work, a neurorights poster, Aletheia Exp 001, Persuasion Topography, "
               "pressure evals v0.1, and ABIM clinical AI evaluation.", "\n".join(out), p)


def exp001(p):
    y, h = 92, 196
    out = [
        box(48, y, 220, h, "Question", [("objective-answer item", "mono muted"),
                                        ("", "mono muted"),
                                        ("fresh baseline answer", "mono muted"),
                                        ("elicited first", "mono muted")]),
        f'<path d="M268,{y + h / 2} H316" class="line" marker-end="url(#arr)"/>',
        box(320, y, 340, h, "Same argument text", [("byte-for-byte constant", "mono muted")]),
        text(336, y + 92, "correct", "mono moss", 12),
        text(400, y + 92, "|", "mono muted", 12),
        text(424, y + 92, "misleading", "mono clay", 12),
        f'<line x1="336" y1="{y + 108}" x2="644" y2="{y + 108}" class="hair"/>',
        text(336, y + 130, "SOURCE LABEL (THE ONLY MANIPULATION)", "mono wine", 10.5,
             extra=' letter-spacing="1.2"'),
        text(336, y + 154, "control · anonymous · expert", "mono ink", 12),
        text(336, y + 174, "other model · consensus", "mono ink", 12),
        f'<path d="M660,{y + h / 2} H708" class="line" marker-end="url(#arr)"/>',
        box(712, y, 196, h, "5 model families", [("qwen · gemma · llama", "mono muted"),
                                                 ("mistral · phi", "mono muted"),
                                                 ("", "mono muted"),
                                                 ("open-weight, local", "mono muted")]),
        f'<path d="M908,{y + h / 2} H948" class="line" marker-end="url(#arr)"/>',
        box(952, y, 200, h, "Deterministic outcomes", [("answer switch", "mono muted"),
                                                       ("appropriate vs.", "mono muted"),
                                                       ("inappropriate update", "mono muted"),
                                                       ("no LLM judge in the", "mono wine"),
                                                       ("primary causal path", "mono wine")],
            title_size=16),
        text(48, 64, "5 SOURCES × 2 CORRECTNESS = 10 CELLS PER ITEM", "mono muted label"),
    ]
    out.append(caption(352, "FIGURE 2", [
        "Aletheia Exp 001 — preregistered design; data collection has not started. Evidence is held",
        "constant; only the attributed source varies, crossed with whether the evidence is correct.",
    ], p))
    return svg(1200, 400, "Figure 2: Aletheia Exp 001 minimal-pair design",
               "A question and fresh baseline answer feed into an identical argument, either correct "
               "or misleading, whose source label is the only manipulation: control, anonymous, "
               "expert, other model, or consensus. Five open-weight model families respond. Outcomes "
               "are deterministic: answer switching and appropriate versus inappropriate updating, "
               "with no LLM judge in the primary causal path. Preregistered; no data collected yet.",
               "\n".join(out), p)


def pressure(p):
    out = [
        text(48, 64, "SAME 180 OUTPUTS · SAME RUBRIC · TWO JUDGES", "mono muted label"),
        box(48, 120, 250, 150, "180 outputs", [("3 models × 4 conditions", "mono muted"),
                                               ("× 15 scenarios", "mono muted"),
                                               ("", "mono muted"),
                                               ("local inference (Ollama)", "mono muted")]),
        f'<path d="M298,195 H346" class="line" marker-end="url(#arr)"/>',
        box(350, 140, 210, 110, "Blinded scoring", [("6 dimensions, 0–2", "mono muted"),
                                                    ("manipulation rubric", "mono muted")]),
        f'<path d="M560,180 C590,180 590,140 616,140" class="line" marker-end="url(#arr)"/>',
        f'<path d="M560,210 C590,210 590,268 616,268" class="line" marker-end="url(#arr)"/>',
        box(620, 88, 280, 104, "Judge A · qwen3:4b", [("no shift detected", "mono ink"),
                                                       ("all primary tests p ≥ 0.63", "mono muted")],
            title_size=16),
        box(620, 210, 280, 116, "Judge B · claude-sonnet-4-6", [("autonomy cue reduces", "mono ink"),
                                                                 ("manipulation-coded language", "mono ink"),
                                                                 ("p = 0.0003 vs. pressure", "mono muted")],
            title_size=16),
        f'<path d="M900,140 C925,140 925,180 948,186" class="line" marker-end="url(#arr)"/>',
        f'<path d="M900,268 C925,268 925,222 948,208" class="line" marker-end="url(#arr)"/>',
        box(952, 140, 200, 110, "Verdict", [("evaluator-sensitive", "mono wine"),
                                            ("report both results", "mono muted")]),
    ]
    out.append(caption(380, "FIGURE 3", [
        "aletheia-pressure-evals v0.1. Identical blinded outputs scored by two judges support opposite",
        "conclusions; agreement is near chance and concentrates in the primary judge's own outputs.",
    ], p))
    return svg(1200, 428, "Figure 3: pressure-evals v0.1 evaluator sensitivity",
               "180 outputs from 3 models, 4 conditions and 15 scenarios are blinded and scored on a "
               "6-dimension manipulation rubric. Judge A, qwen3:4b, finds no shift (all primary tests "
               "p at least 0.63). Judge B, claude-sonnet-4-6, finds the autonomy instruction reduces "
               "manipulation (p = 0.0003 versus pressure). Verdict: evaluator-sensitive; both results "
               "are reported.", "\n".join(out), p)


def avatar(p):
    """Square avatar; key content kept inside the circle GitHub crops to."""
    body = "\n".join([
        f'<circle cx="256" cy="256" r="214" class="hair" stroke-width="1.5"/>',
        f'<g transform="translate(-406,250) scale(0.7)" opacity="0.9">{static_motif()}</g>',
        text(256, 214, "SM", "serif ink", 150, "middle", ' letter-spacing="2"'),
        f'<line x1="186" y1="244" x2="326" y2="244" stroke="{p["sig"]}" stroke-width="1.6"/>',
        text(256, 276, "AI × COGNITION × NEURO", "mono muted", 13, "middle", ' letter-spacing="2.4"'),
    ])
    return svg(512, 512, "SM monogram", "Monogram SM over a fine-line neuron-to-graph motif.",
               body, p).replace('rx="6"', 'rx="0"')


def brand_sheet(p):
    sw = [("bg", "ground"), ("ink", "ink"), ("sage", "olive · motif"), ("moss", "olive · label"),
          ("clay", "clay · text accent"), ("sig", "orange · signal")]
    out = [text(48, 60, "BRAND SHEET", "mono wine label"),
           text(48, 104, "Editorial serif for ideas.", "serif ink", 30),
           text(48, 140, "Monospace for labels, code, and numbers — 0123456789", "mono muted", 15)]
    for i, (k, name) in enumerate(sw):
        x = 48 + i * 184
        out.append(f'<rect x="{x}" y="182" width="164" height="84" rx="4" fill="{p[k]}" '
                   f'stroke="{p["rule"]}"/>')
        out.append(text(x, 292, name, "serif ink", 16))
        out.append(text(x, 312, p[k], "mono muted", 12))
    out.append(caption(372, "TOKENS", ["Light and dark palettes are defined once in assets/build.py;",
                                        "every asset is regenerated from them."], p))
    return svg(1200, 420, "Brand sheet", "Typography and color palette: parchment, charcoal, "
               "olive, clay, signature orange.", "\n".join(out), p)


def ticker(p):
    """Typewriter line cycling through current research threads."""
    phrases = ["epistemic independence in interacting LLMs",
               "confidence contagion & information cascades",
               "persuasion and behavioral drift in LLMs",
               "evaluation of AI in high-stakes settings",
               "human cognition ↔ artificial-agent behavior"]
    n, slot = len(phrases), 3.4
    cycle = n * slot
    vis = 100 / n
    css = [f"@keyframes show{{0%,{vis - 0.1:.2f}%{{opacity:1}}{vis:.2f}%,100%{{opacity:0}}}}",
           ]
    out = [text(48, 52, "> currently investigating:", "mono muted", 15)]
    x0 = 300
    for i, ph in enumerate(phrases):
        w = int(len(ph) * 9.4) + 14
        delay = i * slot - cycle
        css.append(f".ph{i}{{animation:show {cycle}s linear {delay:.1f}s infinite}}"
                   f"@keyframes type{i}{{0%{{transform:translateX(0)}}{vis * 0.45:.2f}%,100%{{transform:translateX({w}px)}}}}"
                   f".cv{i}{{animation:type{i} {cycle}s steps({len(ph)},end) {delay:.1f}s infinite}}")
        out.append(f'<g class="ph ph{i}">'
                   + text(x0, 52, ph, "mono ink", 15)
                   + f'<g class="cover cv{i}"><rect x="{x0 - 2}" y="30" width="{w + 20}" height="32" '
                     f'fill="{p["bg"]}"/><rect x="{x0}" y="38" width="8" height="18" class="sig cursor"/></g>'
                   + "</g>")
    out.insert(0, "<style>" + "".join(css) + "</style>")
    return svg(1200, 84, "Currently investigating",
               "Typewriter line cycling through: " + "; ".join(phrases) + ".", "\n".join(out), p)


def cascade(p):
    """Schematic (not data): confidence propagates along agents; evidence stays flat."""
    k, cyc, step = 8, 12.0, 1.0
    xs = [120 + i * 137 for i in range(k)]
    cy, base = 200, 162
    css = []
    out = [text(48, 56, "SCHEMATIC · NOT DATA", "mono wine label"),
           text(48, 86, "Can confidence travel further than the evidence that justified it?",
                "serif ink", 20, extra=' font-style="italic"')]
    for i, x in enumerate(xs):
        on = (1 + i * step) / cyc * 100
        css.append(f"@keyframes on{i}{{0%,{on:.1f}%{{opacity:0}}{on + 3:.1f}%,92%{{opacity:1}}100%{{opacity:0}}}}"
                   f"@keyframes bar{i}{{0%,{on:.1f}%{{transform:scaleY(0)}}{on + 5:.1f}%,92%"
                   f"{{transform:scaleY({1 - i * 0.04:.2f})}}100%{{transform:scaleY(0)}}}}"
                   f".n{i}{{opacity:{1 if i < 4 else 0};animation:on{i} {cyc}s ease-out infinite}}"
                   f".b{i}{{transform-box:fill-box;transform-origin:50% 100%;"
                   f"transform:scaleY({(1 - i * 0.04) if i < 4 else 0:.2f});animation:bar{i} {cyc}s ease-out infinite}}")
        if i:
            out.append(f'<line x1="{xs[i-1] + 14}" y1="{cy}" x2="{x - 16}" y2="{cy}" class="line" marker-end="url(#arr)"/>')
        out.append(f'<rect x="{x - 5}" y="{base - 50}" width="10" height="50" class="hair"/>')
        out.append(f'<rect x="{x - 5}" y="{base - 50}" width="10" height="50" class="clay b{i}"/>')
        out.append(f'<circle cx="{x}" cy="{cy}" r="12" class="motif" style="fill:{p["panel"]}"/>')
        out.append(f'<circle cx="{x}" cy="{cy}" r="12" class="sig n{i}"/>')
        out.append(text(x, cy + 36, f"agent {i + 1}", "mono muted", 11, "middle"))
    ey = 262
    out += [f'<line x1="{xs[0] - 12}" y1="{ey}" x2="{xs[-1] + 12}" y2="{ey}" stroke="{p["moss"]}" '
            f'stroke-width="1.4" stroke-dasharray="5 5"/>',
            text(xs[0] - 12, ey + 22, "evidence available to each agent: unchanged", "mono moss", 11.5),
            text(xs[-1] + 12, ey + 22, "bars = expressed confidence", "mono clay", 11.5, "end")]
    out.append(caption(342, "SKETCH", [
        "An illustration of the hypothesis Aletheia tests, not a result: each agent sees the previous",
        "agent's answer and confidence, while the evidence itself never changes.",
    ], p))
    out.insert(0, "<style>" + "".join(css) + "</style>")
    return svg(1200, 392, "Sketch: confidence cascade across agents",
               "Schematic, not data. Eight agents in a chain; each turns orange and raises a "
               "confidence bar after the previous one, while a dashed evidence line stays flat. "
               "Illustrates the question of whether confidence can propagate independently of evidence.",
               "\n".join(out), p)


ASSETS = {
    "branding/ticker": ticker,
    "diagrams/confidence-cascade": cascade,
    "branding/avatar": avatar,
    "branding/brand-sheet": brand_sheet,
    "branding/header": header,
    "branding/footer": footer,
    "diagrams/research-map": research_map,
    "research/aletheia-exp001-design": exp001,
    "research/pressure-evals-judges": pressure,
}


def main() -> None:
    for stem, fn in ASSETS.items():
        for theme, pal in PALETTES.items():
            out = fn(pal).replace("var(--bg)", pal["bg"])
            path = ROOT / f"{stem}-{theme}.svg"
            path.write_text(out, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
