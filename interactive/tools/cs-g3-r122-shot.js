const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const dir = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run','--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await p.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  const tag = process.argv[2] || 'r122';
  const base = ['comp-vdd:vcc-gnd', 'comp-vi:vi-keep', 'comp-c1:cap-short', 'comp-c2:cap-short', 'comp-cs:cap-short', 'comp-rs:rs-remove'];
  const drive = (extra) => p.evaluate(({ base, extra }) => {
    base.forEach(s => { const [id, act] = s.split(':'); chooseDrawOption(id, { act, ok: true }); });
    extra.forEach(id => chooseMoveOption(id, true));
  }, { base, extra });

  // A: 仅 RG1 下移
  await p.goto(PAGE + '?cb=' + Date.now()); await p.waitForTimeout(600);
  await drive(['comp-rg1']); await p.waitForTimeout(300);
  await p.screenshot({ path: dir + '/cs-g3-' + tag + '-rg1only.png' });

  // B: 仅 RD 下移
  await p.goto(PAGE + '?cb=' + Date.now()); await p.waitForTimeout(600);
  await drive(['comp-rd']); await p.waitForTimeout(300);
  await p.screenshot({ path: dir + '/cs-g3-' + tag + '-rdonly.png' });

  // C: 两者都下移
  await p.goto(PAGE + '?cb=' + Date.now()); await p.waitForTimeout(600);
  await drive(['comp-rg1', 'comp-rd']); await p.waitForTimeout(300);
  await p.screenshot({ path: dir + '/cs-g3-' + tag + '-both.png' });

  // D: 等效完成
  await p.goto(PAGE + '?cb=' + Date.now()); await p.waitForTimeout(600);
  await drive(['comp-rg1', 'comp-rd']);
  await p.evaluate(() => chooseDrawOption('comp-t', { act: 't-equiv', ok: true }));
  await p.waitForTimeout(200);
  for (const a of ['开路', '上＋下－', '开路', '受控源', '↓i_d']) {
    await p.evaluate(ans => {
      const q = window.__TQ; if (!q) return;
    }, a);
  }
  // 用 ?ts=6 单独走一遍完成态
  await p.goto(PAGE + '?lvl=1&tidy=1&ts=6&cb=' + Date.now()); await p.waitForTimeout(700);
  await p.screenshot({ path: dir + '/cs-g3-' + tag + '-ts6.png' });

  console.log('pageerrors=', errs.length, errs.slice(0, 3));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
