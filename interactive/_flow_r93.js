// r93 真实菜单流程：第1关 → 第4关（先整理 R_C，再移除 R_E2），逐步截图核对
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g3.html';
const norm = s => String(s || '').replace(/[\s_]/g, '');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.addInitScript(() => {
    const patch = () => {
      if (typeof window.speakSeq !== 'function') { setTimeout(patch, 30); return; }
      window.speakSeq = function (parts, onDone) {
        (parts || []).forEach(p => { if (p && p.onStart) { try { p.onStart(); } catch (e) {} } });
        if (onDone) { try { onDone(); } catch (e) {} }
      };
    };
    patch();
  });
  await page.goto(PAGE + '?cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(700);

  async function menuClick(t) {
    const items = page.locator('#ctxmenu .mi');
    for (let i = 0; i < await items.count(); i++) {
      if (norm(await items.nth(i).innerText()).includes(norm(t))) {
        await items.nth(i).hover(); await page.waitForTimeout(160);
        await items.nth(i).click(); await page.waitForTimeout(240);
        return true;
      }
    }
    return false;
  }
  async function hoverUnit(id) {
    await page.evaluate(i => {
      const g = document.querySelector('#circuit-wrap g[data-id="' + i + '"]');
      if (!g) throw new Error('no ' + i);
      try { hideMenu(); } catch (e) {}
      g.dispatchEvent(new MouseEvent('mouseenter', { bubbles: false }));
    }, id);
    await page.waitForTimeout(220);
  }
  async function pick(unitId, first, second) {
    await hoverUnit(unitId);
    if (!(await menuClick(first))) throw new Error(unitId + ' 无「' + first + '」');
    if (second && !(await menuClick(second))) throw new Error(unitId + ' 无二级「' + second + '」');
  }
  const shot = (n, clip) => page.screenshot({ path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/' + n, clip });
  const fx = () => page.evaluate(() => {
    const o = {};
    ['fx-ce-tail', 'fx-gnd-jct', 'fx-tidy-lines', 'fx-ce', 'wire-ce-b', 'comp-ce', 'node-re', 'wire-ree-b'].forEach(id => {
      const el = document.querySelector('#circuit-wrap g[data-id="' + id + '"]') || document.getElementById(id);
      o[id] = el ? getComputedStyle(el).opacity : 'missing';
    });
    return o;
  });

  // 第1关（直流通路）：信号源置零→短路；两电源保留；三电容断路
  await pick('comp-src', '置零', '短路');
  await pick('comp-vcc', '保留');
  await pick('comp-vee', '保留');
  for (const c of ['comp-c1', 'comp-c2', 'comp-ce']) await pick(c, '断路');
  await page.waitForTimeout(1900);
  console.log('第1关后 lvl =', await page.evaluate(() => S.level));

  // 第4关：引擎切关（顺序通关后 L2/L3 走正确路径太耗，直接置状态）
  await page.evaluate(() => { S.level = 4; S.score = 61; resetCircuit(); render(); });
  await page.waitForTimeout(500);
  await pick('comp-src', '保留');
  await pick('comp-vcc', '置零', '接地');
  await pick('comp-vee', '置零', '接地');
  await pick('comp-c1', '短路');
  await pick('comp-c2', '短路');
  await pick('comp-ce', '短路');
  await page.waitForTimeout(500);
  // 先整理 R_C（下移 → 与RL并）
  await pick('comp-rc', '下移'); await menuClick('与RL并');
  await page.waitForTimeout(800);
  console.log('RC整理后 fx:', JSON.stringify(await fx()));
  await shot('r93_flow_rc.png', { x: 380, y: 460, width: 420, height: 300 });
  await shot('r93_flow_rc_full.png', { x: 0, y: 150, width: 950, height: 700 });
  // 再移除 R_E2
  await pick('comp-re2', '移除');
  await page.waitForTimeout(800);
  console.log('RE2移除后 fx:', JSON.stringify(await fx()));
  await shot('r93_flow_re2.png', { x: 380, y: 460, width: 420, height: 300 });
  await shot('r93_flow_re2_full.png', { x: 0, y: 150, width: 950, height: 700 });
  // 保留 R_E1
  await pick('comp-re1', '保留');
  await page.waitForTimeout(600);
  await shot('r93_flow_re1.png', { x: 380, y: 460, width: 420, height: 300 });
  console.log('pageerrors:', errs.length, errs.slice(0, 2));
  await browser.close(); process.exit(0);
})();
