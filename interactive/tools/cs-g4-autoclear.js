// cs-g4（双电源分压偏置共源·案例1，自 cs-g1 移植）通关回归（通用：答案从 GAME_CONFIG 的 ok 标记自动推导）
// 路径 A：全对 → 100（[20,80]，两关 20+80 计分·已取消直流通路关）  路径 B：L2 首个框架错一次 → 容错  路径 C：重新挑战归零
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g4.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.text())) errors.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30), cancel: () => {}, getVoices: () => [] };
    const oST = window.setTimeout;
    window.setTimeout = (fn, ms) => oST(fn, Math.min(ms || 0, 60));
  });
  await page.goto(PAGE + '?cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(500);
  page._errors = errors;
  return page;
}
const st = page => page.evaluate(() => {
  const s = window.getState();
  return { level: s.level, score: s.score, finished: s.finished, lv: s.levelScore };
});

// draw 关的「整理」子步：把 moveIds 里的元件下移
async function answerMove(page, lv) {
  const mids = await page.evaluate(l => {
    const cfg = LEVELS[l - 1].cfg;
    const out = [];
    (cfg.subSteps || []).forEach(s => (s.moveIds || []).forEach(m => { if (out.indexOf(m) < 0) out.push(m); }));
    return out;
  }, lv);
  for (const id of mids) {
    await page.evaluate(i => chooseMoveOption(i, true), id);
    await sleep(200);
  }
  return mids;
}

// draw 关总驱动：有 subSteps 则按子步顺序（ids 菜单作答 / moveIds 下移），否则 gate 优先一次性
async function driveDraw(page, lv) {
  const subs = await page.evaluate(l => LEVELS[l - 1].cfg.subSteps || null, lv);
  if (!subs) { await answerDraw(page, lv); await answerQuiz(page, lv); return; }
  for (let k = 0; k < subs.length; k++) {
    const ids = await page.evaluate(({ l, k }) => {
      const s = LEVELS[l - 1].cfg.subSteps[k];
      return { ids: s.ids || [], moveIds: s.moveIds || [] };
    }, { l: lv, k });
    for (const id of ids.moveIds) { await page.evaluate(i => chooseMoveOption(i, true), id); await sleep(180); }
    for (const id of ids.ids) {
      const opt = await page.evaluate(({ l, i }) => {
        const t = LEVELS[l - 1].cfg.targets.find(x => x.id === i);
        if (!t) return null;
        const find = items => { for (const it of items) { if (it.ok === true) return it; if (it.sub) { const r = find(it.sub); if (r) return r; } } return null; };
        return find(t.menu || []);
      }, { l: lv, i: id });
      if (opt) { await page.evaluate(({ i, o }) => chooseDrawOption(i, o), { i: id, o: opt }); await sleep(180); }
    }
  }
  await answerQuiz(page, lv);
}

// draw 关：按 cfg 的 ok 标记自动作答（gate 内元件优先）
async function answerDraw(page, lv) {
  const plan = await page.evaluate(l => {
    const cfg = LEVELS[l - 1].cfg;
    const hit = [];
    (cfg.targets || []).forEach(t => {
      const find = items => {
        for (const it of items) {
          if (it.ok === true) return it;
          if (it.sub) { const r = find(it.sub); if (r) return r; }
        }
        return null;
      };
      const opt = find(t.menu || []);
      if (opt) hit.push({ id: t.id, opt });
      else if (t.move) hit.push({ id: t.id, move: true });
    });
    const gate = cfg.gate || [];
    const inGate = hit.filter(h => gate.indexOf(h.id) >= 0);
    const rest = hit.filter(h => gate.indexOf(h.id) < 0);
    return inGate.concat(rest);
  }, lv);
  for (const s of plan) {
    if (s.move) await page.evaluate(id => chooseMoveOption(id, true), s.id);
    else await page.evaluate(({ id, opt }) => chooseDrawOption(id, opt), { id: s.id, opt: s.opt });
    await sleep(180);
  }
  return plan.length;
}

// TQUIZ：逐问按 TQUIZ[i].ok 作答
async function answerQuiz(page, lv) {
  const n = await page.evaluate(() => (typeof TQUIZ !== 'undefined' ? TQUIZ.length : 0));
  for (let i = 0; i < n; i++) {
    let ok = false;
    try {
      await page.waitForFunction(() => document.querySelectorAll('#ctxmenu .mi').length > 0, null, { timeout: 8000 });
      ok = true;
    } catch (e) { /* 无问答 */ }
    if (!ok) break;
    const ans = await page.evaluate(k => TQUIZ[k].ok, i);
    await page.evaluate(op => answerTQuiz(op), ans);
    await sleep(200);
  }
}

