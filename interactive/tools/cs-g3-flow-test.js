// cs-g1 三关流程自动化自测（Playwright + 系统 Chrome）
// 路径 A：全对 → 满分 100（L1 27 / L2 28 / L3 45）
// 路径 B：第 2 关 Av 框架错一次 → 容错（score<100 且 finished）
// 路径 C：真实鼠标命中验证（?lvl=1 悬停 comp-vdd 两级菜单；?lvl=3 点框+真实鼠标点 comp-rg / comp-rg1 作答）
// 路径 D：重新挑战归零
// 运行：NODE_PATH=<workspace>/Temp/pwtest/node_modules node 网站/interactive/tools/cs-g1-flow-test.js
const { chromium } = require('playwright-core');

const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    window.speechSynthesis = {
      speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30),
      cancel: () => {}, getVoices: () => []
    };
    const oST = window.setTimeout;
    window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 60));
  });
  await page.goto(PAGE + '?cb=' + Date.now());
  await page.waitForTimeout(500);
  page._errors = errors;
  return page;
}

const st = page => page.evaluate(() => {
  const s = window.getState();
  return { level: s.level, score: s.score, finished: s.finished, lv: s.levelScore };
});

// 通用：从 level===2 起，动态按当前 level 驱动所有 mix 关（框架+填空交错）直到 finished
async function driveMixLevels(page, wrongFw) {
  const fwCorrectIdx = (lv) => page.evaluate(l => {
    const mx = window.getState().mix[l - 1];
    return mx.steps[mx.si].opts.findIndex(o => o.correct);
  }, lv);
  const stepType = (lv) => page.evaluate(l => {
    const mx = window.getState().mix[l - 1];
    return mx.steps[mx.si] ? mx.steps[mx.si].type : 'done';
  }, lv);
  let wrongApplied = false;
  for (let guard = 0; guard < 20 && !((await st(page)).finished); guard++) {
    const lv = (await st(page)).level;
    const bl = lv - 1;
    const ty = await stepType(lv);
    if (ty === 'fw') {
      if (wrongFw && !wrongApplied) {
        const n = await page.evaluate(l => window.getState().mix[l - 1].steps[window.getState().mix[l - 1].si].opts.length, lv);
        const ci = await fwCorrectIdx(lv);
        await page.evaluate(vi => window.pickMixFw(vi), (ci + 1) % n);
        await sleep(150);
        wrongApplied = true;
      }
      await page.evaluate(l => pickMixFw(window.getState().mix[l - 1].steps[window.getState().mix[l - 1].si].opts.findIndex(o => o.correct)), lv);
      await sleep(200);
    } else if (ty === 'fill') {
      const n = await page.evaluate(l => window.getState().mix[l - 1].steps[window.getState().mix[l - 1].si].blanks.length, lv);
      for (let b = 0; b < n; b++) {
        await page.evaluate(({ bl, idx }) => {
          const r = document.querySelector('.blank-box[data-blank-level="' + bl + '"][data-blank-idx="' + idx + '"]');
          r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }, { bl, idx: b });
        await sleep(80);
        await page.evaluate(({ l, bi }) => {
          const mx = window.getState().mix[l - 1];
          const stp = mx.steps[mx.si];
          const bb = stp.blanks[bi];
          window.answerBlank(bb.ansIds[bi % bb.ansIds.length]);
        }, { l: lv, bi: b });
        await sleep(150);
      }
      await sleep(300);
    } else break;
  }
  await page.waitForFunction(() => window.getState().finished, null, { timeout: 12000 });
}

