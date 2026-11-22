# df-b1 双入双出差分放大 · 案例1 制作记录（r123 三关重构定稿）

> 生成方式：`_game-template.html`（v2）+ 原子补丁脚本 `.workbuddy/tmp_dfb1/build.py`
>（19 处逐项唯一性校验后整体替换区 A/B/C/D 与 ★换案例 数据点）。**改本页请改 tmp_dfb1 下的片段后重跑 build.py**，勿直接手改散点。

## r123 三关重构（用户 5 条指令，2026-11-11）
1. **R_L 转横**：rect (509.5,124.5,53×27) 水平放在两集电极连线上（y=138）；文字竖排与电阻垂直同轴——
   `<text transform="rotate(-90 536 96)" x=536 y=96 anchor=middle>`（墨迹底距电阻上沿 ~10px）。
   **wire-col1/wire-col2（集电极→旧输出端的两段导线）删除**；绿点 v_o1/v_o2 移到 R_L 两侧 60px 处负载导线上
   (449.5/622.5,138)，文字在圆点正上方基线 y=117（墨迹底距点顶 10px）。
2. **删两个绘制关**（直流通路 draw、交流微变等效 draw 整体移除），页面变为 **三关**：
   Q点步骤 → Q点计算 → 动态指标。静态只算 **V_EQ、I_EQ1、I_EQ2**（I_CQ1/V_CEQ1 标注与计算全删）。
   图上标注（fx-layer 内 qlabel-layer）：I_EQ1 (451,336)、I_EQ2 (621,336)（发射极轨 y=350 上方两半段中央）、
   V_EQ (536,306)（恒流源上方节点之上）；**V_BE×2**（q-vbe1/q-vbe2，口径同 cj-g1：＋ 在基极导线下 15px、
   文字居中、－ 靠发射极侧；三枚热区各自独立避免盖住晶体管本体热区）；**β×2**（q-beta (366,238) 保留 +
   新增 q-beta2 (706,238) 镜像）。动态关 updateQlabels 只藏 q-veq，I_EQ1/I_EQ2/β/V_BE 常显。
3. **恒流源下移居中**：圆 (536,433.5)（轨 350→−V_EE 端子顶 517 的中点，上下引线各 57.5 对称），
   I_O 文字 (494,440)。
4. **常数 2 方框化 + 数字键盘**（numPad 引擎自 cj-g1 r112/113/114/120 移植）：I_EQ1/I_EQ2 框架改为
   `fr([{box:1}],[{box:1}])`；填空子步 `numPad:true`——数字 0-9 两行 5 列 + 第 6 列「确认」；常数空
   `{num:'2'}` 点数字逐位输入、「确认」提交（对→计分，错→提示重输不扣分）；切换虚线框自动提交（r120 口径）；
   选中框内黄字回显（pointer-events:none）。numPad 无常数空时（r_be 关）只渲染整行 pick-key 按钮。
5. **r_be 直接计算**（不再画等效电路）：r_be = r_bb′ + (1+β)·26mV/I_EQ；分母 I_EQ 为方框，
   **点右侧 I_EQ 按钮（pickBtn）或点电路中 I_EQ1/I_EQ2 标注均可作答**（ansIds ['q-ieq1','q-ieq2']）；
   β 点电路 β/q-beta2 标注。TQUIZ 六问、fx-tmodel/fx-tmodel-r/eq-layer/fx-eq-gnd/fx-dot-*/fx-virt-gnd、
   TQUIZ 相关引擎补丁（execAct 自定义动作/showEquiv/moveCompDown/tquiz 池等）**全部移除**（模板默认代码保留为死代码）。

## 关卡与计分（合计 100）
| 关 | 形式 | 分值 | 要点 |
|---|---|---|---|
| 1 Q点计算步骤 | qorder | 12 | q-ieq1 → q-ieq2 → q-veq（单路线，错一次−2） |
| 2 Q点计算 | mix | 36 | 框架 3×5（I_EQ1/I_EQ2/V_EQ）+ 填空：I_O 4+常数2 4 ×2 组 + V_BE 5；numPad 输入「2」 |
| 3 动态指标 | mix | 52 | 13 步各 4 分：框架 6×4（r_be/A_vd/R_id/R_o/A_vc/K_CMR）+ 填空 7×4（r_be 关 β+I_EQ、A_vd β+R_C+r_be、R_id r_be、R_o R_C） |

- 第 2 关子步顺序由 arrangeMixSubs 跟随第 1 关点选顺序（I_EQ1→I_EQ2→V_EQ）。
- V_EQ 填空：V_BQ=0 参考行 + V_EQ=−V_BE（点电路 V_BE 标注 q-vbe1/q-vbe2 作答）。

## 答案框架（教材口径，未变）
I_EQ1=I_EQ2=I_O/2；V_BQ=0 → V_EQ=−V_BE；r_be=r_bb′+(1+β)·26mV/I_EQ；
A_vd=−βR_C/r_be（双端输出）；R_id=2r_be；R_o=2R_C；A_vc=0；K_CMR=∞。

## numPad 引擎移植清单（build.py 标签）
`numStr-init`（S.numStr）、`blanks-num`（mix blanks 映射带 num/pickBtn）、`numpad-css`（.num-key/.pick-key）、
`mix-numpad`（renderMix 键盘渲染：hasNum 才画数字+确认；pickBtn 空渲染 I_EQ 按钮，无常数时占整行；
eTop 352+196）、`mix-echo`（回显）、`ui-click`（num-key/pick-key/blank-box 自动提交三路委托）、
`submitNum`（常数提交）、`answer-num`（常数空拦截电路点击）、`updateQlabels` 重写（常显+动态藏 V_EQ）。

## 布局口径（r123）
- R_L 水平 (509.5..562.5, 124.5..151.5)，竖排文字 rotate(-90 536 96)；v_o1/v_o2 绿点 (449.5/622.5,138)。
- 恒流源圆 (536,433.5) r26，引线 350..407.5 / 459.5..517；I_O 文字 (494,440)。
- 标注热区：q-ieq1 (419,304,64,42)、q-ieq2 (589,304,64,42)、q-veq (506,274,60,40)；
  q-vbe1 三热区 (237,242,36,38)/(254,283,60,42)/(312,292,36,38)，q-vbe2 镜像 (799/758/724)；
  q-beta (340,204,52,62)、q-beta2 (680,204,52,62)。
- STAGE_UNITS 单组（32 个可见交互单元），仅第 3 关 stageUnits:0 进动态时整级闪烁。

## r139 K_CMR 符号按钮随机顺序（2026-11-14）

用户反馈：「求KCMR时，上方按钮中，AVd、AVc和无穷三个随机顺序显示」。

- build.py `mix-numpad` sym 分支：进入 K_CMR 步时对 A_vd/A_vc/∞ 三键 **Fisher–Yates 洗牌一次**并
  记忆于 `st.btnOrder`——步骤内重渲染（选框/答错/回显）不重排，重新进入页面再随机；键与空的映射
  仍靠 `data-blank-idx`，乱序不影响判分。
- 自检：8 次加载采到 6 种顺序（0,2,1 | 2,0,1 | 2,1,0 | 1,0,2 | 0,1,2 …）；乱序点击按空计分
  ∞=2、A_vd=+1、A_vc=+1 共 4 分并通关（RAND_OK 3 断言）；flow2 FLOW_OK 满分 100；
  RBE 17/17 / NARRATION 82/82 / AVD_RL 26/26 / BLINK 12/12 / IEQ_SYNC 15/15 / IO_ARROW 11/11 /
  AUTO 7/7；svg-layout EXIT=0；DELIVER_OK；截图 r139_kcmr_rand.png 目检（第二行 7/8/9/A_vc/A_vd/∞/确认）。
- 版本：data.js lab `?v=19`；index `data.js?v=12.68`；thumb 保持 `?v=20`。

## r138 A_vc 干扰项改具体随机数字 −62（2026-11-13）

用户反馈：「求AVc时，另一个带方框的，给个100以内，除0和无穷之外的随机数字吧」。

- frag_CONFIG.js A_vc 框架（si8）干扰项 `A_vc=−□/□`（两个方框分式）→ `A_vc=−62`（shuf 10..99 一次定值，
  非 0 非 ∞）；正确项 `A_vc=0` 与 `A_vc=∞` 不变，三选项仍结构互异。**编译期写死不运行时随机**——
  每次加载随机会令框架选项、探针与回归不稳定。
