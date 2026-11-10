# -*- coding: utf-8 -*-
"""cs-g1.html 电路重绘（2026-10-27，用户原图：单电源分压式偏置共源·案例1）

正确电路（用户截图）：
  +V_DD(5V) 顶轨 → R_g1 60kΩ / R_d 3.9kΩ 上端；R_d 下端=漏极节点 d
  漏极节点 → 右横线直接引出 v_o（无输出耦合电容）；漏极支路标 i_D 箭头
  R_g1/R_g2(40kΩ) 分压接栅极节点；C_b1 耦合 v_i 输入；源极 s 直落公共地线（无 R_s）
  衬底 B 引线折下接源极；单电源、接地符号在底轨中部
  删除：−V_SS、R_s、R_si、V_s、C_b2

闯关（三关 18+22+60=100）：
  L1 直流通路 draw=18：v_i 置零短路 / V_DD 保留 / C_b1 断路（3 目标×6）
  L2 交流微变等效 draw=22：v_i 保留 / V_DD 置零接地 / C_b1 短路（3×6=18）+ 等效四问池 tquizPool=4
  L3 动态指标 mix=60：框架 6×3=18 + 填空 8/8/8/8/10（Av=−gm·Rd、Ri=Rg1∥Rg2、Ro≈Rd）

用法：python tools/_rebuild_cs1_v2.py   （对 cs-g1.html 原地重建，可重复执行=幂等）
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(os.path.dirname(HERE), 'cs-g1.html')


def between(s, a, b):
    i = s.index(a)
    j = s.index(b, i)
    return s[i:j]


def rep(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        print('!! rep[%s] 命中 %d 次（应为 1），中止' % (tag, n))
        sys.exit(1)
    return s.replace(old, new)


src = io.open(P, encoding='utf-8', newline='').read()

# ---------- 从现文件提取复用块（保证 comp-t 符号等逐字节原样） ----------
SEG_BIAS = between(src, '        <!-- 上偏置电阻 R_g1', '        <!-- 场效应管 T')          # rg1/gate/rg2 全段
SEG_T = between(src, '        <!-- 场效应管 T（N沟道增强型 MOS）', '\n\n        <!-- 漏极支路')
SEG_VI = between(src, '        <!-- 输入端口 V_i（两枚端子', '        <!-- 输入耦合电容 C_b1')
SEG_CB1 = between(src, '        <!-- 输入耦合电容 C_b1', '\n\n        <!-- 输出回路')
SEG_FXCB1 = between(src, '            <!-- 电容短路桥（交流通路） -->', '            <g id="fx-cb2"')
SEG_FXVI = between(src, '            <!-- 输入端口短接桥', '            <!-- V_DD 置零接地')
SEG_QLBL = between(src, '            <!-- ====== 电量标注层', '            <!-- 场效应管微变等效模型')
SEG_TMODEL = between(src, '            <!-- 场效应管微变等效模型', '\n\n            <!-- ====== 整理电路层')
SEG_RARR1 = between(src, '            <g id="rarr-rg1"', '            <!-- R_d：从漏极导线')
SEG_RARRD = between(src, '            <g id="rarr-rd"', '            </g>\n\n            <!-- ===== 交流等效最终态层')
SEG_EQRG1 = between(src, '                <!-- R_g1（上移：体 315-405） -->', '                <!-- R_g2（上移：体 315-405）')
SEG_EQRG2 = between(src, '                <!-- R_g2（上移：体 315-405）', '                <!-- 源极横线')
SEG_DOTS = between(src, '            <!-- 场效应管等效问答的端点红点', '        </g>\n\n</g>') + '        </g>\n\n</g>\n'

# rarr-rd 注释里的旧坐标描述同步更新
SEG_RARRD = SEG_RARRD.replace('x=640，C_b2 短接桥 670-684 左侧，与输出并联', 'x=640，输出端子 v_o（700）左侧，与输出并联')

# 电阻值标注（按用户原图：R_g1 60kΩ / R_g2 40kΩ / R_d 3.9kΩ）注入偏置电阻组
LBL_RG1 = '            <text class="hot-label" x="288" y="147" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">g1</tspan></text>'
assert SEG_BIAS.count(LBL_RG1) == 1
SEG_BIAS = SEG_BIAS.replace(LBL_RG1, LBL_RG1 +
    '\n            <text x="346" y="130" fill="rgba(255,255,255,0.85)" font-size="28" font-weight="bold" text-anchor="start">60kΩ</text>')
LBL_RG2 = '            <text class="hot-label rg2-label" x="290" y="402" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">g2</tspan></text>'
assert SEG_BIAS.count(LBL_RG2) == 1
SEG_BIAS = SEG_BIAS.replace(LBL_RG2, LBL_RG2 +
    '\n            <text x="346" y="432" fill="rgba(255,255,255,0.85)" font-size="28" font-weight="bold" text-anchor="start">40kΩ</text>')

# ---------- 新电路 SVG（替换区 B） ----------
NEW_B = '''        <!-- ▼▼▼ 替换区 B
        <!-- ====== ① 电路区：单电源分压式偏置共源放大电路（2026-10-27 按用户原图重绘）
             +V_DD(5V) — R_g1 60k / R_g2 40k 分压 — C_b1 耦合输入 v_i — N 沟道 MOS 管 T（衬底 B 接源极）
             — 源极直落地 — R_d 3.9k — 漏极直接引出 v_o（无输出耦合电容、无源极电阻） ====== -->
        <g id="circuit-wrap" transform="translate(18, 260) scale(1)">
        <!-- 电源端 +VDD（右上端子；标注在右侧两行：V_DD / (5V)） -->
        <g class="interactive" data-id="comp-vdd" data-name="直流电源端 +VDD（交流分析中置零接地）">
            <circle class="hot" cx="700" cy="5" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
            <text class="hot-label vdd-label" x="726" y="-6" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">V<tspan class="sub">DD</tspan></text>
            <text class="hot-label vdd-label" x="726" y="34" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="start">(5V)</text>
        </g>
        <!-- 顶部电源导轨（R_g1 上端 — R_d 上端）与 +VDD 端子接线 -->
        <g class="interactive" data-id="wire-vdd-rail" data-name="电源导线（R_g1上端—R_d上端）">
            <path class="hot" d="M 320 5 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-vdd-ext" data-name="电源导线（R_d上端—+VDD端子）">
            <path class="hot" d="M 486 5 H 692" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <!-- R_d 上端节点（顶部电源轨与 +VDD 导线的交汇点） -->
        <g id="node-rd-top" data-id="node-rd-top" data-name="R_d 上端节点（电源轨交汇点）">
            <circle cx="486" cy="5" r="7" fill="#ffffff" pointer-events="none"/>
        </g>

__SEG_BIAS__
__SEG_T__
        <!-- 漏极支路：R_d → 漏极节点 → T 漏极；i_D 箭头标注漏极直流电流；节点右侧直接引出 v_o -->
        <g class="interactive" data-id="wire-d-stub" data-name="漏极接线（漏极节点—T 漏极；i_D 为漏极直流电流）">
            <path class="hot" d="M 486 178 V 236" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <line x1="486" y1="196" x2="486" y2="216" stroke="#ff5252" stroke-width="5"/>
            <polygon points="486,230 478,215 494,215" fill="#ff5252" stroke="none"/>
            <text x="548" y="214" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">i<tspan class="sub">D</tspan></text>
        </g>
        <g id="node-drain" data-id="node-drain" data-name="漏极节点">
            <circle cx="486" cy="178" r="7" fill="#ffffff" pointer-events="none"/>
        </g>
        <g class="interactive" data-id="wire-vo" data-name="输出导线（漏极节点→输出端子 v_o，直接引出）">
            <path class="hot" d="M 486 178 H 692" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-rd-a" data-name="R_d 下端接线（R_d→漏极节点）">
            <path class="hot" d="M 486 140 V 178" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="comp-rd" data-name="漏极电阻 R_d（3.9kΩ）">
            <rect class="hot" x="468" y="60" width="36" height="80" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <text class="hot-label" x="454" y="108" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">d</tspan></text>
            <text x="514" y="146" fill="rgba(255,255,255,0.85)" font-size="28" font-weight="bold" text-anchor="start">3.9kΩ</text>
        </g>
        <g class="interactive" data-id="wire-rd-top" data-name="R_d 上端接线（→电源轨）">
            <path class="hot" d="M 486 60 V 5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>

        <!-- 源极支路：T 源极直落公共地线（本案例无源极电阻） -->
        <g class="interactive" data-id="wire-src-a" data-name="源极接线（T 源极→公共地线）">
            <path class="hot" d="M 486 294 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>

        <!-- 公共地线：输入段（v_i 负端子—R_g2 下端；随 C_b1 断路移除）+ 主段（R_g2 下端—源极落点）+ 接地符号 -->
        <g class="interactive" data-id="wire-gnd-l1" data-name="公共地线·输入段（V_i 负端子—R_g2 下端）">
            <path class="hot" d="M 150 525 H 320" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
        <g class="interactive" data-id="wire-gnd-m" data-name="公共地线·主段（R_g2 下端—源极落点）">
            <path class="hot" d="M 320 525 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="320" cy="525" r="7" fill="#ffffff" pointer-events="none"/>
        </g>
        <g class="interactive" data-id="comp-gnd" data-name="接地（电位参考点）">
            <line class="hot" x1="403" y1="525" x2="403" y2="543" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="375" y1="543" x2="431" y2="543" stroke="#ffffff" stroke-width="3.5"/>
            <line class="hot" x1="385" y1="551" x2="421" y2="551" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="393" y1="559" x2="413" y2="559" stroke="#ffffff" stroke-width="2.5"/>
        </g>

        <!-- 输入回路：输入端口 v_i → C_b1 耦合 → 栅极 -->
        <g class="interactive" data-id="wire-vi-top" data-name="输入导线（V_i 正端子—C_b1 左板）">
            <path class="hot" d="M 158 295 H 206" fill="none" stroke="#ffffff" stroke-width="3.5"/>
        </g>
__SEG_VI__
__SEG_CB1__
        <!-- 输出：v_o 端子（自漏极节点直接引出，本案例无输出耦合电容） -->
        <g class="interactive" data-id="comp-vo" data-name="输出电压 v_o（取自漏极，与输入反相）">
            <circle class="hot" cx="700" cy="178" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
            <text class="hot-label" x="726" y="186" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="start">v<tspan class="sub">o</tspan></text>
        </g>

        <!-- ====== 关卡特效层（绘制关的变换动画；默认隐藏，引擎控制显隐） ====== -->
        <g id="fx-layer" pointer-events="none">
__SEG_FXCB1__
__SEG_FXVI__
            <!-- V_DD 置零接地（端子下方画接地符号） -->
            <g id="fx-vdd" opacity="0">
                <line x1="700" y1="23" x2="700" y2="39" stroke="#34d399" stroke-width="5"/>
                <line x1="672" y1="39" x2="728" y2="39" stroke="#34d399" stroke-width="5"/>
                <line x1="686" y1="51" x2="714" y2="51" stroke="#34d399" stroke-width="4.5"/>
                <line x1="694" y1="63" x2="706" y2="63" stroke="#34d399" stroke-width="4"/>
            </g>
__SEG_QLBL__
__SEG_TMODEL__

            <!-- ====== 整理电路层（交流等效专用态：R_g1、R_d 上端的地下移并入地轨，电阻翻转下挂）
                 与默认态互斥，故放在 fx-layer 内不参与布局静态检查，以截图目检把关 ====== -->
            <g id="rearr-layer">
__SEG_RARR1__
            <!-- R_d：从漏极导线（y=178）下挂到地轨（x=640，输出端子 v_o（700）左侧，与输出并联）；
                 电阻体 y 315-405。整理态与等效态共用此件（等效后位置不变）。标签放电阻体右侧 -->
__SEG_RARRD__
            </g>

            <!-- ===== 交流等效最终态层（第2关「等效场效应管」时启用，与默认/整理态互斥） =====
                 栅极输入线上升到 y=178 与漏极导线对齐（止于 g 节点=开路）；v_i 端子与 R_g1/R_g2 随之上移；
                 R_d 保持整理态下挂位（x=640）；源极经横线 y=420 接受控源下端（530）后直落地轨（486,525） -->
            <g id="eq-layer" opacity="0" pointer-events="none">
                <!-- 栅极输入主线（与漏极导线同高，右端止于 g 节点=开路） -->
                <path d="M 150 178 H 420" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <!-- 漏极横导线（等效段）：左端即交流等效的 d 节点 x=530（受控源支路挂点），向右到 v_o 端子（692） -->
                <path d="M 530 178 H 692" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <!-- C_b1 短接桥（随线上移） -->
                <line x1="206" y1="178" x2="220" y2="178" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>
                <!-- 输入端口 v_i（上端子随线上移，下端子仍接地线） -->
                <circle cx="150" cy="178" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
                <circle cx="150" cy="525" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
                <text x="150" y="290" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>
                <text x="150" y="360" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">v<tspan class="sub">i</tspan></text>
                <text x="150" y="430" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>
__SEG_EQRG1__
__SEG_EQRG2__
                <!-- 源极线：受控源下端（530,420）←→ 源极落点（486,420）→ 直落地轨（本案例无 R_s） -->
                <path d="M 486 525 V 420 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            </g>

__SEG_DOTS__
        <!-- ▲▲▲ 替换区 B 结束 ▲▲▲ -->
'''
NEW_B = (NEW_B.replace('__SEG_BIAS__', SEG_BIAS)
              .replace('__SEG_T__', SEG_T)
              .replace('__SEG_VI__', SEG_VI)
              .replace('__SEG_CB1__', SEG_CB1)
              .replace('__SEG_FXCB1__', SEG_FXCB1)
              .replace('__SEG_FXVI__', SEG_FXVI)
              .replace('__SEG_QLBL__', SEG_QLBL)
              .replace('__SEG_TMODEL__', SEG_TMODEL)
              .replace('__SEG_RARR1__', SEG_RARR1)
              .replace('__SEG_RARRD__', SEG_RARRD)
              .replace('__SEG_EQRG1__', SEG_EQRG1)
              .replace('__SEG_EQRG2__', SEG_EQRG2)
              .replace('__SEG_DOTS__', SEG_DOTS))
# 清理模板占位注释行
NEW_B = NEW_B.replace('<!-- __SEG_BIAS__ -->\n', '')

# ---------- ① 整块替换区 B ----------
B_START = '        <!-- ▼▼▼ 替换区 B'
B_END = '        <!-- ▲▲▲ 替换区 B 结束 ▲▲▲ -->\n'
i = src.index(B_START)
j = src.index(B_END, i) + len(B_END)
src = src[:i] + NEW_B + src[j:]
print('① 替换区 B（电路 SVG）完成')

# ---------- ② 标题区（zone-A）案例行 + 已知行 + <title> + 头部注释 ----------
src = rep(src,
    '        <text x="70" y="172" fill="rgba(255,255,255,0.85)" font-size="36">案例3：双电源分压偏置共源 · 求动态性能指标</text>',
    '        <text x="70" y="172" fill="rgba(255,255,255,0.85)" font-size="36">案例1：分压式偏置共源 · 画交流小信号等效电路，求 A_v、R_i、R_o</text>',
    '案例行')
src = rep(src,
    '        <text x="70" y="210" fill="rgba(255,255,255,0.6)" font-size="26">已知：g<tspan class="sub">m</tspan>、R<tspan class="sub">g1</tspan>、R<tspan class="sub">g2</tspan>、R<tspan class="sub">d</tspan>、R<tspan class="sub">s</tspan>、R<tspan class="sub">si</tspan>、V<tspan class="sub">DD</tspan>、−V<tspan class="sub">SS</tspan></text>',
    '        <text x="70" y="210" fill="rgba(255,255,255,0.6)" font-size="26">已知：g<tspan class="sub">m</tspan>、R<tspan class="sub">g1</tspan>=60kΩ、R<tspan class="sub">g2</tspan>=40kΩ、R<tspan class="sub">d</tspan>=3.9kΩ、V<tspan class="sub">DD</tspan>=5V</text>',
    '已知行')
src = rep(src,
    '<title>双电源分压偏置共源放大 · 闯关挑战（案例3）- 游戏交互</title>',
    '<title>分压式偏置共源放大 · 闯关挑战（案例1）- 游戏交互</title>',
    'title')
src = rep(src, '（cs-g1：2）', '（cs-g1 三关：2）', 'nStatic注释')
print('② 标题/已知行完成')

# ---------- ③ ANNOS 整块重写 ----------
A_START = '    const ANNOS = {'
A_END = '    };\n\n    function showAnno'
i = src.index(A_START)
j = src.index(A_END, i)
NEW_ANNOS = '''    const ANNOS = {
        'comp-vdd':     { text: '<b>直流电源 +V<sub>DD</sub>（5V）</b><br>为电路提供能量，是静态工作点与输出信号的能量来源；交流分析中视为对地短路（置零）',
                          parts: [{ text: '这是直流电源，5伏。它为整个放大电路提供能量，静态工作点和输出信号的能量都由它提供。' }] },
        'wire-vdd-rail':{ text: '电源导线：+V<sub>DD</sub> 接 R<sub>g1</sub> 上端与 R<sub>d</sub> 上端',
                          parts: [{ text: '这条导线把电源接到上偏置电阻RG1和漏极电阻Rd的上端。' }] },
        'wire-vdd-ext': { text: '电源导线：R<sub>d</sub> 上端 → +V<sub>DD</sub> 端子',
                          parts: [{ text: '电源正极经过这条导线，接到漏极电阻Rd的上端。' }] },
        'node-rd-top':  { text: 'R<sub>d</sub> 上端节点：顶部电源轨与 +V<sub>DD</sub> 导线的交汇点',
                          parts: [{ text: '这是漏极电阻Rd上端的节点，顶部电源轨和电源导线在这里交汇。' }] },
        'wire-rg1a':    { text: 'R<sub>g1</sub> 上端接线（→电源轨）',
                          parts: [{ text: 'RG1的上端，接到电源正极。' }] },
        'comp-rg1':     { text: '<b>上偏置电阻 R<sub>g1</sub>（60kΩ）</b><br>与 R<sub>g2</sub> 串联分压，把栅极电位基本固定住，稳定工作点',
                          parts: [{ text: '这是上偏置电阻RG1，60千欧。它和下偏置电阻RG2串联分压，把栅极电位基本固定住，使静态工作点稳定。' }] },
        'wire-rg1b':    { text: 'R<sub>g1</sub> 下端接线（→栅极节点）',
                          parts: [{ text: 'RG1的下端，接到栅极节点。' }] },
        'wire-base-in': { text: '栅极节点导线·C<sub>b1</sub> 段（C<sub>b1</sub> 右板→分压节点）',
                          parts: [{ text: '这一段把耦合电容Cb1连到分压节点。直流通路中Cb1开路，这一段随Cb1一起移除。' }] },
        'wire-gate':    { text: '栅极节点导线：R<sub>g1</sub>/R<sub>g2</sub> 分压点、C<sub>b1</sub>、栅极在此相连',
                          parts: [{ text: '这是栅极节点。分压电路、耦合电容Cb1和场效应管的栅极，都在这里相连。' }] },
        'wire-rg2a':    { text: 'R<sub>g2</sub> 上端接线（栅极节点→R<sub>g2</sub>）',
                          parts: [{ text: '分压节点向下，接到下偏置电阻RG2。' }] },
        'comp-rg2':     { text: '<b>下偏置电阻 R<sub>g2</sub>（40kΩ）</b><br>与 R<sub>g1</sub> 分压决定栅极电位；R<sub>g2</sub> 越小则栅极电位越低',
                          parts: [{ text: '这是下偏置电阻RG2，40千欧。它一端接栅极节点，一端接地，和RG1一起决定栅极电位。' }] },
        'wire-rg2b':    { text: 'R<sub>g2</sub> 下端接线（→公共地线）',
                          parts: [{ text: 'RG2的下端接公共地线。' }] },
        'comp-t':       { text: '<b>场效应管 T（N沟道增强型 MOS）</b><br>放大核心：栅极 g、漏极 d、源极 s；衬底 B 与源极相连；栅极电流近似为零，i<sub>d</sub> 受 v<sub>gs</sub> 控制；微变等效中 g–s 开路、d–s 间为受控源 g<sub>m</sub>v<sub>gs</sub>',
                          parts: [{ text: '这是场效应管，放大电路的核心。它是电压控制电流器件，栅极几乎不取电流，漏极电流受栅源电压控制。衬底B和源极连在一起。微变等效时，栅源之间开路，漏源之间等效为一个受控电流源。' }] },
        'wire-d-stub':  { text: '漏极接线（漏极节点—T 漏极）；红色箭头 i<sub>D</sub> 标注漏极直流电流方向（自漏极流出）',
                          parts: [{ text: '场效应管漏极向上，接到漏极导线。红色箭头标出漏极电流iD的方向，它从漏极流出、自上而下。' }] },
        'node-drain':   { text: '漏极节点：R<sub>d</sub>、T 漏极与输出端 v<sub>o</sub> 的交汇点',
                          parts: [{ text: '这是漏极节点。放大后的信号从这里直接送到输出端；向上经漏极电阻Rd接电源。' }] },
        'wire-vo':      { text: '输出导线：漏极节点 → 输出端子 v<sub>o</sub>（直接引出，无输出耦合电容）',
                          parts: [{ text: '放大后的信号经过这条导线，从漏极直接送到输出端子。' }] },
        'wire-rd-a':    { text: 'R<sub>d</sub> 下端接线（R<sub>d</sub>→漏极节点）',
                          parts: [{ text: '漏极电阻Rd向下，接到漏极节点。' }] },
        'comp-rd':      { text: '<b>漏极电阻 R<sub>d</sub>（3.9kΩ）</b><br>把漏极电流的变化转换成电压变化输出；也是输出电阻 R<sub>o</sub> 的主要构成',
                          parts: [{ text: '这是漏极电阻Rd，3.9千欧。它把漏极电流的变化，转换成电压的变化送出去，是输出的关键元件。' }] },
        'wire-rd-top':  { text: 'R<sub>d</sub> 上端接线（→电源轨）',
                          parts: [{ text: 'Rd的上端，接回到电源正极。' }] },
        'wire-src-a':   { text: '源极接线（T 源极→公共地线）：本案例源极直接接地，无源极电阻',
                          parts: [{ text: '场效应管的源极，经过这条导线直接接公共地线。注意本案例源极没有接电阻。' }] },
        'wire-gnd-l1':  { text: '公共地线·输入段：V<sub>i</sub> 负端子—R<sub>g2</sub> 下端；直流通路中随 C<sub>b1</sub> 断路一并移除',
                          parts: [{ text: '这是公共地线的输入段。输入端口的负端和下偏置电阻RG2的下端都接在这里；画直流通路时，它随输入回路一起断开移除。' }] },
        'wire-gnd-m':   { text: '公共地线·主段：R<sub>g2</sub> 下端—源极落点的公共端',
                          parts: [{ text: '这是公共地线的主段。下偏置电阻和源极的下端都接在这条线上，是整个电路的电位参考端。' }] },
        'comp-gnd':     { text: '接地：电位参考点',
                          parts: [{ text: '这是电位参考点。' }] },
        'wire-vi-top':  { text: '输入导线：V<sub>i</sub> 正端子 → C<sub>b1</sub>',
                          parts: [{ text: '输入信号经过这条导线，送到耦合电容Cb1。' }] },
        'comp-vi':      { text: '<b>输入端口 v<sub>i</sub></b><br>放大电路的输入电压，从这对端子经 C<sub>b1</sub> 送入栅极',
                          parts: [{ text: '这是输入端口。放大电路的输入电压，从这里经过耦合电容Cb1，送到栅极。' }] },
        'comp-cb1':     { text: '<b>输入耦合电容 C<sub>b1</sub></b><br>隔直通交：挡住输入端的直流，只让交流信号进入栅极',
                          parts: [{ text: '这是输入耦合电容Cb1。隔直流、通交流，让交流信号进入栅极，又不影响直流偏置。' }] },
        'comp-vo':      { text: '<b>输出电压 v<sub>o</sub></b><br>取自漏极输出端子（直接引出），相位与输入相反（共源反相放大）',
                          parts: [{ text: '这是输出电压。它从漏极输出端子直接取出，相位与输入相反，这就是共源放大电路的反向放大特性。' }] },
        'q-gm':         { text: '<b>跨导 g<sub>m</sub></b><br>场效应管的转移电导：v<sub>GS</sub> 每变化 1V，漏极电流 i<sub>D</sub> 变化 g<sub>m</sub> 安；受控源 g<sub>m</sub>v<sub>gs</sub> 的系数',
                          parts: [{ text: '这是跨导GM。它是受控电流源GM乘VGS的比例系数，反映栅源电压对漏极电流的控制能力。' }] },

    };

'''
src = src[:i] + NEW_ANNOS + src[j + len('    };\n'):]
print('③ ANNOS 重写完成')

# ---------- ④ resetCircuit fx 清单 + 标签重置 ----------
src = rep(src,
    """        ['fx-cb1', 'fx-cb2', 'fx-vs', 'fx-vi', 'fx-vdd', 'fx-vss', 'fx-tmodel', 'fx-t-vgs', 'fx-t-src', 'fx-t-id',
         'fx-dot-g', 'fx-dot-d', 'fx-dot-s', 'rarr-rg1', 'rarr-rd',
         'eq-layer', 'eq-rg1', 'eq-rg2', 'eq-rs'].forEach(id => {""",
    """        ['fx-cb1', 'fx-vi', 'fx-vdd', 'fx-tmodel', 'fx-t-vgs', 'fx-t-src', 'fx-t-id',
         'fx-dot-g', 'fx-dot-d', 'fx-dot-s', 'rarr-rg1', 'rarr-rd',
         'eq-layer', 'eq-rg1', 'eq-rg2'].forEach(id => {""",
    'resetFx清单')
src = rep(src,
    "document.querySelectorAll('.vdd-label, .vss-label, .rg2-label')",
    "document.querySelectorAll('.vdd-label, .rg2-label')",
    'reset标签')
print('④ resetCircuit 完成')

# ---------- ⑤ nextHint：电容清单 ----------
src = rep(src, "const CAPS = ['comp-cb1', 'comp-cb2'];", "const CAPS = ['comp-cb1'];", 'nextHint CAPS')
src = rep(src,
    '    //   ① 门控电源（Vs / +Vcc）处理完 → 请选择电容处理方式\n    //   ② 第 4 关三只电容处理完 → 请选择阿尔义、阿尔B1和阿尔C的整理方式\n    //   ③ 第 4 关三个电阻全部处理完 → 请等效 BJT',
    '    //   ① 门控输入端与电源（v_i / +V_DD）处理完 → 请选择电容处理方式\n    //   ② 电容处理完 → 请选择 R_g1 与 R_d 的整理方式\n    //   ③ 两个电阻全部整理完 → 请等效场效应管',
    'nextHint注释')
print('⑤ nextHint 完成')

# ---------- ⑥ GAME_CONFIG 整块重写 ----------
C_START = '    /* ▼▼▼ 替换区 C：本案例关卡配置 GAME_CONFIG（两阶段五关，换新案例整块替换）▼▼▼'
C_END = '    /* ▲▲▲ 替换区 C 结束 ▲▲▲ */\n'
i = src.index(C_START)
j = src.index(C_END, i) + len(C_END)
NEW_C = '''    /* ▼▼▼ 替换区 C：本案例关卡配置 GAME_CONFIG（两阶段三关 18+22+60=100）▼▼▼
       ★ 表达式一律分式/点乘写法：tk(主,下标) 下标、{box:1} 虚线框、fr([分子],[分母]) 分式 */
    // ---- 案例：单电源分压式偏置共源放大（2026-10-27 按用户原图重绘）----
    //   已知 g_m、R_g1=60kΩ、R_g2=40kΩ、R_d=3.9kΩ、V_DD=5V；源极直接接地（无 R_s）、输出直接引出（无 C_b2）
    //   L1 直流通路（v_i 置零短路、V_DD 保留、C_b1 断路）；L2 交流微变等效（v_i 保留、V_DD 置零接地、C_b1 短路→整理→等效四问）；
    //   L3 动态指标：A_v = −g_m·R_d、R_i = R_g1∥R_g2、R_o ≈ R_d
    function tk(main, sub) { return { main: main, sub: sub }; }
    function fr(num, den) { return { frac: [num, den] }; }   // 分式（上下式）
    const GAME_CONFIG = {
        phases: [
            {
                name: '直流分析',
                steps: [
                    {
                        kind: 'draw', mode: 'remove', title: '第 1 关 · 绘制直流通路', pts: 18, short: '绘制直流通路',
                        q: '先处理输入信号和电源，再将鼠标悬停到电容上，选择正确的处理方式',
                        subLine: '鼠标移到元件上，在浮出的菜单里选「短路 / 断路」作答',
                        targets: [
                            { id: 'comp-vi', name: '输入端口v_i', menu: [
                                { label: '置零', sub: [
                                    { label: '短路', act: 'vi-short', ok: true },
                                    { label: '断路', act: 'vi-open', ok: false }] },
                                { label: '保留', act: 'vi-keep', ok: false }] },
                            { id: 'comp-vdd', name: '直流电源+V_DD', menu: [
                                { label: '置零', sub: [
                                    { label: '接地', act: 'vdd-gnd', ok: false },
                                    { label: '断路', act: 'vdd-open', ok: false }] },
                                { label: '保留', act: 'vdd-keep', ok: true }] },
                            { id: 'comp-cb1', name: '电容C_b1', menu: [
                                { label: '短路', act: 'cap-short', ok: false },
                                { label: '断路', act: 'cap-open', ok: true }] }
                        ],
                        // 门控：输入端口与电源先处理完，电容才解锁（C_b1 断路会连锁移除输入回路）
                        gateMsg: '请先处理输入信号和电源，再处理电容。',
                        gateTodo: '当前：先处理输入信号和电源',
                        gateDoneMsg: '输入信号与电源已处理，现在处理电容',
                        gate: ['comp-vi', 'comp-vdd'],
                        // 选「断路」后，被隔断回路里的元件与导线连锁移除（fadeWith）
                        fadeWith: {
                            'comp-cb1': ['wire-vi-top', 'comp-vi', 'wire-gnd-l1']
                        },
                        announce: '进入第一关，绘制直流通路。先处理输入信号和电源，再将鼠标悬停到电容上，在弹出的菜单里选择正确的处理方式，答对获得18分。',
                        doneSay: '直流通路画好了。',
                        why: '画直流通路：C_b1 开路；输入端口 v_i 置零后短接，随 C_b1 断开的输入回路一并移除；直流电源 +V_DD 保留。'
                    }
                ]
            },
            {
                name: '动态分析',
                steps: [
                    {
                        kind: 'draw', mode: 'transform', title: '第 2 关 · 绘制交流微变等效电路', pts: 22, short: '绘制等效电路',
                        q: '依次完成三步：先绘制交流通路，再整理电路，最后等效场效应管',
                        subLine: '分三步处理：鼠标移到元件上，在菜单里选择处理方式',
                        gateMsg: '请先处理输入信号和电源，再处理电容。',
                        gateTodo: '当前：先处理输入信号和电源',
                        gateDoneMsg: '输入信号与电源已处理，现在处理电容',
                        gate: ['comp-vi', 'comp-vdd'],
                        targets: [
                            { id: 'comp-vi', name: '输入端口v_i', menu: [
                                { label: '置零', sub: [
                                    { label: '短路', act: 'vi-short', ok: false },
                                    { label: '断路', act: 'vi-open', ok: false }] },
                                { label: '保留', act: 'vi-keep', ok: true }] },
                            { id: 'comp-vdd', name: '直流电源+V_DD', menu: [
                                { label: '置零', sub: [
                                    { label: '接地', act: 'vdd-gnd', ok: true },
                                    { label: '断路', act: 'vdd-open', ok: false }] },
                                { label: '保留', act: 'vdd-keep', ok: false }] },
                            { id: 'comp-cb1', name: '电容C_b1', menu: [
                                { label: '短路', act: 'cap-short', ok: true },
                                { label: '断路', act: 'cap-open', ok: false }] },
                            { id: 'comp-t', name: '场效应管', menu: [
                                { label: '等效', act: 't-equiv', ok: true }] }
                        ],
                        // 三步：交流通路 → 整理电路（R_g1/R_d 翻转下挂到地） → 等效场效应管
                        subSteps: [
                            { name: '绘制交流通路', ids: ['comp-vi', 'comp-vdd', 'comp-cb1'] },
                            { name: '整理电路', ids: [], moveIds: ['comp-rg1', 'comp-rd'] },
                            { name: '等效场效应管', ids: ['comp-t'] }
                        ],
                        // 等效四问分值池（画图 3 目标 ×6=18 + 池 4 = 22）
                        tquizPool: 4,
                        announce: '进入第二关，绘制交流微变等效电路，分三步完成：先处理输入信号和电源，再处理电容绘制交流通路，然后整理电路，最后对场效应管进行等效、逐问作答。答对获得22分。',
                        extra: '把鼠标移到元件上，在浮出的菜单里选择处理方式。',
                        doneSay: '交流微变等效电路画好了。',
                        why: '交流微变等效：C_b1 短路、+V_DD 置零接地、R_g1/R_d 翻转下挂到地、场效应管换成 v_gs 与受控源 g_m·v_gs。'
                    },
                    {
                        // 框架 + 表达式交错关（动态）：按 Av → Ri → Ro 逐项，每项先选框架、再填表达式
                        // 分值：3 个框架题各 6 分（18）+ 填空 8/8/8/8/10（42）= 60；全站 18+22+60 = 100
                        kind: 'mix', title: '第 3 关 · 动态指标计算', pts: 60, short: '动态指标计算', stageUnits: 1,
                        subLine: '每个指标先选计算框架，再点虚线框填表达式',
                        subs: [
                            {
                                type: 'fw', name: 'A<tspan class="sub">v</tspan> 框架', qpts: 6, pen: 3,
                                fwQ: '电压放大倍数 A<tspan class="sub">v</tspan> 的表达式框架：',
                                frameworks: [
                                    // 正确：源极直接接地、输出直接引出 → A_v = −g_m·R_d
                                    { tokens: [tk('A', 'v'), tk('='), tk('−'), { box: 1 }, tk('·'), { box: 1 }], correct: true },
                                    // 干扰①：丢掉负号（误写成同相放大）
                                    { tokens: [tk('A', 'v'), tk('='), { box: 1 }, tk('·'), { box: 1 }] },
                                    // 干扰②：误认为有分母（源极接了电阻）
                                    { tokens: [tk('A', 'v'), tk('='), tk('−'), fr([{ box: 1 }, tk('·'), { box: 1 }], [tk('1'), tk('+'), { box: 1 }, tk('·'), { box: 1 }])] }
                                ]
                            },
                            {
                                type: 'fill', name: 'A<tspan class="sub">v</tspan> 表达式',
                                fullExpr: [[tk('A', 'v'), tk('='), tk('−'), { box: 1 }, tk('·'), { box: 1 }]],
                                blanks: [
                                    // g_m（点等效模型旁的 g_m 标注作答）
                                    { ansIds: ['q-gm'], label: [tk('g', 'm')], pts: 8 },
                                    // R_d（整理/等效态下点下挂件同样按 comp-rd 计）
                                    { ansIds: ['comp-rd'], label: [tk('R', 'd')], pts: 8 }
                                ]
                            },
                            {
                                type: 'fw', name: 'R<tspan class="sub">i</tspan> 框架', qpts: 6, pen: 3,
                                fwQ: '输入电阻 R<tspan class="sub">i</tspan> 的表达式框架：',
                                frameworks: [
                                    // 正确：栅极电流为零 → R_i = R_g1∥R_g2
                                    { tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), { box: 1 }], correct: true },
                                    // 干扰①：误写成串联
                                    { tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('+'), { box: 1 }] },
                                    // 干扰②：多并一条支路（误把受控源也算进输入电阻）
                                    { tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), { box: 1 }, tk('∥'), { box: 1 }] }
                                ]
                            },
                            {
                                type: 'fill', name: 'R<tspan class="sub">i</tspan> 表达式',
                                fullExpr: [[tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), { box: 1 }]],
                                blanks: [
                                    // R_g1∥R_g2 同级并联，不区分先后——两空均可点任一电阻（同 grp 查重）
                                    { ansIds: ['comp-rg1', 'comp-rg2'], grp: 'ri-par', labels: { 'comp-rg1': [tk('R', 'g1')], 'comp-rg2': [tk('R', 'g2')] }, label: [tk('R', 'g1')], pts: 8 },
                                    { ansIds: ['comp-rg1', 'comp-rg2'], grp: 'ri-par', labels: { 'comp-rg1': [tk('R', 'g1')], 'comp-rg2': [tk('R', 'g2')] }, label: [tk('R', 'g2')], pts: 8 }
                                ]
                            },
                            {
                                type: 'fw', name: 'R<tspan class="sub">o</tspan> 框架', qpts: 6, pen: 3,
                                fwQ: '输出电阻 R<tspan class="sub">o</tspan> 的表达式框架：',
                                frameworks: [
                                    { tokens: [tk('R', 'o'), tk('≈'), { box: 1 }], correct: true },
                                    { tokens: [tk('R', 'o'), tk('≈'), { box: 1 }, tk('∥'), { box: 1 }] },
                                    { tokens: [tk('R', 'o'), tk('≈'), { box: 1 }, tk('+'), { box: 1 }] }
                                ]
                            },
                            {
                                type: 'fill', name: 'R<tspan class="sub">o</tspan> 表达式',
                                fullExpr: [[tk('R', 'o'), tk('≈'), { box: 1 }]],
                                blanks: [
                                    { ansIds: ['comp-rd'], label: [tk('R', 'd')], pts: 10 }
                                ]
                            }
                        ],
                        announce: '进入第三关，逐个完成动态性能指标的计算。每个指标先选择表达式框架，再填写表达式，顺序是电压放大倍数、输入电阻、输出电阻，共60分。',
                        extra: '框架答对后进入该指标的表达式填空；表达式先点虚线框，再点电路中对应的元件或电量标注。',
                        doneSay: '动态指标电压放大倍数、输入电阻、输出电阻的框架与表达式全部完成，全部关卡结束。'
                    }
                ]
            }
        ]
    };
    /* ▲▲▲ 替换区 C 结束 ▲▲▲ */
'''
src = src[:i] + NEW_C + src[j:]
print('⑥ GAME_CONFIG 重写完成')

# ---------- ⑦ STAGE_UNITS 整块重写 ----------
D_START = '    const STAGE_UNITS = ['
D_END = '    /* ▲▲▲ 替换区 D 结束 ▲▲▲ */\n'
i = src.index(D_START)
j = src.index(D_END, i) + len(D_END)
NEW_D = '''    const STAGE_UNITS = [
        // 第1组=直流（直流通路：电源轨/R_g1/R_g2/地/T/R_d/v_o 端子；输入回路不在内）
        ['comp-vdd', 'wire-vdd-rail', 'wire-vdd-ext', 'node-rd-top', 'wire-rg1a', 'comp-rg1', 'wire-rg1b', 'wire-gate', 'wire-rg2a', 'comp-rg2', 'wire-rg2b', 'comp-gnd', 'wire-gnd-m',
         'comp-t', 'wire-d-stub', 'node-drain', 'wire-vo', 'wire-rd-a', 'comp-rd', 'wire-rd-top', 'wire-src-a'],
        // 第2组=动态（微变等效：全部元件参与；mix 关按此组高亮）
        ['comp-vdd', 'wire-vdd-rail', 'wire-vdd-ext', 'node-rd-top', 'wire-rg1a', 'comp-rg1', 'wire-rg1b', 'wire-base-in', 'wire-gate', 'wire-rg2a', 'comp-rg2', 'wire-rg2b', 'comp-gnd', 'wire-gnd-l1', 'wire-gnd-m',
         'comp-t', 'wire-d-stub', 'node-drain', 'wire-vo', 'wire-rd-a', 'comp-rd', 'wire-rd-top', 'wire-src-a', 'wire-vi-top', 'comp-vi', 'comp-cb1', 'comp-vo']
    ];
    /* ▲▲▲ 替换区 D 结束 ▲▲▲ */
'''
src = src[:i] + NEW_D + src[j:]
print('⑦ STAGE_UNITS 重写完成')

# ---------- ⑧ CAP_FX ----------
src = rep(src, "const CAP_FX = { 'comp-cb1': 'fx-cb1', 'comp-cb2': 'fx-cb2' };",
          "const CAP_FX = { 'comp-cb1': 'fx-cb1' };", 'CAP_FX')

# ---------- ⑨ execAct 整块重写 ----------
E_START = '    // 执行一个绘制动作（id = 元件 data-id，act = 动作名）\n    function execAct(id, act) {'
i = src.index(E_START)
# execAct 函数体到 switch 结束的 "    }\n" （后面是注释 + showEquiv）
E_ANCHOR_END = '        }\n    }\n    // 交流等效最终布局'
j = src.index(E_ANCHOR_END, i) + len('        }\n    }\n')
NEW_EXEC = '''    // 执行一个绘制动作（id = 元件 data-id，act = 动作名）
    function execAct(id, act) {
        const c = cur().cfg;
        switch (act) {
            case 'cap-short':   // 电容短路：隐藏电容、画短接桥
                fadeGroup(id, true); showFx(CAP_FX[id], true); break;
            case 'cap-open': {  // 电容断路：本体与隔断回路一并淡出
                fadeGroup(id);
                const list = (c.fadeWith && c.fadeWith[id]) || [];
                list.forEach(x => fadeGroup(x));
                // 被移除回路里的特效件一并收起（C_b1 断开输入回路时，v_i 的短接桥随之消失）
                if (list.indexOf('comp-vi') >= 0) showFx('fx-vi', false);
                const d = S.draw[S.level - 1];
                (c.fadeWhenAll || []).forEach(rule => {
                    if (rule.requires.every(x => d.found[x])) rule.units.forEach(x => fadeGroup(x));
                });
                break;
            }
            case 'vi-short': fadeGroup('comp-vi', true); showFx('fx-vi', true); break;
            case 'vi-open':  fadeGroup('comp-vi'); break;
            case 'vi-keep':  break;
            case 'vdd-gnd':  showFx('fx-vdd', true); hideLabelOnly('vdd'); break;
            case 'vdd-open': hideLabelOnly('vdd'); break;
            case 'vdd-keep': break;
            case 't-equiv':  fadeGroup('comp-t', true); showEquiv(); startTQuiz(); break;   // 移除场效应管并切换到交流等效布局
        }
    }
'''
src = src[:i] + NEW_EXEC + src[j:]
print('⑨ execAct 重写完成')

# ---------- ⑩ showEquiv 整块重写 ----------
S_START = '    function showEquiv() {'
S_ANCHOR_END = "        ['eq-rg1', 'eq-rg2', 'eq-rs'].forEach(id => { const el = document.getElementById(id); if (el) el.style.pointerEvents = 'all'; });\n    }\n"
i = src.index(S_START)
j = src.index(S_ANCHOR_END, i) + len(S_ANCHOR_END)
NEW_SHOWEQ = '''    function showEquiv() {
        ['wire-vi-top', 'wire-base-in', 'wire-gate', 'comp-vi', 'wire-rg2a', 'comp-rg2', 'wire-rg2b',
         'wire-d-stub', 'wire-drain', 'node-drain', 'wire-vo', 'wire-src-a'].forEach(x => fadeGroup(x, true));
        // rarr-rg1 收起（eq-rg1 重绘）；rarr-rd 保持在整理态下挂位（x=640，与输出并联）：等效后位置不变
        showFx('rarr-rg1', false);
        showFx('rarr-rd', true);
        const rdKeep = document.getElementById('rarr-rd');
        if (rdKeep) rdKeep.style.pointerEvents = 'all';
        // eq-layer 与其中可作答的 eq-rg1 / eq-rg2 一起点亮（resetCircuit 会把它们 opacity 清零）
        ['eq-layer', 'eq-rg1', 'eq-rg2'].forEach(id => showFx(id, true));
        setCircuitShift(true);   // 整个电路图上移 40px，等效模型区域更宽松
        ['eq-rg1', 'eq-rg2'].forEach(id => { const el = document.getElementById(id); if (el) el.style.pointerEvents = 'all'; });
    }
'''
src = src[:i] + NEW_SHOWEQ + src[j:]
print('⑩ showEquiv 重写完成')

# ---------- ⑪ moveCompDown：顶轨收起清单 ----------
src = rep(src,
    "        if (d.moved['comp-rg1'] && d.moved['comp-rd']) {   // 两个电阻都下移 → 顶部的地与下方地合并，收起顶轨与 +VDD 端子\n            ['wire-vdd-rail', 'wire-vdd-ext', 'comp-vdd'].forEach(x => fadeGroup(x, true));",
    "        if (d.moved['comp-rg1'] && d.moved['comp-rd']) {   // 两个电阻都下移 → 顶部的地与下方地合并，收起剩余顶轨段与 +VDD 端子\n            ['wire-vdd-ext', 'comp-vdd'].forEach(x => fadeGroup(x, true));",
    'moveCompDown收轨')
print('⑪ moveCompDown 完成')

# ---------- ⑫ startTQuiz：分值池读配置 ----------
src = rep(src,
    "        d.tquiz = { step: 0, pool: Math.round(cur().cfg.pts / cur().cfg.targets.length) + 2 };",
    "        const pool = cur().cfg.tquizPool !== undefined ? cur().cfg.tquizPool : Math.round(cur().cfg.pts / cur().cfg.targets.length) + 2;\n        d.tquiz = { step: 0, pool: pool };",
    'startTQuiz池')
print('⑫ startTQuiz 完成')

# ---------- ⑬ ?ts 调试钩子：作答序列与池 ----------
src = rep(src,
    """            execAct('comp-src', 'vs-keep'); d4.found['comp-src'] = true;
            execAct('comp-vdd', 'vdd-gnd'); d4.found['comp-vdd'] = true;
            execAct('comp-vss', 'vss-gnd'); d4.found['comp-vss'] = true;
            execAct('comp-cb1', 'cap-short'); d4.found['comp-cb1'] = true;
            execAct('comp-cb2', 'cap-short'); d4.found['comp-cb2'] = true;
            moveCompDown('comp-rg1'); moveCompDown('comp-rd');""",
    """            execAct('comp-vi', 'vi-keep'); d4.found['comp-vi'] = true;
            execAct('comp-vdd', 'vdd-gnd'); d4.found['comp-vdd'] = true;
            execAct('comp-cb1', 'cap-short'); d4.found['comp-cb1'] = true;
            moveCompDown('comp-rg1'); moveCompDown('comp-rd');""",
    'ts钩子作答')
src = rep(src,
    "                d4.tquiz = { step: done ? last : tv - 1, pool: Math.round(cur().cfg.pts / cur().cfg.targets.length) + 2 };",
    "                const tpool = cur().cfg.tquizPool !== undefined ? cur().cfg.tquizPool : Math.round(cur().cfg.pts / cur().cfg.targets.length) + 2;\n                d4.tquiz = { step: done ? last : tv - 1, pool: tpool };",
    'ts钩子池')
print('⑬ 调试钩子完成')

# ---------- ⑭ 头部注释与零散文案 ----------
src = rep(src,
    '        调试钩子：?lvl=1..5 逐关 ／ &ms=n mix 第n子步 ／ ?lvl=4&tidy=1 整理态 ／ &ts=1..6 等效各态。',
    '        调试钩子：?lvl=1..3 逐关 ／ &ms=n mix 第n子步 ／ ?lvl=2&tidy=1 整理态 ／ &ts=1..5 等效各态。',
    '头部钩子注释')
src = rep(src,
    '   · 自检：?lvl=1..5 逐关截图；?lvl=4&tidy=1 / &ts=1..6 各态核对；正确路径满分 100',
    '   · 自检：?lvl=1..3 逐关截图；?lvl=2&tidy=1 / &ts=1..5 各态核对；正确路径满分 100',
    '头部自检注释')
src = rep(src,
    "        else if (c.gate) guide = c.gateDoneMsg || '信号源与电源已处理，现在处理三只电容';",
    "        else if (c.gate) guide = c.gateDoneMsg || '输入信号与电源已处理，现在处理电容';",
    'guide兜底')
src = rep(src,
    "    // ---- 绘制关（①直流通路 ⑤交流微变等效：悬停菜单选「短路/断路」「置零/保留」） ----",
    "    // ---- 绘制关（①直流通路 ②交流微变等效：悬停菜单选「短路/断路」「置零/保留」） ----",
    '绘制关注释')
print('⑭ 头部注释完成')

io.open(P, 'w', encoding='utf-8', newline='').write(src)
print('全部完成 → cs-g1.html 已重建')

# ⑮ 电阻符号缩小（2026-10-27 用户要求：高×2/3、宽×3/4，默认/整理/等效三层统一）
#    本脚本上文模板仍含旧尺寸（36×90/36×80），重建后必须追加此补丁，否则尺寸回退。
import subprocess
_rc = subprocess.call([sys.executable, os.path.join(HERE, 'patch_cs1_res.py')])
if _rc != 0:
    raise SystemExit('patch_cs1_res.py 失败（%d），cs-g1.html 电阻尺寸未收敛，请人工核查' % _rc)
