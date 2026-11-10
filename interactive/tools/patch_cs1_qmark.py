# -*- coding: utf-8 -*-
"""cs-g1 四项修订：
① TTS 语音稿「栅」→「山」（shān 一声；只改 parts/announce 语音串，屏显不动）。
② 移除 i_D 文字；电流箭头右移 25px（x 486→511，脱离 D 极导线）、杆 20→42px、头部 16×15→22×23。
③ I_DQ 标注上移至箭头水平同轴（基线 y=215），文字左缘距箭头 25px（x=536）。
④ q-vth 显示改为 V_GSQ（＋/V_GSQ/－ 竖排柱，G–S 之间）；新增 q-vdsq（＋/V_DSQ/－ 竖排柱，D–S 之间）；
   I_DO 右移 32px 让位；qlabels +q-vdsq；ANNOS 增 q-vdsq、改 q-vth/q-idq。
唯一性校验：任一 old 串出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html'))
BAK = '/tmp/cs-g1.before-qmark.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

REPS = [
    # ---- ② 电流箭头：右移 25px + 加长 + 头加大；移除 i_D 文字 ----
    ('<line x1="486" y1="186" x2="486" y2="206" stroke="#ff5252" stroke-width="5"/>',
     '<line x1="511" y1="172" x2="511" y2="214" stroke="#ff5252" stroke-width="5"/>'),
    ('<polygon points="486,220 478,205 494,205" fill="#ff5252" stroke="none"/>',
     '<polygon points="511,238 500,215 522,215" fill="#ff5252" stroke="none"/>'),
    ('            <text x="548" y="204" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">i<tspan class="sub">D</tspan></text>\n',
     ''),
    ('data-name="漏极接线（漏极节点—T 漏极；i_D 为漏极直流电流）"',
     'data-name="漏极接线（漏极节点—T 漏极；红色箭头指示漏极电流方向）"'),
    ('<!-- 漏极支路：R_d → 漏极节点 → T 漏极；i_D 箭头标注漏极直流电流；节点右侧直接引出 v_o -->',
     '<!-- 漏极支路：R_d → 漏极节点 → T 漏极；红色箭头指示漏极电流（I_DQ 见第 2 关标注）；节点右侧直接引出 v_o -->'),

    # ---- ③ I_DQ 上移到箭头同轴 ----
    ('''                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ">
                    <rect class="hot" x="560" y="414" width="96" height="52" fill="none" stroke="none"/>
                    <text class="hot-label" x="608" y="448" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">I<tspan class="sub">DQ</tspan></text>
                </g>''',
     '''                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ（漏极电流箭头处）">
                    <rect class="hot" x="530" y="183" width="100" height="42" fill="none" stroke="none"/>
                    <text class="hot-label" x="536" y="215" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">I<tspan class="sub">DQ</tspan></text>
                </g>
                <g class="interactive" data-id="q-vdsq" data-name="漏源静态电压 V_DSQ（＋/− 标出极性）">
                    <rect class="hot" x="498" y="230" width="90" height="108" fill="none" stroke="none"/>
                    <text class="hot-label" x="545" y="258" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="545" y="294" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">DSQ</tspan></text>
                    <text class="hot-label" x="545" y="330" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>'''),

    # ---- ④ q-vth → V_GSQ 竖排柱 ----
    ('''                <g class="interactive" data-id="q-vth" data-name="开启电压 V_GS(th)">
                    <rect class="hot" x="548" y="342" width="120" height="52" fill="none" stroke="none"/>
                    <text class="hot-label" x="608" y="376" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GS(th)</tspan></text>
                </g>''',
     '''                <g class="interactive" data-id="q-vth" data-name="栅源静态电压 V_GSQ（＋/− 标出极性）">
                    <rect class="hot" x="498" y="346" width="90" height="108" fill="none" stroke="none"/>
                    <text class="hot-label" x="545" y="374" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="545" y="410" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GSQ</tspan></text>
                    <text class="hot-label" x="545" y="446" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>'''),

    # I_DO 右移 32px 让位
    ('<rect class="hot" x="560" y="270" width="96" height="52" fill="none" stroke="none"/>',
     '<rect class="hot" x="592" y="270" width="96" height="52" fill="none" stroke="none"/>'),
    ('<text class="hot-label" x="608" y="304" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">I<tspan class="sub">DO</tspan></text>',
     '<text class="hot-label" x="640" y="304" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">I<tspan class="sub">DO</tspan></text>'),

    # qlabels 增 q-vdsq
    ("qlabels: ['q-ido', 'q-vth', 'q-idq'],",
     "qlabels: ['q-ido', 'q-vth', 'q-idq', 'q-vdsq'],"),

    # ---- ANNOS：q-vth / q-idq 改写 + 新增 q-vdsq ----
    ("""        'q-vth':        { text: '<b>V<sub>GS(th)</sub></b><br>增强型 MOS 管的开启电压：v<sub>GS</sub> 超过它之后导电沟道才形成',
                          parts: [{ text: '这是V GS th，增强型场效应管的开启电压，栅源电压超过它之后导电沟道才形成。' }] },""",
     """        'q-vth':        { text: '<b>V<sub>GSQ</sub></b>（＋/−）<br>栅源静态电压：由 R<sub>g1</sub>、R<sub>g2</sub> 分压决定，＋在 G、−在 S 标出极性',
                          parts: [{ text: '这是V GSQ，山源之间的静态电压，由RG1和RG2分压决定，图中加号在山极、减号在源极，标出它的极性。' }] },"""),
    ("""        'q-idq':        { text: '<b>I<sub>DQ</sub></b><br>静态漏极电流：由转移特性方程代入 V<sub>GSQ</sub> 求得',
                          parts: [{ text: '这是IDQ，静态漏极电流，由转移特性方程代入栅源静态电压求得。' }] },""",
     """        'q-idq':        { text: '<b>I<sub>DQ</sub></b><br>静态漏极电流：即漏极导线上红色箭头所示的电流，由转移特性方程代入 V<sub>GSQ</sub> 求得',
                          parts: [{ text: '这是IDQ，静态漏极电流，即漏极导线上红色箭头所示的电流，由转移特性方程代入山源静态电压求得。' }] },
        'q-vdsq':       { text: '<b>V<sub>DSQ</sub></b>（＋/−）<br>漏源静态电压：V<sub>DSQ</sub> = V<sub>DD</sub> − I<sub>DQ</sub>R<sub>d</sub>，＋在 D、−在 S 标出极性',
                          parts: [{ text: '这是V DSQ，漏源静态电压，等于V DD减去IDQ乘RD，图中加号在漏极、减号在源极，标出它的极性。' }] },"""),

    # ---- ① 语音稿「栅」→「山」（shān 一声） ----
    ("parts: [{ text: '这是上偏置电阻RG1。它和下偏置电阻RG2串联分压，把栅极电位基本固定住，使静态工作点稳定。' }]",
     "parts: [{ text: '这是上偏置电阻RG1。它和下偏置电阻RG2串联分压，把山极电位基本固定住，使静态工作点稳定。' }]"),
    ("parts: [{ text: 'RG1的下端，接到栅极节点。' }]",
     "parts: [{ text: 'RG1的下端，接到山极节点。' }]"),
    ("parts: [{ text: '这是栅极节点。分压电路、耦合电容Cb1和场效应管的栅极，都在这里相连。' }]",
     "parts: [{ text: '这是山极节点。分压电路、耦合电容Cb1和场效应管的山极，都在这里相连。' }]"),
    ("parts: [{ text: '这是下偏置电阻RG2。它一端接栅极节点，一端接地，和RG1一起决定栅极电位。' }]",
     "parts: [{ text: '这是下偏置电阻RG2。它一端接山极节点，一端接地，和RG1一起决定山极电位。' }]"),
    ("parts: [{ text: '这是场效应管，放大电路的核心。它是电压控制电流器件，栅极几乎不取电流，漏极电流受栅源电压控制。衬底B和源极连在一起。微变等效时，栅源之间开路，漏源之间等效为一个受控电流源。' }]",
     "parts: [{ text: '这是场效应管，放大电路的核心。它是电压控制电流器件，山极几乎不取电流，漏极电流受山源电压控制。衬底B和源极连在一起。微变等效时，山源之间开路，漏源之间等效为一个受控电流源。' }]"),
    ("parts: [{ text: '这是输入端口。放大电路的输入电压，从这里经过耦合电容Cb1，送到栅极。' }]",
     "parts: [{ text: '这是输入端口。放大电路的输入电压，从这里经过耦合电容Cb1，送到山极。' }]"),
    ("parts: [{ text: '这是输入耦合电容Cb1。隔直流、通交流，让交流信号进入栅极，又不影响直流偏置。' }]",
     "parts: [{ text: '这是输入耦合电容Cb1。隔直流、通交流，让交流信号进入山极，又不影响直流偏置。' }]"),
    ("parts: [{ text: '这是IDO，增强型场效应管的转移特性参数，是栅源电压等于两倍开启电压时的漏极电流。' }]",
     "parts: [{ text: '这是IDO，增强型场效应管的转移特性参数，是山源电压等于两倍开启电压时的漏极电流。' }]"),
    ("announce: '进入第二关，估算静态工作点。依次完成栅源电压、漏极电流、漏源电压三个指标：每个指标先选择计算框架，再点虚线框，点击电路中对应的元件或电量标注填入符号，共24分。'",
     "announce: '进入第二关，估算静态工作点。依次完成山源电压、漏极电流、漏源电压三个指标：每个指标先选择计算框架，再点虚线框，点击电路中对应的元件或电量标注填入符号，共24分。'"),
]

fail = False
for i, (old, new) in enumerate(REPS, 1):
    n = s.count(old)
    if n != 1:
        print('[FAIL] 第%d处 old 出现 %d 次（须为1）: %r' % (i, n, old[:70]))
        fail = True
if fail:
    print('中止：未写盘')
    sys.exit(1)

for old, new in REPS:
    s = s.replace(old, new, 1)

shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('OK %d 处替换完成，长度 %d → %d，备份 %s' % (len(REPS), len(orig), len(s), BAK))