- 验收：flow2 FLOW_OK 满分 100；RBE 17/17 / NARRATION 82/82 / AVD_RL 26/26 / BLINK 12/12 /
  IEQ_SYNC 15/15 / IO_ARROW 11/11 / AUTO 7/7；svg-layout EXIT=0；DELIVER_OK；
  截图 r138_avc_fw.png 目检（A=∞ / B=0 / C=−62，无溢出重叠）。
- 版本：data.js lab `?v=18`；index `data.js?v=12.67`；thumb 保持 `?v=20`。
- 运维：回归前须停掉遗留的 8799 预览服务（SRV.start 端口占用会令所有 Playwright 脚本静默崩溃）。

## r137 R_o 填空去 R_C 按钮（2026-11-13）

用户反馈：「求 RO 时，去掉上方的 RC 按钮」。

- frag_CONFIG.js R_o 填空步（si7）R_C 空**删 `pickBtn:true`**——只点电路 R_C 标注（comp-rc1/comp-rc2）作答，
  与 A_vd 步同路径；padHint 改「常数用数字键并确认；其余量点电路标注」（原「…或按钮」不再适用）。
  R_id 的 r_be 按钮（si5）保留。renderMix 的 qBtns 过滤天然适配：无 pickBtn 即不渲染按钮，numPad 只出 10 数字键＋确认。
- 回归：dfb1_flow2.js fills2 si7 改 `[{num:'2'},{id:'comp-rc1'}]`；FLOW_OK 满分 100（si7 84→88 走电路标注）。
  探针 NARRATION 82/82 / RBE 17/17 / AVD_RL 26/26 / BLINK 12/12 / IEQ_SYNC 15/15 / IO_ARROW 11/11 / AUTO 7/7；
  svg-layout EXIT=0；DELIVER_OK；截图 r137_ro_fill.png 目检（10 数字键＋确认、无 R_C 按钮）。
  注：调试钩子 ms 为 1 基（ms=8 ↔ si7），dfb1_probe_l3.js 为旧三关结构已弃用。
- 版本：data.js lab `?v=17`；index `data.js?v=12.66`；首屏静态未变，thumb 保持 `?v=20`。

## r136 R_id/R_o 常数 2 方框化 + K_CMR 改直接填空（符号按钮）（2026-11-12）

用户反馈：①「R_id 和 R_o 计算框架与填写表达式时，把常量 2 变成方框，手工填写，同样显示数字按钮和 r_be」；②「K_CMR 不选框架了，直接填写表达式，变成 K_CMR=方框/方框=方框，在上方显示 0-9、A_vd、A_vc、无穷的符号和确定按钮」。

### ① R_id / R_o：常数 2 方框化（参照 r_be / A_vd 的常数空口径）
| 项 | 改前 | 改后 |
|---|---|---|
| R_id 正确框架 | `2·□` | `□·□`（两框；干扰项 `□/□`、`□∥□` 结构仍互异） |
| R_id 填空 | 1 空 r_be 4 分 | **2 空**：`{num:'2',pts:0}` + r_be `{pickBtn:true,pts:4}`；`numPad:true` |
| R_o 正确框架 | `2·□` | `□·□`（干扰项 `□`、`□/□`） |
| R_o 填空 | 1 空 R_C 4 分 | **2 空**：`{num:'2',pts:0}` + R_C `{pickBtn:true,pts:4}` |
| 键盘 | 无 | 与 A_vd 步同款：10 数字键 + 右侧参数按钮（R_id 步按钮=r_be、R_o 步按钮=R_C，即「点标注或按钮」均可作答） |

分值不变：R_id/R_o 各「框架 4 + 填空 4 = 8」，第 2 关 52 / 总分 100 不变。注：R_o 的参数是 R_C，按钮文案随空自身 label 渲染（pickBtn 机制通用化），非字面 r_be。

### ② K_CMR：删框架关，改直接填空 + 符号按钮（引擎新增 sym-key）
- 子步由 `fw`（K_CMR=□/0/1 三选一，qpts 4）改为 `fill`：`fullExpr = K_CMR = □/□ = □`（横式分数，与 R_L/2 同款，不用嵌套分式）。
- **新空类型 `btn:[tokens]`**（答案即按钮本身，无 ansIds）：`{btn:[A_vd],pts:1}`、`{btn:[A_vc],pts:1}`、`{btn:[∞],pts:2}`＝4 分，关合计 52 不变。
- **numPad 符号键盘分支**（build.py `mix-numpad`）：子步 blanks 含 `btn` 空时走紧凑 7 列×2 行（键 62×50、间距 5），14 键＝0-9 十个数字键 + A_vd / A_vc / ∞ 三个 `sym-key` + 确认；底 538 < 表达式区 548。r_be/A_vd/R_id/R_o 等普通 numPad 步布局不受影响。
- **点击处理**（`ui-click` 新增 `.sym-key` 分支）：按钮即答案，直接完成对应空并计分/推进，无需先选框；重复点提示「该空已填好」。绿字回填走既有 `pickedLabel` 机制（`echo-label`）。
- **answerBlank 拦截**（build.py 新标签 `answer-btn`）：btn 空点电路标注 → 提示「该空请点表达式上方的符号按钮作答」，不误扣分。
- 语音/提示同步：L2 `announce`/`extra` 补「最后的共模抑制比直接点虚线框、用上方按钮填写」（r134 不漏题口径，无公式符号）；`subLine` 改「指标先选框架再填表达式；共模抑制比直接填」；K_CMR 步 `padHint`「点虚线框，再点上方对应按钮作答」（315px ≤ 520）。

### 验收
- `dfb1_flow2.js` `fills2` 改 `5:[{num:'2'},{btn:true}]`、`7:[{num:'2'},{btn:true}]`、新增 `9:[{sym},{sym},{sym}]`，`fill()` 加 sym 分支 → `FLOW_OK 满分 100`（L2 si=9 步 92→96，+4 与 1+1+2 吻合）。
- `dfb1_probe_narration.js` padHint 计数 4→7、新增 R_id/R_o/K_CMR 三条宽度断言 → `NARRATION_OK 82/82`。
- `dfb1_probe_rbe.js` FW 表删「L2 K_CMR 框架」（ms=10 已不是 fw）→ `RBE_OK 17/17`。其余全绿：`PROBE_OK 7/7`、`BLINK_OK 12/12`、`IEQ_SYNC_OK 15/15`、`IO_ARROW_OK 11/11`、`AVD_RL_OK 26/26`、`DELIVER_OK`、`svg-layout EXIT=0`。
- 截图目检：`r136_kcmr_init.png`（键盘 14 键两行整齐、表达式三框）、`r136_kcmr_done.png`（绿字 `K_CMR=A_vd/A_vc=∞`、得分 4/100）、`r136_rid_done.png`（`R_id=2·r_be` 绿字、r_be 按钮用后变暗）。

### 版本
lab `?v=16` / index `data.js?v=12.65`；首屏静态画面未变，thumb 保持 `?v=20` 不重截。

## r135 R_L 文字正向 + A_vd 分子改 R_C∥R_L/2（2026-11-12）

用户反馈：①「RL 旋转了好几次总是倒的，现在把 RL 文字变成正方向」；②「A_vd 正确结果应该是 R_C∥R_L/2，把原来的 R_L 变成分式，常数 2 也手动填，就像 r_be 一样上面显示数字按钮，将 I_EQ 的位置变成 r_be」。

### ① R_L 文字：彻底取消旋转
`frag_B1.html` 删掉 `transform="rotate(-90 536 96)"`（r123 曾 -90、r128 曾 +90、r133 又 -90，反复倒向）。`x=536 y=96 text-anchor=middle` 保持不变，**不写任何 rotate** = 正向水平横排。
- CTM 实测 `a=1,b=0,c=0,d=1`（单位阵，无旋转）；文字盒 45.25×44.59（37px 单行），与电阻盒 (527.5,412.5,53×27) 净隙 **16.9px**、中心差 4.4px，与 `v_o1/v_o2`、`R_C`、＋V_CC、顶轨均不相交。
- 探针踩坑：`getBBox()` 对 text 返回字体 em 框（R+下标 L 约 45×45 近正方），**不能用「宽>高」判横排**；判「正向」只能查 `transform` 为空 + CTM 单位阵。

