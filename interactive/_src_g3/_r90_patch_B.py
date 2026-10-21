# -*- coding: utf-8 -*-
# round-90（B 文件）：
#  ① V_i 负极下方地轨母线（fx-gnd-rail 横线 y=573）上加空心圆圈，与 + 极上方端子圆 (150,260) 垂直同轴
#  ② R_L 下移至输出水平导线(176)与地(525)正中间（体 323-378，上下引线各 147px）；
#     整理态 R_C（rarr-rc）同步下移保持与 R_L 水平同轴；V_o 标注随 R_L 同步下移
#  ③ 等效态整体下移 25px：eq-layer 与 fx-tmodel 加 transform，fx-dot-b/c/e、fx-t-ib/ic、fx-gnd-e 同步 +25；
#     eq-layer 内 V_i 负极下方实心点改空心圆圈（与 + 极上方圆同款）；
#     补 3 段跨层连接线（fx-c2 短接桥 670 / R_L 下端 800 / 整理态 R_C 下端 640）
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

# ── ② R_L 下移 21px（体中心 329.5 → 350.5）────────────────────────────────
rep('<path class="hot" d="M 800 176 V 302" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot" d="M 800 176 V 323" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<rect class="hot" x="782" y="302" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<rect class="hot" x="782" y="323" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<text class="hot-label" x="770" y="338" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>',
    '<text class="hot-label" x="770" y="359" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">L</tspan></text>')
rep('<path class="hot" d="M 800 357 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot" d="M 800 378 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
# V_o 标注随 R_L 同步下移 21px
rep('<rect class="hot" x="836" y="313" width="44" height="70" fill="none" stroke="none"/>',
    '<rect class="hot" x="836" y="334" width="44" height="70" fill="none" stroke="none"/>')
rep('<text class="hot-label" x="858" y="311" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>',
    '<text class="hot-label" x="858" y="332" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">＋</text>')
rep('<text class="hot-label" x="858" y="357" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">o</tspan></text>',
    '<text class="hot-label" x="858" y="378" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">o</tspan></text>')
rep('<text class="hot-label" x="858" y="428" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
    '<text class="hot-label" x="858" y="449" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>')
# 整理态 R_C（rarr-rc）同步下移 21px，与 R_L 水平同轴
rep('<path class="hot keepw" d="M 640 176 V 302" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot keepw" d="M 640 176 V 323" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<rect class="hot" x="622" y="302" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<rect class="hot" x="622" y="323" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<path class="hot keepw" d="M 640 357 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot keepw" d="M 640 378 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<text class="hot-label" x="670" y="338" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">C</tspan></text>',
    '<text class="hot-label" x="670" y="359" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">C</tspan></text>')

# ── ① 地轨母线（y=573）上 x=150 加空心节点圆（与 + 极上方端子圆同款同轴）──────
rep('''                <!-- 节点圆：R_B(320) / RE2 下端—−V_EE 端子(486) 两处 T 结 -->
                <circle cx="320" cy="573" r="7" fill="#ffffff"/>''',
    '''                <!-- 节点圆（第90轮）：V_i 负极(150) 空心圆，与 + 极上方端子圆(150,260) 垂直同轴；R_B(320) / RE2 下端—−V_EE 端子(486) T 结 -->
                <circle cx="150" cy="573" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>
                <circle cx="320" cy="573" r="7" fill="#ffffff"/>''')

# ── ③ 等效态整体下移 25px ─────────────────────────────────────────────────
rep('<g id="eq-layer" opacity="0" pointer-events="none">',
    '<g id="eq-layer" opacity="0" pointer-events="none" transform="translate(0,25)">')
rep('<g id="fx-tmodel" class="interactive" data-id="comp-t-model" opacity="0" pointer-events="none">',
    '<g id="fx-tmodel" class="interactive" data-id="comp-t-model" opacity="0" pointer-events="none" transform="translate(0,25)">')
# V_i 负极下方实心点 → 空心圆圈（与 + 极上方圆同款；随层 +25 落在地轨上）
rep('<circle cx="150" cy="525" r="7" fill="#ffffff"/>',
    '<circle cx="150" cy="525" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>')
# 五连问端点红点 +25
rep('<circle class="qdot" cx="380" cy="176" r="8" fill="#ff5252"/>',
    '<circle class="qdot" cx="380" cy="201" r="8" fill="#ff5252"/>')
rep('<circle class="qdot" cx="520" cy="176" r="8" fill="#ff5252"/>',
    '<circle class="qdot" cx="520" cy="201" r="8" fill="#ff5252"/>')
rep('<circle class="qdot" cx="380" cy="370" r="8" fill="#ff5252"/>',
    '<circle class="qdot" cx="380" cy="395" r="8" fill="#ff5252"/>')
# i_b / βi_b 箭头 +25
rep('<line x1="380" y1="196" x2="380" y2="226" stroke="#ff5252" stroke-width="5"/>',
    '<line x1="380" y1="221" x2="380" y2="251" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon points="380,240 372,225 388,225" fill="#ff5252" stroke="none"/>',
    '<polygon points="380,265 372,250 388,250" fill="#ff5252" stroke="none"/>')
rep('<text x="364" y="229" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">i<tspan class="sub">b</tspan></text>',
    '<text x="364" y="254" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">i<tspan class="sub">b</tspan></text>')
rep('<line x1="520" y1="196" x2="520" y2="226" stroke="#ff5252" stroke-width="5"/>',
    '<line x1="520" y1="221" x2="520" y2="251" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon points="520,240 512,225 528,225" fill="#ff5252" stroke="none"/>',
    '<polygon points="520,265 512,250 528,250" fill="#ff5252" stroke="none"/>')
rep('<text x="504" y="229" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">βi<tspan class="sub">b</tspan></text>',
    '<text x="504" y="254" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">βi<tspan class="sub">b</tspan></text>')
# 等效态发射极接地符号 fx-gnd-e +25（接 eq-re1 下端 550）
rep('<line x1="450" y1="525" x2="450" y2="543" stroke="#ffffff" stroke-width="3"/>',
    '<line x1="450" y1="550" x2="450" y2="568" stroke="#ffffff" stroke-width="3"/>')
rep('<line x1="422" y1="543" x2="478" y2="543" stroke="#ffffff" stroke-width="3.5"/>',
    '<line x1="422" y1="568" x2="478" y2="568" stroke="#ffffff" stroke-width="3.5"/>')
rep('<line x1="432" y1="551" x2="468" y2="551" stroke="#ffffff" stroke-width="3"/>',
    '<line x1="432" y1="576" x2="468" y2="576" stroke="#ffffff" stroke-width="3"/>')
rep('<line x1="440" y1="559" x2="460" y2="559" stroke="#ffffff" stroke-width="2.5"/>',
    '<line x1="440" y1="584" x2="460" y2="584" stroke="#ffffff" stroke-width="2.5"/>')
# 跨层补线：eq-layer 下移后与默认层保留件（fx-c2 短接桥 670 / R_L 下端 800 / 整理态 R_C 下端 640）接续
rep('''                <circle cx="640" cy="525" r="7" fill="#ffffff"/>
            </g>''',
    '''                <circle cx="640" cy="525" r="7" fill="#ffffff"/>
                <!-- 第90轮：整体下移 25px 后与默认层保留件的跨层补线
                     （fx-c2 短接桥 670,176 / R_L 下端 800,525 / 整理态 R_C 下端 640,525 → 渲染各 +25） -->
                <path d="M 670 151 V 176" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 800 500 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
                <path d="M 640 500 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>
            </g>''')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('WROTE %s' % P)
