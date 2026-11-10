// cs-g1 全状态截图脚本（Playwright + 系统 Chrome）
// 运行：NODE_PATH=<pw-core 目录> node _src_cs1/_shot_cs1.js
const { chromium } = require('playwright-core');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const BASE = 'http://127.0.0.1:8765/interactive/cs-g1.html';
const OUT = __dirname + '/../_shot_cs1';
const sleep = ms => new Promise(r => setTimeout(r, ms));

const SHOTS = [
  ['l1_default', '', null],
  ['l1_tidy', '?lvl=1&tidy=1', null],
  ['l1_ts1', '?lvl=1&ts=1', null],
  ['l1_ts2', '?lvl=1&ts=2', null],
  ['l1_ts3', '?lvl=1&ts=3', null],
  ['l1_ts4', '?lvl=1&ts=4', null],
  ['l1_ts5', '?lvl=1&ts=5', null],
  ['l2_fw', '?lvl=2&eq=1', null],
  ['l2_fill', '?lvl=2&eq=1&ms=2', null],
  ['l3_fw', '?lvl=3&eq=1', null],
  ['l3_fill', '?lvl=3&eq=1&ms=2', null],
  ['l4_fw', '?lvl=4&eq=1', null],
  ['l4_fill', '?lvl=4&eq=1&ms=2', null],
  ['done', '?lvl=done', null],
  // 局部放大：等效电路区（含菱形受控源 / vgs / gm / 红点）
  ['zoom_eq', '?lvl=1&ts=5', { x: 480, y: 380, width: 460, height: 460 }],
  ['zoom_eq2', '?lvl=1&ts=4', { x: 480, y: 380, width: 460, height: 460 }],
  ['zoom_mos', '', { x: 480, y: 380, width: 460, height: 460 }],
  ['zoom_vo', '', { x: 700, y: 380, width: 300, height: 260 }],
];

(async () => {
  const fs = require('fs');
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--force-color-profile=srgb'] });
  const errors = [];
  for (const [name, q, clip] of SHOTS) {
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    page.on('pageerror', e => errors.push(name + ' pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(name + ' console: ' + m.text()); });
    await page.addInitScript(() => {
      window.speakSeq = function (parts, onDone) {
        (parts || []).forEach(p => { if (p.onStart) try { p.onStart(); } catch (e) {} });
        if (onDone) try { onDone(); } catch (e) {}
      };
    });
    await page.goto(BASE + q);
    await page.waitForTimeout(900);
    await page.screenshot({ path: OUT + '/' + name + '.png', clip: clip || undefined });
    await page.close();
    console.log('shot:', name);
  }
  await browser.close();
  if (errors.length) { console.log('!! 页面错误:'); errors.forEach(e => console.log('  -', e)); process.exit(1); }
  console.log('全部截图完成，无页面错误');
})().catch(e => { console.error(e); process.exit(1); });
