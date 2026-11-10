# -*- coding: utf-8 -*-
"""cs-g1 三项修订（2026-11-01 第二轮）：
① 电流箭头并入 q-idq 组（qlabel-layer 内）：仅第 2 关显示（L1/L3 整层隐藏、L4 dyn 分支隐藏、默认态不显示）。
② 移除 q-ido（I_DO）：组+ANNOS 删除；qlabels 去掉；I_DQ 表达式中 I_DO 改为固定符号 token（已知参数不作答），
   其 2 分移至 V_GS(th) 空（2→4），总分 24 配平不变。
③ V_GSQ 移到截图绿框位：＋(408,272) 栅条左侧栅极高度、V_GSQ(526,330) 沟道右下、－(526,366) 其下；
   热区拆两块（＋一块、文字+－一块）。V_DSQ 柱右移 75px（x 545→620）让位（I_DO 已删，空间空闲）。
唯一性校验：任一 old 串出现次数 != 1 即中止，不写盘。
"""
import io, sys, os, shutil

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cs-g1.html'))
BAK = '/tmp/cs-g1.before-qmark2.html'

with io.open(SRC, 'r', encoding='utf-8', newline='') as f:
    s = f.read()
orig = s

REPS = [
    # ---- ① 箭头从 wire-d-stub 移除 ----
    ('''            <line x1="511" y1="172" x2="511" y2="214" stroke="#ff5252" stroke-width="5"/>
            <polygon points="511,238 500,215 522,215" fill="#ff5252" stroke="none"/>
''', ''),
    ('data-name="漏极接线（漏极节点—T 漏极；红色箭头指示漏极电流方向）"',
     'data-name="漏极接线（漏极节点—T 漏极）"'),

    # ---- ① 箭头并入 q-idq 组（第 2 关随标注显示） ----
    ('''                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ（漏极电流箭头处）">
                    <rect class="hot" x="530" y="183" width="100" height="42" fill="none" stroke="none"/>''',
     '''                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ（漏极电流箭头处）">
                    <line x1="511" y1="172" x2="511" y2="214" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="511,238 500,215 522,215" fill="#ff5252" stroke="none"/>
                    <rect class="hot" x="530" y="183" width="100" height="42" fill="none" stroke="none"/>'''),

    # ---- ② 移除 q-ido 组 ----
    ('''                <g class="interactive" data-id="q-ido" data-name="转移特性参数 I_DO">
                    <rect class="hot" x="592" y="270" width="96" height="52" fill="none" stroke="none"/>
                    <text class="hot-label" x="640" y="304" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">I<tspan class="sub">DO</tspan></text>
                </g>
''', ''),

    # ---- ② ANNOS q-ido 删除 ----
    ('''        'q-ido':        { text: '<b>I<sub>DO</sub></b><br>增强型 MOS 管转移特性参数：v<sub>GS</sub> = 2V<sub>GS(th)</sub> 时的漏极电流',
                          parts: [{ text: '这是IDO，增强型场效应管的转移特性参数，是山源电压等于两倍开启电压时的漏极电流。' }] },
''', ''),

    # ---- ② I_DQ 填空：I_DO 固定符号，V_GS(th) 空 2→4 分 ----
    ("""                                fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],
                                blanks: [
                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },
                                    { ansIds: ['q-vth'], label: [tk('V', 'GS(th)')], pts: 2 }
                                ]""",
     """                                fullExpr: [[tk('I', 'DQ'), tk('='), tk('I', 'DO'), tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],
                                blanks: [
                                    { ansIds: ['q-vth'], label: [tk('V', 'GS(th)')], pts: 4 }
                                ]"""),
    ('// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/2、1/1/3（15）= 24',
     '// 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、4、1/1/3（15）= 24（I_DO 为已知参数改固定符号，其 2 分并入 V_GS(th) 空）'),

    # ---- ② qlabels 去 q-ido ----
    ("qlabels: ['q-ido', 'q-vth', 'q-idq', 'q-vdsq'],",
     "qlabels: ['q-vth', 'q-idq', 'q-vdsq'],"),

    # ---- ③ V_GSQ 移到绿框位（＋ 栅条左/栅极高度，V_GSQ 沟道右下，－ 其下） ----
    ('''                <g class="interactive" data-id="q-vth" data-name="栅源静态电压 V_GSQ（＋/− 标出极性）">
                    <rect class="hot" x="498" y="346" width="90" height="108" fill="none" stroke="none"/>
                    <text class="hot-label" x="545" y="374" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="545" y="410" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GSQ</tspan></text>
                    <text class="hot-label" x="545" y="446" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>''',
     '''                <g class="interactive" data-id="q-vth" data-name="栅源静态电压 V_GSQ（＋/− 标出极性）">
                    <rect class="hot" x="395" y="244" width="26" height="32" fill="none" stroke="none"/>
                    <rect class="hot" x="492" y="296" width="72" height="76" fill="none" stroke="none"/>
                    <text class="hot-label" x="408" y="272" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="526" y="330" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GSQ</tspan></text>
                    <text class="hot-label" x="526" y="366" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>'''),

    # ---- ③ V_DSQ 柱右移 75px（x 545→620，I_DO 已删空间空闲） ----
    ('''                <g class="interactive" data-id="q-vdsq" data-name="漏源静态电压 V_DSQ（＋/− 标出极性）">
                    <rect class="hot" x="498" y="230" width="90" height="108" fill="none" stroke="none"/>
                    <text class="hot-label" x="545" y="258" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="545" y="294" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">DSQ</tspan></text>
                    <text class="hot-label" x="545" y="330" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>''',
     '''                <g class="interactive" data-id="q-vdsq" data-name="漏源静态电压 V_DSQ（＋/− 标出极性）">
                    <rect class="hot" x="583" y="230" width="90" height="108" fill="none" stroke="none"/>
                    <text class="hot-label" x="620" y="258" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text class="hot-label" x="620" y="294" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">DSQ</tspan></text>
                    <text class="hot-label" x="620" y="330" fill="#ff5252" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>'''),
]

fail = False
for i, (old, new) in enumerate(REPS, 1):
    n = s.count(old)
    if n != 1:
        print('[FAIL] 第%d处 old 出现 %d 次（须为1）: %r' % (i, n, old[:70]))
        fail = True
if fail:
    print('中止：未写盘')
    sys.exit(1)

for old, new in REPS:
    s = s.replace(old, new, 1)

# 残留校验
for token in ['q-ido']:
    if token in s:
        print('[FAIL] 残留 %s' % token)
        sys.exit(1)

shutil.copyfile(SRC, BAK)
with io.open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('OK %d 处替换完成，长度 %d → %d，备份 %s' % (len(REPS), len(orig), len(s), BAK))
