// cs-g1 第 2 关 I_DQ 标注（箭头+文字）上移 20px 目检
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';

(async () => {
    const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    page.on('pageerror', e => console.log('PAGEERROR:', e.message));
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        const oST = window.setTimeout;
        window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 60));
    });
    await page.goto(PAGE + '?lvl=2&cb=' + Date.now());
    await page.waitForTimeout(900);
    const g = await page.evaluate(() => {
        const grp = document.querySelector('[data-id="q-idq"]');
        const b = grp.getBBox();
        const line = grp.querySelector('line');
        const poly = grp.querySelector('polygon');
        const txt = grp.querySelector('text');
        return {
            bbox: [b.x, b.y, b.width, b.height].map(v => Math.round(v)),
            line: line.getAttribute('y1') + '-' + line.getAttribute('y2'),
            polyTop: poly.getAttribute('points'),
            textY: txt.getAttribute('y'),
            hot: (function () { const r = grp.querySelector('rect'); return r.getAttribute('x') + ',' + r.getAttribute('y'); })()
        };
    });
    console.log('q-idq =', JSON.stringify(g));
    await page.screenshot({ path: OUT + '/l2-idq.png' });
    // 特写（漏极区）
    await page.screenshot({ path: OUT + '/l2-idq-zoom.png', clip: { x: 190, y: 90, width: 640, height: 420 } });
    await browser.close();
    console.log('IDQ-SHOT-DONE');
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
