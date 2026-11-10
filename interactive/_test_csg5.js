/* cs-g5 端到端回归：正确路径满分 100 + 容错路径（答错扣分后仍可完成）
 * 页面：双电源恒流源偏置共源放大 · 案例1（C_s 旁路 + 恒流源置零断路 → 源极交流接地）
 * 口径：A_v=−g_m·R_d、R_i=R_g、R_o≈R_d
 * 覆盖：L1 直流通路(20) / L2 交流微变等效(20, 含 R_d 下移 + FET 等效四连问, tquizPool=5) / L3 动态指标(60)
 * 计分口径（池语义）：答错一次不立即扣总分，按池比例 round(per×(pool-1)/pool) 发剩余；
 *   框架 pen=3（错后 rem=3）；Av 两空同 grp av-mul（不区分先后，同 grp 查重）
 * 容错路径预期：L1 19（cs 错1次发3）+ L2 16（vdd/io 各错1次各发2、TQUIZ 错2问池5→3）
 *   + L3 45（三框架各错1次发3、Av 两空同 grp 共享 rem 池，空0 错1次后两空各得9共18）= 80，仍可 finished
 * 技术口径（沿 cj/lin 系列四坑）：
 *   ① TTS 桩：addInitScript 覆写 window.speechSynthesis 对象属性
 *   ② mouseenter 菜单：dispatchEvent（真实 hover 对 fill=none 热区不可靠）
 *   ③ 填答/点选：真实 page.click（走 .stage click 委托）
 *   ④ browser.close() 前完成全部断言，结尾 process.exit(0)
 * 用法：node _test_csg5.js
 */
const { chromium } = require('F:/AI建课/模电/WorkBuddy/Temp/pw/node_modules/playwright-core');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PAGE = 'file:///' + 'F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g5.html'.replace(/\\/g, '/') + '?cb=csg5full';
const OUT = 'F:/AI建课/模电/WorkBuddy/.workbuddy/tmp_csg5/';

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log('  ✓ ' + msg); } else { fail++; console.log('  ✗ FAIL: ' + msg); } }

