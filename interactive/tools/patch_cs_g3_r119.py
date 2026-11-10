# -*- coding: utf-8 -*-
# 第119轮（cs-g3）：
# ① rs-remove 连带收起 C_S 旁路支路：绿短接桥 fx-cs、支路接线 wire-cs-top/bot（含分支节点圆）
# ② 场效应管等效五问改为与 cs-g1 同口径：G-S开路 → v_gs极性(上＋下－,揭示极性柱) → G-D开路
#    → D-S受控源(揭示菱形) → ↓i_d(揭示箭头+同现 g_m·v_gs 标注 fx-t-idlabel)
#    fx-tmodel 新增 fx-t-vgs 极性柱（G端子正下方 502,322/400/478）；g_m·v_gs 从 fx-t-src 常显移至
#    fx-t-idlabel（data-id 仍为 q-gm，供第2/3关填空作答）
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

PAIRS = []

# P1 rs-remove 连带收 C_S 支路
PAIRS.append((
"""            case 'rs-remove':   // R_S 移除：原位换成短接导线（源极经它接地——C_S 旁路已将 R_S 短接）
                fadeGroup('comp-rs', true); showFx('fx-rs', true);
                break;""",
"""            case 'rs-remove':   // R_S 移除：原位换成短接导线（源极经它接地）；C_S 旁路支路随之失去意义——
                                // 绿短接桥、支路接线与分支节点一并收起（与 cs-g2 同口径：源极只余 fx-rs 一条入地）
                fadeGroup('comp-rs', true); showFx('fx-rs', true);
                fadeGroup('wire-cs-top', true); fadeGroup('wire-cs-bot', true); showFx('fx-cs', false);
                break;"""))

# P2a fx-tmodel 头注释末行
PAIRS.append((
"                 跨导标注 g_m·v_gs 在菱形右侧（填空关点它作答），i_d 箭头在菱形内部（第3问揭示） -->",
"                 v_gs 极性柱（G 端子正下方）第2问揭示；受控源支路第4问揭示；i_d 箭头与 g_m·v_gs\n                 标注（菱形右侧，填空关点它作答）第5问同现 -->"))

# P2b 插入 fx-t-vgs + 更新 fx-t-src 注释
PAIRS.append((
"""                <!-- D-S 受控电流源支路（第2问揭示）：漏极节点直下源极节点，菱形符号居中 -->
                <g id="fx-t-src" opacity="0">""",
"""                <!-- v_gs 控制量极性柱（G—S 之间，第2问作答后显示；与 cs-g1 同口径：
                     ＋随 G 端子、－落源极地电位——R_S 移除后源极直接接地） -->
                <g id="fx-t-vgs" opacity="0">
                    <text x="502" y="322" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text x="502" y="400" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">v<tspan class="sub">gs</tspan></text>
                    <text x="502" y="478" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>
                <!-- D-S 受控电流源支路（第4问揭示）：漏极节点直下源极节点，菱形符号居中（不含 g_m·v_gs 标注） -->
                <g id="fx-t-src" opacity="0">"""))

# P2c fx-t-src 内删常显 g_m·v_gs（fx-t-gm）
PAIRS.append((
"""                    <path class="hot keepw" d="M 554 270 V 274 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 跨导标注 g_m·v_gs（随受控源一同揭示；填空关点它作答） -->
                    <g id="fx-t-gm" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）">
                        <rect class="hot" x="586" y="224" width="82" height="44" fill="none" stroke="none"/>
                        <text class="hot-label" x="590" y="256" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                    </g>
                </g>""",
"""                    <path class="hot keepw" d="M 554 270 V 274 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                </g>"""))

