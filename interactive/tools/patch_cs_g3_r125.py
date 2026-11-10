# -*- coding: utf-8 -*-
"""cs-g3 第125轮原子补丁（逐对唯一性校验，全过才写盘）
① 等效态 R_D（下挂件 rarr-rd）与 R_L 下移 27.5px：电阻体 y 317→344.5、中心 371
   与受控源菱形中心水平同轴；上下引线 344.5/397.5、标签基线 350→377.5
② i_d 箭头长度翻倍（37→74）：y 244.5—318.5，中心仍 281.5（与 g_m·v_gs 同轴）
"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

pairs = [
    # ---------- ② 箭头 2 倍长度 ----------
    ("""                <!-- i_d 方向箭头（第5问揭示：受控源电流自漏极流向源极，箭头朝下）。
                     第124轮：从菱形内移到受控源上端导线中段（216.25—346 的中间，y 263-300，中心≈281） -->
                <g id="fx-t-id" opacity="0">
                    <line x1="570" y1="263" x2="570" y2="285" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="570,300 561,285 579,285" fill="#ff5252" stroke="none"/>
                </g>""",
     """                <!-- i_d 方向箭头（第5问揭示：受控源电流自漏极流向源极，箭头朝下）。
                     第124轮：从菱形内移到受控源上端导线中段（216.25—346 的中间，中心≈281）；
                     第125轮：长度翻倍（箭杆 44 + 三角 30 = 74），两端距 D 极线 216.25 / 菱形上顶点 346 各 28 -->
                <g id="fx-t-id" opacity="0">
                    <line x1="570" y1="244.5" x2="570" y2="288.5" stroke="#ff5252" stroke-width="5"/>
                    <polygon points="570,318.5 561,288.5 579,288.5" fill="#ff5252" stroke="none"/>
                </g>"""),

    # ---------- ① 等效态 R_D / R_L 下移与受控源同轴 ----------
    ("""        // 第122轮：D 极水平导线等效态左端缩短 40px（530→570，红点随动）——受控源模型静态坐标已整体 +40；""",
     """        // —— 第125轮：R_D（整理后下挂件）与 R_L 下移 27.5px，电阻体中心 371 与受控源菱形中心水平同轴 ——
        //    体 317→344.5（下沿 397.5），上下引线各 128.25/127.5 均衡；标签基线 350→377.5（两者仍同轴）
        const rdraw = q('#rarr-rd');
        if (rdraw) {
            const rp = rdraw.querySelectorAll('path');
            if (rp[0]) rp[0].setAttribute('d', up ? 'M 690 216.25 V 344.5' : 'M 690 216.25 V 317');
            if (rp[1]) rp[1].setAttribute('d', up ? 'M 690 397.5 V 525' : 'M 690 370 V 525');
            const rrc = rdraw.querySelector('rect'); if (rrc) rrc.setAttribute('y', up ? '344.5' : '317');
            const rrt = rdraw.querySelector('text'); if (rrt) rrt.setAttribute('y', up ? '377.5' : '350');
        }
        const rlg = q('g[data-id="comp-rl"]');
        if (rlg) {
            const rrc = rlg.querySelector('rect'); if (rrc) rrc.setAttribute('y', up ? '344.5' : '317');
            const rrt = rlg.querySelector('text'); if (rrt) rrt.setAttribute('y', up ? '377.5' : '350');
        }
        //   R_L 上引线：等效态自输出线 216.25（整理态已下移）伸到 344.5；复位回默认态 161.5—317
        setD('g[data-id="wire-rl-top"] path', up ? 'M 850 216.25 V 344.5' : 'M 850 161.5 V 317');
        setD('g[data-id="wire-rl-bot"] path', up ? 'M 850 397.5 V 525' : 'M 850 370 V 525');
        // 第122轮：D 极水平导线等效态左端缩短 40px（530→570，红点随动）——受控源模型静态坐标已整体 +40；"""),
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
