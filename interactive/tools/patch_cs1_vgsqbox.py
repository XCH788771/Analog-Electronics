# -*- coding: utf-8 -*-
"""cs-g1 第2关：I_DQ 表达式中的 V_GSQ 也改为方框（可点击电路 V_GSQ 标注填入）"""
import io, shutil, sys

SRC = 'cs-g1.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
reps = []

def rep(old, new, tag):
    global s
    c = s.count(old)
    assert c == 1, '[%s] count=%d' % (tag, c)
    s = s.replace(old, new, 1)
    reps.append(tag)

# ① fullExpr：分子 V_GSQ 文字 → 方框（分母保持方框）
rep("fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],\n                                blanks: [\n                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },\n                                    { ansIds: ['q-vt'], label: [tk('V', 'T')], pts: 2 }\n                                ]",
    "fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],\n                                blanks: [\n                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },\n                                    { ansIds: ['q-vth'], label: [tk('V', 'GSQ')], pts: 1 },\n                                    { ansIds: ['q-vt'], label: [tk('V', 'T')], pts: 1 }\n                                ]",
    'fill3-boxes')

# ② 分值注释配平
rep('// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/2、1/1/3（15）= 24（I_DQ 方程两空：I_DO 2 分、V_T 2 分，各对应图中同名红标）',
    '// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/1/1、1/1/3（15）= 24（I_DQ 方程三空：I_DO 2 分、V_GSQ 1 分、V_T 1 分，各对应图中同名红标）',
    'pts-comment')

# ③ V_GSQ 标注悬停词条补「可点击填入」
rep("'q-vth':        { text: '<b>V<sub>GSQ</sub></b>（＋/−）<br>栅源静态电压：由 R<sub>g1</sub>、R<sub>g2</sub> 分压决定，＋在 G、−在 S 标出极性',",
    "'q-vth':        { text: '<b>V<sub>GSQ</sub></b>（＋/−）<br>栅源静态电压：由 R<sub>g1</sub>、R<sub>g2</sub> 分压决定，＋在 G、−在 S 标出极性（第 2 关可点击填入 I<sub>DQ</sub> 方程方框）',",
    'anno-vgsq')

# ④ subLine / extra 说明三空（保持「点虚线框填符号」，无需改）；data-name 补用途
rep('data-id="q-vth" data-name="栅源静态电压 V_GSQ（＋/− 标出极性）"',
    'data-id="q-vth" data-name="栅源静态电压 V_GSQ（＋/− 标出极性，第 2 关填入 I_DQ 方程）"',
    'name-vgsq')

if '--dry' in sys.argv:
    print('[DRY] %d reps:' % len(reps), ','.join(reps))
    sys.exit(0)

shutil.copyfile(SRC, '/tmp/cs-g1.before-vgsqbox.html')
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('[OK] %d reps:' % len(reps), ','.join(reps))
