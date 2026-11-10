# -*- coding: utf-8 -*-
"""cs-g1：TQUIZ 前插一问「v_gs 极性选择」（G/S 红点闪烁，两个选项随机顺序）
- 选项：上＋下－（正确，N 沟道 v_gs>0）/ 上－下＋
- 选项渲染为竖排极性柱（＋ / v_gs / －），直观对应图上标注形态
- 作答后 reveal fx-t-vgs（v_gs 标注出现）
"""
import io, sys

P = "cs-g1.html"
s = io.open(P, encoding="utf-8", newline="").read()
reps = []

# ① TQUIZ 头部插入极性问
old1 = """    const TQUIZ = [
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['短路', '开路', '受控源'], ok: '开路',
          q: 'G、S 之间相当于什么？', reveal: 'fx-t-vgs' },"""
new1 = """    const TQUIZ = [
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['上＋下－', '上－下＋'], ok: '上＋下－',
          q: 'v_gs 的标注极性应怎样表示？', reveal: 'fx-t-vgs' },
        { dots: ['fx-dot-g', 'fx-dot-s'], opts: ['短路', '开路', '受控源'], ok: '开路',
          q: 'G、S 之间相当于什么？', reveal: 'fx-t-vgs' },"""
reps.append((old1, new1))

# ② 选项渲染：极性选项画成竖排极性柱
old2 = """    function tquizOptHtml(op) {
        const c = op.charAt(0);
        if (c !== '↑' && c !== '↓') return null;
        return c + 'g' + TQ_SUBD + '·v' + TQ_SUBD2;
    }"""
new2 = """    function tquizOptHtml(op) {
        const c = op.charAt(0);
        if (c === '↑' || c === '↓') return c + 'g' + TQ_SUBD + '·v' + TQ_SUBD2;
        if (op === '上＋下－' || op === '上－下＋') {
            // v_gs 极性选项：竖排极性柱（上端符号 / v_gs / 下端符号），与图上标注形态一致
            return '<span style="display:inline-flex;flex-direction:column;align-items:center;line-height:1.1;padding:2px 0">'
                 + '<span style="font-size:17px">' + op.charAt(1) + ' 上</span>'
                 + '<span style="font-style:italic;font-size:15px;margin:1px 0">v' + TQ_SUBD2 + '</span>'
                 + '<span style="font-size:17px">' + op.charAt(3) + ' 下</span></span>';
        }
        return null;
    }"""
reps.append((old2, new2))

# ③ 注释：四问 → 五问
old3 = "                        // 等效四问分值池（画图 3 目标 ×6=18 + 池 4 = 22）"
new3 = "                        // 等效五问分值池（画图 3 目标 ×6=18 + 池 4 = 22；每题答错扣 1，正误均推进）"
reps.append((old3, new3))

ok = True
for i, (o, n) in enumerate(reps, 1):
    c = s.count(o)
    if c != 1:
        print("rep%d FAIL count=%d" % (i, c)); ok = False
    else:
        print("rep%d OK" % i)
if not ok:
    sys.exit(1)
for o, n in reps:
    s = s.replace(o, n)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("已写盘")
