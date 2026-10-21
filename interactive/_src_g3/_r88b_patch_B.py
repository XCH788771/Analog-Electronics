# -*- coding: utf-8 -*-
# round-88b: V_s 文字与 ＋/－ 号再下移 10px（在 round-88 已下移 30px 基础上）
import io, sys, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_B.txt')
s = io.open(P, 'r', encoding='utf-8', newline='').read()

REPS = [
    # ＋ 号 440 -> 450
    ('<text class="hot-label" x="40" y="440" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="40" y="450" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>'),
    # V_s 文字 478 -> 488
    ('<text class="hot-label" x="40" y="478" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">s</tspan></text>',
     '<text class="hot-label" x="40" y="488" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">s</tspan></text>'),
    # － 号 516 -> 526
    ('<text class="hot-label" x="40" y="516" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
     '<text class="hot-label" x="40" y="526" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>'),
]

for old, new in REPS:
    n = s.count(old)
    if n != 1:
        print('FAIL count=%d for: %s' % (n, old[:70]))
        sys.exit(1)
    s = s.replace(old, new)
    print('OK  %s' % old[:60])

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('WROTE %s  (%d bytes)' % (P, len(s)))
