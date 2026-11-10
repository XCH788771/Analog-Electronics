// cs-g1 逐关截图目检：?lvl=1 / ?lvl=2 / ?tidy=1 / &ts=1..4 / &ts=5(完成) / ?lvl=3 / ?lvl=done
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const OUT = 'F:/AI建课/模电/WorkBuddy/.workbuddy/tmp_csg1/';
const SHOTS = [
  ['01-lvl1', '?lvl=1'],
  ['02-lvl2-ac', '?lvl=2'],
  ['03-lvl2-tidy', '?lvl=2&tidy=1'],
  ['04-ts1', '?lvl=2&tidy=1&ts=1'],
  ['05-ts2', '?lvl=2&tidy=1&ts=2'],
  ['06-ts3', '?lvl=2&tidy=1&ts=3'],
  ['07-ts4', '?lvl=2&tidy=1&ts=4'],
  ['08-ts5-done', '?lvl=2&tidy=1&ts=5'],
  ['09-lvl3-mix', '?lvl=3'],
  ['10-done', '?lvl=done'],
];

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  for (const [name, qs] of SHOTS) {
    await page.goto(PAGE + qs + '&cb=' + Date.now(), { waitUntil: 'load' });
    await page.waitForTimeout(900);
    await page.screenshot({ path: OUT + 'shot-' + name + '.png' });
    console.log('shot:', name);
  }
  if (errs.length) { console.log('PAGEERRORS:', JSON.stringify(errs, null, 2)); await browser.close(); process.exit(1); }
  await browser.close(); console.log('ALL-SHOTS-OK');
})();
