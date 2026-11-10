// cs-g1 截图目检脚本（Playwright + 系统 Chrome）
// 覆盖：默认态、L1 整理+等效、L1 TQUIZ 五态、L2 Av 框架/填空、L3 Ri/Ro 框架/填空
// 运行：node 网站/interactive/tools/cs-g1-shot.js  输出到 网站/interactive/assets/shots/
const { chromium } = require('playwright-core');

const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';
const sleep = ms => new Promise(r => setTimeout(r, ms));

// 各截图参数（查询串）
const SHOTS = [
    ['default', ''],
    ['l1', '?lvl=1'],
    ['l1-tidy', '?lvl=1&tidy=1'],
    ['l1-ts1', '?lvl=1&ts=1'],
    ['l1-ts2', '?lvl=1&ts=2'],
    ['l1-ts3', '?lvl=1&ts=3'],
    ['l1-ts4', '?lvl=1&ts=4'],
    ['l1-ts5', '?lvl=1&ts=5'],
    ['l1-ts6', '?lvl=1&ts=6'],
    ['l2', '?lvl=2'],
    ['l2-fill', '?lvl=2&ms=2'],
    ['l3', '?lvl=3'],
    ['l3-ri-fill', '?lvl=3&ms=2'],
    ['l3-ro-fw', '?lvl=3&ms=3'],
    ['l3-ro-fill', '?lvl=3&ms=4']
];

(async () => {
    const fs = require('fs');
    if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({
        executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'],
    });
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    page.on('pageerror', e => console.log('PAGEERROR:', e.message));
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        const oST = window.setTimeout;
        window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
    });
    for (const [name, q] of SHOTS) {
        await page.goto(PAGE + (q ? q + '&' : '?') + 'cb=' + Date.now());
        await page.waitForTimeout(700);
        const path = OUT + '/cs-g1-' + name + '.png';
        await page.screenshot({ path, fullPage: false });
        console.log('shot:', name);
    }
    await browser.close();
    console.log('CS-G1-SHOTS-DONE');
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
