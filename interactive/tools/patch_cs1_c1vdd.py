# -*- coding: utf-8 -*-
"""cs-g1 修订（用户 2026-11-01 三项指令）：
① V_DD 下移与端子圆垂直同轴、间隔 20px、前加 ＋ 号；
② C_b1 全部改称 C_1（屏显 + TTS；内部 data-id comp-cb1 不动）；
③ 第 2 关 V_GSQ 的 ＋ 移到截图黄框位 (360,322)。
唯一性/计数校验，失败不写盘。"""
import io, shutil, sys

SRC = 'cs-g1.html'
BAK = '/tmp/cs-g1.before-c1vdd.html'

REPS = [
    # ① V_DD：加 ＋、下移、间隔 20
    ('<text class="hot-label vdd-label" x="726" y="16" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">V<tspan class="sub">DD</tspan></text>',
     '<text class="hot-label vdd-label" x="728" y="18" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">＋V<tspan class="sub">DD</tspan></text>'),
    # ③ 红色 ＋ 移到黄框位
    ('<text class="hot-label" x="113" y="317" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>',
     '<text class="hot-label" x="360" y="322" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>'),
    ('<rect class="hot" x="100" y="291" width="26" height="32" fill="none" stroke="none"/>',
     '<rect class="hot" x="346" y="296" width="28" height="28" fill="none" stroke="none"/>'),
]

# ② C_b1 → C_1 全局改称（四种串形；期望计数校验）
GLOBS = [
    ('C<tspan class="sub">b1</tspan>', 'C<tspan class="sub">1</tspan>', 1),   # SVG 元件标注
    ('C<sub>b1</sub>', 'C<sub>1</sub>', None),                                 # ANNOS 屏显
    ('C_b1', 'C_1', None),                                                     # data-name/name/why/注释
    ('Cb1', 'C1', None),                                                       # TTS 语音串
]

s = io.open(SRC, encoding='utf-8', newline='').read()
for old, new in REPS:
    c = s.count(old)
    if c != 1:
        print('FAIL: count=%d for: %s' % (c, old[:70]))
        sys.exit(1)
for old, new, expect in GLOBS:
    c = s.count(old)
    if expect is not None and c != expect:
        print('FAIL: glob %r count=%d expect=%d' % (old, c, expect))
        sys.exit(1)
    if c == 0:
        print('FAIL: glob %r not found' % old)
        sys.exit(1)
    print('glob %r x%d' % (old, c))
shutil.copyfile(SRC, BAK)
for old, new in REPS:
    s = s.replace(old, new, 1)
for old, new, _ in GLOBS:
    s = s.replace(old, new)
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('OK: %d reps + globs written, backup %s' % (len(REPS), BAK))
