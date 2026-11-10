# -*- coding: utf-8 -*-
"""cs-g3 输入通路对齐补丁（原子写入，唯一性校验，任一不匹配则整体不写盘）
内容：
 1) 场效应管净下移 30px（当前为 +40，全部 FET 相关 y 统一 -10）
 2) R_S 居中于 S 极(246)与地(525)之间：中点 385.5，电阻体 359-412
 3) 栅极输入通路翻转为直水平线 y=208（栅极竖条中心）：wire-gate-out 去直角、
    wire-in-gate 去直角、C1 及左右导线、V_i 上端子全部对齐 y=208
 4) R_G1 随输入线下移 30px（体 158.5-211.5，输入线仍从体底部 3.5px 处穿过，
    复刻原 178/181.5 关系，避免与 wire-rg1b 导线交叉）
 5) V_i 文字与 +、- 号下移 22px（组中心 345→367 ≈ 端口顶 208 与地 525 的中点）
 6) fx-tmodel / fx-dots / fx-c1 / fx-rs 特效层同步
"""
import io, sys

PATH = r"F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html"

PAIRS = [
    # --- R_G1 下移 30（体 128.5-181.5 → 158.5-211.5），保持输入线穿体底 3.5px 关系 ---
    ('<path class="hot" d="M 250 5 V 128.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 250 5 V 158.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="236.5" y="128.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="236.5" y="158.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('x="218" y="162"', 'x="218" y="192"'),
    ('<path class="hot" d="M 250 181.5 V 370" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 250 211.5 V 370" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # --- 源极节点 256→246；R_S 居中 S(246)—地(525)：体 359-412 ---
    ('<circle cx="530" cy="256" r="7" fill="#ffffff" pointer-events="none"/>',
     '<circle cx="530" cy="246" r="7" fill="#ffffff" pointer-events="none"/>'),
    ('<path class="hot" d="M 530 256 V 309.5" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 530 246 V 359" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<rect class="hot" x="516.5" y="309.5" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="516.5" y="359" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('x="500" y="343"', 'x="500" y="393"'),
    ('<path class="hot" d="M 530 362.5 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 530 412 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('<line x1="530" y1="309.5" x2="530" y2="362.5" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>',
     '<line x1="530" y1="359" x2="530" y2="412" stroke="#34d399" stroke-width="7" stroke-linecap="round"/>'),
    ('<path class="hot" d="M 530 256 H 598 V 398" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 530 246 H 598 V 398" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    # --- FET 整体 -10（净 +30）：热区/栅极竖条/三段沟道/衬底/端子标注 ---
    ('<rect class="hot" x="438" y="158" width="158" height="140" fill="none" stroke="none"/>',
     '<rect class="hot" x="438" y="148" width="158" height="140" fill="none" stroke="none"/>'),
    ('<line class="hot" x1="502" y1="184" x2="502" y2="252" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="502" y1="174" x2="502" y2="242" stroke="#ffffff" stroke-width="7"/>'),
    ('<line class="hot" x1="530" y1="176.5" x2="530" y2="196" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="530" y1="166.5" x2="530" y2="186" stroke="#ffffff" stroke-width="7"/>'),
    ('<line class="hot" x1="530" y1="208" x2="530" y2="224" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="530" y1="198" x2="530" y2="214" stroke="#ffffff" stroke-width="7"/>'),
    ('<line class="hot" x1="530" y1="236" x2="530" y2="252" stroke="#ffffff" stroke-width="7"/>',
     '<line class="hot" x1="530" y1="226" x2="530" y2="242" stroke="#ffffff" stroke-width="7"/>'),
    ('<polygon class="hot-fill" points="530,218 554,204 554,232" fill="#ffffff" stroke="none"/>',
     '<polygon class="hot-fill" points="530,208 554,194 554,222" fill="#ffffff" stroke="none"/>'),
    ('<path class="hot" d="M 554 218 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<path class="hot" d="M 554 208 H 578" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('x="482" y="278"', 'x="482" y="268"'),
    ('x="562" y="162"', 'x="562" y="152"'),
    ('x="562" y="288"', 'x="562" y="278"'),
    ('x="592" y="230"', 'x="592" y="220"'),
    # --- 漏极引线跟随沟道上端 176.5→166.5 ---
    ('d="M 530 176.5 V 140 H 670"', 'd="M 530 166.5 V 140 H 670"'),
    # --- 栅极节点 178→208；栅极引线去直角（水平直达栅条中心）；输入线去直角 ---
    ('<circle cx="390" cy="178" r="7"', '<circle cx="390" cy="208" r="7"'),
    ('d="M 390 178 H 502 V 218"', 'd="M 390 208 H 502"'),
    ('d="M 220 218 V 178 H 390"', 'd="M 220 208 H 390"'),
    # --- C1 及左右导线对齐 y=208 ---
    ('x1="206" y1="196" x2="206" y2="240"', 'x1="206" y1="186" x2="206" y2="230"'),
    ('x1="220" y1="196" x2="220" y2="240"', 'x1="220" y1="186" x2="220" y2="230"'),
    ('x="213" y="285"', 'x="213" y="275"'),
    ('<line x1="206" y1="218" x2="220" y2="218" stroke="#34d399"',
     '<line x1="206" y1="208" x2="220" y2="208" stroke="#34d399"'),
    ('d="M 110 218 H 206"', 'd="M 110 208 H 206"'),
    ('<circle class="hot" cx="110" cy="218" r="8"', '<circle class="hot" cx="110" cy="208" r="8"'),
    # --- V_i 文字与 +、- 号下移 22（组中心 345→367 ≈ (208+525)/2）---
    ('x="110" y="275"', 'x="110" y="297"'),
    ('x="110" y="345"', 'x="110" y="367"'),
    ('x="110" y="415"', 'x="110" y="437"'),
    # --- R_G 上端接线随栅极节点 178→208 ---
    ('d="M 390 178 V 298.5"', 'd="M 390 208 V 298.5"'),
    # --- fx 层同步：G 端子/红点 → 208；受控源源极侧 → 246；菱形中心 198→193 ---
    ('<circle class="hot" cx="502" cy="218" r="6"', '<circle class="hot" cx="502" cy="208" r="6"'),
    ('d="M 530 140 V 164 H 554 V 168"', 'd="M 530 140 V 159 H 554 V 163"'),
    ('d="M 554 168 L 586 198 L 554 228 L 522 198 Z"', 'd="M 554 163 L 586 193 L 554 223 L 522 193 Z"'),
    ('d="M 554 228 V 252 H 530 V 256"', 'd="M 554 223 V 233 H 530 V 246"'),
    ('x="586" y="186"', 'x="586" y="181"'),
    ('x="590" y="218"', 'x="590" y="213"'),
    ('x1="554" y1="178" x2="554" y2="204"', 'x1="554" y1="173" x2="554" y2="199"'),
    ('points="554,216 545,201 563,201"', 'points="554,211 545,196 563,196"'),
    ('<circle class="qdot" cx="502" cy="178" r="8"', '<circle class="qdot" cx="502" cy="208" r="8"'),
    ('<circle class="qdot" cx="530" cy="216" r="8"', '<circle class="qdot" cx="530" cy="246" r="8"'),
    # --- 注释坐标同步 ---
    ('G 端子留在栅极引线末端 (502,178)', 'G 端子留在栅极引线末端 (502,208)'),
    ('与源极节点 (530,216)，菱形符号居中 (530,178)', '与源极节点 (530,246)，菱形符号居中 (554,193)'),
    ('G 在栅极引线末端 (502,178)，D 在漏极节点 (530,140)，S 在源极节点 (530,216)',
     'G 在栅极引线末端 (502,208)，D 在漏极节点 (530,140)，S 在源极节点 (530,246)'),
]

def main():
    with io.open(PATH, "r", encoding="utf-8", newline="") as f:
        s = f.read()
    for i, (old, new) in enumerate(PAIRS, 1):
        n = s.count(old)
        if n != 1:
            print("FAIL pair %d: count=%d  old=%r" % (i, n, old[:90]))
            sys.exit(1)
    for old, new in PAIRS:
        s = s.replace(old, new)
    with io.open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("OK %d pairs applied" % len(PAIRS))

main()
