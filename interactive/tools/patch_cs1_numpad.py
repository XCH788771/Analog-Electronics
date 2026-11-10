# -*- coding: utf-8 -*-
"""cs-g1 第2关 I_DQ：常数 1 / 指数 2 方框化 + 表达式上方 0~9 数字按钮行（点框→点数字）"""
import io, sys

P = "cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()
reps = []

# ① CSS：数字按钮样式（插在 .g-opt.bad 之后）
reps.append((
"""    .g-opt.bad > rect { fill: rgba(251,113,133,0.18); stroke: #fb7185; }
""",
"""    .g-opt.bad > rect { fill: rgba(251,113,133,0.18); stroke: #fb7185; }
    /* ===== 常数数字按钮行：点虚线框 → 点数字填入（页面无键盘通道） ===== */
    .num-key { cursor: pointer; }
    .num-key rect { fill: rgba(139,92,246,0.20); stroke: #a78bfa; stroke-width: 2; transition: all 0.18s ease; }
    .num-key text { fill: #ffffff; }
    .num-key:hover rect { fill: rgba(167,139,250,0.42); stroke: #ffd93d; }
"""))

# ② buildExpr：支持 sup=1 的小号上标框
reps.append((
"""            if (tok.box) {
                const w = size * 1.18, h = size * 0.80;
                const r = document.createElementNS(NS, 'rect');
                r.setAttribute('x', cx); r.setAttribute('y', -size * 0.70);
                r.setAttribute('width', w); r.setAttribute('height', h);
                r.setAttribute('rx', 6);
                r.setAttribute('fill', 'rgba(255,217,61,0.10)');
                r.setAttribute('stroke', '#ffd93d');
                r.setAttribute('stroke-width', 2.5);
                r.setAttribute('stroke-dasharray', '8 6');
                if (blankLevel !== undefined && blankLevel !== null) {
                    r.setAttribute('class', 'blank-box');
                    r.setAttribute('data-blank-level', blankLevel);
                    r.setAttribute('data-blank-idx', ctx.n);
                    r.setAttribute('pointer-events', 'all');
                }
                ctx.n++;
                g.appendChild(r);
                cx += w + size * 0.22;""",
"""            if (tok.box) {
                // sup=1：指数常数用右上角小号框（共用虚线框 / 回填机制）
                const w = tok.sup ? size * 0.82 : size * 1.18,
                      h = tok.sup ? size * 0.60 : size * 0.80,
                      y = tok.sup ? -size * 0.70 - size * 0.52 : -size * 0.70;
                const r = document.createElementNS(NS, 'rect');
                r.setAttribute('x', cx); r.setAttribute('y', y);
                r.setAttribute('width', w); r.setAttribute('height', h);
                r.setAttribute('rx', tok.sup ? 4 : 6);
                r.setAttribute('fill', 'rgba(255,217,61,0.10)');
                r.setAttribute('stroke', '#ffd93d');
                r.setAttribute('stroke-width', 2.5);
                r.setAttribute('stroke-dasharray', '8 6');
                if (blankLevel !== undefined && blankLevel !== null) {
                    r.setAttribute('class', 'blank-box');
                    r.setAttribute('data-blank-level', blankLevel);
                    r.setAttribute('data-blank-idx', ctx.n);
                    r.setAttribute('pointer-events', 'all');
                    if (tok.sup) r.setAttribute('data-num-sup', '1');
                }
                ctx.n++;
                g.appendChild(r);
                cx += w + (tok.sup ? size * 0.06 : size * 0.22);"""))