### ② A_vd = −β·(R_C∥R_L/2)/r_be
| 项 | 改前 (r133) | 改后 (r135) |
|---|---|---|
| 正确框架 | `−□·(□∥□)/□`（4 框） | `−□·(□∥(□/□))/□`（**5 框**） |
| `fullExpr` | 同步 4 框 | 同步 5 框，与正确框架一致 |
| 干扰项 | `−□·□/□`、`−□·(□+□)/□` | `−□·(□∥□)/□`（漏折半，旧答案）、`−□·(□+□)/□`（并联误作相加）；三选项互异，干扰项不含 `/` |
| `blanks` | 4 空 β/R_C/R_L/r_be 各 3 分 | **5 空 β/R_C/R_L/常数2/r_be = 3/3/3/0/3**；常数空 `{num:'2',pts:0}` 走数字键盘不报分 |
| 键盘 | 无 numPad | `numPad:true` → 10 数字键 + 确认；第 5 空 `pickBtn:true`，右侧按钮由 `I_EQ` 改为 **`r_be`**（即「I_EQ 的位置变成 r_be」），点按钮或点电路 `comp-t1` 均可 |
| `padHint` | 无 | 「常数用数字键并确认；其余量点标注或按钮」（r134 不漏题口径，不含答案常数） |
| 分值 | 12 | **仍是 12**，第 2 关 52 / 总分 100 不变（Σ 校验 52/52） |

**工程权衡（重要）**：`R_L/2` 采用**横式分数 `□/□`**，不用 `fr` 嵌套上下分式。曾试过 `fr([{box:1}],[{box:1}])` 嵌套进主分式分子，2 倍放大截图显示内层分式上下溢出括号、`(` 与 `)` 高度错位、内层分母贴近主分数线；本页 `buildFrac` 按 `inkExtent` 固定 `-0.88fs/+0.88fs` 估算分式高度，不支持嵌套（规范的嵌套分式三条补丁是针对「分母含嵌套」且要改 `inkExtent`/`denBase`/高度缩字，会牵动 `r_be` 的 `26mV/I_EQ` 排版）。题面本身写作 `R_C∥R_L/2`，横式分数与之字面一致。若日后要上下分式，须先改 `build.py` 的表达式渲染引擎并全量回归。

### 验收
- **`.workbuddy/dfb1_probe_avd_rl.js` 重写 → `AVD_RL_OK 26/26`**：R_L 无 rotate/单位阵/净隙/不相撞；正确框架唯一 5 框、含 `∥` 与 `/`、三选项互异；5 空顺序与 3/3/3/0/3 分值、Σ=52；5 个虚线框编号 0~4 全在面板内；11 个数字键、1 个 r_be 按钮（idx=4 / ans=comp-t1）；**真实鼠标**点 `comp-rl` 填第 3 空、数字键输 2 填第 4 空、点 r_be 按钮填第 5 空。
- `dfb1_probe_narration.js` 的 padHint 计数 3→4，新增 A_vd 步宽度断言 → `NARRATION_OK 73/73`（新提示宽 399px ≤ 520、不泄露答案）。
- `dfb1_flow2.js` 的 `fills2[3]` 改 5 空序列 → `FLOW_OK` 满分 100。其余全绿：`PROBE_OK 7/7`、`BLINK_OK 12/12`、`IEQ_SYNC_OK 15/15`、`RBE_OK 18/18`、`IO_ARROW_OK 11/11`、`DELIVER_OK`（http+file）、`svg-layout EXIT=0`。
- 截图 `r135_rl_upright.png`、`r135_fw_zoom.png`（2× 框架选项）、`r135_fill_zoom.png`（2× 回填）、`r135_avd_fw.png`、`r135_avd_fill.png` 目检；重截首屏缩略图 `thumb-df-b1.png` 并目检 R_L 正向可读。

### 版本
lab `?v=15` / thumb `?v=20` / index `data.js?v=12.64`（后两处 thumb-gen 自动递增）。

## r134 语音提示精简：不漏题，只说流程（2026-11-12）

用户反馈：「精简语音提示，两管电路为恒流源一半，这不等于漏题了吗？语音提示，只简单提醒需要做什么，先做什么再做什么即可。」

### 根因
第 1 关 `announce` 把两个待求量的答案整句念了出来：「两管发射极电流各为恒流源的一半；公共发射极电位等于基极电位减去发射结电压」。此外面板 `padHint`、悬停气泡 `ANNOS.text`、讲解稿 `ANNOS.parts`、`data-name` 里也有同类直给结论（`I_EQ1=I_EQ2=I_O/2`、`V_BQ=0`、`V_EQ=V_BQ−V_BE`、虚地、共模抑制最强、常数 200/1/26 等）——学生照抄即可，题目失去考查意义。

### 改动（纯文案，分值/交互/几何一律不动）
| 位置 | 旧（漏题） | 新（只说流程） |
|---|---|---|
| L1 `announce` | 逐个计算静态工作点 + 两管电流各占一半 + V_EQ 等于 V_BQ 减 V_BE + 先符号后数值 + 常数按钮 + 答对48分 | 「进入第一关，计算静态工作点。先选表达式框架，再点虚线框填表达式；按面板顺序逐项完成，先算发射极电流，再算公共发射极电位。本关48分。」 |
| L1 `extra` | 「框架答对才进入…V_BQ、V_BE 点红色标注…」 | 「先选框架，再填表达式；常数用上方数字按钮输入，输入后点确认。」 |
| L1 `doneSay` | 「静态工作点的框架与表达式全部完成。」 | 「第一关完成，进入第二关。」 |
| L2 `announce` | 列常数 200/1/26、β 点标注、I_EQ 点按钮、六个指标全名 | 「进入第二关，计算动态性能指标。每个指标先选表达式框架，再点虚线框填表达式；按面板顺序逐项完成，先算晶体管输入电阻，再依次完成后面的指标。本关52分。」 |
| L2 `extra` | 「常数200、1、26用上方数字按钮…」 | 「先选框架，再填表达式；常数用数字按钮输入后点确认，其余量点电路标注或右侧按钮作答。」 |
| L2 `doneSay` | 列五项指标名 | 「全部关卡完成。」 |
| 3 处 `padHint` | 「分子点恒流源；分母点数字2」「V_BQ、V_BE 可点电路标注」「常数200、1、26点数字键；β点标注；I_EQ点按钮」 | 「点虚线框后点电路标注；常数用数字键并确认」「点电路标注作答；数值用数字键输入后确认」「常数用数字键并确认；其余量点标注或按钮」 |
| `ANNOS` 6 条 | `comp-io` 的 `I_EQ1=I_EQ2=I_O/2`、`node-base1`/`comp-vi1` 的 `V_BQ=0` 与 `V_EQ=V_BQ−V_BE`、`node-emitter` 虚地、`comp-vo` 共模抵消、`comp-rc1` 增益正比（text + parts 双份） | 只留元件作用/连接描述；需要结论处改「请在第一关/第二关里自己推导」 |
| `data-name` 2 处 | `node-base1`、`q-vbq` 含 `V_BQ=0` | 删去答案，保留「静态经输入端口接地」 |

**保留**（题设条件而非待求答案）：`comp-vi1/2` 的「差模输入的一半」、`v_i1=−v_i2`、T1/T2 对称、`fwQ` 题干、已知行、`subLine` 操作说明、报分串与全部计分逻辑。

**额外漏网**：`网站/js/data.js` 的案例卡 `desc` 原写「求 Q 点（I_EQ=I_O/2）…」，学生**进页面之前**就能看到答案，已改为「恒流源偏置差分对：求静态工作点与差模、共模动态指标」；探针加 ⓪ 断言守此条。

### 验收
- **新增 `.workbuddy/dfb1_probe_narration.js` → `NARRATION_OK 69/69`**：配置 6 条语音 + 2 条 subLine + 3 条 padHint 均不命中漏题正则、不含 `= ∥ /2`；两关 `announce` 含「先选→再→顺序」且 ≤90 字；**实际播报**（`announceLevel()` → `lastSay`）同样不漏题；ANNOS 全部 33 条 text/parts、所有 `data-name` 无直给结论；三处 padHint 实测宽 420 / 399 / 399px ≤ 520。
- `dfb1_probe_rbe.js` 的 `padHint 含 200` 断言改为「不泄露答案且不超 520」→ `RBE_OK 18/18`。
- 其余全绿：`FLOW_OK` 满分 100、`PROBE_OK 7/7`、`BLINK_OK 12/12`、`IEQ_SYNC_OK 15/15`、`IO_ARROW_OK 11/11`、`AVD_RL_OK 21/21`、`DELIVER_OK`、`svg-layout EXIT=0`。截图 `r134_pad_ieq.png` / `r134_pad_veq.png` / `r134_pad_rbe.png` 目检无裁切。
- 踩坑：探针禁用词正则里写 `I<sub>EQ1</sub>` 时，`</sub>` 的 `/` 会终止正则字面量，须写成 `<\/sub>`。

