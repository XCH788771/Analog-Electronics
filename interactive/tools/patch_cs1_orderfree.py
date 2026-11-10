# -*- coding: utf-8 -*-
"""cs-g1：① I_DQ 计算框架中 V_GSQ 改方框；② 同级运算填空不区分顺序（V_DSQ 的 I_DQ·R_d、V_GSQ 分母 R_g1+R_g2、A_v 的 g_m·R_d）"""
import io, shutil, sys

SRC = 'cs-g1.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
reps = []

def rep(old, new, tag, cnt=1):
    global s
    c = s.count(old)
    assert c == cnt, '[%s] count=%d (want %d)' % (tag, c, cnt)
    s = s.replace(old, new)
    reps.append(tag)

# ---------- ① I_DQ 计算框架：V_GSQ → 方框（正确项 + 两个干扰项，共 3 处） ----------
rep("fr([tk('V', 'GSQ')], [{ box: 1 }])",
    "fr([{ box: 1 }], [{ box: 1 }])",
    'fw-vgsq-box', 3)

# ---------- ②-1 V_GSQ 分母 R_g1 + R_g2（加分，同级不区分顺序） ----------
rep("""                                    { ansIds: ['comp-rg1'], label: [tk('R', 'g1')], pts: 1 },
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 1 },""",
    """                                    // 分母 R_g1 + R_g2 同级相加，不区分先后——两空均可点任一电阻（同 grp 查重）
                                    { ansIds: ['comp-rg1', 'comp-rg2'], grp: 'vgsq-den', labels: { 'comp-rg1': [tk('R', 'g1')], 'comp-rg2': [tk('R', 'g2')] }, label: [tk('R', 'g1')], pts: 1 },
                                    { ansIds: ['comp-rg1', 'comp-rg2'], grp: 'vgsq-den', labels: { 'comp-rg1': [tk('R', 'g1')], 'comp-rg2': [tk('R', 'g2')] }, label: [tk('R', 'g2')], pts: 1 },""",
    'vgsq-den')

# ---------- ②-2 V_DSQ 的 I_DQ · R_d（乘法，同级不区分顺序；分值 1/3 → 2/2 配平） ----------
rep("""                                    { ansIds: ['q-idq'], label: [tk('I', 'DQ')], pts: 1 },
                                    { ansIds: ['comp-rd'], label: [tk('R', 'd')], pts: 3 }""",
    """                                    // I_DQ · R_d 同级相乘，不区分先后——两空均可点任一量（同 grp 查重），分值配平 2/2
                                    { ansIds: ['q-idq', 'comp-rd'], grp: 'vdsq-prod', labels: { 'q-idq': [tk('I', 'DQ')], 'comp-rd': [tk('R', 'd')] }, label: [tk('I', 'DQ')], pts: 2 },
                                    { ansIds: ['q-idq', 'comp-rd'], grp: 'vdsq-prod', labels: { 'q-idq': [tk('I', 'DQ')], 'comp-rd': [tk('R', 'd')] }, label: [tk('R', 'd')], pts: 2 }""",
    'vdsq-prod')

# ---------- ②-3 A_v 的 g_m · R_d（乘法，同级不区分顺序） ----------
rep("""                                    // g_m（点等效模型旁的 g_m 标注作答）
                                    { ansIds: ['q-gm'], label: [tk('g', 'm')], pts: 6 },
                                    // R_d（整理/等效态下点下挂件同样按 comp-rd 计）
                                    { ansIds: ['comp-rd'], label: [tk('R', 'd')], pts: 6 }""",
    """                                    // g_m · R_d 同级相乘，不区分先后——两空均可点 g_m 标注或 R_d（同 grp 查重）
                                    { ansIds: ['q-gm', 'comp-rd'], grp: 'av-prod', labels: { 'q-gm': [tk('g', 'm')], 'comp-rd': [tk('R', 'd')] }, label: [tk('g', 'm')], pts: 6 },
                                    { ansIds: ['q-gm', 'comp-rd'], grp: 'av-prod', labels: { 'q-gm': [tk('g', 'm')], 'comp-rd': [tk('R', 'd')] }, label: [tk('R', 'd')], pts: 6 }""",
    'av-prod')

# ---------- ③ 文案：分值注释同步（V_DSQ 1/1/3 → 1/2/2） ----------
rep('// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/1/1、1/1/3（15）= 24（I_DQ 方程三空：I_DO 2 分、V_GSQ 1 分、V_T 1 分，各对应图中同名红标）',
    '// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/1/1、1/2/2（15）= 24（I_DQ 方程三空：I_DO 2 分、V_GSQ 1 分、V_T 1 分；V_DSQ 乘积两空 2/2 同分可交换）',
    'pts-comment')

if '--dry' in sys.argv:
    print('[DRY] %d reps:' % len(reps), ','.join(reps))
    sys.exit(0)

shutil.copyfile(SRC, '/tmp/cs-g1.before-orderfree.html')
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('[OK] %d reps:' % len(reps), ','.join(reps))
