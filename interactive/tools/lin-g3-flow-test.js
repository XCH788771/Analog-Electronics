// lin-g3 交替流程自动化自测（Playwright + 系统 Chrome）
// 路径 A：全对 → 满分 100；路径 B：L2 两级框架各错一次 + A₂ 首空错一次 → 88
// （第101轮起第3关为"选框架3分＋填空9分"，两路径第3关均全对）
// 运行：NODE_PATH=<workspace>/node_modules node <this file>
const path = require('path');
const { chromium } = require('playwright-core');

const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/lin-g3.html?cb=' + Date.now();
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function drive(browser, wrongFw, wrongBlank) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.addInitScript(() => {
    // TTS stub：同步触发 onStart/onEnd/onDone
    window.speakSeq = function (parts, onDone) {
      (parts || []).forEach(p => { if (p.onStart) try { p.onStart(); } catch (e) {} if (p.onEnd) try { p.onEnd(); } catch (e) {} });
      if (onDone) try { onDone(); } catch (e) {}
    };
    // 定时器加速（框架/填空完成后的延时推进 2400/2000/2800ms → 40ms）
    const oST = window.setTimeout;
    window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  await page.goto(PAGE);
  await page.waitForTimeout(600);

  const fr = page.mainFrame(); // 引擎在顶层页面？不——lin-g3.html 即顶层
  const st = () => page.evaluate(() => {
    const s = window.getState();
    return { level: s.level, stage: s.stage, phase: s.phase || '', score: s.score,
             finished: s.finished, typeAns: s.typeAns,
             fwSolved: s.fw.map(f => f.solved), fillDone: s.fill.map(a => a.map(b => b.done)),
             avFwSolved: s.avFw ? s.avFw.solved : false,
             fillAvDone: s.fillAv ? s.fillAv.map(b => b.done) : [] };
  });
  // 等待条件（真实时间轮询）
  const until = async (fn, desc, timeout = 8000) => {
    const t0 = Date.now();
    while (Date.now() - t0 < timeout) {
      if (await fn()) return;
      await sleep(60);
    }
    throw new Error('超时: ' + desc);
  };

  const seq = [];
  const snap = async tag => { const s = await st(); seq.push(tag + ' L' + s.level + '/' + s.phase + '/st' + s.stage + ' sc' + s.score); return s; };

  // ---- L1 判类型（答对两级）----
  await until(async () => (await st()).level === 1, 'L1');
  let s = await snap('start');
  for (let i = 0; i < 2; i++) {
    const ans = (await st()).typeAns[i];
    await page.evaluate(idx => window.pickType(idx, window.getState().typeAns[idx]), i);
    await sleep(120);
  }
  await until(async () => (await st()).level === 2, '进入 L2');

  // ---- L2 逐级交替 ----
  for (let stg = 0; stg < 2; stg++) {
    // 选框架（可选：先错一次）
    await until(async () => { const x = await st(); return x.level === 2 && x.phase === 'fw' && x.stage === stg; }, 'fw' + stg);
    await snap('fw' + stg);
    if (wrongFw) {
      const n = await page.evaluate(st2 => window.getState().fwList[st2].length, stg);
      const correct = await page.evaluate(st2 => window.getState().fwList[st2].findIndex(f => f.correct), stg);
      const wrong = (correct + 1) % n;
      await page.evaluate(([st2, i]) => window.pickFramework(st2, i), [stg, wrong]);
      await sleep(150);
    }
    const correct = await page.evaluate(st2 => window.getState().fwList[st2].findIndex(f => f.correct), stg);
    await page.evaluate(([st2, i]) => window.pickFramework(st2, i), [stg, correct]);
    await until(async () => { const x = await st(); return x.level === 2 && x.phase === 'fill' && x.stage === stg; }, 'fill' + stg);
    await snap('fill' + stg);

    // 填空：逐空点框 + 点元件（A₂ 首空可先错一次）；ansIds 依 GAME_CONFIG.blanks 顺序硬编码
    //（A₁ 级 1 空：Vᵢ→输入端子；A₂ 级 3 空：R₂→comp-r2、R₁→comp-r1、Vₒ₁→comp-vo1b）
    const blanks = await page.evaluate(st2 => window.getState().fill[st2].length, stg);
    const ansIds = stg === 0 ? ['comp-vi'] : ['comp-r2', 'comp-r1', 'comp-vo1b'];
    for (let bi = 0; bi < blanks; bi++) {
      await page.evaluate(([st2, i]) => {
        const r = document.querySelector('.blank-box[data-blank-stage="' + st2 + '"][data-blank-idx="' + i + '"]');
        r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }, [stg, bi]);
      await sleep(80);
      if (wrongBlank && stg === 1 && bi === 0) {
        // 故意点平衡电阻（不在 A₂ 级任何空的 ansIds 中）
        await page.evaluate(id => window.answerBlank(id), 'comp-gnd2');
        await sleep(150);
      }
      await page.evaluate(([st2, i, id]) => window.answerBlank(id), [stg, bi, ansIds[bi]]);
      await sleep(120);
    }
    await until(async () => {
      const x = await st();
      return x.level === 2 && x.phase === 'fw' && x.stage === stg + 1 || x.level === 3;
    }, 'after fill' + stg);
  }

  // ---- L3 求Vₒ：选框架（3分）→ 立即填表达式（R₂、R₁、Vᵢ 各3分）----
  await until(async () => (await st()).level === 3, 'L3');
  await snap('av-fw');
  const afw = await page.evaluate(() => window.getState().avFwList.findIndex(f => f.correct));
  await page.evaluate(i => window.pickAvFw(i), afw);
  await until(async () => { const x = await st(); return x.level === 3 && x.phase === 'fill'; }, 'av-fill');
  await snap('av-fill');
  const avAnsIds = ['comp-r2', 'comp-r1', 'comp-vi'];   // 按正确框架虚线框出现顺序
  for (let bi = 0; bi < 3; bi++) {
    await page.evaluate(([st2, i]) => {
      const r = document.querySelector('.blank-box[data-blank-stage="' + st2 + '"][data-blank-idx="' + i + '"]');
      r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }, [2, bi]);
    await sleep(80);
    await page.evaluate(([st2, i, id]) => window.answerBlank(id), [2, bi, avAnsIds[bi]]);
    await sleep(120);
  }
  await until(async () => (await st()).finished, 'finished');
  s = await snap('end');

  // UI 断言：tab 3 个、状态行文案
  const tabs = await page.evaluate(() => [...document.querySelectorAll('#game-ui .g-tab')].length);
  const statusText = await page.evaluate(() => {
    const ts = [...document.querySelectorAll('#game-ui text')];
    return ts.map(t => t.textContent).filter(t => /已处理|本关得分/.test(t)).join(' | ');
  });
  await page.screenshot({ path: path.join(process.env.TEMP || '.', 'lg3-flow-end.png') });
  await page.close();
  return { seq, score: s.score, finished: s.finished, tabs, statusText, errors };
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const out = [];
  let fail = 0;
  try {
    const A = await drive(browser, false, false);
    out.push('路径A(全对): score=' + A.score + ' finished=' + A.finished + ' tabs=' + A.tabs);
    out.push('  序列: ' + A.seq.join(' -> '));
    out.push('  状态行: ' + A.statusText);
    if (A.score !== 100 || !A.finished || A.tabs !== 3) fail++;
    if (A.errors.length) { out.push('  错误: ' + A.errors.slice(0, 3).join('; ')); fail++; }

    const B = await drive(browser, true, true);
    out.push('路径B(含错答): score=' + B.score + ' finished=' + B.finished);
    out.push('  序列: ' + B.seq.join(' -> '));
    if (B.score !== 88 || !B.finished) fail++;
    if (B.errors.length) { out.push('  错误: ' + B.errors.slice(0, 3).join('; ')); fail++; }
  } catch (e) {
    out.push('EXCEPTION: ' + e.message);
    fail++;
  }
  await browser.close();
  console.log(out.join('\n'));
  process.exit(fail ? 1 : 0);
})();
