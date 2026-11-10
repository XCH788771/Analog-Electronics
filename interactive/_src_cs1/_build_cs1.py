#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cs-g1.html 构建脚本（共源放大 · 分压式偏置案例1 闯关页）

以 _game-template.html（v2 引擎）为基底：
  ① 替换区 A（标题/案例行）② 已知行 ③ 替换区 B（电路 SVG）④ 替换区 C（GAME_CONFIG）
  ⑤ 替换区 D（STAGE_UNITS）⑥ ANNOS 注解表 ⑦ 引擎适配补丁（nStatic/阶段名/CAP_FX/resetCircuit/
  setCircuitShift/nextHint/execAct 新动作/showEquiv/TQUIZ/tquizOptHtml/startTQuiz 池/
  选项条位置/调试钩子/结算评语）
所有替换均带唯一性校验，失配即 exit 1 不写盘。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
TPL = os.path.join(ROOT, '_game-template.html')
OUT = os.path.join(ROOT, 'cs-g1.html')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wt(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def frag(name):
    return rd(os.path.join(HERE, name))


def replace_between(text, start_anchor, end_anchor, new_content, name):
    """把 [start_anchor, end_anchor] 整段（含两个锚）替换为 new_content；锚必须唯一"""
    i = text.find(start_anchor)
    if i < 0:
        sys.exit('构建失败：找不到起始锚 [%s]' % name)
    if text.find(start_anchor, i + 1) >= 0:
        sys.exit('构建失败：起始锚不唯一 [%s]' % name)
    j = text.find(end_anchor, i + len(start_anchor))
    if j < 0:
        sys.exit('构建失败：找不到结束锚 [%s]' % name)
    if text.find(end_anchor, j + 1) >= 0:
        sys.exit('构建失败：结束锚不唯一 [%s]' % name)
    return text[:i] + new_content + text[j + len(end_anchor):]


def rep(text, old, new, name):
    n = text.count(old)
    if n != 1:
        sys.exit('构建失败：补丁 [%s] 匹配 %d 次（要求 1 次）' % (name, n))
    return text.replace(old, new, 1)


def main():
    t = rd(TPL)

    # ① 替换区 A：标题 + 案例行
    t = replace_between(t,
        '        <!-- ▼▼▼ 替换区 A：左上角大标题 + 案例行（换成自己的案例名与题面） ▼▼▼ -->',
        '        <!-- ▲▲▲ 替换区 A 结束 ▲▲▲ -->',
        frag('_cs1_A.txt'), 'zoneA')

    # ② 已知行（区 A 之外，单独替换）
    t = rep(t,
        '        <text x="70" y="210" fill="rgba(255,255,255,0.6)" font-size="26">已知：V<tspan class="sub">CC</tspan>、R<tspan class="sub">B1</tspan>、R<tspan class="sub">B2</tspan>、R<tspan class="sub">C</tspan>、R<tspan class="sub">E</tspan>、R<tspan class="sub">S</tspan>、R<tspan class="sub">L</tspan>、β，V<tspan class="sub">BE</tspan>=0.7V</text>\n',
        frag('_cs1_known.txt'), 'known-line')

    # ③ 替换区 B：整块电路 SVG（circuit-wrap + fx-layer）
    t = replace_between(t,
        '        <!-- ▼▼▼ 替换区 B：本案例电路 SVG（<g id="circuit-wrap"> 整块；含 fx-layer 特效/电量标注/整理/等效层；',
        '        <!-- ▲▲▲ 替换区 B 结束 ▲▲▲ -->',
        frag('_cs1_B.txt'), 'zoneB')

    # ④ 替换区 C：GAME_CONFIG
    t = replace_between(t,
        '    /* ▼▼▼ 替换区 C：本案例关卡配置 GAME_CONFIG（两阶段五关，换新案例整块替换）▼▼▼',
        '    /* ▲▲▲ 替换区 C 结束 ▲▲▲ */',
        frag('_cs1_C.txt'), 'zoneC')

    # ⑤ 替换区 D：STAGE_UNITS
    t = replace_between(t,
        '    /* ▼▼▼ 替换区 D：电路分级 STAGE_UNITS（每组=某关对应电路单元 data-id 列表，与区 B 一一对应）▼▼▼ */',
        '    /* ▲▲▲ 替换区 D 结束 ▲▲▲ */',
        frag('_cs1_D.txt'), 'zoneD')

    # ⑥ ANNOS 注解表（TODO ③ 注释 → comp-vo 条目收尾的 `    };`）
    t = replace_between(t,
        '    // ===== TODO ③：注解与语音内容 =====',
        "                          parts: [{ text: '这是输出电压。它取自负载电阻两端，相位与输入相反，这就是共射放大电路的反向放大特性。' }] },\n    };",
        frag('_cs1_ANNOS.txt'), 'ANNOS')

    # ⑦ 引擎适配补丁
    t = rep(t,
        "        const nStatic = 3;   // 静态 3 关（绘制直流通路 / Q点步骤 / Q点框架+表达式）",
        "        const nStatic = 1;   // 本案例：电路等效阶段仅 1 关（绘制交流小信号等效电路）",
        'nStatic')

    # 文档标题：模板沿用共射案例名，须改为共源（浏览器标签/分享标题口径）
    t = rep(t,
        '<title>分压式偏置共射放大 · 闯关挑战（案例1）- 游戏交互</title>',
        '<title>分压式偏置共源放大 · 闯关挑战（案例1）- 游戏交互</title>',
        'doc-title')

    # showMenu 重新展示时取消挂起的 240ms 自动隐藏：
    # 等效问答点选项 → hideMenu 置 menuLock=false → 鼠标原位触发 mouseleave 排下 hideMenu；
    # 若下一问渲染快于 240ms（定时器加速的回归环境 40ms<240ms），陈旧定时器会误杀新菜单
    t = rep(t,
        "    function showMenu(anchorEl, items, lock, pos) {\n"
        "        if (!ctxmenu) return;\n"
        "        menuLock = !!lock;",
        "    function showMenu(anchorEl, items, lock, pos) {\n"
        "        if (!ctxmenu) return;\n"
        "        clearTimeout(menuTimer);   // 重新展示即取消挂起的自动隐藏（等效问答换问竞态修复）\n"
        "        menuLock = !!lock;",
        'showMenu-cancel-hide')

    t = rep(t,
        "        gameUI.appendChild(mkText(phIdx(0), 290, 19, '静态分析', { anchor: 'middle', fill: 'rgba(255,255,255,0.5)', bold: false }));\n"
        "        gameUI.appendChild(mkText(phIdx(1), 290, 19, '动态分析', { anchor: 'middle', fill: 'rgba(255,255,255,0.5)', bold: false }));",
        "        gameUI.appendChild(mkText(phIdx(0), 290, 19, '电路等效', { anchor: 'middle', fill: 'rgba(255,255,255,0.5)', bold: false }));\n"
        "        gameUI.appendChild(mkText(phIdx(1), 290, 19, '动态指标', { anchor: 'middle', fill: 'rgba(255,255,255,0.5)', bold: false }));",
        'phase-labels')

    t = rep(t,
        "    const CAP_FX = { 'comp-c1': 'fx-c1', 'comp-c2': 'fx-c2', 'comp-ce': 'fx-ce' };",
        "    const CAP_FX = { 'comp-cb1': 'fx-cb1' };",
        'CAP_FX')

    t = rep(t,
        "        ['fx-c1', 'fx-c2', 'fx-ce', 'fx-vi', 'fx-vcc', 'fx-vs', 'fx-re', 'fx-tmodel', 'rarr-rb1', 'rarr-rc',\n"
        "         'fx-t-rbe', 'fx-t-src', 'fx-t-ib', 'fx-t-ic', 'fx-dot-b', 'fx-dot-c', 'fx-dot-e',\n"
        "         'eq-layer', 'eq-rb1', 'eq-rb2'].forEach(id => {",
        "        ['fx-cb1', 'fx-vdd', 'fx-tmodel', 'fx-t-src', 'fx-t-id',\n"
        "         'fx-dot-g', 'fx-dot-d', 'fx-dot-s'].forEach(id => {",
        'resetCircuit-ids')

    t = rep(t,
        "    // 交流等效态整图上移 40px（基极线、模型与地线一并上移，给下半部留出空间）\n"
        "    function setCircuitShift(up) {\n"
        "        const w = document.getElementById('circuit-wrap');\n"
        "        if (w) w.setAttribute('transform', 'translate(18, ' + (up ? 220 : 260) + ') scale(1)');\n"
        "    }",
        "    // 共源案例：等效态不整体上移（无整理层，Rg1/Rg2/Rd 原位不动）——固定 272，\n"
        "    // 给等效问答选项条留出上方空白带（已知行 y=210 与顶轨 y=277 之间）\n"
        "    function setCircuitShift(up) {\n"
        "        const w = document.getElementById('circuit-wrap');\n"
        "        if (w) w.setAttribute('transform', 'translate(18, 272) scale(1)');\n"
        "    }",
        'setCircuitShift')

    t = rep(t,
        "    function nextHint(c, d, id) {\n"
        "        if (c.gate && c.gate.indexOf(id) >= 0 && c.gate.every(g => d.found[g])) {\n"
        "            return (c.targets || []).some(t => !d.found[t.id]) ? '请选择电容处理方式。' : '';\n"
        "        }\n"
        "        if (!c.subSteps) return '';\n"
        "        // ★换案例：第4关电容/电阻清单与语音引导链文案（nextHint）\n"
        "        const CAPS = ['comp-c1', 'comp-c2', 'comp-ce'];\n"
        "        const RES = ['comp-re', 'comp-rb1', 'comp-rc'];\n"
        "        if (RES.indexOf(id) < 0 && CAPS.indexOf(id) < 0) return '';\n"
        "        const resDone = !!(d.found['comp-re'] && d.moved && d.moved['comp-rb1'] && d.moved['comp-rc']);\n"
        "        if (CAPS.indexOf(id) >= 0 && CAPS.every(x => d.found[x]) && !resDone) return '请选择阿尔义、阿尔B1和阿尔C的整理方式。';\n"
        "        if (RES.indexOf(id) >= 0 && resDone) return '请等效BJT。';\n"
        "        return '';\n"
        "    }",
        "    function nextHint(c, d, id) {\n"
        "        if (c.gate && c.gate.indexOf(id) >= 0 && c.gate.every(g => d.found[g])) {\n"
        "            return (c.targets || []).some(t => !d.found[t.id]) ? '请将耦合电容短路。' : '';\n"
        "        }\n"
        "        if (!c.subSteps) return '';\n"
        "        // ★换案例：共源案例引导链——电容短路完成 → 请等效场效应管\n"
        "        if (id === 'comp-cb1' && d.found['comp-cb1'] && !d.found['comp-t']) return '请等效场效应管。';\n"
        "        return '';\n"
        "    }",
        'nextHint')

    t = rep(t,
        "            case 'vs-short': fadeGroup('comp-src', true); showFx('fx-vs', true); break;",
        "            case 'vi-keep':  break;   // 输入信号源保留（正是被放大的对象，不做任何变换）\n"
        "            case 'vi-open':  break;   // 干扰项（选错不执行动作，仅扣分）\n"
        "            case 'vdd-gnd':  showFx('fx-vdd', true); hideVccLabel(); break;   // 直流电源置零→接地\n"
        "            case 'vdd-open': hideVccLabel(); break;\n"
        "            case 'vdd-keep': break;\n"
        "            case 'vs-short': fadeGroup('comp-src', true); showFx('fx-vs', true); break;",
        'execAct-acts')

    t = rep(t,
        "    // 交流等效最终布局（第4关第3步选「等效」时启用）：\n"
        "    // 移除晶体管本体后，基极输入线上升到 y=178 与集电极导线对齐，Vs/Rs/RB1/RB2 上移；\n"
        "    // 旧 y=265 输入线、旧 Vs/Rs 列、整理态 R_B1/R_B2、发射极支路（r_be/受控源已直挂地线）全部收起\n"
        "    // ★换案例：等效态切换（纯共射结构可直接沿用；新增状态层须在此同亮）\n"
        "    function showEquiv() {\n"
        "        ['wire-vi-top', 'wire-base-in', 'wire-base', 'comp-vi', 'wire-rs-top', 'comp-rs', 'wire-rs-bot', 'comp-src', 'wire-vi-gnd',\n"
        "         'wire-rb2a', 'comp-rb2', 'wire-rb2b',\n"
        "         'wire-emitter', 'wire-re-a', 'wire-re-b'].forEach(x => fadeGroup(x, true));\n"
        "        // 受控源上方的集电极节点（此时只剩 2 条导线成直角，已非节点）一并移除\n"
        "        fadeGroup('node-collector', true);\n"
        "        // 集电极横导线缩短：左端由晶体管 C 端（486）收到交流等效的 C 节点（580，受控源支路挂点）——\n"
        "        // 原整段导线（wire-collector 485→670）收起，改由 eq-layer 内的 560→670 段承担（见 eq-layer）\n"
        "        fadeGroup('wire-collector', true);\n"
        "        fadeGroup('wire-c-stub', true);   // 晶体管已移除，T 集电极—集电极导线之间的短接线一并收起（等效态导线由 eq-layer 承担）\n"
        "        // rarr-rb1 / rarr-rb2lab 只有 id 没有 data-id，用 getElementById 收起\n"
        "        showFx('rarr-rb1', false);\n"
        "        showFx('rarr-rb2lab', false);\n"
        "        // R_C 保持在整理态下挂位（x=640，与 R_L 并联）：等效后位置不变，学生视觉上不会跳变\n"
        "        showFx('rarr-rc', true);\n"
        "        const rcKeep = document.getElementById('rarr-rc');\n"
        "        if (rcKeep) rcKeep.style.pointerEvents = 'all';\n"
        "        showFx('fx-c1', false);\n"
        "        showFx('fx-re', false);\n"
        "        // eq-layer 与其中可作答的 eq-rb1 / eq-rb2 一起点亮（resetCircuit 会把它们 opacity 清零）\n"
        "        ['eq-layer', 'eq-rb1', 'eq-rb2'].forEach(id => showFx(id, true));\n"
        "        setCircuitShift(true);   // 整个电路图上移 40px，等效模型区域更宽松\n"
        "        ['eq-rb1', 'eq-rb2'].forEach(id => { const el = document.getElementById(id); if (el) el.style.pointerEvents = 'all'; });\n"
        "    }",
        "    // 交流等效态切换（第1关第2步选「等效」时启用）：\n"
        "    // 共源案例无需整理/上移——VDD 置零后顶部导轨即交流地，Rg1/Rg2/Rd 原位不动；\n"
        "    // 场效应管本体已在 execAct('t-equiv') 中移除，此处只点亮等效模型层（startTQuiz 亦会点亮）\n"
        "    // ★换案例：等效态切换（纯共源结构可直接沿用；新增状态层须在此同亮）\n"
        "    function showEquiv() {\n"
        "        showFx('fx-tmodel', true);   // 栅极板（G 端子）+ D–S 压控电流源支路容器\n"
        "    }",
        'showEquiv')

    t = rep(t,
        "    /* ★换案例：TQUIZ 等效问答——⚠️ 改 opts/ok 必须同步回归测试脚本答案表（DOM 文本无下划线 '↓ib'） */\n"
        "    // ---- 晶体管等效五连问（第4关第3步）：\n"
        "    //      ①B–E 之间→r_be ②B–C 之间→开路 ③C–E 之间→受控源（三选一，选项随机顺序）\n"
        "    //      ④给 B 端支路加 i_b 与箭头（选项：↑i_b / ↓i_b）⑤给集电极支路加 βi_b 与箭头（选项：↑βi_b / ↓βi_b）\n"
        "    //      答错从本项 2 分池扣 1，无论对错都推进下一问（答错时同样画出正确结果） ----\n"
        "    // 等效问3（C+E）时 E 红点动态移到受控源支路正下方，与 C 红点同竖直线（问1 保持 r_be 下端原位）\n"
        "    const EDOT_X0 = (function () { const c = document.querySelector('#fx-dot-e circle'); return c ? c.getAttribute('cx') : '420'; })();\n"
        "    function setEPos(x) {\n"
        "        const c = document.querySelector('#fx-dot-e circle');\n"
        "        if (c) c.setAttribute('cx', x ? String(x) : EDOT_X0);\n"
        "    }\n"
        "    const TQUIZ = [\n"
        "        { dots: ['fx-dot-b', 'fx-dot-e'], opts: ['rbe', '开路', '受控源'], ok: 'rbe',\n"
        "          q: 'B、E 之间相当于什么？', reveal: 'fx-t-rbe' },\n"
        "        { dots: ['fx-dot-b', 'fx-dot-c'], opts: ['rbe', '开路', '受控源'], ok: '开路',\n"
        "          q: 'B、C 之间相当于什么？' },\n"
        "        { dots: ['fx-dot-c', 'fx-dot-e'], opts: ['rbe', '开路', '受控源'], ok: '受控源', epos: [530],\n"
        "          q: 'C、E 之间相当于什么？', reveal: 'fx-t-src' },\n"
        "        { dots: ['fx-dot-b'], opts: ['↑i_b', '↓i_b'], ok: '↓i_b',\n"
        "          q: '在 B 端支路（r_be 所在支路）添加电流 i_b 与箭头，箭头方向是？', reveal: 'fx-t-ib' },\n"
        "        { dots: ['fx-dot-c'], opts: ['↑βi_b', '↓βi_b'], ok: '↓βi_b',\n"
        "          q: '在集电极支路（受控源所在支路）添加电流 βi_b 与箭头，箭头方向是？', reveal: 'fx-t-ic' }\n"
        "    ];",
        "    /* ★换案例：TQUIZ 等效问答——⚠️ 改 opts/ok 必须同步回归测试脚本答案表（DOM 文本无下划线 '↓id'） */\n"
        "    // ---- 场效应管等效四连问（第1关第2步）：\n"
        "    //      ①G–S 之间→开路 ②D–S 之间→受控源（三选一，选项随机顺序）\n"
        "    //      ③给漏极支路加 i_d 与箭头（选项：↑i_d / ↓i_d）④受控源类型→压控电流源\n"
        "    //      答错从本项分值池扣 1，无论对错都推进下一问（答错时同样画出正确结果） ----\n"
        "    // 共源案例红点固定在 G/D/S 三个端子，无需动态移位（setEPos 对不存在的 #fx-dot-e 自动空转）\n"
        "    const EDOT_X0 = (function () { const c = document.querySelector('#fx-dot-e circle'); return c ? c.getAttribute('cx') : '420'; })();\n"
        "    function setEPos(x) {\n"
        "        const c = document.querySelector('#fx-dot-e circle');\n"
        "        if (c) c.setAttribute('cx', x ? String(x) : EDOT_X0);\n"
        "    }\n"
        "    const TQUIZ = [\n"
        "        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['开路', '短路', '受控源'], ok: '开路',\n"
        "          q: 'G、S 之间相当于什么？' },\n"
        "        { dots: ['fx-dot-d', 'fx-dot-s'], opts: ['开路', '受控源', '电阻'], ok: '受控源',\n"
        "          q: 'D、S 之间相当于什么？', reveal: 'fx-t-src' },\n"
        "        { dots: ['fx-dot-d'], opts: ['↑i_d', '↓i_d'], ok: '↓i_d',\n"
        "          q: '在漏极支路（受控源所在支路）添加电流 i_d 与箭头，箭头方向是？', reveal: 'fx-t-id' },\n"
        "        { dots: [], opts: ['压控电流源', '流控电流源', '压控电压源'], ok: '压控电流源',\n"
        "          q: '这个受控源是什么类型的受控源？' }\n"
        "    ];",
        'TQUIZ')

    t = rep(t,
        "    function tquizOptHtml(op) {\n"
        "        const c = op.charAt(0);\n"
        "        if (c !== '↑' && c !== '↓') return null;\n"
        "        return c + (op.slice(1) === 'i_b' ? 'i' : 'βi') + TQ_SUBB;\n"
        "    }",
        "    function tquizOptHtml(op) {\n"
        "        const c = op.charAt(0);\n"
        "        if (c !== '↑' && c !== '↓') return null;\n"
        "        const m = op.slice(1).match(/^(β?i)_(.+)$/);   // 'i_d' / 'βi_b' → 符号 + 下标\n"
        "        return c + (m ? m[1] : op.slice(1)) + '<span style=\"font-size:0.72em;vertical-align:-0.16em\">' + (m ? m[2] : '') + '</span>';\n"
        "    }",
        'tquizOptHtml')

    t = rep(t,
        "    function startTQuiz() {\n"
        "        const d = S.draw[S.level - 1];\n"
        "        d.tquiz = { step: 0, pool: 2 };",
        "    function startTQuiz() {\n"
        "        const d = S.draw[S.level - 1], c = cur().cfg;\n"
        "        // 本案例计分口径：comp-t「等效」本身不计分，分值全部由等效问答池结算\n"
        "        //   → 池 = 本关总分 − 其余目标（各 round(pts/targets.length) 分）\n"
        "        const per = Math.round(c.pts / c.targets.length);\n"
        "        d.tquiz = { step: 0, pool: Math.max(1, c.pts - (c.targets.length - 1) * per) };",
        'startTQuiz-pool')

    t = rep(t,
        "        // 水平选项条固定在电路图上方空白带（等效态电路线 y=415 之上、已知行 y=217 之下；\n"
        "        // 居中 cx=450 避开右上 +VCC 端子与接地符号区 795-851），不遮挡电路；顺序仍随机\n"
        "        showMenu(null, items, true, { cx: 450, cy: 306 });   // 锁定菜单：不随鼠标离开消失",
        "        // 水平选项条固定在电路图上方空白带（等效态顶轨 y=277 之上、已知行 y=210 之下；\n"
        "        // 居中 cx=450 避开右上 +VDD 端子与接地符号区 772-828），不遮挡电路；顺序仍随机\n"
        "        showMenu(null, items, true, { cx: 450, cy: 243 });   // 锁定菜单：不随鼠标离开消失",
        'tquiz-menu-pos')

    t = rep(t,
        "        setMsg('晶体管等效 · 第 ' + (d.tquiz.step + 1) + '/' + TQUIZ.length + ' 问：' + q.q, '#ffd93d');",
        "        setMsg('场效应管等效 · 第 ' + (d.tquiz.step + 1) + '/' + TQUIZ.length + ' 问：' + q.q, '#ffd93d');",
        'tquiz-msg')

    t = rep(t,
        "        // 第 4 关状态预览：?lvl=4&tidy=1 整理+等效布局；&ts=n 再看第 n 问（1..5=各问，6=全部完成态）\n"
        "        const mt = location.search.match(/[?&]ts=(\\d+)/);\n"
        "        const mty = location.search.match(/[?&]tidy=(\\d+)/);\n"
        "        if ((mt || mty) && n === 4) {\n"
        "            const d4 = S.draw[3];\n"
        "            // 先摆出整理+等效态（电源置零、电容短路、RE 移除变导线、RB1/RC 下挂）\n"
        "            execAct('comp-vcc', 'vcc-gnd'); d4.found['comp-vcc'] = true;\n"
        "            execAct('comp-c1', 'cap-short'); d4.found['comp-c1'] = true;\n"
        "            execAct('comp-c2', 'cap-short'); d4.found['comp-c2'] = true;\n"
        "            execAct('comp-ce', 'cap-short'); d4.found['comp-ce'] = true;\n"
        "            execAct('comp-src', 'vs-keep'); d4.found['comp-src'] = true;\n"
        "            execAct('comp-re', 're-remove'); d4.found['comp-re'] = true;\n"
        "            moveCompDown('comp-rb1'); moveCompDown('comp-rc');\n"
        "            if (mt) {\n"
        "                const tv = parseInt(mt[1], 10);\n"
        "                const last = TQUIZ.length;   // 5 问\n"
        "                showEquiv();\n"
        "                fadeGroup('comp-t', true);\n"
        "                showFx('fx-tmodel', true);\n"
        "                const done = tv > last;\n"
        "                d4.tquiz = { step: done ? last : tv - 1, pool: 2 };\n"
        "                // 已作答的前 tv-1 问：逐问画出其正确结果\n"
        "                TQUIZ.slice(0, done ? last : tv - 1).forEach(q => { if (q.reveal) showFx(q.reveal, true); });\n"
        "                if (done) {\n"
        "                    d4.found['comp-t'] = true;\n"
        "                    const f = document.getElementById('fx-tmodel');\n"
        "                    if (f) f.style.pointerEvents = 'all';\n"
        "                } else {\n"
        "                    showTQuizMenu(d4);\n"
        "                }\n"
        "            }\n"
        "        }",
        "        // 第 1 关状态预览：?lvl=1&tidy=1 交流通路态（电源置零、电容短路、信号源保留）；\n"
        "        //   &ts=n 再看等效第 n 问（1..4=各问，5=全部完成态）\n"
        "        // 第 2~4 关预览：&eq=1 先摆出等效完成态（电源置零、电容短路、场效应管等效完毕）\n"
        "        const mt = location.search.match(/[?&]ts=(\\d+)/);\n"
        "        const mty = location.search.match(/[?&]tidy=(\\d+)/);\n"
        "        const meq = location.search.match(/[?&]eq=(\\d+)/);\n"
        "        if (meq && n >= 2) {\n"
        "            const d1 = S.draw[0];\n"
        "            execAct('comp-vi', 'vi-keep'); d1.found['comp-vi'] = true;\n"
        "            execAct('comp-vdd', 'vdd-gnd'); d1.found['comp-vdd'] = true;\n"
        "            execAct('comp-cb1', 'cap-short'); d1.found['comp-cb1'] = true;\n"
        "            fadeGroup('comp-t', true);\n"
        "            showFx('fx-tmodel', true);\n"
        "            showFx('fx-t-src', true);\n"
        "            d1.tquiz = { step: TQUIZ.length, pool: 5 };\n"
        "            d1.found['comp-t'] = true;\n"
        "            const f = document.getElementById('fx-tmodel');\n"
        "            if (f) f.style.pointerEvents = 'all';\n"
        "        }\n"
        "        if ((mt || mty) && n === 1) {\n"
        "            const d4 = S.draw[0];\n"
        "            // 先摆出交流通路态（电源置零、电容短路、信号源保留）\n"
        "            execAct('comp-vi', 'vi-keep'); d4.found['comp-vi'] = true;\n"
        "            execAct('comp-vdd', 'vdd-gnd'); d4.found['comp-vdd'] = true;\n"
        "            execAct('comp-cb1', 'cap-short'); d4.found['comp-cb1'] = true;\n"
        "            if (mt) {\n"
        "                const tv = parseInt(mt[1], 10);\n"
        "                const last = TQUIZ.length;   // 4 问\n"
        "                showEquiv();\n"
        "                fadeGroup('comp-t', true);\n"
        "                showFx('fx-tmodel', true);\n"
        "                const done = tv > last;\n"
        "                d4.tquiz = { step: done ? last : tv - 1, pool: 5 };\n"
        "                // 已作答的前 tv-1 问：逐问画出其正确结果\n"
        "                TQUIZ.slice(0, done ? last : tv - 1).forEach(q => { if (q.reveal) showFx(q.reveal, true); });\n"
        "                if (done) {\n"
        "                    d4.found['comp-t'] = true;\n"
        "                    const f = document.getElementById('fx-tmodel');\n"
        "                    if (f) f.style.pointerEvents = 'all';\n"
        "                } else {\n"
        "                    showTQuizMenu(d4);\n"
        "                }\n"
        "            }\n"
        "        }",
        'debug-hooks')

    t = rep(t,
        "        const ev = S.score >= 90 ? '优秀！静动态分析掌握扎实。'",
        "        const ev = S.score >= 90 ? '优秀！交流等效与动态指标掌握扎实。'",
        'done-eval')

    wt(OUT, t)
    print('OK ->', OUT, '(%d bytes)' % len(t))


if __name__ == '__main__':
    main()