### 版本
lab `?v=14` / index `data.js?v=12.63`；**首屏静态内容无变化（语音不可见、padHint 与 ANNOS 均不在首屏），缩略图保持 `?v=19` 不重截**。

## r133 A_vd 分子计入负载 R_L + R_L 文字逆时针旋转（2026-11-12）

用户两条：①「AVd 框架不正确，分子应该是 βR_C∥R_L」；②「电路中的 R_L 文字，逆时针旋转 90 度」。

### ① A_vd 正确框架（frag_CONFIG.js，第 2 关 si=2 框架 / si=3 填空）
- 原式 `A_vd = −□·□/□`（分子 β·R_C，**漏了交流负载**）。按用户裁决改为 **`A_vd = −β·(R_C∥R_L)/r_be`**，分子 3 框 + 分母 1 框 = **4 框**：
  `fr([{box:1}, tk('·'), tk('('), {box:1}, tk('∥'), {box:1}, tk(')')], [{box:1}])`。
- 三个框架选项互异且正确项唯一：`−□·(□∥□)/□`（对）、`−□·□/□`（旧答案干扰）、`−□·(□+□)/□`（并联写成相加）。干扰项均不含 `∥`。
- `fullExpr` 与正确框架同步；blanks 由 3 空 → **4 空**，顺序 `β / R_C / R_L / r_be`；新增 `{ansIds:['comp-rl'], label:[tk('R','L')], pts:3}`，点电路中 R_L 电阻本体作答。
- **配平**：4 空各 `pts:3`（原 3 空各 4 分）＝12 分不变，`Σ(qpts+blanks)=52`、总分 100 不变。探针实测 Σ=52/52、flow2 满分 100。
- 口径留痕：用户明确「分子 βR_C∥R_L」，**未写 R_L/2**；若后续按半电路折半口径（双端输出每侧 R_L/2）需改 `R_C∥(R_L/2)`，须用户再确认，勿自行加。

### ② R_L 文字逆时针 90°（frag_B1.html）
- `transform="rotate(90 536 96)"` → **`rotate(-90 536 96)`**，`x/y` 不变（y=96 时文字墨迹底缘 406.6、电阻上缘 412.5，**净隙 5.9px**，与顺时针时观感一致，无需补偿位移）。
- 实测（SVG 根坐标，CTM 四角换算）：文字 bbox `(521,361.4)-(565.6,406.6)`，电阻 `(527.5,412.5)-(580.5,439.5)`，中心差 10.7px，与 R_C/v_o1/v_o2/＋V_CC 标注及顶轨均不相交。

### 踩坑（探针口径，非页面问题）
- `getBBox()` **不含元素自身 transform**，旋转文字必须把四角经 `getCTM()` 换算到根坐标后再与其它元件比较。
- 旋转后 bbox `44.6×45.3` 近似正方（`R` + 下标 `L` 局部约 45×44），**不能用「高 > 宽×1.5」判竖排**；改验 CTM 矩阵 `a≈0, b≈−1, c≈1, d≈0`（逆时针 90°）。
- 面板虚线框在分式 `<g transform>` 内，`getAttribute('x')` 是局部坐标（读到 0/-24.7 会误判越界）；用 `getBoundingClientRect()` 按 SVG 缩放换算。A_vd 分子三框 y≈541.8（比 r_be 的 548 略高，属分式正常位置）、分母框 y≈588.3，纵向不重叠、右缘 1417<1530。

### 验收
- **新增 `.workbuddy/dfb1_probe_avd_rl.js` → `AVD_RL_OK 21/21`**：旋转矩阵、墨迹净隙/同轴/不碰撞、三选项互异、正确项 4 框含 `∥`、Σ 配平、4 个虚线框位置、真实鼠标点 `comp-rl` 完成第 3 空并回填 `R_L`。
- `dfb1_flow2.js`（`fills2[3]` 补 `{id:'comp-rl'}`）FLOW_OK 满分 100；`PROBE_OK 7/7`、`BLINK_OK 12/12`、`IEQ_SYNC_OK 15/15`、`RBE_OK 18/18`、`IO_ARROW_OK 11/11`、`DELIVER_OK`（http+file 双通道，groups=44）、`svg-layout-check.py` EXIT=0。
- 截图 `r133_rl_ccw.png` / `r133_avd_fw.png` / `r133_avd_fill.png` 与重截缩略图目检通过。

### 版本
lab `?v=13` / thumb `?v=19` / index `data.js?v=12.62`（后两处由 `thumb-gen.js` 自动递增）；首屏 R_L 朝向变化，已重截缩略图。

## r132 I_O 箭头移到恒流源左侧 + r_bb′ 方框化取 200（2026-11-12）
1. **I_O 箭头/文字改到左侧**（`frag_B1.html`，局部坐标同 `#circuit-wrap`）：恒流源圆 cx=536,r=26 → 左缘 510；
   箭头 polygon 由右侧 x590–602 整体左移 100 → **x490–502**，右缘 502 与圆左缘 **净隙 8px**；
   I_O 文字 `text-anchor=end` 由 x=494 改到 **x=476.6**，箭头左缘 490 与文字**可见墨迹右缘 480 净隙 10px**。
   ⚠️ 37px 斜体 + 下标 O 有约 **3.4px 墨迹右溢**：若按字形盒把 x 写成 480，实测 `getBBox().right=483.4`、可见净隙只有 6.6px。
   箭头 y 不变（412–456，中心 434 与圆心 433.5 对齐），仍为一体 polygon（不用 line/path，避免 ④ 判悬空）；
   文字位移后已用真实鼠标复验 `comp-io` 仍可命中并完成 L1 的 I_O 空作答。
2. **r_be 的 r_bb′ 也方框化、取常数 200**（`frag_CONFIG.js`，参照 cj-g1 第 5 关 / 全站口径 `r_be=200+(1+β)·26mV/I_EQ`）：
   3 个框架选项 + `fullExpr` 中的 `tk('r',"bb'")` 全部改 `{box:1}`，正确式 `r_be=□+(□+□)·□mV/□`（**5 框**），
   错项 `(□−□)` 与 `□·(□+□)`（6 框）保证三选项结构互异、无重复。
   填空由 4 空→**5 空**：`{num:'200'}` / `{num:'1'}` / β(4分) / `{num:'26'}` / I_EQ(4分)，常数空 `pts:0` 不报分；
   **第 2 关 52 分、总分 100 不变**。`padHint`、`announce`、`extra` 同步补 200；已知行补 `r_bb′=200Ω`（`build.py` zoneA，26px 单行右缘实测 939 < 960 面板线）。
3. **布局检查器 ⑦ 修假阳性**（`tools/svg-layout-check.py`）：同组子形状（圆 + 自身箭头）净隙 8 < MIN_PITCH 15 被误判「元件拥挤」。
   规则改为 **⑦ 只比不同 `data-id` 元件组**，同组跳过；docstring 同步。已对全站其它 `.html` 回归，失败数 0。
4. **回归脚本同步**：`dfb1_flow2.js`（fills2[1] 补 200、I_EQ 空索引 3→4）、`dfb1_probe_rbe.js`（5 框/5 空、无字面量 200/1/26/r_bb′、已知行右缘）；
   新增 `dfb1_probe_io_arrow.js`（8/10px 双口径、垂直居中、不相交、真实鼠标命中、局部截图）。
5. **验收**：`svg-layout-check.py` EXIT=0；`FLOW_OK 满分100`、`PROBE_OK 7/7`、`BLINK_OK 12/12`、`IEQ_SYNC_OK 15/15`、
   `RBE_OK 18/18`、`IO_ARROW_OK 11/11`、`DELIVER_OK`（http+file，`#circuit-wrap g` 仍 44）；
   截图 `r132_io_arrow.png` / `r132_rbe_fw.png` / `r132_rbe_fill.png` 目检通过。
6. **版本**：`df-b1.html?v=12`、`thumb-df-b1.png?v=18`（首屏电路+已知行变化已重截）、`index.html data.js?v=12.61`（后两处由 thumb-gen 自动递增）。

## r131 I_EQ1 / I_EQ2 闪烁同步（2026-11-12）
1. **现象与诊断**：两标注都在闪但不同亮同灭。多帧同帧采样（`?lvl=1&ms=1/2` 与首屏自然进入）实测两者
   computed opacity 最大差 **0.419**（约 0.24s ≈ 0.27 个 0.9s 周期），q-ieq2 领先 q-ieq1。
