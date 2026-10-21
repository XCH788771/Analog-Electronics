// r91 可视化流程：从第1关顺序通关到第4关（整理完成 + 等效），验证 tidyShift 位移与截图
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

  const st = () => page.evaluate(() => ({
    lvl: S.level, score: Math.round(S.score), finished: S.finished,
    per: Math.round(S.levelScore[S.level - 1]), title: LEVELS[S.level - 1].cfg.title,
  }));
  async function menuClick(optText) {
    const items = page.locator('#ctxmenu .mi');
    const n = await items.count();
    if (!n) return false;
    for (let i = 0; i < n; i++) {
      if (norm(await items.nth(i).innerText()).includes(norm(optText))) {
        await items.nth(i).hover(); await page.waitForTimeout(160);
        await items.nth(i).click(); await page.waitForTimeout(220);
        return true;
      }
    }
    return false;
  }
  async function hoverUnit(unitId) {
    await page.evaluate(id => {
      const g = document.querySelector(`#circuit-wrap g[data-id="${id}"]`);
      if (!g) throw new Error('no ' + id);
      try { hideMenu(); } catch (e) {}
      g.dispatchEvent(new MouseEvent('mouseenter', { bubbles: false }));
    }, unitId);
    await page.waitForTimeout(220);
  }
  async function pickByMenu(unitId, first, second) {
    await hoverUnit(unitId);
    if (!(await menuClick(first))) throw new Error(unitId + ' 无菜单项 ' + first);
    if (second && !(await menuClick(second))) throw new Error(unitId + ' 无二级 ' + second);
  }
  const tf = async id => page.evaluate(i => {
    const el = document.querySelector('#circuit-wrap g[data-id="' + i + '"]') || document.getElementById(i);
    return el ? (el.getAttribute('transform') || 'none') : 'missing';
  }, id);
  const shot = (name, clip) => page.screenshot({ path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/' + name, clip });

  // 第1关
  await pickByMenu('comp-src', '置零', '短路');
  await pickByMenu('comp-vcc', '保留');
  await pickByMenu('comp-vee', '保留');
  for (const c of ['comp-c1', 'comp-c2', 'comp-ce']) await pickByMenu(c, '断路');
  await page.waitForTimeout(1900);
  console.log('第1关后:', JSON.stringify(await st()));

  // 第4关（直接切关到 L4 需 gate 满足——顺序通关后自然进入；此处若仍在 L2/L3 用引擎跳转不可行，
  //       故采用「跑完 L2/L3 正确路径」太耗；替代：切到第4关前把 draw 状态补全再进）
  // 简化：直接操作引擎进入第4关并补齐 gate/found
  await page.evaluate(() => { S.level = 4; S.score = 61; resetCircuit(); startLevel(); });
  await page.waitForTimeout(600);

  await pickByMenu('comp-src', '保留');
  await pickByMenu('comp-vcc', '置零', '接地');
  await pickByMenu('comp-vee', '置零', '接地');
  await pickByMenu('comp-c1', '短路');
  await pickByMenu('comp-c2', '短路');
  await pickByMenu('comp-ce', '短路');
  console.log('交流通路后 transform:', JSON.stringify({ rc: await tf('rarr-rc'), rl: await tf('comp-rl'), t: await tf('comp-t') }));

  await pickByMenu('comp-re2', '移除');
  await page.waitForTimeout(500);
  console.log('RE2移除后 transform:', JSON.stringify({ rc: await tf('rarr-rc'), rl: await tf('comp-rl'), t: await tf('comp-t'), re1: await tf('comp-re1'),
    tidyLines: await page.evaluate(() => document.getElementById('fx-tidy-lines').style.opacity) }));
  await shot('r91_tidy.png', { x: 0, y: 150, width: 950, height: 700 });

  await pickByMenu('comp-re1', '保留');
  await pickByMenu('comp-rc', '下移'); await menuClick('与RL并');
  await page.waitForTimeout(700);
  console.log('整理完成 transform:', JSON.stringify({ rc: await tf('rarr-rc'), rl: await tf('comp-rl'), fx2: await tf('fx-c2'),
    tidyLines: await page.evaluate(() => document.getElementById('fx-tidy-lines').style.opacity) }));
  await shot('r91_tidy2.png', { x: 0, y: 150, width: 950, height: 700 });

  await pickByMenu('comp-t', '等效');
  await page.waitForTimeout(1200);
  console.log('等效态 transform:', JSON.stringify({ rc: await tf('rarr-rc'), rl: await tf('comp-rl'), fx2: await tf('fx-c2'), c2: await tf('comp-c2'),
    tidyLines: await page.evaluate(() => document.getElementById('fx-tidy-lines').style.opacity) }));
  await shot('r91_eq.png', { x: 0, y: 150, width: 950, height: 720 });
  // 五连问（验 fx-t-ib/ic 新位置与红点对齐）
  for (let k = 0; k < 6; k++) {
    const q = await page.evaluate(() => {
      const d = S.draw[3];
      if (!d.tquiz || d.tquiz.step >= TQUIZ.length) return null;
      return { ok: TQUIZ[d.tquiz.step].ok, step: d.tquiz.step };
    });
    if (!q) break;
    if (!(await menuClick(q.ok))) throw new Error('问' + (q.step + 1) + '无选项 ' + q.ok);
    await page.waitForTimeout(750);
  }
  await page.waitForTimeout(900);
  await shot('r91_eq_quiz.png', { x: 200, y: 150, width: 700, height: 560 });
  console.log('pageerrors:', errs.length, errs.slice(0, 2));
  await browser.close(); process.exit(0);
})();
