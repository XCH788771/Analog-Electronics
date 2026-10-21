// cj-g4 满分回归：Playwright 真实 UI 走正确路径，断言 score===100 && finished && pageerrors=0
// 答案表运行时从页面内部状态读（TQUIZ[step].ok / opts.findIndex(o=>o.correct) / blanks.ansIds），不硬编码。
// 结构：L1 直流通路(10) / L2 qorder 4路线(16) / L3 Q点 mix(28) / L4 交流等效 draw(16) / L5 动态 mix(30) = 100
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g4.html';
const norm = s => String(s || '').replace(/[\s_]/g, '');
const ROUTE = ['0', '1', '2', '3'].indexOf(process.env.ROUTE) >= 0 ? +process.env.ROUTE : 0;

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
  await page.waitForTimeout(500);

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
        await items.nth(i).hover(); await page.waitForTimeout(150);
        await items.nth(i).click(); await page.waitForTimeout(180);
        return true;
      }
    }
    return false;
  }
  async function hoverUnit(unitId) {
    const ok = await page.evaluate(id => {
      const g = document.querySelector(`#circuit-wrap g[data-id="${id}"]`);
      if (!g) return false;
      try { hideMenu(); } catch (e) {}
      g.dispatchEvent(new MouseEvent('mouseenter', { bubbles: false }));
      return true;
    }, unitId);
    if (!ok) throw new Error('无此元件 ' + unitId);
    await page.waitForTimeout(200);
  }
  async function pickByMenu(unitId, first, second) {
    await hoverUnit(unitId);
    if (!(await menuClick(first))) {
      const items = page.locator('#ctxmenu .mi'); const t = [];
      for (let i = 0; i < await items.count(); i++) t.push(await items.nth(i).innerText());
      throw new Error(`${unitId} 菜单无「${first}」，现有：${JSON.stringify(t)}`);
    }
    if (second && !(await menuClick(second))) throw new Error(`${unitId} 二级菜单无「${second}」`);
  }
  const clickUnit = id => page.evaluate(i => {
    const g = document.querySelector(`#circuit-wrap g[data-id="${i}"]`);
    if (!g) throw new Error('无此单元 ' + i);
    g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  }, id);
  const pickMixOpt = async idx => { await page.locator('.g-opt').nth(idx).click({ force: true }); await page.waitForTimeout(1700); };

  console.log('  起点:', JSON.stringify(await st()));

  // 第1关：直流通路（无 comp-vee）
  await pickByMenu('comp-src', '置零', '短路');
  await pickByMenu('comp-vcc', '保留');
  for (const c of ['comp-c1', 'comp-c2', 'comp-ce']) await pickByMenu(c, '断路');
  await page.waitForTimeout(1800);
  console.log('  第1关后:', JSON.stringify(await st()));

  // 第2关：按 ROUTE 取第 ROUTE 条合法顺序
  const seq = await page.evaluate(i => {
    const c = LEVELS[S.level - 1].cfg;
    const ss = c.seqs || [c.seq];
    return ss[i].map(x => [].concat(x)[0]);
  }, ROUTE);
  console.log('  第2关路线#' + ROUTE + ':', seq.join(' → '));
  for (let i = 0; i < seq.length; i++) {
    await clickUnit(seq[i]);
    await page.waitForTimeout(300);
    if (i === seq.length - 1) {
      for (let w = 0; w < 20; w++) { const cur = await st(); if (cur.lvl !== 2) break; await page.waitForTimeout(250); }
    }
  }
  await page.waitForTimeout(600);
  console.log('  第2关后:', JSON.stringify(await st()));

  // 第3关：mix（读运行时答案）
  for (let guard = 0; guard < 60; guard++) {
    const s = await st(); if (s.lvl !== 3) break;
    const info = await page.evaluate(() => {
      const mx = S.mix[S.level - 1], stp = mx.steps[mx.si];
      if (stp.type === 'fw') return { type: 'fw', idx: stp.opts.findIndex(o => o.correct), nopts: stp.opts.length, si: mx.si, name: stp.name };
      const bi = stp.blanks.findIndex(b => !b.done);
      if (bi < 0) return { type: 'wait', si: mx.si };
      const b = stp.blanks[bi];
      const sibs = stp.blanks.filter((x, i) => b.grp && x.grp === b.grp && i !== bi && x.done).map(x => x.picked);
      return { type: 'fill', boxIdx: bi, ans: b.ansIds.slice(), grp: b.grp || null, sibs, si: mx.si };
    });
    if (process.env.DBG) console.log('    L3 guard#' + guard, JSON.stringify(info));
    if (info.type === 'fw') { await pickMixOpt(info.idx); continue; }
    if (info.type === 'wait') { await page.waitForTimeout(900); continue; }
    await page.locator(`.blank-box[data-blank-level="2"][data-blank-idx="${info.boxIdx}"]`).first().click({ force: true });
    await page.waitForTimeout(150);
    let pick = info.ans[0];
    if (info.grp && info.sibs.includes(pick)) pick = info.ans.find(a => !info.sibs.includes(a)) || info.ans[0];
    await clickUnit(pick);
    await page.waitForTimeout(220);
  }
  await page.waitForTimeout(1800);
  console.log('  第3关后:', JSON.stringify(await st()));

  // 第4关：交流微变等效（src保留 / vcc置零-接地 / caps短路 / re2移除 / re1保留 / rb1,rc 下移-并 / t等效 + TQUIZ）
  await pickByMenu('comp-src', '保留');
  await pickByMenu('comp-vcc', '置零', '接地');
  for (const c of ['comp-c1', 'comp-c2', 'comp-ce']) await pickByMenu(c, '短路');
  await pickByMenu('comp-re2', '移除');
  await pickByMenu('comp-re1', '保留');
  await pickByMenu('comp-rb1', '下移', '与RB2并');
  await pickByMenu('comp-rc', '下移', '与RL并');
  await page.waitForTimeout(400);
  await pickByMenu('comp-t', '等效');
  for (let k = 0; k < 8; k++) {
    const q = await page.evaluate(() => {
      const d = S.draw[3];
      if (!d.tquiz || d.tquiz.step >= TQUIZ.length) return null;
      return { ok: TQUIZ[d.tquiz.step].ok, step: d.tquiz.step };
    });
    if (!q) break;
    if (!(await menuClick(q.ok))) throw new Error(`第${q.step + 1} 问无选项「${q.ok}」`);
    await page.waitForTimeout(750);
  }
  await page.waitForTimeout(2200);
  console.log('  第4关后:', JSON.stringify(await st()));

  // 第5关：动态 mix
  for (let guard = 0; guard < 40; guard++) {
    const s = await st(); if (s.lvl !== 5) break;
    const info = await page.evaluate(() => {
      const mx = S.mix[S.level - 1], stp = mx.steps[mx.si];
      if (stp.type === 'fw') return { type: 'fw', idx: stp.opts.findIndex(o => o.correct) };
      const bi = stp.blanks.findIndex(b => !b.done);
      if (bi < 0) return { type: 'wait' };
      const b = stp.blanks[bi];
      const sibs = stp.blanks.filter((x, i) => b.grp && x.grp === b.grp && i !== bi && x.done).map(x => x.picked);
      return { type: 'fill', boxIdx: bi, ans: b.ansIds.slice(), grp: b.grp || null, sibs };
    });
    if (info.type === 'fw') { await pickMixOpt(info.idx); continue; }
    if (info.type === 'wait') { await page.waitForTimeout(900); continue; }
    await page.locator(`.blank-box[data-blank-level="4"][data-blank-idx="${info.boxIdx}"]`).first().click({ force: true });
    await page.waitForTimeout(150);
    let pick = info.ans[0];
    if (info.grp && info.sibs.includes(pick)) pick = info.ans.find(a => !info.sibs.includes(a)) || info.ans[0];
    await clickUnit(pick);
    await page.waitForTimeout(220);
  }
  await page.waitForTimeout(2200);

  const fin = await st();
  const per = await page.evaluate(() => S.levelScore.map(v => Math.round(v)));
  const declared = await page.evaluate(() => LEVELS.map(L => L.cfg.pts));
  const wantPts = [10, 16, 28, 16, 30];
  console.log('\n===== 结果 =====');
  console.log('  路线#' + ROUTE, '| finished =', fin.finished, '| score =', fin.score, '| pageerrors =', errs.length ? errs : 0);
  console.log('  逐关得分 =', per.join(' / '), '（合计', per.reduce((a, b) => a + b, 0), '）');
  const okPts = JSON.stringify(declared) === JSON.stringify(wantPts);
  const okPer = JSON.stringify(per) === JSON.stringify(wantPts);
  console.log('  分值声明 =', declared.join(' / '), okPts ? '' : '❌ 与 ' + wantPts.join(' / ') + ' 不符');
  const ok = fin.finished && fin.score === 100 && errs.length === 0 && okPts && okPer;
  console.log(ok ? `\n✅ 满分通关 100/100（路线#${ROUTE}）` : '\n❌ 未达满分');
  await browser.close();
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('ERR', e); process.exit(1); });