2. **根因**：`renderMix` 静态关框架步 `fwBlinkQId()` 会调 `blinkGroup('q-ieq1', '#ff5252')` 做一次性红闪，
   只加在左标注；而 `g.red-blink { animation: redBlink 0.22s ease 3 }` 与 `g.calc-blink { animation: calcBlink 0.9s ... infinite }`
   **都设置 `animation` 简写属性**、选择器优先级相同 → 红闪期间 `calcBlink` 被覆盖 0.66s，
   类移除后连续动画**重新启动**；q-ieq2 从未被打断。0.9 − 0.66 = 0.24s，与实测相位差吻合。
3. **改法（从根上消除多动画源）**：
   - `frag_B2.html`：把 q-ieq1 / q-ieq2 两个 `g.interactive` 包进 `<g id="ieq-blink-pair">`（无 data-id，
     不进 ANNOS / STAGE_UNITS，点击热区不变）。
   - `build.py` 的 `updateQlabels`：**只给容器** `classList.toggle('calc-blink', flashing['q-ieq1'] || flashing['q-ieq2'])`；
     两个子 g 用 `isPair` 跳过自身 calc-blink。整对由**单一动画**驱动，任何后续事件都无法造成相位差。
   - `build.py` 新增补丁 `fw-blink-guard`：静态关框架步若目标标注（自身或 `.closest('.calc-blink')` 祖先）
     已在连续闪，则跳过一次性红闪——连续闪本身已起到定位作用，无需叠加。
   - 连等量仍「两个都闪」（符合 r129「等号左边的量」）；V_EQ 单独闪、动态关不闪、代入量常亮均不变。
4. 验收：新增 `.workbuddy/dfb1_probe_ieq_sync.js` **IEQ_SYNC_OK 15/15**（容器动画幅度 0.776、
   子标注不各自挂类、无 red-blink 叠加、两标注合成 opacity 最大差 **0.000**、无 JS 错误）；
   定格截图 `shots-dfb1/r131_ieq_bright.png`（0ms 最亮）/ `r131_ieq_dim.png`（450ms 最暗）目检：
   两个标注同时变亮/变淡，V_EQ 始终常亮。`dfb1_probe_blink.js` 同步更新为 **12/12**
   （I_EQ 两步的 `g.interactive.calc-blink` 集合改为空 ＋ 容器断言）。
   `dfb1_flow2.js` FLOW_OK 满分 100；`dfb1_probe_auto.js` 7/7；`dfb1_probe_rbe.js` 15/15；
   svg-layout EXIT=0；DELIVER_OK（`#circuit-wrap g` 43→44，即新增的容器 g，属预期）。
5. 版本：data.js lab `?v=11`、index `data.js?v=12.59`；首屏静态内容未变（仅动画机制），
   thumbImg 保持 `?v=16` 不重截，避免新图截到暗相位。

## r130 r_be 常数全方框化 + 框架题干删括号（2026-11-12）
1. **框架题干超框**：`fwQ` 由 `mkText(1010, BODY_TOP+40, 26, ...)` 单行渲染，面板可用宽仅 520px（LX 1010→RX 1530），不自动换行。用户指出 r_be 框架题干超框、要求「不用写那么多提示内容，删除括号部分」。
   自检实测 8 条题干原宽：I_EQ1 566 / V_EQ 556 / r_be 566（原带括号）/ A_vd 521 / R_id 569 / **R_o 667** / A_vc 617 / K_CMR 521 —— **7 条超框**，故按统一口径把 8 条全改为「〈量名〉 的框架：」（K_CMR 保留定义式 `= |A_vd / A_vc|`），删净所有括号补充说明。改后最宽 417px，全部 ≤520。
2. **r_be 常数全方框化**（参照 `cj-g1.html` 分压式共射案例1 第 5 关口径）：原来 `1`、`26` 是字面量，只有 β 与 I_EQ 是方框。现三个框架选项与 `fullExpr` 全部把常数改成 `{box:1}`：
   正确 `r_be = r_bb′ + (□+□)·□mV/□`；干扰 `(□−□)`、`□·(□+□)`（三项结构互异、无重复、无裸常数）。
   `r_bb′` 是给定符号而非常数，保留字面量（cj-g1 的 200 是数值故彼处方框化）。
3. **填空 2 空 → 4 空**：`{num:'1',pts:0}` → β(4 分) → `{num:'26',pts:0}` → I_EQ(4 分, pickBtn)。常数空只走数字键盘、答对不报分（`submitNum` 的 gain=0 分支走「正确。」），**第 2 关 52 分与总分 100 不变**。
   `padHint` 缩短为「常数1、26点数字键；β点标注；I_EQ点按钮」（避免 >520 裁切）；`announce`/`extra` 补常数输入说明。
   常数空出现后 `hasNum=true`，numPad 从「整行 I_EQ 按钮」变为「10 数字键 + 右侧 I_EQ 按钮 + 确认」；`needDot=false` 故小数点键不渲染，两者不冲突。
4. 回归脚本 `dfb1_flow2.js` 的 `fills2[1]` 改 4 空路径、附加路径的 I_EQ 空索引 1→3。
- 验收：新增 `.workbuddy/dfb1_probe_rbe.js` **RBE_OK 15/15**（8 条题干宽度、三框架无字面量常数且结构互异、4 空分值与位置、11 数字键+1 按钮、padHint 不超宽、无 JS 错误）；截图 `shots-dfb1/r130_rbe_fw.png` / `r130_rbe_fill.png` 目检无重叠裁切；`dfb1_flow2.js` FLOW_OK 满分 100；`dfb1_probe_auto.js` 7/7；`dfb1_probe_blink.js` 10/10；svg-layout EXIT=0；DELIVER_OK。
- 版本：首屏（L1 第 1 步题干）文字变更 → `thumb-gen.js df-b1 --wait 3200` 重截 `thumb-df-b1.png?v=16`；data.js lab `?v=10`、index `data.js?v=12.58`。

## r129 闪烁收敛：只闪等号左边的待求量（2026-11-11）
- 需求：填写 V_EQ 表达式时**只 V_EQ 闪烁，其它标注不要闪**（闪烁对象＝等号左边的待求量）。
- 根因：r128 给「V_EQ 代入符号」「V_EQ 代入数值」两个子步都写了 `blink:['q-veq','q-vbq','q-vbe1','q-vbe2']`，
  而 updateQlabels 中 `blink` 优先于 `qid`，导致参与代入的已知量 V_BQ / V_BE 也一起闪。
- 改法（`frag_CONFIG.js` 两处，重跑 build.py）：**删掉这两个 blink 字段**，回落到 `qid:'q-veq'` → 只闪 V_EQ 标注；
  片段头部与 build.py 的 updateQlabels 注释同步写明规则「只闪等号左边的待求量（qid），代入量不闪；blink 仅特殊需求使用」。
  I_EQ1=I_EQ2 连等属两个等号左边的量，q-ieq1 带 q-ieq2 同闪的规则保留；动态关仍不闪。
- 验收：新增 `.workbuddy/dfb1_probe_blink.js`（6 个调试钩子子步 + 多帧 computed opacity 采样，10 断言）
  **BLINK_OK 10/10**——V_EQ 框架/符号/数值三步闪烁集合均恰为 [q-veq]；q-vbq/q-vbe1/q-vbe2 全程
  animationName=none 且 opacity=1；q-veq 的 animationName=calcBlink 且 opacity 在 0.22~1 间变化。
  截图 `shots-dfb1/r129_veq_sym.png`、`r129_veq_num.png` 目检：V_BQ/V_BE 常亮、仅 V_EQ 变淡，面板无裁切重叠。
  `svg-layout EXIT=0`（2 条 R_C 导线不均结构性提示）；`dfb1_flow2.js` FLOW_OK 满分 100（L1 分步 8→16→24→32→48）；
  `deliver_check_dfb1.js` DELIVER_OK（http + file 双通道 groups 43）。
- 版本：data.js lab `?v=9`（thumbImg 未变，静态外观无改动不重生成缩略图）、index `data.js?v=12.57`。

