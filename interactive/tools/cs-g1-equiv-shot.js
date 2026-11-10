// cs-g1 等效态各问目检截图（源极直落地 / g-s 同轴 / v_gs 重排 / 受控源下移 / g_m·v_gs 标注）
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
    const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    page.on('pageerror', e => console.log('PAGEERROR:', e.message));
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        const oST = window.setTimeout;
        window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 60));
    });
    for (const tv of [1, 2, 4, 5, 6]) {   // 五问：1=极性问、2=GS开路后、4=前3问、5=DS受控源后(第5问选项)、6=完成
        await page.goto(PAGE + '?lvl=3&ts=' + tv + '&cb=' + Date.now());
        await page.waitForTimeout(900);
        // 几何断言
        const g = await page.evaluate(() => {
            const box = s => { const e = document.querySelector(s); return e ? e.getBBox() : null; };
            const cx = s => { const e = document.querySelector(s); return e ? e.getAttribute('cx') + ',' + e.getAttribute('cy') : null; };
            const op = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).opacity : null; };
            const txt = s => { const e = document.querySelector(s); return e ? e.textContent.trim() : null; };
            return {
                dotG: cx('#fx-dot-g circle'), dotS: cx('#fx-dot-s circle'), dotD: cx('#fx-dot-d circle'),
                opVgs: op('#fx-t-vgs'), opSrc: op('#fx-t-src'), opId: op('#fx-t-id'),
                opIdLabel: op('#fx-t-idlabel'), idText: txt('#fx-t-idlabel text'),
                srcText: document.querySelectorAll('#fx-t-src text').length,
                vgsBox: box('#fx-t-vgs'),
                idBox: box('#fx-t-id text'),
                rdTopBox: box('#rarr-rd'),
                menu: Array.from(document.querySelectorAll('#ctxmenu .mi')).map(x => x.textContent.trim()),
                greenBridge: document.querySelectorAll('#eq-layer line[stroke="#34d399"]').length,
                gmText: (function () { const g = document.querySelectorAll('#fx-t-idlabel text'); return g.length ? g[0].textContent.trim() + '@' + g[0].getAttribute('x') + ',' + g[0].getAttribute('y') + '/' + g[0].getAttribute('fill') : null; })(),
                srcText: document.querySelectorAll('#fx-t-src text').length
            };
        });
        console.log('ts=' + tv, JSON.stringify(g));
        await page.screenshot({ path: OUT + '/eq-ts' + tv + '.png' });
    }
    await browser.close();
    console.log('EQUIV-SHOTS-DONE');
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
