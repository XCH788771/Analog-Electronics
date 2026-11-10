# -*- coding: utf-8 -*-
"""cs-g1 第 2 关（静态工作点）：自动移除 v_o 标注与输出导线（直流通路视角）"""
import io, shutil, sys

SRC = 'cs-g1.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
reps = []

def rep(old, new, tag):
    global s
    c = s.count(old)
    assert c == 1, '[%s] count=%d' % (tag, c)
    s = s.replace(old, new, 1)
    reps.append(tag)

# ① 新增函数（放在 fadeGroup 之后、showFx 之前）
rep("""    function showFx(id, on) {""",
    """    // 第 2 关（静态工作点）＝直流通路视角：v_o 属交流量，其标注与输出导线随关卡自动移除
    //   （resetCircuit 统一清 opacity/hit-off，进入第 3 关交流等效时自动恢复）
    function applyQPointView() {
        fadeGroup('comp-vo', true);
        fadeGroup('wire-vo', true);
    }
    function showFx(id, on) {""",
    'fn-apply')

# ② 进入第 2 关时调用（completeLevel）
rep("""        if (cur().cfg.kind === 'mix') arrangeMixSubs(S.level - 1);   // 子步顺序跟随第 2 关点选顺序""",
    """        if (cur().cfg.kind === 'mix') arrangeMixSubs(S.level - 1);   // 子步顺序跟随第 2 关点选顺序
        // 静态工作点关：保留直流通路视图，并移除 v_o 标注与输出导线
        if (cur().cfg.kind === 'mix' && cur().cfg.stageUnits === 0) applyQPointView();""",
    'call-complete')

# ③ 调试钩子同步（?lvl=2 预览一致）
rep("""        render();
        // 调试预览不播音：直接高亮对应级""",
    """        if (n === 2) applyQPointView();
        render();
        // 调试预览不播音：直接高亮对应级""",
    'call-debug')

if '--dry' in sys.argv:
    print('[DRY] %d reps:' % len(reps), ','.join(reps))
    sys.exit(0)

shutil.copyfile(SRC, '/tmp/cs-g1.before-voq.html')
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('[OK] %d reps:' % len(reps), ','.join(reps))