## r128 V_EQ 两步代入与 V_BQ 标注（2026-11-11）
1. **R_L 文字顺时针旋转 90°**：rotate(-90)→rotate(90)（字头朝上、自上而下读）。
2. **新增基极节点 node-base1**：左管基极导线 (140,230)-(300,230) 中点 (220,230) 紫色圆 r=7（同公共发射极节点配色 #a78bfa）；ANNOS/STAGE_UNITS 同步登记。其上方 15px（文字盒底 208.2 → 圆顶 223）新增可点击标注 **q-vbq**（V_BQ，红色 28px 斜体，热区 190,174,60×48，不越基极导线墨迹顶 228.25）。
3. **V_EQ 框架改 □−□**：正确项 V_EQ=□−□（V_BQ−V_BE）；干扰项 V_EQ=□、V_EQ=−□（三者结构互异）。
4. **V_EQ 填空拆两步**（第 1 关变 5 子步）：
   - 子步 4「代入符号」：V_EQ=□−□，两空点电路 q-vbq / q-vbe1/2 标注（各 4 分，无键盘）；
   - 子步 5「代入数值」：两行 V_BQ=□ ＋ V_EQ=□−□=−□，四空各 4 分：V_BQ 空 num='0'；V_EQ 左项/右项/结果空为**多解空 alts**——点标注（V_BQ/V_BE）或输数值（0/0.7）均可，四种正确写法全覆盖（V_BQ−V_BE=−V_BE / 0−V_BE=−V_BE / 0−V_BE=−0.7 / 0−0.7=−0.7）。
5. **引擎多解空机制**（build.py 标签 blanks-num 加 alts、answer-alts、submitNum alts、echo-label、blankNum() 辅助）：alts=[{ids,label}|{num,label}]，点标注命中 ids 项或数值匹配 num 项均判对，回填 pickedLabel（命中项自己的标签，如 0.7）；纯常数空仍只走键盘。
6. **小数点键**：needDot（某空允许含'.'数值）时右侧空位渲染「.」键；输入规则——已含小数点忽略、直接点「.」补前导 0、位数上限 5。原 5 列×2 行键盘布局不变。
7. **闪烁按步配置**：子步新增 blink:[...] 字段优先于 qid；V_EQ 两步曾设 blink=['q-veq','q-vbq','q-vbe1','q-vbe2']（四标注同闪）——**r129 已删该字段，改为只闪 q-veq**；动态关隐藏 V_BQ/V_EQ。
8. 分值：第 1 关 = 框架 2×8 + 填空 8×4 = 48（总分 100 不变）。
- 验收：svg-layout EXIT=0；flow2 FLOW_OK 满分 100（L1 分步 8→16→24→32→48 精确，含 alts 点标注与 0.7 键盘路径）；probe_auto 7 断言全过；DELIVER_OK（groups 43）；data.js lab ?v=8 / thumb ?v=14、index 12.56。

## r127 五项调整（2026-11-11）
1. **I_O 下标缩小＋向下箭头**：tspan 加 font-size="60%"（22px）；圆右侧 x=596 加黄色向下箭头（polygon 一体成型——line/path 会被检查器判导线悬空，polygon 归符号类，距圆缘 28px 过间距检查）。
2. **删 I_EQ2 独立步骤**：I_EQ1 表达式已含 I_EQ1=I_EQ2，删其框架步与填空步 → 第 1 关 6 个计分单元各 8 分（框架 2×8 + 填空 I_O/常数2/V_BQ/V_BE 4×8 = 48，总分仍 100）。
3. **公共发射极节点改紫色**（#a78bfa，与 numPad 按钮同色系）。
4. **计算中标注连续闪烁**：CSS `g.calc-blink { animation: calcBlink 0.9s infinite }`＋updateQlabels 按 `L.cfg.subs[S.mix[i].si].qid` 点亮（运行时步对象不含 qid，必须从关卡配置取）；qid=q-ieq1 时 q-ieq2 同闪；动态关无 qid 不闪；算完随步骤推进自动停止。
5. **V_BQ 表达式填空**（无框架）：V_EQ 填空步 fullExpr 首行 V_BQ=0 改 V_BQ=□，blanks 加 `{num:'0'}`（数字键盘），该步开 numPad、padHint「V_BQ 点数字0确认；V_EQ 点电路 V_BE 标注」。
- 回归：flow2（L1 si 0..3，si=3 先 num 0 再点 V_BE）FLOW_OK 满分 100；probe_auto 7 断言全过；layout EXIT=0（箭头初版 line+path 被判「导线交叉/端点悬空」，改 polygon 后通过）；DELIVER_OK；data.js lab ?v=7 / thumb ?v=12、index 12.55。

## r126 常数自动提交（2026-11-11）
- 需求：常数空 numPad 输入后，点数字键盘/虚线框以外的**任何位置**（面板空白、电路、电量按钮、提醒等）都视为「确认」。
- 实现（build.py 标签 ui-click 尾部追加）： 全局捕获——有未提交缓冲（S.numStr 非空）且当前 selBox 指向未 done 的常数空时，先  再让原点击照常执行；排除 .num-key/.blank-box（各自分支已处理，防双重提交），**不排除 .pick-key**（点电量按钮先提交缓冲再作答）。护栏沿用：空缓冲不提交、错值只清空重输不扣分、finished/非 mix/非 fill 步不触发。
- 语义说明：自动提交后 selBox 清空，若随后要点电路标注作答其它空，需先点对应虚线框再点标注（「先选空、再点标注」流程不变）。
- 探针 ：7 断言（缓冲校验、点面板空白提交、点电路标注先提交常数、重新选空后电路作答正常、错值不锁定、无 JS 错误）全过。
- 验收：flow2 FLOW_OK 满分 100；layout EXIT=0；DELIVER_OK；data.js lab ?v=6 / thumb ?v=10、index 12.54。

## r125 两关重构（2026-11-11）
- 删除「Q点计算步骤」qorder 关（静态工作点不需计算顺序步骤）→ **两关：①Q点计算 48 分（8 个计分单元各 6 分 = 框架 3×6 + 填空 5×6）②动态指标 52 分（13 单元各 4 分）**。
- I_EQ1/I_EQ2 框架选项常数方框化并去重：A=□/□（正确，分式）、B=□、C=□·□——三选项结构互不相同、无裸常数 2；fwQ 文案同步缩短（「（对称均分）」「（两管完全对称）」，顺带解决贴边裁切）。R_id/R_o 的系数 2 是公式固有项、非待填常数，保留字面量；填空回填 label 的 2 保留。
- 回归脚本改  两关版（L1 48 / L2 52，附加 I_EQ 电路标注作答路径 ?lvl=2&ms=2）。调试钩子 ?lvl=1..2。
- 验收：svg-layout EXIT=0；FLOW_OK 4 断言满分 100（分步日志 L1 6→48、L2 48→100）；deliver_check DELIVER_OK；data.js lab ?v=5 / thumb ?v=8、index 12.53。

## r124 标注微调（2026-11-11）
- I_EQ1/I_EQ2 新增红色水平箭头（指向公共节点：左半段向右、右半段向左），间距口径：箭头墨迹距发射极导线墨迹顶（348.25）10px → 箭头中线 y=337；文字字形盒底（baseline+9.2）距箭头墨迹顶（335.5）10px → baseline=316；热区扩为 80×53 盖住文字+箭头。
- V_EQ 下移：文字盒底（328.2）距节点圆顶（343）15px → baseline=319。
- 实测口径：28px 斜体标注字形盒高 34.2、baseline→盒底 9.2（getBBox 实测，非 37px 的 +8 推算）。
- 验收：svg-layout EXIT=0；dfb1_flow2.js FLOW_OK 满分 100；deliver_check DELIVER_OK；data.js lab ?v=4 / thumb ?v=7、index 12.52。

## 测试（2026-11-11 r123）
- `svg-layout-check.py df-b1.html` EXIT=0（③ 零冲突、④⑤⑥ 全过；2 条 R_C 两端导线不均为结构性提示）。
- 全流程真实鼠标回归 `.workbuddy/dfb1_flow2.js`：**3 关全对，最终 100/100**（FLOW_OK 5 断言：
  L1=12、L2=48、L3=100+finished、I_EQ 电路标注作答路径、无 JS 错误）。
- 计分探针 `.workbuddy/dfb1_probe_l3.js`：L3 每步精确 +4（曾因配置分值错排 40/48→36/52 返工一次，
  根因是第 3 关实际 13 个计分单元而非 11 个，探针证实引擎计分无误）。
- 截图目检 `.workbuddy/shots-dfb1/n*.png`：R_L 横放竖字、绿点/文字位、标注三行、V_BE/β 双管、
  numPad 两态（数字键盘 / 整行 I_EQ 按钮）、结算屏 12/36/52 均正常；padHint 曾超面板宽裁切已缩短。

