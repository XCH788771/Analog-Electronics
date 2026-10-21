# -*- coding: utf-8 -*-
# r88c: 红框->SVG 标定 v2（黄 mask 膨胀合并后聚类）
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open(r'C:/Users/Administrator/.workbuddy/clipboard-images/clipboard-2026-10-19T15-55-06-868Z-60f28d74.png').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
yellow = (r > 200) & (g > 180) & (b < 160)
d = ndimage.binary_dilation(yellow, iterations=6)
lab, n = ndimage.label(d, structure=np.ones((3, 3)))
print('clusters after dilate:', n)
res = []
for i in range(1, n + 1):
    ys, xs = np.nonzero((lab == i) & yellow)
    if len(xs) < 60:
        continue
    res.append((xs.mean(), ys.mean(), len(xs)))
res.sort(key=lambda c: (round(c[0] / 30), c[1]))
for c in res:
    print('cx=%.1f cy=%.1f n=%d' % c)

# 左列(Vs,SVG x=40): +440 / Vs478 / -516 ；右列(Vi,SVG x=150): +310 / Vi375 / -440
left = sorted([c for c in res if c[0] < 110], key=lambda c: c[1])
right = sorted([c for c in res if c[0] >= 110], key=lambda c: c[1])
print('left=%d right=%d' % (len(left), len(right)))
SVG_L = [440, 478, 516]
SVG_R = [310, 375, 440]
if len(left) == 3 and len(right) == 3:
    px = np.array([c[0] for c in left + right])
    py = np.array([c[1] for c in left + right])
    sxv = np.array([40] * 3 + [150] * 3)
    syv = np.array(SVG_L + SVG_R)
    A = np.stack([px, np.ones_like(px)], 1)
    (sx, ox), _, _, _ = np.linalg.lstsq(A, sxv, rcond=None)
    (sy, oy), _, _, _ = np.linalg.lstsq(A, syv, rcond=None)
    print('scale_x=%.4f off_x=%.2f scale_y=%.4f off_y=%.2f' % (sx, ox, sy, oy))
    for (x, y, _), ux, uy in zip(left + right, sxv, syv):
        print('  SVG(%d,%d) err=(%.1f,%.1f)' % (ux, uy, x * sx + ox - ux, y * sy + oy - uy))
    rcx, rcy = (63 + 79) / 2, (279 + 287) / 2
    print('RED center -> SVG (%.1f, %.1f)' % (rcx * sx + ox, rcy * sy + oy))
    print('RED y-range -> SVG y %.1f .. %.1f' % (279 * sy + oy, 287 * sy + oy))
    print('RED x-range -> SVG x %.1f .. %.1f' % (63 * sx + ox, 79 * sx + ox))
