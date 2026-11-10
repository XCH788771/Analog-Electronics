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
  // 1) 默认态
  await p.goto(PAGE + '?cb=' + Date.now());
  await p.waitForTimeout(600);
  await p.screenshot({ path: dir + '/cs-g3-r117-default.png' });
  // 2) 整理+等效态
  await p.goto(PAGE + '?lvl=1&tidy=1&ts=1&cb=' + Date.now());
  await p.waitForTimeout(600);
  await p.screenshot({ path: dir + '/cs-g3-r117-tidy.png' });
  // 3) 整理后 reset 恢复（验证 rg2a 全长复现 / node-drain 复现 / 标签归位）
  await p.evaluate(() => resetCircuit());
  await sleep(300);
  const chk = await p.evaluate(() => ({
    rg2a: document.querySelector('g[data-id="wire-rg2a"] path').getAttribute('d'),
    ndOp: document.getElementById('node-drain').style.opacity,
    lbl: (t => [t.getAttribute('x'), t.getAttribute('y'), t.getAttribute('text-anchor')].join(','))(document.querySelector('.rg2-label')),
  }));
  await p.screenshot({ path: dir + '/cs-g3-r117-reset.png' });
  console.log('CHK', JSON.stringify(chk), 'pageerrors=', errs.length);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
