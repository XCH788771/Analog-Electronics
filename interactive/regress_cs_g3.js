// cs-g3 满分回归（双电源分压偏置共源·案例3）：Playwright 真实 UI 走正确路径，断言 score===100 && finished && pageerrors=0 && 重新挑战归零
// 答案一律运行时从页面内部状态读（TQUIZ[step].ok / fw 步 opts[i].correct / fill 空 blanks[bi].ansIds），不硬编码。
// 说明：q* 电量标注位于 fx-layer（pointer-events 受控），统一用 dispatchEvent 冒泡点击；
//       绘制关菜单必须 hover（dispatch mouseenter 等价链，见 regress_g3 注释）。
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const norm = s => String(s || '').replace(/[\s_]/g, '');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  // headless 无 TTS：脚本执行后轮询覆写 speakSeq（函数声明会覆盖 initScript 桩，须加载后补丁）
  await page.addInitScript(() => {
    const patch = () => {
      if (typeof window.speakSeq !== 'function') { setTimeout(patch, 30); return; }
      if (window.speakSeq.__orig) return;
      window.speakSeq = function (parts, onDone) {
        (parts || []).forEach(p => { if (p && p.onStart) { try { p.onStart(); } catch (e) {} } });
        if (onDone) { try { onDone(); } catch (e) {} }
      };
      window.speakSeq.__orig = true;
      setTimeout(patch, 30);   // 防后续声明覆盖
    };
    patch();
  });
  await page.goto(PAGE + '?cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(600);

  const st = () => page.evaluate(() => ({
    lvl: S.level, score: Math.round(S.score), finished: S.finished,
    per: Math.round(S.levelScore[S.level - 1]),
  }));
  const waitLvl = async target => {
    for (let k = 0; k < 40; k++) { const c = await st(); if (c.lvl === target) return; await page.waitForTimeout(250); }
    throw new Error('未到达 level=' + target + '，当前 ' + JSON.stringify(await st()));
  };

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
  const hoverUnit = async unitId => {
    const ok = await page.evaluate(id => {
      const g = document.querySelector(`#circuit-wrap g[data-id="${id}"]`);
      if (!g) return false;
      try { hideMenu(); } catch (e) {}
      g.dispatchEvent(new MouseEvent('mouseenter', { bubbles: false }));
      return true;
    }, unitId);
    if (!ok) throw new Error('无此元件 ' + unitId);
    await page.waitForTimeout(220);
  };
  // 路径容错：[[一级, 二级], [一级]]——第一组全中则用之，否则试第二组；过场期自动重试
  async function pick(unitId, paths) {
    for (let attempt = 0; attempt < 6; attempt++) {
      for (const p of paths) {
        await hoverUnit(unitId);
        let ok = true;
        for (const t of p) { if (!(await menuClick(t))) { ok = false; break; } }
        if (ok) return;
      }
      await page.waitForTimeout(800);
    }
    throw new Error(unitId + ' 无可用菜单路径 ' + JSON.stringify(paths));
  }
  const clickUnit = id => page.evaluate(i => {
    const g = document.querySelector(`#circuit-wrap g[data-id="${i}"]`);
    if (!g) throw new Error('无此单元 ' + i);
    g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  }, id);

  // ===== 第 1 关 · 直流通路（gate：三电源先行） =====
  await pick('comp-src', [['置零', '短路'], ['短路']]);
  await pick('comp-vdd', [['保留']]);
  await pick('comp-vss', [['保留']]);
  await pick('comp-cb1', [['断路']]);
  await pick('comp-cb2', [['断路']]);
  await waitLvl(2);
  c = await st();
  const p1 = await page.evaluate(() => Math.round(S.levelScore[0]));
  console.log('L1 done: per=' + p1 + ' score=' + c.score);
  if (p1 !== 20) throw new Error('L1 应得 20 分，实得 ' + p1);
  await page.waitForTimeout(600);

  // ===== 第 2 关 · 交流微变等效（通路→整理→等效四问） =====
  await pick('comp-src', [['保留']]);
  await pick('comp-vdd', [['置零', '接地']]);
  await pick('comp-vss', [['置零', '接地']]);
  await pick('comp-cb1', [['短路']]);
  await pick('comp-cb2', [['短路']]);
  await pick('comp-rg1', [['下移', '与RG2并']]);
  await pick('comp-rd', [['下移', '与输出并']]);
  await pick('comp-t', [['等效']]);
  const nq = await page.evaluate(() => TQUIZ.length);
  for (let k = 0; k < nq; k++) {
    const okAns = await page.evaluate(() => TQUIZ[S.draw[S.level - 1].tquiz.step].ok);
    if (!(await menuClick(okAns))) throw new Error('TQUIZ 第' + (k + 1) + '问菜单无「' + okAns + '」');
    await page.waitForTimeout(1400);
  }
  await waitLvl(3);
  c = await st();
  const p2 = await page.evaluate(() => Math.round(S.levelScore[1]));
  console.log('L2 done: per=' + p2 + ' score=' + c.score);
  if (p2 !== 20) throw new Error('L2 应得 20 分，实得 ' + p2);
  await page.waitForTimeout(600);

  // ===== 第 3 关 · 动态指标（3 框架 + 填空；先点虚线框再点元件） =====
  const clicked = {};
  for (let guard = 0; guard < 12; guard++) {
    const cur = await page.evaluate(() => {
      const mx = S.mix[S.level - 1]; if (!mx) return null;
      const s = mx.steps[mx.si]; if (!s) return null;
      if (s.type === 'fw') return s.solved ? null : { kind: 'fw' };
      const bi = s.blanks.findIndex(b => !b.done);
      if (bi < 0) return null;
      const b = s.blanks[bi];
      return { kind: 'fill', ansIds: b.ansIds, grp: b.grp || null };
    });
    if (!cur) break;
    if (cur.kind === 'fw') {
      const idx = await page.evaluate(() => S.mix[S.level - 1].steps[S.mix[S.level - 1].si].opts.findIndex(o => o.correct));
      if (idx < 0) throw new Error('fw 步无 correct 项');
      await page.locator('.g-opt').nth(idx).click({ force: true });
      await page.waitForTimeout(1900);
    } else {
      await page.locator('.blank-box[data-blank-level="2"]:not(.done)').first().click({ force: true });
      await page.waitForTimeout(280);
      const ans = cur.ansIds.find(id => !cur.grp || !clicked[id]) || cur.ansIds[0];
      clicked[ans] = true;
      await clickUnit(ans);
      await page.waitForTimeout(1900);
    }
  }
  c = await st();
  console.log('L3 done: per=' + c.per + ' score=' + c.score + ' finished=' + c.finished);
  for (let k = 0; k < 30; k++) { const w = await st(); if (w.finished) break; await page.waitForTimeout(300); }
  c = await st();
  if (!(c.score === 100 && c.finished)) throw new Error('应满分通关，实得 ' + JSON.stringify(c));
  console.log('FINISHED: score=' + c.score);

  // ===== 重新挑战归零 =====
  await page.getByText('重新挑战').click();
  await page.waitForTimeout(800);
  c = await st();
  if (!(c.score === 0 && c.lvl === 1 && !c.finished)) throw new Error('重新挑战未归零：' + JSON.stringify(c));
  console.log('RESTART-OK');

  if (errs.length) { console.log('PAGEERRORS:', JSON.stringify(errs, null, 2)); await browser.close(); process.exit(1); }
  await browser.close();
  console.log('REGRESS-PASS');
})();
