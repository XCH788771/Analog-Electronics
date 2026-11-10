# -*- coding: utf-8 -*-
import io

PATH = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html"

# (old, new) 严格唯一性校验后整文件替换；全部通过才写盘
REPS = [
    # --- 输入端口 V_i（顶端子 + 标注下移40）---
    ('            <path class="hot" d="M 110 178 H 206" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 110 218 H 206" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <circle class="hot" cx="110" cy="178" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>',
     '            <circle class="hot" cx="110" cy="218" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>'),
    ('                <text class="hot-label" x="110" y="235" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '                <text class="hot-label" x="110" y="275" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    ('                <text class="hot-label" x="110" y="305" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>',
     '                <text class="hot-label" x="110" y="345" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>'),
    ('                <text class="hot-label" x="110" y="375" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '                <text class="hot-label" x="110" y="415" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),

    # --- 输入耦合电容 C1（下移40）---
    ('            <line class="hot" x1="206" y1="156" x2="206" y2="200" stroke="#ffffff" stroke-width="3.5"/>',
     '            <line class="hot" x1="206" y1="196" x2="206" y2="240" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <line class="hot" x1="220" y1="156" x2="220" y2="200" stroke="#ffffff" stroke-width="3.5"/>',
     '            <line class="hot" x1="220" y1="196" x2="220" y2="240" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <text class="hot-label" x="213" y="245" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>',
     '            <text class="hot-label" x="213" y="285" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>'),

    # --- 输入导线 / 栅极节点 / 栅极引线（下移40）---
    ('            <path class="hot" d="M 220 178 H 390" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 220 218 H 390" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <circle cx="390" cy="178" r="7" fill="#ffffff" pointer-events="none"/>',
     '            <circle cx="390" cy="218" r="7" fill="#ffffff" pointer-events="none"/>'),
    ('            <path class="hot" d="M 390 178 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 390 218 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # --- 栅极电阻 RG（下移40）---
    ('            <rect class="hot" x="376.5" y="258.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <rect class="hot" x="376.5" y="298.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <text class="hot-label" x="356" y="293" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G</tspan></text>',
     '            <text class="hot-label" x="356" y="333" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G</tspan></text>'),
    ('            <path class="hot" d="M 390 178 V 258.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 390 218 V 298.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <path class="hot" d="M 390 311.5 V 330 H 250" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 390 351.5 V 370 H 250" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # --- 分压节点 node-div 下移40（RG/RG2 自然连接）---
    ('            <circle cx="250" cy="330" r="7" fill="#ffffff" pointer-events="none"/>',
     '            <circle cx="250" cy="370" r="7" fill="#ffffff" pointer-events="none"/>'),
    ('            <path class="hot" d="M 250 181.5 V 330" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 250 181.5 V 370" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <path class="hot" d="M 250 330 V 393.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 250 370 V 433.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # --- 下偏置电阻 RG2（下移40）---
    ('            <rect class="hot" x="236.5" y="393.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <rect class="hot" x="236.5" y="433.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <text class="hot-label rg2-label" x="218" y="427" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G2</tspan></text>',
     '            <text class="hot-label rg2-label" x="218" y="467" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G2</tspan></text>'),
    ('            <path class="hot" d="M 250 446.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 250 486.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # --- 源极节点 / 源极电阻 RS / 旁路 C_S 引线（下移40）---
    ('            <circle cx="530" cy="216" r="7" fill="#ffffff" pointer-events="none"/>',
     '            <circle cx="530" cy="256" r="7" fill="#ffffff" pointer-events="none"/>'),
    ('            <path class="hot" d="M 530 216 V 269.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 530 256 V 309.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <rect class="hot" x="516.5" y="269.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <rect class="hot" x="516.5" y="309.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <text class="hot-label" x="500" y="303" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>',
     '            <text class="hot-label" x="500" y="343" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>'),
    ('            <path class="hot" d="M 530 322.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 530 362.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <path class="hot" d="M 530 216 H 598 V 398" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 530 256 H 598 V 398" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # --- 漏极：节点保持不动，FET 漏极引线改为向上接到固定漏极节点 ---
    ('            <path class="hot" d="M 530 136.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 530 176.5 V 140 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # --- 场效应管 FET（整体下移40）---
    ('            <rect class="hot" x="438" y="118" width="158" height="140" fill="none" stroke="none"/>',
     '            <rect class="hot" x="438" y="158" width="158" height="140" fill="none" stroke="none"/>'),
    ('            <line class="hot" x1="502" y1="144" x2="502" y2="212" stroke="#ffffff" stroke-width="7"/>',
     '            <line class="hot" x1="502" y1="184" x2="502" y2="252" stroke="#ffffff" stroke-width="7"/>'),
    ('            <line class="hot" x1="530" y1="136.5" x2="530" y2="156" stroke="#ffffff" stroke-width="7"/>',
     '            <line class="hot" x1="530" y1="176.5" x2="530" y2="196" stroke="#ffffff" stroke-width="7"/>'),
    ('            <line class="hot" x1="530" y1="168" x2="530" y2="184" stroke="#ffffff" stroke-width="7"/>',
     '            <line class="hot" x1="530" y1="208" x2="530" y2="224" stroke="#ffffff" stroke-width="7"/>'),
    ('            <line class="hot" x1="530" y1="196" x2="530" y2="212" stroke="#ffffff" stroke-width="7"/>',
     '            <line class="hot" x1="530" y1="236" x2="530" y2="252" stroke="#ffffff" stroke-width="7"/>'),
    ('            <polygon class="hot-fill" points="530,178 554,164 554,192" fill="#ffffff" stroke="none"/>',
     '            <polygon class="hot-fill" points="530,218 554,204 554,232" fill="#ffffff" stroke="none"/>'),
    ('            <path class="hot" d="M 554 178 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 554 218 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <text class="hot-label" x="482" y="238" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">g</text>',
     '            <text class="hot-label" x="482" y="278" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">g</text>'),
    ('            <text class="hot-label" x="562" y="122" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>',
     '            <text class="hot-label" x="562" y="162" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>'),
    ('            <text class="hot-label" x="562" y="248" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>',
     '            <text class="hot-label" x="562" y="288" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>'),
    ('            <text class="hot-label" x="592" y="190" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">B</text>',
     '            <text class="hot-label" x="592" y="230" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">B</text>'),

    # --- fx 特效层：C1 短路桥、等效模型、RS 短接桥 同步跟随 ---
    ('                <line x1="206" y1="178" x2="220" y2="178" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '                <line x1="206" y1="218" x2="220" y2="218" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    ('                <circle class="hot" cx="502" cy="178" r="6" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>',
     '                <circle class="hot" cx="502" cy="218" r="6" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>'),
    ('                    <path class="hot keepw" d="M 530 136.5 V 144 H 554 V 148" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '                    <path class="hot keepw" d="M 530 140 V 164 H 554 V 168" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('                    <path class="hot" d="M 554 148 L 586 178 L 554 208 L 522 178 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>',
     '                    <path class="hot" d="M 554 168 L 586 198 L 554 228 L 522 198 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>'),
    ('                    <path class="hot keepw" d="M 554 208 V 212 H 530 V 216" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '                    <path class="hot keepw" d="M 554 228 V 252 H 530 V 256" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('                        <rect class="hot" x="586" y="146" width="82" height="44" fill="none" stroke="none"/>',
     '                        <rect class="hot" x="586" y="186" width="82" height="44" fill="none" stroke="none"/>'),
    ('                        <text class="hot-label" x="590" y="178" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>',
     '                        <text class="hot-label" x="590" y="218" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>'),
    ('                    <line x1="554" y1="158" x2="554" y2="184" stroke="#ff5252" stroke-width="5"/>',
     '                    <line x1="554" y1="178" x2="554" y2="204" stroke="#ff5252" stroke-width="5"/>'),
    ('                    <polygon points="554,196 545,181 563,181" fill="#ff5252" stroke="none"/>',
     '                    <polygon points="554,216 545,201 563,201" fill="#ff5252" stroke="none"/>'),
    ('                <line x1="530" y1="269.5" x2="530" y2="356" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '                <line x1="530" y1="309.5" x2="530" y2="362.5" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
]

with io.open(PATH, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

fail = []
for i, (old, new) in enumerate(REPS):
    n = content.count(old)
    if n != 1:
        fail.append((i, n))

if fail:
    for i, n in fail:
        print("UNIQUE-FAIL idx=%d count=%d  old=%r" % (i, n, REPS[i][0][:60]))
    print("ABORT: 未写盘")
    sys.exit(1)

for old, new in REPS:
    content = content.replace(old, new, 1)

with io.open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("OK: 全部 %d 处替换成功并写盘" % len(REPS))
