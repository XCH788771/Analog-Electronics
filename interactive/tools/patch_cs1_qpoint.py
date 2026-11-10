# -*- coding: utf-8 -*-
"""cs-g1 新增第 2 关「静态工作点估算」（2026-10-29 用户三项之 3，纯表达式版）：
- 直流分析阶段插入 mix 关：V_GSQ（分压）→ I_DQ（转移特性方程）→ V_DSQ，框架+表达式交错；
- 计分改两阶段四关：12 + 24 + 22 + 42 = 100（L1 18→12；L4 60→42：框架 6→4、填空 8/8/8/8/10→6×5）；
- 新增 3 枚电量标注 q-ido / q-vth / q-idq（qlabel-layer，红色，仅本关显示）；
- 已知行补参数符号 V_GS(th)、I_DO；updateQlabels 支持 cfg.qlabels 过滤；
- 调试钩子 ts/tidy 目标关 2→3（交流等效后移），S.draw[1]→S.draw[2]。
所有替换带唯一性校验，任一失配即中止不写盘。
"""
import io
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.normpath(os.path.join(D, '..', 'cs-g1.html'))

NEW_STEP = '''                    {
                        // 框架 + 表达式交错关（静态工作点）：V_GSQ → I_DQ → V_DSQ，每项先选框架、再填符号
                        // 分值：3 个框架题各 3 分（9）+ 填空 2/2/1/1、2/2、1/1/3（15）= 24
                        kind: 'mix', title: '第 2 关 · 静态工作点估算', pts: 24, short: '工作点估算', stageUnits: 0,
                        subLine: '每个指标先选计算框架，再点虚线框填符号',
                        subs: [
                            {
                                type: 'fw', name: 'V<tspan class="sub">GSQ</tspan> 框架', qpts: 3, pen: 2, qid: 'comp-rg2',
                                fwQ: '栅源静态电压 V<tspan class="sub">GSQ</tspan> 的表达式框架：',
                                frameworks: [
                                    // 正确：栅极电流为零 → R_g1、R_g2 分压
                                    { tokens: [tk('V', 'GSQ'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])], correct: true },
                                    // 干扰①：分母漏一只电阻
                                    { tokens: [tk('V', 'GSQ'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }], [{ box: 1 }])] },
                                    // 干扰②：漏乘 V_DD（只剩分压比）
                                    { tokens: [tk('V', 'GSQ'), tk('='), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])] }
                                ]
                            },
                            {
                                type: 'fill', name: 'V<tspan class="sub">GSQ</tspan> 表达式',
                                fullExpr: [[tk('V', 'GSQ'), tk('='), { box: 1 }, tk('·'), fr([{ box: 1 }], [{ box: 1 }, tk('+'), { box: 1 }])]],
                                blanks: [
                                    { ansIds: ['comp-vdd'], label: [tk('V', 'DD')], pts: 2 },
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 2 },
                                    { ansIds: ['comp-rg1'], label: [tk('R', 'g1')], pts: 1 },
                                    { ansIds: ['comp-rg2'], label: [tk('R', 'g2')], pts: 1 }
                                ]
                            },
                            {
                                type: 'fw', name: 'I<tspan class="sub">DQ</tspan> 框架', qpts: 3, pen: 2, qid: 'comp-t',
                                fwQ: '静态漏极电流 I<tspan class="sub">DQ</tspan> 的表达式框架（转移特性方程）：',
                                frameworks: [
                                    // 正确：I_DQ = I_DO(V_GSQ / V_GS(th) − 1)²
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')], correct: true },
                                    // 干扰①：漏掉 −1
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk(')²')] },
                                    // 干扰②：减序颠倒（1 − V_GSQ/V_GS(th)）
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), tk('1'), tk('−'), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk(')²')] }
                                ]
                            },
                            {
                                type: 'fill', name: 'I<tspan class="sub">DQ</tspan> 表达式',
                                fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([tk('V', 'GSQ')], [{ box: 1 }]), tk('−'), tk('1'), tk(')²')]],
                                blanks: [
                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },
                                    { ansIds: ['q-vth'], label: [tk('V', 'GS(th)')], pts: 2 }
                                ]
                            },
                            {
                                type: 'fw', name: 'V<tspan class="sub">DSQ</tspan> 框架', qpts: 3, pen: 2, qid: 'comp-rd',
                                fwQ: '漏源静态电压 V<tspan class="sub">DSQ</tspan> 的表达式框架：',
                                frameworks: [
                                    // 正确：V_DSQ = V_DD − I_DQ·R_d
                                    { tokens: [tk('V', 'DSQ'), tk('='), { box: 1 }, tk('−'), { box: 1 }, tk('·'), { box: 1 }], correct: true },
                                    // 干扰①：极性错（+）
                                    { tokens: [tk('V', 'DSQ'), tk('='), { box: 1 }, tk('+'), { box: 1 }, tk('·'), { box: 1 }] },
                                    // 干扰②：漏掉电源项（只剩 I_DQ·R_d）
                                    { tokens: [tk('V', 'DSQ'), tk('='), { box: 1 }, tk('·'), { box: 1 }] }
                                ]
                            },
                            {
                                type: 'fill', name: 'V<tspan class="sub">DSQ</tspan> 表达式',
                                fullExpr: [[tk('V', 'DSQ'), tk('='), { box: 1 }, tk('−'), { box: 1 }, tk('·'), { box: 1 }]],
                                blanks: [
                                    { ansIds: ['comp-vdd'], label: [tk('V', 'DD')], pts: 1 },
                                    { ansIds: ['q-idq'], label: [tk('I', 'DQ')], pts: 1 },
                                    { ansIds: ['comp-rd'], label: [tk('R', 'd')], pts: 3 }
                                ]
                            }
                        ],
                        qlabels: ['q-ido', 'q-vth', 'q-idq'],
                        announce: '进入第二关，估算静态工作点。依次完成栅源电压、漏极电流、漏源电压三个指标：每个指标先选择计算框架，再点虚线框，点击电路中对应的元件或电量标注填入符号，共24分。',
                        extra: '框架答对后进入该指标的表达式填空；先点虚线框，再点电路中对应的元件或电量标注。',
                        doneSay: '静态工作点三个指标的框架与表达式全部完成。',
                        why: '静态工作点：V_GSQ 由 R_g1、R_g2 分压求得；I_DQ 由转移特性方程 I_DO(V_GSQ/V_GS(th) − 1)² 求得；V_DSQ = V_DD − I_DQ·R_d。'
                    }
'''

