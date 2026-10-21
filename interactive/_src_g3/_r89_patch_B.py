# -*- coding: utf-8 -*-
# round-89（B 文件）：
#  ① V_s 置零短接桥 fx-vs 未随 V_s 下移同步 → 底部 472~492 断开 20px，改为与圆同范围
#  ② V_s 符号、文字与 +/- 极性全部上移 5px（圆 cy 470→465；接wire 同步）
#  ③ 等效态（eq-layer）Vi：删掉负极下方多余导线与节点圆（圆圈下移到接地导线 525）；
#     ＋ 上移 5px、－ 下移靠近地线、V_i 置于 +/- 中间
import io, sys, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_B.txt')
s = io.open(P, 'r', encoding='utf-8', newline='').read()

REPS = [
    # ── ② V_s 信号源整体（圆 + 正弦）上移 5px ──────────────────────────────
    ('<circle class="hot" cx="90" cy="470" r="22" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>',
     '<circle class="hot" cx="90" cy="465" r="22" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 76 470 Q 83 460 90 470 T 104 470" fill="none" stroke="#ffffff" stroke-width="2.5"/>',
     '<path class="hot" d="M 76 465 Q 83 455 90 465 T 104 465" fill="none" stroke="#ffffff" stroke-width="2.5"/>'),
    # ＋ / V_s / － 三段标注上移 5px
    ('<text class="hot-label" x="40" y="450" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="40" y="445" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    ('<text class="hot-label" x="40" y="488" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">s</tspan></text>',
     '<text class="hot-label" x="40" y="483" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">s</tspan></text>'),
    ('<text class="hot-label" x="40" y="526" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="40" y="521" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    # 上/下接wire 随圆同步（圆范围 448-492 → 443-487）
    ('<path class="hot" d="M 90 371 V 448" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 90 371 V 443" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 90 492 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 90 487 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # ── ① fx-vs 置零短接桥：与圆同范围（旧 428-472 留下 20px 断口）──────────
    ('<line x1="90" y1="428" x2="90" y2="472" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="90" y1="443" x2="90" y2="487" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),

    # ── ③ 等效态 Vi ────────────────────────────────────────────────────────
    # ＋ 上移 5px（250→245）、V_i 置于 +/- 中间（→370）、－ 下移靠近地线（440→495）
    ('<text x="150" y="250" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '<text x="150" y="245" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    ('<text x="150" y="345" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>',
     '<text x="150" y="370" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>'),
    ('<text x="150" y="440" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text x="150" y="495" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    # 负极下方多余导线 + 节点圆（480）移除；圆圈保留在接地导线（525）上
    ('                <!-- 第85轮：vi 负端下移靠近地线；下方导线接公共地轨，并加与上端圆圈(150,176)垂直同轴的节点圆 -->\n'
     '                <path d="M 150 440 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n'
     '                <circle cx="150" cy="480" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>\n'
     '                <circle cx="150" cy="525" r="7" fill="#ffffff"/>\n',
     '                <!-- 第89轮：负极下方多余导线与节点圆移除，圆圈只保留在接地导线（地轨 y=525）上 -->\n'
     '                <circle cx="150" cy="525" r="7" fill="#ffffff"/>\n'),
]

for i, (old, new) in enumerate(REPS):
    n = s.count(old)
    if n != 1:
        print('FAIL #%d count=%d for: %s' % (i, n, old[:70]))
        sys.exit(1)
    s = s.replace(old, new)
    print('OK #%d  %s' % (i, old[:60]))

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('WROTE %s' % P)
