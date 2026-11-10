# -*- coding: utf-8 -*-
"""cs-g1 等效态第二轮：删绿桥 / 选项与图注改 g_m·v_gs / g_m 标注置于 v_gs 与受控源之间
1) eq-layer 删 C_1 短接绿桥（R_g1 左上侧一小段，206,178→220,178）
2) 第 4 问选项文字 i_d → g_m·v_gs（含题面）；图中 g_m·v_gs 标注改为「点选项后」才显示
3) v_gs 标注列左移 10px（445→435）腾位；受控源菱形左侧新增 g_m 标注（x=479，与 v_gs 同基线同轴）
"""
import io, sys

P = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()
dry = "--dry" in sys.argv
reps = []


def rep(old, new, tag):
    reps.append((old, new, tag))


# ---------- 1) 删绿桥 ----------
rep(
    '''                <!-- C_1 短接桥（随线上移） -->
                <line x1="206" y1="178" x2="220" y2="178" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>
''',
    '''                <!-- C_1 短接桥已移除：输入主线本身即短接后的通路，不再叠绿色短接线 -->
''',
    "删 C_1 绿桥",
)

# ---------- 2) v_gs 列左移 10px（腾出 g_m 位） ----------
rep(
    '''                <g id="fx-t-vgs" opacity="0">
                    <text x="445" y="213" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text x="445" y="352" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">v<tspan class="sub">gs</tspan></text>
                    <text x="445" y="495" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>''',
    '''                <g id="fx-t-vgs" opacity="0">
                    <text x="435" y="213" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text x="435" y="352" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">v<tspan class="sub">gs</tspan></text>
                    <text x="435" y="495" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>''',
    "v_gs 左移 10px",
)

# ---------- 3) 受控源菱形左侧加 g_m（与 v_gs 同轴） ----------
rep(
    '''                    <!-- 落地点：地线中段 T 形交汇（左—右—上），画节点圆 -->
                    <circle class="hot" cx="530" cy="525" r="7" fill="#ffffff"/>''',
    '''                    <!-- 增益标注 g_m：夹在 v_gs（控制量）与菱形（受控源）之间，与 v_gs 同基线水平同轴 -->
                    <text x="479" y="352" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">g<tspan class="sub">m</tspan></text>
                    <!-- 落地点：地线中段 T 形交汇（左—右—上），画节点圆 -->
                    <circle class="hot" cx="530" cy="525" r="7" fill="#ffffff"/>''',
    "加 g_m 标注",
)

# ---------- 4) 选项文字 → g_m·v_gs ----------
rep(
    '''    // 电流方向问的选项渲染：↑/↓ + 带下标的符号（↓i_d → ↓i 加下标 d）；其余选项返回 null 走纯文本
    const TQ_SUBD = '<span style="font-size:0.72em;vertical-align:-0.16em">d</span>';
    function tquizOptHtml(op) {
        const c = op.charAt(0);
        if (c !== '↑' && c !== '↓') return null;
        return c + 'i' + TQ_SUBD;
    }''',
    '''    // 电流方向问的选项渲染：↑/↓ + g_m·v_gs（下标用小号行内 span）；其余选项返回 null 走纯文本
    const TQ_SUBD = '<span style="font-size:0.72em;vertical-align:-0.16em">m</span>';
    const TQ_SUBD2 = '<span style="font-size:0.72em;vertical-align:-0.16em">gs</span>';
    function tquizOptHtml(op) {
        const c = op.charAt(0);
        if (c !== '↑' && c !== '↓') return null;
        return c + 'g' + TQ_SUBD + '·v' + TQ_SUBD2;
    }''',
    "选项渲染 g_m·v_gs",
)

# ---------- 5) 题面文案 i_d → g_m·v_gs ----------
rep(
    '''          q: '在受控源支路添加电流 i_d 与箭头，箭头方向是？', reveal: 'fx-t-id' }''',
    '''          q: '受控源支路电流为 g_m·v_gs，箭头方向是？', reveal: 'fx-t-id' }''',
    "题面文案",
)

# ---------- 6) 图注显示时机：选项弹出时不显示，作答后才显示 ----------
rep(
    '''        q.dots.forEach(id => showFx(id, true));
        setEPos(q.epos);
        if (q.idlabel) showFx(q.idlabel, true);   // 第 4 问：选项弹出时先显数值 g_m·v_gs（箭头待作答后画）''',
    '''        q.dots.forEach(id => showFx(id, true));
        setEPos(q.epos);''',
    "撤销选项期显示",
)

rep(
    '''        if (q.reveal) showFx(q.reveal, true);
        d.tquiz.step++;''',
    '''        if (q.reveal) showFx(q.reveal, true);
        if (q.idlabel) showFx(q.idlabel, true);   // 箭头旁的 g_m·v_gs 数值：作答后才与箭头同时出现
        d.tquiz.step++;''',
    "作答后显示图注",
)

ok = True
out = s
for old, new, tag in reps:
    n = out.count(old)
    if n != 1:
        print("FAIL [%s] count=%d" % (tag, n))
        ok = False
        continue
    out = out.replace(old, new)
    print("OK   [%s]" % tag)

if not ok:
    print("未写盘")
    sys.exit(1)
if dry:
    print("dry-run 完成，未写盘")
    sys.exit(0)
io.open(P, "w", encoding="utf-8", newline="").write(out)
print("已写盘")
