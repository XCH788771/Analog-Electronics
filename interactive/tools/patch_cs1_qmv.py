# -*- coding: utf-8 -*-
"""cs-g1 第2关标注微调（用户 2026-11-01 指令）：
① Vi 的 － 号下移 25px（y 476→501）；
② V_GSQ 文字下移 25px、左移 120px（(526,330)→(406,355)）；
③ G 极红色 ＋ 下移 45px、左移 295px（(408,272)→(113,317)）；
④ G-S 组红色 － 左移 60px（(526,366)→(466,366)）。
热区矩形随动。唯一性校验，失败不写盘。"""
import io, shutil, sys

SRC = 'cs-g1.html'
BAK = '/tmp/cs-g1.before-qmv.html'

REPS = [
    # ① Vi － 下移 25
    ('<text class="hot-label" x="150" y="476" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="150" y="501" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
    # ③ ＋ 下移45 左移295
    ('<text class="hot-label" x="408" y="272" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="113" y="317" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>'),
    # ② V_GSQ 下移25 左移120
    ('<text class="hot-label" x="526" y="330" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GSQ</tspan></text>',
     '<text class="hot-label" x="406" y="355" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GSQ</tspan></text>'),
    # ④ － 左移60
    ('<text class="hot-label" x="526" y="366" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="466" y="366" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>'),
    # 热区随动：＋ 热区
    ('<rect class="hot" x="395" y="244" width="26" height="32" fill="none" stroke="none"/>',
     '<rect class="hot" x="100" y="291" width="26" height="32" fill="none" stroke="none"/>'),
    # 热区随动：V_GSQ＋－ 联合热区
    ('<rect class="hot" x="492" y="296" width="72" height="76" fill="none" stroke="none"/>',
     '<rect class="hot" x="374" y="329" width="106" height="44" fill="none" stroke="none"/>'),
]

s = io.open(SRC, encoding='utf-8', newline='').read()
for old, new in REPS:
    c = s.count(old)
    if c != 1:
        print('FAIL: count=%d for: %s' % (c, old[:70]))
        sys.exit(1)
shutil.copyfile(SRC, BAK)
for old, new in REPS:
    s = s.replace(old, new, 1)
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('OK: %d replacements written, backup %s' % (len(REPS), BAK))