# P2d fx-t-id 后追加 fx-t-idlabel（g_m·v_gs，data-id 仍 q-gm）
PAIRS.append((
"""                    <polygon points="554,263 545,248 563,248" fill="#ff5252" stroke="none"/>
                </g>""",
"""                    <polygon points="554,263 545,248 563,248" fill="#ff5252" stroke="none"/>
                </g>
                <!-- 受控源电流数值标注 g_m·v_gs：第5问作答后与箭头同现（菱形右侧；第2/3关填空点它作答） -->
                <g id="fx-t-idlabel" class="interactive" data-id="q-gm" data-name="跨导 g_m（微变等效模型参数）">
                    <rect class="hot" x="586" y="224" width="82" height="44" fill="none" stroke="none"/>
                    <text class="hot-label" x="590" y="256" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>"""))

# P3 TQUIZ 注释 + 数组（与 cs-g1 五问同口径）
PAIRS.append((
"""    /* ★换案例：TQUIZ 等效问答——⚠️ 改 opts/ok 必须同步回归测试脚本答案表（DOM 文本无下划线 '↓id'） */
    // ---- 场效应管等效五连问（第1关第3步）：
    //      ①G–S 之间→开路（i_G=0）②D–S 之间→受控源（揭示菱形符号与跨导标注 g_m·v_gs）
    //      ③i_d 方向→↓（自漏极流向源极，揭示箭头）④受控源类型→电压控制电流源 ⑤控制电压→栅源电压
    //      答错从本项 2 分池扣 1，无论对错都推进下一问（答错时同样画出正确结果） ----
    // 本案例 G/D/S 三端点位置固定（红点不动态移位），setEPos 保留为空操作
    const EDOT_X0 = (function () { const c = document.querySelector('#fx-dot-e circle'); return c ? c.getAttribute('cx') : '420'; })();
    function setEPos(x) {
        const c = document.querySelector('#fx-dot-e circle');
        if (c) c.setAttribute('cx', x ? String(x) : EDOT_X0);
    }
    const TQUIZ = [
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['开路', '受控源', '电导'], ok: '开路',
          q: 'G、S 之间相当于什么？' },
        { dots: ['fx-dot-d', 'fx-dot-s'], opts: ['开路', '受控源', '电导'], ok: '受控源',
          q: 'D、S 之间相当于什么？', reveal: 'fx-t-src' },
        { dots: ['fx-dot-d'], opts: ['↑i_d', '↓i_d'], ok: '↓i_d',
          q: '受控源电流 i_d 的方向是？', reveal: 'fx-t-id' },
        { dots: ['fx-dot-d'], opts: ['电压控制电流源', '电流控制电流源', '电压控制电压源'], ok: '电压控制电流源',
          q: '该受控源的类型是？' },
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['栅源电压', '漏源电压', '栅漏电压'], ok: '栅源电压',
          q: '受控源电流大小与哪个电压成正比？' }
    ];
    // 电流方向问的选项渲染：↑/↓ + 带下标的符号（如 ↓i_b → ↓i 加下标 b）；其余选项返回 null 走纯文本
    const TQ_SUBB = '<span style="font-size:0.72em;vertical-align:-0.16em">d</span>';
    function tquizOptHtml(op) {
        const c = op.charAt(0);
        if (c !== '↑' && c !== '↓') return null;
        return c + 'i' + TQ_SUBB;   // 本案例仅 i_d 方向问（↑i_d / ↓i_d）
    }""",
"""    /* ★换案例：TQUIZ 等效问答（与 cs-g1 同口径五问）——⚠️ 改 opts/ok 必须同步回归测试脚本答案表 */
    // ---- 场效应管等效五连问（第1关第3步）：
    //      ①G–S 之间→开路（i_G=0）②v_gs 极性→上＋下－（揭示极性柱 fx-t-vgs）③G–D 之间→开路
    //      ④D–S 之间→受控源（揭示菱形 fx-t-src）⑤箭头方向→↓i_d（揭示 fx-t-id 并同现 fx-t-idlabel）
    //      答错从本项池扣 1，无论对错都推进下一问（答错时同样画出正确结果） ----
    // 本案例 G/D/S 三端点位置固定（红点不动态移位），setEPos 保留为空操作
    const EDOT_X0 = (function () { const c = document.querySelector('#fx-dot-e circle'); return c ? c.getAttribute('cx') : '420'; })();
    function setEPos(x) {
        const c = document.querySelector('#fx-dot-e circle');
        if (c) c.setAttribute('cx', x ? String(x) : EDOT_X0);
    }
    const TQUIZ = [
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['短路', '开路', '受控源'], ok: '开路',
          q: 'G、S 之间相当于什么？' },
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['上＋下－', '上－下＋'], ok: '上＋下－',
          q: 'v_gs 的标注极性应怎样表示？', reveal: 'fx-t-vgs' },
        { dots: ['fx-dot-g', 'fx-dot-d'], opts: ['短路', '开路', '受控源'], ok: '开路',
          q: 'G、D 之间相当于什么？' },
        { dots: ['fx-dot-d', 'fx-dot-s'], opts: ['短路', '开路', '受控源'], ok: '受控源',
          q: 'D、S 之间相当于什么？', reveal: 'fx-t-src' },
        { dots: ['fx-dot-d'], opts: ['↑i_d', '↓i_d'], ok: '↓i_d', idlabel: 'fx-t-idlabel',
          q: '受控源支路电流为 g_m·v_gs，箭头方向是？', reveal: 'fx-t-id' }
    ];
    // 选项渲染：↑/↓ → 箭头+g_m·v_gs（下标用小号行内 span）；上＋下－/上－下＋ → 竖排极性柱（与图上标注形态一致）；
    // 其余选项返回 null 走纯文本
    const TQ_SUBM = '<span style="font-size:0.72em;vertical-align:-0.16em">m</span>';
    const TQ_SUBGS = '<span style="font-size:0.72em;vertical-align:-0.16em">gs</span>';
    function tquizOptHtml(op) {
        const c = op.charAt(0);
        if (c === '↑' || c === '↓') return c + 'g' + TQ_SUBM + '·v' + TQ_SUBGS;
        if (op === '上＋下－' || op === '上－下＋') {
            return '<span style="display:inline-flex;flex-direction:column;align-items:center;line-height:1.15;padding:3px 0;width:44px">'
                 + '<span style="font-size:17px;width:100%;text-align:center">' + op.charAt(1) + '</span>'
                 + '<span style="font-style:italic;font-size:15px;line-height:1.2;width:100%;text-align:center;position:relative;top:-2px">v' + TQ_SUBGS + '</span>'
                 + '<span style="font-size:17px;width:100%;text-align:center">' + op.charAt(3) + '</span></span>';
        }
        return null;
    }"""))

