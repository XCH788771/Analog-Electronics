# -*- coding: utf-8 -*-
"""cs-g3 第121轮：等效态 R_G 竖直化 + R_G1/R_G2 整体右移 + 栅极导线缩短 & S 红点落地
三个改动全部落在「等效态」applyEquivInput(up)，resetCircuit 走 up=false 完整复原。
"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()
pairs = []

# ---------- 1) 地线节点圆加 id（R_G2 右移后落点随动） ----------
pairs.append((
'''        <g class="interactive" data-id="wire-gnd-l" data-name="公共地线·输入段（V_i 下端—R_G2 下端）">
            <path class="hot" d="M 110 525 H 280" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="280" cy="525" r="7" fill="#ffffff" pointer-events="none"/>''',
'''        <g class="interactive" data-id="wire-gnd-l" data-name="公共地线·输入段（V_i 下端—R_G2 下端）">
            <path class="hot" d="M 110 525 H 280" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle id="node-rg2-gnd" cx="280" cy="525" r="7" fill="#ffffff" pointer-events="none"/>'''))

# ---------- 2) S 极接地点节点（等效态红点正下方，红点隐藏后仍标示接地点） ----------
pairs.append((
'''            <!-- 等效问答端点红点（G/D/S，持续闪烁；引擎按问显隐）。
                 放在 fx-layer 最末：保证红点画在模型导线之上不被遮挡。
                 G 在栅极引线末端 (502,216.25)（等效态随输入主线上移），D 在沟道 d 段中点 (530,216.25)，S 在沟道 s 段中点 (530,274) -->''',
'''            <!-- 等效态地节点（第121轮）：S 极＝地电位，红点落在公共地线上 (462,525)，
                 与其正下方节点圆同点；红点隐藏后节点仍标示该接地点 -->
            <g id="fx-gnd-node-s" opacity="0">
                <circle cx="462" cy="525" r="7" fill="#ffffff"/>
            </g>

            <!-- 等效问答端点红点（G/D/S，持续闪烁；引擎按问显隐）。
                 放在 fx-layer 最末：保证红点画在模型导线之上不被遮挡。
                 G 在栅极引线末端（第121轮缩短 40px）：默认 (502,282) → 等效态 (462,216.25)；
                 D 在沟道 d 段中点 (530,216.25)；S 默认在沟道 s 段中点 (530,274)，
                 等效态落到公共地线 (462,525)——与 G 红点垂直同轴 -->'''))

# ---------- 3) applyEquivInput 扩展：R_G 竖直化 + R_G1/R_G2 右移 + 栅极线缩短 + 红点/极性柱随动 ----------
old_js = '''        setD('g[data-id="wire-in-gate"] path', up ? 'M 195 216.25 H 502' : 'M 195 282 H 502');
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
        }'''

new_js = '''        // 栅极水平引线：等效态右端止于 G 端子（第121轮再缩短 40px：502→462，红点/极性柱随动）
        setD('g[data-id="wire-in-gate"] path', up ? 'M 195 216.25 H 462' : 'M 195 282 H 502');
        // —— R_G：等效态逆时针转 90° 竖直化，与 R_G2 同轴（x=280）串在栅极引线与分压节点之间 ——
        //    体 257.5-310.5（上下引线各 41.25/41.5 对称），标签移到本体右侧同轴位 (309.5,291.5)
        const rgr = q('g[data-id="comp-rg"] rect');
        if (rgr) {
            rgr.setAttribute('x', up ? '266.5' : '336.5');
            rgr.setAttribute('y', up ? '257.5' : '338.5');
            rgr.setAttribute('width', up ? '27' : '53');
            rgr.setAttribute('height', up ? '53' : '27');
        }
        const rgt = q('g[data-id="comp-rg"] text');
        if (rgt) {
            rgt.setAttribute('x', up ? '309.5' : '363');
            rgt.setAttribute('y', up ? '291.5' : '400');
            rgt.setAttribute('text-anchor', up ? 'start' : 'middle');
        }
        // 上引线（栅极引线→R_G 上端，含栅极引线上的接线节点）／下引线（R_G 下端→分压节点）
        setD('g[data-id="wire-rg-drop"] path', up ? 'M 280 216.25 V 257.5' : 'M 446 282 V 352 H 389.5');
        const rgn = q('g[data-id="wire-rg-drop"] circle');
        if (rgn) { rgn.setAttribute('cx', up ? '280' : '446'); rgn.setAttribute('cy', up ? y : '282'); }
        setD('g[data-id="wire-rg-link"] path', up ? 'M 280 310.5 V 352' : 'M 336.5 352 H 280');
        setD('g[data-id="wire-rg1b"] path',  up ? 'M 280 170 V 216.25' : 'M 280 170 V 282');
        setD('g[data-id="wire-rg1b2"] path', up ? 'M 280 216.25 V 302' : 'M 280 282 V 302');
        // —— R_G1 / R_G2 整体右移 55px（170→225 / 280→335）：R_G(280) 正对两者中点 ——
        const r1 = q('#rarr-rg1');
        if (r1) {
            const p1 = r1.querySelectorAll('path');
            if (p1[0]) p1[0].setAttribute('d', up ? 'M 280 352 H 225 V 412' : 'M 280 352 H 170 V 412');
            if (p1[1]) p1[1].setAttribute('d', up ? 'M 225 465 V 525' : 'M 170 465 V 525');
            const rc = r1.querySelector('rect'); if (rc) rc.setAttribute('x', up ? '211.5' : '156.5');
            const cc = r1.querySelector('circle'); if (cc) cc.setAttribute('cx', up ? '225' : '170');
            const tt = r1.querySelector('text'); if (tt) tt.setAttribute('x', up ? '248.5' : '193.5');
        }
        const r2 = q('g[data-id="comp-rg2"]');
        if (r2) {
            const rc = r2.querySelector('rect'); if (rc) rc.setAttribute('x', up ? '321.5' : '266.5');
            const tt = r2.querySelector('text'); if (tt) tt.setAttribute('x', up ? '364.5' : '309.5');
        }
        // R_G2 上下接线与入地节点随右移；下段起止随整理态是否已下挂（352 起 / 302 起）
        const mv = (S.draw[S.level - 1] || {}).moved || {};
        setD('g[data-id="wire-rg2a"] path', up ? 'M 280 352 H 335 V 412'
                                             : (mv['comp-rg1'] ? 'M 280 352 V 412' : 'M 280 302 V 412'));
        setD('g[data-id="wire-rg2b"] path', up ? 'M 335 465 V 525' : 'M 280 465 V 525');
        const nrg2 = document.getElementById('node-rg2-gnd');
        if (nrg2) nrg2.setAttribute('cx', up ? '335' : '280');
        // —— G 端子 / G 红点 / v_gs 极性柱横向随引线端点（502→462）——
        const gt = q('#fx-tmodel circle'); if (gt) { gt.setAttribute('cx', up ? '462' : '502'); gt.setAttribute('cy', y); }
        const gd = q('#fx-dot-g circle'); if (gd) { gd.setAttribute('cx', up ? '462' : '502'); gd.setAttribute('cy', y); }
        // S 红点：默认沟道 s 段中点 (530,274) → 等效态落到公共地线 (462,525)，与 G 红点垂直同轴
        const sd = q('#fx-dot-s circle');
        if (sd) { sd.setAttribute('cx', up ? '462' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }
        const gndS = document.getElementById('fx-gnd-node-s');
        if (gndS) gndS.style.opacity = up ? '1' : '0';
        const vg = q('#fx-t-vgs');
        if (vg) {
            const ts = vg.querySelectorAll('text');
            const vx = up ? '462' : '502';
            ts.forEach(t => t.setAttribute('x', vx));                   // 极性柱随 G 端子横向移动
            if (ts[0]) ts[0].setAttribute('y', up ? '256' : '322');     // ＋（随 G 端子）
            if (ts[1]) ts[1].setAttribute('y', up ? '367' : '400');     // v_gs（－ 478 不动=地电位）
        }'''
pairs.append((old_js, new_js))

# ---------- 4) applyEquivInput 头注释同步 ----------
pairs.append((
'''    // 第120轮：等效态输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25）——V_i 上端子、C_1（板 194.25-238.25、
    // 标注 178）、短接桥、栅极线、R_G 下引线（446 竖线上延）、分压竖线交叉点 (280,216.25)、G 端子/G 红点、
    // v_gs 极性柱（＋256、v_gs 367；－478 不动=地电位）随动；resetCircuit(false) 恢复默认（y=282）''',
'''    // 第120轮：等效态输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25）——V_i 上端子、C_1（板 194.25-238.25、
    // 标注 178）、短接桥、栅极线、分压竖线交叉点 (280,216.25)、G 端子/G 红点、v_gs 极性柱随动；
    // 第121轮：R_G 逆时针 90° 竖直化（与 R_G2 同轴 x=280，串于栅极引线—分压节点之间），栅极引线右端再缩 40px（→462）、
    // 红点与极柱横移随动，S 红点落到公共地线 (462,525) 并补地节点；R_G1/R_G2 整体右移 55px（225/335）使 R_G 居中；
    // resetCircuit(false) 全部复原（R_G 回水平、y=282、G 端点 502、S 红点回沟道）'''))

for i, (o, n) in enumerate(pairs):
    k = c.count(o)
    if k != 1:
        print('FAIL pair %d count=%d' % (i, k))
        sys.exit(1)
for o, n in pairs:
    c = c.replace(o, n)
io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d pairs' % len(pairs))
