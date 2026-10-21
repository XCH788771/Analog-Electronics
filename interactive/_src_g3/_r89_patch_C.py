# -*- coding: utf-8 -*-
# round-89（C 文件）：第86轮由白实线框改来的 { dbox: 1 } 只是"显示用虚框"，点不起、不能填。
# 用户要求：这些框应与其他方框一样可点击填写（β / I_EQ）。
#   · 简化框架 fill 的 I_EQ 位：dbox → box，blanks 补首项 { q-ieq }（与非简化版一致）
#   · A_v 的 β（首位 + (1+β)）：dbox → box，blanks 补 2 个 β 空（不加 grp，引擎只在同 grp 内查重）
#   · R_i 的 (1+β) 中 β：dbox → box，blanks 补 1 个 β 空
# 分值配平：第3关 43、第5关 21 不变
#   第3关：简化框架 fw qpts 6→5（+1 空 I_EQ 各路线）
#   第5关：A_v/R_i/R_o 三个框架 qpts 4→3（9）+ 11 空 12 分（A_v 6 / R_i 5 / R_o 1）= 21
import io, sys, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_C.txt')
s = io.open(P, 'r', encoding='utf-8', newline='').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        print('FAIL count=%d (want %d) for: %s' % (c, n, old[:80]))
        sys.exit(1)
    s = s.replace(old, new)
    print('OK  %s' % old[:72])

# ── A. 简化 fill（subs / subsC 各 1 处）：dbox→box + blanks 补 I_EQ ──────────
pat = (r"fullExpr: \[\[tk\('I', 'CQ'\), tk\('≈'\), \{ dbox: 1 \}, tk\('≈'\), "
       r"fr\(\[\{ box: 1 \}, tk\('−'\), \{ box: 1 \}\], \[\{ box: 1 \}, tk\('\+'\), \{ box: 1 \}\]\)\]\],\n"
       r"(\s*)blanks: \[\n")
new = ("fullExpr: [[tk('I', 'CQ'), tk('≈'), { box: 1 }, tk('≈'), "
       "fr([{ box: 1 }, tk('−'), { box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])]],\n"
       "\\1blanks: [\n"
       "\\1    { ansIds: ['q-ieq'], label: [tk('I', 'EQ')], pts: 1 },\n")
m = re.findall(pat, s)
if len(m) != 2:
    print('FAIL 简化 fill 匹配数 = %d (want 2)' % len(m)); sys.exit(1)
s = re.sub(pat, new, s)
print('OK  简化 fill dbox→box + 补 I_EQ 空 ×2')

# 简化框架 fw qpts 6→5（subs/subsC 两处，为新增 I_EQ 空腾 1 分，第3关仍 43）
rep("type: 'fw', name: 'I<tspan class=\"sub\">CQ</tspan>≈□ 简化框架', qpts: 6, pen: 2,",
    "type: 'fw', name: 'I<tspan class=\"sub\">CQ</tspan>≈□ 简化框架', qpts: 5, pen: 2,", 2)

# ── B. A_v：框架与表达式的 β 位 dbox→box ─────────────────────────────────────
rep("{ tokens: [tk('A', 'v'), tk('='), tk('−'), { dbox: 1 }, tk('·'), fr([{ box: 1 }, tk('∥'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }])], correct: true },",
    "{ tokens: [tk('A', 'v'), tk('='), tk('−'), { box: 1 }, tk('·'), fr([{ box: 1 }, tk('∥'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }])], correct: true },")
rep("{ tokens: [tk('A', 'v'), tk('='), tk('−'), { dbox: 1 }, tk('·'), fr([{ box: 1 }, tk('+'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }])] },",
    "{ tokens: [tk('A', 'v'), tk('='), tk('−'), { box: 1 }, tk('·'), fr([{ box: 1 }, tk('+'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }])] },")
rep("{ tokens: [tk('A', 'v'), tk('='), { dbox: 1 }, tk('·'), fr([{ box: 1 }, tk('∥'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }])] }",
    "{ tokens: [tk('A', 'v'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }, tk('∥'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }])] }")
rep("fullExpr: [[tk('A', 'v'), tk('='), tk('−'), { dbox: 1 }, tk('·'), fr([{ box: 1 }, tk('∥'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }])]],",
    "fullExpr: [[tk('A', 'v'), tk('='), tk('−'), { box: 1 }, tk('·'), fr([{ box: 1 }, tk('∥'), { box: 1 }], [{ box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }])]],")