# ③ renderMix：表达式标题后插入数字按钮行
reps.append((
"""        gameUI.appendChild(mkText(1010, BODY_TOP + 40, 26, '\u8868\u8fbe\u5f0f\uff1a', { fill: '#ffd93d' }));
        const es = 42;   // \u6587\u5b57\u6807\u51c6\uff08lin-g \u7cfb\u5217\uff09\uff1a\u586b\u7a7a\u8868\u8fbe\u5f0f 42\uff0c\u8d85\u5bbd\u81ea\u52a8\u7f29\u6392""",
"""        gameUI.appendChild(mkText(1010, BODY_TOP + 40, 26, '\u8868\u8fbe\u5f0f\uff1a', { fill: '#ffd93d' }));
        // 常数 / 指数按钮行：本子步含数字空时，在表达式上方列 0~9 圆角按钮；点虚线框 → 点数字填入
        if (sb.numPad) {
            gameUI.appendChild(mkText(LX, BODY_TOP + 100, 21, '\u5e38\u6570\uff1a\u5148\u70b9\u865a\u7ebf\u6846\uff0c\u518d\u70b9\u6570\u5b57', { fill: 'rgba(255,255,255,0.72)', bold: false }));
            const nkY = BODY_TOP + 116, nkW = 42, nkH = 44, nkGap = 8;
            '0123456789'.split('').forEach((d, di) => {
                const x = LX + 4 + di * (nkW + nkGap);
                const g = mkBtn(x, nkY, nkW, nkH, 'num-key');
                g.setAttribute('data-digit', d);
                g.appendChild(mkText(x + nkW / 2, nkY + nkH / 2 + 9, 24, d, { anchor: 'middle' }));
                gameUI.appendChild(g);
            });
        }
        const es = 42;   // \u6587\u5b57\u6807\u51c6\uff08lin-g \u7cfb\u5217\uff09\uff1a\u586b\u7a7a\u8868\u8fbe\u5f0f 42\uff0c\u8d85\u5bbd\u81ea\u52a8\u7f29\u6392"""))

# ④ renderMix 回填：指数小框用 20 号字
reps.append((
"""            const g2 = buildExpr(r.parentNode, (b.labels && b.picked && b.labels[b.picked]) || b.label, 27, '#34d399');""",
"""            const bfs = r.getAttribute('data-num-sup') ? 20 : 27;   // 指数小框用 20 号回填
            const g2 = buildExpr(r.parentNode, (b.labels && b.picked && b.labels[b.picked]) || b.label, bfs, '#34d399');"""))

# ⑤ 面板点击：数字按钮
reps.append((
"""    gameUI.addEventListener('click', e => {
        const r = e.target.closest ? e.target.closest('.blank-box') : null;""",
"""    gameUI.addEventListener('click', e => {
        // 常数数字按钮：等价于以 num-<digit> 作答当前选中的虚线框（复用 answerBlank）
        const nk = e.target.closest ? e.target.closest('.num-key') : null;
        if (nk) {
            const d = nk.getAttribute('data-digit');
            if (cur().kind === 'mix' && S.selBox && S.selBox.mix !== undefined && !S.finished) {
                answerBlank('num-' + d);
            } else {
                setMsg('\u8bf7\u5148\u70b9\u8868\u8fbe\u5f0f\u91cc\u7684\u865a\u7ebf\u6846\uff0c\u518d\u70b9\u6570\u5b57\u3002', '#ffd93d');
                render();
            }
            return;
        }
        const r = e.target.closest ? e.target.closest('.blank-box') : null;"""))

# ⑥ answerBlank：常数空 0 分，只回填不报分；答错不扣分可重试
reps.append((
"""        const full = isMix ? b.full : c.pts / c.blanks.length;
        if (b.done) return;""",
"""        const full = isMix ? b.full : c.pts / c.blanks.length;
        if (b.done) return;
        const isNum = /^num-/.test((spec.ansIds || [])[0] || '');   // 常数/指数空：0 分，只回填不报分"""))

reps.append((
"""            addScore(Math.round(b.rem));
            blinkGroup(id, '#34d399');
            setMsg('\u6b63\u786e\uff0c\u5f97 ' + Math.round(b.rem) + ' \u5206\u3002', '#34d399');
            say('\u56de\u7b54\u6b63\u786e\uff0c\u83b7\u5f97' + Math.round(b.rem) + '\u5206\u3002');""",
"""            addScore(Math.round(b.rem));
            if (!isNum) blinkGroup(id, '#34d399');
            if (isNum) {
                setMsg('\u6b63\u786e\uff0c\u5e38\u6570 ' + id.slice(4) + ' \u5df2\u586b\u5165\u3002', '#34d399');
                say('\u5e38\u6570\u586b\u5199\u6b63\u786e\u3002');
            } else {
                setMsg('\u6b63\u786e\uff0c\u5f97 ' + Math.round(b.rem) + ' \u5206\u3002', '#34d399');
                say('\u56de\u7b54\u6b63\u786e\uff0c\u83b7\u5f97' + Math.round(b.rem) + '\u5206\u3002');
            }"""))

