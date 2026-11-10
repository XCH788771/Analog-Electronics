# ⚠️ 已废弃（2026-10-27）：cs-g1 已按用户原图重绘为单电源分压式偏置共源·案例1，与 cs-g3 不再互为内容副本；本脚本（双电源版互换）不得再运行。
# -*- coding: utf-8 -*-
"""cs-g1.html / cs-g3.html 内容错位修正（幂等，从备份源重建）

用户裁决（2026-10-26）：
  案例1 电路 = 双电源分压偏置共源（原误放在 cs-g3.html）→ 应落在 cs-g1.html
  案例3 电路 = 单电源分压偏置共源完整版（含 RG / RS∥CS / RL，原误放在 cs-g1.html）→ 应落在 cs-g3.html
源固定取备份目录，重复执行结果一致；同步改 title / 案例行 / 头部注释的案例编号。
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../网站
D = os.path.join(ROOT, 'interactive')
BAK = os.path.join(ROOT, '..', '.workbuddy', 'archive', 'bak-csg1g3-swap-20261026')
P1 = os.path.join(D, 'cs-g1.html')
P3 = os.path.join(D, 'cs-g3.html')
SRC1 = os.path.join(BAK, 'cs-g3.html')   # 案例1 电路（双电源）
SRC3 = os.path.join(BAK, 'cs-g1.html')   # 案例3 电路（单电源完整版）


def rd(p):
    with io.open(p, 'r', encoding='utf-8', newline='') as f:
        return f.read()


def wr(p, s):
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def rep(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        print('!! rep 命中 %d 次（应为 1）：%s' % (n, tag))
        sys.exit(1)
    return s.replace(old, new)


# ---- cs-g1.html ← 案例1（双电源分压偏置共源）----
n1 = rd(SRC1)
n1 = rep(n1, '<title>双电源分压偏置共源放大 · 闯关挑战（案例3）- 游戏交互</title>',
         '<title>双电源分压偏置共源放大 · 闯关挑战（案例1）- 游戏交互</title>', 'g1-title')
n1 = rep(n1, '>案例3：双电源分压偏置共源 · 求动态性能指标<',
         '>案例1：双电源分压偏置共源 · 求动态性能指标<', 'g1-case-line')

# ---- cs-g3.html ← 案例3（单电源分压偏置共源完整版）----
n3 = rd(SRC3)
n3 = rep(n3, '<title>分压式偏置共源放大 · 闯关挑战（案例1）- 游戏交互</title>',
         '<title>分压式偏置共源放大 · 闯关挑战（案例3）- 游戏交互</title>', 'g3-title')
n3 = rep(n3, '>案例1：分压式偏置共源 · 求动态性能指标<',
         '>案例3：分压式偏置共源 · 求动态性能指标<', 'g3-case-line')
n3 = rep(n3, 'cs-g1 共源放大（分压式偏置 · 案例1，2026-10 制稿）',
         'cs-g3 共源放大（分压式偏置 · 案例3，2026-10 制稿）', 'g3-head-comment')

wr(P1, n1)
wr(P3, n3)
print('写入完成：cs-g1.html %d 字符 / cs-g3.html %d 字符' % (len(n1), len(n3)))
