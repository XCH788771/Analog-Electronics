/* 逻辑回归测试：cj-g4 第66轮「I_EQ 可选 → 4 条合法路线 + arrangeMixSubs 重排」
 * 直接从 cj-g4.html 抽取真实引擎函数与 seqs 配置，避免手抄分歧。 */
const fs = require('fs');
const path = require('path');

const HTML = path.join(__dirname, 'cj-g4.html');
const html = fs.readFileSync(HTML, 'utf8');

// 抽取 <script> 主体
const sm = html.match(/<script>([\s\S]*?)<\/script>/);
if (!sm) throw new Error('no <script> found');
const js = sm[1];

// 括号匹配切片（支持 { 或 [ 起始）
function sliceBrace(src, openIdx) {
  const open = src[openIdx], close = open === '{' ? '}' : ']';
  let depth = 0;
  for (let i = openIdx; i < src.length; i++) {
    if (src[i] === open) depth++;
    else if (src[i] === close) { depth--; if (depth === 0) return src.slice(openIdx, i + 1); }
  }
  throw new Error('unbalanced brace near ' + openIdx);
}

function extractFn(name) {
  const idx = js.indexOf('function ' + name + '(');
  if (idx < 0) throw new Error('fn not found: ' + name);
  const bi = js.indexOf('{', idx);
  return js.slice(idx, bi) + sliceBrace(js, bi);   // 含函数签名，否则裸块里 c 未定义
}

function extractSeqs() {
  const idx = js.indexOf('seqs:');
  if (idx < 0) throw new Error('seqs: not found');
  const bi = js.indexOf('[', idx);
  return sliceBrace(js, bi);
}

// 抽取 6 个引擎函数 + seqs
const fns = ['qSeqs', 'qLen', 'qSpan', 'qAllIds', 'qAccept', 'arrangeMixSubs'].map(extractFn);
const seqsSrc = extractSeqs();
const SEQS = eval(seqsSrc);

// 在受控作用域中定义函数（互相引用在调用期解析）
const factory = new Function(
  'LEVELS', 'S',
  fns.join('\n') + '\nreturn {qSeqs,qLen,qSpan,qAllIds,qAccept,arrangeMixSubs};'
);

// ---- 测试设施 ----
let pass = 0, fail = 0;
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function ok(cond, msg) { if (cond) { pass++; } else { fail++; console.log('  ✗ FAIL: ' + msg); } }
function show(arr) { return '[' + arr.join(',') + ']'; }

// 静态第3关 8 个子步（配置原序：fw/fill 成对，均带 qid），用于 arrangeMixSubs 验证
const MOCK_SUBS = [
  { type: 'fw', qid: 'q-vbq' }, { type: 'fill', qid: 'q-vbq' },
  { type: 'fw', qid: 'q-icq' }, { type: 'fill', qid: 'q-icq' },
  { type: 'fw', qid: 'q-ibq' }, { type: 'fill', qid: 'q-ibq' },
  { type: 'fw', qid: 'q-vceq' }, { type: 'fill', qid: 'q-vceq' }
];
// 动态第5关：无 qid（应维持配置原序）
const DYN_SUBS = [
  { type: 'fw', qid: null }, { type: 'fill', qid: null },
  { type: 'fw', qid: null }, { type: 'fill', qid: null },
  { type: 'fw', qid: null }, { type: 'fill', qid: null }
];

const LEVELS = [
  { phase: 0, kind: 'qorder', cfg: { kind: 'qorder', seqs: SEQS } },
  { phase: 0, kind: 'mix', cfg: { kind: 'mix', subs: MOCK_SUBS } },
  { phase: 1, kind: 'draw', cfg: { kind: 'draw' } },
  { phase: 1, kind: 'mix', cfg: { kind: 'mix', subs: DYN_SUBS } }
];
const S = {
  qorder: [{ done: [] }],
  mix: [null, { subs: [], steps: [], stepsOrig: MOCK_SUBS.slice() }, null, { subs: [], steps: [], stepsOrig: DYN_SUBS.slice() }]
};

const api = factory(LEVELS, S);
const { qSeqs, qLen, qSpan, qAllIds, qAccept, arrangeMixSubs } = api;
const C = LEVELS[0].cfg;

