// cs-g1 任务1/2 验证截图：默认态 + 直流通路关 V_i 置零短路态
const { chromium } = require('playwright-core');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const URL = 'file:///F:/AI%E5%BB%BA%E8%AF%BE/%E6%A8%A1%E7%94%B5/WorkBuddy/%E7%BD%91%E7%AB%99/interactive/cs-g1.html';

(async () => {
    const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
    const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
    p.on('pageerror', e => console.log('PAGEERROR', e.message));
    await p.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30), cancel: () => {}, getVoices: () => [] };
        const o = window.setTimeout; window.setTimeout = (fn, ms) => o(fn, Math.min(ms || 0, 60));
    });
    await p.goto(URL + '?cb=' + Date.now(), { waitUntil: 'load' });
    await sleep(700);
    await p.screenshot({ path: '_shot_cs1v2/t1_default.png' });

    // 直流通路关：V_i 置零→短路（正确答案）
    await p.evaluate(() => {
        const cfg = LEVELS[0].cfg;
        const t = cfg.targets.find(x => x.id === 'comp-vi');
        const opt = t.menu[0].sub.find(x => x.act === 'vi-short');
        chooseDrawOption('comp-vi', opt);
    });
    await sleep(800);
    await p.screenshot({ path: '_shot_cs1v2/t1_vishort.png' });
    console.log('done');
    await b.close();
})();