NEW_QLABELS = '''                <g class="interactive" data-id="q-ido" data-name="转移特性参数 I_DO">
                    <rect class="hot" x="560" y="270" width="96" height="52" fill="none" stroke="none"/>
                    <text class="hot-label" x="608" y="304" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">I<tspan class="sub">DO</tspan></text>
                </g>
                <g class="interactive" data-id="q-vth" data-name="开启电压 V_GS(th)">
                    <rect class="hot" x="548" y="342" width="120" height="52" fill="none" stroke="none"/>
                    <text class="hot-label" x="608" y="376" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">GS(th)</tspan></text>
                </g>
                <g class="interactive" data-id="q-idq" data-name="静态漏极电流 I_DQ">
                    <rect class="hot" x="560" y="414" width="96" height="52" fill="none" stroke="none"/>
                    <text class="hot-label" x="608" y="448" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">I<tspan class="sub">DQ</tspan></text>
                </g>
'''

NEW_ANNOS = '''        'q-ido':        { text: '<b>I<sub>DO</sub></b><br>增强型 MOS 管转移特性参数：v<sub>GS</sub> = 2V<sub>GS(th)</sub> 时的漏极电流',
                          parts: [{ text: '这是IDO，增强型场效应管的转移特性参数，是栅源电压等于两倍开启电压时的漏极电流。' }] },
        'q-vth':        { text: '<b>V<sub>GS(th)</sub></b><br>增强型 MOS 管的开启电压：v<sub>GS</sub> 超过它之后导电沟道才形成',
                          parts: [{ text: '这是V GS th，增强型场效应管的开启电压，栅源电压超过它之后导电沟道才形成。' }] },
        'q-idq':        { text: '<b>I<sub>DQ</sub></b><br>静态漏极电流：由转移特性方程代入 V<sub>GSQ</sub> 求得',
                          parts: [{ text: '这是IDQ，静态漏极电流，由转移特性方程代入栅源静态电压求得。' }] },
'''

