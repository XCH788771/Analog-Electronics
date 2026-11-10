# -*- coding: utf-8 -*-
"""cs-g3 第122轮原子补丁：
① 整理态 RG1 下挂后收起电源轨左段（280—578）与 R_D 上方节点 (578,5)
② 等效态栅极线收紧（左端 195→215 / 右端与红点、v_gs 462→442，C1 链随右移 20）
   D 极线左端 530→570（红点随动）、受控源模型整体 +40、g_m·v_gs 移菱形右下、接地符号右移 32
逐对唯一性校验，全过才写盘。"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

pairs = [
# ── ① node-rd-top：R_D 上端节点加 id ──
('''            <path class="hot" d="M 578 5 V 63.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle cx="578" cy="5" r="7" fill="#ffffff" pointer-events="none"/>''',
 '''            <path class="hot" d="M 578 5 V 63.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            <circle id="node-rd-top" cx="578" cy="5" r="7" fill="#ffffff" pointer-events="none"/>'''),

# ── ① moveCompDown('comp-rg1')：轨左段收起 + 节点隐藏 ──
('''            // R_G1 下挂后收起分压节点上段导线（302→352 段已无连接意义；节点改接 R_G1 下挂支路左行线）
            const wrg2a = document.querySelector('g[data-id="wire-rg2a"] path');
            if (wrg2a) wrg2a.setAttribute('d', 'M 280 352 V 412');''',
 '''            // R_G1 下挂后收起分压节点上段导线（302→352 段已无连接意义；节点改接 R_G1 下挂支路左行线）
            const wrg2a = document.querySelector('g[data-id="wire-rg2a"] path');
            if (wrg2a) wrg2a.setAttribute('d', 'M 280 352 V 412');
            // 第122轮：R_G1 脱开后电源轨左段（280—578）左端悬空——收起轨左段与 R_D 上方节点 (578,5)
            //（右段 578—640 仍接 R_D 上端与 +V_DD；全下挂时整轨照旧收起）
            const wvr = document.querySelector('g[data-id="wire-vdd-rail"] path');
            if (wvr) wvr.setAttribute('d', 'M 578 5 H 640');
            const nrt = document.getElementById('node-rd-top');
            if (nrt) nrt.style.opacity = '0';'''),

# ── ① resetCircuit：恢复轨全长 + 节点 ──
('''        const wrg2a = document.querySelector('g[data-id="wire-rg2a"] path');
        if (wrg2a) wrg2a.setAttribute('d', 'M 280 302 V 412');''',
 '''        const wrg2a = document.querySelector('g[data-id="wire-rg2a"] path');
        if (wrg2a) wrg2a.setAttribute('d', 'M 280 302 V 412');
        const wvr = document.querySelector('g[data-id="wire-vdd-rail"] path');
        if (wvr) wvr.setAttribute('d', 'M 280 5 H 640');
        const nrt = document.getElementById('node-rd-top');
        if (nrt) nrt.style.opacity = '';'''),

# ── ② 等效态：V_i—C_1 链右移 20（vi-in 右端延到 C_1 新左板 201）──
("""        setD('g[data-id="wire-vi-in"] path',   up ? 'M 110 216.25 H 181' : 'M 110 282 H 181');""",
 """        setD('g[data-id="wire-vi-in"] path',   up ? 'M 110 216.25 H 201' : 'M 110 282 H 181');"""),

# ── ② C_1 板/标注/绿桥右移 20（第122轮）──
('''        const c1 = q('g[data-id="comp-c1"]');
        if (c1) {
            c1.querySelectorAll('line').forEach(l => { l.setAttribute('y1', up ? '194.25' : '260'); l.setAttribute('y2', up ? '238.25' : '304'); });
            const t = c1.querySelector('text'); if (t) t.setAttribute('y', up ? '178' : '244');
        }
        const fc1 = q('#fx-c1 line');
        if (fc1) { fc1.setAttribute('y1', y); fc1.setAttribute('y2', y); }''',
 '''        const c1 = q('g[data-id="comp-c1"]');
        if (c1) {
            // 第122轮：等效态 C_1 链整体右移 20px（板 201/215），与栅极线新左端 (215) 保持相接
            c1.querySelectorAll('line').forEach((l, i) => {
                l.setAttribute('y1', up ? '194.25' : '260'); l.setAttribute('y2', up ? '238.25' : '304');
                const px = up ? (i === 0 ? '201' : '215') : (i === 0 ? '181' : '195');
                l.setAttribute('x1', px); l.setAttribute('x2', px);
            });
            const t = c1.querySelector('text');
            if (t) { t.setAttribute('y', up ? '178' : '244'); t.setAttribute('x', up ? '208' : '188'); }
        }
        const fc1 = q('#fx-c1 line');
        if (fc1) { fc1.setAttribute('y1', y); fc1.setAttribute('y2', y);
                   fc1.setAttribute('x1', up ? '201' : '181'); fc1.setAttribute('x2', up ? '215' : '195'); }'''),

# ── ② 栅极线：左端 195→215、右端 462→442 ──
("""        setD('g[data-id="wire-in-gate"] path', up ? 'M 195 216.25 H 462' : 'M 195 282 H 502');""",
 """        setD('g[data-id="wire-in-gate"] path', up ? 'M 215 216.25 H 442' : 'M 195 282 H 502');"""),

# ── ② G 端子 / G 红点 / S 红点 / 地节点 / v_gs：462→442 ──
("""        const gt = q('#fx-tmodel circle'); if (gt) { gt.setAttribute('cx', up ? '462' : '502'); gt.setAttribute('cy', y); }""",
 """        const gt = q('#fx-tmodel circle'); if (gt) { gt.setAttribute('cx', up ? '442' : '502'); gt.setAttribute('cy', y); }"""),
("""        const gd = q('#fx-dot-g circle'); if (gd) { gd.setAttribute('cx', up ? '462' : '502'); gd.setAttribute('cy', y); }""",
 """        const gd = q('#fx-dot-g circle'); if (gd) { gd.setAttribute('cx', up ? '442' : '502'); gd.setAttribute('cy', y); }"""),
("""        if (sd) { sd.setAttribute('cx', up ? '462' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }""",
 """        if (sd) { sd.setAttribute('cx', up ? '442' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }"""),
('''        const gndS = document.getElementById('fx-gnd-node-s');
        if (gndS) gndS.style.opacity = up ? '1' : '0';''',
 '''        const gndS = document.getElementById('fx-gnd-node-s');
        if (gndS) {
            gndS.style.opacity = up ? '1' : '0';
            const gsc = gndS.querySelector('circle');
            if (gsc) gsc.setAttribute('cx', up ? '442' : '462');   // 第122轮随 S 红点左移 20
        }'''),
("""            const vx = up ? '462' : '502';""",
 """            const vx = up ? '442' : '502';"""),

# ── ② D 极线左端 530→570（红点随动）＋ 受控源模型静态 +40 的动态配套：接地符号右移 32 ──
("""            if (ts[0]) ts[0].setAttribute('y', up ? '256' : '322');     // ＋（随 G 端子）
            if (ts[1]) ts[1].setAttribute('y', up ? '367' : '400');     // v_gs（－ 478 不动=地电位）
        }
    }""",
 """            if (ts[0]) ts[0].setAttribute('y', up ? '256' : '322');     // ＋（随 G 端子）
            if (ts[1]) ts[1].setAttribute('y', up ? '367' : '400');     // v_gs（－ 478 不动=地电位）
        }
        // 第122轮：D 极水平导线等效态左端缩短 40px（530→570，红点随动）——受控源模型静态坐标已整体 +40；
        // 接地符号等效态右移 32px（578→610），避让受控源落地节点 (570,525)
        const dd = q('#fx-dot-d circle'); if (dd) dd.setAttribute('cx', up ? '570' : '530');
        setD('g[data-id="wire-rd-lead"] path', up ? 'M 570 216.25 H 690' : 'M 530 216.25 H 578 V 161.5');
        const gnde = q('g[data-id="comp-gnd"]');
        if (gnde) gnde.setAttribute('transform', up ? 'translate(32,0)' : 'translate(0,0)');
    }"""),

# ── ② fx-t-src 受控源支路 +40（静态坐标；仅等效态显示）──
('''                    <path class="hot keepw" d="M 530 216.25 V 220 H 554" fill="none" stroke="#ffffff" stroke-width="3.5"/>''',
 '''                    <path class="hot keepw" d="M 570 216.25 V 220 H 594" fill="none" stroke="#ffffff" stroke-width="3.5"/>'''),
('''                    <path class="hot" d="M 554 220 L 586 245 L 554 270 L 522 245 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>''',
 '''                    <path class="hot" d="M 594 220 L 626 245 L 594 270 L 562 245 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>'''),
('''                    <path class="hot keepw" d="M 554 270 V 274 H 530 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>''',
 '''                    <path class="hot keepw" d="M 594 270 V 274 H 570 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'''),
('''                    <!-- 受控源支路直落公共地线（S 极=地电位，原 S 极入地导线等效态整体移除）；落地 T 交有节点 -->
                    <circle cx="530" cy="525" r="7" fill="#ffffff"/>''',
 '''                    <!-- 受控源支路直落公共地线（S 极=地电位，原 S 极入地导线等效态整体移除）；落地 T 交有节点 (570,525) -->
                    <circle cx="570" cy="525" r="7" fill="#ffffff"/>'''),

# ── ② fx-t-id 箭头 +40 ──
('''                    <line x1="554" y1="225" x2="554" y2="248" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="554,263 545,248 563,248" fill="#ff5252" stroke="none"/>''',
 '''                    <line x1="594" y1="225" x2="594" y2="248" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="594,263 585,248 603,248" fill="#ff5252" stroke="none"/>'''),

# ── ② g_m·v_gs 标注移菱形右下 (590,318)：右随 +40 会压 R_D 下挂线 (690)，改置下方空区 ──
('''                <!-- 受控源电流数值标注 g_m·v_gs：第5问作答后与箭头同现（菱形右侧；第2/3关填空点它作答） -->
                <g id="fx-t-idlabel" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）" opacity="0">
                    <rect class="hot" x="586" y="224" width="82" height="44" fill="none" stroke="none"/>
                    <text class="hot-label" x="590" y="256" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>''',
 '''                <!-- 受控源电流数值标注 g_m·v_gs：第5问作答后与箭头同现（第122轮移菱形右下 590,318——
                     原右侧位随模型 +40 后右缘 712 会压 R_D 下挂线 x=690；第2/3关填空点它作答） -->
                <g id="fx-t-idlabel" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）" opacity="0">
                    <rect class="hot" x="584" y="290" width="82" height="44" fill="none" stroke="none"/>
                    <text class="hot-label" x="590" y="318" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>'''),

# ── ② 函数头注释补第122轮 ──
('''    // 红点与极柱横移随动，S 红点落到公共地线 (462,525) 并补地节点；R_G1/R_G2 整体右移 55px（225/335）使 R_G 居中；
    // resetCircuit(false) 全部复原（R_G 回水平、y=282、G 端点 502、S 红点回沟道）''',
 '''    // 红点与极柱横移随动，S 红点落到公共地线 (462,525) 并补地节点；R_G1/R_G2 整体右移 55px（225/335）使 R_G 居中；
    // resetCircuit(false) 全部复原（R_G 回水平、y=282、G 端点 502、S 红点回沟道）
    // 第122轮：等效态栅极线再收紧（左端 195→215、右端与 G/S 红点、v_gs 柱、G 端子 462→442），C_1 链右移 20px 保持相接；
    // D 极水平导线左端缩短 40px（530→570，红点随动）、受控源模型整体 +40（静态）、g_m·v_gs 移菱形右下、接地符号右移 32'''),
]

for i, (o, n) in enumerate(pairs):
    k = c.count(o)
    if k != 1:
        print('FAIL pair %d count=%d' % (i, k))
        sys.exit(1)
for o, n in pairs:
    c = c.replace(o, n)
io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d pairs' % len(pairs))
