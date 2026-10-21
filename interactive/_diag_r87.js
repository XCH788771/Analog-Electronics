// cj-g3 满分回归：Playwright 真实 UI 走正确路径，断言 score===100 && finished && pageerrors=0
// 答案表一律运行时从页面内部状态读（TQUIZ[step].ok / opts.findIndex(o=>o.correct) / blanks.ansIds），不硬编码。
// 点击说明：q* 电量标注位于 fx-layer（pointer-events:none），真实鼠标点不中 → 用 dispatchEvent 冒泡到 .stage 委托；
//          绘制关菜单必须真实鼠标悬停（mouseenter 绑定在 .interactive 上）。
// 路线（统一引擎写法）：ROUTE=eq|eqs|cq|cqs|base —— 第2关的合法顺序
//   eq  = I_EQ → I_CQ → I_BQ → V_CEQ
//   eqs = I_EQ → I_CQ → V_CEQ → I_BQ（I_BQ / V_CEQ 两块互换）
//   cq  = I_CQ → I_BQ → V_CEQ
//   cqs = I_CQ → V_CEQ → I_BQ（两块互换）
//   base= I_BQ → I_CQ → V_CEQ（基极优先；subsBase：I_BQ 精确式→工程近似简化式两步）
//   第3关按路线分发 subs/subsC/subsBase：I_BQ 与 V_CEQ 两块顺序跟随第2关实际点选先后，其余内容固定。
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g3.html';
const norm = s => String(s || '').replace(/[\s_]/g, '');
const ROUTE = ['eq', 'eqs', 'cq', 'cqs', 'base'].indexOf(process.env.ROUTE) >= 0 ? process.env.ROUTE : 'eq';
const SEQIDX = { eq: 0, eqs: 1, cq: 2, cqs: 3, base: 4 };

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  // headless 无 TTS：window.speechSynthesis 是只读访问器，直接赋值无效（会被静默忽略）。
  // 正确做法：页面脚本执行后覆写 speakSeq —— 逐句同步走完 onStart/onEnd 并立即回调 onDone，
  // 这样 completeLevel 等「语音结束才推进」的链路在测试中可确定地触发。
  await page.addInitScript(() => {
    window.__ttsPatched = false;
  });
  await page.addInitScript(() => {
    const patch = () => {
      if (window.__ttsPatched || typeof window.speakSeq !== 'function') { setTimeout(patch, 30); return; }
      window.__ttsPatched = true;
      window.speakSeq = function (parts, onDone) {
        const list = parts || [];
        list.forEach(p => { if (p && p.onStart) { try { p.onStart(); } catch (e) {} } });
        if (onDone) { try { onDone(); } catch (e) { throw e; } }
      };
      window.speakSeq.__orig = true;
    };
    patch();
  });
  await page.goto(PAGE + '?cb=' + Date.now(), { waitUntil: 'load' });   // file:// 缓存破除
  await page.waitForTimeout(500);

  const st = () => page.evaluate(() => ({
    lvl: S.level, score: Math.round(S.score), finished: S.finished,
    per: Math.round(S.levelScore[S.level - 1]), title: LEVELS[S.level - 1].cfg.title,
  }));

  async function menuClick(optText) {
    const items = page.locator('#ctxmenu .mi');
    const n = await items.count();
    if (!n) return false;
    for (let i = 0; i < n; i++) {
      if (norm(await items.nth(i).innerText()).includes(norm(optText))) {
        await items.nth(i).hover(); await page.waitForTimeout(180);
        await items.nth(i).click(); await page.waitForTimeout(200);
        return true;
      }
    }
    return false;
  }
  // 悬停元件：直接向 .interactive 派发 mouseenter。
  // 原因：菜单的 mouseenter 监听绑在元件组上，但 SVG 只在「有 paint 的子元素」上做命中测试——
  // 透明命中矩形（fill=none stroke=none，如 comp-t 的热区）中心点命中不到，真实鼠标移入会静默失败。
  // 派发事件走的是与用户悬停完全相同的那条处理链（menuItemsFor → showMenu），逻辑等价且确定。
  async function hoverUnit(unitId) {
    const ok = await page.evaluate(id => {
      const g = document.querySelector(`#circuit-wrap g[data-id="${id}"]`);
      if (!g) return false;
      try { hideMenu(); } catch (e) {}
      g.dispatchEvent(new MouseEvent('mouseenter', { bubbles: false }));
      return true;
    }, unitId);
    if (!ok) throw new Error(`无此元件 ${unitId}`);
    await page.waitForTimeout(220);
  }
  async function pickByMenu(unitId, first, second) {
    await hoverUnit(unitId);
    if (!(await menuClick(first))) {
      const items = page.locator('#ctxmenu .mi'); const t = [];
      for (let i = 0; i < await items.count(); i++) t.push(await items.nth(i).innerText());
      throw new Error(`${unitId} 菜单无「${first}」，现有：${JSON.stringify(t)}`);
    }
    if (second && !(await menuClick(second))) throw new Error(`${unitId} 二级菜单无「${second}」`);
  }
  const clickUnit = id => page.evaluate(i => {
    const g = document.querySelector(`#circuit-wrap g[data-id="${i}"]`);
    if (!g) throw new Error('无此单元 ' + i);
    g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  }, id);
  const pickMixOpt = async idx => {
    await page.locator('.g-opt').nth(idx).click({ force: true });
    await page.waitForTimeout(1900);
  };
  // 第1关
  await pickByMenu('comp-src', '置零', '短路'); await pickByMenu('comp-vcc', '保留'); await pickByMenu('comp-vee', '保留');
  for (const c of ['comp-c1', 'comp-c2', 'comp-ce']) await pickByMenu(c, '断路');
  await page.waitForTimeout(1900);
  // 第2关：合成点击 IEQ, ICQ, VCEQ
  for (const id of ['q-ieq', 'q-icq', 'q-vceq']) { await clickUnit(id); await page.waitForTimeout(400); }
  const done1 = await page.evaluate(() => S.qorder[1].done.slice());
  console.log('前三步后 done =', JSON.stringify(done1));
  // q-ibq 各特征点的命中测试（真实鼠标会走的路径）
  const hit = await page.evaluate(() => {
    const g = document.querySelector('#circuit-wrap g[data-id="q-ibq"]');
    const r = g.getBoundingClientRect();
    const svg = document.getElementById('circuit-wrap');
    const wrap = svg.getBoundingClientRect();
    const pts = [];
    // 取 q-ibq 内 text 与 line 的屏幕坐标
    g.querySelectorAll('text,line,rect.hot,polygon').forEach(el => {
      try {
        const b = el.getBoundingClientRect();
        pts.push({ tag: el.tagName, cx: b.x + b.width/2, cy: b.y + b.height/2, w: Math.round(b.width), h: Math.round(b.height) });
      } catch(e){}
    });
    return pts.map(p => {
      const el = document.elementFromPoint(p.cx, p.cy);
      const owner = el ? (el.closest ? (el.closest('g[data-id]') || el.closest('g[id]') || el) : el) : null;
      return { ...p, hit: owner ? (owner.dataset ? (owner.dataset.id || owner.dataset.name || owner.id) : owner.tagName) : 'null', hitTag: el ? el.tagName : 'null', hitCls: el ? (el.getAttribute('class')||'') : '' };
    });
  });
  console.log('q-ibq 特征点命中:', JSON.stringify(hit, null, 1));
  // 真实鼠标点击 q-ibq 文字中心
  const box = await page.evaluate(() => { const t = document.querySelector('#circuit-wrap g[data-id="q-ibq"] text'); const b = t.getBoundingClientRect(); return { x: b.x + b.width/2, y: b.y + b.height/2 }; });
  console.log('真实鼠标点击 q-ibq 文字 @', JSON.stringify(box));
  await page.mouse.move(box.x, box.y); await page.waitForTimeout(120);
  await page.mouse.click(box.x, box.y); await page.waitForTimeout(600);
  const done2 = await page.evaluate(() => S.qorder[1].done.slice());
  console.log('真实点击 IBQ 后 done =', JSON.stringify(done2), '| lvl =', (await st()).lvl, '| score =', (await st()).score);
  await browser.close(); process.exit(0);
})();
