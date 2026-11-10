# -*- coding: utf-8 -*-
"""cs-g3 第124轮原子补丁（逐对唯一性校验，全过才写盘）
① 等效态 S 红点回到与 G 红点垂直同轴（570 → 442）
② i_d 箭头上移到受控源上端导线中段（y 263-300，中心≈281），g_m·v_gs 标注与箭头水平同轴（Y 318→291）
③ 新增受控源右侧 g_m 标注 fx-gm-tag（菱形右顶点 602 + 15px = 617），第2关显示（render 按关卡切换）
"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

pairs = [
    # ---------- ② i_d 箭头移到受控源上端导线中段 ----------
    ("""                <!-- i_d 方向箭头（第3问揭示：受控源电流自漏极流向源极，箭头朝下） -->
                <g id="fx-t-id" opacity="0">
                    <line x1="570" y1="352" x2="570" y2="374" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="570,389 561,374 579,374" fill="#ff5252" stroke="none"/>
                </g>""",
     """                <!-- i_d 方向箭头（第5问揭示：受控源电流自漏极流向源极，箭头朝下）。
                     第124轮：从菱形内移到受控源上端导线中段（216.25—346 的中间，y 263-300，中心≈281） -->
                <g id="fx-t-id" opacity="0">
                    <line x1="570" y1="263" x2="570" y2="285" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="570,300 561,285 579,285" fill="#ff5252" stroke="none"/>
                </g>"""),

    # ---------- ②③ g_m·v_gs 标注与箭头同轴 + 新增受控源右侧 g_m 标注 ----------
    ("""                <!-- 受控源电流数值标注 g_m·v_gs：第5问作答后与箭头同现（第122轮移菱形右下 590,318——
                     原右侧位随模型 +40 后右缘 712 会压 R_D 下挂线 x=690；第2/3关填空点它作答） -->
                <g id="fx-t-idlabel" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）" opacity="0">
                    <rect class="hot" x="584" y="290" width="82" height="44" fill="none" stroke="none"/>
                    <text class="hot-label" x="590" y="318" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>""",
     """                <!-- 受控源电流数值标注 g_m·v_gs：第5问作答后与箭头同现（第124轮上移到箭头右侧、与箭头水平同轴：
                     基线 291（视觉中线≈281 = 箭头中心），起点 x=590（距箭头 x=570 净 20）；
                     右缘约 666 距 R_D 下挂线 690 净 24；第2/3关填空点它作答） -->
                <g id="fx-t-idlabel" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）" opacity="0">
                    <rect class="hot" x="584" y="257" width="82" height="48" fill="none" stroke="none"/>
                    <text class="hot-label" x="590" y="291" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>

                <!-- 受控源跨导标注 g_m（第124轮）：第2关（Av 表达式要填 g_m）单独显示在受控源右侧，
                     文字左缘 617 = 菱形右顶点 602 + 15px，与菱形水平同轴（基线 381）；
                     与 fx-t-idlabel 同为 q-gm 作答区（点它可直接作答），第1/3关隐藏——由 render() 按关卡切换 -->
                <g id="fx-gm-tag" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）" opacity="0">
                    <rect class="hot" x="611" y="349" width="62" height="44" fill="none" stroke="none"/>
                    <text class="hot-label" x="617" y="381" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan></text>
                </g>"""),

    # ---------- ① S 红点回到与 G 红点同轴 ----------
    ("""        // S 红点：默认沟道 s 段中点 (530,274) → 等效态落到公共地线 (570,525)，与 D 极导线端点红点垂直同轴
        //   （第123轮：原 (462,525) 与 G 红点同轴，改为与受控源落地点/D 红点同轴，正对受控源支路）
        const sd = q('#fx-dot-s circle');
        if (sd) { sd.setAttribute('cx', up ? '570' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }""",
     """        // S 红点：默认沟道 s 段中点 (530,274) → 等效态落到公共地线 (442,525)，与 G 红点 (442,216.25) 垂直同轴
        //   （第124轮按用户裁决回到 G 极同轴：第123轮曾移到 570 与 D 红点同轴，导致 G—S 两点错位）
        const sd = q('#fx-dot-s circle');
        if (sd) { sd.setAttribute('cx', up ? '442' : '530'); sd.setAttribute('cy', up ? '525' : '274'); }"""),

    # ---------- ③ resetCircuit 隐藏清单补 fx-gm-tag ----------
    ("""         'fx-t-src', 'fx-t-id', 'fx-t-vgs', 'fx-t-idlabel', 'fx-dot-g', 'fx-dot-d', 'fx-dot-s',
         'fx-gnd-node'].forEach(id => {""",
     """         'fx-t-src', 'fx-t-id', 'fx-t-vgs', 'fx-t-idlabel', 'fx-gm-tag', 'fx-dot-g', 'fx-dot-d', 'fx-dot-s',
         'fx-gnd-node'].forEach(id => {"""),

    # ---------- ③ render() 按关卡切换 g_m 标注（仅第2关显示） ----------
    ("""    function render() {
        clearUI();
        updateQlabels();""",
     """    function render() {
        clearUI();
        updateQlabels();
        // 第124轮：受控源右侧 g_m 标注只在本案例第 2 关（Av 表达式填 g_m）显示，第1/3关隐藏
        showFx('fx-gm-tag', S.level === 2 && !S.finished);"""),

    # ---------- fx-tmodel 头注释同步 ----------
    ("""                 v_gs 极性柱（G 端子正下方，＋256 / v_gs 367 / －505 贴近地线）第2问揭示；
                 受控源支路第4问揭示；i_d 箭头与 g_m·v_gs 标注（菱形右上，填空关点它作答）第5问同现 -->""",
     """                 v_gs 极性柱（G 端子正下方，＋256 / v_gs 367 / －505 贴近地线）第2问揭示；
                 受控源支路第4问揭示；i_d 箭头（第124轮移到上端导线中段 263-300）与 g_m·v_gs 标注
                 （箭头右侧同轴 590,291）第5问同现；受控源右侧 g_m 标注（617,381，距菱形 15px）仅第2关显示 -->"""),
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
