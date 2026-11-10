// cs-g1 第2关 I_DQ：常数 1 / 指数 2 方框化 + 表达式上方数字按钮行 —— 定向断言 + 截图
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g1.html';

const out = [];
const ck = (name, cond, extra) => { out.push((cond ? 'PASS ' : 'FAIL ') + name + (extra !== undefined ? ' | ' + extra : '')); return cond; };

(async () => {
    const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true, args: ['--no-first-run'] });
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    page.on('pageerror', e => console.log('PAGEERROR', e.message));
    await page.addInitScript(() => {
        window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 20), cancel: () => {}, getVoices: () => [] };
        const oST = window.setTimeout; window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 60));
    });
    await page.goto(PAGE + '?lvl=2&cb=' + Date.now());
    await page.waitForTimeout(1500);

    const stOf = () => page.evaluate(() => {
        const s = window.getState(); const mx = s.mix && s.mix[s.level - 1];
        if (!mx) return { si: -1, type: 'none', done: null, picked: null, score: s.score || 0, lv: (s.lv || []).map(Math.round) };
        const stp = mx.steps[mx.si] || { type: 'none', blanks: null };
        const bl = stp.blanks || [];
        return { si: mx.si, type: stp.type, done: bl.map(x => !!x.done),
                 picked: bl.map(x => x.picked || null), score: s.score, lv: (s.lv || []).map(Math.round) };
    });

    // 推进到 I_DQ 表达式子步（si === 3）
    for (let it = 0; it < 16; it++) {
        const st = await stOf();
        if (st.si === 3) break;
        if (st.type === 'fw') {
            await page.evaluate(() => {
                const s = window.getState(); const mx = s.mix[s.level - 1];
                pickMixFw(mx.steps[mx.si].opts.findIndex(o => o.correct));
            });
            await page.waitForTimeout(280);
            continue;
        }
        const bi = st.done.findIndex(x => !x);
        if (bi < 0) { await page.waitForTimeout(250); continue; }
        await page.evaluate(idx => {
            const r = document.querySelector('.blank-box[data-blank-level="1"][data-blank-idx="' + idx + '"]');
            if (r) r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }, bi);
        await page.waitForTimeout(120);
        await page.evaluate(idx => {
            const s = window.getState(); const mx = s.mix[s.level - 1];
            const bb = mx.steps[mx.si].blanks[idx];
            answerBlank(bb.ansIds[idx % bb.ansIds.length]);
        }, bi);
        await page.waitForTimeout(200);
    }
    console.log('AT-STEP ' + JSON.stringify(await stOf()));

    const info = await page.evaluate(() => {
        const s = window.getState(); const mx = s.mix[s.level - 1]; const step = mx.steps[mx.si];
        const keys = [...document.querySelectorAll('.num-key')];
        const boxes = [...document.querySelectorAll('.blank-box[data-blank-level="1"]')];
        const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), b: Math.round(r.bottom) }; };
        return {
            stepType: step.type, blanks: step.blanks.length,
            ansIds: step.blanks.map(b => b.ansIds[0]),
            keys: keys.length, keyDigits: keys.map(k => k.getAttribute('data-digit')),
            keyRow: keys.length ? { top: bb(keys[0]).y, bot: bb(keys[0]).b, x0: bb(keys[0]).x, x9: bb(keys[9]).x } : null,
            boxCount: boxes.length,
            boxGeo: boxes.map(b => { const g = bb(b); return { sup: !!b.getAttribute('data-num-sup'), x: g.x, y: g.y, b: g.b, w: g.w, h: g.h }; })
        };
    });
    console.log('BOXES ' + JSON.stringify(info.boxGeo.map(o => ({ sup: o.sup, x: o.x, y: o.y, b: o.b, w: o.w }))));
    console.log('KEYS ' + JSON.stringify(info.keyRow));

    ck('处于 I_DQ 表达式填空步', info.stepType === 'fill', info.stepType);
    ck('空白框 5 个', info.boxCount === 5, info.boxCount);
    ck('答案序 q-ido/q-vth/q-vt/num-1/num-2', info.ansIds.join(',') === 'q-ido,q-vth,q-vt,num-1,num-2', info.ansIds.join(','));
    ck('数字键 10 个 0~9', info.keys === 10 && info.keyDigits.join('') === '0123456789', info.keyDigits.join(''));
    const g = info.boxGeo;
    ck('第 5 空为上标小框（更小更靠上）', !!g[4].sup && g[4].w < g[0].w && g[4].b < g[3].b - 8, JSON.stringify(g[4]) + ' vs const ' + JSON.stringify(g[3]));
    ck('数字键行整体位于表达式上方（无重叠）', info.keyRow.bot < Math.min.apply(null, g.map(o => o.y)) - 8, 'keys.bot=' + info.keyRow.bot + ' exprTop=' + Math.min.apply(null, g.map(o => o.y)));
    ck('数字键行不越右边界', info.keyRow.x9 <= 1530, 'x9=' + info.keyRow.x9);

    // 真实鼠标点击：点常数框 → 点错数字（应提示不填） → 点 1；点指数框 → 点 2
    async function clickBlank(idx) {
        const b = await page.evaluate(i => { const r = document.querySelector('.blank-box[data-blank-level="1"][data-blank-idx="' + i + '"]').getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; }, idx);
        await page.mouse.click(b.x, b.y);
        await page.waitForTimeout(160);
        return page.evaluate(() => window.getState().selBox);
    }
    async function clickDigit(d) {
        const b = await page.evaluate(dd => { const r = document.querySelector('.num-key[data-digit="' + dd + '"]').getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; }, d);
        await page.mouse.click(b.x, b.y);
        await page.waitForTimeout(240);
    }
    ck('真实鼠标点常数框可选中', (await clickBlank(3) || {}).idx === 3);
    await clickDigit('3');
    let st = await stOf();
    ck('点错数字不填（可重试）', st.done[3] === false && st.picked[3] === null, 'done=' + st.done[3]);
    await clickDigit('1');
    st = await stOf();
    ck('常数空填入 1', st.picked[3] === 'num-1', st.picked[3]);
    ck('点指数框可选中', (await clickBlank(4) || {}).idx === 4);
    await clickDigit('2');
    st = await stOf();
    ck('指数空填入 2', st.picked[4] === 'num-2', st.picked[4]);
    ck('数字空不计分（填 1、2 前后总分仍为 12）', st.score === 12, 'score=' + st.score);

    await page.screenshot({ path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/assets/shots/idq-numpad.png' });
    await browser.close();
    console.log('\n' + out.join('\n'));
    const fails = out.filter(x => x.startsWith('FAIL'));
    console.log(fails.length ? ('\nFAILED ' + fails.length) : '\nALL PASS');
})();
