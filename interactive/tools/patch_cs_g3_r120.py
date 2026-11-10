# -*- coding: utf-8 -*-
# 第120轮：① RG 下引竖线右移至节点(390)与栅极条底角(502)中点 446，R_G 文字/电阻右移至水平导线中间（两侧引线各 56.5px 对称）
#          ② 整理态（RD 下移后）输出水平导线下移与 D 极对齐（y 161.5→216.25），C_2/短接桥/输出线/R_L 上引线/V_o 随动
#          ③ 等效态参照 cs-g1：输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25），原 S 极到地端导线整体移除
#             （wire-rs-top/lead/bot + fx-rs + node-rs-gnd），受控源支路（fx-t-src）下延直落地线 (530,525)
#          ④ 修复 setCircuitShift 基准 x=18 与静态 translate(-12,260) 不一致（重玩后整图右移30 的隐藏 bug）
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

pairs = [
# ── ① RG 下引竖线右移 390→446，节点随动；R_G 体/标签右移至 280-446 中点 363 ──
('<path class="hot" d="M 390 282 V 352 H 376.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot" d="M 446 282 V 352 H 389.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
('<circle cx="390" cy="282" r="7" fill="#ffffff" pointer-events="none"/>',
 '<circle cx="446" cy="282" r="7" fill="#ffffff" pointer-events="none"/>'),
('<rect class="hot" x="323.5" y="338.5" width="53" height="27" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<rect class="hot" x="336.5" y="338.5" width="53" height="27" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
('<text class="hot-label" x="350" y="400" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">R<tspan class="sub">G</tspan></text>',
 '<text class="hot-label" x="363" y="400" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">R<tspan class="sub">G</tspan></text>'),
('<path class="hot" d="M 323.5 352 H 280" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot" d="M 336.5 352 H 280" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
# ── ② rarr-rd（仅整理/等效态可见）顶部改为 D 极水平位 216.25（静态改）──
('<path class="hot keepw" d="M 690 161.5 V 317" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot keepw" d="M 690 216.25 V 317" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
('<circle cx="690" cy="161.5" r="7" fill="#ffffff"/>',
 '<circle cx="690" cy="216.25" r="7" fill="#ffffff"/>'),
# ── ③ fx-t-src 受控源支路下延直落地线 (530,525)，落地点加节点圆 ──
('<path class="hot keepw" d="M 554 270 V 274 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '''<path class="hot keepw" d="M 554 270 V 274 H 530 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 受控源支路直落公共地线（S 极=地电位，原 S 极入地导线等效态整体移除）；落地 T 交有节点 -->
                    <circle cx="530" cy="525" r="7" fill="#ffffff"/>'''),
# S 极入地节点圆（wire-gnd-m 内）：等效态源极路径移除后随收
('<circle cx="578" cy="525" r="7" fill="#ffffff" pointer-events="none"/>',
 '<circle id="node-rs-gnd" cx="578" cy="525" r="7" fill="#ffffff" pointer-events="none"/>'),
# ── ④ setCircuitShift 基准修复（-12 与静态一致）──
("    // 交流等效态整图上移 40px（基极线、模型与地线一并上移，给下半部留出空间）\n    function setCircuitShift(up) {\n        const w = document.getElementById('circuit-wrap');\n        if (w) w.setAttribute('transform', 'translate(18, ' + (up ? 220 : 260) + ') scale(1)');",
 "    // 整图位移基准（第115轮整体左移30：x=-12；第120轮起等效态不再整图上移，本函数仅复位用）\n    function setCircuitShift(up) {\n        const w = document.getElementById('circuit-wrap');\n        if (w) w.setAttribute('transform', 'translate(-12, ' + (up ? 220 : 260) + ') scale(1)');"),
# ── ③ 等效注释更新 ──
('''    // 交流等效最终布局（第1关第3步选「等效」时启用）：
    // 移除场效应管本体后，漏极—源极之间改画受控电流源（fx-tmodel，逐问揭示），栅极引线末端留 G 端子（G-S 开路）；
    // 输入回路、R_G、分压电阻、整理态下挂件（R_G1/R_D）、R_S 短接桥均保持原位，无需重绘、无需整图上移
    // ★换案例：等效态切换（本案例为场效应管新结构：仅切模型层，电路骨架不动）
    function showEquiv() {
        fadeGroup('comp-t', true);      // 场效应管本体移除
        showFx('fx-tmodel', true);      // 微变等效模型层点亮（父层 PE 暂 none，五连问完成后才可点击）
    }''',
 '''    // 交流等效最终布局（第1关第3步选「等效」时启用；第120轮起参照 cs-g1 口径）：
    // 移除场效应管本体后，漏极—源极之间改画受控电流源（fx-tmodel，逐问揭示），栅极引线末端留 G 端子（G-S 开路）；
    // 输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25），原 S 极到地端导线整体移除（受控源支路直落地线）；
    // R_G、分压电阻（经分压节点接线）、整理态下挂件（R_G1/R_D）保持原位，无需整图上移
    function showEquiv() {
        fadeGroup('comp-t', true);      // 场效应管本体移除
        showFx('fx-tmodel', true);      // 微变等效模型层点亮（父层 PE 暂 none，五连问完成后才可点击）
        applyEquivInput(true);          // 输入主线上移与 D 极对齐（V_i/C_1/短接桥/下引线/交叉点/G 端子与红点/极性柱随动）
        // 原 S 极到地端之间的导线整体移除：源极接线、R_S 上下引线、短接桥、入地节点
        fadeGroup('wire-rs-top', true); fadeGroup('wire-rs-lead', true); fadeGroup('wire-rs-bot', true);
        showFx('fx-rs', false);
        showFx('node-rs-gnd', false);   // R_S 入地节点：源极路径移除后地线在此直通，节点圆多余
    }'''),
# fx-tmodel 头注释坐标口径
('                 等效布局：G 端子留在栅极引线末端 (502,282)（G-S 开路，不画支路）；',
 '                 等效布局：G 端子留在栅极引线末端 (502,216.25)（G-S 开路，不画支路；随输入主线上移）；'),
('                 G 在栅极引线末端 (502,282)，D 在沟道 d 段中点 (530,216.25)，S 在沟道 s 段中点 (530,274) -->',
 '                 G 在栅极引线末端 (502,216.25)（等效态随输入主线上移），D 在沟道 d 段中点 (530,216.25)，S 在沟道 s 段中点 (530,274) -->'),
# ── ② moveCompDown(comp-rd) 增补输出线下移 ──
('''            const nd = document.getElementById('node-drain');
            if (nd) nd.style.opacity = '0';''',
 '''            const nd = document.getElementById('node-drain');
            if (nd) nd.style.opacity = '0';
            applyTidyOutput(true);   // 输出水平导线下移与 D 极对齐（y 161.5→216.25），C_2/输出线/R_L 上引线/V_o 随动'''),
# ── 两个随动函数插入（moveCompDown 之后、TQUIZ 注释之前）──
('''            showFx('fx-vdd', false);
        }
        render();
    }
    /* ★换案例：TQUIZ 等效问答（与 cs-g1 同口径五问）''',
 '''            showFx('fx-vdd', false);
        }
        render();
    }
    // 第120轮：整理态输出水平导线下移与 D 极对齐（y 161.5→216.25）——D 极引线直行至 R_D 下挂点 (690)，
    // C_2（板 194.25-238.25、标注 179）/短接桥/输出线/R_L 上引线/V_o（＋229.75、V_o 384、热区 204-564）随动；
    // resetCircuit(false) 恢复默认（线 y=161.5，经 (578,161.5) 转角上行）
    function applyTidyOutput(down) {
        const q = s => document.querySelector(s);
        const setD = (s, d) => { const e = q(s); if (e) e.setAttribute('d', d); };
        setD('g[data-id="wire-rd-lead"] path',   down ? 'M 530 216.25 H 690' : 'M 530 216.25 H 578 V 161.5');
        setD('g[data-id="wire-drain-out"] path', down ? 'M 690 216.25 H 707' : 'M 578 161.5 H 707');
        setD('g[data-id="wire-c2-out"] path',    down ? 'M 721 216.25 H 850' : 'M 721 161.5 H 850');
        setD('g[data-id="wire-rl-top"] path',    down ? 'M 850 216.25 V 317' : 'M 850 161.5 V 317');
        const c2 = q('g[data-id="comp-c2"]');
        if (c2) {
            c2.querySelectorAll('line').forEach(l => { l.setAttribute('y1', down ? '194.25' : '139.5'); l.setAttribute('y2', down ? '238.25' : '183.5'); });
            const t = c2.querySelector('text'); if (t) t.setAttribute('y', down ? '179' : '124');
        }
        const fc2 = q('#fx-c2 line');
        if (fc2) { fc2.setAttribute('y1', down ? '216.25' : '161.5'); fc2.setAttribute('y2', down ? '216.25' : '161.5'); }
        const vo = q('g[data-id="comp-vo"]');
        if (vo) {
            const ts = vo.querySelectorAll('text');
            if (ts[0]) ts[0].setAttribute('y', down ? '229.75' : '175');   // ＋（随上拐角）
            if (ts[1]) ts[1].setAttribute('y', down ? '384' : '357');      // V_o（＋/－ 中点）
            const r = vo.querySelector('rect');
            if (r) { r.setAttribute('y', down ? '204' : '150'); r.setAttribute('height', down ? '360' : '415'); }
        }
    }
    // 第120轮：等效态输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25）——V_i 上端子、C_1（板 194.25-238.25、
    // 标注 178）、短接桥、栅极线、R_G 下引线（446 竖线上延）、分压竖线交叉点 (280,216.25)、G 端子/G 红点、
    // v_gs 极性柱（＋256、v_gs 367；－478 不动=地电位）随动；resetCircuit(false) 恢复默认（y=282）
    function applyEquivInput(up) {
        const q = s => document.querySelector(s);
        const setD = (s, d) => { const e = q(s); if (e) e.setAttribute('d', d); };
        const y = up ? '216.25' : '282';
        setD('g[data-id="wire-vi-in"] path',   up ? 'M 110 216.25 H 181' : 'M 110 282 H 181');
        const vit = q('g[data-id="comp-vi"] circle'); if (vit) vit.setAttribute('cy', y);   // 上端子（下端子 525 不动）
        const c1 = q('g[data-id="comp-c1"]');
        if (c1) {
            c1.querySelectorAll('line').forEach(l => { l.setAttribute('y1', up ? '194.25' : '260'); l.setAttribute('y2', up ? '238.25' : '304'); });
            const t = c1.querySelector('text'); if (t) t.setAttribute('y', up ? '178' : '244');
        }
        const fc1 = q('#fx-c1 line');
        if (fc1) { fc1.setAttribute('y1', y); fc1.setAttribute('y2', y); }
        setD('g[data-id="wire-in-gate"] path', up ? 'M 195 216.25 H 502' : 'M 195 282 H 502');
        setD('g[data-id="wire-rg-drop"] path', up ? 'M 446 216.25 V 352 H 389.5' : 'M 446 282 V 352 H 389.5');
        const rgn = q('g[data-id="wire-rg-drop"] circle'); if (rgn) rgn.setAttribute('cy', y);
        setD('g[data-id="wire-rg1b"] path',  up ? 'M 280 170 V 216.25' : 'M 280 170 V 282');
        setD('g[data-id="wire-rg1b2"] path', up ? 'M 280 216.25 V 302' : 'M 280 282 V 302');
        const gt = q('#fx-tmodel circle'); if (gt) gt.setAttribute('cy', y);   // G 端子（首个 circle）
        const gd = q('#fx-dot-g circle'); if (gd) gd.setAttribute('cy', y);    // G 红点
        const vg = q('#fx-t-vgs');
        if (vg) {
            const ts = vg.querySelectorAll('text');
            if (ts[0]) ts[0].setAttribute('y', up ? '256' : '322');   // ＋（随 G 端子）
            if (ts[1]) ts[1].setAttribute('y', up ? '367' : '400');   // v_gs（－ 478 不动）
        }
    }
    /* ★换案例：TQUIZ 等效问答（与 cs-g1 同口径五问）'''),
# ── resetCircuit 恢复 ──
('''        const ncg = document.getElementById('node-cs-gnd');
        if (ncg) ncg.style.opacity = '';
        hideMenu();''',
 '''        const ncg = document.getElementById('node-cs-gnd');
        if (ncg) ncg.style.opacity = '';
        const nrg = document.getElementById('node-rs-gnd');
        if (nrg) nrg.style.opacity = '';
        applyTidyOutput(false);   // 输出水平导线回默认位（y=161.5）
        applyEquivInput(false);   // 输入主线回默认位（y=282）、源极路径复现
        hideMenu();'''),
]

for i, (o, n) in enumerate(pairs):
    k = c.count(o)
    if k != 1:
        print('FAIL pair %d count=%d : %s' % (i, k, o[:90]))
        sys.exit(1)
for o, n in pairs:
    c = c.replace(o, n)
io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d pairs' % len(pairs))
