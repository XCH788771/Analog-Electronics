# -*- coding: utf-8 -*-
# round-91（B 文件）：
#  ① 等效态 V_i 负极下方圆圈被地轨横线穿过圆心（圆绘制在横线之前）→ 改绘到横线之后（深绿填充遮线，同 + 极上方圆）
#  ② 删第90轮 3 段跨层补线（保留件改由引擎 tidyShift('keep',25) 整体平移，直接与地轨/横线相接）
#  ③ i_b / βi_b 文字与箭头上移 15px（在 r90 +25 基础上 -15 → 净 +10）
#  ④ rearr-layer 增加整理态接缝补线组 fx-tidy-lines（上部电路上移 15px 后与地轨母线顶 525 之间的 5 段）
import io, sys, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_B.txt')
s = io.open(P, 'r', encoding='utf-8', newline='').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        print('FAIL count=%d (want %d): %s' % (c, n, old[:76]))
        sys.exit(1)
    s = s.replace(old, new)
    print('OK  %s' % old[:64])

# ── ② 删第90轮 3 段跨层补线（改为引擎状态位移）──────────────────────────────
rep('''                <!-- 第90轮：整体下移 25px 后与默认层保留件的跨层补线
                     （fx-c2 短接桥 670,176 / R_L 下端 800,525 / 整理态 R_C 下端 640,525 → 渲染各 +25） -->
                <path d="M 670 151 V 176" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 800 500 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 640 500 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
''',
    '''                <!-- 第91轮：删第90轮补线——等效态保留件由引擎 tidyShift('keep',25) 整体平移，直接与地轨/集电极横线相接 -->
''')

# ── ① V_i 负极下方圆圈改绘到地轨横线之后（不穿过圆心）──────────────────────
rep('''                <text x="150" y="495" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>
                <!-- 第89轮：负极下方多余导线与节点圆移除，圆圈只保留在接地导线（地轨 y=525）上 -->
                <circle cx="150" cy="525" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
''',
    '''                <text x="150" y="495" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>
''')
rep('''                <!-- 公共地轨（第66轮）：V_s 负极(90) → V_o 负极(R_L 下端 800) 一根导线，替代各自独立的接地符号 -->
                <path d="M 90 525 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>
''',
    '''                <!-- 公共地轨（第66轮）：V_s 负极(90) → V_o 负极(R_L 下端 800) 一根导线，替代各自独立的接地符号 -->
                <path d="M 90 525 H 800" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <!-- 第91轮：V_i 负极下方圆圈必须绘在地轨横线之后——深绿填充遮住穿过圆心的线段（与 + 极上方圆同效） -->
                <circle cx="150" cy="525" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
''')

# ── ③ i_b / βi_b 文字与箭头上移 15px（r90 +25 → 净 +10）───────────────────
rep('<line x1="380" y1="221" x2="380" y2="251" stroke="#ff5252" stroke-width="5"/>',
    '<line x1="380" y1="206" x2="380" y2="236" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon points="380,265 372,250 388,250" fill="#ff5252" stroke="none"/>',
    '<polygon points="380,250 372,235 388,235" fill="#ff5252" stroke="none"/>')
rep('<text x="364" y="254" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">i<tspan class="sub">b</tspan></text>',
    '<text x="364" y="239" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">i<tspan class="sub">b</tspan></text>')
rep('<line x1="520" y1="221" x2="520" y2="251" stroke="#ff5252" stroke-width="5"/>',
    '<line x1="520" y1="206" x2="520" y2="236" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon points="520,265 512,250 528,250" fill="#ff5252" stroke="none"/>',
    '<polygon points="520,250 512,235 528,235" fill="#ff5252" stroke="none"/>')
rep('<text x="504" y="254" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">βi<tspan class="sub">b</tspan></text>',
    '<text x="504" y="239" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">βi<tspan class="sub">b</tspan></text>')

# ── ④ 整理态接缝补线组（rearr-layer 内，随整理态显隐）──────────────────────
rep('''                <text class="hot-label" x="670" y="359" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">C</tspan></text>
            </g>
            </g>''',
    '''                <text class="hot-label" x="670" y="359" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">C</tspan></text>
            </g>
            <!-- 第91轮：整理态接缝补线——上部电路整体上移 15px（引擎 tidyShift('up',-15)）后，
                 与「保持不动的下方接地系统」之间的 5 段 15px 短接：
                 信号源接地(90) / R_B 下端(320) / R_C 下端(640) / R_L 下端(800) / C_E 支路(598，re2-keep 路线) → 地轨母线顶 525 -->
            <g id="fx-tidy-lines" opacity="0">
                <path d="M 90 510 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 320 510 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 640 510 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 800 510 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 598 510 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            </g>
            </g>''')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('WROTE %s' % P)
