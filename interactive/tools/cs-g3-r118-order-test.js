const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const dir = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';
const st = p => p.evaluate(() => { const s = window.getState(); return { score: s.score, found: Object.keys(s.draw[0].found), msg: s.msg && s.msg.text }; });
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run','--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  // 路径①：先信号源 → 再电源
  await p.goto(PAGE + '?lvl=1&cb=' + Date.now()); await p.waitForTimeout(400);
  await p.evaluate(() => chooseDrawOption('comp-vi', { act: 'vi-keep', ok: true })); await p.waitForTimeout(80);
  let a = await st(p);
  // 此时电容应仍锁定（点击不扣分、给门控提示）
  await p.evaluate(() => chooseDrawOption('comp-c1', { act: 'cap-short', ok: true })); await p.waitForTimeout(80);
  const locked = await st(p);
  await p.evaluate(() => chooseDrawOption('comp-vdd', { act: 'vcc-gnd', ok: true })); await p.waitForTimeout(80);
  await p.evaluate(() => chooseDrawOption('comp-c1', { act: 'cap-short', ok: true })); await p.waitForTimeout(80);
  const unlocked = await st(p);
  // 路径②：反向（电源先 → 信号源后）
  await p.goto(PAGE + '?lvl=1&cb=' + Date.now()); await p.waitForTimeout(400);
  await p.evaluate(() => chooseDrawOption('comp-vdd', { act: 'vcc-gnd', ok: true })); await p.waitForTimeout(80);
  const b1 = await st(p);
  await p.evaluate(() => chooseDrawOption('comp-c2', { act: 'cap-short', ok: true })); await p.waitForTimeout(80);
  const b1locked = await st(p);
  await p.evaluate(() => chooseDrawOption('comp-vi', { act: 'vi-keep', ok: true })); await p.waitForTimeout(80);
  await p.evaluate(() => chooseDrawOption('comp-c2', { act: 'cap-short', ok: true })); await p.waitForTimeout(80);
  const b2 = await st(p);
  await p.screenshot({ path: dir + '/cs-g3-r118-order.png' });
  console.log('①Vi先  ', JSON.stringify(a));
  console.log('  电容锁定', JSON.stringify(locked));
  console.log('  VDD后解锁', JSON.stringify(unlocked));
  console.log('②VDD先 ', JSON.stringify(b1));
  console.log('  电容锁定', JSON.stringify(b1locked));
  console.log('   Vi后解锁', JSON.stringify(b2));
  console.log('pageerrors=', errs.length, errs.slice(0, 2));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
