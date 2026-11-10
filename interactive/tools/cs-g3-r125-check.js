// cs-g3 第125轮断言 + 截图：R_D/R_L 与受控源水平同轴、i_d 箭头 2 倍长度
const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = 'F:/AI建课/模电/WorkBuddy/archive/r125';
const fs = require('fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 2 });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.addInitScript(() => {
    window.speechSynthesis = { speak: u => setTimeout(() => { if (u.onend) u.onend(); }, 30), cancel: () => {}, getVoices: () => [] };
  });
  await page.goto(PAGE + '?lvl=1&tidy=1&ts=6&cb=' + Date.now());
  await sleep(900);

  const geom = await page.evaluate(() => {
    const rd = document.getElementById('rarr-rd');
    const rp = rd.querySelectorAll('path');
    const rl = document.querySelector('g[data-id="comp-rl"]');
    const ar = document.getElementById('fx-t-id');
    const src = document.getElementById('fx-t-src').querySelectorAll('path')[1].getAttribute('d');
    return {
      rd: { up: rp[0].getAttribute('d'), dn: rp[1].getAttribute('d'),
            y: rd.querySelector('rect').getAttribute('y'), labelY: rd.querySelector('text').getAttribute('y'),
            cx: +rd.querySelector('rect').getAttribute('x') + 13.5 },
      rl: { y: rl.querySelector('rect').getAttribute('y'), labelY: rl.querySelector('text').getAttribute('y'),
            top: document.querySelector('g[data-id="wire-rl-top"] path').getAttribute('d'),
            bot: document.querySelector('g[data-id="wire-rl-bot"] path').getAttribute('d') },
      arrow: { y1: ar.querySelector('line').getAttribute('y1'), y2: ar.querySelector('line').getAttribute('y2'),
               poly: ar.querySelector('polygon').getAttribute('points') },
      rhombus: src
    };
  });
  console.log('等效态几何:', JSON.stringify(geom, null, 0));

  const r = await page.evaluate(() => {
    const b = document.getElementById('rarr-rd').getBoundingClientRect();
    return { x: b.x, y: b.y, w: b.width, h: b.height };
  });
  await page.screenshot({ path: OUT + '/equiv-row.png', clip: { x: r.x - 40, y: r.y - 60, width: 400, height: 330 } });
  await page.screenshot({ path: OUT + '/equiv-page.png' });

  // 复位断言：重玩后 R_D 下挂件与 R_L 回原位
  const reset = await page.evaluate(() => {
    resetCircuit();
    const rd = document.getElementById('rarr-rd'), rl = document.querySelector('g[data-id="comp-rl"]');
    return { rdY: rd.querySelector('rect').getAttribute('y'), rdTop: rd.querySelectorAll('path')[0].getAttribute('d'),
             rlY: rl.querySelector('rect').getAttribute('y'), rlTop: document.querySelector('g[data-id="wire-rl-top"] path').getAttribute('d'),
             rlBot: document.querySelector('g[data-id="wire-rl-bot"] path').getAttribute('d') };
  });
  console.log('复位后:', JSON.stringify(reset));

  const ok = [], bad = [];
  const A = (c, m) => (c ? ok : bad).push(m);
  A(geom.rd.y === '344.5' && geom.rl.y === '344.5', 'R_D/R_L 体 y=344.5: ' + geom.rd.y + '/' + geom.rl.y);
  A(+geom.rd.y + 26.5 === 371 && +geom.rl.y + 26.5 === 371, '电阻体中心 371 = 菱形中心 371（同轴）');
  A(geom.rd.labelY === '377.5' && geom.rl.labelY === '377.5', 'R_D/R_L 标签基线 377.5 同轴: ' + geom.rd.labelY + '/' + geom.rl.labelY);
  A(geom.rd.up === 'M 690 216.25 V 344.5' && geom.rd.dn === 'M 690 397.5 V 525', 'R_D 上下引线随之: ' + geom.rd.up + ' | ' + geom.rd.dn);
  A(geom.rl.top === 'M 850 216.25 V 344.5' && geom.rl.bot === 'M 850 397.5 V 525', 'R_L 上下引线随之');
  A(geom.arrow.y1 === '244.5' && geom.arrow.y2 === '288.5' && geom.arrow.poly === '570,318.5 561,288.5 579,288.5', '箭头长度 74（2×37）: ' + JSON.stringify(geom.arrow));
  A((+geom.arrow.y1 + +geom.arrow.poly.split(' ')[0].split(',')[1]) / 2 === 281.5, '箭头中心仍 281.5 与 g_m·v_gs 同轴');
  A(reset.rdY === '317' && reset.rlY === '317' && reset.rdTop === 'M 690 216.25 V 317' && reset.rlTop === 'M 850 161.5 V 317' && reset.rlBot === 'M 850 370 V 525', '复位全复原: ' + JSON.stringify(reset));
  A(errors.length === 0, '无页面错误: ' + errors.join(' | '));
  console.log('通过: ' + ok.length + ' / 失败: ' + bad.length);
  bad.forEach(x => console.log('  ✗ ' + x));
  console.log(bad.length === 0 && errors.length === 0 ? 'CS-G3-R125-OK' : 'CS-G3-R125-FAIL');
  await browser.close();
})();
