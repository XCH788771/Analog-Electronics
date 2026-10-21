// cj-g5 满分回归：Playwright 真实 UI 走正确路径，断言 score===100 && finished && pageerrors=0
// 答案表一律运行时从页面内部状态读（TQUIZ[step].ok / opts.findIndex(o=>o.correct) / blanks.ansIds），不硬编码。
// 点击说明：q* 电量标注位于 fx/qlabel-layer（pointer-events:none），真实鼠标点不中 → 用 dispatchEvent 冒泡到 .stage 委托；
//          绘制关菜单必须真实鼠标悬停（mouseenter 绑定在 .interactive 上）→ 派发 mouseenter 事件等价触发。
// 两轮：①正确路径 → 100/100；②含错路径（L1 选错电容处理 + L3 首个框架答错）→ finished 且 score<100 且无 pageerror。
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g5.html';
const norm = s => String(s || '').replace(/[\s_]/g, '');
const ROUTE = process.env.ROUTE || 'icq';   // icq/ieq=长路线(I_CQ/I_EQ 起步) / icq2/ieq2=r15 短路线(V_CEQ 提前)

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });

  async function runOnce(wrongMode) {
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    // headless 无 TTS：window.speechSynthesis 是只读访问器，赋值被静默忽略。
    // 正确做法：页面脚本执行后覆写 speakSeq —— 同步走完 onStart/onEnd 并立即回调 onDone。
    await page.addInitScript(() => {
      const patch = () => {
        if (typeof window.speakSeq !== 'function') { setTimeout(patch, 30); return; }
        window.speakSeq = function (parts, onDone) {
          const list = parts || [];
          list.forEach(p => { if (p && p.onStart) { try { p.onStart(); } catch (e) {} } });
          if (onDone) { try { onDone(); } catch (e) {} }
        };
      };
      patch();
    });
    await page.goto(PAGE + '?cb=' + Date.now(), { waitUntil: 'load' });
    await page.waitForTimeout(500);

    // mix 分值配平核算：Σ(各 fw 的 qpts + 各 fill 的 blanks[].pts) 必须精确等于 pts
    const balance = await page.evaluate(() => LEVELS.map((L, li) => {
      const s = L.cfg;
      if (s.kind !== 'mix') return null;
      const sum = s.subs.reduce((a, sub) => a + (sub.type === 'fw' ? sub.qpts : sub.blanks.reduce((x, b) => x + b.pts, 0)), 0);
      return { level: li + 1, pts: s.pts, sum, ok: sum === s.pts };
    }).filter(Boolean));
    console.log('  mix配平:', JSON.stringify(balance));
    if (balance.some(b => !b.ok)) throw new Error('mix 分值未配平！');

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

    // ===== 第 1 关：直流通路（CB/CE 断路、Vs 置零短路、Vcc/Vee/Io 保留） =====
    // 含错路径：①电容 C_E 先错选「短路」（扣分可重选），②第 3 关首个框架答错
    await pickByMenu('comp-src', '置零', '短路');
    await pickByMenu('comp-vcc', '保留');
    await pickByMenu('comp-vee', '保留');
    await pickByMenu('comp-io', '保留');   // 恒流源属门控件，须先处理，电容才解锁
    if (wrongMode) { await pickByMenu('comp-ce', '短路'); await page.waitForTimeout(400); }
    await pickByMenu('comp-ce', '断路');
    await pickByMenu('comp-c1', '断路');
    await page.waitForTimeout(1900);
    console.log('  第1关后:', JSON.stringify(await st()));

    // ===== 第 2 关：Q 点步骤（运行时读 seqs；ROUTE=icq→路线1 / ieq→路线3 / ieq2→路线5（r15 短路线）/ icq2→路线7） =====
    const routeIdx = ROUTE === 'ieq' ? 2 : (ROUTE === 'ieq2' ? 4 : (ROUTE === 'icq2' ? 6 : 0));
    const seqs = await page.evaluate(() => LEVELS[S.level - 1].cfg.seqs);
    // 四条合法路线逐一逻辑校验：每条按序点选，每一步都必须被 qAccept 接受，且终点无后续
    const routeCheck = await page.evaluate(() => {
      const c = LEVELS[S.level - 1].cfg;
      return (c.seqs || []).map(route => {
        const flat = route.reduce((a, k) => a.concat(Array.isArray(k) ? k : [k]), []);
        const done = [];
        for (const id of flat) {
          if (qAccept(c, done).indexOf(id) < 0) return { route: flat.join('>'), ok: false, at: id };
          done.push(id);
        }
        return { route: flat.join('>'), ok: qAccept(c, done).length === 0 };
      });
    });
    console.log('  全路线(' + routeCheck.length + '条)逻辑校验:', JSON.stringify(routeCheck));
    if (routeCheck.some(r => !r.ok)) throw new Error('存在不被引擎接受的路线！');
    const seq = seqs[routeIdx];
    console.log('  路线 ROUTE=' + ROUTE + '，第2关 seq=', JSON.stringify(seq));
    for (let i = 0; i < seq.length; i++) {
      const it = seq[i];
      const id = Array.isArray(it) ? it[0] : it;
      await clickUnit(id);
      await page.waitForTimeout(300);
      if (i === seq.length - 1) {
        for (let w = 0; w < 20; w++) {
          const cur = await st();
          if (cur.lvl !== 2) break;
          await page.waitForTimeout(250);
        }
      }
    }
    await page.waitForTimeout(600);
    console.log('  第2关后:', JSON.stringify(await st()));

    // ===== 第 3 关：Q 点 mix（框架 + 填空，V_EQ→I_EQ→I_CQ→V_CEQ） =====
    let wrongUsed = false;
    for (let guard = 0; guard < 40; guard++) {
      const s = await st(); if (s.lvl !== 3) break;
      if (guard === 0) {
        const bal = await page.evaluate(() => {
          const s = LEVELS[S.level - 1].cfg;
          const sum = s.subs.reduce((a, sub) => a + (sub.type === 'fw' ? sub.qpts : sub.blanks.reduce((x, b) => x + b.pts, 0)), 0);
          return { pts: s.pts, sum, ok: sum === s.pts };
        });
        console.log('  mix当前路线(' + ROUTE + ')配平:', JSON.stringify(bal));
        if (!bal.ok) throw new Error('mix 配平失败（当前路线 ' + ROUTE + '）');
      }
      const info = await page.evaluate(() => {
        const mx = S.mix[S.level - 1], stp = mx.steps[mx.si];
        if (stp.type === 'fw') return { type: 'fw', n: stp.opts.length, idx: stp.opts.findIndex(o => o.correct) };
        const bi = stp.blanks.findIndex(b => !b.done);
        if (bi < 0) return { type: 'wait' };
        const b = stp.blanks[bi];
        const sibs = stp.blanks.filter((x, i) => b.grp && x.grp === b.grp && i !== bi && x.done).map(x => x.picked);
        return { type: 'fill', boxIdx: bi, ans: b.ansIds.slice(), grp: b.grp || null, sibs };
      });
      if (info.type === 'fw') {
        let idx = info.idx;
        if (wrongMode && !wrongUsed) { idx = (idx + 1) % info.n; wrongUsed = true; }  // 首个框架故意答错
        await pickMixOpt(idx); continue;
      }
      if (info.type === 'wait') { await page.waitForTimeout(900); continue; }
      await page.locator(`.blank-box[data-blank-level="2"][data-blank-idx="${info.boxIdx}"]`).first().click({ force: true });
      await page.waitForTimeout(160);
      let pick = info.ans[0];
      if (info.grp && info.sibs.includes(pick)) pick = info.ans.find(a => !info.sibs.includes(a)) || info.ans[0];
      await clickUnit(pick);
      await page.waitForTimeout(220);
    }
    await page.waitForTimeout(1900);
    console.log('  第3关后:', JSON.stringify(await st()));

    // ===== 第 4 关：交流微变等效（三步：交流通路→整理→等效） =====
    // gate：信号源 + 两个电源 + 恒流源先行（r5：恒流源并入门控电源组，须先于电容）；
    // Vs 交流中保留（是输入信号），Vcc/Vee 置零接地，I_o 置零后等效断路
    await pickByMenu('comp-src', '保留');
    await pickByMenu('comp-vcc', '置零', '接地');
    await pickByMenu('comp-vee', '置零', '接地');
    await pickByMenu('comp-io', '置零', '断路');
    await pickByMenu('comp-c1', '短路');
    await pickByMenu('comp-ce', '短路');
    await pickByMenu('comp-rc', '下移'); await menuClick('与RL并');
    await page.waitForTimeout(400);
    await pickByMenu('comp-t', '等效');
    for (let k = 0; k < 6; k++) {
      const q = await page.evaluate(() => {
        const d = S.draw[3];
        if (!d.tquiz || d.tquiz.step >= TQUIZ.length) return null;
        return { ok: TQUIZ[d.tquiz.step].ok, step: d.tquiz.step };
      });
      if (!q) break;
      if (!(await menuClick(q.ok))) throw new Error(`第${q.step + 1} 问无选项「${q.ok}」`);
      await page.waitForTimeout(750);
    }
    await page.waitForTimeout(2300);
    console.log('  第4关后:', JSON.stringify(await st()));

    // ===== 第 5 关：动态指标 mix（Av→Ri→Ro） =====
    for (let guard = 0; guard < 40; guard++) {
      const s = await st(); if (s.lvl !== 5) break;
      const info = await page.evaluate(() => {
        const mx = S.mix[S.level - 1], stp = mx.steps[mx.si];
        if (stp.type === 'fw') return { type: 'fw', idx: stp.opts.findIndex(o => o.correct) };
        const bi = stp.blanks.findIndex(b => !b.done);
        if (bi < 0) return { type: 'wait' };
        const b = stp.blanks[bi];
        const sibs = stp.blanks.filter((x, i) => b.grp && x.grp === b.grp && i !== bi && x.done).map(x => x.picked);
        return { type: 'fill', boxIdx: bi, ans: b.ansIds.slice(), grp: b.grp || null, sibs };
      });
      if (info.type === 'fw') { await pickMixOpt(info.idx); continue; }
      if (info.type === 'wait') { await page.waitForTimeout(900); continue; }
      await page.locator(`.blank-box[data-blank-level="4"][data-blank-idx="${info.boxIdx}"]`).first().click({ force: true });
      await page.waitForTimeout(160);
      let pick = info.ans[0];
      if (info.grp && info.sibs.includes(pick)) pick = info.ans.find(a => !info.sibs.includes(a)) || info.ans[0];
      await clickUnit(pick);
      await page.waitForTimeout(220);
    }
    await page.waitForTimeout(2300);

    const fin = await st();
    const per = await page.evaluate(() => S.levelScore.map(v => Math.round(v)));
    await page.close();
    return { fin, per, errs };
  }

  // ===== 第①轮：正确路径 =====
  console.log('===== 第①轮 正确路径 =====');
  const r1 = await runOnce(false);
  console.log('  finished =', r1.fin.finished, '| score =', r1.fin.score, '| pageerrors =', r1.errs.length ? r1.errs : 0);
  console.log('  逐关得分 =', r1.per.join(' / '), '（合计', r1.per.reduce((a, b) => a + b, 0), '）');
  const ok1 = r1.fin.finished && r1.fin.score === 100 && r1.errs.length === 0;
  console.log(ok1 ? '  ✅ 满分通关 100/100' : '  ❌ 未达满分');

  // ===== 第②轮：含错路径 =====
  console.log('===== 第②轮 含错路径 =====');
  const r2 = await runOnce(true);
  console.log('  finished =', r2.fin.finished, '| score =', r2.fin.score, '| pageerrors =', r2.errs.length ? r2.errs : 0);
  const ok2 = r2.fin.finished && r2.fin.score > 0 && r2.fin.score < 100 && r2.errs.length === 0;
  console.log(ok2 ? '  ✅ 含错路径可通关且不满分（扣分生效）' : '  ❌ 含错路径异常');

  const ok = ok1 && ok2;
  console.log(ok ? '\n✅ 回归全部通过' : '\n❌ 回归未通过');
  // headless 下 browser.close() 在本机偶发挂起（进程被 SIGTERM，实为已完工）→ 断言后直接退出
  process.exit(ok ? 0 : 1);
})();
