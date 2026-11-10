// cs-g5 三关流程自动化自测（Playwright + 系统 Chrome）
// 路径 A：全对 → 满分 100（L1 20 / L2 20 / L3 60）；路径 B：第 3 关 A_v 框架错一次 → 97；
// 路径 C：真实鼠标命中验证（?lvl=1 悬停菜单两级点击；?lvl=3 点框+真实鼠标点 comp-rd / q-gm 作答）
// 运行：NODE_PATH=<workspace>/node_modules node 网站/interactive/tools/cs-g2-flow-test.js
const { chromium } = require('playwright-core');

const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g5.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    // TTS 桩：speak() 立即回调 onend，语音链瞬时推进（页面内 speakSeq 用 speechSynthesis.speak）
    window.speechSynthesis = {
      speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30),
      cancel: () => {}, getVoices: () => []
    };
    // 延时推进加速（completeLevel 1200 / mixFillDone 1600 / fill 2000 → 60ms）
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
const until = async (page, fn, desc, timeout = 12000) => {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) { if (await fn()) return; await sleep(60); }
  throw new Error('超时: ' + desc);
};

// ---- 路径 A / B：引擎直驱满分通关 ----
async function driveFull(browser, wrongFw, tag) {
  const page = await newPage(browser);
  const opt = (act, ok) => ({ act: act, ok: ok });

  // 第 1 关：直流通路（信号源置零短路；两电源与恒流源保留；C_s 断路）
  await page.evaluate(() => chooseDrawOption('comp-vi', { act: 'vi-short', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-vdd', { act: 'vcc-keep', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-vss', { act: 'vss-keep', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-io', { act: 'io-keep', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-cs', { act: 'cap-open', ok: true }));
  await until(page, async () => (await st(page)).level === 2, tag + ' 进入第2关');
  const s1 = await st(page); console.log(tag + ' L1 完成: score=' + s1.score);

  // 第 2 关：交流通路（V_i 保留；两电源接地；恒流源断路；C_s 短路）→ R_d 下移 → 等效四问
  await page.evaluate(() => chooseDrawOption('comp-vi', { act: 'vi-keep', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-vdd', { act: 'vcc-gnd', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-vss', { act: 'vss-gnd', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-io', { act: 'io-open', ok: true }));
  await page.evaluate(() => chooseDrawOption('comp-cs', { act: 'cap-short', ok: true }));
  await page.evaluate(() => chooseMoveOption('comp-rd', true));
  await page.evaluate(() => chooseDrawOption('comp-t', { act: 't-equiv', ok: true }));
  await until(page, async () => page.evaluate(() => !!window.getState().draw[1].tquiz), tag + ' 问答开始');
  // 逐问等待菜单重弹（引擎在每次作答后 900ms 重显选项条），贴近真实操作节拍
  for (const ans of ['开路', '开路', '受控源', '↓i_d']) {
    await until(page, async () => page.evaluate(() =>
      document.querySelectorAll('#ctxmenu .mi').length > 0), tag + ' 问答菜单');
    await page.evaluate(op => answerTQuiz(op), ans);
    await sleep(150);
  }
  await until(page, async () => (await st(page)).level === 3, tag + ' 进入第3关');

  // 第 3 关：Av/Ri/Ro 框架+填空交错（框架选项运行时查 correct，兼容 shuffle）
  const fwCorrect = () => page.evaluate(() => {
    const mx = window.getState().mix[2];
    return mx.steps[mx.si].opts.findIndex(o => o.correct);
  });
  const stepType = () => page.evaluate(() => {
    const mx = window.getState().mix[2];
    return mx.steps[mx.si] ? mx.steps[mx.si].type : 'done';
  });
  for (let guard = 0; guard < 14 && !((await st(page)).finished); guard++) {
    const ty = await stepType();
    if (ty === 'fw') {
      if (wrongFw && guard === 0) {
        const ci = await fwCorrect();
        const n = await page.evaluate(() => window.getState().mix[2].steps[window.getState().mix[2].si].opts.length);
        await page.evaluate(vi => pickMixFw(vi), (ci + 1) % n);
        await sleep(150);
      }
      await page.evaluate(vi => pickMixFw(vi), await fwCorrect());
      await sleep(200);
    } else if (ty === 'fill') {
      const n = await page.evaluate(() => window.getState().mix[2].steps[window.getState().mix[2].si].blanks.length);
      for (let b = 0; b < n; b++) {
        await page.evaluate(idx => {
          const r = document.querySelector('.blank-box[data-blank-level="2"][data-blank-idx="' + idx + '"]');
          r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }, b);
        await sleep(80);
        await page.evaluate(bi => answerBlank(
          window.getState().mix[2].steps[window.getState().mix[2].si].blanks[bi]
            .ansIds[bi % window.getState().mix[2].steps[window.getState().mix[2].si].blanks[bi].ansIds.length]
        ), b);
        await sleep(150);
      }
      await sleep(300);
    } else break;
  }
  await until(page, async () => (await st(page)).finished, tag + ' 完成全部关卡');
  const s = await st(page);
  console.log(tag + ' 最终: score=' + s.score + ' 各关=' + JSON.stringify(s.lv));
  if (page._errors.length) { console.log(tag + ' PAGEERRORS:', page._errors); await browser.close(); process.exit(1); }
  const expect = wrongFw ? 97 : 100;
  if (s.score !== expect || !s.finished) { console.log(tag + ' 断言失败: 期望 ' + expect); await browser.close(); process.exit(1); }
  if (!wrongFw && JSON.stringify(s.lv.map(Math.round)) !== '[20,20,60]') {
    console.log(tag + ' 分关断言失败: ' + JSON.stringify(s.lv)); await browser.close(); process.exit(1);
  }
  await page.close();
  return s;
}

// ---- 路径 C：真实鼠标命中验证 ----
// 屏幕坐标 = SVG 坐标 + svg 原点 + #circuit-wrap 的 translate 偏移（初始 (18,260)，等效态会变，故每次现读）
const wrapOff = page => page.evaluate(() => {
  const m = getComputedStyle(document.getElementById('circuit-wrap')).transform;
  const t = m && m.match(/matrix\(1, 0, 0, 1, ([-\d.]+), ([-\d.]+)\)/);
  return t ? [+t[1], +t[2]] : [0, 0];
});
async function driveMouse(browser) {
  // C1：?lvl=1 悬停 comp-vi → 两级菜单（置零 → 短路）真实点击
  const page = await newPage(browser);
  const svg = await page.evaluate(() => {
    const r = document.querySelector('svg.circuit').getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
  const mkPt = async (sx, sy) => {
    const [dx, dy] = await wrapOff(page);
    return { x: svg.x + (sx + dx) / 1600 * svg.w, y: svg.y + (sy + dy) / 900 * svg.h };
  };
  let p = await mkPt(150, 294);   // V_i 上端子圆心（可见笔画命中）
  await page.mouse.move(p.x, p.y); await sleep(300);
  let mi = await page.evaluate(() => Array.from(document.querySelectorAll('#ctxmenu .mi')).map(d => d.textContent));
  if (!(mi.includes('置零') && mi.includes('保留'))) {   // 一级菜单可能随机排序
    console.log('C1 失败: 一级菜单=' + JSON.stringify(mi)); await browser.close(); process.exit(1);
  }
  await page.evaluate(() => { Array.from(document.querySelectorAll('#ctxmenu .mi')).find(d => d.textContent === '置零').click(); });
  await sleep(200);
  mi = await page.evaluate(() => Array.from(document.querySelectorAll('#ctxmenu .mi')).map(d => d.textContent));
  if (!(mi.includes('短路') && mi.includes('断路'))) {   // 二级菜单 Fisher-Yates 随机顺序
    console.log('C1 失败: 二级菜单=' + JSON.stringify(mi)); await browser.close(); process.exit(1);
  }
  await page.evaluate(() => { Array.from(document.querySelectorAll('#ctxmenu .mi')).find(d => d.textContent === '短路').click(); });
  await sleep(200);
  let found = await page.evaluate(() => window.getState().draw[0].found['comp-vi'] === true);
  if (!found) { console.log('C1 失败: comp-vi 未记分'); await browser.close(); process.exit(1); }
  console.log('C1 悬停两级菜单 OK（置零→短路，comp-vi 记分）');

  // C2：?lvl=3 真实鼠标点虚线框 + 点 comp-rd / q-gm 作答
  const page2 = await newPage(browser);
  await page2.evaluate(() => { window.getState().level = 3; });
  // 直达第 3 关：?lvl=3 钩子已置 level；直接用 URL 参数重进更稳
  await page2.goto(PAGE + '?lvl=3&cb=' + Date.now());
  await page2.waitForTimeout(600);
  // 先把 Av 框架答对，进入填空子步
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
  // 点 comp-rd 电阻体（486,100——避开 q-gm 热区 x≤480）
  p = await mkPt2(486, 100);
  await page2.mouse.click(p.x, p.y); await sleep(150);
  let b0 = await page2.evaluate(() => window.getState().mix[2].steps[1].blanks[0]);
  if (!b0.done || b0.picked !== 'comp-rd') {
    console.log('C2 失败: 空0 picked=' + b0.picked + ' done=' + b0.done); await browser.close(); process.exit(1);
  }
  // 虚线框 1：真实点击 + 点 q-gm 标注（592,352——受控源菱形右侧，热区 566-618/336-384）
  box = await page2.evaluate(() => {
    const r = document.querySelector('.blank-box[data-blank-level="2"][data-blank-idx="1"]').getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  });
  await page2.mouse.click(box.x, box.y); await sleep(150);
  p = await mkPt2(592, 352);
  await page2.mouse.click(p.x, p.y); await sleep(150);
  const b1 = await page2.evaluate(() => window.getState().mix[2].steps[1].blanks[1]);
  if (!b1.done || b1.picked !== 'q-gm') {
    console.log('C2 失败: 空1 picked=' + b1.picked + ' done=' + b1.done); await browser.close(); process.exit(1);
  }
  console.log('C2 真实鼠标命中 OK（comp-rd / q-gm 均命中并记分）');
  await page.close(); await page2.close();
}

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  await driveFull(browser, false, '路径A(全对)');
  await driveFull(browser, true, '路径B(Av框架错1次)');
  await driveMouse(browser);
  await browser.close();
  console.log('CS-G3-FLOW-ALL-OK');
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
