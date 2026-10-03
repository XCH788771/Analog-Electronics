#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互电路页 · SVG 几何布局自检工具（通用模板配套 · v2）

用法:
    python tools/svg-layout-check.py <html路径> [--quiet]

检查项:
  ① 结构  : data-id 唯一性 / STAGE_UNITS 覆盖 / ANNOS 覆盖
  ② 元件互压
  ③ 标签冲突: ③a 标签压元件(含多边形精判, 仅"完全内嵌"豁免, 如运放三角内 A₁)
              ③b 标签互压
              ③c 标签与元件净间隙 < LABEL_GAP  → 警告(下标下沉后易贴边)
  ④ 导线端点悬空
  ⑤ 导线非端点交叉
  ⑥ 越出右侧面板 / 顶部 / 底部安全线
  ⑦ 元件间距均匀性 : 最近邻净间隙 < MIN_PITCH → 错误(拥挤) ; > LOOSE_PITCH → 提示(松散)
  ⑧ 两端导线均衡   : 两终端导线长度比 > LEAD_RATIO → 警告(一端贴死一端拖长)
  ⑨ 下标尺寸一致性 : 页面 tspan.sub 的 font-size 百分比须与 SUB_SCALE 一致

退出码: 0=无硬错误(警告不影响), 1=存在硬错误

设计标准（与 制作规范.md 第五节一致）:
  · 元件标签墨迹(含 100% 下标下沉 -20%)与元件图形净间隙 ≥ LABEL_GAP(8px)
  · 横向电阻标签基线 y = 电阻上沿 − 22（37px 字号时墨迹底距上沿约 8px）
  · 元件最近邻净间隙 ≥ MIN_PITCH(20px)，同类元件间距差异 ≤ 1.5 倍
  · 元件两端导线长度尽量接近（比 ≤ 1.5:1）
