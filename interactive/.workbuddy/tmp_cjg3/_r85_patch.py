# -*- coding: utf-8 -*-
"""cj-g3 第85轮补丁：
1) R_C 下移使其居于集电极节点(y=176)与上端水平导线(y=33)正中(body 77..132)；q-icq 电流标注同步下移17px。
2/3) 工程近似(简化)框架的 I_CQ≈I_EQ → I_CQ≈□（fw 步用可填方框{box:1}+qid，fill 步用显示□）；全路线(eq/cq)一致。
4) 等效电路 Vi 端口：− 极下移靠近地线、Vi 文字移到 +/− 正中、− 极下方导线接公共地轨并加与上端圆圈(150,176)同轴节点圆。
5) 动态性能指标(A_v/R_i)中的 β → □（显示方框，不改分）。
"""
import io, sys

B = '_src_g3/_g3_B.txt'
C = '_src_g3/_g3_C.txt'

def load(p):
    return io.open(p, encoding='utf-8', newline='').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

def rep(s, label, old, new, n, all_=False):
    if all_:
        c = s.count(old)
        if c < 1:
            raise SystemExit('[%s] 期望≥1处, 实得 %d: %r' % (label, c, old[:60]))
        return s.replace(old, new)
    c = s.count(old)
    if c != n:
        raise SystemExit('[%s] 期望 %d 处唯一, 实得 %d: %r' % (label, n, c, old[:60]))
    return s.replace(old, new, 1) if n == 1 else s.replace(old, new)

# ===================== _g3_B.txt =====================
b = load(B)

# --- Req1: R_C 下移 17px (body 60→77..132)；上端导线 33→77；下端导线 132→176 ---
b = rep(b, 'B wire-rc-top', 'M 486 33 V 60', 'M 486 33 V 77', 1)
b = rep(b, 'B comp-rc rect', 'x="468" y="60" width="36" height="55"', 'x="468" y="77" width="36" height="55"', 1)
b = rep(b, 'B comp-rc label', 'x="454" y="96" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">C</tspan></text>',
                   'x="454" y="113" fill="#ffffff" font-size="37" font-weight="bold" text-anchor="end">R<tspan class="sub">C</tspan></text>', 1)
b = rep(b, 'B wire-rc-a', 'M 486 115 V 176', 'M 486 132 V 176', 1)
# q-icq 电流标注同步下移 17px
b = rep(b, 'B q-icq rect', 'x="522" y="44" width="90" height="90"', 'x="522" y="61" width="90" height="90"', 1)
b = rep(b, 'B q-icq arrow', 'x1="530" y1="58" x2="530" y2="110" stroke="#ff5252" stroke-width="5"',
                   'x1="530" y1="75" x2="530" y2="127" stroke="#ff5252" stroke-width="5"', 1)
b = rep(b, 'B q-icq poly', 'points="530,124 522,109 538,109"', 'points="530,141 522,126 538,126"', 1)
b = rep(b, 'B q-icq text', 'x="546" y="101" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">I<tspan class="sub">CQ</tspan></text>',
                   'x="546" y="118" fill="#ff5252" font-size="28" font-weight="bold" font-style="italic" text-anchor="start">I<tspan class="sub">CQ</tspan></text>', 1)

# --- Req4: 等效电路 Vi 端口 ---
# − 极下移(380→440) 并补导线+同轴圆圈
b = rep(b, 'B vi dash', '<text x="150" y="380" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>',
  '<text x="150" y="440" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">－</text>\n'
  '                <!-- 第85轮：vi 负端下移靠近地线；下方导线接公共地轨，并加与上端圆圈(150,176)垂直同轴的节点圆 -->\n'
  '                <path d="M 150 440 V 525" fill="none" stroke="#ffffff" stroke-width="3.5"/>\n'
  '                <circle cx="150" cy="480" r="8" fill="#0a3d20" stroke="#ffffff" stroke-width="3"/>\n'
  '                <circle cx="150" cy="525" r="7" fill="#ffffff"/>', 1)
