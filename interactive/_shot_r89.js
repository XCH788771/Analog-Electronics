// r89: 验证 ①V_s 置零后短接桥连通 ②V_s 上移后渲染 ③等效态 Vi 新布局
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g3.html';

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.addInitScript(() => { window.__ttsPatched = false; });
  await page.addInitScript(() => {
    const patch = () => {
      if (window.__ttsPatched || typeof window.speakSeq !== 'function') { setTimeout(patch, 30); return; }
      window.__ttsPatched = true;
      window.speakSeq = function (parts, onDone) {
        (parts || []).forEach(p => { if (p && p.onStart) { try { p.onStart(); } catch (e) {} } });
        if (onDone) { try { onDone(); } catch (e) {} }
      };
    };
    patch();
  });
  await page.goto(PAGE + '?cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(800);

  // ① V_s 置零 → 短接桥应连通（fx-vs 覆盖范围 = 圆 443-487，与上下导线 371-443 / 487-525 无缝）
  const hoverUnit = async id => {
    await page.evaluate(i => {
      const g = document.querySelector(`#circuit-wrap g[data-id="${i}"]`);
      if (!g) throw new Error('no ' + i);
      try { hideMenu(); } catch (e) {}
      g.dispatchEvent(new MouseEvent('mouseenter', { bubbles: false }));
    }, id);
    await page.waitForTimeout(250);
  };
  const menuClick = async t => {
    const items = page.locator('#ctxmenu .mi');
    const n = await items.count();
    for (let i = 0; i < n; i++) {
      const txt = (await items.nth(i).innerText()).replace(/[\s_]/g, '');
      if (txt.includes(String(t).replace(/[\s_]/g, ''))) {
        await items.nth(i).hover(); await page.waitForTimeout(160);
        await items.nth(i).click(); await page.waitForTimeout(300);
        return true;
      }
    }
    return false;
  };
  await hoverUnit('comp-src');
  console.log('V_s 菜单置零:', await menuClick('置零'));
  await page.waitForTimeout(600);
  const fx = await page.evaluate(() => {
    const g = document.querySelector('#fx-vs');
    const line = g && g.querySelector('line');
    return { op: g && g.style.opacity, y1: line && line.getAttribute('y1'), y2: line && line.getAttribute('y2') };
  });
  console.log('fx-vs:', JSON.stringify(fx));

  // 截取信号源列（含 R_S 下端 → 短接桥 → 地），目检连通性
  const box = await page.locator('#circuit-wrap g[data-id="wire-rs-bot"]').boundingBox();
  await page.screenshot({
    path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/r89_vs_zero.png',
    clip: { x: Math.max(0, box.x - 90), y: box.y - 20, width: 300, height: 400 },
  });
  console.log('V_s 置零截图完成');

  // ③ 跳到第 4 关等效态，截取 Vi 列
  await page.goto(PAGE + '?lvl=4&cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(900);
  // 走完第4关三步（信号源/电源置零 → 电容 → 整理 → 等效）
  for (const id of ['comp-src', 'comp-vcc', 'comp-vee']) { await hoverUnit(id); await menuClick('置零'); }
  await page.waitForTimeout(500);
  for (const id of ['comp-c1', 'comp-c2', 'comp-ce']) { await hoverUnit(id); await menuClick('短路'); }
  await page.waitForTimeout(500);
  await hoverUnit('comp-rc'); await menuClick('整理');
  await page.waitForTimeout(400);
  await hoverUnit('comp-t'); await menuClick('等效');
  await page.waitForTimeout(1200);
  const eqVisible = await page.evaluate(() => {
    const l = document.querySelector('#eq-layer');
    return l ? (l.style.opacity || getComputedStyle(l).opacity) : 'no';
  });
  console.log('eq-layer opacity =', eqVisible);
  const vb = await page.locator('#circuit-wrap g[data-id="comp-vi"]').boundingBox().catch(() => null);
  await page.screenshot({
    path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/r89_eq_vi.png',
    clip: { x: 0, y: 350, width: 420, height: 480 },
  });
  console.log('等效态 Vi 截图完成; pageerrors =', errs.length);
  await browser.close(); process.exit(0);
})();
