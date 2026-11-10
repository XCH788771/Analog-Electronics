const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run','--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  const dir = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';
  await p.goto(PAGE + '?cb=' + Date.now());
  await p.waitForTimeout(600);
  await p.screenshot({ path: dir + '/cs-g3-cur-default.png' });
  // L1 tidy+equiv
  await p.goto(PAGE + '?lvl=1&tidy=1&ts=0&cb=' + Date.now());
  await p.waitForTimeout(600);
  await p.screenshot({ path: dir + '/cs-g3-cur-l1.png' });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await b.close();
  console.log('shots done; pageerrors=', errs.length);
})().catch(e => { console.error(e); process.exit(1); });