REPS = [
    # ---------- 头部注释 ----------
    ('    /* ▼▼▼ 替换区 C：本案例关卡配置 GAME_CONFIG（两阶段三关 18+22+60=100）▼▼▼',
     '    /* ▼▼▼ 替换区 C：本案例关卡配置 GAME_CONFIG（两阶段四关 12+24+22+42=100）▼▼▼', 1, '区C标题'),
    ('''    //   L1 直流通路（v_i 置零短路、V_DD 保留、C_b1 断路）；L2 交流微变等效（v_i 保留、V_DD 置零接地、C_b1 短路→整理→等效四问）；
    //   L3 动态指标：A_v = −g_m·R_d、R_i = R_g1∥R_g2、R_o ≈ R_d''',
     '''    //   L1 直流通路（v_i 置零短路、V_DD 保留、C_b1 断路）；L2 静态工作点估算（V_GSQ/I_DQ/V_DSQ 纯表达式）；
    //   L3 交流微变等效（v_i 保留、V_DD 置零接地、C_b1 短路→整理→等效四问）；
    //   L4 动态指标：A_v = −g_m·R_d、R_i = R_g1∥R_g2、R_o ≈ R_d''', 1, '关卡描述注释'),
    ('（cs-g1 三关：2）', '（cs-g1 四关：2）', 1, 'nStatic注释'),
    # ---------- L1 计分 18 → 12 ----------
    ("title: '第 1 关 · 绘制直流通路', pts: 18,", "title: '第 1 关 · 绘制直流通路', pts: 12,", 1, 'L1 pts'),
    ('答对获得18分。', '答对获得12分。', 1, 'L1 announce'),
    # ---------- 原第2/3关顺延为第3/4关 ----------
    ("title: '第 2 关 · 绘制交流微变等效电路'", "title: '第 3 关 · 绘制交流微变等效电路'", 1, 'L3 title'),
    ("announce: '进入第二关，绘制交流微变等效电路", "announce: '进入第三关，绘制交流微变等效电路", 1, 'L3 announce'),
    ("kind: 'mix', title: '第 3 关 · 动态指标计算', pts: 60,", "kind: 'mix', title: '第 4 关 · 动态指标计算', pts: 42,", 1, 'L4 title/pts'),
    ('顺序是电压放大倍数、输入电阻、输出电阻，共60分。', '顺序是电压放大倍数、输入电阻、输出电阻，共42分。', 1, 'L4 announce'),
    ('qpts: 6, pen: 3', 'qpts: 4, pen: 3', 3, 'L4 框架分'),
    ('pts: 8 }', 'pts: 6 }', 4, 'L4 填空8分'),
    ('pts: 10 }', 'pts: 6 }', 1, 'L4 填空10分'),
    ('                        // 分值：3 个框架题各 6 分（18）+ 填空 8/8/8/8/10（42）= 60；全站 18+22+60 = 100',
     '                        // 分值：3 个框架题各 4 分（12）+ 填空 6/6/6/6/6（30）= 42；全站 12+24+22+42 = 100', 1, 'L4 分值注释'),
    # ---------- 插入第 2 关（工作点估算） ----------
    ('''                        why: '画直流通路：C_b1 开路；输入端口 v_i 置零后短接，随 C_b1 断开的输入回路一并移除；直流电源 +V_DD 保留。'
                    }
                ]
            },
            {
                name: '动态分析',''',
     '''                        why: '画直流通路：C_b1 开路；输入端口 v_i 置零后短接，随 C_b1 断开的输入回路一并移除；直流电源 +V_DD 保留。'
                    },
''' + NEW_STEP + '''                ]
            },
            {
                name: '动态分析',''', 1, '插入工作点关'),
    # ---------- updateQlabels：支持 cfg.qlabels 过滤 ----------
    ('''        layer.querySelectorAll('g.interactive').forEach(g => {
            if (!dyn) { g.style.opacity = ''; g.style.pointerEvents = ''; g.classList.remove('hit-off'); return; }
            const isGm = g.dataset.id === 'q-gm';''',
     '''        const wantIds = (!dyn && on && L.cfg.qlabels) ? L.cfg.qlabels : null;   // 工作点关：只显本关所需电量标注
        layer.querySelectorAll('g.interactive').forEach(g => {
            if (!dyn) {
                const want = !wantIds || wantIds.indexOf(g.dataset.id) >= 0;
                g.style.opacity = want ? '' : '0';
                g.style.pointerEvents = want ? '' : 'none';
                g.classList.toggle('hit-off', !want);
                return;
            }
            const isGm = g.dataset.id === 'q-gm';''', 1, 'updateQlabels'),
    # ---------- 新增电量标注 SVG（qlabel-layer 内，q-gm 之后） ----------
    ('''                    <text class="hot-label" x="440" y="368" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>
                </g>
            </g>''',
     '''                    <text class="hot-label" x="440" y="368" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>
                </g>
''' + NEW_QLABELS + '''            </g>''', 1, '电量标注SVG'),
    # ---------- ANNOS：三个新标注 ----------
    ("反映栅源电压对漏极电流的控制能力。' }] },",
     "反映栅源电压对漏极电流的控制能力。' }] },\n" + NEW_ANNOS.rstrip('\n'), 1, 'ANNOS'),
    # ---------- 已知行补参数符号 ----------
    ('V<tspan class="sub">DD</tspan>=5V</text>',
     'V<tspan class="sub">DD</tspan>=5V、V<tspan class="sub">GS(th)</tspan>、I<tspan class="sub">DO</tspan></text>', 1, '已知行'),
    # ---------- 调试钩子：ts/tidy 目标关 2 → 3 ----------
    ('        if ((mt || mty) && n === 2) {', '        if ((mt || mty) && n === 3) {', 1, 'ts/tidy 关卡号'),
    ('        const d4 = S.draw[1];', '        const d4 = S.draw[2];', 1, 'ts/tidy draw 索引'),
]


def main():
    raw = io.open(P, 'rb').read()
    s = raw.decode('utf-8').replace('\r\n', '\n')
    crlf = b'\r\n' in raw

    bad = []
    for old, new, exp, tag in REPS:
        n = s.count(old)
        if n != exp:
            bad.append('%s：命中 %d 次（应为 %d）' % (tag, n, exp))
    if bad:
        print('中止，未写盘：')
        for b in bad:
            print('  - ' + b)
        return 1

    for old, new, exp, tag in REPS:
        s = s.replace(old, new)
    out = s if not crlf else s.replace('\n', '\r\n')
    io.open(P, 'wb').write(out.encode('utf-8'))
    print('已写入（%d 组替换）：%s' % (len(REPS), P))
    return 0


if __name__ == '__main__':
    sys.exit(main())
