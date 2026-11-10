# -*- coding: utf-8 -*-
"""第117轮补之二：标签间距微调（防连读）
- RD 整理态标签 x 728.5→722.5（离体 9px；实测 bbox 46.8 宽，右缘 769.3）
- R_L 静态标签 end 820→824（离体 12.5px；左缘 778.8 → 与 RD 净隙 9.5px）
- RG1 整理态标签 x 198.5→193.5（离体 10px；右缘 255.7 → 距 RG2 体 10.8px）"""
import io, sys
P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()
REPS = [
('<text class="hot-label" x="728.5" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">D</tspan></text>',
 '<text class="hot-label" x="722.5" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">D</tspan></text>'),
('<text class="hot-label" x="820" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>',
 '<text class="hot-label" x="824" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>'),
('<text class="hot-label" x="198.5" y="446" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">G1</tspan></text>',
 '<text class="hot-label" x="193.5" y="446" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">G1</tspan></text>'),
('标签放本体右侧（x=728.5 起、间距 15px、y=350 与本体同轴），与 R_L 标签净距 ≥20',
 '标签放本体右侧（x=722.5 起、y=350 与本体同轴），与 R_L 标签净隙 ≥9.5'),
('标签放本体右侧（x=198.5 起、间距 15px），\n             与 R_G2 标签同基线 y=446',
 '标签放本体右侧（x=193.5 起），\n             与 R_G2 标签同基线 y=446'),
]
for i, (old, new) in enumerate(REPS):
    n = c.count(old)
    if n != 1:
        print('FAIL rep#%d count=%d :: %s' % (i, n, old[:60].replace('\n', '\\n')))
        sys.exit(1)
for old, new in REPS:
    c = c.replace(old, new)
io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d reps' % len(REPS))
