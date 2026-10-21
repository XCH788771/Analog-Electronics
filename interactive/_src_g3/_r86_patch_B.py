# -*- coding: utf-8 -*-
"""cj-g3 第86轮 区B 几何补丁（需求1/2/3）：
   需求1：q-ibq（I_BQ 标注+箭头）右移 20px（与 R_B 支路导线间距 40→20，减半）
   需求2：交流等效态红框内对象整体左移 40px
   需求3：发射极横线上移 30px、R_E1 上移 15px、r_be/受控源上移 15px
   原子补丁：rep() 唯一性校验，失败 exit 不写盘；CRLF 保真。
"""
import io, sys, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_B.txt')
with io.open(P, encoding='utf-8', newline='') as f:
    raw = f.read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')
n0 = s

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.stderr.write('ANCHOR FAIL (%d!=1): %r\n' % (n, old[:70]))
        sys.exit(1)
    s = s.replace(old, new, 1)

# ============ 需求1：q-ibq 右移 20px（箭头 x280→300、文字 end 264→284、热区 206→226）============
rep('<rect class="hot" x="206" y="280" width="88" height="72" fill="none" stroke="none"/>',
    '<rect class="hot" x="226" y="280" width="88" height="72" fill="none" stroke="none"/>')
rep('<line class="hot" x1="280" y1="346" x2="280" y2="300" stroke="#ff5252" stroke-width="5"/>',
    '<line class="hot" x1="300" y1="346" x2="300" y2="300" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon class="hot-fill" points="280,286 272,301 288,301" fill="#ff5252" stroke="none"/>',
    '<polygon class="hot-fill" points="300,286 292,301 308,301" fill="#ff5252" stroke="none"/>')
rep('<text class="hot-label" x="264" y="322" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">I<tspan class="sub">BQ</tspan></text>',
    '<text class="hot-label" x="284" y="322" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">I<tspan class="sub">BQ</tspan></text>')

# ============ 需求2：fx-gnd-e 接地符号左移 40px（490→450 居中）============
rep('<line x1="490" y1="525" x2="490" y2="543" stroke="#ffffff" stroke-width="3"/>',
    '<line x1="450" y1="525" x2="450" y2="543" stroke="#ffffff" stroke-width="3"/>')
rep('<line x1="462" y1="543" x2="518" y2="543" stroke="#ffffff" stroke-width="3.5"/>',
    '<line x1="422" y1="543" x2="478" y2="543" stroke="#ffffff" stroke-width="3.5"/>')
rep('<line x1="472" y1="551" x2="508" y2="551" stroke="#ffffff" stroke-width="3"/>',
    '<line x1="432" y1="551" x2="468" y2="551" stroke="#ffffff" stroke-width="3"/>')
rep('<line x1="480" y1="559" x2="500" y2="559" stroke="#ffffff" stroke-width="2.5"/>',
    '<line x1="440" y1="559" x2="460" y2="559" stroke="#ffffff" stroke-width="2.5"/>')

# ============ 需求2/3：eq-layer 导线（左右端随组件左移；横线上移 30px）============
rep('<path d="M 90 176 H 420" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path d="M 90 176 H 380" fill="none" stroke="#ffffff" stroke-width="3.5"/>')          # 基极输入主线右端 420→380
rep('<path d="M 560 176 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path d="M 520 176 H 670" fill="none" stroke="#ffffff" stroke-width="3.5"/>')        # 集电极横导线左端 560→520
rep('<path d="M 420 400 H 560" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path d="M 380 370 H 520" fill="none" stroke="#ffffff" stroke-width="3.5"/>')        # 发射极横线 左移40 + 上移30

# ============ 需求2：eq-rb 左移 40px（320→280）============
rep('<path class="hot keepw" d="M 320 176 V 292" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot keepw" d="M 280 176 V 292" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<rect class="hot" x="302" y="292" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<rect class="hot" x="262" y="292" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<path class="hot keepw" d="M 320 347 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot keepw" d="M 280 347 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<circle cx="320" cy="176" r="7" fill="#ffffff"/>',
    '<circle cx="280" cy="176" r="7" fill="#ffffff"/>')
rep('<text class="hot-label" x="288" y="328" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">B</tspan></text>',
    '<text class="hot-label" x="248" y="328" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">B</tspan></text>')

# ============ 需求2/3：eq-re1 左移 40px（490→450）+ 上移（体 435→420、横线→370）============
rep('<path class="hot keepw" d="M 490 400 V 435" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot keepw" d="M 450 370 V 420" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<rect class="hot" x="472" y="435" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<rect class="hot" x="432" y="420" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<path class="hot keepw" d="M 490 490 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot keepw" d="M 450 475 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<circle cx="490" cy="400" r="7" fill="#ffffff"/>',
    '<circle cx="450" cy="370" r="7" fill="#ffffff"/>')
rep('<text class="hot-label" x="522" y="470" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">E1</tspan></text>',
    '<text class="hot-label" x="482" y="455" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="start">R<tspan class="sub">E1</tspan></text>')

