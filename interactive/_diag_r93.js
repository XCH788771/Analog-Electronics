// r93 诊断：先 RC 整理 → 再移除 RE2 后，红框区域可见图元 + R_E2 下端断点
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g3.html';

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.addInitScript(() => {
    const patch = () => {
      if (typeof window.speakSeq !== 'function') { setTimeout(patch, 30); return; }
      window.speakSeq = function (parts, onDone) {
        (parts || []).forEach(p => { if (p && p.onStart) { try { p.onStart(); } catch (e) {} } });
        if (onDone) { try { onDone(); } catch (e) {} }
      };
    };
    patch();
  });
  await page.goto(PAGE + '?lvl=4&cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(800);
  await page.evaluate(() => {
    const d4 = S.draw[3];
    execAct('comp-src', 'vs-keep'); d4.found['comp-src'] = true;
    execAct('comp-vcc', 'vcc-gnd'); d4.found['comp-vcc'] = true;
    execAct('comp-vee', 'vee-gnd'); d4.found['comp-vee'] = true;
    execAct('comp-c1', 'cap-short'); d4.found['comp-c1'] = true;
    execAct('comp-c2', 'cap-short'); d4.found['comp-c2'] = true;
    execAct('comp-ce', 'cap-short'); d4.found['comp-ce'] = true;
    moveCompDown('comp-rc');
    execAct('comp-re2', 're2-remove'); d4.found['comp-re2'] = true;
  });
  await page.waitForTimeout(700);
  const r = await page.evaluate(() => {
    const out = {};
    ['wire-re2-a', 'comp-re2', 'wire-ree-b', 'wire-ce-a', 'wire-ce-b', 'comp-ce', 'fx-ce', 'fx-ce-tail',
     'node-re', 'fx-re2-wire', 'fx-gnd-jct', 'fx-gnd-rail', 'fx-tidy-lines', 'comp-vee', 'fx-vee'].forEach(id => {
      const el = document.querySelector('#circuit-wrap g[data-id="' + id + '"]') || document.getElementById(id);
      out[id] = el ? getComputedStyle(el).opacity : 'missing';
    });
    // 红框区域（SVG 585-665, 525-595）内可见图元
    const hits = [];
    document.querySelectorAll('#circuit-wrap path, #circuit-wrap line, #circuit-wrap circle').forEach(p => {
      const g = p.closest('g');
      if (!g) return;
      const gid = g.getAttribute('id') || g.getAttribute('data-id') || '';
      const st = getComputedStyle(g);
      if (st.opacity === '0' || st.visibility === 'hidden') return;
      let bb = null;
      try { bb = p.getBBox(); } catch (e) {}
      if (!bb) return;
      const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
      if (cx >= 585 && cx <= 665 && cy >= 525 && cy <= 595) hits.push(gid + ' (' + Math.round(cx) + ',' + Math.round(cy) + ')');
    });
    out.redboxHits = hits;
    // R_E2 下端断点：wire-ree-b 下端 vs comp-vee 顶
    const ree = document.querySelector('#circuit-wrap g[data-id="wire-ree-b"] path');
    const vee = document.querySelector('#circuit-wrap g[data-id="comp-vee"] circle');
    out.reeY2 = ree ? ree.getAttribute('d') : 'none';
    out.veeY = vee ? vee.getAttribute('cy') : 'none';
    return out;
  });
  console.log(JSON.stringify(r, null, 1));
  await page.screenshot({ path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/r93_diag.png', clip: { x: 380, y: 480, width: 400, height: 260 } });
  await browser.close(); process.exit(0);
})();
