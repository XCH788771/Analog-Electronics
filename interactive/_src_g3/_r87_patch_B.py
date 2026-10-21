# -*- coding: utf-8 -*-
"""cj-g3 第87轮 区B 补丁：
   需求1：q-ieq 的 I_EQ 箭头加长一半（轴 34→51px，+17px，向上延伸，箭头尖端不动）
   需求2：eq-rb / eq-re1 默认加 hit-off（隐藏等效层的可作答件断命中，防压住默认态电量标注）
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

# ============ 需求1：I_EQ 箭头加长一半（轴上端 372→355，+17px；尖端 420 不动）============
rep('<line class="hot" x1="520" y1="372" x2="520" y2="406" stroke="#ff5252" stroke-width="5"/>',
    '<line class="hot" x1="520" y1="355" x2="520" y2="406" stroke="#ff5252" stroke-width="5"/>')
rep('<rect class="hot" x="508" y="368" width="72" height="58" fill="none" stroke="none"/>',
    '<rect class="hot" x="508" y="351" width="72" height="75" fill="none" stroke="none"/>')

# ============ 需求2：eq-rb / eq-re1 默认加 hit-off（隐藏态断子孙命中）============
rep('<g id="eq-rb" class="interactive" data-id="comp-rb">',
    '<g id="eq-rb" class="interactive hit-off" data-id="comp-rb">')
rep('<g id="eq-re1" class="interactive" data-id="comp-re1">',
    '<g id="eq-re1" class="interactive hit-off" data-id="comp-re1">')

if s == n0:
    sys.stderr.write('NO CHANGE\n'); sys.exit(1)
out = s.replace('\n', '\r\n') if crlf else s
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(out)
print('_g3_B.txt 第87轮补丁完成（需求1 箭头 +17px、需求2 eq-rb/eq-re1 hit-off，共 4 处）')
