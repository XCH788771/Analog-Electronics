const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const dir = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run','--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await p.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  const shots = [['default', ''], ['tidy', '?lvl=1&tidy=1'], ['ts1', '?lvl=1&tidy=1&ts=1'], ['ts2', '?lvl=1&tidy=1&ts=2'],
                 ['ts3', '?lvl=1&tidy=1&ts=3'], ['ts4', '?lvl=1&tidy=1&ts=4'], ['ts5', '?lvl=1&tidy=1&ts=5'], ['ts6', '?lvl=1&tidy=1&ts=6']];
  for (const [name, qs] of shots) {
    await p.goto(PAGE + qs + (qs ? '&' : '?') + 'cb=' + Date.now());
    await p.waitForTimeout(650);
    await p.screenshot({ path: dir + '/cs-g3-r119-' + name + '.png' });
  }
  console.log('pageerrors=', errs.length, errs.slice(0, 3));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