# Vi 文字下移(315→345, 居中于 +250 与 −440)
b = rep(b, 'B vi text', '<text x="150" y="315" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>',
                   '<text x="150" y="345" fill="#ffe66d" font-size="37" font-weight="bold" font-style="italic" text-anchor="middle">V<tspan class="sub">i</tspan></text>', 1)

save(B, b)
print('B patched OK')

# ===================== _g3_C.txt =====================
c = load(C)

# --- Req3: 简化框架 I_CQ≈I_EQ → I_CQ≈□ ---
# subsC 简化 fw：name + qid（q-icq → q-ieq，方框代表 I_EQ）
c = rep(c, 'C subsC simp fw name+qid',
  "name: 'I<tspan class=\"sub\">CQ</tspan>≈I<tspan class=\"sub\">EQ</tspan> 简化框架', qpts: 6, pen: 2,\n                                qid: 'q-icq',",
  "name: 'I<tspan class=\"sub\">CQ</tspan>≈□ 简化框架', qpts: 6, pen: 2,\n                                qid: 'q-ieq',", 1)
# subs 简化 fw name（149）
c = rep(c, 'C subs simp fw name',
  "name: 'I<tspan class=\"sub\">CQ</tspan>≈I<tspan class=\"sub\">EQ</tspan> 简化框架', qpts: 6, pen: 2,",
  "name: 'I<tspan class=\"sub\">CQ</tspan>≈□ 简化框架', qpts: 6, pen: 2,", 1)
# 简化 fill name（164, 281）
c = rep(c, 'C simp fill name',
  "name: 'I<tspan class=\"sub\">CQ</tspan>≈I<tspan class=\"sub\">EQ</tspan> 简化表达式',",
  "name: 'I<tspan class=\"sub\">CQ</tspan>≈□ 简化表达式',", 2, all_=True)
# 简化 fwQ（153, 271）
c = rep(c, 'C simp fwQ',
  "fwQ: '工程近似估算：I<tspan class=\"sub\">CQ</tspan>≈I<tspan class=\"sub\">EQ</tspan> 的简化框架：',",
  "fwQ: '工程近似估算：I<tspan class=\"sub\">CQ</tspan>≈□ 的简化框架：',", 2, all_=True)
# 简化 fill fullExpr（166, 283）→ 显示□
c = rep(c, 'C simp fill fullExpr',
  "fullExpr: [[tk('I', 'CQ'), tk('≈'), tk('I', 'EQ'), tk('≈'),",
  "fullExpr: [[tk('I', 'CQ'), tk('≈'), tk('□'), tk('≈'),", 2, all_=True)
# 简化 fw tokens（158,159,160,275,276,277）→ 可填方框{box:1}（fill 已在上式改为□，此处仅剩 fw）
c = rep(c, 'C simp fw tokens',
  "tk('I', 'CQ'), tk('≈'), tk('I', 'EQ'), tk('≈'),",
  "tk('I', 'CQ'), tk('≈'), { box: 1 }, tk('≈'),", 6, all_=True)

# --- Req5: 动态性能指标 β → □（仅动态关，不改静态关；不改分） ---
c = rep(c, 'C beta lead -', "tk('−'), tk('β'), tk('·'),", "tk('−'), tk('□'), tk('·'),", 3, all_=True)   # 550,551,557
c = rep(c, 'C beta lead =', "tk('='), tk('β'), tk('·'),", "tk('='), tk('□'), tk('·'),", 1)               # 552
c = rep(c, 'C beta 1+beta', "tk('('), tk('1'), tk('+'), tk('β'), tk(')')", "tk('('), tk('1'), tk('+'), tk('□'), tk(')')", 7, all_=True)  # 550,551,552,557,580,581,588

save(C, c)
print('C patched OK')
