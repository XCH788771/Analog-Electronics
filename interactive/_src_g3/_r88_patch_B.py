# -*- coding: utf-8 -*-
"""cj-g3 第88轮 区B 补丁：Vs 信号源下移 20px、Vs 文字与 +/- 号下移 30px。
   圆下移后同步调整上下接wire 端点，保持电路连通（R_S↔Vs↔地）。
"""
import io, sys, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_B.txt')
with io.open(P, encoding='utf-8', newline='') as f:
    raw = f.read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')
n0 = s

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.stderr.write('ANCHOR FAIL (%d!=1): %r\n' % (n, old[:70]))
        sys.exit(1)
    s = s.replace(old, new, 1)

# ---- Vs 信号源（圆 + 正弦线）下移 20px：cy 450→470 ----
rep('<circle class="hot" cx="90" cy="450" r="22" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>',
    '<circle class="hot" cx="90" cy="470" r="22" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>')
rep('<path class="hot" d="M 76 450 Q 83 440 90 450 T 104 450" fill="none" stroke="#ffffff" stroke-width="2.5"/>',
    '<path class="hot" d="M 76 470 Q 83 460 90 470 T 104 470" fill="none" stroke="#ffffff" stroke-width="2.5"/>')

# ---- Vs 文字与 +/- 号下移 30px：410→440 / 448→478 / 486→516 ----
rep('<text class="hot-label" x="40" y="410" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
    '<text class="hot-label" x="40" y="440" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>')
rep('<text class="hot-label" x="40" y="448" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">s</tspan></text>',
    '<text class="hot-label" x="40" y="478" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">s</tspan></text>')
rep('<text class="hot-label" x="40" y="486" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
    '<text class="hot-label" x="40" y="516" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>')

# ---- 接wire 端点随圆调整：上wire 428→448（伸长）、下wire 472→492（缩短）----
rep('<path class="hot" d="M 90 371 V 428" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot" d="M 90 371 V 448" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<path class="hot" d="M 90 472 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot" d="M 90 492 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>')

if s == n0:
    sys.stderr.write('NO CHANGE\n'); sys.exit(1)
out = s.replace('\n', '\r\n') if crlf else s
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(out)
print('_g3_B.txt 第88轮补丁完成：Vs 圆 +20px、文字 +/- +30px、接wire 端点随调（7 处）')
