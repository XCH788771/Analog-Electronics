// lin-g3 语音内容自测（Playwright + 系统 Chrome）
// 断言：①第3关 V_o 填空完成后，最后一空语音仅为「填写正确，获得3分」，随后只有结算得分语音，
//       不得出现 V_o 推导说明（原 av.say）；②第2关级间提示语音保持不变。
// 运行：NODE_PATH=<workspace>/node_modules node lin-g3-voice-test.js
const { chromium } = require('playwright-core');
const URL = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/lin-g3.html';

(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.addInitScript(() => {
    window.__spoken = [];
    const oST = window.setTimeout;
    window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 40));
  });
  // speakSeq 是页面函数声明（会覆盖 initScript 的桩），改为加载后补丁 speechSynthesis.speak 记录语音文本
  const armRecorder = () => page.evaluate(() => {
    window.__spoken = [];
    try {
      window.speechSynthesis.speak = function (u) { window.__spoken.push(u && u.text); };
    } catch (e) {}
  });
  let fail = 0;
  const check = (name, cond, detail) => {
    console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail ? ' :: ' + detail : ''));
    if (!cond) fail++;
  };
  const clickBlank = (stage, idx) => page.evaluate(
    ([s, i]) => document.querySelector('.blank-box[data-blank-stage="' + s + '"][data-blank-idx="' + i + '"]')
      .dispatchEvent(new MouseEvent('click', { bubbles: true })), [stage, idx]);

  // ---- 场景1：第3关 V_o 填空（全对）----
  await page.goto(URL + '?lvl=3&ph=fill&cb=' + Date.now());
  await page.waitForTimeout(400);
  await armRecorder();
  for (const [i, id] of [[0, 'comp-r2'], [1, 'comp-r1'], [2, 'comp-vi']]) {
    await clickBlank('2', i);
    await page.waitForTimeout(50);
    await page.evaluate(id => window.answerBlank(id), id);
    await page.waitForTimeout(150);
  }
  await page.waitForTimeout(500);
  const r1 = await page.evaluate(() => ({ spoken: window.__spoken.slice(), st: getState() }));
  const tail = r1.spoken.slice(-2);
  check('L3最后一空语音=填写正确，获得3分', tail[0] === '填写正确，获得3分。', JSON.stringify(tail));
  check('L3随后仅结算得分语音', /^恭喜你，完成全部关卡！最终得分\d+分。$/.test(tail[1] || ''), JSON.stringify(tail));
  check('无V_o推导说明语音', !r1.spoken.some(t => /第一级跟随|负10乘微埃|正11微埃|威欧，上端为正/.test(t)), r1.spoken.join(' | '));
  check('已进入结算态（钩子进入仅计本关注分）', r1.st.finished === true && r1.st.score === 9, JSON.stringify({ fin: r1.st.finished, sc: r1.st.score }));

  // ---- 场景2：第2关 A1 填空完成后的级间语音仍在 ----
  await page.goto(URL + '?lvl=2&ph=fill&st=0&cb=' + Date.now());
  await page.waitForTimeout(400);
  await armRecorder();
  await clickBlank('0', 0);
  await page.waitForTimeout(50);
  await page.evaluate(() => window.answerBlank('comp-vi'));
  await page.waitForTimeout(400);
  const r2 = await page.evaluate(() => ({ spoken: window.__spoken.slice(), st: getState() }));
  check('L2 A1填空语音=填写正确，获得24分', r2.spoken.indexOf('填写正确，获得24分。') >= 0, r2.spoken.join(' | '));
  check('L2级间提示语音仍在', r2.spoken.some(t => /A1电路表达式填写完成！接下来选择A2电路的表达式框架。/.test(t)), r2.spoken.join(' | '));
  check('L2推进到A2选框架', r2.st.level === 2 && r2.st.phase === 'fw' && r2.st.stage === 1,
    JSON.stringify({ lv: r2.st.level, ph: r2.st.phase, st: r2.st.stage }));

  check('0 pageerror', errs.length === 0, errs.join(';'));
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
