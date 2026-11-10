# -*- coding: utf-8 -*-
"""cs-g3 第113轮（2026-10-29 22:35）：RG1 居中于 C1 输入线与 VDD 轨之间；RG2 居中于分压竖线；
RS 与 C_S 水平同轴；+VDD 文字/端子左移30 导线缩短对齐；RL 居中于输出竖线、Vo 记号移到两拐角右侧。"""
import io, sys

P = "cs-g3.html"
s = io.open(P, encoding="utf-8", newline="").read()

pairs = [
    # ── 1) R_G1 上移至 y=143.5（VDD 轨 5 与输入线 282 的中点），体 117-170 ──
    ('<path class="hot" d="M 250 5 V 168.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 250 5 V 117" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="236.5" y="168.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="236.5" y="117" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 250 221.5 V 282" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 250 170 V 282" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="218" y="202" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G1</tspan></text>',
     '<text class="hot-label" x="218" y="150" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G1</tspan></text>'),
    # ── 2) R_G2 上移至分压竖线中点 y=438.5（352→525），体 412-465 ──
    ('<path class="hot" d="M 250 302 V 433.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 250 302 V 412" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="236.5" y="433.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="236.5" y="412" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 250 486.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 250 465 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label rg2-label" x="218" y="467" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G2</tspan></text>',
     '<text class="hot-label rg2-label" x="218" y="446" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G2</tspan></text>'),
    # ── 3) R_S 下移与 C_S 水平同轴（中心 433.5，C_S 板 425.25/441.25 中心 433.25），体 407-460 ──
    ('<path class="hot" d="M 578 341.5 V 389" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 578 341.5 V 407" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="564.5" y="389" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="564.5" y="407" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 578 442 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 578 460 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="548" y="423" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>',
     '<text class="hot-label" x="548" y="440" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>'),
    ('<line x1="578" y1="389" x2="578" y2="442" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="578" y1="407" x2="578" y2="460" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    # ── 4) +VDD 文字与端子左移 30px（860→830），电源导线缩短对齐（851→821）──
    ('<circle class="hot" cx="860" cy="5" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>',
     '<circle class="hot" cx="830" cy="5" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>'),
    ('<text class="hot-label vcc-label" x="860" y="54" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋V<tspan class="sub">DD</tspan></text>',
     '<text class="hot-label vcc-label" x="830" y="54" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋V<tspan class="sub">DD</tspan></text>'),
    ('<!-- 止于 +VDD 端子圆圈外缘（851），不再伸进端子圆圈内 -->',
     '<!-- 止于 +VDD 端子圆圈外缘（821），不再伸进端子圆圈内 -->'),
    ('<path class="hot" d="M 640 5 H 851" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 640 5 H 821" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line x1="860" y1="23" x2="860" y2="39" stroke="#34d399" stroke-width="5"/>',
     '<line x1="830" y1="23" x2="830" y2="39" stroke="#34d399" stroke-width="5"/>'),
    ('<line x1="832" y1="39" x2="888" y2="39" stroke="#34d399" stroke-width="5"/>',
     '<line x1="802" y1="39" x2="858" y2="39" stroke="#34d399" stroke-width="5"/>'),
    ('<line x1="846" y1="51" x2="874" y2="51" stroke="#34d399" stroke-width="4.5"/>',
     '<line x1="816" y1="51" x2="844" y2="51" stroke="#34d399" stroke-width="4.5"/>'),
    ('<line x1="854" y1="63" x2="866" y2="63" stroke="#34d399" stroke-width="4"/>',
     '<line x1="824" y1="63" x2="836" y2="63" stroke="#34d399" stroke-width="4"/>'),
    # ── 5) R_L 上移至输出竖线中点 y=343.25（161.5→525），体 317-370 ──
    ('<path class="hot" d="M 800 161.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 800 161.5 V 317" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="786.5" y="327" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="786.5" y="317" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 800 380 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 800 370 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="770" y="360" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>',
     '<text class="hot-label" x="770" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>'),
    # ── 6) V_o 记号移到输出竖线上下拐角右侧（＋175 / －538，V_o 353→357 居中），热区随扩 ──
    ('<rect class="hot" x="830" y="218" width="56" height="230" fill="none" stroke="none"/>',
     '<rect class="hot" x="830" y="150" width="56" height="415" fill="none" stroke="none"/>'),
    ('<text class="hot-label" x="858" y="268" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="858" y="175" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    ('<text class="hot-label" x="858" y="353" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">o</tspan></text>',
     '<text class="hot-label" x="858" y="357" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">o</tspan></text>'),
    ('<text class="hot-label" x="858" y="438" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="858" y="538" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    # ── 7) 整理态 rarr-rd 与 R_L 保持对齐（体 317-370）──
    ('<path class="hot keepw" d="M 700 161.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot keepw" d="M 700 161.5 V 317" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="686.5" y="327" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="686.5" y="317" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot keepw" d="M 700 380 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot keepw" d="M 700 370 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="668" y="360" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>',
     '<text class="hot-label" x="668" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>'),
]

for i, (o, n) in enumerate(pairs):
    c = s.count(o)
    if c != 1:
        print("FAIL pair#%d count=%d :: %s" % (i + 1, c, o[:70].replace("\n", "\\n")))
        sys.exit(1)
for o, n in pairs:
    s = s.replace(o, n)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("OK %d pairs applied" % len(pairs))
