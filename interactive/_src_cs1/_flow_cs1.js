// cs-g1 全流程自动化回归（Playwright + 系统 Chrome，真实鼠标交互）
// 路径 A：全对 → 100 分；路径 B：L1 电源/电容各错一次 + 等效四问全错 + L2 框架错一次/首空错一次 → 87 分
// 运行：NODE_PATH=<pw-core 目录> node _src_cs1/_flow_cs1.js
const { chromium } = require('playwright-core');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const BASE = 'http://127.0.0.1:8765/interactive/cs-g1.html?cb=' + Date.now();
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function newPage(browser, errors) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  // 资源 404 才记（favicon 404 忽略，属正常噪音）；console error 文本不可区分资源，改看 response
  page.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) errors.push('http ' + r.status() + ': ' + r.url()); });
  page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    // TTS stub：同步触发 onStart/onEnd/onDone
    window.speakSeq = function (parts, onDone) {
      (parts || []).forEach(p => { if (p.onStart) try { p.onStart(); } catch (e) {} if (p.onEnd) try { p.onEnd(); } catch (e) {} });
      if (onDone) try { onDone(); } catch (e) {}
    };
    // 定时器加速（关卡推进延时 900/1200/1600/2000ms → 40ms）
    const oST = window.setTimeout;
    window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  await page.goto(BASE);
  await page.waitForTimeout(500);
  return page;
}

const st = page => page.evaluate(() => {
  const s = window.getState(), L = window.getLevels();
  return { level: s.level, score: s.score, finished: s.finished, kind: L[s.level - 1].kind,
           si: s.mix[s.level - 1] ? s.mix[s.level - 1].si : -1,
           levelScore: s.levelScore.map(x => Math.round(x)) };
});

async function until(page, fn, desc, timeout = 12000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) {
    if (await fn(await st(page))) return;
    await sleep(50);
  }
  const s = await st(page);
  throw new Error('超时: ' + desc + '（当前 L' + s.level + ' si' + s.si + ' sc' + s.score + '）');
}
const untilScore = (page, n, desc) => until(page, s => s.score === n, desc || ('得分 ' + n));

// 悬停命中映射：bbox 中心落在空白的组，须悬停具体子元素（circle/line/rect.hot）；
// comp-t 的 rect.hot 中心靠近沟道线，用 position 偏移到符号右侧空白
const HOVER = {
  'comp-vi':  { sel: 'g[data-id="comp-vi"] circle >> nth=0' },
  'comp-vdd': { sel: 'g[data-id="comp-vdd"] circle' },
  'comp-cb1': { sel: 'g[data-id="comp-cb1"] .hot-label' },   // line 几何宽度 0 被判不可见，改悬停 C_b1 标注（组内冒泡同样浮菜单）
  'comp-t':   { sel: 'g[data-id="comp-t"] rect.hot', pos: { x: 100, y: 50 } },
};
const FILL = {
  'comp-rg1': { sel: 'g[data-id="comp-rg1"] rect.hot' },
  'comp-rg2': { sel: 'g[data-id="comp-rg2"] rect.hot' },
  'comp-rd':  { sel: 'g[data-id="comp-rd"] rect.hot' },
  'q-gm':     { sel: 'g[data-id="q-gm"] rect.hot', pos: { x: 43, y: 6 } },   // 中心被 g_m 标注墨迹压住，偏移到其上方
};
// 悬停元件 → 在浮出菜单里点选项（支持二级：subText）
async function menuPick(page, dataId, itemText, subText) {
  const h = HOVER[dataId] || { sel: 'g[data-id="' + dataId + '"] rect.hot' };
  console.log('    · menuPick', dataId, itemText, subText || '');
  await page.hover(h.sel, h.pos ? { position: h.pos } : {});
  await page.waitForSelector('#ctxmenu .mi', { timeout: 4000 });
  await page.click('#ctxmenu .mi:has-text("' + itemText + '")');
  if (subText) {
    await page.waitForSelector('#ctxmenu .mi', { timeout: 4000 });
    await page.click('#ctxmenu .mi:has-text("' + subText + '")');
  }
}
// 等效问答：等选项条出现含指定文本的项后点它
async function tquizPick(page, waitText, pickText) {
  if (waitText) await until(page, async () => (await page.evaluate(() => document.getElementById('ctxmenu').textContent)).indexOf(waitText) >= 0, '选项条出现 ' + waitText);
  await page.click('#ctxmenu .mi:has-text("' + pickText + '")');
}
// mix 框架：按内部状态找正确项索引后真实点击
async function pickFw(page, lvIdx, wrong) {
  const idx = await page.evaluate(([li, w]) => {
    const mx = window.getState().mix[li];
    const opts = mx.steps[mx.si].opts;
    const c = opts.findIndex(o => o.correct);
    return w ? (c + 1) % opts.length : c;
  }, [lvIdx, !!wrong]);
  await page.click('#game-ui g[data-opt-idx="' + idx + '"]');
}
// mix 填空：点虚线框 → 点电路元件/电量标注（rect.hot 均带 pointer-events:all，偏移点须避开压住它的标注墨迹）
async function fillBlank(page, lvIdx, bi, dataId) {
  await page.click('.blank-box[data-blank-level="' + lvIdx + '"][data-blank-idx="' + bi + '"]');
  const f = FILL[dataId] || { sel: 'g[data-id="' + dataId + '"] rect.hot' };
  await page.click(f.sel, f.pos ? { position: f.pos } : {});
}

