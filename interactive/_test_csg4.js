/* cs-g4 端到端回归：正确路径满分 100 + 容错路径（答错扣分后仍可完成）
 * 页面：双电源共源放大 · 案例1（R_s 无旁路 → A_v=−g_m·R_d/(1+g_m·R_s)）
 * 覆盖：L1 直流通路(20) / L2 交流微变等效(20, 含 R_G1/R_D 下移 + FET 等效四连问) / L3 动态指标(60)
 * 计分口径（池语义，与 cs-g2 同）：
 *   L1：5 targets（src 置零→短路 / vdd 保留 / vss 保留 / cb1 断路 / cb2 断路）per=round(20/5)=4
 *   L2：6 targets，t-equiv 不计 per → draw 满分 5×3=15；TQUIZ 四问独立 pool=5 配平至 20
 *   答错一次不发 per-1，而是按池比例 round(per×(pool-1)/pool)：per=3 池4 → round(2.4)=2；框架 pen=3（错后 rem=3）
 *   L3：Av fw6+fill4×6 / Ri fw6+fill2×6 / Ro fw6+fill1×6 = 60
 * 容错路径预期：L1 18（src/cb1 各错1次，池4→3 各发 round(3×4/5)=2）+ L2 15（draw 13 - rd串错1 + TQUIZ 池3）
 *   + L3 48（三框架各错1次发3、Av 空0 错1次发3）= 81，仍可 finished
 * 技术口径（沿 cj/lin 系列四坑）：
 *   ① TTS 桩：addInitScript 覆写 window.speechSynthesis 对象属性
 *   ② mouseenter 菜单：dispatchEvent（真实 hover 对 fill=none 热区不可靠）
 *   ③ 填答/点选：真实 page.click（走 .stage click 委托）
 *   ④ browser.close() 前完成全部断言，结尾 process.exit(0)
 * 用法：node _test_csg4.js
 */
const { chromium } = require('F:/AI建课/模电/WorkBuddy/Temp/pw/node_modules/playwright-core');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PAGE = 'file:///' + 'F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g4.html'.replace(/\\/g, '/') + '?cb=csg4full';
const OUT = 'F:/AI建课/模电/WorkBuddy/.workbuddy/tmp_csg3/';

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log('  ✓ ' + msg); } else { fail++; console.log('  ✗ FAIL: ' + msg); } }

