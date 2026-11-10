# -*- coding: utf-8 -*-
"""cs-g1：
① v_o 标注 74px → 49px（74 的 2/3），基线 y 190→181、x 722→726（与输出端子垂直居中）。
② 场效应管整体右移 28px：B 引线折点 458→486，与 S 极直角点 (486,294) 重合（三线交汇，节点圆随移）；
   漏/源水平引线右端仍接 486（wire-d-stub / wire-src-a 不动），左端随本体右移。
   字符：g +28；B 486→514、T 516→544（原位被新竖线穿过，右移让位）；d/s 标在引线端不动。
唯一性校验：任一 old 串出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html'))
BAK = '/tmp/cs-g1.before-t28.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

REPS = [
    # ② 管子本体右移 28px
    ('<rect class="hot" x="386" y="192" width="120" height="150" fill="none" stroke="none"/>',
     '<rect class="hot" x="414" y="192" width="120" height="150" fill="none" stroke="none"/>'),
    ('<line class="hot" x1="400" y1="235" x2="400" y2="295" stroke="#ffffff" stroke-width="5"/>',
     '<line class="hot" x1="428" y1="235" x2="428" y2="295" stroke="#ffffff" stroke-width="5"/>'),
    ('<line class="hot" x1="414" y1="227" x2="414" y2="245" stroke="#ffffff" stroke-width="5"/>',
     '<line class="hot" x1="442" y1="227" x2="442" y2="245" stroke="#ffffff" stroke-width="5"/>'),
    ('<line class="hot" x1="414" y1="256" x2="414" y2="274" stroke="#ffffff" stroke-width="5"/>',
     '<line class="hot" x1="442" y1="256" x2="442" y2="274" stroke="#ffffff" stroke-width="5"/>'),
    ('<line class="hot" x1="414" y1="285" x2="414" y2="303" stroke="#ffffff" stroke-width="5"/>',
     '<line class="hot" x1="442" y1="285" x2="442" y2="303" stroke="#ffffff" stroke-width="5"/>'),
    ('<path class="hot" d="M 414 236 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 442 236 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<path class="hot" d="M 414 294 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 442 294 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # B 引线：折点右移到 S 极直角点 (486,294)
    ('<path class="hot" d="M 446 265 H 458 V 294" fill="none" stroke="#ffffff" stroke-width="3"/>',
     '<path class="hot" d="M 474 265 H 486 V 294" fill="none" stroke="#ffffff" stroke-width="3"/>'),
    ('<polygon class="hot-fill" points="418,265 446,253 446,277" fill="#ffffff" stroke="none"/>',
     '<polygon class="hot-fill" points="446,265 474,253 474,277" fill="#ffffff" stroke="none"/>'),
    ('<circle cx="458" cy="294" r="7" fill="#ffffff" pointer-events="none"/>',
     '<circle cx="486" cy="294" r="7" fill="#ffffff" pointer-events="none"/>'),
    # 字符：g 随本体；B/T 让开新竖线；d/s 标在引线端不动
    ('<text class="hot-label" x="390" y="337" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">g</text>',
     '<text class="hot-label" x="418" y="337" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">g</text>'),
    ('<text class="hot-label" x="486" y="278" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">B</text>',
     '<text class="hot-label" x="514" y="278" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">B</text>'),
    ('<text class="hot-label" x="516" y="282" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">T</text>',
     '<text class="hot-label" x="544" y="282" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="start">T</text>'),
    # ① v_o 74 → 49px（74 的 2/3）
    ('<text class="hot-label" x="722" y="190" fill="#ffe66d" font-size="74" font-weight="bold" font-style="italic" text-anchor="start">v<tspan class="sub">o</tspan></text>',
     '<text class="hot-label" x="726" y="181" fill="#ffe66d" font-size="49" font-weight="bold" font-style="italic" text-anchor="start">v<tspan class="sub">o</tspan></text>'),
]

fail = False
for i, (old, new) in enumerate(REPS, 1):
    n = s.count(old)
    if n != 1:
        print('[FAIL] 第%d处 old 出现 %d 次（须为1）: %r' % (i, n, old[:60]))
        fail = True
if fail:
    print('中止：未写盘')
    sys.exit(1)

for old, new in REPS:
    s = s.replace(old, new, 1)

shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('OK %d 处替换完成，长度 %d → %d，备份 %s' % (len(REPS), len(orig), len(s), BAK))
