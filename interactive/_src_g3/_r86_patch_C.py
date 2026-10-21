# -*- coding: utf-8 -*-
"""cj-g3 第86轮 区C 补丁（需求4）：将白实线框 tk('□') 统一改为虚线显示框 { dbox: 1 }。
   dbox 渲染与 {box:1} 完全一致（黄虚线），但不可填、不被 countBoxes 计数 → 框数仍与 blanks 对齐，计分不变。
   涉及：简化框架 fill 的 I_EQ 位（subs/subsC 各1）+ 动态关 A_v/R_i 的 β 位（fw框架+fill 共11）。
"""
import io, sys, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_C.txt')
with io.open(P, encoding='utf-8', newline='') as f:
    raw = f.read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')

OLD = "tk('\u25a1')"   # tk('□')
NEW = '{ dbox: 1 }'
n = s.count(OLD)
if n != 13:
    sys.stderr.write('tk(□) 数量异常：%d（应为 13）\n' % n)
    sys.exit(1)
s = s.replace(OLD, NEW)

out = s.replace('\n', '\r\n') if crlf else s
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(out)
print('_g3_C.txt 第86轮补丁完成：tk(□) → { dbox: 1 } 共 %d 处' % n)
