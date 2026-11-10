# -*- coding: utf-8 -*-
"""cs-g1：v_o 标注字号增大一倍（37 → 74px），基线 y 176 → 190 保持与输出端子垂直居中。
唯一性校验：old 出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html'))
BAK = '/tmp/cs-g1.before-vo.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

OLD = '<text class="hot-label" x="726" y="176" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="start">v<tspan class="sub">o</tspan></text>'
NEW = '<text class="hot-label" x="722" y="190" fill="#ffe66d" font-size="74" font-weight="bold" font-style="italic" text-anchor="start">v<tspan class="sub">o</tspan></text>'

n = s.count(OLD)
if n != 1:
    print('[FAIL] old 出现 %d 次（须为1）' % n)
    sys.exit(1)

s = s.replace(OLD, NEW, 1)

shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('OK v_o 37→74px（x 726→722 / y 176→190），长度 %d → %d，备份 %s' % (len(orig), len(s), BAK))
