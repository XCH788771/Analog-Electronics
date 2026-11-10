# -*- coding: utf-8 -*-
"""第117轮（2026-11-02）cs-g3.html 原子补丁
① RG2 下方地线节点圆错位修复：节点 (250,525)→(280,525)，地线输入段/主段随 x=280 对齐
② 整理态：RG1 与 RG2 水平同轴（体 412-465）、顶引线改接分压节点 (280,352)、
   RG1 文字移到本体右侧 15px 同轴；收起分压节点上段导线（rg2a 302→352 段）
③ 整理态：RD 文字移到本体右侧 15px；RD 下移后收起漏极输出节点圆 (578,161.5)
④ 废除 rg2-label 各态重摆（218/427、290/427 均为过期坐标，标签固定 309.5/446）
唯一性校验全过才写盘。"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

REPS = [
# ---------- ① 地线节点错位修复 ----------
('<path class="hot" d="M 110 525 H 250" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot" d="M 110 525 H 280" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<circle cx="250" cy="525" r="7" fill="#ffffff" pointer-events="none"/>',
 '<circle cx="280" cy="525" r="7" fill="#ffffff" pointer-events="none"/>'),

('<path class="hot" d="M 250 525 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot" d="M 280 525 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

# ---------- ③ node-drain：漏极输出节点圆加 id（RD 下移后收起） ----------
('<circle cx="578" cy="161.5" r="7" fill="#ffffff" pointer-events="none"/>',
 '<circle id="node-drain" cx="578" cy="161.5" r="7" fill="#ffffff" pointer-events="none"/>'),

# ---------- ② rarr-rg1 整理态几何：同轴 412-465 + 顶引线改接节点 + 标签右置 ----------
('''        <!-- R_G1：自分压节点下挂到地轨（x=170，居于 V_i 端口与 R_G2 之间偏左；电阻体 y 375-465 与 R_G2 对齐），
             与 R_G2 并联。标签放本体左侧（x=146 起），与 R_G2 标签净距 ≥14 -->''',
 '''        <!-- R_G1：自分压节点 (280,352) 下挂到地轨（x=170，居于 V_i 端口与 R_G2 之间；
             电阻体 y 412-465 与 R_G2 水平同轴），与 R_G2 并联。标签放本体右侧（x=198.5 起、间距 15px），
             与 R_G2 标签同基线 y=446 -->'''),

('<path class="hot keepw" d="M 250 330 H 170 V 390" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot keepw" d="M 280 352 H 170 V 412" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<rect class="hot" x="156.5" y="390" width="27" height="60" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<rect class="hot" x="156.5" y="412" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<path class="hot keepw" d="M 170 450 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot keepw" d="M 170 465 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<text class="hot-label" x="146" y="427" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">G1</tspan></text>',
 '<text class="hot-label" x="198.5" y="446" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">G1</tspan></text>'),

# ---------- ③ rarr-rd 标签右置 ----------
('''        <!-- R_D：从输出导线下挂到地轨（x=700，居于 C_2 与 R_L 之间；电阻体 y 235-325 与 R_L 对齐），与 R_L 并联。
             标签放本体左侧（x=668 起、y=287 与 R_L 标签同基线），与 R_L 标签净距 ≥40 -->''',
 '''        <!-- R_D：从输出导线下挂到地轨（x=700，居于 C_2 与 R_L 之间；电阻体 y 317-370 与 R_L 对齐），与 R_L 并联。
             标签放本体右侧（x=728.5 起、间距 15px、y=350 与本体同轴），与 R_L 标签净距 ≥20 -->'''),

('<text class="hot-label" x="668" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">D</tspan></text>',
 '<text class="hot-label" x="728.5" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">D</tspan></text>'),

# ---------- ② moveCompDown(comp-rg1)：收起节点上段导线，废除 rg2-label 重摆 ----------
('''            // R_G2 标签右移到整理态安全位（避让下挂后居于其左侧的 R_G1 本体；resetCircuit 回位）
            document.querySelectorAll('.rg2-label').forEach(t => { t.setAttribute('x', '290'); t.setAttribute('y', '427'); t.setAttribute('text-anchor', 'start'); });''',
 '''            // R_G1 下挂后收起分压节点上段导线（302→352 段已无连接意义；节点改接 R_G1 下挂支路左行线）
            const wrg2a = document.querySelector('g[data-id="wire-rg2a"] path');
            if (wrg2a) wrg2a.setAttribute('d', 'M 280 352 V 412');'''),

# ---------- ③ moveCompDown(comp-rd)：收起漏极输出节点圆 ----------
('''            const f2 = document.getElementById('rarr-rd');
            if (f2) f2.style.pointerEvents = 'all';''',
 '''            const f2 = document.getElementById('rarr-rd');
            if (f2) f2.style.pointerEvents = 'all';
            // R_D 下挂后漏极输出点只剩 L 形转角（漏极引线上行→C_2 右行），节点圆多余，一并收起
            const nd = document.getElementById('node-drain');
            if (nd) nd.style.opacity = '0';'''),

# ---------- ④ resetCircuit：废除 rg2-label 过期回位，恢复动态改动 ----------
('''        // R_G2 标签回默认态位（体左侧 anchor=end x=218；整理态右移至 x=290 避让下挂件）
        document.querySelectorAll('.rg2-label').forEach(t => { t.setAttribute('x', '218'); t.setAttribute('y', '427'); t.setAttribute('text-anchor', 'end'); });''',
 '''        // R_G2 标签固定于电阻右侧同轴位（x=309.5 / y=446，与默认态一致，各态不再重摆）
        // 恢复整理态动态改动：R_G2 上段导线全长复现、漏极输出节点圆复现
        const wrg2a = document.querySelector('g[data-id="wire-rg2a"] path');
        if (wrg2a) wrg2a.setAttribute('d', 'M 280 302 V 412');
        const nd = document.getElementById('node-drain');
        if (nd) nd.style.opacity = '';'''),
]

for i, (old, new) in enumerate(REPS):
    n = c.count(old)
    if n != 1:
        print('FAIL rep#%d count=%d :: %s' % (i, n, old[:70].replace('\n', '\\n')))
        sys.exit(1)

for old, new in REPS:
    c = c.replace(old, new)

io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK all %d reps applied' % len(REPS))