## 接入
- data.js df-b1 分支 `interactive/df-b1.html?v=3`（thumbImg ?v=4）；thumb-gen 重生成，index `data.js?v=12.50`。

## 遗留 / 后续
1. df-b2/b3/b4（双入单出/单入双出/单入单出）待建——可复用本页三关骨架（numPad 引擎已在 build.py 内）。
2. **A_vd 仍为空载式 −βR_C/r_be，图上已有 R_L**——是否改 −β(R_C∥R_L/2)/r_be 待用户裁决。
3. `_game-template.html` 本体未动（本页 numPad 为页面级移植）；模板是否升级 numPad 另议。


## ★ 第145轮（2026-11-15）：恒流源内阻 r_O 悬停并联示意
- 全 4 个差分页统一：默认隐藏的 `<g id="fx-ro-hover">` 置于 `#circuit-wrap` 末尾、`#fx-layer` 之后；hover `comp-io` → 浅蓝(#7dd3fc)虚线并联支路 + 27×53 内阻 + `r_O` 标注，整体 `opacity=0.7`；移开归 0。`pointer-events:none`，不影响点 `I_O` 作答。
- 几何：接点 `(536,380)/(536,490)` 接 I_O 上/下端引线（避开 y=350 公共发射极导线与 −V_EE 端子）；右侧竖线 x660；电阻中心 `(660,433.5)` 与恒流源圆同轴；标注 `x=683.5/y=444`；虚线 `stroke-dasharray="9 7"`。
- 生成链：本页由 `.workbuddy/tmp_dfbN/build.py` 生成（**改页须改片段重跑**）；同步 `frag_B2.html` + `build.py` 第 18 段（共 **25 处**补丁）。**本轮同时修正 tmp_dfb2/3/4 默认输出名误写 `df-b1.html` 的既有缺陷**（曾致 4 次重跑互相覆盖同一页）。
- 验收：`verify_r145.js` 本页 19 断言全 PASS；`svg-layout-check.py` EXIT=0；**FLOW_OK 满分 100**；DELIVER_OK 双通道；`probe_narration` OK；截图目检（df-b1 hover/idle）。
- 版本：`df-b1.html?v=19→20`；index `data.js?v=12.75`；首屏静态不变 → thumb 不动。详见 `制作规范.md` 第145轮规约。
- 备注：模板族生成 `__eq_test.html` 与现网本页**完全字节一致（418,171 B）**，等价基线恢复 `EQUIV_IDENTICAL`；r141 规约注释已随重跑同步进本页。
## ★ 第147轮（2026-11-15 晚）：r_O 并联净距减半 + hover 触发区统一
- 用户指令：「rO与恒流源并联离恒流源太远啦，将距离减小一半，而且只有将鼠标移到IO文字与箭头才能触发显示rO，改成移动到恒流源、文字或箭头上都触发显示rO。」
- 几何：以「恒流源圆右缘 562 → 电阻左缘」净距为准，84.5 → **42.25px**（精确减半）；右侧竖线/电阻中心 660 → **617.75**、电阻 x 646.5 → **604.25**、r_O 标注 x 683.5 → **641.25**，27×53 尺寸与上下接点 (536,380)/(536,490) 不变。**本页 r145 小节记的 x660 / 646.5 / 683.5 是旧值，以本条为准。**
- **本页无 r146 共模等效层**：恒流源圆区原本即可触发（未被透明层拦截），本轮统一改为几何热区，使文字→箭头→圆之间连续、无空隙闪烁。
- 触发改造：`build.py` 第 18 段 IIFE 改为 `comp-io.getBBox()` 几何热区（覆盖恒流源圆 + I_O 文字 + 箭头），用 `getScreenCTM().inverse()` 把鼠标换到局部坐标判定，±2px 余量；保留「恒流源不可见不显示」与「移开即隐藏」。上/下引线不在热区内，不误触发。
- 命中隔离：同一 IIFE 的 `syncHit()` 对 `#fx-layer` 内隐藏的 `fx-cm-*` 可点子组**及其全部后代**写 inline `pointer-events:none`（`rect.hot` 自带 CSS `all`，只设父组无效）；显示态只清本轮写入的 inline，父层 style 交还 `showCmTail/showCmSplit`；用 `MutationObserver` 监听 `#fx-layer` 的 style 变化即时同步，带 `syncing` 重入标志。
- 生成链：本页由 `tmp_dfb1/build.py`（25 处补丁）+ `frag_B2.html` 重跑生成；补丁 `patch_r147.py` / `patch_r147b.py` / `patch_r147c.py` / `patch_r147d.py`；备份 `.workbuddy/archive/bak-r147/`。`r146_layers.html` 与 r146 片段未改。
- 验收：`verify_r147.js` 本页 17 项断言全 PASS（4 页共 **68/68**）；`verify_r145.js` **76/76**；`probe_r146.js` **80/80**；本页 `dfb1_flow2.js` **FLOW_OK 满分 100**、`probe_narration` **82/82**、`deliver_check` 双通道 **DELIVER_OK**、`svg-layout-check.py` **EXIT=0**；截图 `shots-r147/df-b1_ro_hover.png` 目检（虚线框明显收窄、不压 I_O / −V_EE / 输出侧元件 / 右面板）。
- 版本：lab `df-b1.html?v=20→21`；index `data.js?v=12.76→12.77`；首屏静态不变（悬停层默认隐藏）→ **thumb 不动**。
- 详见 `制作规范.md` 第147轮规约。

## ★ 第148轮（2026-11-16）：步骤精简、真下标、节点补齐、K_CMR 三按钮、分值均分

- **分值**：本页仍 2 关，按「框架 + 填空」动作均分改为 **Q点 34 / 动态 66**（旧 48/52 作废），`Σ(qpts+blanks.pts)==pts` 配平通过。
- **L1 去重**：由 5 子步精简为 **4 子步**，删去「V_EQ 代入符号」步；只保留 `fw I_EQ1 → fill I_EQ1 → fw V_EQ → fill V_EQ`，最后一步 `fullExpr` 两行（`V_BQ=□` 与 `V_EQ=□−□=−□`）共 4 空，`alts` 支持点标注或数字键盘（0 / 0.7）。
- **按钮一致性**：`I_EQ` 填空步加 `padExtra: [tkl('r','be')]`，「确认」上方渲染 `r_be` 装饰按钮（`.pick-key.deco`，`pointer-events:none`，纯显示）。
- **节点与真下标**：新增 `node-vcc`（`(536,5)` 白圆，`+VCC` 引线与顶轨交汇）；`v_i1`/`v_i2`、`r_O` 的 `O`、`v_o1`/`v_o2` 全部改用 `tspan.sublow`（CSS `font-size:75%; baseline-shift:sub`）。**本页无共模等效关，故无置零地端节点**。
- **K_CMR**：框架改 `K_CMR=□/□≈□`，`A_vd`/`A_vc`/`∞` 三个符号按钮由 `st.btnOrder` 洗牌随机排序；旧的 `K_CMR=□/□` 两按钮口径作废。
- **未改**：本页 `A_vc` 框架仍为 `A_vc=0`（第 6 条裁决只针对单端输出两案例）；无 `v_o1/v_o2` 变更（双端输出本就如此）。
- **生成链**：`gen_r148_config.py` 重写 `tmp_dfb1/frag_CONFIG.js`；`patch_r148.py` 改 `frag_B1.html` / `frag_B2.html` / `build.py`；`patch_r148b.py` 补 `node-vcc` 的 `ANNOS`/`STAGE_UNITS` 登记（否则布局检查 EXIT=1）；`patch_r148c.py` 为 `renderSubLine` 加空值 guard。本页 `build.py` 共 **29 处**补丁；备份 `archive/bak-r148/`。`template_diffamp/build.py __eq_test.html` 与本页 **421,517 B 字节一致**。
- **验收**：`probe_r148.js` 本页断言全过（4 页共 **114/114**）；`dfb1_flow2.js` → `flow_r148.js df-b1` **FLOW_OK 满分 100**；`dfb1_probe_narration.js` **83/83**（L1 V_EQ 预览由 `ms=5` 改 `ms=4`）；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb1.js` 双通道 **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；截图 `shots-r148/new_b1_L1_ieq.png`、`new_b1_L1_veq.png`、`new_b1_L2_kcmr.png` 目检通过。
- **版本**：lab `df-b1.html?v=21→22`；`thumb-df-b1.png?v=20→21`（首屏静态已变，重截）；index `data.js?v=12.78`。
- 详见 `制作规范.md` 第148轮规约。
## ★ 第149轮（2026-11-17）：R_o 步 r_be 按钮、乘法两空可交换、提示精简、符号键同款

- **需求 1**：`R_o 表达式` 步加 `padExtra: [tkl('r','be')]`，「确认」正上方出现 `r_be` 装饰按钮，与 `R_id` 步按钮区一致；`R_id = 2·r_be` 与 `R_o = 2·R_C` 两空改同构 `alts` 多解 + 同 `grp`（`rid-mul` / `ro-mul`）+ alts 项 `key`，`2·r_be` / `r_be·2`、`2·R_C` / `R_C·2` 均判对，`2·2`、`r_be·r_be`、`R_C·R_C` 被拒。
- **需求 2 / 3**：`renderMix` 顶部提示删除 `✓/▶/·` 步骤数串，只留「第 x / y 步 · 名称」；`K_CMR` 的 `A_vd`/`A_vc`/`∞` 三个 `.sym-key` 补与 `.num-key` 同款 CSS（紫底、白字、hover 黄描边），不再是黑色实心块。
- **用户裁决**：「交换顺序」＝乘法两空的 `2` 与 `r_be` 前后顺序任意（非两个指标的做题顺序互换）；`r_be` 补到 4 页 `R_o` 步。
- **生成链**：`patch_r149_config.py` 改 `tmp_dfb1/frag_CONFIG.js`；`patch_r149.py`（8 项 add）、`patch_r149b.py`（修 `pickBtn` 的 `data-ans` 在 alts 空下取空串的根因）改 `build.py`。本页 **38 处**补丁；备份 `archive/bak-r149/`；`template_diffamp/build.py __eq_test.html` 与 `df-b1.html` **424,331 B 字节一致**。
- **验收**：`probe_r149.js` 本页全过（4 页共 **74/74**）；`probe_r148.js` **114/114**；`flow_r148.js df-b1` **满分 100**；`dfb1_probe_narration.js` **83/83**；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb1.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；截图 `shots-r149/after_b1_L2_ro_fw.png`、`after_b1_L2_ro_fill.png`、`after_b1_L2_kcmr.png`、`after_b1_L2_kcmr_hover.png`、`after_b1_L2_rid_reverse.png`、`after_b1_L2_ro_reverse.png` 目检通过。
- **版本**：lab `df-b1.html?v=22→23`；`thumb-df-b1.png?v=21→22`；index `data.js?v=12.79`。
- 详见 `制作规范.md` 第149轮规约。

## ★ 第150轮（2026-11-17）：padExtra 恢复 hasNum（本页 R_o 按钮不变）

- **背景**：用户裁决单端输出案例（b2/b4）`R_o` 步「上方原本没有数字按钮，也移除 rbe 按钮」。本页为双端输出，`R_o = □·□` 有数字键盘与「确认」键，`r_be` 装饰按钮**保留**；`I_EQ1` 步的 `r_be` 也保留。
- **改动**：`patch_r150.py` 撤销 5 份 `build.py` 的 `r149-padextra-no-hasnum` 补丁，`padExtra` 渲染恢复 `hasNum` 条件（r148 口径）。本页所有带 `padExtra` 的步都有数字键盘，故视觉与交互**无变化**；本页补丁数 38→**37 处**。
- **同时**：B 型 `frag_B2.html` 移除拆分态两个地端交点白色节点（本页无 `fx-cm-split` 层，不受影响）。
- **验收**：`probe_r150.js` **38/38**（含本页 A 型 11 键+1 装饰按钮、`I_EQ1` 步 `r_be`）；`probe_r149.js` **74/74**；`probe_r148.js` **114/114**；`flow_r148.js df-b1` **满分 100**；`dfb1_probe_narration.js` **83/83**；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb1.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；模板等价基线与本页 **424,242 B 字节一致**。
- **版本**：lab `df-b1.html?v=23→24`；thumb 首屏未变保持 `?v=22`；index `data.js?v=12.80`。
- 详见 `制作规范.md` 第150轮规约。

## ★ 第151轮（2026-11-17）：本页未改动

- 本轮只修单端输出两页（b2/b4）共模拆分态 `2r_O` 的电阻本体点击热区；本页无 `#fx-cm-split` 层，**页面字节与功能均未改变**（424,242 B，模板等价基线继续一致）。
- `probe_r151.js` 只跑 b2/b4；本页例行回归仍全绿：`probe_r150.js` **38/38**、`probe_r148.js` **114/114**、`flow_r148.js df-b1` **满分 100**、`dfb1_probe_narration.js` **83/83**、`deliver_check_dfb1.js` **DELIVER_OK**、布局 **EXIT=0**。
- 版本：lab 保持 `df-b1.html?v=24`；index 随 `data.js` 递增到 `12.81`。
- 详见 `制作规范.md` 第151轮规约。

## ★ 第152轮（2026-11-17）：本页未改动

- 本轮只把单端输出两页（b2/b4）拆分态 `2r_O` 下方地端下移 18px 与端口地端同轴；本页无 `#fx-cm-split` 层，**页面字节与功能均未改变**（424,242 B，模板等价基线继续一致）。
- `probe_r152.js` 只跑 b2/b4；本页例行回归仍全绿：`probe_r150.js` **38/38**、`probe_r149.js` **74/74**、`probe_r148.js` **114/114**、`verify_r147.js` **68/68**、`verify_r145.js` **76/76**、`flow_r148.js df-b1` **满分 100**、`dfb1_probe_narration.js` **83/83**、`deliver_check_dfb1.js` **DELIVER_OK**、布局 **EXIT=0**。
- 版本：lab 保持 `df-b1.html?v=24`、thumb `?v=22`；index 随 `data.js` 递增到 `12.82`。
- 详见 `制作规范.md` 第152轮规约。

## ★ 第153轮（2026-11-18）：Vi / r_O 下标缩小 1/3

- 4 页统一下标改造：新增 `.subsm { font-size:50%; baseline-shift:sub; }`，本页 `v_i1` / `v_i2` 与 hover `#fx-ro-hover` 的 `r_O` 的 `O` 由 75%→50%（父 37px：27.75→18.5px）；`v_o` / `v_o1` / `v_o2` 与面板 `tkl()` 生成的下标保持 75%。本页为双端输出、无共模置零层，`-VEE` 节点需求不适用。
- `probe_r153.js` **68/68**（本页 3 个 subsm、字号比 0.5 / 0.75、无 JS 错误）；例行回归 `probe_r150` 38/38、`probe_r149` 74/74、`probe_r148` 118/118、`verify_r147` 68/68、`verify_r145` 76/76、`flow_r148.js df-b1` 满分 100、`dfb1_probe_narration.js` 83/83、`deliver_check_dfb1.js` DELIVER_OK、布局 **EXIT=0**；模板等价基线与本页字节一致 **424,402 B**。
- 截图：`shots-r153/df-b1_vi_r153.png`、`df-b1_ro_r153.png`。
- 版本：lab `df-b1.html?v=24→25`、thumb `?v=22→23`（首屏改动已重截）；index `data.js?v=12.83`。
- 详见 `制作规范.md` 第153轮规约。

## ★ 第155轮（2026-11-22）：用户裁决只改单端输出案例，本页完全回退
- 用户先要求「4 个差分案例填写 R_o 表达式时上移 50px」，随后裁决「只改单端输出的案例吧」→ 范围收窄为 B 型 `df-b2` / `df-b4`，**本页（A 型双入双出）不改动**。
- `patch_r155b.py` 已撤销 `tmp_dfb1` / `template_diffamp` 的 `r155-expr-dy` 引擎补丁与 `exprDy: -50` 配置行；重新生成后本页与 `archive/bak-r155/`（r154 交付态）**字节完全一致（424,402 B）**，`__eq_test.html` 同值；A 型生成链补丁数保持 **37**。
- 本页第 2 关 `R_o 表达式`（`?lvl=2&ms=8`）虚线框中心仍 **absY 625.2**、与按钮区净距 **70.4px**（原样）；`probe_r155.js` **65/65** 已断言本页「Δ=0、无 exprDy、与 r154 字节一致」并验证真实鼠标仍可命中；截图 `shots-r155/df-b1_ro_r155.png` 为未改动对照。
- 版本：lab 回退 `df-b1.html?v=25`、thumb `?v=23` 保持；index `data.js?v=12.85`（随 `data.js` 递增）。详见 `制作规范.md` 第155轮规约。

