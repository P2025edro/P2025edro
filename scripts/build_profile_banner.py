from PIL import Image, ImageEnhance
import numpy as np, os

SRC="portrait-dither.png"
im=Image.open(SRC).convert("L")
# portrait-dither.png is already the user's real portrait. Re-sample into a dense native SVG dot map.
im=ImageEnhance.Contrast(im).enhance(1.25)
g=np.asarray(im.resize((100,118),Image.Resampling.LANCZOS))
strength=(255-g)/255.0

def paths(color):
    bins=[[],[],[],[]]
    for j in range(118):
        for i in range(100):
            s=float(strength[j,i])
            if s<.12: continue
            k=min(3,int(s*4))
            x=58+i*3.42; y=112+j*3.35
            z=(.65,.9,1.15,1.45)[k]
            bins[k].append(f"M{x:.1f},{y:.1f}h{z}v{z}h-{z}z")
    op=(.22,.40,.66,.96)
    return "\n".join(f'<path d="{"".join(v)}" fill="{color}" opacity="{op[k]}"/>' for k,v in enumerate(bins) if v)

def make(dark=True):
    bg="#0A101F" if dark else "#F8FAFC"; panel="#070B16" if dark else "#FFFFFF"
    purple="#A78BFA" if dark else "#7C3AED"; cyan="#22D3EE" if dark else "#0891B2"
    main="#E5E7EB" if dark else "#111827"; muted="#64748B" if dark else "#475569"
    p=paths(purple)
    travelers=[]
    for n in range(180):
        x=60+(n*37)%340; y=120+(n*61)%390; x2=60+(n*53)%340
        travelers.append(f'<circle cx="{x}" cy="{y}" r=".7"><animate attributeName="cx" values="{x};{x2};{x}" dur="{6+(n%9)*.7:.1f}s" begin="{(n%32)*.1:.1f}s" repeatCount="indefinite"/></circle>')
    tr="".join(travelers)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs><clipPath id="pc"><rect x="46" y="104" width="378" height="418" rx="7"/></clipPath></defs>
<rect width="1180" height="610" fill="{bg}"/><rect x="14" y="14" width="1152" height="582" rx="12" fill="none" stroke="{cyan}" opacity=".35"/>
<g font-family="monospace"><text x="38" y="49" fill="{cyan}" font-size="19">profile.sh --live</text><circle cx="1015" cy="42" r="6" fill="#10B981"><animate attributeName="opacity" values="1;.3;1" dur="1.8s" repeatCount="indefinite"/></circle><text x="1034" y="49" fill="{cyan}" font-size="15">@P2025edro</text><text x="45" y="91" fill="{purple}" font-size="16">VISUAL.MAP</text></g>
<rect x="45" y="103" width="380" height="420" rx="8" fill="{panel}" stroke="{purple}"/>
<g clip-path="url(#pc)"><g>{p}<animate attributeName="opacity" values="0;.12;.45;1;1" keyTimes="0;.08;.16;.225;1" dur="14.2s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 2;1 -1;-1 1;0 2" dur="14.2s" repeatCount="indefinite"/></g><g fill="{cyan}" opacity=".42">{tr}</g></g>
<text x="55" y="550" fill="{purple}" font-family="monospace" font-size="12">&gt; HUMAN.EXE // BUILDING A BETTER TOMORROW</text><line x1="462" y1="78" x2="462" y2="535" stroke="{cyan}" opacity=".25"/>
<g font-family="monospace"><text x="500" y="95" fill="{cyan}" font-size="17">SYSTEM.INFO</text>
<text x="500" y="137" fill="{muted}" font-size="12">SUBJECT</text><text x="680" y="137" fill="{main}" font-size="15">Pedro Silva</text>
<text x="500" y="174" fill="{muted}" font-size="12">ROLE</text><text x="680" y="174" fill="{main}" font-size="15">Founder · Software Developer</text>
<text x="500" y="211" fill="{muted}" font-size="12">ORIGIN</text><text x="680" y="211" fill="{main}" font-size="15">Dublin, Ireland</text>
<text x="500" y="248" fill="{muted}" font-size="12">EDUCATION</text><text x="680" y="248" fill="{main}" font-size="15">BSc Computing</text>
<text x="500" y="285" fill="{muted}" font-size="12">STATUS</text><text x="680" y="285" fill="#10B981" font-size="14">BUILDING · LEARNING · SHIPPING</text>
<text x="500" y="339" fill="{cyan}" font-size="17">TECH.STACK // </text><text x="930" y="339" fill="{muted}" font-size="11">TOOLS FOR REAL-WORLD SOLUTIONS</text>
<text x="500" y="380" fill="{muted}" font-size="12">CORE.LANG</text><text x="680" y="380" fill="{main}" font-size="14">JavaScript · TypeScript</text>
<text x="500" y="417" fill="{muted}" font-size="12">CORE.FRONTEND</text><text x="680" y="417" fill="{main}" font-size="14">React · Vite</text>
<text x="500" y="454" fill="{muted}" font-size="12">CORE.BACKEND</text><text x="680" y="454" fill="{main}" font-size="14">Node.js</text>
<text x="500" y="491" fill="{muted}" font-size="12">CORE.DATABASE</text><text x="680" y="491" fill="{main}" font-size="14">SQLite</text>
<text x="500" y="528" fill="{muted}" font-size="12">CORE.INFRA</text><text x="680" y="528" fill="{main}" font-size="14">GitHub · Vercel</text>
<text x="930" y="380" fill="{muted}" font-size="12">○ PLAN</text><text x="930" y="410" fill="{muted}" font-size="12">○ DEVELOP</text><text x="930" y="440" fill="{muted}" font-size="12">○ TEST</text><text x="930" y="470" fill="{muted}" font-size="12">○ DEPLOY</text><text x="930" y="500" fill="#10B981" font-size="12">● ✓SOLVE</text>
<text x="500" y="70" fill="{muted}" font-size="11">IDEAS → SOLUTIONS → REAL IMPACT</text></g>
<rect x="480" y="545" width="205" height="42" rx="6" fill="none" stroke="{cyan}" opacity=".55"/><rect x="695" y="545" width="205" height="42" rx="6" fill="none" stroke="{cyan}" opacity=".55"/><rect x="910" y="545" width="235" height="42" rx="6" fill="none" stroke="{cyan}" opacity=".55"/>
<g font-family="monospace"><text x="493" y="563" fill="{cyan}" font-size="12">Silva Solutions Ltd</text><text x="493" y="579" fill="{muted}" font-size="9">Technology for real business problems.</text><text x="708" y="563" fill="{cyan}" font-size="12">Silvix</text><text x="708" y="579" fill="{muted}" font-size="9">AI CCTV · Fleet · Drone</text><text x="923" y="563" fill="{cyan}" font-size="12">STRAVIQ</text><text x="923" y="579" fill="{muted}" font-size="9">Project Intelligence &amp; Execution</text></g></svg>'''

open("dark.svg","w",encoding="utf-8").write(make(True))
open("light.svg","w",encoding="utf-8").write(make(False))

# trigger banner build
