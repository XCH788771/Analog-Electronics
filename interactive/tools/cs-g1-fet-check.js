const { chromium } = require('playwright-core');
const PAGE = 'file:///F:/AI建课/模电/WorkBuddy/网站/interactive/cs-g3.html';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args:['--no-first-run','--disable-gpu'] });
  const p = await b.newPage({ viewport:{width:1600,height:900} });
  await p.addInitScript(() => {
    window.speechSynthesis = { speak:u=>setTimeout(()=>{if(u.onend)u.onend();},20), cancel:()=>{}, getVoices:()=>[] };
    const oST=window.setTimeout; window.setTimeout=(fn,ms)=>oST(fn,Math.min(ms||0,40));
  });
  // 默认态
  await p.goto(PAGE+'?cb='+Date.now());
  await p.waitForTimeout(600);
  await p.screenshot({ path:'assets/shots/cs-g1-fet-default.png' });
  // 等效态：驱动到 t-equiv（隐藏 comp-t，显示 fx-tmodel）
  await p.evaluate(() => { chooseDrawOption('comp-vdd',{act:'vcc-gnd',ok:true}); chooseDrawOption('comp-c1',{act:'cap-short',ok:true}); chooseDrawOption('comp-c2',{act:'cap-short',ok:true}); chooseDrawOption('comp-cs',{act:'cap-short',ok:true}); chooseDrawOption('comp-rs',{act:'rs-remove',ok:true}); chooseMoveOption('comp-rg1',true); chooseMoveOption('comp-rd',true); chooseDrawOption('comp-t',{act:'t-equiv',ok:true}); });
  await p.waitForTimeout(600);
  await p.screenshot({ path:'assets/shots/cs-g1-fet-equiv.png' });
  await b.close();
  console.log('OK shots saved');
})().catch(e=>{console.error(e);process.exit(1);});
