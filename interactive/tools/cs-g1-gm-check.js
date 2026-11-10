// cs-g1：验证 ①第3关等效完成态箭头旁 g_m·v_gs 恢复 ②第4关红色 g_m 在受控源右侧、不与 v_gs 重叠
const { chromium } = require('playwright-core');
const path = require('path');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots/';

(async () => {
    const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true, args: ['--no-first-run'] });
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 60));
    });
    const cls = await browser.newPage({ viewport: { width: 1600, height: 900 } });

    await page.goto(PAGE + '?lvl=3&ts=6&cb=' + Date.now());
    await page.waitForTimeout(900);

    const l3 = await page.evaluate(() => {
        const box = id => { const e = document.querySelector(id); if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
        const op = id => { const e = document.getElementById(id); return e ? getComputedStyle(e).opacity : null; };
        const label = document.querySelector('#fx-t-idlabel text');
        return {
            idLabelOp: op('fx-t-idlabel'),
            idLabelText: label ? label.textContent.trim() : null,
            idLabelXY: label ? label.getAttribute('x') + ',' + label.getAttribute('y') : null,
            idLabelBox: box('#fx-t-idlabel text'),
            vgsBox: box('#fx-t-vgs text:nth-of-type(2)'),
            qlabelLayerOp: getComputedStyle(document.getElementById('qlabel-layer')).opacity,
            gmTextX: (document.querySelector('[data-id="q-gm"] .hot-label') || {}).getAttribute ? document.querySelector('[data-id="q-gm"] .hot-label').getAttribute('x') : null
        };
    });
    console.log('L3-done', JSON.stringify(l3));

    // 进第 4 关
    const l4 = await page.evaluate(() => {
        try { completeLevel(); } catch (e) { return { err: String(e) }; }
        const box = id => { const e = document.querySelector(id); if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
        const g = document.querySelector('[data-id="q-gm"]');
        const st = g ? getComputedStyle(g) : null;
        const txt = g ? g.querySelector('.hot-label') : null;
        return {
            level: S.level,
            gmVisible: st ? st.opacity : null,
            gmPE: st ? st.pointerEvents : null,
            gmXY: txt ? txt.getAttribute('x') + ',' + txt.getAttribute('y') : null,
            gmBox: box('[data-id="q-gm"] .hot-label'),
            vgsBox: box('#fx-t-vgs text:nth-of-type(2)'),
            diamondBox: box('#fx-t-src path'),
            idLabelOp: getComputedStyle(document.getElementById('fx-t-idlabel')).opacity,
            rdLineBox: box('#rarr-rd')
        };
    });
    console.log('L4', JSON.stringify(l4));
    await page.waitForTimeout(500);
    await page.screenshot({ path: OUT + 'gm-l4.png' });

    // 回到第 3 关完成态截图
    await page.goto(PAGE + '?lvl=3&ts=6&cb=' + Date.now());
    await page.waitForTimeout(900);
    await page.screenshot({ path: OUT + 'gm-l3done.png' });
    await browser.close();
    console.log('GM-CHECK-DONE');
})();
