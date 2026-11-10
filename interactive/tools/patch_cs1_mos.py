# -*- coding: utf-8 -*-
"""cs-g1.html 场效应管符号几何微调（2026-10-27）

用户要求：
  ① D、S 极与衬底 B 极之间的距离减小 1/3，D、S、B 短竖线（三段沟道）相应变短
  ② 字母 B 右移：水平与 B 箭头同轴（垂直中心落在 y=265），垂直与 R_d 电阻同轴（x=486）
  ③ B 极箭头变大一倍（长 14→28、高 12→24）

几何口径（局部坐标系，circuit-wrap translate 前）：
  原：D 引线 y=221 / B 引线 y=265 / S 引线 y=309，间距 44；三段沟道段长 32、间隙 12
  新：D 引线 y=236 / B 引线 y=265 / S 引线 y=294，间距 29（44×2/3≈29.3，取 29）
      三段沟道段长 18、间隙 11（保持原有线间呼吸感）
      D 段 227-245、B 段 256-274、S 段 285-303
      栅极条随沟道整体缩短：235-295 → 246-284
      箭头：418,265 / 446,253 / 446,277（尖端仍指沟道，底边右移一倍）
      衬底引线起点随箭头底边：M 446 265 H 458 V 294；圆点 (458,294)
      B 文字：x 445→486、y 248→278（37px 黑体视觉中心上移约 13）
      连带接线：wire-d-stub 178→236、wire-src-a 294→385

用法：python tools/patch_cs1_mos.py [--also-backup]
  加 --also-backup 时同步改写 .workbuddy/archive/bak-csg1g3-swap-20261026/cs-g3.html
  （该备份是 cs-g1.html 的内容源，swap_csg1g3.py 会从它重建，故须同步）
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # 网站/interactive
G1 = os.path.join(ROOT, 'cs-g1.html')
BAK = os.path.join(os.path.dirname(os.path.dirname(ROOT)),
                   '.workbuddy', 'archive', 'bak-csg1g3-swap-20261026', 'cs-g3.html')

PATCHES = [
    # ① 栅极条（随沟道整体缩短，保持与沟道同轴居中于 265）
    ('            <line class="hot" x1="400" y1="235" x2="400" y2="295" stroke="#ffffff" stroke-width="5"/>',
     '            <line class="hot" x1="400" y1="246" x2="400" y2="284" stroke="#ffffff" stroke-width="5"/>'),

    # ② 三段沟道：中心 236 / 265 / 294，段长 18
    ('            <line class="hot" x1="414" y1="205" x2="414" y2="237" stroke="#ffffff" stroke-width="5"/>\n'
     '            <line class="hot" x1="414" y1="249" x2="414" y2="281" stroke="#ffffff" stroke-width="5"/>\n'
     '            <line class="hot" x1="414" y1="293" x2="414" y2="325" stroke="#ffffff" stroke-width="5"/>',
     '            <line class="hot" x1="414" y1="227" x2="414" y2="245" stroke="#ffffff" stroke-width="5"/>\n'
     '            <line class="hot" x1="414" y1="256" x2="414" y2="274" stroke="#ffffff" stroke-width="5"/>\n'
     '            <line class="hot" x1="414" y1="285" x2="414" y2="303" stroke="#ffffff" stroke-width="5"/>'),

    # ③ 漏极 / 源极水平引线
    ('            <path class="hot" d="M 414 221 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 414 236 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
    ('            <path class="hot" d="M 414 309 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 414 294 H 486" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # ④ 衬底引线 + 箭头（放大一倍）+ 连接圆点
    ('            <path class="hot" d="M 432 265 H 458 V 309" fill="none" stroke="#ffffff" stroke-width="3"/>\n'
     '            <polygon class="hot-fill" points="418,265 432,259 432,271" fill="#ffffff" stroke="none"/>\n'
     '            <circle cx="458" cy="309" r="7" fill="#ffffff" pointer-events="none"/>',
     '            <path class="hot" d="M 446 265 H 458 V 294" fill="none" stroke="#ffffff" stroke-width="3"/>\n'
     '            <polygon class="hot-fill" points="418,265 446,253 446,277" fill="#ffffff" stroke="none"/>\n'
     '            <circle cx="458" cy="294" r="7" fill="#ffffff" pointer-events="none"/>'),

    # ⑤ 字母 B：右移至 R_d 同轴（x=486），垂直中心对齐箭头水平线（y=265）
    ('            <text class="hot-label" x="445" y="248" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">B</text>',
     '            <text class="hot-label" x="486" y="278" fill="#ffe66d" font-size="37" font-weight="bold" text-anchor="middle">B</text>'),

    # ⑥ 漏极竖接线：178 → 236（跟随漏极引线）
    ('            <path class="hot" d="M 486 178 V 221" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 486 178 V 236" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),

    # ⑦ 源极竖接线：294 → 385（跟随源极引线）
    ('            <path class="hot" d="M 486 309 V 385" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '            <path class="hot" d="M 486 294 V 385" fill="none" stroke="#ffffff" stroke-width="3.5"/>'),
]


def apply(path):
    s = io.open(path, encoding='utf-8', newline='').read()
    for i, (old, new) in enumerate(PATCHES, 1):
        n = s.count(old)
        if n != 1:
            print('!! patch #%d 命中 %d 次（应为 1），中止，未写盘：%s' % (i, n, path))
            return False
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    print('OK 已写入：%s（%d 处）' % (path, len(PATCHES)))
    return True


if __name__ == '__main__':
    ok = apply(G1)
    if ok and '--also-backup' in sys.argv:
        if os.path.exists(BAK):
            ok = apply(BAK)
        else:
            print('!! 备份源不存在：%s' % BAK)
            ok = False
    sys.exit(0 if ok else 1)
