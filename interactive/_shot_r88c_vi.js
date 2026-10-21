// r88c: 截取左下角区域验证 comp-vi 新位置（初始态）
const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true, args: ['--no-first-run', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto('file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cj-g3.html?cb=' + Date.now(), { waitUntil: 'load' });
  await page.waitForTimeout(900);
  const op = await page.evaluate(() => {
    const g = document.querySelector('#circuit-wrap g[data-id="comp-vi"]');
    return g ? (g.style.opacity || getComputedStyle(g).opacity) : 'no';
  });
  console.log('初始态 comp-vi opacity =', op);
  await page.screenshot({ path: 'F:/AI建课/模电/WorkBuddy/网站/interactive/r88c_vi.png', clip: { x: 0, y: 200, width: 380, height: 420 } });
  console.log('clip 截图完成');
  await browser.close(); process.exit(0);
})();
