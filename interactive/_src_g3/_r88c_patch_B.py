# -*- coding: utf-8 -*-
# round-88c: 默认态 comp-vi —— －号下移到用户红框位（墨迹中心 y≈533，基线 543），
#            Vi 文字下移到 ＋/－ 墨迹中点（中心 421.5，基线 432）
import io, sys, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_B.txt')
s = io.open(P, 'r', encoding='utf-8', newline='').read()

REPS = [
    ('<text class="hot-label" x="150" y="385" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>',
     '<text class="hot-label" x="150" y="432" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>'),
    ('<text class="hot-label" x="150" y="450" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="150" y="543" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
]

for old, new in REPS:
    n = s.count(old)
    if n != 1:
        print('FAIL count=%d for: %s' % (n, old[:80]))
        sys.exit(1)
    s = s.replace(old, new)
    print('OK  %s' % old[:66])

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('WROTE %s' % P)