# A_v blanks：4 → 6（β / R_C / R_L / r_be / β / R_E1，各 1 分 = 6）
rep("""                                blanks: [
                                    // 并联因子 R_C∥R_L 与相加因子 r_be+R_e1 均可交换顺序（并集 ansIds + 同 grp）
                                    { ansIds: ['comp-rc', 'comp-rl'], grp: 'av-par',
                                      labels: { 'comp-rc': [tk('R', 'C')], 'comp-rl': [tk('R', 'L')] },
                                      label: [tk('R', 'C')], pts: 1 },
                                    { ansIds: ['comp-rc', 'comp-rl'], grp: 'av-par',
                                      labels: { 'comp-rc': [tk('R', 'C')], 'comp-rl': [tk('R', 'L')] },
                                      label: [tk('R', 'L')], pts: 1 },
                                    // r_be + R_E1 同级相加 → 填写顺序不固定（第72轮）
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'av-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('r', 'be')], pts: 1 },
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'av-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('R', 'E1')], pts: 1 }
                                ]""",
    """                                blanks: [
                                    // 第89轮：β 由不可填虚框改为可填空（点 β 标注或晶体管均可）
                                    { ansIds: ['q-beta', 'comp-t'], label: [tk('β')], pts: 1 },
                                    // 并联因子 R_C∥R_L 与相加因子 r_be+R_e1 均可交换顺序（并集 ansIds + 同 grp）
                                    { ansIds: ['comp-rc', 'comp-rl'], grp: 'av-par',
                                      labels: { 'comp-rc': [tk('R', 'C')], 'comp-rl': [tk('R', 'L')] },
                                      label: [tk('R', 'C')], pts: 1 },
                                    { ansIds: ['comp-rc', 'comp-rl'], grp: 'av-par',
                                      labels: { 'comp-rc': [tk('R', 'C')], 'comp-rl': [tk('R', 'L')] },
                                      label: [tk('R', 'L')], pts: 1 },
                                    // r_be + R_E1 同级相加 → 填写顺序不固定（第72轮）
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'av-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('r', 'be')], pts: 1 },
                                    // (1+β) 中的 β：与首位 β 不加 grp —— 引擎只在同 grp 内查重
                                    { ansIds: ['q-beta', 'comp-t'], label: [tk('β')], pts: 1 },
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'av-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('R', 'E1')], pts: 1 }
                                ]""")

# ── C. R_i：(1+β) 中 β dbox→box + blanks 补 1 个 β 空 ────────────────────────
rep("{ tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), tk('('), { box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }, tk(')')], correct: true },",
    "{ tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), tk('('), { box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }, tk(')')], correct: true },")
rep("{ tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('+'), tk('('), { box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }, tk(')')] },",
    "{ tokens: [tk('R', 'i'), tk('='), { box: 1 }, tk('+'), tk('('), { box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }, tk(')')] },")
rep("fullExpr: [[tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), tk('('), { box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { dbox: 1 }, tk(')'), { box: 1 }, tk(')')]],",
    "fullExpr: [[tk('R', 'i'), tk('='), { box: 1 }, tk('∥'), tk('('), { box: 1 }, tk('+'), tk('('), tk('1'), tk('+'), { box: 1 }, tk(')'), { box: 1 }, tk(')')]],")

# R_i blanks：3 → 4（R_B 2 / r_be 1 / β 1 / R_E1 1 = 5）
rep("""                                blanks: [
                                    { ansIds: ['comp-rb'], label: [tk('R', 'B')], pts: 2 },
                                    // r_be + R_E1 同级相加 → 填写顺序不固定（第72轮）
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'ri-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('r', 'be')], pts: 1 },
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'ri-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('R', 'E1')], pts: 1 }
                                ]""",
    """                                blanks: [
                                    { ansIds: ['comp-rb'], label: [tk('R', 'B')], pts: 2 },
                                    // r_be + R_E1 同级相加 → 填写顺序不固定（第72轮）
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'ri-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('r', 'be')], pts: 1 },
                                    // 第89轮：(1+β) 中的 β 改为可填空
                                    { ansIds: ['q-beta', 'comp-t'], label: [tk('β')], pts: 1 },
                                    { ansIds: ['comp-t', 'comp-re1'], grp: 'ri-den',
                                      labels: { 'comp-t': [tk('r', 'be')], 'comp-re1': [tk('R', 'E1')] },
                                      label: [tk('R', 'E1')], pts: 1 }
                                ]""")

# ── D. 第5关配平：三个框架 qpts 4→3（9 + 12 = 21）─────────────────────────────
rep("type: 'fw', name: 'A<tspan class=\"sub\">v</tspan> 框架', qpts: 4, pen: 2,",
    "type: 'fw', name: 'A<tspan class=\"sub\">v</tspan> 框架', qpts: 3, pen: 2,")
rep("type: 'fw', name: 'R<tspan class=\"sub\">i</tspan> 框架', qpts: 4, pen: 2,",
    "type: 'fw', name: 'R<tspan class=\"sub\">i</tspan> 框架', qpts: 3, pen: 2,")
rep("type: 'fw', name: 'R<tspan class=\"sub\">o</tspan> 框架', qpts: 4, pen: 2,",
    "type: 'fw', name: 'R<tspan class=\"sub\">o</tspan> 框架', qpts: 3, pen: 2,")
rep("// 分值：3 个框架题各 4 分（12）+ 8 个空共 9 分 = 21（第69轮：为第 3 关腾出 3 分，全站仍 100）",
    "// 分值：3 个框架题各 3 分（9）+ 11 个空共 12 分 = 21（第89轮：β 改可填空，框架各让 1 分）")

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('WROTE %s' % P)
print('剩余 dbox 数 =', s.count('{ dbox: 1 }'))
