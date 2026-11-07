"""Build the animated terminal-style profile banner (dark.svg).

Layout follows the reference design in banner.jpg. The portrait is
re-sampled from portrait-source.png (Pedro's dot-matrix portrait) into
native SVG dots, so it renders crisply on GitHub at any size.
"""
from PIL import Image, ImageFilter
import numpy as np

W, H = 1180, 610
BG = "#060B19"
FRAME = "#2BB6E0"
CYAN = "#5EE6F5"
LABEL = "#7CC8F2"
VALUE = "#E6EAF5"
MUTED = "#6B86B8"
PURPLE = "#A78BFA"
GREEN = "#22C55E"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ---------- portrait as native dots ----------
PX, PY, PW, PH = 40, 95, 392, 410  # portrait area inside VISUAL.MAP
STEP = 4.2


def portrait():
    src = Image.open("portrait-source.png").convert("RGB").resize((PW, PH))
    src = src.filter(ImageFilter.GaussianBlur(1.4))
    a = np.asarray(src).astype(float)
    groups = {}
    ny, nx = int(PH / STEP), int(PW / STEP)
    for j in range(ny):
        for i in range(nx):
            cx, cy = (i + .5) * STEP, (j + .5) * STEP
            r, g, b = a[min(PH - 1, int(cy)), min(PW - 1, int(cx))]
            lum = (.3 * r + .55 * g + .15 * b) / 255
            if lum < .05:
                size, col = .9, (40, 52, 90)  # faint background grid
            else:
                size = round(min(3.6, .9 + lum * 3.6) * 2) / 2
                if lum > .3 and g > r * 1.25 and b > r:  # cyan rim light in the source
                    col = (70, 220, 240)
                else:  # lavender ramp: deep violet -> soft white-lilac
                    t = min(1.0, lum * 1.25)
                    lo, hi = (92, 72, 200), (236, 232, 255)
                    col = tuple(int(lo[n] + (hi[n] - lo[n]) * t) // 12 * 12 for n in range(3))
            key = (size, "#%02X%02X%02X" % tuple(min(255, v) for v in col))
            groups.setdefault(key, []).append(f"M{PX + cx:.1f} {PY + cy:.1f}h0")
    out = []
    for (size, col), d in sorted(groups.items()):
        out.append(f'<path d="{"".join(d)}" stroke="{col}" stroke-width="{size}" stroke-linecap="round"/>')
    return "\n".join(out)


def leaders(x1, x2, y):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="1.6 6" stroke-linecap="round" opacity=".7"/>'


def row(label, value, y, lx=470, vx=734, extra=""):
    w = len(label) * 8.6
    return (f'<text x="{lx}" y="{y}" fill="{LABEL}">{label}</text>'
            + leaders(lx + w + 10, vx - 14, y - 4)
            + f'<text x="{vx}" y="{y}" fill="{VALUE}">{value}</text>' + extra)


def section(title, tagline, y, x1=467, x2=1147):
    return (f'<text x="{x1}" y="{y}" fill="{CYAN}" font-size="17" font-weight="700">{title}</text>'
            f'<text x="{x1 + len(title) * 10.6 + 20}" y="{y}" fill="{MUTED}" font-size="14">//</text>'
            f'<text x="{x2}" y="{y}" fill="{LABEL}" font-size="12" text-anchor="end" letter-spacing="1.5">{tagline}</text>'
            f'<line x1="{x1}" y1="{y + 12}" x2="{x2}" y2="{y + 12}" stroke="{FRAME}" opacity=".55"/>')


def card(x, w, icon, title, l1, l2):
    return (f'<rect x="{x}" y="450" width="{w}" height="90" rx="6" fill="#0A1328" stroke="{FRAME}" opacity=".9"/>'
            f'<g transform="translate({x + 18},472)" fill="none" stroke="{PURPLE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
            f'<text x="{x + 62}" y="482" fill="{VALUE}" font-size="14" font-weight="700">{title}</text>'
            f'<text x="{x + 62}" y="504" fill="{MUTED}" font-size="10.5">{l1}</text>'
            f'<text x="{x + 62}" y="520" fill="{MUTED}" font-size="10.5">{l2}</text>')


ICON_S = '<path d="M30 4 L8 16 L30 26 L8 38" /><path d="M14 4 L30 4" opacity=".0"/>'
ICON_EYE = '<path d="M2 20 Q20 2 38 20 Q20 38 2 20Z"/><circle cx="20" cy="20" r="6"/>'
ICON_BARS = '<path d="M6 38V26M18 38V16M30 38V6M2 40H36"/>'

steps = ["PLAN", "DEVELOP", "TEST", "DEPLOY"]
steps_svg = "".join(
    f'<circle cx="1033" cy="{295 + n * 24 - 4}" r="5.5" fill="none" stroke="{LABEL}" stroke-width="1.5"/>'
    f'<text x="1055" y="{295 + n * 24}" fill="{LABEL}" font-size="13">{s}</text>' for n, s in enumerate(steps))
steps_svg += (f'<circle cx="1033" cy="387" r="6" fill="{GREEN}"><animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/></circle>'
              f'<text x="1044" y="391" fill="{GREEN}" font-size="13">✓SOLVE</text>')

flag = ('<g transform="translate(882,146)"><rect width="7" height="13" fill="#169B62"/>'
        '<rect x="7" width="7" height="13" fill="#FFFFFF"/><rect x="14" width="7" height="13" fill="#FF883E"/></g>')

corners = "".join(
    f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="3"/>' for d in [
        "M40 100V85H55", "M432 100V85H417", "M40 497V512H55", "M432 497V512H417"])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".85" stop-color="{CYAN}" stop-opacity=".18"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".55"/></linearGradient>
  <clipPath id="pc"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}"/></clipPath>
  <filter id="glow" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="11" y="11" width="{W - 22}" height="{H - 22}" rx="14" fill="none" stroke="{FRAME}" stroke-width="1.6"/>
