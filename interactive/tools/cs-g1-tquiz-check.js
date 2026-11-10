const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  for (let n = 1; n <= 5; n++) {
    await p.goto(PAGE + '?lvl=1&ts=' + n + '&cb=' + Date.now());
    await p.waitForTimeout(500);
    const info = await p.evaluate(() => {
      const mi = Array.from(document.querySelectorAll('#ctxmenu .mi')).map(d => d.textContent.trim());
      const q = (document.querySelector('#msg') || {}).textContent || '';
      return { mi, q: q.slice(0, 36) };
    });
    console.log('ts=' + n, 'menuItems=', JSON.stringify(info.mi), 'msg=', info.q);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