async function mkPage(browser, cb) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String((e && e.message) || e)));
  page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    window.SpeechSynthesisUtterance = function (t) { this.text = t; };
    window.speechSynthesis = {
      getVoices: () => [],
      speak: u => { if (u.onend) setTimeout(() => u.onend(), 5); },
      cancel: () => {}
    };
  });
  await page.goto(PAGE + '&sc=' + cb, { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(900);
  const st = () => page.evaluate(() => {
    const S = window.getState();
    return { score: S.score, level: S.level, finished: S.finished, lv: S.levelScore.map(x => Math.round(x)) };
  });
  async function hover(id) {
    await page.evaluate(id => {
      const g = document.querySelector('g[data-id="' + id + '"]');
      if (!g) throw new Error('no g[data-id=' + id + ']');
      g.dispatchEvent(new MouseEvent('mouseenter'));
    }, id);
    await page.waitForTimeout(150);
  }
  async function menuVisible() {
    return await page.evaluate(() => {
      const c = document.getElementById('ctxmenu');
      return c && c.style.display === 'flex' && c.style.visibility === 'visible';
    });
  }
  async function clickMi(label) {
    await page.click('.ctxmenu .mi:has-text("' + label + '")', { timeout: 4000 });
    await page.waitForTimeout(250);
  }
  async function pickFw(correct) {
    const idx = await page.evaluate(correct => {
      const S = window.getState();
      const mx = S.mix[S.level - 1];
      const s = mx.steps[mx.si];
      return correct ? s.opts.findIndex(o => o.correct) : s.opts.findIndex(o => !o.correct);
    }, correct);
    await page.click('g.g-opt[data-opt-idx="' + idx + '"]', { timeout: 4000 });
    await page.waitForTimeout(400);
  }
  async function fillBlank(bi, sel) {
    await page.click('.blank-box[data-blank-level="2"][data-blank-idx="' + bi + '"]', { timeout: 4000 });
    await page.waitForTimeout(150);
    await page.click(sel, { timeout: 4000 });
    await page.waitForTimeout(400);
  }
  return { page, errs, st, hover, menuVisible, clickMi, pickFw, fillBlank };
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });

  // ==================== 场景 A：正确路径（满分 100） ====================
  {
    const { page, errs, st, hover, menuVisible, clickMi, pickFw, fillBlank } = await mkPage(browser, 'correct');
    console.log('— 场景A 正确路径：初始状态 —');
    let s0 = await st();
    ok(s0.level === 1 && s0.score === 0, '初始：第 1 关 / 0 分（实得 level=' + s0.level + ' score=' + s0.score + '）');

    console.log('— L1 绘制直流通路 —');
    await hover('comp-cb1');
    ok(!(await menuVisible()), '门控：信号源/电源未处理前 C_b1 不弹菜单');
    await hover('comp-src');
    ok(await menuVisible(), '门控：信号源悬停弹出菜单');
    await clickMi('置零');
    await clickMi('短路');
    s0 = await st();
    ok(s0.lv[0] === 4, 'L1：信号源置零短路 +4（实得 ' + s0.lv[0] + '）');
    await hover('comp-vdd');
    await clickMi('保留');
    await hover('comp-vss');
    await clickMi('保留');
    s0 = await st();
    ok(s0.lv[0] === 12, 'L1：双电源保留 +8（实得 ' + s0.lv[0] + '）');
    for (const cap of ['comp-cb1', 'comp-cb2']) {
      await hover(cap);
      ok(await menuVisible(), cap + ' 悬停弹出菜单');
      await clickMi('断路');
    }
    await page.waitForTimeout(1600);
    s0 = await st();
    ok(s0.lv[0] === 20 && s0.level === 2, 'L1 完成：20 分并进入第 2 关（实得 ' + s0.lv[0] + ' / level=' + s0.level + '）');

    console.log('— L2 绘制交流微变等效电路 —');
    await page.waitForTimeout(600);
    await hover('comp-src');
    await clickMi('保留');
    await hover('comp-vdd');
    await clickMi('置零');
    await clickMi('接地');
    await hover('comp-vss');
    await clickMi('置零');
    await clickMi('接地');
    for (const cap of ['comp-cb1', 'comp-cb2']) {
      await hover(cap);
      await clickMi('短路');
    }
    s0 = await st();
    ok(s0.lv[1] === 15, 'L2：信号源保留 + 双电源置零 + 两电容短路 = 15 分（实得 ' + s0.lv[1] + '）');
    await hover('comp-rg1');
    await clickMi('下移');
    await clickMi('与RG2并');
    await hover('comp-rd');
    await clickMi('下移');
    await clickMi('与输出并');
    await hover('comp-t');
    await clickMi('等效');
    await page.waitForTimeout(500);
    await clickMi('开路');
    await page.waitForTimeout(1100);
    await clickMi('开路');
    await page.waitForTimeout(1100);
    await clickMi('受控源');
    await page.waitForTimeout(1100);
    await clickMi('↓id');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[1] === 20 && s0.level === 3, 'L2 完成：15 + TQUIZ 池5 = 20 分并进入第 3 关（实得 ' + s0.lv[1] + ' / level=' + s0.level + '）');

    console.log('— L3 动态指标计算 —');
    await page.waitForTimeout(600);
    await pickFw(true);
    s0 = await st();
    ok(s0.lv[2] === 6, 'L3：Av 框架 +6（实得 ' + s0.lv[2] + '）');
    await fillBlank(0, 'g[data-id="q-gm"] text');
    await fillBlank(1, '#rarr-rd rect.hot');
    await fillBlank(2, 'g[data-id="q-gm"] text');
    await fillBlank(3, '#eq-rs rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 30, 'L3：Av 表达式 4 空 = 24 分（累计 ' + s0.lv[2] + '）');
    await pickFw(true);
    await fillBlank(0, '#eq-rg1 rect.hot');
    await fillBlank(1, '#eq-rg2 rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 48, 'L3：Ri 框架 6 + 表达式 12 = 18 分（累计 ' + s0.lv[2] + '）');
    await pickFw(true);
    await fillBlank(0, '#rarr-rd rect.hot');
    await page.waitForTimeout(2200);
    s0 = await st();
    ok(s0.lv[2] === 60 && s0.score === 100 && s0.finished, 'L3 完成：Ro 框架 6 + 表达式 6 = 12 分；总分 100（实得 ' + s0.score + ' finished=' + s0.finished + '）');

    console.log('\n— 场景A 页面错误 —');
    ok(errs.length === 0, '无 pageerror / console.error（' + (errs.length ? errs.slice(0, 3).join(' | ') : '0 条') + '）');
    await page.screenshot({ path: OUT + 'shot_done.png' });
    await page.close();
  }

  // ==================== 场景 B：容错路径（答错扣分后仍完成，预期 86） ====================
  {
    const { page, errs, st, hover, menuVisible, clickMi, pickFw, fillBlank } = await mkPage(browser, 'fault');
    console.log('\n— 场景B 容错路径 —');
    let s0 = await st();
    ok(s0.level === 1 && s0.score === 0, '初始：第 1 关 / 0 分');

    // ---- L1：src 先错选「保留」（池4→3）；cb1 先错选「短路」（池4→3） ----
    console.log('— L1（src 错1次、cb1 错1次）—');
    await hover('comp-src');
    await clickMi('保留');   // 错：直流通路信号源应置零
    s0 = await st();
    ok(s0.lv[0] === 0, 'L1：src 答错不立即扣总分，仅池 4→3（实得 ' + s0.lv[0] + '）');
    await hover('comp-src');
    await clickMi('置零');
    await clickMi('短路');
    s0 = await st();
    ok(s0.lv[0] === 3, 'L1：src 答对只发剩余 3 分（实得 ' + s0.lv[0] + '）');
    await hover('comp-vdd');
    await clickMi('保留');
    await hover('comp-vss');
    await clickMi('保留');
    await hover('comp-cb1');
    await clickMi('短路');   // 错：直流通路电容应断路
    await hover('comp-cb1');
    await clickMi('断路');
    await hover('comp-cb2');
    await clickMi('断路');
    await page.waitForTimeout(1600);
    s0 = await st();
    ok(s0.lv[0] === 18 && s0.level === 2, 'L1 完成：18 分（错2次）并进入第 2 关（实得 ' + s0.lv[0] + '）');

    // ---- L2：vdd 与 cb1 各错一次（各发3）；rd 误选「串」立即 -1；TQUIZ 错 2 问（池5→3） ----
    console.log('— L2（vdd/cb1 错、rd 串错、TQUIZ 错2问）—');
    await page.waitForTimeout(600);
    await hover('comp-src');
    await clickMi('保留');
    await hover('comp-vdd');
    await clickMi('置零');
    await clickMi('断路');   // 错：交流通路电源应置零接地
    await hover('comp-vdd');
    await clickMi('置零');
    await clickMi('接地');
    await hover('comp-vss');
    await clickMi('置零');
    await clickMi('接地');
    await hover('comp-cb1');
    await clickMi('断路');   // 错：交流通路电容应短路
    await hover('comp-cb1');
    await clickMi('短路');
    await hover('comp-cb2');
    await clickMi('短路');
    s0 = await st();
    ok(s0.lv[1] === 13, 'L2：vdd/cb1 各错1次按池比例各发2，其余满分 = 13 分（实得 ' + s0.lv[1] + '）');
    await hover('comp-rg1');
    await clickMi('下移');
    await clickMi('与RG2并');
    await hover('comp-rd');
    await clickMi('下移');
    await clickMi('与输出串');   // 错：R_d 应与输出并联（立即扣 1）
    s0 = await st();
    ok(s0.lv[1] === 12, 'L2：rd 误选「串」立即扣 1 分（实得 ' + s0.lv[1] + '）');
    await hover('comp-rd');
    await clickMi('下移');
    await clickMi('与输出并');
    await hover('comp-t');
    await clickMi('等效');
    await page.waitForTimeout(500);
    await clickMi('开路');    // 问1 对（G-S 开路）
    await page.waitForTimeout(1100);
    await clickMi('受控源');  // 问2 错（G-D 应为开路）
    await page.waitForTimeout(1100);
    await clickMi('开路');    // 问3 错（D-S 应为受控源）
    await page.waitForTimeout(1100);
    await clickMi('↓id');     // 问4 对
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[1] === 15 && s0.level === 3, 'L2 完成：13 - 1 + TQUIZ 池3 = 15 分（实得 ' + s0.lv[1] + ' / level=' + s0.level + '）');

    // ---- L3：三框架各先错一次（rem 6→4）；Av 空0 先错填 R_d（rem 6→3） ----
    console.log('— L3（三框架各错1次 + Av 空0 错1次）—');
    await page.waitForTimeout(600);
    await pickFw(false);      // Av 框架错（干扰项）
    s0 = await st();
    ok(s0.lv[2] === 0, 'L3：Av 框架答错不立即扣总分，仅 rem 6→4（实得 ' + s0.lv[2] + '）');
    await pickFw(true);
    s0 = await st();
    ok(s0.lv[2] === 3, 'L3：Av 框架答对只发剩余 3 分（pen=3，实得 ' + s0.lv[2] + '）');
    await fillBlank(0, '#rarr-rd rect.hot');   // 错：空0 应填 g_m
    s0 = await st();
    ok(s0.lv[2] === 3, 'L3：Av 空0 答错不立即扣总分，仅 rem 6→3（实得 ' + s0.lv[2] + '）');
    await fillBlank(0, 'g[data-id="q-gm"] text');
    await fillBlank(1, '#rarr-rd rect.hot');
    await fillBlank(2, 'g[data-id="q-gm"] text');
    await fillBlank(3, '#eq-rs rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 24, 'L3：Av 表达式 3+6+6+6 = 21 分（累计 ' + s0.lv[2] + '）');
    await pickFw(false);      // Ri 框架错
    await pickFw(true);
    await fillBlank(0, '#eq-rg1 rect.hot');
    await fillBlank(1, '#eq-rg2 rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 39, 'L3：Ri 框架 3 + 表达式 12 = 15 分（累计 ' + s0.lv[2] + '）');
    await pickFw(false);      // Ro 框架错
    await pickFw(true);
    await fillBlank(0, '#rarr-rd rect.hot');
    await page.waitForTimeout(2200);
    s0 = await st();
    ok(s0.lv[2] === 48 && s0.score === 81 && s0.finished, 'L3 完成：Ro 框架 3 + 空 6 = 9 分；总分 18+15+48 = 81（实得 ' + s0.score + ' finished=' + s0.finished + '）');

    console.log('\n— 场景B 页面错误 —');
    ok(errs.length === 0, '无 pageerror / console.error（' + (errs.length ? errs.slice(0, 3).join(' | ') : '0 条') + '）');
    await page.screenshot({ path: OUT + 'shot_fault_done.png' });
    await page.close();
  }

  console.log('\n========== 双场景回归：PASS=' + pass + '  FAIL=' + fail + ' ==========');
  await browser.close();
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(2); });
