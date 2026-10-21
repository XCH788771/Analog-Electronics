#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cj-g3 构建脚本：以 _game-template.html 为蓝本，替换 A/B/ANNOS/C/D 五个区块 → cj-g3.html"""
import io, os, re, sys

SRC = os.path.dirname(os.path.abspath(__file__))          # 源片段目录（_src_g3/）
BASE = os.path.dirname(SRC)                                  # interactive/
TPL = os.path.join(BASE, '_game-template.html')
OUT = os.path.join(BASE, 'cj-g3.html')

def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()

def wr(p, s):
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)

def block(fn):
    # 源片段与本脚本同目录（_src_g3/），改图/改题只需编辑这些 .txt 后重跑
    return rd(os.path.join(os.path.dirname(os.path.abspath(__file__)), fn))

def replace_span(html, start_mark, end_mark, new_text, tag):
    """把 start_mark..end_mark（含）之间的内容整块替换为 new_text。
       替换文本若本身以注释横幅开头，必须自带闭合符（见制作规范踩坑①）。"""
    i = html.find(start_mark)
    if i < 0:
        raise SystemExit('[%s] 找不到起始标记: %r' % (tag, start_mark))
    j = html.find(end_mark, i)
    if j < 0:
        raise SystemExit('[%s] 找不到结束标记: %r' % (tag, end_mark))
    j += len(end_mark)
    return html[:i] + new_text + html[j:]

html = rd(TPL)

# ---------- 区 A ----------
html = replace_span(
    html,
    '        <!-- ▼▼▼ 替换区 A：左上角大标题 + 案例行（换成自己的案例名与题面） ▼▼▼ -->',
    '        <!-- ▲▲▲ 替换区 A 结束 ▲▲▲ -->',
    block('_g3_A.txt').rstrip('\n'), 'A')

# ---------- 区 A 补充：删除模板默认「已知」行 ----------
# 模板默认已知行位于「▲▲▲ 替换区 A 结束」标记之外（ cj-g1 蓝本沿用不改所以留在模板里），
# 本案例的已知行由 _g3_A.txt 自带 → 若不删掉模板默认行，两条同 y=210 叠印成乱码。
TPL_KNOWN = ('        <text x="70" y="210" fill="rgba(255,255,255,0.6)" font-size="26">'
             '已知：V<tspan class="sub">CC</tspan>、R<tspan class="sub">B1</tspan>、'
             'R<tspan class="sub">B2</tspan>、R<tspan class="sub">C</tspan>、'
             'R<tspan class="sub">E</tspan>、R<tspan class="sub">S</tspan>、'
             'R<tspan class="sub">L</tspan>、β，V<tspan class="sub">BE</tspan>=0.7V</text>\n')
if html.count(TPL_KNOWN) != 1:
    raise SystemExit('[A-已知行] 模板默认已知行未唯一命中（count=%d）' % html.count(TPL_KNOWN))
html = html.replace(TPL_KNOWN, '', 1)

# ---------- 区 B ----------
html = replace_span(
    html,
    '        <!-- ▼▼▼ 替换区 B：本案例电路 SVG（<g id="circuit-wrap"> 整块；含 fx-layer 特效/电量标注/整理/等效层；\n             元件/导线须为 g.interactive[data-id]，id 与区 C/D 一一对应；共射类案例可改造本示例） ▼▼▼ -->',
    '        <!-- ▲▲▲ 替换区 B 结束 ▲▲▲ -->',
    block('_g3_B.txt').rstrip('\n'), 'B')

# ---------- ANNOS ----------
i = html.find('    const ANNOS = {')
if i < 0:
    raise SystemExit('找不到 ANNOS 起点')
j = html.find('\n    };\n', i)
if j < 0:
    raise SystemExit('找不到 ANNOS 终点')
j += len('\n    };\n')
html = html[:i] + block('_g3_ANNOS.txt').rstrip('\n') + '\n' + html[j:]

# ---------- 区 C + 区 D（相邻，一次替换；C 自带 ▲▲▲ */ 闭合符，D 自带 ▲▲▲ */ 闭合符） ----------
c_start = '    /* ▼▼▼ 替换区 C：本案例关卡配置 GAME_CONFIG'
c_end = '    /* ▲▲▲ 替换区 D 结束 ▲▲▲ */'
html = replace_span(html, c_start, c_end, block('_g3_C.txt').rstrip('\n'), 'CD')

# ---------- 标题 ----------
html = html.replace(
    '<title>分压式偏置共射放大 · 闯关挑战（案例1）- 游戏交互</title>',
    '<title>双电源共射放大 · 闯关挑战（案例1）- 游戏交互</title>')

wr(OUT, html)
print('已生成 %s（%d 字节）' % (OUT, len(html.encode('utf-8'))))
