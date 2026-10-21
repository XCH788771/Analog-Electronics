// r92 诊断：三种整理顺序的导线连通 + −V_EE 文字隐藏
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

  const setup = async () => {
    await page.goto(PAGE + '?lvl=4&cb=' + Date.now(), { waitUntil: 'load' });
    await page.waitForTimeout(800);
    await page.evaluate(() => {
      const d4 = S.draw[3];
      execAct('comp-src', 'vs-keep'); d4.found['comp-src'] = true;
      execAct('comp-vcc', 'vcc-gnd'); d4.found['comp-vcc'] = true;
      execAct('comp-vee', 'vee-gnd'); d4.found['comp-vee'] = true;
      execAct('comp-c1', 'cap-short'); d4.found['comp-c1'] = true;
      execAct('comp-c2', 'cap-short'); d4.found['comp-c2'] = true;
      execAct('comp-ce', 'cap-short'); d4.found['comp-ce'] = true;
    });
    await page.waitForTimeout(400);
  };
  const probe = async () => page.evaluate(() => {
    const op = id => { const el = document.querySelector('#circuit-wrap g[data-id="' + id + '"]') || document.getElementById(id); return el ? getComputedStyle(el).opacity : 'missing'; };
    const vee = document.querySelector('.vee-label');
    return { veeLabelOp: vee ? vee.style.visibility + '/' + vee.style.opacity : 'none',
             re1Op: op('comp-re1'), ceOp: op('comp-ce'), ceB: op('wire-ce-b'), fxCe: op('fx-ce'), fxTail: op('fx-ce-tail'),
             base: op('wire-base'), baseIn: op('wire-base-in'), nodeBase: op('node-base'), vcc: op('comp-vcc') };
  });
  const shot = (n, clip) => page.screenshot({ path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/' + n, clip });

  // 场景0：仅置零/短路后（未整理）—— 验证 −V_EE 文字隐藏
  await setup();
  console.log('置零后:', JSON.stringify(await probe()));
  await shot('r92_step0.png', { x: 0, y: 150, width: 950, height: 700 });

  // 场景A：先整理 R_C
  await page.evaluate(() => { moveCompDown('comp-rc'); });
  await page.waitForTimeout(600);
  console.log('A 先RC:', JSON.stringify(await probe()));
  await shot('r92_stepA.png', { x: 0, y: 150, width: 950, height: 700 });
  await shot('r92_stepA_emitter.png', { x: 340, y: 480, width: 360, height: 260 });
  await shot('r92_stepA_base.png', { x: 40, y: 380, width: 460, height: 140 });

  // 场景B：再整理 RE2（移除）
  await page.evaluate(() => { execAct('comp-re2', 're2-remove'); S.draw[3].found['comp-re2'] = true; });
  await page.waitForTimeout(600);
  console.log('B 再RE2:', JSON.stringify(await probe()));
  await shot('r92_stepB.png', { x: 0, y: 150, width: 950, height: 700 });
  await shot('r92_stepB_emitter.png', { x: 340, y: 440, width: 420, height: 320 });

  // 场景C（另开页面）：先 RE1 保留、再 RE2 移除
  await setup();
  await page.evaluate(() => { execAct('comp-re1', 're1-keep'); S.draw[3].found['comp-re1'] = true; });
  await page.waitForTimeout(400);
  await page.evaluate(() => { execAct('comp-re2', 're2-remove'); S.draw[3].found['comp-re2'] = true; });
  await page.waitForTimeout(600);
  console.log('C 先RE1再RE2:', JSON.stringify(await probe()));
  await shot('r92_stepC.png', { x: 0, y: 150, width: 950, height: 700 });
  await shot('r92_stepC_emitter.png', { x: 340, y: 440, width: 420, height: 320 });

  console.log('pageerrors:', errs.length, errs.slice(0, 2));
  await browser.close(); process.exit(0);
})();
