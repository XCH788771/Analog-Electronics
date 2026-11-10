// cs-g1 第3关 R_d 下移目检：菜单项数、直接下移、上端节点位置、下端无节点
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

    // ---- A. 整理态（未等效）：鼠标悬停 R_d → 点「下移」 ----
    await page.goto(PAGE + '?lvl=3&cb=' + Date.now());
    await page.waitForTimeout(700);
    await page.evaluate(() => {
        const d = S.draw[2];
        execAct('comp-vi', 'vi-keep'); d.found['comp-vi'] = true;
        execAct('comp-vdd', 'vdd-gnd'); d.found['comp-vdd'] = true;
        execAct('comp-cb1', 'cap-short'); d.found['comp-cb1'] = true;
        moveCompDown('comp-rg1');
        render();
    });
    await page.waitForTimeout(200);
    await page.screenshot({ path: OUT + '/rd-A-before.png' });

    // 悬停 R_d（元件体中心 (486,85) + circuit-wrap translate(18,260)）
    const pt = await page.evaluate(() => {
        const st = document.querySelector('.stage').getBoundingClientRect();
        const w = document.getElementById('circuit-wrap');
        const m = /translate\(([-\d.]+),\s*([-\d.]+)\)/.exec(w.getAttribute('transform') || '');
        const tx = m ? parseFloat(m[1]) : 0, ty = m ? parseFloat(m[2]) : 0;
        const sx = st.width / 1600, sy = st.height / 900;
        return { x: st.left + (486 + tx) * sx, y: st.top + (85 + ty) * sy };
    });
    await page.mouse.move(pt.x, pt.y);
    await page.waitForTimeout(400);
    const menu1 = await page.evaluate(() => {
        const m = document.getElementById('ctxmenu');
        return { display: getComputedStyle(m).display, items: Array.from(m.querySelectorAll('.mi')).map(d => d.textContent.trim()) };
    });
    console.log('A 悬停 R_d 菜单 =', JSON.stringify(menu1));
    await page.screenshot({ path: OUT + '/rd-A-menu.png' });

    // 点第一项「下移」
    const miBox = await page.evaluate(() => {
        const d = document.querySelector('#ctxmenu .mi');
        const r = d.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    });
    await page.mouse.click(miBox.x, miBox.y);
    await page.waitForTimeout(500);
    const after = await page.evaluate(() => {
        const m = document.getElementById('ctxmenu');
        const d = S.draw[2];
        const top = document.getElementById('rarr-rd-top');
        const node = document.getElementById('rarr-rd-node');
        const circles = Array.from(document.querySelectorAll('#rarr-rd circle')).map(c => c.getAttribute('cx') + ',' + c.getAttribute('cy'));
        return {
            menuDisplay: getComputedStyle(m).display,
            menuItems: Array.from(m.querySelectorAll('.mi')).map(x => x.textContent.trim()),
            moved: !!(d.moved && d.moved['comp-rd']),
            rdTopD: top ? top.getAttribute('d') : null,
            nodeCy: node ? node.getAttribute('cy') : null,
            circles: circles,
            gndExt: (function () { const g = document.getElementById('fx-gnd-ext'); return g ? g.style.opacity : null; })()
        };
    });
    console.log('A 点「下移」后 =', JSON.stringify(after));
    await page.screenshot({ path: OUT + '/rd-A-after.png' });

    // ---- B. 等效态：R_d 上端应回到 178（栅漏对齐布局） ----
    await page.goto(PAGE + '?lvl=3&ts=1&cb=' + Date.now());
    await page.waitForTimeout(900);
    const eq = await page.evaluate(() => {
        const top = document.getElementById('rarr-rd-top');
        const node = document.getElementById('rarr-rd-node');
        const circles = Array.from(document.querySelectorAll('#rarr-rd circle')).map(c => c.getAttribute('cx') + ',' + c.getAttribute('cy'));
        return { rdTopD: top ? top.getAttribute('d') : null, nodeCy: node ? node.getAttribute('cy') : null, circles };
    });
    console.log('B 等效态 =', JSON.stringify(eq));
    await page.screenshot({ path: OUT + '/rd-B-equiv.png' });

    await browser.close();
    console.log('RD-MOVE-CHECK-DONE');
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
