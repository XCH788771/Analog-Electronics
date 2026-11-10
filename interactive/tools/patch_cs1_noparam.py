# -*- coding: utf-8 -*-
"""cs-g1：去掉题干（已知行）与电路图中的参数数值，只保留元件号/符号。
覆盖：已知行 4 处 =值、电源端子 (5V)、R_g1/R_g2/R_d 的 60kΩ/40kΩ/3.9kΩ 标注、
      comp-rd 的 data-name、ANNOS 四条（屏显+语音）、台账注释。
唯一性校验：任一 old 串出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html'))
BAK = '/tmp/cs-g1.before-noparam.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

REPS = [
    # ① 已知行：去掉 =数值（保留元件号与符号）
    ('R<tspan class="sub">g1</tspan>=60kΩ、', 'R<tspan class="sub">g1</tspan>、'),
    ('R<tspan class="sub">g2</tspan>=40kΩ、', 'R<tspan class="sub">g2</tspan>、'),
    ('R<tspan class="sub">d</tspan>=3.9kΩ、', 'R<tspan class="sub">d</tspan>、'),
    ('V<tspan class="sub">DD</tspan>=5V、', 'V<tspan class="sub">DD</tspan>、'),

    # ② 电源端子：删 (5V)，V_DD 单行垂直对齐端子
    ('''            <text class="hot-label vdd-label" x="726" y="-6" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">V<tspan class="sub">DD</tspan></text>
            <text class="hot-label vdd-label" x="726" y="34" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="start">(5V)</text>''',
     '''            <text class="hot-label vdd-label" x="726" y="16" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">V<tspan class="sub">DD</tspan></text>'''),

    # ③ 三只电阻的数值标注整行删除
    ('\n            <text x="346" y="130" fill="rgba(255,255,255,0.85)" font-size="28" font-weight="bold" text-anchor="start">60kΩ</text>', ''),
    ('\n            <text x="346" y="432" fill="rgba(255,255,255,0.85)" font-size="28" font-weight="bold" text-anchor="start">40kΩ</text>', ''),
    ('\n            <text x="514" y="131" fill="rgba(255,255,255,0.85)" font-size="28" font-weight="bold" text-anchor="start">3.9kΩ</text>', ''),

    # ④ comp-rd 的 data-name 去参数
    ('data-name="漏极电阻 R_d（3.9kΩ）"', 'data-name="漏极电阻 R_d"'),

    # ⑤ ANNOS：屏显与语音同步去参数
    ("""        'comp-vdd':     { text: '<b>直流电源 +V<sub>DD</sub>（5V）</b><br>为电路提供能量，是静态工作点与输出信号的能量来源；交流分析中视为对地短路（置零）',
                          parts: [{ text: '这是直流电源，5伏。它为整个放大电路提供能量，静态工作点和输出信号的能量都由它提供。' }] },""",
     """        'comp-vdd':     { text: '<b>直流电源 +V<sub>DD</sub></b><br>为电路提供能量，是静态工作点与输出信号的能量来源；交流分析中视为对地短路（置零）',
                          parts: [{ text: '这是直流电源。它为整个放大电路提供能量，静态工作点和输出信号的能量都由它提供。' }] },"""),
    ("<b>上偏置电阻 R<sub>g1</sub>（60kΩ）</b>", "<b>上偏置电阻 R<sub>g1</sub></b>"),
    ("这是上偏置电阻RG1，60千欧。它和", "这是上偏置电阻RG1。它和"),
    ("<b>下偏置电阻 R<sub>g2</sub>（40kΩ）</b>", "<b>下偏置电阻 R<sub>g2</sub></b>"),
    ("这是下偏置电阻RG2，40千欧。它一端", "这是下偏置电阻RG2。它一端"),
    ("<b>漏极电阻 R<sub>d</sub>（3.9kΩ）</b>", "<b>漏极电阻 R<sub>d</sub></b>"),
    ("这是漏极电阻Rd，3.9千欧。它把", "这是漏极电阻Rd。它把"),

    # ⑥ 台账注释同步（维护信息，避免误导）
    ("""             +V_DD(5V) — R_g1 60k / R_g2 40k 分压 — C_b1 耦合输入 v_i — N 沟道 MOS 管 T（衬底 B 接源极）
             — 源极直落地 — R_d 3.9k — 漏极直接引出 v_o（无输出耦合电容、无源极电阻） ====== -->""",
     """             +V_DD — R_g1 / R_g2 分压 — C_b1 耦合输入 v_i — N 沟道 MOS 管 T（衬底 B 接源极）
             — 源极直落地 — R_d — 漏极直接引出 v_o（无输出耦合电容、无源极电阻）
             ★参数数值已从题干与电路图中隐去，只保留元件号（原值 5V/60k/40k/3.9k，见制作记录） ====== -->"""),
    ('<!-- 电源端 +VDD（右上端子；标注在右侧两行：V_DD / (5V)） -->',
     '<!-- 电源端 +VDD（右上端子；只标符号 V_DD，不标数值） -->'),
    ('//   已知 g_m、R_g1=60kΩ、R_g2=40kΩ、R_d=3.9kΩ、V_DD=5V；',
     '//   已知 g_m、R_g1、R_g2、R_d、V_DD（页面不标数值，只标元件号）；'),
]

# ---- 唯一性校验 ----
fail = False
for i, (old, new) in enumerate(REPS, 1):
    n = s.count(old)
    if n != 1:
        print('[FAIL] 第%d处 old 出现 %d 次（须为1）: %r' % (i, n, old[:60]))
        fail = True
if fail:
    print('中止：未写盘')
    sys.exit(1)

for old, new in REPS:
    s = s.replace(old, new, 1)

shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)

# 残留核查
import re
left = []
for i, l in enumerate(s.split('\n'), 1):
    if len(l) > 400:
        continue
    if re.search(r'60kΩ|40kΩ|3\.9kΩ|\(5V\)|60千欧|40千欧|3\.9千欧|5伏', l):
        left.append((i, l.strip()[:100]))
print('OK %d 处替换完成，长度 %d → %d，备份 %s' % (len(REPS), len(orig), len(s), BAK))
print('残留参数行：', left if left else '无')
