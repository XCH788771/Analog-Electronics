# -*- coding: utf-8 -*-
"""cj-g3 第87轮 区C 补丁（需求2）：新增合法顺序 I_BQ → V_CEQ → I_CQ。
   用户指定四个正确答案：IEQ/ICQ/VCEQ/IBQ、IEQ/ICQ/IBQ/VCEQ、IBQ/ICQ/VCEQ、IBQ/VCEQ/ICQ。
   前三条已存在（seqs[0..4]），本条新增 seqs[5]；首步 I_BQ → 走 base 路线（subsBase）。
"""
import io, sys, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_g3_C.txt')
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

# 新增 seqs[5] = I_BQ → V_CEQ → I_CQ（接在原 base 顺序后）
rep("                            ['q-ibq', 'q-icq', 'q-vceq']",
    "                            ['q-ibq', 'q-icq', 'q-vceq'],\n                            ['q-ibq', 'q-vceq', 'q-icq']")
# routes 同步加一项（seqs[5] 首步 I_BQ → base）
rep("                        routes: ['eq', 'eq', 'cq', 'cq', 'base'],",
    "                        routes: ['eq', 'eq', 'cq', 'cq', 'base', 'base'],")
# 注释更新（⑤⑥ 均为 I_BQ 首步）
rep("                        //   ① ② 首步 I_EQ → 'eq'（subs）｜③ ④ 首步 I_CQ → 'cq'（subsC）｜⑤ 首步 I_BQ → 'base'（subsBase）",
    "                        //   ① ② 首步 I_EQ → 'eq'（subs）｜③ ④ 首步 I_CQ → 'cq'（subsC）｜⑤ ⑥ 首步 I_BQ → 'base'（subsBase）")

if s == n0:
    sys.stderr.write('NO CHANGE\n'); sys.exit(1)
out = s.replace('\n', '\r\n') if crlf else s
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(out)
print('_g3_C.txt 第87轮补丁完成：新增 seqs[5] IBQ→VCEQ→ICQ + routes[5]=base（3 处）')
