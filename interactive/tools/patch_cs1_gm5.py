# -*- coding: utf-8 -*-
"""cs-g1 等效态第四轮（用户纠正）：
1) 恢复第 4 问作答后箭头旁的红色 g_m·v_gs（fx-t-idlabel，原位 548,222）
2) 删除上一轮加的受控源右侧红 g_m（fx-t-idlabel 内 581）
3) q-gm（第 4 关点选跨导）从 (440,368) 移到受控源右侧 (581,352)，热区跟随 —— 不再压 v_gs
"""
import io, sys

P = "cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()
reps = []

# ① q-gm 标注与热区移到受控源右侧
old1 = """                    <rect class="hot" x="404" y="340" width="72" height="56" fill="none" stroke="none"/>
                    <text class="hot-label" x="440" y="368" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>"""
new1 = """                    <rect class="hot" x="545" y="324" width="72" height="56" fill="none" stroke="none"/>
                    <text class="hot-label" x="581" y="352" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>"""
reps.append((old1, new1))

# ② fx-t-idlabel 恢复 g_m·v_gs（箭头旁原文位置），去掉受控源右侧的 g_m
old2 = """                <!-- 增益标注 g_m：第 4 问作答后随箭头同现，红色，置于受控源右侧（距右顶点 21px，与 v_gs 同基线水平同轴） -->
                <g id="fx-t-idlabel" opacity="0">
                    <text x="581" y="352" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>
                </g>"""
new2 = """                <!-- 受控源电流数值标注 g_m·v_gs：第 4 问作答后与箭头同现（箭头右侧，原 i_d 位） -->
                <g id="fx-t-idlabel" opacity="0">
                    <text x="548" y="222" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
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
