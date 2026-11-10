# -*- coding: utf-8 -*-
"""cs-g1 修订（用户 2026-11-01 五项指令）：
① V_i 标注下移到 ＋、－ 中间（413→426）；
② 第2关 V_GSQ 正确框架：代表 V_DD 的方框移到后面（分压比·V_DD）；
③ I_DQ 箭头移到 D 极导线左侧（x 511→461，距导线仍 25px），文字移到箭头左侧（anchor end 436）；
④ V_DSQ 左移（620→560）并与衬底 B 箭头水平同轴（中心 y 294→265），＋/－ 同步；
⑤ 新增 V_T 标注（V_GSQ 下方）与 I_DO 标注（D 极导线右侧，无箭头）。
唯一性校验，失败不写盘。"""
import io, shutil, sys

SRC = 'cs-g1.html'
BAK = '/tmp/cs-g1.before-qlayout.html'

# ---- ① V_i 下移到 ＋、－ 中间 ----
R1 = (
    '<text class="hot-label" x="150" y="413" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>',
    '<text class="hot-label" x="150" y="426" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>')

# ---- ② V_GSQ 正确框架：V_DD 方框放后面 ----
R2 = (
    """                                    // 正确：栅极电流为零 → R_g1、R_g2 分压
                                    { tokens: [tk('V', 'GSQ'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])], correct: true },
                                    // 干扰①：分母漏一只电阻
                                    { tokens: [tk('V', 'GSQ'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }], [{ box: 1 }])] },
                                    // 干扰②：漏乘 V_DD（只剩分压比）
                                    { tokens: [tk('V', 'GSQ'), tk('='), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])] }""",
    """                                    // 正确：栅极电流为零 → R_g1、R_g2 分压；代表 V_DD 的方框放在后面
                                    { tokens: [tk('V', 'GSQ'), tk('='), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }]), tk('·'), { box: 1 }], correct: true },
                                    // 干扰①：分母漏一只电阻
                                    { tokens: [tk('V', 'GSQ'), tk('='), fr([{ box: 1 }], [{ box: 1 }]), tk('·'), { box: 1 }] },
                                    // 干扰②：漏乘 V_DD（只剩分压比）
                                    { tokens: [tk('V', 'GSQ'), tk('='), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])] }""")

R2F = (
    """                                fullExpr: [[tk('V', 'GSQ'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])]],
                                blanks: [
                                    { ansIds: ['comp-vdd'], label: [tk('V', 'DD')], pts: 2 },
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 2 },
                                    { ansIds: ['comp-rg1'], label: [tk('R', 'g1')], pts: 1 },
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 1 }
                                ]""",
    """                                fullExpr: [[tk('V', 'GSQ'), tk('='), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }]), tk('·'), { box: 1 }]],
                                blanks: [
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 2 },
                                    { ansIds: ['comp-rg1'], label: [tk('R', 'g1')], pts: 1 },
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 1 },
                                    { ansIds: ['comp-vdd'], label: [tk('V', 'DD')], pts: 2 }
                                ]""")

# ---- ③ q-idq 移到 D 极导线左侧 + ⑤ 新增 q-ido（D 极导线右侧，无箭头） ----
R3 = (
    """                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ（漏极电流箭头处）">
                    <line x1="511" y1="172" x2="511" y2="214" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="511,238 500,215 522,215" fill="#ff5252" stroke="none"/>
                    <rect class="hot" x="530" y="183" width="100" height="42" fill="none" stroke="none"/>
                    <text class="hot-label" x="536" y="215" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">I<tspan class="sub">DQ</tspan></text>
                </g>""",
    """                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ（漏极导线左侧红色箭头处）">
                    <line x1="461" y1="174" x2="461" y2="208" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="461,232 450,208 472,208" fill="#ff5252" stroke="none"/>
                    <rect class="hot" x="384" y="176" width="88" height="58" fill="none" stroke="none"/>
                    <text class="hot-label" x="436" y="215" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">I<tspan class="sub">DQ</tspan></text>
                </g>
                <g class="interactive" data-id="q-ido" data-name="饱和漏极电流 I_DO（已知参数，无箭头）">
                    <rect class="hot" x="500" y="176" width="66" height="30" fill="none" stroke="none"/>
                    <text class="hot-label" x="505" y="200" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">I<tspan class="sub">DO</tspan></text>
                </g>""")

