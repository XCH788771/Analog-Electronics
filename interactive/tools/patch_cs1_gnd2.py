# -*- coding: utf-8 -*-
"""cs-g1：整理/等效态地轨延伸到下挂 R_d 落点 (640,525)——修复 R_d 下挂底端悬空的既有缺陷。
新增 fx-gnd-ext（默认态隐藏；R_d 下移时点亮；等效态保留；resetCircuit 清零）。
唯一性校验：任一 old 串出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html'))
BAK = '/tmp/cs-g1.before-gnd2.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

REPS = []

# ① SVG：在 eq-layer 注释前插入地轨延伸线（fx-layer 内，静态检查自动豁免）
REPS.append((
    """            </g>

            <!-- ===== 交流等效最终态层（第2关「等效场效应管」时启用，与默认/整理态互斥） =====""",
    """            </g>

            <!-- 整理/等效态：地轨向右延伸到下挂 R_d 落点（640,525），默认态隐藏（R_d 下移时点亮） -->
            <g id="fx-gnd-ext" opacity="0" pointer-events="none">
                <path d="M 486 525 H 640" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            </g>

            <!-- ===== 交流等效最终态层（第2关「等效场效应管」时启用，与默认/整理态互斥） ====="""
))

# ② moveCompDown：R_d 下移时点亮延伸线
REPS.append((
    """            fadeGroup('node-drain', true);      // R_d 下移（与输出并联）后漏极只是导线折角，节点圆一并移除
            showFx('rarr-rd', true);""",
    """            fadeGroup('node-drain', true);      // R_d 下移（与输出并联）后漏极只是导线折角，节点圆一并移除
            showFx('fx-gnd-ext', true);         // 地轨延伸到 R_d 下挂落点（640,525）
            showFx('rarr-rd', true);"""
))

# ③ resetCircuit 清零清单补 fx-gnd-ext
REPS.append((
    """         'fx-dot-g', 'fx-dot-d', 'fx-dot-s', 'rarr-rg1', 'rarr-rd',
         'eq-layer', 'eq-rg1', 'eq-rg2'].forEach(id => {""",
    """         'fx-dot-g', 'fx-dot-d', 'fx-dot-s', 'rarr-rg1', 'rarr-rd', 'fx-gnd-ext',
         'eq-layer', 'eq-rg1', 'eq-rg2'].forEach(id => {"""
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

for old, new in REPS:
    s = s.replace(old, new, 1)

shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('OK 3 处替换完成，长度 %d → %d，备份 %s' % (len(orig), len(s), BAK))
