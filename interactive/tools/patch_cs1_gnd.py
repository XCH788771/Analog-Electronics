# -*- coding: utf-8 -*-
"""cs-g1：接地符号右移到 S 极垂直导线处（x=403 → 486），并在 (486,525) 新增接地端节点。
唯一性校验：任一 old 串出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil, datetime

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html')
SRC = os.path.normpath(SRC)
BAK = '/tmp/cs-g1.before-gnd.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

REPS = []

# ① 接地符号整体右移 83px（x: 403→486 / 375→458 / 431→514 / 385→468 / 421→504 / 393→476 / 413→496）
REPS.append((
    '''        <g class="interactive" data-id="comp-gnd" data-name="接地（电位参考点）">
            <line class="hot" x1="403" y1="525" x2="403" y2="543" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="375" y1="543" x2="431" y2="543" stroke="#ffffff" stroke-width="3.5"/>
            <line class="hot" x1="385" y1="551" x2="421" y2="551" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="393" y1="559" x2="413" y2="559" stroke="#ffffff" stroke-width="2.5"/>
        </g>''',
    '''        <g class="interactive" data-id="comp-gnd" data-name="接地（电位参考点）">
            <line class="hot" x1="486" y1="525" x2="486" y2="543" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="458" y1="543" x2="514" y2="543" stroke="#ffffff" stroke-width="3.5"/>
            <line class="hot" x1="468" y1="551" x2="504" y2="551" stroke="#ffffff" stroke-width="3"/>
            <line class="hot" x1="476" y1="559" x2="496" y2="559" stroke="#ffffff" stroke-width="2.5"/>
        </g>
        <!-- 接地端节点（公共地线主段、S 极垂直导线、接地引线三线交汇点） -->
        <g id="node-gnd" data-id="node-gnd" data-name="接地端节点（公共地线·S 极落点·接地符号交汇）">
            <circle cx="486" cy="525" r="7" fill="#ffffff" pointer-events="none"/>
        </g>'''
))

# ② ANNOS 新增 node-gnd 条目
REPS.append((
    """        'comp-gnd':     { text: '接地：电位参考点',
                          parts: [{ text: '这是电位参考点。' }] },""",
    """        'comp-gnd':     { text: '接地：电位参考点',
                          parts: [{ text: '这是电位参考点。' }] },
        'node-gnd':     { text: '接地端节点：公共地线、S 极垂直导线与接地符号在此交汇',
                          parts: [{ text: '这是接地端节点。公共地线、源极的垂直导线和接地符号都在这里交汇。' }] },"""
))

# ③ STAGE_UNITS 第1组（直流通路）补 node-gnd
REPS.append((
    "'wire-rg2b', 'comp-gnd', 'wire-gnd-m',",
    "'wire-rg2b', 'comp-gnd', 'node-gnd', 'wire-gnd-m',"
))

# ④ STAGE_UNITS 第2组（全件组）补 node-gnd
REPS.append((
    "'comp-gnd', 'wire-gnd-l1', 'wire-gnd-m',",
    "'comp-gnd', 'node-gnd', 'wire-gnd-l1', 'wire-gnd-m',"
))

# ---- 唯一性校验 ----
fail = False
for i, (old, new) in enumerate(REPS, 1):
    n = s.count(old)
    if n != 1:
        print('[FAIL] 第%d处 old 出现 %d 次（须为1）' % (i, n))
        fail = True
if fail:
    print('中止：未写盘')
    sys.exit(1)

# ---- 应用（顺序替换，前一处不产生后一处的 old）----
for old, new in REPS:
    s = s.replace(old, new, 1)

# ---- 写盘（保持行尾）----
shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)

print('OK 4 处替换完成，长度 %d → %d，备份 %s' % (len(orig), len(s), BAK))