// mix 关：框架选正确项 + 填空按 ansIds 作答（可注入一次错选）
async function driveMix(page, wrongOnce) {
  let injected = false;
  for (let guard = 0; guard < 30; guard++) {
    const s = await st(page);
    if (s.finished) break;
    if ((await page.evaluate(() => LEVELS[window.getState().level - 1].kind)) !== 'mix') break;
    const ty = await page.evaluate(() => {
      const stt = window.getState(); const mx = stt.mix[stt.level - 1];
      return mx && mx.steps[mx.si] ? mx.steps[mx.si].type : 'done';
    });
    if (ty === 'fw') {
      if (wrongOnce && !injected) {
        await page.evaluate(() => {
          const stt = window.getState(); const mx = stt.mix[stt.level - 1];
          const ci = mx.steps[mx.si].opts.findIndex(o => o.correct);
          pickMixFw((ci + 1) % mx.steps[mx.si].opts.length);
        });
        await sleep(150); injected = true;
      }
      await page.evaluate(() => {
        const stt = window.getState(); const mx = stt.mix[stt.level - 1];
        pickMixFw(mx.steps[mx.si].opts.findIndex(o => o.correct));
      });
      await sleep(220);
    } else if (ty === 'fill') {
      const lv = (await st(page)).level;
      const n = await page.evaluate(l => window.getState().mix[l - 1].steps[window.getState().mix[l - 1].si].blanks.length, lv);
      for (let b = 0; b < n; b++) {
        await page.evaluate(({ bl, idx }) => {
          const r = document.querySelector('.blank-box[data-blank-level="' + bl + '"][data-blank-idx="' + idx + '"]');
          if (r) r.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }, { bl: lv - 1, idx: b });
        await sleep(80);
        await page.evaluate(({ l, bi }) => {
          const mx = window.getState().mix[l - 1];
          const bb = mx.steps[mx.si].blanks[bi];
          answerBlank(bb.ansIds[bi % bb.ansIds.length]);
        }, { l: lv, bi: b });
        await sleep(150);
      }
      await sleep(300);
    } else break;
  }
}

async function run(browser, wrongOnce, tag) {
  const page = await newPage(browser);
  // L1 交流等效（按 subSteps：交流通路 → 整理下移 → 等效场效应管 + TQUIZ）
  await driveDraw(page, 1);
  await page.waitForFunction(() => window.getState().level === 2, null, { timeout: 15000 });
  const s2 = await st(page);
  console.log(tag + ' L1 完成: score=' + s2.score + ' 各关=' + JSON.stringify(s2.lv.map(Math.round)));
  // L2 动态指标
  await driveMix(page, wrongOnce);
  await page.waitForFunction(() => window.getState().finished, null, { timeout: 15000 });
  const s = await st(page);
  console.log(tag + ' 最终: score=' + s.score + ' 各关=' + JSON.stringify(s.lv.map(Math.round)));
  if (page._errors.length) { console.log(tag + ' PAGEERRORS: ' + page._errors.join(' | ')); process.exit(1); }
  if (!wrongOnce) {
    if (s.score !== 100 || !s.finished) { console.log(tag + ' 满分断言失败 score=' + s.score); process.exit(1); }
    if (JSON.stringify(s.lv.map(Math.round)) !== '[20,80]') { console.log(tag + ' 分关断言失败 ' + JSON.stringify(s.lv)); process.exit(1); }
  } else if (s.score >= 100 || !s.finished) { console.log(tag + ' 容错断言失败 score=' + s.score); process.exit(1); }
  return page;
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-first-run', '--disable-gpu'] });
  await run(browser, false, '路径A(全对)');
  const page = await run(browser, true, '路径B(框架错1次)');
  // 路径 C：重新挑战归零
  await page.evaluate(() => {
    const g = Array.from(document.querySelectorAll('g')).find(e => e.textContent.trim() === '重新挑战');
    if (g) g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  });
  await sleep(500);
  const after = await st(page);
  if (after.score !== 0 || after.finished || after.level !== 1) { console.log('路径C 失败: ' + JSON.stringify(after)); process.exit(1); }
  console.log('路径C 重新挑战归零 OK（score=0 level=1）');
  await browser.close();
  console.log('CS-G1-AUTOCLEAR-ALL-OK');
})().catch(e => { console.error('FATAL:', e.message); process.exit(1); });