# ⑦ 第2关 I_DQ 框架：三条选项的「1」与「²」都改方框（含上标框），不泄题
reps.append((
"""                                frameworks: [
                                    // \u6b63\u786e\uff1aI_DQ = I_DO(V_GSQ / V_GS(th) \u2212 1)\u00b2
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk('\u2212'), tk('1'), tk(')\u00b2')], correct: true },
                                    // \u5e72\u6270\u2460\uff1a\u6f0f\u6389 \u22121
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk(')\u00b2')] },
                                    // \u5e72\u6270\u2461\uff1a\u51cf\u5e8f\u98a0\u5012\uff081 \u2212 V_GSQ/V_GS(th)\uff09
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), tk('1'), tk('\u2212'), fr([{ box: 1 }], [{ box: 1 }]), tk(')\u00b2')] }
                                ]""",
"""                                frameworks: [
                                    // \u6b63\u786e\uff1aI_DQ = I_DO(V_GSQ / V_T \u2212 1)\u00b2\uff08\u5e38\u6570 1 \u4e0e\u6307\u6570 2 \u5747\u4e3a\u65b9\u6846\uff0c\u4e0d\u6cc4\u9898\uff09
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk('\u2212'), { box: 1 }, tk(')'), { box: 1, sup: 1 }], correct: true },
                                    // \u5e72\u6270\u2460\uff1a\u6f0f\u6389 \u22121
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk(')'), { box: 1, sup: 1 }] },
                                    // \u5e72\u6270\u2461\uff1a\u51cf\u5e8f\u98a0\u5012\uff081 \u2212 V_GSQ/V_T\uff09
                                    { tokens: [tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), { box: 1 }, tk('\u2212'), fr([{ box: 1 }], [{ box: 1 }]), tk(')'), { box: 1, sup: 1 }] }
                                ]"""))

# ⑧ 第2关 I_DQ 表达式：方框化 + 两个 0 分数字空
reps.append((
"""                            {
                                type: 'fill', name: 'I<tspan class="sub">DQ</tspan> \u8868\u8fbe\u5f0f',
                                fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk('\u2212'), tk('1'), tk(')\u00b2')]],
                                blanks: [
                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },
                                    { ansIds: ['q-vth'], label: [tk('V', 'GSQ')], pts: 1 },
                                    { ansIds: ['q-vt'], label: [tk('V', 'T')], pts: 1 }
                                ]
                            },""",
"""                            {
                                type: 'fill', name: 'I<tspan class="sub">DQ</tspan> \u8868\u8fbe\u5f0f',
                                numPad: true,   // \u8868\u8fbe\u5f0f\u4e0a\u65b9\u5217 0~9 \u6570\u5b57\u6309\u94ae\uff08\u5e38\u6570 1 / \u6307\u6570 2 \u7528\u70b9\u9009\u8f93\u5165\uff09
                                fullExpr: [[tk('I', 'DQ'), tk('='), { box: 1 }, tk('('), fr([{ box: 1 }], [{ box: 1 }]), tk('\u2212'), { box: 1 }, tk(')'), { box: 1, sup: 1 }]],
                                blanks: [
                                    { ansIds: ['q-ido'], label: [tk('I', 'DO')], pts: 2 },
                                    { ansIds: ['q-vth'], label: [tk('V', 'GSQ')], pts: 1 },
                                    { ansIds: ['q-vt'], label: [tk('V', 'T')], pts: 1 },
                                    // \u5e38\u6570 / \u6307\u6570\u7a7a\u4e0d\u8ba1\u5206\uff08\u4fdd\u6301 24 \u5206\u914d\u5e73\uff09\uff1a\u7b54\u6848\u8d70 num-N\uff0c\u7531\u6570\u5b57\u6309\u94ae\u70b9\u51fb\u8f93\u5165
                                    { ansIds: ['num-1'], label: [tk('1')], pts: 0 },
                                    { ansIds: ['num-2'], label: [tk('2')], pts: 0 }
                                ]
                            },"""))

ok = True
for i, (o, n) in enumerate(reps, 1):
    c = s.count(o)
    print("rep%d %s" % (i, "OK" if c == 1 else "FAIL count=%d" % c))
    if c != 1: ok = False
if not ok:
    print("有替换未唯一命中，未写盘")
    sys.exit(1)
for o, n in reps: s = s.replace(o, n)

# 分值配平自检：第2关 mix 总分 24
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("已写盘")
