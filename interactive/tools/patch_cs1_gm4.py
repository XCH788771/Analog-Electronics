# -*- coding: utf-8 -*-
"""cs-g1 等效态第三轮：
1) fx-t-src 删除黄色 g_m（第 3 关不再显示）
2) fx-t-idlabel 红色 g_m·v_gs → 红色 g_m，移到受控源右侧（x=581，距右顶点 560 仍 21px，y 同轴 352）
"""
import io, sys

P = "cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()

reps = []

# ① fx-t-src 内黄色 g_m 整块移除（注释一并删）
old1 = """                    <!-- 增益标注 g_m：夹在 v_gs（控制量）与菱形（受控源）之间，与 v_gs 同基线水平同轴 -->
                    <text x="479" y="352" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>
"""
new1 = ""
reps.append((old1, new1))

# ② fx-t-idlabel：g_m·v_gs → g_m，移到受控源右侧、与 v_gs 同基线
old2 = """                <!-- 受控源电流数值标注：第 4 问弹出方向选项时即显示（先见数值、再选方向），作答后与箭头同现 -->
                <g id="fx-t-idlabel" opacity="0">
                    <text x="548" y="222" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>"""
new2 = """                <!-- 增益标注 g_m：第 4 问作答后随箭头同现，红色，置于受控源右侧（距右顶点 21px，与 v_gs 同基线水平同轴） -->
                <g id="fx-t-idlabel" opacity="0">
                    <text x="581" y="352" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>
                </g>"""
reps.append((old2, new2))

ok = True
for i, (o, n) in enumerate(reps, 1):
    c = s.count(o)
    if c != 1:
        print("rep%d FAIL count=%d" % (i, c)); ok = False
    else:
        print("rep%d OK" % i)
if not ok:
    sys.exit(1)
for o, n in reps:
    s = s.replace(o, n)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("已写盘")