<g font-family="{FONT}" font-size="14">
<!-- title bar -->
<circle cx="35" cy="34" r="6.5" fill="#FF5F57"/><circle cx="60" cy="34" r="6.5" fill="#FEBC2E"/><circle cx="85" cy="34" r="6.5" fill="#28C840"/>
<text x="125" y="39" fill="{CYAN}" font-size="17">profile.sh --live</text>
<text x="886" y="39" fill="#FF6B4A" font-size="17">[</text><circle cx="909" cy="33" r="5.5" fill="#FF4D3A"><animate attributeName="opacity" values="1;.25;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="924" y="39" fill="#FF6B4A" font-size="17" font-weight="700">LIVE</text><text x="972" y="39" fill="#FF6B4A" font-size="17">]</text>
<rect x="1003" y="19" width="152" height="30" rx="6" fill="#0A1A2E" stroke="{CYAN}" stroke-width="1.6"/>
<text x="1079" y="39" fill="{CYAN}" font-size="16" font-weight="700" text-anchor="middle">@P2025edro</text>
<line x1="11" y1="57" x2="{W - 11}" y2="57" stroke="{FRAME}" opacity=".6"/>

<!-- VISUAL.MAP -->
<rect x="30" y="68" width="413" height="478" rx="4" fill="#050916" stroke="{FRAME}" stroke-width="1.3"/>
<g clip-path="url(#pc)" filter="url(#glow)">{portrait()}</g>
<g clip-path="url(#pc)"><rect x="{PX}" y="{PY - 60}" width="{PW}" height="60" fill="url(#scan)"><animate attributeName="y" values="{PY - 60};{PY + PH}" dur="5s" repeatCount="indefinite"/></rect></g>
<rect x="{PX}" y="{PY - 14}" width="{PW}" height="18" fill="#050916"/>
<text x="55" y="90" fill="{CYAN}" font-size="14" font-weight="700">VISUAL.MAP</text>
<line x1="160" y1="86" x2="415" y2="86" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="1.6 5" stroke-linecap="round"/>
{corners}
<text x="55" y="536" fill="{CYAN}" font-size="13">&gt;</text><text x="72" y="536" fill="{LABEL}" font-size="13">HUMAN.EXE</text><text x="155" y="536" fill="{MUTED}" font-size="13">//</text><text x="182" y="536" fill="{PURPLE}" font-size="13">BUILDING A BETTER TOMORROW</text>

<!-- SYSTEM.INFO -->
{section("SYSTEM.INFO", "IDEAS  →  SOLUTIONS  →  REAL IMPACT", 83)}
{row("Subject", "Pedro Silva", 117)}
{row("Role", "Founder / Software Developer", 138)}
{row("Location", "Dublin, Ireland", 159)}{flag}
{row("Education", "BSc Computing", 180)}
{row("Status", "Building · Learning · Shipping", 201)}
{row("Focus", "Software · AI · Security · Efficiency", 222)}

<!-- TECH.STACK -->
{section("TECH.STACK", "TOOLS FOR REAL-WORLD SOLUTIONS", 265)}
{row("Core.Lang", "JavaScript · TypeScript", 299, vx=726)}
{row("Core.Frontend", "React · Vite", 320, vx=726)}
{row("Core.Backend", "Node.js", 341, vx=726)}
{row("Core.Database", "SQLite", 362, vx=726)}
{row("Core.Infra", "GitHub · Vercel", 383, vx=726)}
<line x1="1000" y1="287" x2="1000" y2="396" stroke="{FRAME}" opacity=".5"/>
{steps_svg}

<!-- PROJECTS -->
{section("PROJECTS", "FROM IDEAS TO REAL IMPACT", 430).replace('>//<', '><').replace('text-anchor="end" letter-spacing="1.5">', 'text-anchor="end" letter-spacing="1.5">//   ')}
{card(465, 217, ICON_S, "Silva Solutions Ltd", "Technology for real", "business problems.")}
{card(692, 225, ICON_EYE, "Silvix", "AI CCTV · Fleet · Drone", "Monitoring Platform")}
{card(927, 221, ICON_BARS, "STRAVIQ", "Project Intelligence", "&amp; Execution")}

<!-- footer -->
<line x1="11" y1="555" x2="{W - 11}" y2="555" stroke="{FRAME}" opacity=".6"/>
<text x="30" y="583" fill="{GREEN}" font-size="16" font-weight="700">&gt;</text>
<text x="56" y="583" fill="{VALUE}" font-size="16">const <tspan fill="{LABEL}">future</tspan> = better();</text>
<text x="1110" y="583" fill="{LABEL}" font-size="13" text-anchor="end" letter-spacing="1.5">DISCIPLINE TODAY. BIGGER TOMORROW.</text>
<rect x="1121" y="569" width="9" height="17" fill="{LABEL}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
</g>
</svg>'''

open("dark.svg", "w", encoding="utf-8").write(svg)
print("dark.svg", len(svg) // 1024, "KB")
