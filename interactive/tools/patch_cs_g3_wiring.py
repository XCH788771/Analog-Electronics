# -*- coding: utf-8 -*-
"""cs-g3 第111轮结构改造（2026-10-28 23:40）
1) C1 左移 25px；C1→G 极一条直导线，横穿分压竖线处去节点（不连通）；
   R_G 移到栅极引线下方支路：下引 50px + 90° 转角向左接分压节点，R_G 居该水平线中间。
2) C_S 分支节点下移到 R_S 上端导线中间 (578,341.5)；C_S 下移到其竖直导线中间。
3) D/S 引线改接沟道上/下段中点（236.25/294）；水平段延长与 B 端右对齐(x=578)；
   R_D/R_S/C_S 右移 13px；移除漏极/源极节点圆与 C_S 上方 ＋ 号；B 经导线下接 S 极。
"""
import io, sys

P = "cs-g3.html"
s = io.open(P, encoding="utf-8", newline="").read()

pairs = [
    # ---------- ① 输入回路：C1 左移 25px ----------
    ('<path class="hot" d="M 110 302 H 206" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 110 302 H 181" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="206" y1="280" x2="206" y2="324" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="181" y1="280" x2="181" y2="324" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="220" y1="280" x2="220" y2="324" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="195" y1="280" x2="195" y2="324" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="213" y="369" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>',
     '<text class="hot-label" x="188" y="369" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>'),
    ('<line x1="206" y1="302" x2="220" y2="302" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="181" y1="302" x2="195" y2="302" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    # 输入导线直连栅极；R_G 下挂支路两段导线（解析器不支持多 M 子路径，拆两条）
    ('''        <g class="interactive" data-id="wire-in-gate" data-name="输入导线（C_1—R_G 左端）">
            <path class="hot" d="M 220 302 H 363.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-gate-out" data-name="栅极引线（R_G 右端—MOSFET 栅极）">
            <path class="hot" d="M 416.5 302 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-in-gate" data-name="输入导线（C_1—MOSFET 栅极，与分压竖线交叉不连通）">
            <path class="hot" d="M 195 302 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-rg-drop" data-name="R_G 接线·下引段（栅极引线—R_G 右端，下引 50px 后 90° 转角向左）">
            <path class="hot" d="M 390 302 V 352 H 346.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="390" cy="302" r="7" fill="#ffffff" pointer-events="none"/>
        </g>
        <g class="interactive" data-id="wire-rg-link" data-name="R_G 接线·左段（R_G 左端—分压节点）">
            <path class="hot" d="M 293.5 352 H 250" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    # R_G 移到下挂水平线中间 (320,352)
    ('''            <rect class="hot" x="363.5" y="288.5" width="53" height="27" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <text class="hot-label" x="390" y="275" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">R<tspan class="sub">G</tspan></text>''',
     '''            <rect class="hot" x="293.5" y="338.5" width="53" height="27" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <text class="hot-label" x="320" y="400" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">R<tspan class="sub">G</tspan></text>'''),
    # 分压节点圆移到 R_G 接入点 (250,352)
    ('''        <g id="node-div" data-id="node-div" data-name="分压节点（R_G1/R_G2/输入导线交汇）">
            <circle cx="250" cy="302" r="7" fill="#ffffff" pointer-events="none"/>
        </g>''',
     '''        <g id="node-div" data-id="node-div" data-name="分压节点（R_G1/R_G2/R_G 交汇）">
            <circle cx="250" cy="352" r="7" fill="#ffffff" pointer-events="none"/>
        </g>'''),
    # ---------- ③ 漏极支路：右移对齐 B 端(x=578)，D 接沟道上段中点 ----------
    ('<path class="hot" d="M 565 5 V 83.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 578 5 V 83.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="551.5" y="83.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="564.5" y="83.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="535" y="117" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>',
     '<text class="hot-label" x="548" y="117" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>'),
    ('''        <!-- 漏极节点（R_D 下端 — 沟道上端 — C_2 左端接线在此交汇） -->
        <g id="node-drain" data-id="node-drain" data-name="漏极节点（R_D 下端引线—C_2 分支）">
            <circle cx="565" cy="181.5" r="7" fill="#ffffff" pointer-events="none"/>
        </g>
        <g class="interactive" data-id="wire-rd-lead" data-name="漏极引线（沟道上端—R_D 下端，经 90° 转角）">
            <path class="hot" d="M 530 226.5 H 565 V 181.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rd-lead" data-name="漏极引线（沟道 d 段中点—漏极输出节点，经 90° 转角）">
            <path class="hot" d="M 530 236.25 H 578 V 181.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    ('''        <g class="interactive" data-id="wire-rd-bot" data-name="R_D 下端引线（漏极节点—R_D）">
            <path class="hot" d="M 565 181.5 V 136.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rd-bot" data-name="R_D 下端引线（漏极输出节点—R_D）">
            <path class="hot" d="M 578 181.5 V 136.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    ('''        <g class="interactive" data-id="wire-drain-out" data-name="漏极输出导线（漏极节点—C_2）">
            <path class="hot" d="M 565 181.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-drain-out" data-name="漏极输出导线（漏极输出节点—C_2）">
            <path class="hot" d="M 578 181.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    # ---------- ③ 场效应管符号：B 移到沟道中段中点并下接 S 极 ----------
    ('<polygon class="hot-fill" points="530,268 554,254 554,282" fill="#ffffff" stroke="none"/>',
     '<polygon class="hot-fill" points="530,266 554,252 554,280" fill="#ffffff" stroke="none"/>'),
    ('<path class="hot" d="M 554 268 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 554 266 H 578 V 294" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="578" y="214" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>',
     '<text class="hot-label" x="554" y="222" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">d</text>'),
    ('<text class="hot-label" x="578" y="322" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>',
     '<text class="hot-label" x="554" y="334" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">s</text>'),
    ('            <!-- 衬底 B：自沟道右侧引出，箭头指向沟道（N 沟道衬底箭头向内）；共源组态中 B 接源极 -->',
     '            <!-- 衬底 B：自沟道中段中点引出，箭头指向沟道（N 沟道衬底箭头向内）；经导线右行后垂直下接 S 极 -->'),
    # ---------- ③ 源极支路：S 接沟道下段中点(294)、右移对齐 x=578 ----------
    ('''        <g class="interactive" data-id="wire-rs-top" data-name="源极接线（源极节点→R_S，经 90° 转角）">
            <path class="hot" d="M 530 306 H 565 V 336" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rs-top" data-name="源极接线（S 极—C_S 分支点，经 90° 转角）">
            <path class="hot" d="M 530 294 H 578 V 341.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    ('''        <!-- 源极节点（沟道下端 — R_S 上端 — C_S 上端接线在此交汇） -->
        <g id="node-source" data-id="node-source" data-name="源极节点">
            <circle cx="530" cy="306" r="7" fill="#ffffff" pointer-events="none"/>
        </g>
''', ''),
    ('<path class="hot" d="M 565 336 V 389" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 578 341.5 V 389" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="551.5" y="389" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="564.5" y="389" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="535" y="423" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>',
     '<text class="hot-label" x="548" y="423" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>'),
    ('<path class="hot" d="M 565 442 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 578 442 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # C_S 分支节点下移到 R_S 上端导线中间 (578,341.5)；C_S 右移 13、下移到竖直导线中间
    ('''            <path class="hot" d="M 565 336 H 633 V 422.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="565" cy="336" r="7" fill="#ffffff" pointer-events="none"/>''',
     '''            <path class="hot" d="M 578 341.5 H 646 V 425.25" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="578" cy="341.5" r="7" fill="#ffffff" pointer-events="none"/>'''),
    ('<line class="hot" x1="611" y1="422.5" x2="655" y2="422.5" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="624" y1="425.25" x2="668" y2="425.25" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="611" y1="438.5" x2="655" y2="438.5" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="624" y1="441.25" x2="668" y2="441.25" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <text class="hot-label" x="675" y="407" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">＋</text>\n', ''),
    ('<text class="hot-label" x="675" y="463" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">C<tspan class="sub">S</tspan></text>',
     '<text class="hot-label" x="688" y="463" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">C<tspan class="sub">S</tspan></text>'),
    ('<path class="hot" d="M 633 438.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 646 441.25 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # ---------- 地轨 / 接地符号随右移 ----------
    ('<line x1="633" y1="422.5" x2="633" y2="438.5" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="646" y1="425.25" x2="646" y2="441.25" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    ('<line x1="565" y1="389" x2="565" y2="442" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="578" y1="389" x2="578" y2="442" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    ('''            <path class="hot" d="M 250 525 H 565" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="565" cy="525" r="7" fill="#ffffff" pointer-events="none"/>''',
     '''            <path class="hot" d="M 250 525 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="578" cy="525" r="7" fill="#ffffff" pointer-events="none"/>'''),
    ('''            <path class="hot" d="M 565 525 H 633" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="633" cy="525" r="7" fill="#ffffff" pointer-events="none"/>''',
     '''            <path class="hot" d="M 578 525 H 646" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="646" cy="525" r="7" fill="#ffffff" pointer-events="none"/>'''),
    ('<path class="hot" d="M 633 525 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 646 525 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('''            <line class="hot" x1="565" y1="525" x2="565" y2="543" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="533" y1="543" x2="597" y2="543" stroke="#ffffff" stroke-width="3.5"/>
            <line class="hot" x1="543" y1="551" x2="587" y2="551" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="551" y1="559" x2="579" y2="559" stroke="#ffffff" stroke-width="2.5"/>''',
     '''            <line class="hot" x1="578" y1="525" x2="578" y2="543" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="546" y1="543" x2="610" y2="543" stroke="#ffffff" stroke-width="3.5"/>
            <line class="hot" x1="556" y1="551" x2="600" y2="551" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="564" y1="559" x2="592" y2="559" stroke="#ffffff" stroke-width="2.5"/>'''),
    # ---------- fx-tmodel 等效层随动（D 236.25 / S 294 / 菱形中心 265） ----------
    ('''                    <path class="hot keepw" d="M 530 226.5 V 236 H 554 V 241" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot" d="M 554 241 L 586 266 L 554 291 L 522 266 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot keepw" d="M 554 291 V 296 H 530 V 306" fill="none" stroke="#ffffff" stroke-width="3.5"/>''',
     '''                    <path class="hot keepw" d="M 530 236.25 V 240 H 554" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot" d="M 554 240 L 586 265 L 554 290 L 522 265 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot keepw" d="M 554 290 V 294 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>'''),
    ('''                    <line x1="554" y1="246" x2="554" y2="269" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="554,284 545,269 563,269" fill="#ff5252" stroke="none"/>''',
     '''                    <line x1="554" y1="245" x2="554" y2="268" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="554,283 545,268 563,268" fill="#ff5252" stroke="none"/>'''),
    ('<circle class="qdot" cx="530" cy="226.5" r="8" fill="#ff5252"/>',
     '<circle class="qdot" cx="530" cy="236.25" r="8" fill="#ff5252"/>'),
    ('<circle class="qdot" cx="530" cy="306" r="8" fill="#ff5252"/>',
     '<circle class="qdot" cx="530" cy="294" r="8" fill="#ff5252"/>'),
    ('                 D-S 受控源支路直连漏极节点 (530,140) 与源极节点 (530,306)，菱形符号居中 (554,223)；',
     '                 D-S 受控源支路直连沟道 d 段中点 (530,236.25) 与 s 段中点 (530,294)，菱形符号居中 (554,265)；'),
    ('                 G 在栅极引线末端 (502,268)，D 在漏极节点 (530,140)，S 在源极节点 (530,306) -->',
     '                 G 在栅极引线末端 (502,302)，D 在沟道 d 段中点 (530,236.25)，S 在沟道 s 段中点 (530,294) -->'),
    # ---------- 区 C/D：fadeWith / STAGE_UNITS / ANNOS ----------
    ("                            'comp-c2': ['wire-drain-out', 'node-drain', 'wire-c2-out', 'comp-rl', 'wire-rl-top', 'wire-rl-bot', 'comp-vo', 'wire-gnd-r'],",
     "                            'comp-c2': ['wire-drain-out', 'wire-c2-out', 'comp-rl', 'wire-rl-top', 'wire-rl-bot', 'comp-vo', 'wire-gnd-r'],"),
    ("            fadeGroup('comp-rd', true); fadeGroup('wire-rd-top', true); fadeGroup('wire-rd-bot', true);\n            fadeGroup('node-drain', true);   // R_D 下移后漏极节点只是导线折角，节点圆一并移除",
     "            fadeGroup('comp-rd', true); fadeGroup('wire-rd-top', true); fadeGroup('wire-rd-bot', true);"),
    ("        ['comp-vi', 'wire-vi-in', 'comp-c1', 'wire-in-gate', 'wire-gate-out',",
     "        ['comp-vi', 'wire-vi-in', 'comp-c1', 'wire-in-gate',"),
    ("         'comp-t', 'comp-rd', 'wire-rd-top', 'wire-rd-bot', 'node-drain', 'wire-rd-lead', 'wire-drain-out',",
     "         'comp-t', 'comp-rd', 'wire-rd-top', 'wire-rd-bot', 'wire-rd-lead', 'wire-drain-out',"),
    ("         'comp-rg',\n         'comp-rs', 'wire-rs-top', 'wire-rs-lead', 'node-source', 'wire-rs-bot',",
     "         'comp-rg', 'wire-rg-drop', 'wire-rg-link',\n         'comp-rs', 'wire-rs-top', 'wire-rs-lead', 'wire-rs-bot',"),
    ("        'node-div':     { text: '分压节点：R<sub>G1</sub> / R<sub>G2</sub> / R<sub>G</sub> 下端在此交汇',",
     "        'node-div':     { text: '分压节点：R<sub>G1</sub> / R<sub>G2</sub> / R<sub>G</sub> 右端在此交汇',"),
    ("        'node-drain':   { text: '漏极节点：R<sub>D</sub> 下端—输出导线—沟道上端在此交汇',\n                          parts: [{ text: '这是漏极节点，漏极电阻、输出导线和沟道上端在这里连接。' }] },\n", ''),
    ("        'wire-rd-lead': { text: '漏极引线：沟道上端 → 35px 水平 → 垂直向上（90° 转角）',\n                          parts: [{ text: '这条导线从沟道上端向右走一小段，再垂直向上接到漏极电阻，形成直角。' }] },",
     "        'wire-rd-lead': { text: '漏极引线：沟道 d 段中点 → 水平右行 → 垂直向上（90° 转角）',\n                          parts: [{ text: '这条导线从沟道d段中点向右，再垂直向上接到漏极输出节点，形成直角。' }] },"),
    ("        'wire-rd-bot':  { text: 'R<sub>D</sub> 下端引线：漏极节点 → R<sub>D</sub>',\n                          parts: [{ text: '这条导线把漏极节点接到漏极电阻的下端。' }] },",
     "        'wire-rd-bot':  { text: 'R<sub>D</sub> 下端引线：漏极输出节点 → R<sub>D</sub>',\n                          parts: [{ text: '这条导线把漏极输出节点接到漏极电阻的下端。' }] },"),
    ("        'wire-drain-out':{ text: '漏极输出导线：漏极节点 → C<sub>2</sub>',\n                          parts: [{ text: '这条导线把漏极节点接出的信号送到输出耦合电容。' }] },",
     "        'wire-drain-out':{ text: '漏极输出导线：漏极输出节点 → C<sub>2</sub>',\n                          parts: [{ text: '这条导线把漏极输出节点接出的信号送到输出耦合电容。' }] },"),
    ("        'node-source':  { text: '源极节点：沟道下端—R<sub>S</sub>—C<sub>S</sub> 在此交汇',\n                          parts: [{ text: '这是源极节点，沟道下端、源极电阻和旁路电容在这里连接。' }] },\n", ''),
    ("        'wire-rs-top':  { text: '源极接线：源极节点 → 35px 水平 → 垂直向下（90° 转角）',\n                          parts: [{ text: '这条导线把源极节点接到源极电阻的上端。' }] },",
     "        'wire-rs-top':  { text: '源极接线：S 极 → 水平右行 → 垂直向下（90° 转角）',\n                          parts: [{ text: '这条导线把源极接到源极电阻的上端，途中引出旁路电容的分支点。' }] },"),
    ("        'wire-cs-top':  { text: 'C<sub>S</sub> 上端接线：源极节点 → C<sub>S</sub> 上极板',\n                          parts: [{ text: '这条导线把源极节点接到旁路电容的上极板。' }] },",
     "        'wire-cs-top':  { text: 'C<sub>S</sub> 上端接线：C<sub>S</sub> 分支点 → C<sub>S</sub> 上极板',\n                          parts: [{ text: '这条导线从源极分支点向右，接到旁路电容的上极板。' }] },"),
    ("""        'wire-in-gate': { text: '输入导线：C<sub>1</sub> → 栅极节点',
                          parts: [{ text: '这条导线把输入耦合电容接出的信号送到栅极节点。' }] },
        'wire-gate-out':{ text: '栅极引线：栅极节点 → MOSFET 栅极',
                          parts: [{ text: '这条导线把栅极信号送到场效应管的栅极。' }] }""",
     """        'wire-in-gate': { text: '输入导线：C<sub>1</sub> → MOSFET 栅极（横穿分压竖线、交叉不连通）',
                          parts: [{ text: '这条导线把输入耦合电容接出的信号直接送到场效应管的栅极，途中横穿分压竖线但没有连在一起。' }] },
        'wire-rg-drop': { text: 'R<sub>G</sub> 接线·下引段：栅极引线 → 下引 50px → 90° 转角向左',
                          parts: [{ text: '这条接线从栅极引线向下引50像素，再向左转弯，栅极电阻就串在这一段水平导线上。' }] },
        'wire-rg-link': { text: 'R<sub>G</sub> 接线·左段：R<sub>G</sub> 左端 → 分压节点',
                          parts: [{ text: '这段导线把栅极电阻的左端接到分压节点。' }] }"""),
]

fail = False
for i, (o, n) in enumerate(pairs, 1):
    c = s.count(o)
    if c != 1:
        print("FAIL pair %d: count=%d | %s" % (i, c, o[:72].replace("\n", "\\n")))
        fail = True
if fail:
    sys.exit(1)
for o, n in pairs:
    s = s.replace(o, n)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("OK %d pairs written" % len(pairs))