// ---- 路径 A / B：引擎直驱满分通关 ----
async function driveFull(browser, wrongFw, tag) {
  const page = await newPage(browser);

  // 第 1 关：绘制交流微变等效电路（门控：+VDD 先置零接地；再电容短路；再移除 R_S；再 R_G1/R_D 下挂；最后等效）
  await page.evaluate(() => chooseDrawOption('comp-vdd', { act: 'vcc-gnd', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-vi', { act: 'vi-keep', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-c1', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-c2', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-cs', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-rs', { act: 'rs-remove', ok: true }));
  await page.evaluate(() => chooseMoveOption('comp-rg1', true));
  await page.evaluate(() => chooseMoveOption('comp-rd', true));
  await page.evaluate(() => chooseDrawOption('comp-t', { act: 't-equiv', ok: true }));
  await page.waitForFunction(() => !!window.getState().draw[0].tquiz, null, { timeout: 12000 });
  // TQUIZ 五连问：逐问等待菜单 → 作答（菜单每次作答后重弹）
  for (const ans of ['开路', '上＋下－', '开路', '受控源', '↓i_d']) {
    await page.waitForFunction(() =>
      document.querySelectorAll('#ctxmenu .mi').length > 0, null, { timeout: 12000 });
    await page.evaluate(op => answerTQuiz(op), ans);
    await sleep(150);
  }
  await page.waitForFunction(() => window.getState().level === 2, null, { timeout: 12000 });
  const s1 = await st(page); console.log(tag + ' L1 完成: score=' + s1.score);

  // 第 2、3 关：mix 框架+填空交错（动态按当前 level 驱动）
  await driveMixLevels(page, wrongFw);
  const s = await st(page);
  console.log(tag + ' 最终: score=' + s.score + ' 各关=' + JSON.stringify(s.lv.map(Math.round)));
  if (page._errors.length) { console.log(tag + ' PAGEERRORS:', page._errors); await browser.close(); process.exit(1); }
  if (!wrongFw) {
    if (s.score !== 100 || !s.finished) { console.log(tag + ' 满分断言失败: score=' + s.score); await browser.close(); process.exit(1); }
    if (JSON.stringify(s.lv.map(Math.round)) !== '[27,28,45]') { console.log(tag + ' 分关断言失败: ' + JSON.stringify(s.lv)); await browser.close(); process.exit(1); }
  } else {
    if (s.score >= 100 || !s.finished) { console.log(tag + ' 容错断言失败: score=' + s.score); await browser.close(); process.exit(1); }
  }
  await page.close();
  return s;
}

// ---- 路径 C：真实鼠标命中验证 ----
const wrapOff = page => page.evaluate(() => {
  const m = getComputedStyle(document.getElementById('circuit-wrap')).transform;
  const t = m && m.match(/matrix\(1, 0, 0, 1, ([-\d.]+), ([-\d.]+)\)/);
  return t ? [+t[1], +t[2]] : [0, 0];
});
async function driveMouse(browser) {
  // C1：?lvl=1 悬停 comp-vdd → 两级菜单（置零 → 接地）真实点击
  const page = await newPage(browser);
  const svg = await page.evaluate(() => {
    const r = document.querySelector('svg.circuit').getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
  const mkPt = async (sx, sy) => {
    const [dx, dy] = await wrapOff(page);
    return { x: svg.x + (sx + dx) / 1600 * svg.w, y: svg.y + (sy + dy) / 900 * svg.h };
  };
  let p = await mkPt(830, 5);   // +VDD 端子圆心（第113轮端子左移30px：860→830）
  await page.mouse.move(p.x, p.y); await sleep(300);
  let mi = await page.evaluate(() => Array.from(document.querySelectorAll('#ctxmenu .mi')).map(d => d.textContent.trim()));
  if (!(mi.includes('置零') && mi.includes('保留'))) {
    console.log('C1 失败: 一级菜单=' + JSON.stringify(mi)); await browser.close(); process.exit(1);
  }
  await page.evaluate(() => { Array.from(document.querySelectorAll('#ctxmenu .mi')).find(d => d.textContent.trim() === '置零').click(); });
  await sleep(200);
  mi = await page.evaluate(() => Array.from(document.querySelectorAll('#ctxmenu .mi')).map(d => d.textContent.trim()));
  if (!(mi.includes('接地') && mi.includes('断路'))) {
    console.log('C1 失败: 二级菜单=' + JSON.stringify(mi)); await browser.close(); process.exit(1);
  }
  await page.evaluate(() => { Array.from(document.querySelectorAll('#ctxmenu .mi')).find(d => d.textContent.trim() === '接地').click(); });
  await sleep(200);
  let found = await page.evaluate(() => window.getState().draw[0].found['comp-vdd'] === true);
  if (!found) { console.log('C1 失败: comp-vdd 未记分'); await browser.close(); process.exit(1); }
  console.log('C1 悬停两级菜单 OK（置零→接地，comp-vdd 记分）');
  await page.close();

  // C2：?lvl=3 真实鼠标点虚线框 + 点 comp-rg / comp-rg1 作答（Ri 填空）
  const page2 = await newPage(browser);
  await page2.goto(PAGE + '?lvl=3&cb=' + Date.now());
  await page2.waitForTimeout(600);
  // 先把 Ri 框架答对，进入填空子步
  await page2.evaluate(() => {
    const mx = window.getState().mix[2];
    window.pickMixFw(mx.steps[mx.si].opts.findIndex(o => o.correct));
  });
  await sleep(250);
  const svg2 = await page2.evaluate(() => {
    const r = document.querySelector('svg.circuit').getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
  const mkPt2 = async (sx, sy) => {
    const [dx, dy] = await wrapOff(page2);
    return { x: svg2.x + (sx + dx) / 1600 * svg2.w, y: svg2.y + (sy + dy) / 900 * svg2.h };
  };
  // 虚线框 0：真实点击（面板内）
  let box = await page2.evaluate(() => {
    const r = document.querySelector('.blank-box[data-blank-level="2"][data-blank-idx="0"]').getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  });
  await page2.mouse.click(box.x, box.y); await sleep(150);
  // 点 comp-rg 电阻体（320,352；第111轮 R_G 下挂于栅极引线下方转角水平线，中心 (320,352)）
  p = await mkPt2(363, 352);
  await page2.mouse.click(p.x, p.y); await sleep(150);
  let b0 = await page2.evaluate(() => window.getState().mix[2].steps[1].blanks[0]);
  if (!b0.done || b0.picked !== 'comp-rg') {
    console.log('C2 失败: 空0 picked=' + b0.picked + ' done=' + b0.done); await browser.close(); process.exit(1);
  }
  // 虚线框 1：真实点击 + 点 comp-rg1 电阻体（250,143；第113轮 RG1 上移至体 117-170，中心 y=143.5）
  box = await page2.evaluate(() => {
    const r = document.querySelector('.blank-box[data-blank-level="2"][data-blank-idx="1"]').getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  });
  await page2.mouse.click(box.x, box.y); await sleep(150);
  p = await mkPt2(280, 143);
  await page2.mouse.click(p.x, p.y); await sleep(150);
  const b1 = await page2.evaluate(() => window.getState().mix[2].steps[1].blanks[1]);
  if (!b1.done || b1.picked !== 'comp-rg1') {
    console.log('C2 失败: 空1 picked=' + b1.picked + ' done=' + b1.done); await browser.close(); process.exit(1);
  }
  console.log('C2 真实鼠标命中 OK（comp-rg / comp-rg1 均命中并记分）');
  await page2.close();
}

// ---- 路径 D：重新挑战归零 ----
async function driveRestart(browser) {
  const page = await newPage(browser);
  // 直驱 L1 绘制 + TQUIZ 到 level===2
  await page.evaluate(() => chooseDrawOption('comp-vdd', { act: 'vcc-gnd', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-vi', { act: 'vi-keep', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-c1', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-c2', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-cs', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-rs', { act: 'rs-remove', ok: true }));
  await page.evaluate(() => chooseMoveOption('comp-rg1', true));
  await page.evaluate(() => chooseMoveOption('comp-rd', true));
  await page.evaluate(() => chooseDrawOption('comp-t', { act: 't-equiv', ok: true }));
  await page.waitForFunction(() => !!window.getState().draw[0].tquiz, null, { timeout: 12000 });
  for (const ans of ['开路', '上＋下－', '开路', '受控源', '↓i_d']) {
    await page.waitForFunction(() => document.querySelectorAll('#ctxmenu .mi').length > 0, null, { timeout: 12000 });
    await page.evaluate(op => answerTQuiz(op), ans);
    await sleep(150);
  }
  await page.waitForFunction(() => window.getState().level === 2, null, { timeout: 12000 });
  // 复用通用 mix 驱动通关
  await driveMixLevels(page, false);
  const before = await st(page);
  if (!before.finished) { console.log('D 失败: 未通关 before=' + JSON.stringify(before)); await browser.close(); process.exit(1); }
  // 点击「重新挑战」（精确定位带监听的按钮 <g>，避免误命中包含该文字的父容器）
  await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('g'));
    const g = els.find(e => e.textContent.trim() === '重新挑战');
    if (g) g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  });
  await sleep(400);
  const after = await st(page);
  if (after.score !== 0 || after.finished || after.level !== 1) {
    console.log('D 失败: 归零后 state=' + JSON.stringify(after)); await browser.close(); process.exit(1);
  }
  console.log('D 重新挑战归零 OK（score=' + after.score + ' level=' + after.level + ' finished=' + after.finished + '）');
  await page.close();
}

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  await driveFull(browser, false, '路径A(全对)');
  await driveFull(browser, true, '路径B(Av框架错1次)');
  await driveMouse(browser);
  await driveRestart(browser);
  await browser.close();
  console.log('CS-G1-FLOW-ALL-OK');
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
