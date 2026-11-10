# -*- coding: utf-8 -*-
"""cs-g3 第126轮原子补丁（逐对唯一性校验，全过才写盘）
点击场效应管等效后整图上移 30px：circuit-wrap translate y 260→230（setCircuitShift up 分支 220→230
并恢复 showEquiv 调用；此前 up 分支为死代码，第120轮曾取消等效态整图上移）
"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

pairs = [
    # ① setCircuitShift：up 分支 220→230
    ("""    // 整图位移基准（第115轮整体左移30：x=-12；第120轮起等效态不再整图上移，本函数仅复位用）
    function setCircuitShift(up) {
        const w = document.getElementById('circuit-wrap');
        if (w) w.setAttribute('transform', 'translate(-12, ' + (up ? 220 : 260) + ') scale(1)');
    }""",
     """    // 整图位移基准（第115轮整体左移30：x=-12；第126轮：等效态整图上移 30px——y 260→230，resetCircuit 复位 260）
    function setCircuitShift(up) {
        const w = document.getElementById('circuit-wrap');
        if (w) w.setAttribute('transform', 'translate(-12, ' + (up ? 230 : 260) + ') scale(1)');
    }"""),

    # ② showEquiv 恢复整图上移调用
    ("""    // 输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25），原 S 极到地端导线整体移除（受控源支路直落地线）；
    // R_G、分压电阻（经分压节点接线）、整理态下挂件（R_G1/R_D）保持原位，无需整图上移
    function showEquiv() {
        fadeGroup('comp-t', true);      // 场效应管本体移除
        showFx('fx-tmodel', true);      // 微变等效模型层点亮（父层 PE 暂 none，五连问完成后才可点击）
        applyEquivInput(true);          // 输入主线上移与 D 极对齐（V_i/C_1/短接桥/下引线/交叉点/G 端子与红点/极性柱随动）""",
     """    // 输入主线（G 极水平导线）上移与 D 极对齐（y 282→216.25），原 S 极到地端导线整体移除（受控源支路直落地线）；
    // R_G、分压电阻（经分压节点接线）、整理态下挂件（R_G1/R_D）保持原位；第126轮起整图上移 30px（顶轨 5→-25 视位）
    function showEquiv() {
        fadeGroup('comp-t', true);      // 场效应管本体移除
        showFx('fx-tmodel', true);      // 微变等效模型层点亮（父层 PE 暂 none，五连问完成后才可点击）
        setCircuitShift(true);          // 第126轮：等效态整图上移 30px（translate y 260→230），resetCircuit 归位
        applyEquivInput(true);          // 输入主线上移与 D 极对齐（V_i/C_1/短接桥/下引线/交叉点/G 端子与红点/极性柱随动）"""),
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
