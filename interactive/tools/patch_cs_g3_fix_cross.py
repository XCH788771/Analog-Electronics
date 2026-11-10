# -*- coding: utf-8 -*-
import io, sys

PATH = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html"

# 修正 wire-rg1b × wire-in-gate 交叉：
# 保持栅极节点(390,178)与输入导线 y=178 不变；FET 栅极下移后由 wire-gate-out 折线接入，
# C1 由短竖引线 (220,218)->(220,178) 接到输入导线。唯一性校验，全过才写盘。
REPS = [
    ('            <circle cx="390" cy="218" r="7" fill="#ffffff" pointer-events="none"/>',
     '            <circle cx="390" cy="178" r="7" fill="#ffffff" pointer-events="none"/>'),
    ('            <path class="hot" d="M 220 218 H 390" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 220 218 V 178 H 390" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <path class="hot" d="M 390 218 V 298.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 390 178 V 298.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <path class="hot" d="M 390 218 H 502" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 390 178 H 502 V 218" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
]

with io.open(PATH, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

fail = []
for i, (old, new) in enumerate(REPS):
    n = content.count(old)
    if n != 1:
        fail.append((i, n))

if fail:
    for i, n in fail:
        print("UNIQUE-FAIL idx=%d count=%d old=%r" % (i, n, REPS[i][0][:60]))
    print("ABORT")
    sys.exit(1)

for old, new in REPS:
    content = content.replace(old, new, 1)

with io.open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("OK: 交叉修正 %d 处写盘" % len(REPS))
