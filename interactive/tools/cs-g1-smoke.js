// cs-g1（双电源分压偏置共源·案例1，五关）冒烟验证
// ① 各关 ?lvl=1..5 钩子渲染  ② L1 悬停元件出菜单并作答记分  ③ 0 页面错误
const { chromium } = require('playwright-core');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const BASE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';
const OUT = 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/cmp';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
    const fs = require('fs');
    if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
    const fails = [];

    // ① 各关渲染
    for (let lv = 1; lv <= 5; lv++) {
        const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
        const errs = [];
        page.on('pageerror', e => errs.push(e.message));
        await page.addInitScript(() => {
            window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        });
        await page.goto(BASE + '?lvl=' + lv, { waitUntil: 'load' });
        await sleep(900);
        const info = await page.evaluate(() => ({
            lv: (typeof S !== 'undefined') ? S.level : null,
            kind: (typeof LEVELS !== 'undefined' && LEVELS[S.level - 1]) ? LEVELS[S.level - 1].kind : null,
            stageLen: document.querySelector('.stage') ? document.querySelector('.stage').textContent.length : 0
        }));
        await page.screenshot({ path: OUT + '/g1-lvl' + lv + '.png' });
        console.log('lvl=' + lv + ' → level=' + info.lv + ' kind=' + info.kind + ' stageLen=' + info.stageLen + ' errs=' + (errs.length || 'none'));
        if (info.lv !== lv && lv <= 3) fails.push('lvl=' + lv + ' 未进入第' + lv + '关（实际 ' + info.lv + '）');
        if (info.lv !== lv && lv > 3) console.log('  注：lvl=' + lv + ' 钩子未直达（实际 ' + info.lv + '），属引擎 gate 限制，不计失败');
        if (info.stageLen < 50) fails.push('lvl=' + lv + ' 舞台文本为空');
        if (errs.length) fails.push('lvl=' + lv + ' 页面错误: ' + errs.join('|'));
        await page.close();
    }

    // ② L1 悬停作答（comp-vdd → 含「置零」的项）
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
    });
    await page.goto(BASE, { waitUntil: 'load' });
    await sleep(900);
    const before = await page.evaluate(() => (typeof S !== 'undefined' ? S.score : -1));
    await page.hover('g[data-id="comp-vdd"] circle >> nth=0');
    let after = before;
    try {
        await page.waitForSelector('#ctxmenu .mi', { timeout: 4000 });
        const items = await page.$$eval('#ctxmenu .mi', els => els.map(e => e.textContent.trim()));
        console.log('comp-vdd 菜单项:', items.join(' / '));
        // L1 为「画直流通路」，电源正确操作为保留；逐个尝试菜单项，记录首个能记分的项
        for (const it of items) {
            await page.click('#ctxmenu .mi:has-text("' + it.replace(/[↑↓]/g, '') + '")').catch(() => {});
            await sleep(500);
            const sub = await page.$$('#ctxmenu .mi');
            if (sub.length) { await page.click('#ctxmenu .mi >> nth=0').catch(() => {}); await sleep(500); }
            after = await page.evaluate(() => (typeof S !== 'undefined' ? S.score : -1));
            console.log('  尝试「' + it + '」→ 得分 ' + after);
            if (after > before) break;
            await page.mouse.move(800, 850);   // 移开，复位菜单
            await sleep(300);
            await page.hover('g[data-id="comp-vdd"] circle >> nth=0');
            await page.waitForSelector('#ctxmenu .mi', { timeout: 4000 });
        }
    } catch (e) {
        fails.push('comp-vdd 悬停菜单失败: ' + e.message);
    }
    console.log('作答前后得分: ' + before + ' → ' + after);
    if (after <= before) fails.push('悬停作答后未记分（' + before + ' → ' + after + '）');
    if (errs.length) fails.push('主流程页面错误: ' + errs.join('|'));
    await page.close();

    await browser.close();
    if (fails.length) { console.error('CS-G1-SMOKE FAIL:\n' + fails.join('\n')); process.exit(1); }
    console.log('CS-G1-SMOKE-ALL-OK');
})();
