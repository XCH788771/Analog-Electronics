# -*- coding: utf-8 -*-
"""第118轮（2026-11-02）cs-g3.html 原子补丁
① C_2 右移到输出水平导线正中：水平段 578（漏极输出节点）→850（R_L 支路），中点 714；
   板 670/684 → 707/721，短接桥 fx-c2 同步；R_D 下挂支路 x 700→690（节点圆 693-697 与桥 707 起净隙 10，
   标签 712.5 起、右缘 759.3 与 R_L 标签 778.8 净隙 19.5）
② 信号源与直流电源不分先后：gate ['comp-vdd'] → ['comp-vdd','comp-vi']，文案同步
唯一性校验全过才写盘。"""
import io, sys

P = 'cs-g3.html'
c = io.open(P, newline='', encoding='utf-8').read()

REPS = [
# ---------- ① C_2 主体 / 标签 ----------
('<line class="hot" x1="670" y1="139.5" x2="670" y2="183.5" stroke="#ffffff" stroke-width="3.5"/>',
 '<line class="hot" x1="707" y1="139.5" x2="707" y2="183.5" stroke="#ffffff" stroke-width="3.5"/>'),

('<line class="hot" x1="684" y1="139.5" x2="684" y2="183.5" stroke="#ffffff" stroke-width="3.5"/>',
 '<line class="hot" x1="721" y1="139.5" x2="721" y2="183.5" stroke="#ffffff" stroke-width="3.5"/>'),

('<text class="hot-label" x="677" y="124" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">2</tspan></text>',
 '<text class="hot-label" x="714" y="124" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="middle">C<tspan class="sub">2</tspan></text>'),

# ---------- ① C_2 两侧水平导线 ----------
('<path class="hot" d="M 578 161.5 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot" d="M 578 161.5 H 707" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<path class="hot" d="M 684 161.5 H 850" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot" d="M 721 161.5 H 850" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

# ---------- ① 短接桥 fx-c2 ----------
('''                <!-- 平头端帽：桥体恰为 670-684（替代 C_2 两板；整理态 R_D 下挂节点在 x=700，与桥分立） -->
                <line x1="670" y1="161.5" x2="684" y2="161.5" stroke="#34d399" stroke-width="7"/>''',
 '''                <!-- 平头端帽：桥体恰为 707-721（替代 C_2 两板；整理态 R_D 下挂节点在 x=690，与桥分立） -->
                <line x1="707" y1="161.5" x2="721" y2="161.5" stroke="#34d399" stroke-width="7"/>'''),

# ---------- ① R_D 下挂支路 700→690 ----------
('''        <!-- R_D：从输出导线下挂到地轨（x=700，居于 C_2 与 R_L 之间；电阻体 y 317-370 与 R_L 对齐），与 R_L 并联。''',
 '''        <!-- R_D：从输出导线下挂到地轨（x=690，居于 C_S 支路与 C_2 之间；电阻体 y 317-370 与 R_L 对齐），与 R_L 并联。'''),

('<path class="hot keepw" d="M 700 161.5 V 317" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot keepw" d="M 690 161.5 V 317" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<rect class="hot" x="686.5" y="317" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<rect class="hot" x="676.5" y="317" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<path class="hot keepw" d="M 700 370 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
 '<path class="hot keepw" d="M 690 370 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

('<circle cx="700" cy="161.5" r="7" fill="#ffffff"/>',
 '<circle cx="690" cy="161.5" r="7" fill="#ffffff"/>'),

('<circle cx="700" cy="525" r="7" fill="#ffffff"/>',
 '<circle cx="690" cy="525" r="7" fill="#ffffff"/>'),

('<text class="hot-label" x="722.5" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">D</tspan></text>',
 '<text class="hot-label" x="712.5" y="350" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">D</tspan></text>'),

('标签放本体右侧（x=722.5 起、y=350 与本体同轴），与 R_L 标签净隙 ≥9.5',
 '标签放本体右侧（x=712.5 起、y=350 与本体同轴），与 R_L 标签净隙 ≥19'),

# ---------- ② 信号源与直流电源不分先后 ----------
('        moveIds：RG1 下挂（与 RG2 并）、RD 下挂（与 RL 并）；gate：+VDD 先处理完才放行电容',
 '        moveIds：RG1 下挂（与 RG2 并）、RD 下挂（与 RL 并）；gate：信号源与直流电源（不分先后）处理后放行电容'),

('''                        gateMsg: '请先处理直流电源，再处理电容。',
                        gateTodo: '当前：先处理直流电源',
                        gateDoneMsg: '电源已处理，按当前步骤继续处理',
                        // 门控：+VDD 必须先处理完（置零接地），电容等其它目标才解锁
                        gate: ['comp-vdd'],''',
 '''                        gateMsg: '请先处理信号源与直流电源（两者不分先后），再处理电容。',
                        gateTodo: '当前：先处理信号源和直流电源（不分先后）',
                        gateDoneMsg: '信号源与电源已处理，按当前步骤继续处理',
                        // 门控：+VDD 与输入信号源 V_i 都处理完（不分先后），电容等其它目标才解锁
                        gate: ['comp-vdd', 'comp-vi'],'''),

('先处理直流电源和输入信号源，再处理三只电容绘制交流通路',
 '先处理直流电源和输入信号源（两者不分先后），再处理三只电容绘制交流通路'),
]

for i, (old, new) in enumerate(REPS):
    n = c.count(old)
    if n != 1:
        print('FAIL rep#%d count=%d :: %s' % (i, n, old[:70].replace('\n', '\\n')))
        sys.exit(1)
for old, new in REPS:
    c = c.replace(old, new)
io.open(P, 'w', newline='', encoding='utf-8').write(c)
print('OK %d reps' % len(REPS))
