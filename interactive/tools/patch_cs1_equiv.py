# -*- coding: utf-8 -*-
"""cs-g1 第 3 关等效态：源极直落地 + g/s 垂直同轴 + v_gs 重排 + 受控源下移 + g_m·v_gs 标注改到 i_d 位
1) 删除 eq-layer 源极线（M 486 525 V 420 H 530：地端上方那段竖导线）
2) S 红点 (486,420) → (420,525)：落在地线上，与 G 红点 (420,178) 垂直同轴
3) v_gs 列随 g—s 跨度重排（x=445：＋213 / v_gs 352 / －495）
4) 受控源支路 x=530 直落地面：上引线 178→319、菱形中心 (530,351)、下引线 383→525 + 落地点节点圆
5) 菱形旁 g_m·v_gs 文字删除（第 4 问前不显示）；第 4 问箭头旁的 i_d 文字改为 g_m·v_gs（位置不变）
6) setEPos 目标 id 修正（#fx-dot-e → #fx-dot-s，第 3 问 S 点随受控源支路移到 530）
"""
import io, sys

P = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()
dry = "--dry" in sys.argv
reps = []


def rep(old, new, tag):
    reps.append((old, new, tag))


# ---------- 1) 删除 eq-layer 源极线 ----------
rep(
    '''                <!-- 源极线：受控源下端（530,420）←→ 源极落点（486,420）→ 直落地轨（本案例无 R_s） -->
                <path d="M 486 525 V 420 H 530" fill="none" stroke="#ffffff" stroke-width="3.5"/>
''',
    '''                <!-- 源极：经受控源支路（x=530）直接落地线 y=525，无独立源极引线（本案例无 R_s） -->
''',
    "eq-layer 删源极线",
)

# ---------- 2) fx-tmodel 头注释更新 ----------
rep(
    '''            <!-- 场效应管微变等效模型（v_gs 标注 + 受控电流源（VCCS，菱形）+ 电流 i_d 及箭头）；逐问显示。
                 等效布局：栅极线 y=178 止于 g 节点（栅极开路），受控源支路挂漏极导线 x=530，
                 源极横线 y=420 连接受控源下端与 R_s（eq-layer 重绘），v_gs 标注列在 g—s 之间 -->''',
    '''            <!-- 场效应管微变等效模型（v_gs 标注 + 受控电流源（VCCS，菱形）+ 电流及箭头）；逐问显示。
                 等效布局：栅极线 y=178 止于 g 节点（栅极开路）；s 点取在 g 正下方的地线上（x=420 垂直同轴，
                 两问红点同为 420 → 一眼看出 G—S、G—D 段开路）；受控源支路挂漏极导线 x=530 后直落地线 y=525；
                 v_gs 标注列在 x=445 的 g—s 跨度内 -->''',
    "fx-tmodel 注释",
)

# ---------- 3) v_gs 标注重排 ----------
rep(
    '''                <g id="fx-t-vgs" opacity="0">
                    <text x="445" y="235" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text x="445" y="318" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">v<tspan class="sub">gs</tspan></text>
                    <text x="445" y="398" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>''',
    '''                <g id="fx-t-vgs" opacity="0">
                    <text x="445" y="213" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">＋</text>
                    <text x="445" y="352" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="middle">v<tspan class="sub">gs</tspan></text>
                    <text x="445" y="495" fill="#ffe66d" font-size="28" font-weight="bold" text-anchor="middle">－</text>
                </g>''',
    "v_gs 重排",
)

# ---------- 4) 受控源支路下移直落地面 + 删 gm·vgs 文字 ----------
rep(
    '''                <g id="fx-t-src" opacity="0">
                    <line class="hot keepw" x1="530" y1="178" x2="530" y2="268" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 压控电流源（VCCS）：菱形符号，菱形内以横线连接左右顶点 -->
                    <path class="hot" d="M 530 268 L 560 300 L 530 332 L 500 300 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>
                    <line class="hot" x1="500" y1="300" x2="560" y2="300" stroke="#ffffff" stroke-width="3"/>
                    <line class="hot keepw" x1="530" y1="332" x2="530" y2="420" stroke="#ffffff" stroke-width="3.5"/>
                    <text x="568" y="292" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>
                </g>''',
    '''                <g id="fx-t-src" opacity="0">
                    <line class="hot keepw" x1="530" y1="178" x2="530" y2="319" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 压控电流源（VCCS）：菱形符号，菱形内以横线连接左右顶点（菱形中心 351 = 178—525 中点） -->
                    <path class="hot" d="M 530 319 L 560 351 L 530 383 L 500 351 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>
                    <line class="hot" x1="500" y1="351" x2="560" y2="351" stroke="#ffffff" stroke-width="3"/>
                    <line class="hot keepw" x1="530" y1="383" x2="530" y2="525" stroke="#ffffff" stroke-width="3.5"/>
                    <!-- 落地点：地线中段 T 形交汇（左—右—上），画节点圆 -->
                    <circle class="hot" cx="530" cy="525" r="7" fill="#ffffff"/>
                    <!-- 受控源电流数值标注不在此处：第 4 问选定方向后由 fx-t-id 在箭头旁标 g_m·v_gs -->
                </g>''',
    "受控源下移直落地",
)

# ---------- 5) fx-t-id 文字 i_d → g_m·v_gs ----------
rep(
    '''                    <text x="548" y="222" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">i<tspan class="sub">d</tspan></text>''',
    '''                    <!-- 第 4 问画出电流箭头后才标数值 g_m·v_gs（此前不显示任何电流标注） -->
                    <text x="548" y="222" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">g<tspan class="sub">m</tspan>·v<tspan class="sub">gs</tspan></text>''',
    "i_d 文字 → g_m·v_gs",
)

# ---------- 6) S 红点位置 ----------
rep(
    '''            <g id="fx-dot-s" opacity="0">
                <circle class="qdot" cx="486" cy="420" r="8" fill="#ff5252"/>
            </g>''',
    '''            <g id="fx-dot-s" opacity="0">
                <circle class="qdot" cx="420" cy="525" r="8" fill="#ff5252"/>
            </g>''',
    "S 红点 → (420,525)",
)

# ---------- 7) setEPos 目标 id 修正 ----------
rep(
    '''    function setEPos(x) {
        const c = document.querySelector('#fx-dot-e circle');
        if (c) c.setAttribute('cx', x ? String(x) : EDOT_X0);
    }''',
    '''    function setEPos(x) {   // 第 3 问 S 点随受控源支路移到其落地处（530），其余问回到 g 正下方（420）
        const c = document.querySelector('#fx-dot-s circle');
        if (c) c.setAttribute('cx', x ? String(x) : EDOT_X0);
    }''',
    "setEPos id 修正",
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