# ---- ④ q-vdsq 左移 60 + 中心对齐 B 箭头 y=265 ----
R4 = (
    """                <g class="interactive" data-id="q-vdsq" data-name="漏源静态电压 V_DSQ（＋/− 标出极性）">
                    <rect class="hot" x="583" y="230" width="90" height="108" fill="none" stroke="none"/>
                    <text class="hot-label" x="620" y="258" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="620" y="294" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">DSQ</tspan></text>
                    <text class="hot-label" x="620" y="330" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>""",
    """                <g class="interactive" data-id="q-vdsq" data-name="漏源静态电压 V_DSQ（＋/− 标出极性）">
                    <rect class="hot" x="523" y="209" width="74" height="100" fill="none" stroke="none"/>
                    <text class="hot-label" x="560" y="229" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="560" y="265" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">DSQ</tspan></text>
                    <text class="hot-label" x="560" y="301" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>""")

# ---- ⑤ 新增 q-vt（V_GSQ 下方） ----
R5 = (
    """                    <text class="hot-label" x="466" y="366" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>""",
    """                    <text class="hot-label" x="466" y="366" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>
                <g class="interactive" data-id="q-vt" data-name="开启电压 V_T（阈值电压）">
                    <rect class="hot" x="382" y="371" width="62" height="30" fill="none" stroke="none"/>
                    <text class="hot-label" x="406" y="396" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">T</tspan></text>
                </g>""")

# ---- ANNOS：新增两条 + 修正 I_DQ 描述 ----
R6 = (
    """        'q-vdsq':""",
    """        'q-vt':         { text: '<b>V<sub>T</sub></b><br>开启电压（阈值电压）：V<sub>GS</sub> 超过 V<sub>T</sub> 才形成导电沟道，是转移特性方程中的门槛电压',
                          parts: [{ text: '这是开启电压VT，也叫阈值电压。山源电压超过它，才会形成导电沟道。' }] },
        'q-ido':        { text: '<b>I<sub>DO</sub></b><br>饱和漏极电流：转移特性参数（已知量），本图中只标符号、不画箭头',
                          parts: [{ text: '这是饱和漏极电流IDO，是转移特性里的已知参数。' }] },
        'q-vdsq':""")

R7 = (
    """        'q-idq':        { text: '<b>I<sub>DQ</sub></b><br>静态漏极电流：即漏极导线上红色箭头所示的电流，由转移特性方程代入 V<sub>GSQ</sub> 求得',
                          parts: [{ text: '这是IDQ，静态漏极电流，即漏极导线上红色箭头所示的电流，由转移特性方程代入山源静态电压求得。' }] },""",
    """        'q-idq':        { text: '<b>I<sub>DQ</sub></b><br>静态漏极电流：即漏极导线左侧红色箭头所示的电流，由转移特性方程代入 V<sub>GSQ</sub> 求得',
                          parts: [{ text: '这是IDQ，静态漏极电流，即漏极导线左侧红色箭头所示的电流，由转移特性方程代入山源静态电压求得。' }] },""")

# ---- qlabels：第2关显示新增两条 ----
R8 = (
    """                        qlabels: ['q-vth', 'q-idq', 'q-vdsq'],""",
    """                        qlabels: ['q-vth', 'q-vt', 'q-idq', 'q-ido', 'q-vdsq'],""")

REPS = [R1, R2, R2F, R3, R4, R5, R6, R7, R8]

s = io.open(SRC, encoding='utf-8', newline='').read()
for i, (old, new) in enumerate(REPS, 1):
    c = s.count(old)
    if c != 1:
        print('FAIL R%d: count=%d\n---\n%s' % (i, c, old[:160]))
        sys.exit(1)
shutil.copyfile(SRC, BAK)
for old, new in REPS:
    s = s.replace(old, new, 1)
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('OK: %d replacements written, backup %s' % (len(REPS), BAK))
