# -*- coding: utf-8 -*-
"""cs-g3 第123轮原子补丁（逐对唯一性校验，全过才写盘）
① 等效态接地符号移到公共地线中点 (480,525) 并加节点
② v_gs 极性柱的 － 号下移（478→505）靠近地线
③ 等效态 S 红点与 D 红点垂直同轴（442→570）
④ 受控源：上顶点与 D 极导线端点 x=570 对齐、整体下移至垂直导线中点 (570,371)，
   菱形内加水平线连接左右顶点；i_d 箭头随菱形
"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

pairs = [
    # ---------- ① 接地节点：改名为 fx-gnd-node 并落在 (480,525) ----------
    ("""            <!-- 等效态地节点（第121轮）：S 极＝地电位，红点落在公共地线上 (462,525)，
                 与其正下方节点圆同点；红点隐藏后节点仍标示该接地点 -->
            <g id="fx-gnd-node-s" opacity="0">
                <circle cx="462" cy="525" r="7" fill="#ffffff"/>
            </g>""",
     """            <!-- 等效态接地节点（第123轮）：接地符号等效态移到公共地线中点 (480,525)，
                 该处补节点圆标示接地点（源极侧接地点由 fx-t-src 落地节点 (570,525) 标示） -->
            <g id="fx-gnd-node" opacity="0">
                <circle cx="480" cy="525" r="7" fill="#ffffff"/>
            </g>"""),

    # ---------- ④ fx-t-src 几何重排 ----------
    ("""                <!-- D-S 受控电流源支路（第4问揭示）：漏极节点直下源极节点，菱形符号居中（不含 g_m·v_gs 标注） -->
                <g id="fx-t-src" opacity="0">
                    <path class="hot keepw" d="M 570 216.25 V 220 H 594" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot" d="M 594 220 L 626 245 L 594 270 L 562 245 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot keepw" d="M 594 270 V 274 H 570 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 受控源支路直落公共地线（S 极=地电位，原 S 极入地导线等效态整体移除）；落地 T 交有节点 (570,525) -->
                    <circle cx="570" cy="525" r="7" fill="#ffffff"/>
                </g>""",
     """                <!-- D-S 受控电流源支路（第4问揭示）：第123轮起整条支路竖直——上顶点与 D 极导线端点 (570,216.25)
                     同轴、菱形下移到垂直导线中点 (570,371)；菱形内加水平线连接左右顶点（不含 g_m·v_gs 标注） -->
                <g id="fx-t-src" opacity="0">
                    <path class="hot keepw" d="M 570 216.25 V 346" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot" d="M 570 346 L 602 371 L 570 396 L 538 371 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot keepw" d="M 538 371 H 602" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <path class="hot keepw" d="M 570 396 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 受控源支路直落公共地线（S 极=地电位，原 S 极入地导线等效态整体移除）；落地 T 交有节点 (570,525) -->
                    <circle cx="570" cy="525" r="7" fill="#ffffff"/>
                </g>"""),

    # ---------- ④ i_d 箭头随菱形 ----------
    ("""                <g id="fx-t-id" opacity="0">
                    <line x1="594" y1="225" x2="594" y2="248" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="594,263 585,248 603,248" fill="#ff5252" stroke="none"/>
                </g>""",
     """                <g id="fx-t-id" opacity="0">
                    <line x1="570" y1="352" x2="570" y2="374" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="570,389 561,374 579,374" fill="#ff5252" stroke="none"/>
                </g>"""),

    # ---------- fx-tmodel 头注释同步（几何已多轮变化，统一到现状） ----------
    ("""            <!-- 场效应管微变等效模型（G-S 开路 + D-S 受控电流源 g_m·v_gs）；逐问显示，完成后保留可读。
                 等效布局：G 端子留在栅极引线末端 (502,216.25)（G-S 开路，不画支路；随输入主线上移）；
                 D-S 受控源支路直连沟道 d 段中点 (530,216.25) 与 s 段中点 (530,274)，菱形符号居中 (554,245)；
                 v_gs 极性柱（G 端子正下方）第2问揭示；受控源支路第4问揭示；i_d 箭头与 g_m·v_gs
                 标注（菱形右侧，填空关点它作答）第5问同现 -->""",
     """            <!-- 场效应管微变等效模型（G-S 开路 + D-S 受控电流源 g_m·v_gs）；逐问显示，完成后保留可读。
                 等效布局（第123轮现值）：G 端子留在栅极引线末端 (442,216.25)（G-S 开路，不画支路）；
                 D-S 受控源支路为 x=570 的竖直支路（D 极线端点 216.25 → 地线 525），菱形居中 (570,371)
                 且内部横线连接左右顶点 (538/602,371)；
                 v_gs 极性柱（G 端子正下方，＋256 / v_gs 367 / －505 贴近地线）第2问揭示；
                 受控源支路第4问揭示；i_d 箭头与 g_m·v_gs 标注（菱形右上，填空关点它作答）第5问同现 -->"""),

    # ---------- ③ S 红点与 D 红点同轴 ----------
    ("""        // S 红点：默认沟道 s 段中点 (530,274) → 等效态落到公共地线 (462,525)，与 G 红点垂直同轴
        const sd = q('#fx-dot-s circle');
        if (sd) { sd.setAttribute('cx', up ? '442' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }
        const gndS = document.getElementById('fx-gnd-node-s');
        if (gndS) {
            gndS.style.opacity = up ? '1' : '0';
            const gsc = gndS.querySelector('circle');
            if (gsc) gsc.setAttribute('cx', up ? '442' : '462');   // 第122轮随 S 红点左移 20
        }""",
     """        // S 红点：默认沟道 s 段中点 (530,274) → 等效态落到公共地线 (570,525)，与 D 极导线端点红点垂直同轴
        //   （第123轮：原 (462,525) 与 G 红点同轴，改为与受控源落地点/D 红点同轴，正对受控源支路）
        const sd = q('#fx-dot-s circle');
        if (sd) { sd.setAttribute('cx', up ? '570' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }
        const gndT = document.getElementById('fx-gnd-node');   // 接地符号接地点节点（等效态才显示）
        if (gndT) gndT.style.opacity = up ? '1' : '0';"""),

    # ---------- ② － 号下移 ----------
    ("""            if (ts[0]) ts[0].setAttribute('y', up ? '256' : '322');     // ＋（随 G 端子）
            if (ts[1]) ts[1].setAttribute('y', up ? '367' : '400');     // v_gs（－ 478 不动=地电位）""",
     """            if (ts[0]) ts[0].setAttribute('y', up ? '256' : '322');     // ＋（随 G 端子）
            if (ts[1]) ts[1].setAttribute('y', up ? '367' : '400');     // v_gs
            if (ts[2]) ts[2].setAttribute('y', up ? '505' : '478');     // －（第123轮下移贴地线 525）"""),

    # ---------- ① 接地符号移到地线中点 ----------
    ("""        // 第122轮：D 极水平导线等效态左端缩短 40px（530→570，红点随动）——受控源模型静态坐标已整体 +40；
        // 接地符号等效态右移 32px（578→610），避让受控源落地节点 (570,525)""",
     """        // 第122轮：D 极水平导线等效态左端缩短 40px（530→570，红点随动）——受控源模型静态坐标已整体 +40；
        // 第123轮：接地符号等效态移到公共地线中点 578→480（translate -98），并加接地点节点 fx-gnd-node"""),
    ("""        const gnde = q('g[data-id="comp-gnd"]');
        if (gnde) gnde.setAttribute('transform', up ? 'translate(32,0)' : 'translate(0,0)');""",
     """        const gnde = q('g[data-id="comp-gnd"]');
        if (gnde) gnde.setAttribute('transform', up ? 'translate(-98,0)' : 'translate(0,0)');"""),

    # ---------- resetCircuit 隐藏清单补 fx-gnd-node ----------
    ("""         'fx-t-src', 'fx-t-id', 'fx-t-vgs', 'fx-t-idlabel', 'fx-dot-g', 'fx-dot-d', 'fx-dot-s'].forEach(id => {""",
     """         'fx-t-src', 'fx-t-id', 'fx-t-vgs', 'fx-t-idlabel', 'fx-dot-g', 'fx-dot-d', 'fx-dot-s',
         'fx-gnd-node'].forEach(id => {"""),
]

for i, (o, n) in enumerate(pairs):
    k = c.count(o)
    if k != 1:
        print('FAIL pair %d count=%d  |%s' % (i, k, o.strip().splitlines()[0][:80]))
        sys.exit(1)

for o, n in pairs:
    c = c.replace(o, n)

io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d pairs applied' % len(pairs))
