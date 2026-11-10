# -*- coding: utf-8 -*-
"""cs-g1：第 3 关 R_d 下移直连
1) 菜单：R_d 点「下移」直接下挂（与输出并联），不再弹二级选项
2) R_d 上端节点移到与 v_o 水平导线相交处（y=168）；等效态（y=178 栅漏对齐布局）动态回 178
3) 删除 R_d 下端节点圆（地轨延伸段端点，L 形拐角无需节点）
"""
import io, sys

P = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()
dry = "--dry" in sys.argv
reps = []


def rep(old, new, tag):
    reps.append((old, new, tag))


# ---------- 1) SVG：rarr-rd 上端接 v_o 导线（168），上端节点随迁，删除下端节点 ----------
rep(
    '''            <!-- R_d：从漏极导线（y=178）下挂到地轨（x=640，输出端子 v_o（700）左侧，与输出并联）；
                 电阻体 y 315-405。整理态与等效态共用此件（等效后位置不变）。标签放电阻体右侧 -->
            <g id="rarr-rd" class="interactive" data-id="comp-rd" opacity="0" pointer-events="none">
                <path class="hot keepw" d="M 640 178 V 333.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <rect class="hot" x="626.5" y="333.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path class="hot keepw" d="M 640 386.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <circle cx="640" cy="178" r="8" fill="#ffffff"/>
                <circle cx="640" cy="525" r="7" fill="#ffffff"/>''',
    '''            <!-- R_d：从 v_o 水平导线（整理态 y=168）交点下挂到地轨（x=640，输出端子 v_o（692）左侧，与输出并联）；
                 电阻体 y 333.5-386.5。整理态与等效态共用此件；上端引线/节点随两态导线高度切换
                 （整理态 168 ↔ 等效态 178，见 showEquiv / resetCircuit）。下端为地轨延伸段端点（L 形拐角），不画节点 -->
            <g id="rarr-rd" class="interactive" data-id="comp-rd" opacity="0" pointer-events="none">
                <path id="rarr-rd-top" class="hot keepw" d="M 640 168 V 333.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <rect class="hot" x="626.5" y="333.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path class="hot keepw" d="M 640 386.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <circle id="rarr-rd-node" cx="640" cy="168" r="8" fill="#ffffff"/>''',
    "rarr-rd 上端接 168 / 删下端节点",
)

# ---------- 2) 菜单：R_d 下移无二级选项 ----------
rep(
    '''            if (st && (st.moveIds || []).indexOf(id) >= 0 && !(d.moved && d.moved[id])) {
                const pair = id === 'comp-rg1'
                    ? [['与RG2串', false], ['与RG2并', true]]
                    : [['与输出串', false], ['与输出并', true]];
                return [{
                    label: '下移',
                    fn: (anchor) => {
                        showMenu(anchor, pair.map(p => ({
                            label: p[0],
                            fn: () => chooseMoveOption(id, p[1])
                        })));
                    }
                }];
            }''',
    '''            if (st && (st.moveIds || []).indexOf(id) >= 0 && !(d.moved && d.moved[id])) {
                if (id === 'comp-rd') {   // R_d 下移无分支（源极接地、输出直接引出）→ 点「下移」直接下挂并联
                    return [{ label: '下移', fn: () => chooseMoveOption(id, true) }];
                }
                const pair = [['与RG2串', false], ['与RG2并', true]];
                return [{
                    label: '下移',
                    fn: (anchor) => {
                        showMenu(anchor, pair.map(p => ({
                            label: p[0],
                            fn: () => chooseMoveOption(id, p[1])
                        })));
                    }
                }];
            }''',
    "menuItemsFor: R_d 直接下移",
)

# ---------- 3) showEquiv：上端随等效态导线回到 178 ----------
rep(
    '''        const rdKeep = document.getElementById('rarr-rd');
        if (rdKeep) rdKeep.style.pointerEvents = 'all';''',
    '''        const rdKeep = document.getElementById('rarr-rd');
        if (rdKeep) rdKeep.style.pointerEvents = 'all';
        // R_d 上端引线/节点随等效态漏极横导线（y=178）回到 178（整理态为 v_o 导线 y=168）
        const rdTopE = document.getElementById('rarr-rd-top');
        if (rdTopE) rdTopE.setAttribute('d', 'M 640 178 V 333.5');
        const rdNodeE = document.getElementById('rarr-rd-node');
        if (rdNodeE) rdNodeE.setAttribute('cy', '178');''',
    "showEquiv: R_d 上端回 178",
)

# ---------- 4) resetCircuit：恢复整理态 168 ----------
rep(
    '''        document.querySelectorAll('.vdd-label, .rg2-label').forEach(t => { t.style.opacity = ''; t.style.visibility = ''; });''',
    '''        // R_d 上端引线/节点复位到整理态位（v_o 导线 y=168）
        const rdTop0 = document.getElementById('rarr-rd-top');
        if (rdTop0) rdTop0.setAttribute('d', 'M 640 168 V 333.5');
        const rdNode0 = document.getElementById('rarr-rd-node');
        if (rdNode0) rdNode0.setAttribute('cy', '168');
        document.querySelectorAll('.vdd-label, .rg2-label').forEach(t => { t.style.opacity = ''; t.style.visibility = ''; });''',
    "resetCircuit: R_d 上端复位 168",
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