console.log('— 抽取校验 —');
ok(SEQS.length === 4, 'seqs 应为 4 条路线，实为 ' + SEQS.length);
console.log('  seqs =');
SEQS.forEach((s, i) => console.log('    R' + i + ': ' + show(s)));

console.log('\n— A. qAccept 并集（点错对象/可点集合） —');
ok(eq(qAccept(C, []), ['q-vbq']), 'd=[] → 仅 q-vbq，实得 ' + show(qAccept(C, [])));
ok(eq(qAccept(C, ['q-vbq']).sort(), ['q-icq', 'q-ieq']), 'd=[q-vbq] → {q-ieq,q-icq}，实得 ' + show(qAccept(C, ['q-vbq']).sort()));
ok(eq(qAccept(C, ['q-vbq', 'q-ieq']), ['q-icq']), 'd=[q-vbq,q-ieq] → 仅 q-icq，实得 ' + show(qAccept(C, ['q-vbq', 'q-ieq'])));
ok(eq(qAccept(C, ['q-vbq', 'q-icq']).sort(), ['q-ibq', 'q-vceq']), 'd=[q-vbq,q-icq] → {q-ibq,q-vceq}（无 I_EQ 路线在此分叉），实得 ' + show(qAccept(C, ['q-vbq', 'q-icq']).sort()));
ok(eq(qAccept(C, ['q-vbq', 'q-ieq', 'q-icq']).sort(), ['q-ibq', 'q-vceq']), 'd=[q-vbq,q-ieq,q-icq] → {q-ibq,q-vceq}，实得 ' + show(qAccept(C, ['q-vbq', 'q-ieq', 'q-icq']).sort()));
ok(eq(qAccept(C, ['q-vbq', 'q-icq', 'q-ibq']), ['q-vceq']), 'd=[q-vbq,q-icq,q-ibq] → 仅 q-vceq，实得 ' + show(qAccept(C, ['q-vbq', 'q-icq', 'q-ibq'])));

console.log('\n— B. qSpan 收敛（含 I_EQ=5 步 / 省略=4 步） —');
ok(qSpan(C, []) === 5, 'd=[] → span 5，实得 ' + qSpan(C, []));
ok(qSpan(C, ['q-vbq']) === 5, 'd=[q-vbq] → span 5，实得 ' + qSpan(C, ['q-vbq']));
ok(qSpan(C, ['q-vbq', 'q-ieq']) === 5, 'd=[q-vbq,q-ieq] → span 5，实得 ' + qSpan(C, ['q-vbq', 'q-ieq']));
ok(qSpan(C, ['q-vbq', 'q-icq']) === 4, 'd=[q-vbq,q-icq] → span 4（省略 I_EQ），实得 ' + qSpan(C, ['q-vbq', 'q-icq']));
ok(qSpan(C, ['q-vbq', 'q-ieq', 'q-icq']) === 5, 'd=[q-vbq,q-ieq,q-icq] → span 5，实得 ' + qSpan(C, ['q-vbq', 'q-ieq', 'q-icq']));
ok(qSpan(C, ['q-vbq', 'q-icq', 'q-ibq', 'q-vceq']) === 4, 'd=[q-vbq,q-icq,q-ibq,q-vceq] → span 4，实得 ' + qSpan(C, ['q-vbq', 'q-icq', 'q-ibq', 'q-vceq']));
ok(qSpan(C, ['q-vbq', 'q-ieq', 'q-icq', 'q-ibq', 'q-vceq']) === 5, 'd 满 R0 → span 5，实得 ' + qSpan(C, ['q-vbq', 'q-ieq', 'q-icq', 'q-ibq', 'q-vceq']));

