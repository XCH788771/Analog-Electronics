# -*- coding: utf-8 -*-
"""cs-g1 电阻符号缩小：高 ×2/3、宽 ×3/4（2026-10-27 用户要求）
- 三个默认态电阻 R_g1 / R_g2 / R_d：rect 36×90 → 27×60（R_d 80 → 53），以中心为锚缩放；
- 上下引线端点同步贴合新矩形边（避免悬空/重叠）；
- 整理层（rearr-layer）与等效层（eq-layer）的电阻副本同步统一，避免关卡推进时尺寸跳变。
所有替换带唯一性校验，任一失配即中止不写盘。
"""
import io
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, '..', 'cs-g1.html')

REPS = [
    # ---------- 默认态：R_g1（rect 95-185 → 110-170，中心 140 不变） ----------
    ('<rect class="hot" x="302" y="95" width="36" height="90" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="306.5" y="110" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     'R_g1 矩形'),
    ('d="M 320 5 V 95"', 'd="M 320 5 V 110"', 'R_g1 上引线'),
    ('d="M 320 185 V 295"', 'd="M 320 170 V 295"', 'R_g1 下引线'),
    # ---------- 默认态：R_g2（rect 350-440 → 365-425，中心 395 不变） ----------
    ('<rect class="hot" x="302" y="350" width="36" height="90" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="306.5" y="365" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     'R_g2 矩形'),
    ('d="M 320 295 V 350"', 'd="M 320 295 V 365"', 'R_g2 上引线'),
    ('d="M 320 440 V 525"', 'd="M 320 425 V 525"', 'R_g2 下引线'),
    # ---------- 默认态：R_d（rect 60-140 → 74-127，中心 100 → 100.5） ----------
    ('<rect class="hot" x="468" y="60" width="36" height="80" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="472.5" y="74" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     'R_d 矩形'),
    ('d="M 486 60 V 5"', 'd="M 486 74 V 5"', 'R_d 上引线'),
    ('d="M 486 140 V 178"', 'd="M 486 127 V 178"', 'R_d 下引线'),
    ('<text class="hot-label" x="454" y="108"', '<text class="hot-label" x="454" y="113"', 'R_d 标签垂直居中'),
    # ---------- 整理层：R_g1 下挂（rect 350-440 → 365-425） ----------
    ('<rect class="hot" x="202" y="350" width="36" height="90" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="206.5" y="365" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '整理层 R_g1 矩形'),
    ('d="M 220 295 V 350"', 'd="M 220 295 V 365"', '整理层 R_g1 上引线'),
    ('d="M 220 440 V 525"', 'd="M 220 425 V 525"', '整理层 R_g1 下引线'),
    # ---------- 整理层：R_d 下挂（rect 315-405 → 330-390，中心 360 不变） ----------
    ('<rect class="hot" x="622" y="315" width="36" height="90" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="626.5" y="330" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '整理层 R_d 矩形'),
    ('d="M 640 178 V 315"', 'd="M 640 178 V 330"', '整理层 R_d 上引线'),
    ('d="M 640 405 V 525"', 'd="M 640 390 V 525"', '整理层 R_d 下引线'),
    # ---------- 等效层：R_g1（rect 315-405 → 330-390） ----------
    ('<rect class="hot" x="202" y="315" width="36" height="90" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="206.5" y="330" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '等效层 R_g1 矩形'),
    ('d="M 220 178 V 315"', 'd="M 220 178 V 330"', '等效层 R_g1 上引线'),
    ('d="M 220 405 V 525"', 'd="M 220 390 V 525"', '等效层 R_g1 下引线'),
    # ---------- 等效层：R_g2（rect 315-405 → 330-390） ----------
    ('<rect class="hot" x="302" y="315" width="36" height="90" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="306.5" y="330" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '等效层 R_g2 矩形'),
    ('d="M 320 178 V 315"', 'd="M 320 178 V 330"', '等效层 R_g2 上引线'),
    ('d="M 320 405 V 525"', 'd="M 320 390 V 525"', '等效层 R_g2 下引线'),
]


def main():
    p = os.path.normpath(P)
    raw = io.open(p, 'rb').read()
    s = raw.decode('utf-8').replace('\r\n', '\n')
    crlf = b'\r\n' in raw

    bad = []
    for old, new, tag in REPS:
        n = s.count(old)
        if n != 1:
            bad.append('%s：命中 %d 次（应为 1）' % (tag, n))
    if bad:
        print('中止，未写盘：')
        for b in bad:
            print('  - ' + b)
        return 1

    for old, new, tag in REPS:
        s = s.replace(old, new)
    out = s if not crlf else s.replace('\n', '\r\n')
    io.open(p, 'wb').write(out.encode('utf-8'))
    print('已写入 %s（%d 处替换）' % (p, len(REPS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
