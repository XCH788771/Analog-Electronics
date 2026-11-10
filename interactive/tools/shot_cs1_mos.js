// cs-g1 场效应管符号特写（放大 viewBox 到 comp-t 区域，逐项核对几何）
const { chromium } = require('playwright-core');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/cmp';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
    const fs = require('fs');
    if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
    const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.goto('file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html?cb=' + Date.now(), { waitUntil: 'load' });
    await sleep(1000);
    const btn = await page.$('#start-btn, .start-btn, #btn-start');
    if (btn) { await btn.click().catch(() => {}); await sleep(1200); }

    // 全页默认态
    await page.screenshot({ path: OUT + '/cs-g1-mos-full.png' });

    // 放大 comp-t 区域：读 circuit-wrap 的 translate，把 comp-t 局部 bbox 换算到根坐标
    const box = await page.evaluate(() => {
        const svg = document.querySelector('svg.circuit');
        svg.setAttribute('data-viewbox-backup', svg.getAttribute('viewBox'));
        const wrap = document.getElementById('circuit-wrap') || document.querySelector('[id^="circuit-wrap"]');
        const m = (wrap.getAttribute('transform') || '').match(/translate\(\s*([-\d.]+)[ ,]+([-\d.]+)\s*\)/);
        const tx = m ? +m[1] : 0, ty = m ? +m[2] : 0;
        const b = document.querySelector('g[data-id="comp-t"]').getBBox();
        const pad = 34;
        const x = b.x + tx - pad, y = b.y + ty - pad, w = b.width + pad * 2, h = b.height + pad * 2;
        svg.setAttribute('viewBox', x + ' ' + y + ' ' + w + ' ' + h);
        return { x, y, w, h, wrap: wrap.getAttribute('transform') };
    });
    console.log('zoom box:', JSON.stringify(box));
    await sleep(400);
    await page.screenshot({ path: OUT + '/cs-g1-mos-zoom.png' });

    // 量取实际几何（供数值核对）
    const geo = await page.evaluate(() => {
        const g = document.querySelector('g[data-id="comp-t"]');
        const out = [];
        g.querySelectorAll('line,path,polygon,circle,text').forEach(el => {
            const tag = el.tagName.toLowerCase();
            if (tag === 'text') out.push({ t: 'text', v: el.textContent.trim(), x: el.getAttribute('x'), y: el.getAttribute('y') });
            else if (tag === 'line') out.push({ t: 'line', y1: el.getAttribute('y1'), y2: el.getAttribute('y2'), x1: el.getAttribute('x1'), x2: el.getAttribute('x2') });
            else if (tag === 'path') out.push({ t: 'path', d: el.getAttribute('d') });
            else if (tag === 'polygon') out.push({ t: 'polygon', p: el.getAttribute('points') });
            else out.push({ t: 'circle', cx: el.getAttribute('cx'), cy: el.getAttribute('cy'), r: el.getAttribute('r') });
        });
        return out;
    });
    console.log(JSON.stringify(geo, null, 1));
    console.log('errs:', errs.length ? errs : 'none');
    await browser.close();
})();