"""
import io
import re
import sys
import html as _html

NUM = r'-?\d+(?:\.\d+)?'
SNAP = 7.0            # 端点吸附容差(inner 单位)
PAD = 2.0             # 元件/标签重叠判定的内缩容差
PANEL_GAP = 5.0       # 元素右缘与面板左缘的最小间距
TOP_LIMIT = 20.0      # inner 顶部安全线
BOTTOM_LIMIT = 790.0  # inner 底部安全线(底部品牌字样/提示 之上)
SUB_SCALE = 1.0       # tspan.sub 下标相对父字号比例（须与页面 CSS font-size 百分比一致）
LABEL_GAP = 8.0       # 标签墨迹与元件的最小净间隙
NEAR_GAP = 6.0        # 净间隙低于此值 → ③c 警告
MIN_PITCH = 15.0      # 元件最近邻净间隙下限（低于 → 拥挤错误）
LOOSE_PITCH = 300.0   # 元件最近邻净间隙上限（高于 → 松散提示）
LEAD_RATIO = 1.5      # 元件两端导线长度比上限
FOOTER_KEYS = ('提示：', '交互式学习平台', '《模拟电子技术》')


def _f(s, d=0.0):
    try:
        return float(s)
    except Exception:
        return d


def _clean(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = _html.unescape(t)
    return re.sub(r'\s+', '', t)


def _tw(s, size):
    """文本宽度估算: 中文/全角 1.0em; 数字与拉丁字母 0.58em; 其余 0.42em"""
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o > 0x2E80:
            w += 1.0
        elif ch.isdigit() or ('a' <= ch.lower() <= 'z'):
            w += 0.58
        else:
            w += 0.42
    return w * size


def measure_text(inner, size):
    """测量 <text> 内容的墨迹宽度(含 tspan sub 缩小)"""
    total = 0.0
    pos = 0
    for m in re.finditer(r'<tspan([^>]*)>(.*?)</tspan>', inner, re.S):
        total += _tw(_clean(inner[pos:m.start()]), size)
        sub = ('sub' in m.group(1))
        total += _tw(_clean(m.group(2)), size * (SUB_SCALE if sub else 1.0))
        pos = m.end()
    total += _tw(_clean(inner[pos:]), size)
    return total


def path_points(d):
    pts = []
    cur = None
    for cmd, args in re.findall(r'([MmLlHhVv])\s*([-\d.,\s]*)', d):
        nums = [float(x) for x in re.findall(NUM, args)]
        if not nums:
            continue
        if cmd in 'Mm':
            if len(nums) >= 2:
                cur = (nums[0], nums[1])
                pts.append(cur)
        elif cmd in 'Hh':
            for v in nums:
                cur = (v, cur[1])
                pts.append(cur)
        elif cmd in 'Vv':
            for v in nums:
                cur = (cur[0], v)
                pts.append(cur)
        elif cmd in 'Ll':
            if len(nums) >= 2:
                cur = (nums[0], nums[1])
                pts.append(cur)
    return pts


class Item(object):
    def __init__(self, kind, owner, name, bbox, extra=None):
        self.kind = kind          # comp / label / wire
        self.owner = owner        # data-id 或 'misc'
        self.name = name
        self.bbox = bbox          # (x0,y0,x1,y1)
        self.extra = extra or {}  # wire: segs=[(x1,y1,x2,y2)] ; polygon: pts=[(x,y)]

    def __repr__(self):
        b = self.bbox
        return '%s[%s] (%.0f,%.0f)-(%.0f,%.0f)' % (self.kind, self.owner, b[0], b[1], b[2], b[3])


def parse(html_text):
    # 剔除隐藏特效层（fx-layer：opacity="0"，不可见内容不参与布局检查）
    fx = html_text.find('<g id="fx-layer"')
    if fx >= 0:
        depth = 0
        for m2 in re.finditer(r'<g\b|</g>', html_text[fx:]):
            if m2.group(0) == '<g':
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = fx + m2.end()
                    html_text = html_text[:fx] + html_text[end:]
                    break
    """解析电路区段, 返回 (items, panel_left_inner)。支持有/无 circuit-wrap 两种写法"""
    m = re.search(r'<g id="circuit-wrap"[^>]*?transform="translate\(\s*(%s)[,\s]+(%s)\s*\)\s*scale\(\s*(%s)\s*\)"' % (NUM, NUM, NUM), html_text)
    if m:
        tx, ty, sc = _f(m.group(1)), _f(m.group(2)), _f(m.group(3))
        start = m.end()
        # 找 wrap 结束位置(括号配平)
        depth = 1
        i = start
        tok = re.compile(r'<\s*(/?)\s*(g)\b[^>]*>', re.I)
        while depth > 0:
            t = tok.search(html_text, i)
            if not t:
                break
            depth += -1 if t.group(1) else 1
            i = t.end()
        body = html_text[start:i]
    else:
        # 旧写法(lin-l1 / lin-t4 / 模板)：整幅 svg，无缩放
        tx = ty = 0.0
        sc = 1.0
        sm = re.search(r'<svg class="circuit"[^>]*>', html_text)
        if not sm:
            raise SystemExit('未找到 <svg class="circuit"> 或 circuit-wrap')
        start = sm.end()
        em = html_text.rindex('</svg>')
        body = html_text[start:em]

    # 面板左缘(svg 坐标) → inner（属性顺序无关，取右侧面板矩形）
    panel_svg_x = 980.0
    for mm in re.finditer(r'<rect\b[^>]*>', html_text):
        at = dict((k.lower(), v) for k, v in re.findall(r'([\w:-]+)\s*=\s*"([^"]*)"', mm.group(0)))
        if _f(at.get('x'), -1) >= 900 and _f(at.get('width'), 0) >= 380:
            panel_svg_x = _f(at.get('x'))
            if 'panel' in (at.get('fill', '') or ''):
                break
    panel_left_inner = (panel_svg_x - tx) / sc

    items = []
    stack = []
    pos = 0
    tag = re.compile(r'<\s*(/?)\s*([a-zA-Z]+)((?:"[^"]*"|[^>"])*?)(/?)>', re.S)
    tclose = re.compile(r'</text\s*>', re.I)
    while True:
        m2 = tag.search(body, pos)
        if not m2:
            break
        closing, name, attrs, selfc = m2.group(1), m2.group(2).lower(), m2.group(3), m2.group(4)
        name = name.lower()
        if name not in ('g', 'rect', 'circle', 'polygon', 'line', 'path', 'text'):
            pos = m2.end()
            continue
        if closing:
            if name == 'g' and stack:
                stack.pop()
            pos = m2.end()
            continue

        a = dict((k.lower(), v) for k, v in re.findall(r'([\w:-]+)\s*=\s*"([^"]*)"', attrs))
        owner = 'misc'
        disp = ''
        for fr in reversed(stack):
            if fr.get('data-id'):
                owner = fr['data-id']
                disp = fr.get('data-name', '')
                break

        if name == 'g':
            stack.append(a)
            if selfc:
                stack.pop()
            pos = m2.end()
            continue

        if name == 'rect' and a.get('fill') == 'none':
            if a.get('stroke') == 'none':
                pass  # 纯命中区（不可见热区）：无视觉冲突，不参与检查
            else:
                x, y = _f(a.get('x')), _f(a.get('y'))
                w, h = _f(a.get('width')), _f(a.get('height'))
                if w <= 300 and h <= 300:      # 排除装饰/演示/热区大框
                    items.append(Item('comp', owner, disp, (x, y, x + w, y + h)))
        elif name == 'rect':
            pass  # 装饰矩形忽略
        elif name == 'circle':
            if a.get('fill') == 'transparent':
                pass  # 热区
            else:
                cx, cy, r = _f(a.get('cx')), _f(a.get('cy')), _f(a.get('r'))
                if r <= 150:
                    items.append(Item('comp', owner, disp, (cx - r, cy - r, cx + r, cy + r), {'circle': r}))
        elif name == 'polygon':
            pts = [float(v) for v in re.findall(NUM, a.get('points', ''))]
            xs = pts[0::2]
            ys = pts[1::2]
            if xs and ys:
                poly = list(zip(xs, ys))
                items.append(Item('comp', owner, disp, (min(xs), min(ys), max(xs), max(ys)), {'poly': poly}))
        elif name == 'line':
            x1, y1 = _f(a.get('x1')), _f(a.get('y1'))
            x2, y2 = _f(a.get('x2')), _f(a.get('y2'))
            items.append(Item('wire', owner, disp, (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)),
                              {'segs': [(x1, y1, x2, y2)]}))
        elif name == 'path':
            d = a.get('d', '')
            pts = path_points(d)
            if pts:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                segs = [(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1]) for k in range(len(pts) - 1)]
                items.append(Item('wire', owner, disp, (min(xs), min(ys), max(xs), max(ys)), {'segs': segs}))
        elif name == 'text':
            tc = tclose.search(body, m2.end())
            inner = body[m2.end():tc.start()] if tc else ''
            txt = _clean(inner)
            if any(k in txt for k in FOOTER_KEYS):
                pos = tc.end() if tc else m2.end()
                continue
            size = _f(a.get('font-size'), 32.0)
            x, y = _f(a.get('x')), _f(a.get('y'))
            anchor = a.get('text-anchor', 'start')
            w = measure_text(inner, size)
            if anchor == 'middle':
                x0 = x - w / 2.0
            elif anchor == 'end':
                x0 = x - w
            else:
                x0 = x
            items.append(Item('label', owner, txt or disp,
                              (x0, y - size * 0.80, x0 + w, y + size * 0.26)))
            pos = tc.end() if tc else m2.end()
            continue

        pos = m2.end()

    # 剔除右侧面板内的元素（lin-l1/lin-t4 面板与电路同 svg）与顶部表头带(分隔线/校徽 y≤130)
    items = [it for it in items if it.bbox[0] < panel_left_inner - 1 and it.bbox[3] > 130]
    return items, panel_left_inner


def seg_dist(p, s):
    (x, y), (x1, y1, x2, y2) = p, s
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    if L2 == 0:
        return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
    px, py = x1 + t * dx, y1 + t * dy
    return ((x - px) ** 2 + (y - py) ** 2) ** 0.5


def seg_cross(a, b):
    """两线段是否真交叉(不含共享端点/共线重叠)"""
    x1, y1, x2, y2 = a
    x3, y3, x4, y4 = b
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-9:
        return False
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    eps = 1e-6
    return (eps < t < 1 - eps) and (eps < u < 1 - eps)


def overlap(a, b, pad=PAD):
    return (min(a[2], b[2]) - max(a[0], b[0]) > pad) and (min(a[3], b[3]) - max(a[1], b[1]) > pad)


def gap(a, b):
    """两盒净间隙: 分离→正(欧氏距离); 相交→负(交叠长度)"""
    dx = max(a[0] - b[2], b[0] - a[2])
    dy = max(a[1] - b[3], b[1] - a[3])
    if dx > 0 and dy > 0:
        return (dx * dx + dy * dy) ** 0.5
    if dx > 0:
        return dx
    if dy > 0:
        return dy
    return -min(abs(dx), abs(dy))


def _in_poly(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi):
            c = not c
        j = i
    return c


def rect_poly_overlap(r, poly):
    """矩形(bbox)与多边形真实相交判定"""
    corners = [(r[0], r[1]), (r[2], r[1]), (r[0], r[3]), (r[2], r[3])]
    if any(_in_poly(p, poly) for p in corners):
        return True
    if any(r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3] for p in poly):
        return True
    edges = [((r[0], r[1]), (r[2], r[1])), ((r[2], r[1]), (r[2], r[3])),
             ((r[2], r[3]), (r[0], r[3])), ((r[0], r[3]), (r[0], r[1]))]
    n = len(poly)
    for i in range(n):
        f = (poly[i], poly[(i + 1) % n])
        for e in edges:
            if seg_cross(e[0] + e[1], f[0] + f[1]):
                return True
    return False


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'lin-g4.html'
    quiet = '--quiet' in sys.argv
    html_text = io.open(path, encoding='utf-8').read()
    # 剔除 HTML 注释：模板里的「写法示例」是注释状态，不能当真实元件解析（否则误报悬空/重叠/ANNOS 缺）
    html_text = re.sub(r'<!--.*?-->', '', html_text, flags=re.S)
    svg = html_text[:html_text.index('<script>')]
    script = html_text[html_text.index('<script>'):]

    problems = []
    warnings = []
    print('=' * 74)
    print('SVG 布局自检 :', path)
    print('=' * 74)

    # ---------- ① 结构 ----------
    ids = [i for i in re.findall(r'data-id="([^"]+)"', svg) if i != 'calc-panel']
    dup = sorted(set(i for i in ids if ids.count(i) > 1))
    m = re.search(r'const STAGE_UNITS = \[(.*?)\n    \];', script, re.S)
    su = re.findall(r"'([a-z0-9-]+)'", m.group(1)) if m else []
    ann = re.findall(r"^\s{8}'([a-z0-9-]+)':\s*\{", script, re.M)
    print('[结构] 交互单元 %d 个, 唯一 %d 个' % (len(ids), len(set(ids))))
    if dup:
        problems.append('data-id 重复: %s' % dup)
    if su:   # 仅游戏闯关页有 STAGE_UNITS；学习/训练页无此结构
        miss_su = [i for i in ids if i not in su]
        extra_su = [i for i in set(su) if i not in ids]
        if miss_su:
            problems.append('STAGE_UNITS 缺: %s' % miss_su)
        if extra_su:
            problems.append('STAGE_UNITS 多: %s' % extra_su)
    miss_ann = [i for i in ids if i not in ann]
    if miss_ann:
        problems.append('ANNOS 缺: %s' % miss_ann)
    print('       STAGE_UNITS %d 项 / ANNOS %d 项 %s'
          % (len(su), len(set(ann)), 'OK' if not (miss_ann or dup or (su and miss_su)) else '见报告'))

    # ---------- 解析 ----------
    items, panel_left = parse(html_text)
    comps = [i for i in items if i.kind == 'comp']
    labels = [i for i in items if i.kind == 'label']
    wires = [i for i in items if i.kind == 'wire']
    print('[解析] 元件 %d / 标签 %d / 导线 %d ; 面板内左缘 %.1f'
          % (len(comps), len(labels), len(wires), panel_left))
    if not quiet:
        print('-' * 74)
        for it in items:
            b = it.bbox
            print('  %-6s %-16s %-28s (%.0f,%.0f)-(%.0f,%.0f)  %.0f×%.0f'
                  % (it.kind, it.owner, it.name[:14], b[0], b[1], b[2], b[3], b[2] - b[0], b[3] - b[1]))
    print('-' * 74)

    # ---------- ② 元件互压 ----------（端子小圆点(r<15)贴元件属设计，不参与互压）
    solids = [c for c in comps if c.extra.get('circle', 99) >= 15]
    for k in range(len(solids)):
        for j in range(k + 1, len(solids)):
            if overlap(solids[k].bbox, solids[j].bbox):
                problems.append('元件重叠: %s ↔ %s' % (solids[k].owner, solids[j].owner))
    print('[② 元件互压] %s' % ('无' if not any('元件重叠' in p for p in problems) else '见报告'))

    # ---------- ③ 标签冲突 ----------
    n_a = n_b = n_c = 0
    for lb in labels:
        for cp in comps:
            # 设计性豁免: 运放内的 ＋/− 极性符号
            if lb.name in ('＋', '－', '+', '−') and re.match(r'comp-input-(pos|neg)', lb.owner):
                continue
            b, cb = lb.bbox, cp.bbox
            poly = cp.extra.get('poly')
            if poly:
                hit = rect_poly_overlap(b, poly)
            else:
                hit = overlap(b, cb)
            if hit:
                # 完全内嵌（运放三角内 A₁ / 三角内极性符号）→ 设计如此
                inside = (b[0] >= cb[0] - 1 and b[2] <= cb[2] + 1 and b[1] >= cb[1] - 1 and b[3] <= cb[3] + 1)
                if inside:
                    continue
                n_a += 1
                problems.append('标签压元件: 「%s」%s ↔ %s(%s) gap=%.1f'
                                % (lb.name, lb.owner, cp.owner, cp.name[:12], gap(b, cb)))
            else:
                g = gap(b, cb)
                if 0 < g < NEAR_GAP and cp.owner != lb.owner:
                    n_c += 1
                    warnings.append('标签贴边(间隙 %.1f < %.0f): 「%s」%s ↔ %s' % (g, NEAR_GAP, lb.name, lb.owner, cp.owner))
    for k in range(len(labels)):
        for j in range(k + 1, len(labels)):
            if overlap(labels[k].bbox, labels[j].bbox, PAD):
                n_b += 1
                problems.append('标签互压: 「%s」%s ↔ 「%s」%s'
                                % (labels[k].name, labels[k].owner, labels[j].name, labels[j].owner))
    print('[③ 标签冲突] 压元件 %d / 标签互压 %d / 贴边警告 %d' % (n_a, n_b, n_c))

    # ---------- ③b 导线穿行（lin-g4 教训：导线不得从「标签与自身元件」之间的空档穿过）----------
    n_w = 0
    for lb in labels:
        owns = [c for c in comps if c.owner == lb.owner]
        if not owns:
            continue
        cb = owns[0].bbox
        b = lb.bbox
        if b[3] <= cb[1]:          # 标签在元件上方 → 检查 (标签墨迹底, 元件上沿) 水平带
            y_lo, y_hi = b[3] + 1, cb[1] - 1
        elif b[1] >= cb[3]:        # 标签在元件下方 → 检查 (元件下沿, 标签墨迹顶) 水平带
            y_lo, y_hi = cb[3] + 1, b[1] - 1
        else:
            continue
        x_lo, x_hi = max(b[0], cb[0]) + 2, min(b[2], cb[2]) - 2
        if x_hi <= x_lo:
            continue
        for w in wires:
            if w.owner == lb.owner:
                continue
            hit = False
            for s in w.extra['segs']:
                x1, y1, x2, y2 = s
                if abs(y1 - y2) < 0.5 and y_lo < y1 < y_hi:
                    sx, ex = min(x1, x2), max(x1, x2)
                    if ex > x_lo and sx < x_hi:
                        problems.append('导线从标签与元件之间穿过: 「%s」%s ↔ %s(%s)  y=%.0f'
                                        % (lb.name, lb.owner, owns[0].owner, owns[0].name[:10], y1))
                        n_w += 1
                        hit = True
                        break
            if hit:
                break
    print('[③b 导线穿行] %s' % ('无' if n_w == 0 else '%d 处，见报告'))

    # ---------- ④ 导线端点悬空 ----------
    # 豁免: ① data-name 含"接地" ② 接地符号的短横线(同组内多条同轴水平线)
    #       ③ owner=misc 的装饰/演示图层箭头(表头分隔线、示意箭头、动画演示线)
    #       ④ 电容极板 / 晶体管基极条（开路端为元件符号固有画法，非接线，cj-g1 新增）
    hatch = set()
    by_owner = {}
    for w in wires:
        by_owner.setdefault(w.owner, []).append(w)
    for own, ws in by_owner.items():
        hs = [w for w in ws if all(abs(s[1] - s[3]) < 0.5 for s in w.extra['segs'])]
        if len(hs) >= 2:
            cx = [ (w.bbox[0] + w.bbox[2]) / 2.0 for w in hs ]
            if max(cx) - min(cx) < 3:
                for w in hs:
                    hatch.add(id(w))
    before = len(problems)
    for w in wires:
        if '接地' in (w.name or '') or '电容' in (w.name or '') or '晶体管' in (w.name or '') or w.owner == 'misc' or id(w) in hatch:
            continue
        own = []
        for s in w.extra['segs']:
            own.append((s[0], s[1]))
            own.append((s[2], s[3]))
        for s in w.extra['segs']:
            for p in ((s[0], s[1]), (s[2], s[3])):
                if sum(1 for q in own if abs(q[0] - p[0]) <= 1 and abs(q[1] - p[1]) <= 1) > 1:
                    continue
                ok = False
                for w2 in wires:
                    if w2 is w:
                        continue
                    for s2 in w2.extra['segs']:
                        if seg_dist(p, s2) <= SNAP:
                            ok = True
                            break
                    if ok:
                        break
                if not ok:
                    for cp in comps:
                        b = cp.bbox
                        if b[0] - SNAP <= p[0] <= b[2] + SNAP and b[1] - SNAP <= p[1] <= b[3] + SNAP:
                            ok = True
                            break
                if not ok:
                    problems.append('导线端点悬空: %s @ (%.0f,%.0f)' % (w.owner, p[0], p[1]))
    print('[④ 导线端点] %s' % ('全部连接' if len(problems) == before else '见报告'))

    # ---------- ⑤ 导线交叉 ----------
    before = len(problems)
    for k in range(len(wires)):
        for j in range(k + 1, len(wires)):
            for sa in wires[k].extra['segs']:
                for sb in wires[j].extra['segs']:
                    if seg_cross(sa, sb):
                        problems.append('导线交叉: %s × %s' % (wires[k].owner, wires[j].owner))
    print('[⑤ 导线交叉] %d 处' % (len(problems) - before))

    # ---------- ⑥ 越界 ----------
    before = len(problems)
    for it in items:
        b = it.bbox
        if b[2] > panel_left - PANEL_GAP:
            problems.append('越入右侧面板: %s 右缘 %.0f > %.0f' % (it.owner, b[2], panel_left - PANEL_GAP))
        if b[1] < TOP_LIMIT:
            problems.append('越过顶部: %s 上缘 %.0f' % (it.owner, b[1]))
        if b[3] > BOTTOM_LIMIT:
            problems.append('越过底部安全线: %s 下缘 %.0f' % (it.owner, b[3]))
    print('[⑥ 边界] %s' % ('安全' if len(problems) == before else '见报告'))

    # ---------- ⑦ 元件间距均匀性 ----------
    real = [c for c in comps if c.owner != 'misc' and c.extra.get('circle', 99) >= 15]
    nn = []
    for i, c in enumerate(real):
        best, who = 1e9, ''
        for j, d in enumerate(real):
            if i == j:
                continue
            g = gap(c.bbox, d.bbox)
            if g < best:
                best, who = g, d.owner
        nn.append((best, c.owner, who))
    crowded = [t for t in nn if t[0] < MIN_PITCH]
    loose = [t for t in nn if t[0] > LOOSE_PITCH]
    for t in crowded:
        problems.append('元件拥挤(净间隙 %.1f < %.0f): %s ↔ %s' % (t[0], MIN_PITCH, t[1], t[2]))
    for t in loose:
        warnings.append('布局松散(最近邻 %.0f > %.0f): %s ↔ %s' % (t[0], LOOSE_PITCH, t[1], t[2]))
    if nn:
        print('[⑦ 元件间距] 最近邻 中位 %.1f / 最小 %.1f / 最大 %.1f  %s'
              % (sorted(t[0] for t in nn)[len(nn) // 2], min(t[0] for t in nn), max(t[0] for t in nn),
                 'OK' if not crowded else '✗ 拥挤 %d 处' % len(crowded)))

    # ---------- ⑧ 两端导线均衡 ----------
    leads = []
    for c in real:
        b = c.bbox
        horiz = (b[2] - b[0]) > (b[3] - b[1])
        cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
        ends = (((b[0], cy), (b[2], cy)) if horiz else ((cx, b[1]), (cx, b[3])))
        lens = []
        for e in ends:
            L = None
            for w in wires:
                for s in w.extra['segs']:
                    for p, q in (((s[0], s[1]), (s[2], s[3])), ((s[2], s[3]), (s[0], s[1]))):
                        if abs(p[0] - e[0]) <= 3 and abs(p[1] - e[1]) <= 3:
                            L = ((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** 0.5
            lens.append(L)
        if lens[0] and lens[1] and min(lens) > 0:
            r = max(lens) / min(lens)
            leads.append((r, c.owner, lens[0], lens[1]))
    bad = [t for t in leads if t[0] > LEAD_RATIO]
    for t in bad:
        warnings.append('两端导线不均: %s  %.0f : %.0f = %.2f (>%.1f)'
                        % (t[1], t[2], t[3], t[0], LEAD_RATIO))
    print('[⑧ 导线均衡] 可比元件 %d 个, 不均衡 %d 处' % (len(leads), len(bad)))

    # ---------- ⑨ 下标比例一致性 ----------
    pct = re.findall(r'tspan\.sub[^}]*font-size:\s*(\d+)%', svg)
    uniq = sorted(set(pct))
    if uniq and (len(uniq) > 1 or abs(int(uniq[0]) - SUB_SCALE * 100) > 0.5):
        warnings.append('下标字号 %s%% 与自检 SUB_SCALE=%s 不一致（须统一，见规范第五节）' % ('/'.join(uniq), SUB_SCALE))
    print('[⑨ 下标比例] %s' % ('/'.join('%s%%' % u for u in uniq) or '未声明'))

    print('-' * 74)
    if warnings:
        print('⚠ 提示 %d 条（不判失败）:' % len(warnings))
        for w in sorted(set(warnings)):
            print('   -', w)
    if problems:
        print('✗ 发现 %d 个硬错误:' % len(problems))
        for p in sorted(set(problems)):
            print('   -', p)
        sys.exit(1)
    print('✓ 布局自检全部通过')


if __name__ == '__main__':
    main()
