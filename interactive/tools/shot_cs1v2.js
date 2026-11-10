// cs-g1（单电源重绘版）全状态截图
const { chromium } = require('playwright-core');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/_shot_cs1v2';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const URL = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';

const SHOTS = [
    ['l1_default', '?cb=1'],
    ['l2_fw1', '?lvl=2&ms=1&cb=1'],
    ['l2_fill1', '?lvl=2&ms=2&cb=1'],
    ['l2_fill4', '?lvl=2&ms=4&cb=1'],
    ['l3_tidy', '?lvl=3&tidy=1&cb=1'],
    ['l3_ts5', '?lvl=3&ts=5&cb=1'],
    ['l4_fw', '?lvl=4&ms=1&cb=1'],
    ['l4_fill', '?lvl=4&ms=2&cb=1'],
    ['done', '?lvl=done&cb=1'],
];

(async () => {
    const fs = require('fs');
    if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
    for (const [name, q] of SHOTS) {
        const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
        await page.addInitScript(() => {
            window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        });
        const errs = [];
        page.on('pageerror', e => errs.push(e.message));
        await page.goto(URL + q, { waitUntil: 'load' });
        await sleep(1400);
        await page.screenshot({ path: OUT + '/' + name + '.png' });
        console.log(name + (errs.length ? '  ERRS: ' + errs.join(' | ') : '  ok'));
        await page.close();
    }
    await browser.close();
})();
