# -*- coding: utf-8 -*-
"""cs-g1 第2关：① V_GSQ 的 + 号右移 20px；② I_DO 与 V_T 改为方框（可填空）"""
import io, os, shutil, sys

SRC = 'cs-g1.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
orig = s
reps = []

def rep(old, new, tag):
    global s
    c = s.count(old)
    assert c == 1, '[%s] count=%d' % (tag, c)
    s = s.replace(old, new, 1)
    reps.append(tag)

# ---------- ① V_GSQ 的 + 右移 20px（热区随动） ----------
rep('<rect class="hot" x="346" y="296" width="28" height="28" fill="none" stroke="none"/>',
    '<rect class="hot" x="366" y="296" width="28" height="28" fill="none" stroke="none"/>',
    'plus-hot')

rep('<text class="hot-label" x="360" y="322" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>',
    '<text class="hot-label" x="380" y="322" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>',
    'plus-text')

# ---------- ② I_DO 与 V_T 改为方框 ----------
# 2-1 I_DQ 表达式：I_DO 固定符号 → 方框
rep("fullExpr: [[tk('I', 'DQ'), tk('='), tk('I', 'DO'), tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],\n                                blanks: [\n                                    { ansIds: ['q-vth'], label: [tk('V', 'GS(th)')], pts: 4 }\n                                ]",
    "fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],\n                                blanks: [\n                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },\n                                    { ansIds: ['q-vt'], label: [tk('V', 'T')], pts: 2 }\n                                ]",
    'fill2-boxes')

# 2-2 分值注释配平
rep('// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、4、1/1/3（15）= 24（I_DO 为已知参数改固定符号，其 2 分并入 V_GS(th) 空）',
    '// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/2、1/1/3（15）= 24（I_DQ 方程两空：I_DO 2 分、V_T 2 分，各对应图中同名红标）',
    'pts-comment')

# 2-3 复盘文案改 V_T
rep("why: '静态工作点：V_GSQ 由 R_g1、R_g2 分压求得；I_DQ 由转移特性方程 I_DO(V_GSQ/V_GS(th) − 1)² 求得；V_DSQ = V_DD − I_DQ·R_d。'",
    "why: '静态工作点：V_GSQ 由 R_g1、R_g2 分压求得；I_DQ 由转移特性方程 I_DO(V_GSQ/V_T − 1)² 求得；V_DSQ = V_DD − I_DQ·R_d。'",
    'why-vt')

# 2-4 已知行：V_GS(th) → V_T（与方程、图中红标一致）
rep('、V<tspan class="sub">GS(th)</tspan>、I<tspan class="sub">DO</tspan></text>',
    '、V<tspan class="sub">T</tspan>、I<tspan class="sub">DO</tspan></text>',
    'known-line')

# 2-5 悬停词条：标明可点击填入
rep("'q-vt':         { text: '<b>V<sub>T</sub></b><br>开启电压（阈值电压）：V<sub>GS</sub> 超过 V<sub>T</sub> 才形成导电沟道，是转移特性方程中的门槛电压',",
    "'q-vt':         { text: '<b>V<sub>T</sub></b><br>开启电压（阈值电压）：V<sub>GS</sub> 超过 V<sub>T</sub> 才形成导电沟道，是转移特性方程分母的门槛电压（第 2 关可点击填入方框）',",
    'anno-vt')

rep("'q-ido':        { text: '<b>I<sub>DO</sub></b><br>饱和漏极电流：转移特性参数（已知量），本图中只标符号、不画箭头',",
    "'q-ido':        { text: '<b>I<sub>DO</sub></b><br>饱和漏极电流：转移特性参数（已知量），本图中只标符号、不画箭头（第 2 关可点击填入方框）',",
    'anno-ido')

# 2-6 data-name 同步
rep('data-id="q-vt" data-name="开启电压 V_T（阈值电压）"',
    'data-id="q-vt" data-name="开启电压 V_T（第 2 关填入 I_DQ 方程分母）"',
    'name-vt')

if '--dry' in sys.argv:
    print('[DRY] %d reps would apply:' % len(reps), ','.join(reps))
    sys.exit(0)

shutil.copyfile(SRC, '/tmp/cs-g1.before-box2.html')
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('[OK] %d reps:' % len(reps), ','.join(reps))
