// 对比截图：cs-g1 / cs-g3 默认态（判断两页电路是否互换）
const { chromium } = require('playwright-core');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/cmp';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
    const fs = require('fs');
    if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
    for (const id of ['cs-g1', 'cs-g3']) {
        const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
        await page.addInitScript(() => {
            window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        });
        const errs = [];
        page.on('pageerror', e => errs.push(e.message));
        await page.goto('file:///F:/AI建课/模电/WorkBuddy/网站/interactive/' + id + '.html', { waitUntil: 'load' });
        await sleep(1200);
        // 关掉开场遮罩（若有）
        const btn = await page.$('#start-btn, .start-btn, #btn-start');
        if (btn) { await btn.click().catch(() => {}); await sleep(1200); }
        await page.screenshot({ path: OUT + '/' + id + '-default.png' });
        // 提取页面文案要点
        const info = await page.evaluate(() => {
            const t = s => { const e = document.querySelector(s); return e ? e.textContent.trim().slice(0, 200) : null; };
            return {
                title: document.title,
                h1: t('h1'), sub: t('.subtitle, .sub, #subtitle'),
                known: t('.known, #known, .known-line'),
                stage: t('#stage-text, .stage-text'),
                ids: Array.from(document.querySelectorAll('svg [data-id]')).map(e => e.getAttribute('data-id'))
            };
        });
        console.log('=== ' + id + ' ===');
        console.log('title:', info.title);
        console.log('sub:', info.sub);
        console.log('known:', info.known);
        console.log('ids:', info.ids.join(' '));
        console.log('errs:', errs.length ? errs : 'none');
        await page.close();
    }
    await browser.close();
})();