# ============ 需求2：公共地轨 T 结节点圆左移（R_B 320→280、R_E1 490→450；R_C 640 不动）============
rep('<circle cx="320" cy="525" r="7" fill="#ffffff"/>',
    '<circle cx="280" cy="525" r="7" fill="#ffffff"/>')
rep('<circle cx="490" cy="525" r="7" fill="#ffffff"/>',
    '<circle cx="450" cy="525" r="7" fill="#ffffff"/>')

# ============ 需求2/3：fx-t-rbe 左移 40px（420→380）+ 上移 15px（体 280→265、下端接横线 370）============
rep('<line class="hot keepw" x1="420" y1="176" x2="420" y2="280" stroke="#ffffff" stroke-width="3.5"/>',
    '<line class="hot keepw" x1="380" y1="176" x2="380" y2="265" stroke="#ffffff" stroke-width="3.5"/>')
rep('<rect class="hot" x="402" y="280" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
    '<rect class="hot" x="362" y="265" width="36" height="55" fill="none" stroke="#ffffff" stroke-width="3.5"/>')
rep('<line class="hot keepw" x1="420" y1="335" x2="420" y2="400" stroke="#ffffff" stroke-width="3.5"/>',
    '<line class="hot keepw" x1="380" y1="320" x2="380" y2="370" stroke="#ffffff" stroke-width="3.5"/>')
rep('<text class="hot-label" x="452" y="315" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">r<tspan class="sub">be</tspan></text>',
    '<text class="hot-label" x="412" y="300" fill="#ffe66d" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">r<tspan class="sub">be</tspan></text>')

# ============ 需求2/3：fx-t-src 受控源左移 40px（560→520）+ 上移 15px（菱形 278→263、下端接横线 370）============
rep('<line class="hot" x1="560" y1="176" x2="560" y2="278" stroke="#ffffff" stroke-width="3.5"/>',
    '<line class="hot" x1="520" y1="176" x2="520" y2="263" stroke="#ffffff" stroke-width="3.5"/>')
rep('<path class="hot" d="M 560 278 L 584 308 L 560 338 L 536 308 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>',
    '<path class="hot" d="M 520 263 L 544 293 L 520 323 L 496 293 Z" fill="rgba(255,255,255,0.10)" stroke="#ffffff" stroke-width="3.5"/>')
rep('<line class="hot" x1="536" y1="308" x2="584" y2="308" stroke="#ffffff" stroke-width="3"/>',
    '<line class="hot" x1="496" y1="293" x2="544" y2="293" stroke="#ffffff" stroke-width="3"/>')
rep('<line class="hot" x1="560" y1="338" x2="560" y2="400" stroke="#ffffff" stroke-width="3.5"/>',
    '<line class="hot" x1="520" y1="323" x2="520" y2="370" stroke="#ffffff" stroke-width="3.5"/>')

# ============ 需求2：fx-t-ib / fx-t-ic 电流箭头左移 40px（y 不变）============
rep('<line x1="420" y1="196" x2="420" y2="226" stroke="#ff5252" stroke-width="5"/>',
    '<line x1="380" y1="196" x2="380" y2="226" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon points="420,240 412,225 428,225" fill="#ff5252" stroke="none"/>',
    '<polygon points="380,240 372,225 388,225" fill="#ff5252" stroke="none"/>')
rep('<text x="404" y="229" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">i<tspan class="sub">b</tspan></text>',
    '<text x="364" y="229" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">i<tspan class="sub">b</tspan></text>')
rep('<line x1="560" y1="196" x2="560" y2="226" stroke="#ff5252" stroke-width="5"/>',
    '<line x1="520" y1="196" x2="520" y2="226" stroke="#ff5252" stroke-width="5"/>')
rep('<polygon points="560,240 552,225 568,225" fill="#ff5252" stroke="none"/>',
    '<polygon points="520,240 512,225 528,225" fill="#ff5252" stroke="none"/>')
rep('<text x="544" y="229" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">βi<tspan class="sub">b</tspan></text>',
    '<text x="504" y="229" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="end">βi<tspan class="sub">b</tspan></text>')

# ============ 需求2/3：红点 B/C/E 左移 40px；E 点随横线上移到 370 ============
rep('<circle class="qdot" cx="420" cy="176" r="8" fill="#ff5252"/>',
    '<circle class="qdot" cx="380" cy="176" r="8" fill="#ff5252"/>')
rep('<circle class="qdot" cx="560" cy="176" r="8" fill="#ff5252"/>',
    '<circle class="qdot" cx="520" cy="176" r="8" fill="#ff5252"/>')
rep('<circle class="qdot" cx="420" cy="400" r="8" fill="#ff5252"/>',
    '<circle class="qdot" cx="380" cy="370" r="8" fill="#ff5252"/>')

if s == n0:
    sys.stderr.write('NO CHANGE\n'); sys.exit(1)
out = s.replace('\n', '\r\n') if crlf else s
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(out)
print('_g3_B.txt 第86轮几何补丁完成（40 处）')
