#!/usr/bin/env node
/*
 * thumb-gen.js — 案例缩略图自动生成 / 刷新工具（第83轮新增）
 * 规约见 网站/interactive/制作规范.md「缩略图联动规约」。
 *
 * 背景：专题页案例卡显示的是「首次进页可见画面」的真实截图（thumb-<id>.png）。
 *       凡改动会出现在该画面里的内容（L1 题面/副标题/状态行、默认态电路与标注、
 *       标题区、已知行、案例行、得分区等），都必须用本工具重截缩略图。
 *
 * 用法（在 网站/interactive/tools/ 目录或任意目录运行均可，路径自动解析）：
 *   node thumb-gen.js                  # 刷新所有「过期」缩略图（页面 mtime > 图 mtime，或图缺失）
 *   node thumb-gen.js cj-g1 cj-g5      # 只刷新指定 id（可多个）
 *   node thumb-gen.js --all            # 强制全部重截（不论新旧）
 *   node thumb-gen.js --dry            # 只列出会刷新的 id，不截图不改版本
 *   node thumb-gen.js --no-bump        # 只截图，不击破 data.js 缓存版本、不递增 index ?v=
 *   node thumb-gen.js --wait 3500      # 自定义截图前等待毫秒数（默认 2800）
 *
 * 截图规格（与 制作规范.md 一致，勿随意改）：
 *   - 1280x720、deviceScaleFactor=1、隐藏滚动条
 *   - TTS stub：钩 speechSynthesis.speak 即时回放（onstart/onend 立即触发），
 *     避免无头环境语音挂起导致关卡引导语不落地、画面停在中间态
 *   - 真实时间等待 ≥2800ms：校徽金色粒子入场总时长约 2.5s，
 *     --virtual-time-budget 不推进合成器动画/SMIL，故必须用真实等待
 *   - file:// + ?cb= 时间戳绕过磁盘缓存
 *
 * 截图成功后自动做两件缓存击破（--no-bump 可关）：
 *   1. data.js 中该 thumbImg 追加/递增 ?v=N（img src 变化，浏览器必重新拉图）
 *   2. index.html 的 data.js?v= 递增 0.01（保证新 data.js 本身不被缓存）
 * 两处均为「读-改-写前复核」：写盘前重读文件，若已被外部修改则中止该步并报警。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

// ---------- 路径解析（本文件位于 网站/interactive/tools/） ----------
const TOOLS_DIR = __dirname;
const SITE = path.resolve(TOOLS_DIR, '..', '..');       // 网站/
const ROOT = path.resolve(SITE, '..');                  // 工作区根
const INTERACTIVE = path.join(SITE, 'interactive');
const ASSETS = path.join(SITE, 'assets');
const DATA_JS = path.join(SITE, 'js', 'data.js');
const INDEX_HTML = path.join(SITE, 'index.html');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const DEFAULT_WAIT = 2800;   // 校徽粒子动画 ≈2.5s + 余量（制作规约要求 ≥2.6s）

// ---------- 参数 ----------
const argv = process.argv.slice(2);
const flags = new Set(argv.filter(a => a.startsWith('--')));
const waitIdx = argv.indexOf('--wait');
const WAIT = waitIdx > -1 ? parseInt(argv[waitIdx + 1], 10) : DEFAULT_WAIT;
const DRY = flags.has('--dry');
const ALL = flags.has('--all');
const NO_BUMP = flags.has('--no-bump');
const IDS_ARG = argv.filter(a => !a.startsWith('--') && a !== argv[waitIdx + 1]);

// ---------- 从 data.js 解析 thumbImg 清单 ----------
function parseThumbs() {
  const src = fs.readFileSync(DATA_JS, 'utf8');
  const re = /thumbImg:\s*'(assets\/thumb-([A-Za-z0-9_-]+)\.png)(\?v=(\d+))?'/g;
  const map = new Map();   // id -> { ref, ver }
  let m;
  while ((m = re.exec(src)) !== null) {
    map.set(m[2], { ref: m[1], ver: m[4] ? parseInt(m[4], 10) : 0 });
  }
  return map;
}

function isStale(id) {
  const page = path.join(INTERACTIVE, id + '.html');
  const thumb = path.join(ASSETS, 'thumb-' + id + '.png');
  if (!fs.existsSync(page)) return { stale: false, why: '页面缺失' };
  if (!fs.existsSync(thumb)) return { stale: true, why: '缩略图缺失' };
  return {
    stale: fs.statSync(page).mtimeMs > fs.statSync(thumb).mtimeMs,
    why: '页面 ' + fmtTime(fs.statSync(page).mtimeMs) + ' vs 图 ' + fmtTime(fs.statSync(thumb).mtimeMs),
  };
}

function fmtTime(ms) {
  const d = new Date(ms);
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

// ---------- PNG 校验 ----------
function checkPng(p) {
  const b = fs.readFileSync(p);
  if (b.length < 33) return '文件过小';
  if (b[0] !== 0x89 || b[1] !== 0x50 || b[2] !== 0x4e || b[3] !== 0x47) return '非 PNG';
  const w = b.readUInt32BE(16), h = b.readUInt32BE(20);
  if (w !== 1280 || h !== 720) return `尺寸 ${w}x${h}（应为 1280x720）`;
  if (b.length < 15000) return `体积 ${(b.length / 1024).toFixed(0)}KB 过小（疑似空白/黑屏）`;
  return null;
}

// ---------- data.js 缓存击破 ----------
function bumpThumbVer(id) {
  const before = fs.readFileSync(DATA_JS, 'utf8');
  const re = new RegExp("(thumbImg:\\s*'assets/thumb-" + id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + "\\.png)(?:\\?v=\\d+)?'", 'g');
  let n = 0, nv = 0;
  const after = before.replace(re, (mm, base) => { n++; nv = (parseInt((mm.match(/\?v=(\d+)/) || [0, 0])[1], 10) || 0) + 1; return base + '?v=' + nv + "'"; });
  if (n !== 1) throw new Error(`data.js 中 thumb-${id} 锚点数=${n}（应为 1），未改写`);
  const now = fs.readFileSync(DATA_JS, 'utf8');
  if (now !== before) throw new Error('data.js 在截图期间被外部修改，已中止缓存击破（缩略图本身已生成）');
  fs.writeFileSync(DATA_JS, after);
  return nv;
}

// ---------- index.html 的 data.js?v= 递增 ----------
function bumpIndexVer() {
  const before = fs.readFileSync(INDEX_HTML, 'utf8');
  const re = /(data\.js\?v=)(\d+(?:\.\d+)?)/g;
  let n = 0, nv = '';
  const after = before.replace(re, (mm, pre, v) => {
    n++;
    nv = (parseFloat(v) + 0.01).toFixed(2);
    return pre + nv;
  });
  if (n !== 1) throw new Error(`index.html 中 data.js?v= 锚点数=${n}（应为 1），未改写`);
  const now = fs.readFileSync(INDEX_HTML, 'utf8');
  if (now !== before) throw new Error('index.html 在截图期间被外部修改，已中止递增（缩略图与 data.js 已更新）');
  fs.writeFileSync(INDEX_HTML, after);
  return nv;
}

// ---------- 单页截图 ----------
async function shoot(browser, id) {
  const pagePath = path.join(INTERACTIVE, id + '.html');
  const url = 'file:///' + pagePath.replace(/\\/g, '/') + '?cb=' + Date.now();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  try {
    // TTS stub：必须在页面脚本前注入
    await page.addInitScript(() => {
      const instant = () => {
        const ss = window.speechSynthesis;
        if (!ss) return;
        try { ss.getVoices = () => []; } catch (e) {}
        try {
          ss.speak = function (u) {
            try { if (u && u.onstart) u.onstart({}); } catch (e) {}
            setTimeout(() => { try { if (u && u.onend) u.onend({}); } catch (e) {}
              try { if (u && u.onerror && !u.__fired) { u.__fired = 1; } } catch (e) {} }, 0);
          };
        } catch (e) {}
        try { ss.cancel = () => {}; } catch (e) {}
      };
      instant();
      let k = 0;
      const t = setInterval(() => { instant(); if (++k > 40) clearInterval(t); }, 50);
    });
    const errs = [];
    page.on('pageerror', e => errs.push(String(e && e.message || e)));
    await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(WAIT);
    const probe = await page.evaluate(() => (document.body.textContent || '').replace(/\s+/g, ' ').slice(0, 90));
    const out = path.join(ASSETS, 'thumb-' + id + '.png');
    await page.screenshot({ path: out });
    return { errs, probe };
  } finally {
    await page.close();
  }
}

// ---------- 主流程 ----------
(async () => {
  if (!fs.existsSync(CHROME)) { console.error('未找到 Chrome: ' + CHROME); process.exit(2); }
  if (!fs.existsSync(DATA_JS)) { console.error('未找到 data.js: ' + DATA_JS); process.exit(2); }

  const thumbs = parseThumbs();
  if (thumbs.size === 0) { console.error('data.js 中未解析到任何 thumbImg 条目'); process.exit(2); }

  let targets = [];
  if (IDS_ARG.length) {
    for (const id of IDS_ARG) {
      if (!thumbs.has(id)) { console.error(`data.js 中无 thumb-${id}.png 条目（可用 --dry 查看清单）`); process.exit(2); }
      targets.push(id);
    }
  } else if (ALL) {
    targets = [...thumbs.keys()];
  } else {
    targets = [...thumbs.keys()].filter(id => isStale(id).stale);
  }

  console.log('=== 缩略图刷新计划（' + (DRY ? 'DRY 干跑' : '正式执行') + '）===');
  if (targets.length === 0) { console.log('无过期缩略图，全部最新。'); process.exit(0); }
  for (const id of targets) {
    const st = isStale(id);
    const thumb = path.join(ASSETS, 'thumb-' + id + '.png');
    const oldSize = fs.existsSync(thumb) ? (fs.statSync(thumb).size / 1024).toFixed(0) + 'KB' : '(缺失)';
    console.log(`  ${id.padEnd(10)} 旧:${oldSize.padStart(8)}  ${st.why}`);
  }
  if (DRY) process.exit(0);

  const browser = await chromium.launch({
    executablePath: CHROME, headless: true,
    args: ['--no-first-run', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1'],
  });

  let fail = 0;
  const done = [];
  try {
    for (const id of targets) {
      const thumb = path.join(ASSETS, 'thumb-' + id + '.png');
      const oldSize = fs.existsSync(thumb) ? fs.statSync(thumb).size : 0;
      let r;
      try {
        r = await shoot(browser, id);
      } catch (e) {
        console.log(`  [FAIL] ${id}: 截图异常 ${e.message}`);
        fail++; continue;
      }
      const bad = checkPng(thumb);
      if (bad) { console.log(`  [FAIL] ${id}: ${bad}`); fail++; continue; }
      const newSize = fs.statSync(thumb).size;
      const chg = newSize === oldSize ? '=' : (newSize > oldSize ? '↑' : '↓');
      let bumpInfo = '';
      if (!NO_BUMP) {
        try { bumpInfo = ' data.js ?v=' + bumpThumbVer(id); } catch (e) { console.log(`  [WARN] ${id}: ${e.message}`); }
      }
      done.push(id);
      console.log(`  [OK] ${id.padEnd(10)} ${(oldSize / 1024).toFixed(0)}KB → ${(newSize / 1024).toFixed(0)}KB ${chg}${bumpInfo}` +
        (r.errs.length ? `  pageerror: ${r.errs[0].slice(0, 60)}` : '  0 pageerror'));
      if (r.probe) console.log(`         画面文字: ${r.probe}`);
    }
  } finally {
    await browser.close();
  }

  if (!NO_BUMP && done.length) {
    try {
      const nv = bumpIndexVer();
      console.log(`=== index.html data.js?v= 已递增 → ${nv} ===`);
    } catch (e) {
      console.log('=== [WARN] index.html 递增失败: ' + e.message + '（请手动递增）===');
      fail++;
    }
  }

  console.log(`=== 汇总：成功 ${done.length} / ${targets.length}，失败 ${fail} ===`);
  if (done.length) console.log('缩略图已更新（专题页案例卡刷新即可见；缓存已被 ?v= 击破）。');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('运行异常: ' + (e && e.stack || e)); process.exit(2); });
