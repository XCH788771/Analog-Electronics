// cj-g3 整理态/等效态标签墨迹实测（只统计真正可见的元素；fx-layer 不在静态自检范围）
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g3.html';

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
    const labels = [], shapes = [];
    document.querySelectorAll('#circuit-wrap text').forEach(el => {
      if (!vis(el)) return;
      let r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      // 用 getComputedTextLength 收紧左右边界（getBBox 含 em 盒偏大）
      const cx = parseFloat(el.getAttribute('x')) || 0;
      const anch = el.getAttribute('text-anchor') || 'start';
      let w = 0; try { w = el.getComputedTextLength(); } catch (e) {}
      let x0 = cx; if (anch === 'middle') x0 = cx - w/2; else if (anch === 'end') x0 = cx - w;
      labels.push({ id: el.id || (el.parentNode && el.parentNode.id) || '', txt: (el.textContent||'').trim().slice(0,12),
                    x0:+x0.toFixed(1), x1:+(x0+w).toFixed(1), y0:+r.top.toFixed(1), y1:+r.bottom.toFixed(1) });
    });
    document.querySelectorAll('#circuit-wrap rect[fill="none"], #circuit-wrap circle, #circuit-wrap polygon, #circuit-wrap line').forEach(el => {
      if (!vis(el)) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 && r.height < 2) return;
      const tag = el.tagName;
      shapes.push({ tag, id: el.id || (el.parentNode && el.parentNode.id) || '',
                    x0:+r.left.toFixed(1), x1:+r.right.toFixed(1), y0:+r.top.toFixed(1), y1:+r.bottom.toFixed(1) });
    });
    return { labels, shapes };
  });

  const gap = (a,b) => {
    const dx = Math.max(0, Math.max(a.x0-b.x1, b.x0-a.x1));
    const dy = Math.max(0, Math.max(a.y0-b.y1, b.y0-a.y1));
    return Math.hypot(dx, dy);
  };

  for (const [name, q] of [['def 默认态','?lvl=1'],['tidy 整理态','?lvl=4&tidy=1'],['ts6 等效完成','?lvl=4&ts=6'],['ts3 受控源','?lvl=4&ts=3']]) {
    await page.goto(PAGE + q, { waitUntil: 'load' });
    await page.waitForTimeout(500);
    const { labels, shapes } = await collect();
    console.log(`\n===== ${name}：可见标签 ${labels.length} =====`);
    const bad = [];
    for (let i=0;i<labels.length;i++) for (let j=i+1;j<labels.length;j++) {
      const g = gap(labels[i], labels[j]);
      if (g > 0.5 && g < 14) bad.push(`  标签互近 ${g.toFixed(1)}px: "${labels[i].txt}" × "${labels[j].txt}"`);
    }
    console.log(bad.length ? [...new Set(bad)].join('\n') : '  ✓ 标签互压/近压 无（≥14px）');
    const bad2 = [];
    for (const t of labels) for (const s of shapes) {
      const g = gap(t, s);
      if (g > 0.5 && g < 12) bad2.push(`  标签压图 ${g.toFixed(1)}px: "${t.txt}" ↔ ${s.tag}#${s.id||'-'}`);
    }
    console.log(bad2.length ? [...new Set(bad2)].join('\n') : '  ✓ 标签-图形 近压 无（≥12px）');
  }
  console.log('\npageerrors:', errs.length ? errs : '无');
  await browser.close();
})();