console.log('\n— C. 完成判定（done.length >= qSpan，且为某路线前缀） —');
// R0/R1（5 步）
ok(!(['q-vbq', 'q-ieq'].length >= qSpan(C, ['q-vbq', 'q-ieq'])), '部分 R0 前缀不应判完成');
ok((['q-vbq', 'q-ieq', 'q-icq', 'q-ibq', 'q-vceq'].length >= qSpan(C, ['q-vbq', 'q-ieq', 'q-icq', 'q-ibq', 'q-vceq'])), 'R0 满 5 步应完成');
ok((['q-vbq', 'q-ieq', 'q-icq', 'q-vceq', 'q-ibq'].length >= qSpan(C, ['q-vbq', 'q-ieq', 'q-icq', 'q-vceq', 'q-ibq'])), 'R1 满 5 步应完成');
// R2/R3（4 步）
ok(!(['q-vbq', 'q-icq'].length >= qSpan(C, ['q-vbq', 'q-icq'])), '部分 R2 前缀不应判完成');
ok((['q-vbq', 'q-icq', 'q-ibq', 'q-vceq'].length >= qSpan(C, ['q-vbq', 'q-icq', 'q-ibq', 'q-vceq'])), 'R2 满 4 步应完成（不再被 qLen=5 误判）');
ok((['q-vbq', 'q-icq', 'q-vceq', 'q-ibq'].length >= qSpan(C, ['q-vbq', 'q-icq', 'q-vceq', 'q-ibq'])), 'R3 满 4 步应完成');

console.log('\n— D. arrangeMixSubs：第3关子步顺序 = 第2关实点顺序（fw/fill 成对） —');
function reorderFor(picked) {
  S.qorder[0].done = picked;
  S.mix[1] = { subs: [], steps: [], stepsOrig: MOCK_SUBS.slice() };
  arrangeMixSubs(1);
  return S.mix[1].subs.map(s => s.qid);
}
const R0 = reorderFor(['q-vbq', 'q-ieq', 'q-icq', 'q-ibq', 'q-vceq']);
const R1 = reorderFor(['q-vbq', 'q-ieq', 'q-icq', 'q-vceq', 'q-ibq']);
const R2 = reorderFor(['q-vbq', 'q-icq', 'q-ibq', 'q-vceq']);
const R3 = reorderFor(['q-vbq', 'q-icq', 'q-vceq', 'q-ibq']);
const exp0 = ['q-vbq', 'q-vbq', 'q-icq', 'q-icq', 'q-ibq', 'q-ibq', 'q-vceq', 'q-vceq'];
const exp1 = ['q-vbq', 'q-vbq', 'q-icq', 'q-icq', 'q-vceq', 'q-vceq', 'q-ibq', 'q-ibq'];
const exp2 = ['q-vbq', 'q-vbq', 'q-icq', 'q-icq', 'q-ibq', 'q-ibq', 'q-vceq', 'q-vceq'];
const exp3 = ['q-vbq', 'q-vbq', 'q-icq', 'q-icq', 'q-vceq', 'q-vceq', 'q-ibq', 'q-ibq'];
ok(eq(R0, exp0), 'R0 重排 → ' + show(R0) + '，期望 ' + show(exp0));
ok(eq(R1, exp1), 'R1（VCEQ 先于 IBQ）重排 → ' + show(R1) + '，期望 ' + show(exp1));
ok(eq(R2, exp2), 'R2（省略 I_EQ）重排 → ' + show(R2) + '，期望 ' + show(exp2));
ok(eq(R3, exp3), 'R3（省略 I_EQ，VCEQ 先于 IBQ）重排 → ' + show(R3) + '，期望 ' + show(exp3));
// 每对 fw/fill 必须相邻（成对）
function paired(arr) {
  for (let k = 0; k < arr.length; k += 2) if (arr[k] !== arr[k + 1]) return false;
  return true;
}
ok(paired(R0) && paired(R1) && paired(R2) && paired(R3), '所有路线 fw/fill 均成对相邻（不再「全框架在前、全填空在后」）');

console.log('\n— E. arrangeMixSubs：动态第5关无 qorder → 维持配置原序 —');
S.mix[3] = { subs: [], steps: [], stepsOrig: DYN_SUBS.slice() };
arrangeMixSubs(3);
const dynOrder = S.mix[3].subs.map((s, k) => k);
ok(eq(dynOrder, DYN_SUBS.map((_, k) => k)), '动态第5关子步索引保持原序，实得 ' + show(dynOrder));

console.log('\n— F. qAllIds —');
ok(eq(qAllIds(C).sort(), ['q-ibq', 'q-icq', 'q-ieq', 'q-vbq', 'q-vceq']), 'qAllIds → 5 个电量，实得 ' + show(qAllIds(C).sort()));

console.log('\n========== 结果 ==========');
console.log('PASS=' + pass + '  FAIL=' + fail);
process.exit(fail === 0 ? 0 : 1);
