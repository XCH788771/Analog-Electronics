// cs-g3 第126轮断言：等效态整图上移 30px（translate y 260→230），复位归位
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/archive/r126';
const fs = require('fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 2 });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.addInitScript(() => { window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30), cancel: () => {}, getVoices: () => [] }; });
  await page.goto(PAGE + '?lvl=1&tidy=1&ts=6&cb=' + Date.now());
  await sleep(900);
  const eq = await page.evaluate(() => {
    const m = getComputedStyle(document.getElementById('circuit-wrap')).transform;
    const r = document.querySelector('svg.circuit').getBoundingClientRect();
    const top = document.querySelector('g[data-id="wire-vdd-rail"] path').getBoundingClientRect();
    return { transform: m, svgTop: r.top, railTop: top.top };
  });
  await page.screenshot({ path: OUT + '/equiv-shift.png' });
  const back = await page.evaluate(() => { resetCircuit(); return getComputedStyle(document.getElementById('circuit-wrap')).transform; });
  await page.screenshot({ path: OUT + '/reset-shift.png' });
  console.log('等效态 transform:', eq.transform, '| svgTop:', eq.svgTop, '| 顶轨屏幕 y:', eq.railTop);
  console.log('复位 transform:', back);
  const ok = [], bad = [];
  const A = (c, m) => (c ? ok : bad).push(m);
  A(/,\s*230\)/.test(eq.transform), '等效态 translate y=230（上移30）: ' + eq.transform);
  A(/,\s*260\)/.test(back), '复位 translate y=260: ' + back);
  A(errors.length === 0, '无页面错误: ' + errors.join(' | '));
  console.log('通过: ' + ok.length + ' / 失败: ' + bad.length);
  bad.forEach(x => console.log('  ✗ ' + x));
  console.log(bad.length === 0 ? 'CS-G3-R126-OK' : 'CS-G3-R126-FAIL');
  await browser.close();
})();