async function run(browser, errors, wrong) {
  const page = await newPage(browser, errors);
  const log = [];
  const note = (t, s) => log.push(t + ' → L' + s.level + ' 得 ' + s.score + ' ' + JSON.stringify(s.levelScore));

  // ---- L1 绘制交流小信号等效电路（26 分）----
  await until(page, s => s.level === 1, 'L1');
  if (wrong) {
    // 门控顺序：信号源与电源必须先处理完，电容才解锁（与线上行为一致）
    await menuPick(page, 'comp-vdd', '保留');            // 错：电源不应保留
    await menuPick(page, 'comp-vdd', '置零', '接地');    // 对
    await menuPick(page, 'comp-vi', '保留');             // 对（信号源保留）
    await menuPick(page, 'comp-cb1', '断路');            // 错：交流通路电容应短路
    await menuPick(page, 'comp-cb1', '短路');            // 对
    let s = await st(page); note('L1 画图完', s);
    if (s.score !== 19) throw new Error('路径B L1 画图得分 ' + s.score + ' ≠ 19');
  } else {
    await menuPick(page, 'comp-vi', '保留');
    await menuPick(page, 'comp-vdd', '置零', '接地');
    await menuPick(page, 'comp-cb1', '短路');
    let s = await st(page); note('L1 画图完', s);
    if (s.score !== 21) throw new Error('路径A L1 画图得分 ' + s.score + ' ≠ 21');
  }
  // 场效应管等效 → 四连问答
  await page.hover('g[data-id="comp-t"] rect.hot', { position: { x: 100, y: 50 } });
  await page.click('#ctxmenu .mi:has-text("等效")');
  if (wrong) {
    await tquizPick(page, null, '受控源');        // Q1 错（应为开路）
    await tquizPick(page, '电阻', '电阻');        // Q2 错（应为受控源）
    await tquizPick(page, '↓', '↑');              // Q3 错（应向下）
    await tquizPick(page, '压控电压源', '流控电流源'); // Q4 错（应为压控电流源）
  } else {
    await tquizPick(page, null, '开路');          // Q1 对
    await tquizPick(page, '电阻', '受控源');      // Q2 对
    await tquizPick(page, '↓', '↓');              // Q3 对
    await tquizPick(page, '压控电压源', '压控电流源'); // Q4 对
  }
  await until(page, s => s.level === 2, '进入 L2');
  let s = await st(page); note('L1 完', s);
  if (s.score !== (wrong ? 20 : 26)) throw new Error('L1 总分 ' + s.score + ' ≠ ' + (wrong ? 20 : 26));

  // ---- L2 电压放大倍数（26 分：框架6 + gm 10 + Rd 10）----
  await until(page, s => s.level === 2 && s.kind === 'mix', 'L2');
  if (wrong) await pickFw(page, 1, true);    // 框架先错一次（罚分，停在框架步）
  await pickFw(page, 1, false);              // 再选对 → 推进到填空步
  await until(page, s => s.si === 1, 'L2 填空步');
  if (wrong) {
    await fillBlank(page, 1, 0, 'comp-rg1');       // 错：Av 首空是 gm
    await untilScore(page, 24, 'L2 首空错后扣分');
  }
  await fillBlank(page, 1, 0, 'q-gm');
  await fillBlank(page, 1, 1, 'comp-rd');
  await until(page, s => s.level === 3, '进入 L3');
  s = await st(page); note('L2 完', s);
  if (s.score !== (wrong ? 39 : 52)) throw new Error('L2 后总分 ' + s.score + ' ≠ ' + (wrong ? 39 : 52));

  // ---- L3 输入电阻（24 分：框架4 + Rg1/Rg2 各10）----
  await until(page, s => s.level === 3 && s.kind === 'mix', 'L3');
  await pickFw(page, 2, false);
  await until(page, s => s.si === 1, 'L3 填空步');
  await fillBlank(page, 2, 0, 'comp-rg1');
  await fillBlank(page, 2, 1, 'comp-rg2');
  await until(page, s => s.level === 4, '进入 L4');
  s = await st(page); note('L3 完', s);
  if (s.score !== (wrong ? 63 : 76)) throw new Error('L3 后总分 ' + s.score + ' ≠ ' + (wrong ? 63 : 76));

  // ---- L4 输出电阻（24 分：框架4 + Rd 20）----
  await until(page, s => s.level === 4 && s.kind === 'mix', 'L4');
  await pickFw(page, 3, false);
  await until(page, s => s.si === 1, 'L4 填空步');
  await fillBlank(page, 3, 0, 'comp-rd');
  await until(page, s => s.finished, '结算');
  s = await st(page); note('完', s);
  const want = wrong ? 87 : 100;
  if (s.score !== want) throw new Error('最终得分 ' + s.score + ' ≠ ' + want);
  const wantLS = wrong ? [20, 19, 24, 24] : [26, 26, 24, 24];
  if (JSON.stringify(s.levelScore) !== JSON.stringify(wantLS))
    throw new Error('分项 ' + JSON.stringify(s.levelScore) + ' ≠ ' + JSON.stringify(wantLS));
  // 结算屏文字
  const doneText = await page.evaluate(() => document.getElementById('game-ui').textContent);
  if (doneText.indexOf('最终得分：' + want) < 0) throw new Error('结算屏未见 ' + want + ' 分：' + doneText.slice(0, 80));
  await page.close();
  return log;
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const errors = [];
  try {
    console.log('== 路径 A（全对）==');
    (await run(browser, errors, false)).forEach(l => console.log('  ', l));
    console.log('== 路径 B（含错答）==');
    (await run(browser, errors, true)).forEach(l => console.log('  ', l));
  } catch (e) {
    console.error('✗', e.message);
    if (errors.length) errors.forEach(x => console.error('  ', x));
    await browser.close();
    process.exit(1);
  }
  await browser.close();
  if (errors.length) { console.error('✗ 页面错误:'); errors.forEach(x => console.error('  ', x)); process.exit(1); }
  console.log('✓ 两条路径全部通过（A=100 / B=87），无页面错误');
})().catch(e => { console.error(e); process.exit(1); });
