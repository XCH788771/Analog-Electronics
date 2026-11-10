// cs-g3 第124轮几何/显隐断言 + 截图
// ① 等效态 S 红点与 G 红点同轴（cx 均 442）
// ② i_d 箭头上移到受控源上端导线中段（263-300），g_m·v_gs 与箭头水平同轴（基线 291）
// ③ 第2关受控源右侧 g_m 标注显示（左缘 617 = 菱形右顶点 602 + 15），第1/3关隐藏
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/archive/r124';
const fs = require('fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30), cancel: () => {}, getVoices: () => [] };
  });
  await page.goto(PAGE + '?lvl=1&tidy=1&ts=6&cb=' + Date.now());
  await sleep(900);

  const geom = await page.evaluate(() => {
    const g = id => document.getElementById(id);
    const gd = g('fx-dot-g').querySelector('circle'), sd = g('fx-dot-s').querySelector('circle'), dd = g('fx-dot-d').querySelector('circle');
    const idl = g('fx-t-id'), line = idl.querySelector('line'), poly = idl.querySelector('polygon');
    const lab = g('fx-t-idlabel').querySelector('text');
    const tag = g('fx-gm-tag'), tagT = tag.querySelector('text');
    const src = g('fx-t-src').querySelectorAll('path')[1].getAttribute('d');   // 菱形
    const o = id => { const e = g(id); return e ? e.style.opacity : 'n/a'; };
    return {
      dotG: [gd.getAttribute('cx'), gd.getAttribute('cy')],
      dotS: [sd.getAttribute('cx'), sd.getAttribute('cy')],
      dotD: [dd.getAttribute('cx'), dd.getAttribute('cy')],
      arrow: { y1: line.getAttribute('y1'), y2: line.getAttribute('y2'), poly: poly.getAttribute('points') },
      idlabel: { x: lab.getAttribute('x'), y: lab.getAttribute('y') },
      gmTag: { opacity: o('fx-gm-tag'), x: tagT.getAttribute('x'), y: tagT.getAttribute('y') },
      idlabelOpacity: o('fx-t-idlabel'),
      rhombus: src
    };
  });
  console.log('L1(等效完成) 几何:', JSON.stringify(geom));

  // 第2关：显示 g_m 标注
  const lv2 = await page.evaluate(() => {
    window.getState().level = 2; render();
    const t = document.querySelector('#fx-gm-tag text');
    return { opacity: document.getElementById('fx-gm-tag').style.opacity, x: t.getAttribute('x'), y: t.getAttribute('y') };
  });
  console.log('L2 g_m 标注:', JSON.stringify(lv2));
  await page.screenshot({ path: OUT + '/l2-gm.png', clip: { x: 300, y: 180, width: 900, height: 500 } });

  // 第3关：隐藏
  const lv3 = await page.evaluate(() => {
    window.getState().level = 3; render();
    return document.getElementById('fx-gm-tag').style.opacity;
  });
  console.log('L3 g_m 标注 opacity:', lv3);

  // 回第1关等效态截图（箭头/标注位置目检）
  await page.evaluate(() => { window.getState().level = 1; render(); });
  await sleep(200);
  await page.screenshot({ path: OUT + '/l1-equiv.png', clip: { x: 380, y: 190, width: 420, height: 400 } });

  // 断言
  const ok = [];
  const bad = [];
  const A = (cond, msg) => (cond ? ok : bad).push(msg);
  A(geom.dotG[0] === '442' && geom.dotS[0] === '442', 'S 红点与 G 红点垂直同轴 (442): ' + geom.dotS[0]);
  A(geom.dotS[1] === '525', 'S 红点落在地线 y=525: ' + geom.dotS[1]);
  A(geom.arrow.y1 === '263' && geom.arrow.y2 === '285' && geom.arrow.poly === '570,300 561,285 579,285', '箭头移到上端导线中段: ' + JSON.stringify(geom.arrow));
  A(geom.idlabel.y === '291', 'g_m·v_gs 与箭头同轴(基线291): ' + geom.idlabel.y);
  A(geom.gmTag.opacity === '0', '第1关 g_m 标注隐藏: ' + geom.gmTag.opacity);
  A(geom.idlabelOpacity === '1', '第1关 g_m·v_gs 可见: ' + geom.idlabelOpacity);
  A(lv2.opacity === '1' && lv2.x === '617' && lv2.y === '381', '第2关 g_m 标注显示且距菱形15px: ' + JSON.stringify(lv2));
  A(lv3 === '0', '第3关 g_m 标注隐藏: ' + lv3);
  A(errors.length === 0, '无页面错误: ' + errors.join(' | '));

  console.log('通过: ' + ok.length + ' / 失败: ' + bad.length);
  bad.forEach(x => console.log('  ✗ ' + x));
  console.log(bad.length === 0 && errors.length === 0 ? 'CS-G3-R124-OK' : 'CS-G3-R124-FAIL');
  await browser.close();
})();
