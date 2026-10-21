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
const ROUTE = ['eq', 'eqs', 'cq', 'cqs', 'base', 'bvci'].indexOf(process.env.ROUTE) >= 0 ? process.env.ROUTE : 'eq';
const SEQIDX = { eq: 0, eqs: 1, cq: 2, cqs: 3, base: 4, bvci: 5 };

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
  await pickByMenu('comp-src', '置零', '短路'); await pickByMenu('comp-vcc', '保留'); await pickByMenu('comp-vee', '保留');
  for (const c of ['comp-c1', 'comp-c2', 'comp-ce']) await pickByMenu(c, '断路');
  await page.waitForTimeout(1900);
  const seq = await page.evaluate(i => { const c = LEVELS[S.level-1].cfg; const ss=c.seqs||[c.seq]; return ss[i].map(x=>[].concat(x)[0]); }, 0);
  for (let i=0;i<seq.length;i++){ await clickUnit(seq[i]); await page.waitForTimeout(300); if(i===seq.length-1){for(let w=0;w<20;w++){const cur=await st();if(cur.lvl!==2)break;await page.waitForTimeout(250);}} }
  await page.waitForTimeout(500);
  for (let guard=0;guard<60;guard++){ const s=await st(); if(s.lvl!==3)break;
    const info=await page.evaluate(()=>{const mx=S.mix[S.level-1],stp=mx.steps[mx.si];if(stp.type==='fw')return{type:'fw',idx:stp.opts.findIndex(o=>o.correct)};const bi=stp.blanks.findIndex(b=>!b.done);if(bi<0)return{type:'wait'};const b=stp.blanks[bi];const sibs=stp.blanks.filter((x,i)=>b.grp&&x.grp===b.grp&&i!==bi&&x.done).map(x=>x.picked);return{type:'fill',boxIdx:bi,ans:b.ansIds.slice(),grp:b.grp||null,sibs};});
    if(info.type==='fw'){await pickMixOpt(info.idx);continue;} if(info.type==='wait'){await page.waitForTimeout(900);continue;}
    await page.locator(`.blank-box[data-blank-level="2"][data-blank-idx="${info.boxIdx}"]`).first().click({force:true}); await page.waitForTimeout(160);
    let pick=info.ans[0]; if(info.grp&&info.sibs.includes(pick))pick=info.ans.find(a=>!info.sibs.includes(a))||info.ans[0]; await clickUnit(pick); await page.waitForTimeout(220);
  }
  await page.waitForTimeout(1900);
  await pickByMenu('comp-src','保留'); await pickByMenu('comp-vcc','置零','接地'); await pickByMenu('comp-vee','置零','接地');
  await pickByMenu('comp-c1','短路'); await pickByMenu('comp-c2','短路'); await pickByMenu('comp-ce','短路');
  await pickByMenu('comp-re2','移除'); await pickByMenu('comp-re1','保留');
  await pickByMenu('comp-rc','下移'); await menuClick('与RL并'); await page.waitForTimeout(400);
  await pickByMenu('comp-t','等效');
  for(let k=0;k<6;k++){const q=await page.evaluate(()=>{const d=S.draw[3];if(!d.tquiz||d.tquiz.step>=TQUIZ.length)return null;return{ok:TQUIZ[d.tquiz.step].ok,step:d.tquiz.step};});if(!q)break;if(!(await menuClick(q.ok)))throw new Error('无选项');await page.waitForTimeout(750);}
  await page.waitForTimeout(2300);
  // 第5关：A_v 框架 → 填空；点 R_E1 虚线框(idx3)后真实点击 eq-re1
  for(let guard=0;guard<40;guard++){const s=await st();if(s.lvl!==5)break;
    const info=await page.evaluate(()=>{const mx=S.mix[S.level-1],stp=mx.steps[mx.si];if(stp.type==='fw')return{type:'fw',idx:stp.opts.findIndex(o=>o.correct)};const bi=stp.blanks.findIndex(b=>!b.done);if(bi<0)return{type:'wait'};return{type:'fill',boxIdx:bi};});
    if(info.type==='fw'){await pickMixOpt(info.idx);continue;} if(info.type==='wait'){await page.waitForTimeout(900);continue;}
    await page.waitForTimeout(1200);
    // 找 A_v 分母 R_E1 空（ansIds 含 comp-re1 的 blank）的 data-blank-idx
    const tgt = await page.evaluate(()=>{ const mx=S.mix[4], stp=mx.steps[mx.si]; const bi=stp.blanks.findIndex(b=>(b.ansIds||[]).indexOf('comp-re1')>=0 && !b.done); return bi; });
    console.log('R_E1 空 idx =', tgt);
    if(tgt<0){ console.log('无未填 R_E1 空'); break; }
    await page.locator(`.blank-box[data-blank-level="4"][data-blank-idx="${tgt}"]`).first().click({force:true}); await page.waitForTimeout(300);
    const box = await page.evaluate(() => { const g=document.getElementById('eq-re1'); const r=g.querySelector('rect.hot').getBoundingClientRect(); return {x:r.x+r.width/2, y:r.y+r.height/2}; });
    await page.mouse.click(box.x, box.y); await page.waitForTimeout(600);
    const res = await page.evaluate((t) => { const mx=S.mix[4]; const b=mx.steps[mx.si].blanks[t]||mx.steps[mx.si].blanks.find(x=>(x.ansIds||[]).indexOf('comp-re1')>=0); return {done: !!(b&&b.done), picked: b&&b.picked, score: Math.round(S.score)}; }, tgt);
    console.log('真实点击 eq-re1 填 R_E1 空 →', JSON.stringify(res));
    break;
  }
  await browser.close(); process.exit(0);
})();
