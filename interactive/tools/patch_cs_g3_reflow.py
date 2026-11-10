# -*- coding: utf-8 -*-
"""cs-g3 第110轮结构重排补丁（原子写入，唯一性校验，任一不匹配则整体不写盘）

用户四项指令：
 1) RG1 上移 50px；RG 改横置于栅极水平导线上；C1 及左右导线下降到与栅极竖条底端(302)对齐成直角
 2) D 极加 35px 水平导线，R_D 及上下引线右移 35 接成 90°转角；C2 接点下移到垂直引线中点(181.5)
 3) S 极同加 35px 水平导线，R_S/C_S 右移 35；C_S 分支点下移 30(→336)；C_S 下移到其垂直导线中点(430.5)
 4) 移除 R_L 下方节点圆；R_L 下移到垂直导线中点(353.25)
"""
import io, sys

PATH = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html"

PAIRS = [
    # ========== 1) R_G1 上移 50 ==========
    ('d="M 250 5 V 218.5"', 'd="M 250 5 V 168.5"'),
    ('<rect class="hot" x="236.5" y="218.5" width="27" height="53"',
     '<rect class="hot" x="236.5" y="168.5" width="27" height="53"'),
    ('x="218" y="252"', 'x="218" y="202"'),
    ('d="M 250 271.5 V 370"', 'd="M 250 221.5 V 302"'),
    # ========== 分压节点下移到栅极水平线(302) ==========
    ('<g id="node-div" data-id="node-div" data-name="分压节点（R_G1/R_G2/R_G 交汇）">\n            <circle cx="250" cy="370" r="7"',
     '<g id="node-div" data-id="node-div" data-name="分压节点（R_G1/R_G2/输入导线交汇）">\n            <circle cx="250" cy="302" r="7"'),
    ('d="M 250 370 V 433.5"', 'd="M 250 302 V 433.5"'),
    # ========== R_G 改横置：删除 wire-rg-top / wire-rg-bot，comp-rg 横放 ==========
    ('''        <!-- 栅极电阻 R_G（分压节点→栅极节点；交流等效中与 R_G1∥R_G2 串联决定输入电阻） -->
        <g class="interactive" data-id="wire-rg-top" data-name="栅极节点接线（栅极节点→R_G）">
            <path class="hot" d="M 390 268 V 298.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="comp-rg" data-name="栅极电阻 R_G">
            <rect class="hot" x="376.5" y="298.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <text class="hot-label" x="356" y="333" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G</tspan></text>
        </g>
        <g class="interactive" data-id="wire-rg-bot" data-name="R_G 下端接线（→分压节点）">
            <path class="hot" d="M 390 351.5 V 370 H 250" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <!-- 栅极电阻 R_G（横置于栅极水平导线上；交流等效中与 R_G1∥R_G2 串联决定输入电阻） -->
        <g class="interactive" data-id="comp-rg" data-name="栅极电阻 R_G">
            <rect class="hot" x="363.5" y="288.5" width="53" height="27" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <text class="hot-label" x="390" y="275" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">R<tspan class="sub">G</tspan></text>
        </g>'''),
    # ========== 公共地线：R_S→565、C_S→633、删 R_L 下节点 ==========
    ('<path class="hot" d="M 250 525 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n            <circle cx="530" cy="525" r="7"',
     '<path class="hot" d="M 250 525 H 565" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n            <circle cx="565" cy="525" r="7"'),
    ('<path class="hot" d="M 530 525 H 598" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n            <circle cx="598" cy="525" r="7"',
     '<path class="hot" d="M 565 525 H 633" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n            <circle cx="633" cy="525" r="7"'),
    ('<path class="hot" d="M 598 525 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n            <circle cx="800" cy="525" r="7" fill="#ffffff" pointer-events="none"/>',
     '<path class="hot" d="M 633 525 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # ========== 接地符号随 R_S 右移到 565 ==========
    ('<line class="hot" x1="530" y1="525" x2="530" y2="543" stroke="#ffffff" stroke-width="3"/>',
     '<line class="hot" x1="565" y1="525" x2="565" y2="543" stroke="#ffffff" stroke-width="3"/>'),
    ('<line class="hot" x1="498" y1="543" x2="562" y2="543" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="533" y1="543" x2="597" y2="543" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="508" y1="551" x2="552" y2="551" stroke="#ffffff" stroke-width="3"/>',
     '<line class="hot" x1="543" y1="551" x2="587" y2="551" stroke="#ffffff" stroke-width="3"/>'),
    ('<line class="hot" x1="516" y1="559" x2="544" y2="559" stroke="#ffffff" stroke-width="2.5"/>',
     '<line class="hot" x1="551" y1="559" x2="579" y2="559" stroke="#ffffff" stroke-width="2.5"/>'),
    # ========== com-t 端子标注 d/s 避让新引线 ==========
    ('<text class="hot-label" x="562" y="212" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>',
     '<text class="hot-label" x="538" y="214" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>'),
    ('<text class="hot-label" x="562" y="338" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>',
     '<text class="hot-label" x="538" y="352" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>'),
    # ========== 2) 漏极支路：R_D→565，35px 水平 + 90°转角，C2 接点 181.5 ==========
    ('<g class="interactive" data-id="wire-rd-top" data-name="R_D 上端接线（→电源轨）">\n            <path class="hot" d="M 530 5 V 83.5"',
     '<g class="interactive" data-id="wire-rd-top" data-name="R_D 上端接线（→电源轨）">\n            <path class="hot" d="M 565 5 V 83.5"'),
    ('<rect class="hot" x="516.5" y="83.5" width="27" height="53"',
     '<rect class="hot" x="551.5" y="83.5" width="27" height="53"'),
    ('<text class="hot-label" x="500" y="117" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>',
     '<text class="hot-label" x="535" y="117" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>'),
    ('<g id="node-drain" data-id="node-drain" data-name="漏极节点">\n            <circle cx="530" cy="140" r="7"',
     '<g id="node-drain" data-id="node-drain" data-name="漏极节点（R_D 下端引线—C_2 分支）">\n            <circle cx="565" cy="181.5" r="7"'),
    ('''        <g class="interactive" data-id="wire-drain-out" data-name="漏极输出导线（漏极节点—C_2）">
            <path class="hot" d="M 530 226.5 V 140 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rd-lead" data-name="漏极引线（沟道上端—R_D 下端，经 90° 转角）">
            <path class="hot" d="M 530 226.5 H 565 V 181.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-rd-bot" data-name="R_D 下端引线（漏极节点—R_D）">
            <path class="hot" d="M 565 181.5 V 136.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-drain-out" data-name="漏极输出导线（漏极节点—C_2）">
            <path class="hot" d="M 565 181.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    ('<line class="hot" x1="670" y1="118" x2="670" y2="162" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="670" y1="159.5" x2="670" y2="203.5" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="684" y1="118" x2="684" y2="162" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="684" y1="159.5" x2="684" y2="203.5" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="677" y="102" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">2</tspan></text>',
     '<text class="hot-label" x="677" y="144" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">2</tspan></text>'),
    ('<path class="hot" d="M 684 140 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 684 181.5 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # ========== 4) R_L 下移到垂直导线中点 353.25（体 327-380），V_o 随动 ==========
    ('<path class="hot" d="M 800 140 V 253.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 800 181.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="786.5" y="253.5" width="27" height="53"',
     '<rect class="hot" x="786.5" y="327" width="27" height="53"'),
    ('<text class="hot-label" x="770" y="287" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>',
     '<text class="hot-label" x="770" y="360" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>'),
    ('<path class="hot" d="M 800 306.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 800 380 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="830" y="145" width="56" height="230" fill="none" stroke="none"/>',
     '<rect class="hot" x="830" y="218" width="56" height="230" fill="none" stroke="none"/>'),
    ('<text class="hot-label" x="858" y="195" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="858" y="268" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    ('<text class="hot-label" x="858" y="280" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">o</tspan></text>',
     '<text class="hot-label" x="858" y="353" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">o</tspan></text>'),
    ('<text class="hot-label" x="858" y="365" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="858" y="438" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    # ========== 3) 源极支路：35px 水平 + 90°转角，R_S/C_S 右移 35，C_S 分支下移 30 ==========
    ('''        <g class="interactive" data-id="wire-rs-top" data-name="源极接线（源极节点→R_S）">
            <path class="hot" d="M 530 306 V 389" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rs-top" data-name="源极接线（源极节点→R_S，经 90° 转角）">
            <path class="hot" d="M 530 306 H 565 V 336" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-rs-lead" data-name="R_S 上端引线（C_S 分支点→R_S）">
            <path class="hot" d="M 565 336 V 389" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    ('<rect class="hot" x="516.5" y="389" width="27" height="53"',
     '<rect class="hot" x="551.5" y="389" width="27" height="53"'),
    ('<text class="hot-label" x="500" y="423" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>',
     '<text class="hot-label" x="535" y="423" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">S</tspan></text>'),
    ('<path class="hot" d="M 530 442 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 565 442 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('''        <g class="interactive" data-id="wire-cs-top" data-name="C_S 上端接线（源极节点—C_S）">
            <path class="hot" d="M 530 306 H 598 V 398" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-cs-top" data-name="C_S 上端接线（R_S 上端分支点—C_S）">
            <path class="hot" d="M 565 336 H 633 V 422.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="565" cy="336" r="7" fill="#ffffff" pointer-events="none"/>
        </g>'''),
    ('<line class="hot" x1="576" y1="398" x2="620" y2="398" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="611" y1="422.5" x2="655" y2="422.5" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="576" y1="414" x2="620" y2="414" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="611" y1="438.5" x2="655" y2="438.5" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="640" y="382" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">＋</text>',
     '<text class="hot-label" x="675" y="407" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">＋</text>'),
    ('<text class="hot-label" x="640" y="438" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">C<tspan class="sub">S</tspan></text>',
     '<text class="hot-label" x="675" y="463" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">C<tspan class="sub">S</tspan></text>'),
    ('<path class="hot" d="M 598 414 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 633 438.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # ========== 1) 输入通路下移到 302（与栅条底端成直角） ==========
    ('<path class="hot" d="M 110 268 H 206" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 110 302 H 206" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<circle class="hot" cx="110" cy="268" r="8"', '<circle class="hot" cx="110" cy="302" r="8"'),
    ('<line class="hot" x1="206" y1="246" x2="206" y2="290" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="206" y1="280" x2="206" y2="324" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="220" y1="246" x2="220" y2="290" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="220" y1="280" x2="220" y2="324" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="213" y="335" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>',
     '<text class="hot-label" x="213" y="369" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>'),
    ('''        <g class="interactive" data-id="wire-in-gate" data-name="输入导线（C_1—栅极节点）">
            <path class="hot" d="M 220 268 H 390" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-in-gate" data-name="输入导线（C_1—R_G 左端）">
            <path class="hot" d="M 220 302 H 363.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    # 删除 node-gate（R_G 横置后栅极节点不再存在）
    ('''        <!-- 栅极节点（输入导线 — 栅极引线 — R_G 上端接线在此交汇） -->
        <g id="node-gate" data-id="node-gate" data-name="栅极节点">
            <circle cx="390" cy="268" r="7" fill="#ffffff" pointer-events="none"/>
        </g>
''', ''),
    ('<g class="interactive" data-id="wire-gate-out" data-name="栅极引线（栅极节点—MOSFET 栅极）">\n            <path class="hot" d="M 390 268 H 502"',
     '<g class="interactive" data-id="wire-gate-out" data-name="栅极引线（R_G 右端—MOSFET 栅极）">\n            <path class="hot" d="M 416.5 302 H 502"'),
    # ========== fx 层同步 ==========
    ('<line x1="206" y1="268" x2="220" y2="268" stroke="#34d399"',
     '<line x1="206" y1="302" x2="220" y2="302" stroke="#34d399"'),
    ('<line x1="670" y1="140" x2="684" y2="140" stroke="#34d399" stroke-width="7"/>',
     '<line x1="670" y1="181.5" x2="684" y2="181.5" stroke="#34d399" stroke-width="7"/>'),
    ('<line x1="598" y1="398" x2="598" y2="414" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="633" y1="422.5" x2="633" y2="438.5" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    ('<line x1="530" y1="389" x2="530" y2="442" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="565" y1="389" x2="565" y2="442" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    ('<circle class="hot" cx="502" cy="268" r="6"', '<circle class="hot" cx="502" cy="302" r="6"'),
    ('d="M 530 140 V 189 H 554 V 193"', 'd="M 530 226.5 V 236 H 554 V 241"'),
    ('d="M 554 193 L 586 223 L 554 253 L 522 223 Z"', 'd="M 554 241 L 586 266 L 554 291 L 522 266 Z"'),
    ('d="M 554 253 V 278 H 530 V 306"', 'd="M 554 291 V 296 H 530 V 306"'),
    ('<rect class="hot" x="586" y="211" width="82" height="44"', '<rect class="hot" x="586" y="244" width="82" height="44"'),
    ('<text class="hot-label" x="590" y="243" fill="#ff5252"', '<text class="hot-label" x="590" y="276" fill="#ff5252"'),
    ('<line x1="554" y1="203" x2="554" y2="229" stroke="#ff5252" stroke-width="5"/>',
     '<line x1="554" y1="246" x2="554" y2="269" stroke="#ff5252" stroke-width="5"/>'),
    ('points="554,241 545,226 563,226"', 'points="554,284 545,269 563,269"'),
    ('<circle class="qdot" cx="502" cy="268" r="8"', '<circle class="qdot" cx="502" cy="302" r="8"'),
    ('<circle class="qdot" cx="530" cy="140" r="8"', '<circle class="qdot" cx="530" cy="226.5" r="8"'),
    # ========== 整理态 R_D 下挂件随输出节点/R_L 下移 ==========
    ('<path class="hot keepw" d="M 700 140 V 253.5"', '<path class="hot keepw" d="M 700 181.5 V 327"'),
    ('<rect class="hot" x="686.5" y="253.5" width="27" height="53"', '<rect class="hot" x="686.5" y="327" width="27" height="53"'),
    ('<path class="hot keepw" d="M 700 306.5 V 525"', '<path class="hot keepw" d="M 700 380 V 525"'),
    ('<circle cx="700" cy="140" r="7" fill="#ffffff"/>', '<circle cx="700" cy="181.5" r="7" fill="#ffffff"/>'),
    ('<text class="hot-label" x="668" y="287" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>',
     '<text class="hot-label" x="668" y="360" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>'),
    # ========== 配置：STAGE_UNITS / ANNOS / fadeWith / tidy ==========
    ("""        ['comp-vi', 'wire-vi-in', 'comp-c1', 'wire-in-gate', 'node-gate', 'wire-gate-out',
         'comp-t', 'comp-rd', 'wire-rd-top', 'node-drain', 'wire-drain-out',""",
     """        ['comp-vi', 'wire-vi-in', 'comp-c1', 'wire-in-gate', 'wire-gate-out',
         'comp-t', 'comp-rd', 'wire-rd-top', 'wire-rd-bot', 'node-drain', 'wire-rd-lead', 'wire-drain-out',"""),
    ("""         'wire-rg-top', 'comp-rg', 'wire-rg-bot',
         'comp-rs', 'wire-rs-top', 'node-source', 'wire-rs-bot',""",
     """         'comp-rg',
         'comp-rs', 'wire-rs-top', 'wire-rs-lead', 'node-source', 'wire-rs-bot',"""),
    ("""        'wire-rg-top':  { text: '栅极节点接线：栅极节点 → R<sub>G</sub> 上端',
                          parts: [{ text: '这条导线把栅极节点接到栅极电阻的上端。' }] },
""", ''),
    ("""        'wire-rg-bot':  { text: 'R<sub>G</sub> 下端接线：R<sub>G</sub> → 分压节点',
                          parts: [{ text: '这条导线把栅极电阻的下端接到分压节点。' }] },
""", ''),
    ("""        'node-gate':    { text: '栅极节点：输入导线—栅极引线—R<sub>G</sub> 上端接线在此交汇',
                          parts: [{ text: '这是栅极节点，输入导线、栅极引线和栅极电阻上端接线在这里交汇。' }] },
""", ''),
    ("""        'wire-drain-out':{ text: '漏极输出导线：漏极节点 → C<sub>2</sub>',
                          parts: [{ text: '这条导线把漏极节点接出的信号送到输出耦合电容。' }] },""",
     """        'wire-rd-lead': { text: '漏极引线：沟道上端 → 35px 水平 → 垂直向上（90° 转角）',
                          parts: [{ text: '这条导线从沟道上端向右走一小段，再垂直向上接到漏极电阻，形成直角。' }] },
        'wire-rd-bot':  { text: 'R<sub>D</sub> 下端引线：漏极节点 → R<sub>D</sub>',
                          parts: [{ text: '这条导线把漏极节点接到漏极电阻的下端。' }] },
        'wire-drain-out':{ text: '漏极输出导线：漏极节点 → C<sub>2</sub>',
                          parts: [{ text: '这条导线把漏极节点接出的信号送到输出耦合电容。' }] },"""),
    ("""        'wire-rs-top':  { text: '源极接线：源极节点 → R<sub>S</sub> 上端',""",
     """        'wire-rs-lead': { text: 'R<sub>S</sub> 上端引线：C<sub>S</sub> 分支点 → R<sub>S</sub>',
                          parts: [{ text: '这条导线把旁路电容的分支点接到源极电阻的上端。' }] },
        'wire-rs-top':  { text: '源极接线：源极节点 → 35px 水平 → 垂直向下（90° 转角）',"""),
    ("'comp-c1': ['wire-vi-in', 'comp-vi', 'wire-in-gate', 'node-gate'],",
     "'comp-c1': ['wire-vi-in', 'comp-vi', 'wire-in-gate'],"),
    ("fadeGroup('comp-rd', true); fadeGroup('wire-rd-top', true);",
     "fadeGroup('comp-rd', true); fadeGroup('wire-rd-top', true); fadeGroup('wire-rd-bot', true);"),
]

def main():
    with io.open(PATH, "r", encoding="utf-8", newline="") as f:
        s = f.read()
    bad = []
    for i, (old, new) in enumerate(PAIRS, 1):
        if old == new:
            continue  # 占位对
        n = s.count(old)
        if n != 1:
            bad.append((i, n, old[:80]))
    if bad:
        for i, n, o in bad:
            print("FAIL pair %d: count=%d  old=%r" % (i, n, o))
        sys.exit(1)
    for old, new in PAIRS:
        if old != new:
            s = s.replace(old, new)
    with io.open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("OK %d pairs applied" % len([1 for o, n in PAIRS if o != n]))

main()
