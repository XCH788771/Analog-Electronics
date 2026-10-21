// cj-g5 面板文字右缘实测 + 各状态标签近压复查
// 断言：①右侧面板（x>1000）内所有可见文本右缘 ≤1530；②电路区标签互近/近压同 measure_g3 门槛
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g5.html';

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = []; page.on('pageerror', e => errs.push(String(e)));
  await page.addInitScript(() => {
    window.speechSynthesis = { speak(u){ setTimeout(()=>u.onend&&u.onend({}),2); }, cancel(){}, getVoices:()=>[] };
    window.SpeechSynthesisUtterance = function(t){ this.text=t; };
  });

  const collect = () => page.evaluate(() => {
    function vis(el) {
      let n = el;
      while (n && n !== document.body) {
        const cs = getComputedStyle(n);
        if (cs.display === 'none' || cs.visibility === 'hidden') return false;
        if (parseFloat(cs.opacity) === 0) return false;
        n = n.parentNode;
      }
      return true;
    }
    const panel = [], labels = [], shapes = [];
    // SVG 文本
    document.querySelectorAll('svg text').forEach(el => {
      if (!vis(el)) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      const item = { txt: (el.textContent || '').trim().slice(0, 16),
                     x0: +r.left.toFixed(1), x1: +r.right.toFixed(1), y0: +r.top.toFixed(1), y1: +r.bottom.toFixed(1) };
      const inPanel = r.left > 1000 && r.bottom > 100;   // y<100 为页头部件（返回/✕），非计分面板
      if (inPanel) panel.push(item);
      else if (r.top > 160) labels.push(item);           // top≤160 为页头案例行/已知行，模板固定布局
    });
    // HTML 文本（右面板若为 HTML）
    document.querySelectorAll('body *').forEach(el => {
      if (el.closest('svg')) return;
      if (!vis(el) || !el.childNodes.length) return;
      const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      if (!hasText) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      if (r.left > 1000 && r.bottom > 100) panel.push({ txt: (el.textContent || '').trim().slice(0, 16),
                                                        x0: +r.left.toFixed(1), x1: +r.right.toFixed(1), y0: 0, y1: 0 });
    });
    // 电路区图形（近压复查用）
    document.querySelectorAll('#circuit-wrap rect[fill="none"], #circuit-wrap circle, #circuit-wrap polygon, #circuit-wrap line').forEach(el => {
      if (!vis(el)) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 && r.height < 2) return;
      shapes.push({ tag: el.tagName, id: el.id || (el.parentNode && el.parentNode.id) || '-',
                    x0: +r.left.toFixed(1), x1: +r.right.toFixed(1), y0: +r.top.toFixed(1), y1: +r.bottom.toFixed(1) });
    });
    return { panel, labels, shapes };
  });

  const gap = (a, b) => {
    const dx = Math.max(0, Math.max(a.x0 - b.x1, b.x0 - a.x1));
    const dy = Math.max(0, Math.max(a.y0 - b.y1, b.y0 - a.y1));
    return Math.hypot(dx, dy);
  };

  const states = [
    ['第1关 默认态', '?lvl=1'],
    ['第3关 Q点计算', '?lvl=3'],
    ['第4关 整理态', '?lvl=4&tidy=1'],
    ['第4关 等效完成', '?lvl=4&ts=6'],
    ['第5关 动态指标', '?lvl=5'],
  ];
  let fail = 0;
  for (const [name, q] of states) {
    await page.goto(PAGE + q + '&cb=' + Date.now(), { waitUntil: 'load' });
    await page.waitForTimeout(600);
    const { panel, labels, shapes } = await collect();
    // ① 面板右缘
    const over = panel.filter(t => t.x1 > 1530);
    const mx = panel.length ? Math.max(...panel.map(t => t.x1)) : 0;
    console.log(`\n===== ${name}：面板文本 ${panel.length} 条，最右 ${mx.toFixed(1)}px =====`);
    if (over.length) { fail++; over.forEach(t => console.log(`  ❌ 右缘超限 ${t.x1}px: "${t.txt}"`)); }
    else console.log('  ✓ 面板右缘 ≤1530');
    // ② 电路区标签复查（口径同 cj-g3 基线：互近为硬项但豁免单字符 ±/－ 与其所属量的设计配对；压图为信息项）
    const PM = t => ['＋', '−', '－'].includes(t);
    const bad = [];
    for (let i = 0; i < labels.length; i++) for (let j = i + 1; j < labels.length; j++) {
      const g = gap(labels[i], labels[j]);
      if (g > 0.5 && g < 14 && !PM(labels[i].txt) && !PM(labels[j].txt))
        bad.push(`  标签互近 ${g.toFixed(1)}px: "${labels[i].txt}" × "${labels[j].txt}"`);
    }
    const near = [];
    for (const t of labels) for (const s of shapes) {
      const g = gap(t, s);
      if (g > 0.5 && g < 12) near.push(`  [info] 标签压图 ${g.toFixed(1)}px: "${t.txt}" ↔ ${s.tag}#${s.id}`);
    }
    if (bad.length) { fail++; console.log([...new Set(bad)].join('\n')); }
    else console.log('  ✓ 电路区标签互近 无');
    if (near.length) console.log([...new Set(near)].join('\n') + '\n  （上为 info：标注与其所属元件的固有邻近，em 盒高估墨迹，同 cj-g3 定稿基线）');
  }
  console.log('\npageerrors:', errs.length ? errs : '无');
  console.log(fail ? `❌ ${fail} 处待修` : '✅ 右缘/近压全部通过');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
