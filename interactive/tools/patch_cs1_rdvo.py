# -*- coding: utf-8 -*-
"""cs-g1 修订（2026-10-29 用户三项之 1、2）：
1) R_d 上移 15px（rect 74-127 → 59-112，标签/阻值随动）；v_o 水平导线上移 10px
   （漏极节点 y 178 → 168：wire-vo / node-drain / comp-vo / wire-d-stub 及 i_D 箭头随动）；
2) v_i 置零短接线两端接驳修正：输入导线起点 158 → 150（与底侧地线一致，均接端子圆心），
   使绿色短接桥（x=150，y 295-525）与上下水平导线成标准 T 形连接。
所有替换带唯一性校验，任一失配即中止不写盘。
"""
import io
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.normpath(os.path.join(D, '..', 'cs-g1.html'))

REPS = [
    # ---- 1) R_d 上移 15px ----
    ('<rect class="hot" x="472.5" y="74" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     '<rect class="hot" x="472.5" y="59" width="27" height="53" fill="none" stroke="#ffffff" stroke-width="3.5"/>',
     'R_d 矩形上移'),
    ('d="M 486 74 V 5"', 'd="M 486 59 V 5"', 'R_d 上引线'),
    ('<text class="hot-label" x="454" y="113"', '<text class="hot-label" x="454" y="98"', 'R_d 标签'),
    ('<text x="514" y="146"', '<text x="514" y="131"', '3.9kΩ 标注'),
    # ---- 1) 漏极节点 y 178 → 168（v_o 水平导线上移 10px）----
    ('d="M 486 127 V 178"', 'd="M 486 112 V 168"', 'R_d 下引线接新节点'),
    ('<circle cx="486" cy="178" r="7" fill="#ffffff" pointer-events="none"/>',
     '<circle cx="486" cy="168" r="7" fill="#ffffff" pointer-events="none"/>',
     '漏极节点圆'),
    ('d="M 486 178 H 692"', 'd="M 486 168 H 692"', 'v_o 水平导线'),
    ('<circle class="hot" cx="700" cy="178" r="8"', '<circle class="hot" cx="700" cy="168" r="8"', 'v_o 端子'),
    ('<text class="hot-label" x="726" y="186"', '<text class="hot-label" x="726" y="176"', 'v_o 标注'),
    ('d="M 486 178 V 236"', 'd="M 486 168 V 236"', '漏极竖接线'),
    ('<line x1="486" y1="196" x2="486" y2="216" stroke="#ff5252" stroke-width="5"/>',
     '<line x1="486" y1="186" x2="486" y2="206" stroke="#ff5252" stroke-width="5"/>',
     'i_D 杆'),
    ('<polygon points="486,230 478,215 494,215" fill="#ff5252" stroke="none"/>',
     '<polygon points="486,220 478,205 494,205" fill="#ff5252" stroke="none"/>',
     'i_D 箭头'),
    ('<text x="548" y="214"', '<text x="548" y="204"', 'i_D 标注'),
    # ---- 2) 输入导线起点接到端子圆心（与绿色短接桥、底侧地线对齐）----
    ('d="M 158 295 H 206"', 'd="M 150 295 H 206"', '输入导线起点'),
]


def main():
    raw = io.open(P, 'rb').read()
    s = raw.decode('utf-8').replace('\r\n', '\n')
    crlf = b'\r\n' in raw

    bad = []
    for old, new, tag in REPS:
        n = s.count(old)
        if n != 1:
            bad.append('%s：命中 %d 次（应为 1）' % (tag, n))
    if bad:
        print('中止，未写盘：')
        for b in bad:
            print('  - ' + b)
        return 1

    for old, new, tag in REPS:
        s = s.replace(old, new)
    out = s if not crlf else s.replace('\n', '\r\n')
    io.open(P, 'wb').write(out.encode('utf-8'))
    print('已写入（%d 处替换）：%s' % (len(REPS), P))
    return 0


if __name__ == '__main__':
    sys.exit(main())
