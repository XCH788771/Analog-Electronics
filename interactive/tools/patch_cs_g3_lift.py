# -*- coding: utf-8 -*-
"""cs-g3 第112轮（2026-10-29 08:45）：FET 上移20px；G极导线/C1/Vi 同步上移20、Vᵢ'－'号再下移15；
RD/C2 上移20、输出导线对齐上移；RD上端与C2-D连接处加节点。全对唯一性校验，全过才写盘。"""
import io, sys

P = "cs-g3.html"
s = io.open(P, encoding="utf-8", newline="").read()

pairs = [
    # ── A. FET 上移 20px ──
    ('<rect class="hot" x="438" y="208" width="158" height="140" fill="none" stroke="none"/>',
     '<rect class="hot" x="438" y="188" width="158" height="140" fill="none" stroke="none"/>'),
    ('<line class="hot" x1="502" y1="234" x2="502" y2="302" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="502" y1="214" x2="502" y2="282" stroke="#ffffff" stroke-width="7"/>'),
    ('<line class="hot" x1="530" y1="226.5" x2="530" y2="246" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="530" y1="206.5" x2="530" y2="226" stroke="#ffffff" stroke-width="7"/>'),
    ('<line class="hot" x1="530" y1="258" x2="530" y2="274" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="530" y1="238" x2="530" y2="254" stroke="#ffffff" stroke-width="7"/>'),
    ('<line class="hot" x1="530" y1="286" x2="530" y2="302" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="530" y1="266" x2="530" y2="282" stroke="#ffffff" stroke-width="7"/>'),
    ('points="530,266 554,252 554,280"',
     'points="530,246 554,232 554,260"'),
    ('<path class="hot" d="M 554 266 H 578 V 294" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 554 246 H 578 V 274" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="482" y="328" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">g</text>',
     '<text class="hot-label" x="482" y="308" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">g</text>'),
    ('<text class="hot-label" x="592" y="214" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>',
     '<text class="hot-label" x="592" y="194" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">d</text>'),
    ('<text class="hot-label" x="592" y="330" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>',
     '<text class="hot-label" x="592" y="310" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">s</text>'),
    ('<text class="hot-label" x="592" y="280" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">B</text>',
     '<text class="hot-label" x="592" y="260" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">B</text>'),
    # ── B. 源极支路：S 引线随 FET 上移（分支点 341.5 以下不动）──
    ('<path class="hot" d="M 530 294 H 578 V 341.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 530 274 H 578 V 341.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # ── C. 栅极支路：wire-rg1b 拆段（交叉点 282 变端点防误判）+ 输入线上移 ──
    ('''        <g class="interactive" data-id="wire-rg1b" data-name="R_G1 下端接线（→分压节点）">
            <path class="hot" d="M 250 221.5 V 302" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rg1b" data-name="R_G1 下端接线·上段（→与输入导线交叉处）">
            <path class="hot" d="M 250 221.5 V 282" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-rg1b2" data-name="R_G1 下端接线·下段（与输入导线交叉不连通）">
            <path class="hot" d="M 250 282 V 302" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>'''),
    ('<path class="hot" d="M 195 302 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 195 282 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('''        <g class="interactive" data-id="wire-rg-drop" data-name="R_G 接线·下引段（栅极引线—R_G 右端，下引 50px 后 90° 转角向左）">
            <path class="hot" d="M 390 302 V 352 H 346.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="390" cy="302" r="7" fill="#ffffff" pointer-events="none"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rg-drop" data-name="R_G 接线·下引段（栅极引线—R_G 右端，下引 70px 后 90° 转角向左）">
            <path class="hot" d="M 390 282 V 352 H 346.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="390" cy="282" r="7" fill="#ffffff" pointer-events="none"/>
        </g>'''),
    # ── D. Vᵢ / C1 上移 20，Vᵢ '－' 号净上移 5（先 20 后回 15）──
    ('<path class="hot" d="M 110 302 H 181" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 110 282 H 181" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<circle class="hot" cx="110" cy="302" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>',
     '<circle class="hot" cx="110" cy="282" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>'),
    ('<text class="hot-label" x="110" y="354" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="110" y="334" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    ('<text class="hot-label" x="110" y="414" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>',
     '<text class="hot-label" x="110" y="394" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>'),
    ('<text class="hot-label" x="110" y="474" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="110" y="459" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    ('<line class="hot" x1="181" y1="280" x2="181" y2="324" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="181" y1="260" x2="181" y2="304" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="195" y1="280" x2="195" y2="324" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="195" y1="260" x2="195" y2="304" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="188" y="369" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>',
     '<text class="hot-label" x="188" y="349" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">1</tspan></text>'),
    ('<line x1="181" y1="302" x2="195" y2="302" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="181" y1="282" x2="195" y2="282" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    # ── E. 漏极支路：RD/C2 上移 20 + 两处新节点 ──
    ('''        <g class="interactive" data-id="wire-rd-top" data-name="R_D 上端接线（→电源轨）">
            <path class="hot" d="M 578 5 V 83.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-rd-top" data-name="R_D 上端接线（→电源轨，T 交汇处有节点）">
            <path class="hot" d="M 578 5 V 63.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="578" cy="5" r="7" fill="#ffffff" pointer-events="none"/>
        </g>'''),
    ('<rect class="hot" x="564.5" y="83.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="564.5" y="63.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="548" y="117" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>',
     '<text class="hot-label" x="548" y="97" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>'),
    ('<path class="hot" d="M 530 236.25 H 578 V 181.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 530 216.25 H 578 V 161.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 578 181.5 V 136.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 578 161.5 V 116.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('''        <g class="interactive" data-id="wire-drain-out" data-name="漏极输出导线（漏极输出节点—C_2）">
            <path class="hot" d="M 578 181.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>''',
     '''        <g class="interactive" data-id="wire-drain-out" data-name="漏极输出导线（漏极输出节点—C_2，分支点有节点）">
            <path class="hot" d="M 578 161.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="578" cy="161.5" r="7" fill="#ffffff" pointer-events="none"/>
        </g>'''),
    ('<line class="hot" x1="670" y1="159.5" x2="670" y2="203.5" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="670" y1="139.5" x2="670" y2="183.5" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line class="hot" x1="684" y1="159.5" x2="684" y2="203.5" stroke="#ffffff" stroke-width="3.5"/>',
     '<line class="hot" x1="684" y1="139.5" x2="684" y2="183.5" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<text class="hot-label" x="677" y="144" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">2</tspan></text>',
     '<text class="hot-label" x="677" y="124" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">2</tspan></text>'),
    ('<path class="hot" d="M 684 181.5 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 684 161.5 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 800 181.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 800 161.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line x1="670" y1="181.5" x2="684" y2="181.5" stroke="#34d399" stroke-width="7"/>',
     '<line x1="670" y1="161.5" x2="684" y2="161.5" stroke="#34d399" stroke-width="7"/>'),
    ('<path class="hot keepw" d="M 700 181.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot keepw" d="M 700 161.5 V 327" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<circle cx="700" cy="181.5" r="7" fill="#ffffff"/>',
     '<circle cx="700" cy="161.5" r="7" fill="#ffffff"/>'),
    # ── F. fx-tmodel 与问答红点随动 ──
    ('<circle class="hot" cx="502" cy="302" r="6" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>',
     '<circle class="hot" cx="502" cy="282" r="6" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>'),
    ('<circle class="qdot" cx="502" cy="302" r="8" fill="#ff5252"/>',
     '<circle class="qdot" cx="502" cy="282" r="8" fill="#ff5252"/>'),
    ('<path class="hot keepw" d="M 530 236.25 V 240 H 554" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot keepw" d="M 530 216.25 V 220 H 554" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 554 240 L 586 265 L 554 290 L 522 265 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 554 220 L 586 245 L 554 270 L 522 245 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot keepw" d="M 554 290 V 294 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot keepw" d="M 554 270 V 274 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="586" y="244" width="82" height="44" fill="none" stroke="none"/>',
     '<rect class="hot" x="586" y="224" width="82" height="44" fill="none" stroke="none"/>'),
    ('<text class="hot-label" x="590" y="276" fill="#ff5252"',
     '<text class="hot-label" x="590" y="256" fill="#ff5252"'),
    ('<line x1="554" y1="245" x2="554" y2="268" stroke="#ff5252" stroke-width="5"/>',
     '<line x1="554" y1="225" x2="554" y2="248" stroke="#ff5252" stroke-width="5"/>'),
    ('<polygon points="554,283 545,268 563,268" fill="#ff5252" stroke="none"/>',
     '<polygon points="554,263 545,248 563,248" fill="#ff5252" stroke="none"/>'),
    ('<circle class="qdot" cx="530" cy="236.25" r="8" fill="#ff5252"/>',
     '<circle class="qdot" cx="530" cy="216.25" r="8" fill="#ff5252"/>'),
    ('<circle class="qdot" cx="530" cy="294" r="8" fill="#ff5252"/>',
     '<circle class="qdot" cx="530" cy="274" r="8" fill="#ff5252"/>'),
    # ── G. 注释坐标同步 ──
    ('等效布局：G 端子留在栅极引线末端 (502,268)（G-S 开路，不画支路）；',
     '等效布局：G 端子留在栅极引线末端 (502,282)（G-S 开路，不画支路）；'),
    ('D-S 受控源支路直连沟道 d 段中点 (530,236.25) 与 s 段中点 (530,294)，菱形符号居中 (554,265)；',
     'D-S 受控源支路直连沟道 d 段中点 (530,216.25) 与 s 段中点 (530,274)，菱形符号居中 (554,245)；'),
    ('G 在栅极引线末端 (502,302)，D 在沟道 d 段中点 (530,236.25)，S 在沟道 s 段中点 (530,294) -->',
     'G 在栅极引线末端 (502,282)，D 在沟道 d 段中点 (530,216.25)，S 在沟道 s 段中点 (530,274) -->'),
    # ── H. 配置区：STAGE_UNITS / ANNOS / fadeGroup 注册 wire-rg1b2，下引段 50→70 ──
    ("'wire-rg1a', 'comp-rg1', 'wire-rg1b', 'node-div', 'wire-rg2a', 'comp-rg2', 'wire-rg2b',",
     "'wire-rg1a', 'comp-rg1', 'wire-rg1b', 'wire-rg1b2', 'node-div', 'wire-rg2a', 'comp-rg2', 'wire-rg2b',"),
    ('''        'wire-rg1b':    { text: 'R<sub>G1</sub> 下端接线：R<sub>G1</sub> → 分压节点',
                          parts: [{ text: '这条导线把上偏置电阻的下端接到分压节点。' }] },''',
     '''        'wire-rg1b':    { text: 'R<sub>G1</sub> 下端接线·上段：R<sub>G1</sub> → 交叉处',
                          parts: [{ text: '这条导线把上偏置电阻的下端接到分压节点方向，途中与输入导线交叉但没有连在一起。' }] },
        'wire-rg1b2':   { text: 'R<sub>G1</sub> 下端接线·下段：交叉处 → 分压节点',
                          parts: [{ text: '这段导线继续把上偏置电阻的下端接到分压节点。' }] },'''),
    ("fadeGroup('comp-rg1', true); fadeGroup('wire-rg1a', true); fadeGroup('wire-rg1b', true);",
     "fadeGroup('comp-rg1', true); fadeGroup('wire-rg1a', true); fadeGroup('wire-rg1b', true); fadeGroup('wire-rg1b2', true);"),
    ("text: 'R<sub>G</sub> 接线·下引段：栅极引线 → 下引 50px → 90° 转角向左',",
     "text: 'R<sub>G</sub> 接线·下引段：栅极引线 → 下引 70px → 90° 转角向左',"),
    ('parts: [{ text: \'这条接线从栅极引线向下引50像素，再向左转弯，栅极电阻就串在这一段水平导线上。\' }] },',
     'parts: [{ text: \'这条接线从栅极引线向下引70像素，再向左转弯，栅极电阻就串在这一段水平导线上。\' }] },'),
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