# P5 answerTQuiz 同现 idlabel
PAIRS.append((
"""        if (q.reveal) showFx(q.reveal, true);
        d.tquiz.step++;""",
"""        if (q.reveal) showFx(q.reveal, true);
        if (q.idlabel) showFx(q.idlabel, true);   // g_m·v_gs 数值标注：第5问作答后与箭头同现
        d.tquiz.step++;"""))

# P6 resetCircuit 隐清单
PAIRS.append((
"""         'fx-t-src', 'fx-t-id', 'fx-t-gm', 'fx-dot-g', 'fx-dot-d', 'fx-dot-s'].forEach(id => {""",
"""         'fx-t-src', 'fx-t-id', 'fx-t-vgs', 'fx-t-idlabel', 'fx-dot-g', 'fx-dot-d', 'fx-dot-s'].forEach(id => {"""))

# P7 ?ts 钩子同现 idlabel
PAIRS.append((
"""                TQUIZ.slice(0, done ? last : tv - 1).forEach(q => { if (q.reveal) showFx(q.reveal, true); });""",
"""                TQUIZ.slice(0, done ? last : tv - 1).forEach(q => { if (q.reveal) showFx(q.reveal, true); if (q.idlabel) showFx(q.idlabel, true); });"""))

for i, (o, n) in enumerate(PAIRS):
    k = c.count(o)
    if k != 1:
        print('FAIL pair %d count=%d :: %s' % (i, k, o.strip().splitlines()[0][:60]))
        sys.exit(1)
for o, n in PAIRS:
    c = c.replace(o, n)
io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d pairs applied' % len(PAIRS))
