# -*- coding: utf-8 -*-
"""cs-g3 第115轮：V_i －号下移40；R_G1/R_G2/R_G 右移30（标注改右侧）；C_S 标注同轴；
整体左移30（wrap translate 18→-12）；R_L/V_o 组右移50。原子补丁：全对唯一性校验，全过才写盘。"""
import io, sys

P = "cs-g3.html"
s = io.open(P, encoding="utf-8", newline="").read()

pairs = [
    # ④ 整体左移30px（wrap 平移；检查器/回归脚本均动态读取该值）
    ('<g id="circuit-wrap" transform="translate(18, 260) scale(1)">',
     '<g id="circuit-wrap" transform="translate(-12, 260) scale(1)">'),
    # ① V_i －号下移40px（459→499，靠近下端子但保持净距）
    ('<text class="hot-label" x="110" y="459" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="110" y="499" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    # ② R_G1 右移30：电源轨起点 / 上接线 / 电阻体 / 下接线两段
    ('d="M 250 5 H 640"', 'd="M 280 5 H 640"'),
    ('d="M 250 5 V 117"', 'd="M 280 5 V 117"'),
    ('<rect class="hot" x="236.5" y="117" width="27" height="53"',
     '<rect class="hot" x="266.5" y="117" width="27" height="53"'),
    ('<text class="hot-label" x="218" y="150" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G1</tspan></text>',
     '<text class="hot-label" x="309.5" y="150" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">G1</tspan></text>'),
    ('d="M 250 170 V 282"', 'd="M 280 170 V 282"'),
    ('d="M 250 282 V 302"', 'd="M 280 282 V 302"'),
    # ② 分压节点 / R_G2 右移30：上接线 / 电阻体 / 下接线；标注改右侧
    ('<circle cx="250" cy="352" r="7" fill="#ffffff" pointer-events="none"/>',
     '<circle cx="280" cy="352" r="7" fill="#ffffff" pointer-events="none"/>'),
    ('d="M 250 302 V 412"', 'd="M 280 302 V 412"'),
    ('<rect class="hot" x="236.5" y="412" width="27" height="53"',
     '<rect class="hot" x="266.5" y="412" width="27" height="53"'),
    ('<text class="hot-label rg2-label" x="218" y="446" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G2</tspan></text>',
     '<text class="hot-label rg2-label" x="309.5" y="446" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">G2</tspan></text>'),
    ('d="M 250 465 V 525"', 'd="M 280 465 V 525"'),
    # ② R_G 右移30：电阻体 / 标注随体 / 左段接线接新分压节点 / 下引段接新右端
    ('<rect class="hot" x="293.5" y="338.5" width="53" height="27"',
     '<rect class="hot" x="323.5" y="338.5" width="53" height="27"'),
    ('<text class="hot-label" x="320" y="400"', '<text class="hot-label" x="350" y="400"'),
    ('d="M 293.5 352 H 250"', 'd="M 323.5 352 H 280"'),
    ('d="M 390 282 V 352 H 346.5"', 'd="M 390 282 V 352 H 376.5"'),
    # ③ C_S 标注与电容水平同轴（板 425.25/441.25 中心 433.25，基线 440 与 R_S 同）
    ('<text class="hot-label" x="688" y="463"', '<text class="hot-label" x="688" y="440"'),
    # ④ R_L/V_o 组右移50（文件坐标；整体已左移30，净 +20）
    ('d="M 684 161.5 H 800"', 'd="M 684 161.5 H 850"'),
    ('d="M 800 161.5 V 317"', 'd="M 850 161.5 V 317"'),
    ('<rect class="hot" x="786.5" y="317" width="27" height="53"',
     '<rect class="hot" x="836.5" y="317" width="27" height="53"'),
    ('<text class="hot-label" x="770" y="350"', '<text class="hot-label" x="820" y="350"'),
    ('d="M 800 370 V 525"', 'd="M 850 370 V 525"'),
    ('<rect class="hot" x="830" y="150" width="56" height="415"',
     '<rect class="hot" x="880" y="150" width="56" height="415"'),
    ('<text class="hot-label" x="858" y="175"', '<text class="hot-label" x="908" y="175"'),
    ('<text class="hot-label" x="858" y="357"', '<text class="hot-label" x="908" y="357"'),
    ('<text class="hot-label" x="858" y="538"', '<text class="hot-label" x="908" y="538"'),
    # ④ 地轨输出段延长到 R_L 新下端 (850,525)
    ('d="M 646 525 H 800"', 'd="M 646 525 H 850"'),
]

for o, n in pairs:
    c = s.count(o)
    if c != 1:
        print("FAIL count=%d for: %s" % (c, o[:70]))
        sys.exit(1)
for o, n in pairs:
    s = s.replace(o, n)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("OK %d replacements written" % len(pairs))