async function mkPage(browser, cb) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String((e && e.message) || e)));
  page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    const stub = {
      getVoices: () => [],
      speak: u => { if (u && u.onend) setTimeout(() => u.onend(), 5); },
      cancel: () => {}
    };
    try { Object.defineProperty(window, 'speechSynthesis', { value: stub, configurable: true, writable: true }); }
    catch (e) { try { window.speechSynthesis = stub; } catch (e2) {} }
    try { window.SpeechSynthesisUtterance = function (t) { this.text = t; }; } catch (e) {}
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
    // 等待填空框渲染（say 的 onDone 回调渲染，桩 5ms 触发；极端情况下看门狗 3000ms 兜底）
    await page.waitForSelector('.blank-box[data-blank-level="2"][data-blank-idx="' + bi + '"]', { timeout: 6000 });
    // blank-box 用冒泡 dispatch（.stage 委托生效；对答消息浮层会拦截真实鼠标点击）
    await page.evaluate(bi => {
      const b = document.querySelector('.blank-box[data-blank-level="2"][data-blank-idx="' + bi + '"]');
      if (!b) throw new Error('no blank-box idx=' + bi);
      b.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }, bi);
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
    await hover('comp-cs');
    ok(!(await menuVisible()), '门控：信号源/电源/恒流源未处理前 C_S 不弹菜单');
    await hover('comp-vi');
    ok(await menuVisible(), '门控：信号源悬停弹出菜单');
    await clickMi('置零');
    await clickMi('短路');
    s0 = await st();
    ok(s0.lv[0] === 4, 'L1：信号源置零短路 +4（实得 ' + s0.lv[0] + '）');
    await hover('comp-vdd');
    await clickMi('保留');
    await hover('comp-vss');
    await clickMi('保留');
    await hover('comp-io');
    await clickMi('保留');
    s0 = await st();
    ok(s0.lv[0] === 16, 'L1：双电源与恒流源保留 +12（实得 ' + s0.lv[0] + '）');
    await hover('comp-cs');
    ok(await menuVisible(), 'comp-cs 悬停弹出菜单');
    await clickMi('断路');
    await page.waitForTimeout(1600);
    s0 = await st();
    ok(s0.lv[0] === 20 && s0.level === 2, 'L1 完成：20 分并进入第 2 关（实得 ' + s0.lv[0] + ' / level=' + s0.level + '）');

    console.log('— L2 绘制交流微变等效电路 —');
    await page.waitForTimeout(600);
    await hover('comp-vi');
    await clickMi('保留');
    await hover('comp-vdd');
    await clickMi('置零');
    await clickMi('接地');
    await hover('comp-vss');
    await clickMi('置零');
    await clickMi('接地');
    await hover('comp-io');
    await clickMi('置零');
    await clickMi('断路');
    await hover('comp-cs');
    await clickMi('短路');
    s0 = await st();
    ok(s0.lv[1] === 15, 'L2：信号源保留 + 双电源置零 + 恒流源断路 + 电容短路 = 15 分（实得 ' + s0.lv[1] + '）');
    await hover('comp-rd');
    await clickMi('下移');
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
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 30, 'L3：Av 表达式 2 空 = 24 分（累计 ' + s0.lv[2] + '）');
    await pickFw(true);
    await fillBlank(0, '#eq-rg rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 45, 'L3：Ri 框架 6 + 表达式 9 = 15 分（累计 ' + s0.lv[2] + '）');
    await pickFw(true);
    await fillBlank(0, '#rarr-rd rect.hot');
    await page.waitForTimeout(2200);
    s0 = await st();
    ok(s0.lv[2] === 60 && s0.score === 100 && s0.finished, 'L3 完成：Ro 框架 6 + 表达式 9 = 15 分；总分 100（实得 ' + s0.score + ' finished=' + s0.finished + '）');

    console.log('\n— 场景A 页面错误 —');
    ok(errs.length === 0, '无 pageerror / console.error（' + (errs.length ? errs.slice(0, 3).join(' | ') : '0 条') + '）');
    await page.screenshot({ path: OUT + 'shot_done.png' });
    await page.close();
  }

  // ==================== 场景 B：容错路径（答错扣分后仍完成，预期 83） ====================
  {
    const { page, errs, st, hover, menuVisible, clickMi, pickFw, fillBlank } = await mkPage(browser, 'fault');
    console.log('\n— 场景B 容错路径 —');
    let s0 = await st();
    ok(s0.level === 1 && s0.score === 0, '初始：第 1 关 / 0 分');

    // ---- L1：cs 先错选「短路」（池4→3，按池比例发 round(4×4/5)=3） ----
    console.log('— L1（cs 错1次）—');
    await hover('comp-vi');
    await clickMi('置零');
    await clickMi('短路');
    await hover('comp-vdd');
    await clickMi('保留');
    await hover('comp-vss');
    await clickMi('保留');
    await hover('comp-io');
    await clickMi('保留');
    await hover('comp-cs');
    await clickMi('短路');   // 错：直流通路电容应断路
    s0 = await st();
    ok(s0.lv[0] === 16, 'L1：cs 答错不立即扣总分，仅池 4→3（实得 ' + s0.lv[0] + '）');
    await hover('comp-cs');
    await clickMi('断路');
    await page.waitForTimeout(1600);
    s0 = await st();
    ok(s0.lv[0] === 19 && s0.level === 2, 'L1 完成：19 分（错1次）并进入第 2 关（实得 ' + s0.lv[0] + '）');

    // ---- L2：vdd 与 io 各错一次（各发2）；TQUIZ 错 2 问（池5→3） ----
    console.log('— L2（vdd/io 错、TQUIZ 错2问）—');
    await page.waitForTimeout(600);
    await hover('comp-vi');
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
    await hover('comp-io');
    await clickMi('保留');   // 错：交流通路恒流源应置零断路
    await hover('comp-io');
    await clickMi('置零');
    await clickMi('断路');
    await hover('comp-cs');
    await clickMi('短路');
    s0 = await st();
    ok(s0.lv[1] === 13, 'L2：vdd/io 各错1次按池比例各发2，其余满分 = 13 分（实得 ' + s0.lv[1] + '）');
    await hover('comp-rd');
    await clickMi('下移');
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
    ok(s0.lv[1] === 16 && s0.level === 3, 'L2 完成：13 + TQUIZ 池3 = 16 分（实得 ' + s0.lv[1] + ' / level=' + s0.level + '）');

    // ---- L3：三框架各先错一次（rem 6→3）；Av 空0 先错填 R_d（rem 12→9） ----
    console.log('— L3（三框架各错1次 + Av 空0 错1次）—');
    await page.waitForTimeout(600);
    await pickFw(false);      // Av 框架错（干扰项）
    s0 = await st();
    ok(s0.lv[2] === 0, 'L3：Av 框架答错不立即扣总分，仅 rem 6→3（实得 ' + s0.lv[2] + '）');
    await pickFw(true);
    s0 = await st();
    ok(s0.lv[2] === 3, 'L3：Av 框架答对只发剩余 3 分（pen=3，实得 ' + s0.lv[2] + '）');
    await fillBlank(0, '#eq-rg rect.hot');   // 错：空0 应填 g_m 或 R_d（av-mul 组），R_g 是错件
    s0 = await st();
    ok(s0.lv[2] === 3, 'L3：Av 空0 答错不立即扣总分，仅 rem 12→9（实得 ' + s0.lv[2] + '）');
    await fillBlank(0, 'g[data-id="q-gm"] text');
    await fillBlank(1, '#rarr-rd rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 21, 'L3：Av 表达式 18 分（两空同 grp 共 rem9，各得9；累计 ' + s0.lv[2] + '）');
    await pickFw(false);      // Ri 框架错
    await pickFw(true);
    await fillBlank(0, '#eq-rg rect.hot');
    await page.waitForTimeout(1800);
    s0 = await st();
    ok(s0.lv[2] === 33, 'L3：Ri 框架 3 + 表达式 9 = 12 分（累计 ' + s0.lv[2] + '）');
    await pickFw(false);      // Ro 框架错
    await pickFw(true);
    await fillBlank(0, '#rarr-rd rect.hot');
    await page.waitForTimeout(2200);
    s0 = await st();
    ok(s0.lv[2] === 45 && s0.score === 80 && s0.finished, 'L3 完成：Ro 框架 3 + 空 9 = 12 分；总分 19+16+45 = 80（实得 ' + s0.score + ' finished=' + s0.finished + '）');

    console.log('\n— 场景B 页面错误 —');
    ok(errs.length === 0, '无 pageerror / console.error（' + (errs.length ? errs.slice(0, 3).join(' | ') : '0 条') + '）');
    await page.screenshot({ path: OUT + 'shot_fault_done.png' });
    await page.close();
  }

  console.log('\n========== 双场景回归：PASS=' + pass + '  FAIL=' + fail + ' ==========');
  await browser.close();
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(2); });
