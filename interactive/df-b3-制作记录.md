# df-b3（单入双出差分放大 · 案例1）制作记录

> 创建：2026-11-14（r142），会话「游戏-差分放大-单入双出差分放大案例1，如图 @image#1:Clipboard_Screenshot.png」。
> 基线：`.workbuddy/template_diffamp/` 模板族 + `差分放大-案例模板规范.md` 第八节变体矩阵 b3 列。
> 片段目录：`.workbuddy/tmp_dfb3/`（**改页须改片段重跑 build.py，禁直改生成的 HTML**）。

## 一、拓扑（相对 df-b1 的差异）

| 部位 | df-b1（双入双出） | df-b3（单入双出） |
|---|---|---|
| 左输入 | 端口 v_i1（±/文字/−） | 端口 **v_i**（`comp-vi1`→`comp-vi`，标注 v_i1→v_i），±/端子/负端接地全保留 |
| 右输入 | 端口 v_i2（880,230~490 两端子） | **删除端口**；`wire-in2`（772→880）末端直接挂接地符号：`comp-gnd2` 移位至 (880,230) 下挂（stub 230→248，三横杠 248/256/264，线宽 3/3.5/3/2.5 同 gnd1 口径） |
| 输出侧 | R_L 跨接两集电极 + v_o1/v_o2 绿点 + ＋v_o− | **与 b1 完全相同**（矩阵 b3「输出同 b1」） |
| 其余 | — | 不变（VCC 轨、R_C×2、T1/T2、发射极轨、恒流源、−V_EE） |

- 参考图（用户截图）与该拓扑一致：左侧竖排 ＋V_i−、顶部两绿点 V_o1/V_o2 夹 ＋V_o−。

## 二、公式与关卡（矩阵 b3 列，与 b1 同）

- A_vd = −β(R_C∥R_L/2)/r_be（R_L/2 横式 □/□）、R_id=2r_be、R_o=2R_C、A_vc=0、K_CMR=∞。
- **frag_CONFIG.js 关卡体零改动**（两关 48+52=100、14 计分单元、numPad/sym-key/洗牌全沿用）；仅改头注释与 STAGE_UNITS（`comp-vi1`→`comp-vi`、删 `comp-vi2`，仍 32 项）。
- frag_B2.html 仅一处：`q-veq` data-name 去掉「（基极经输入端口接地）」（右管基极是直接接地，原句不再全称成立）。

## 三、ANNOS 改动

键集合同步：删 `comp-vi2`；`comp-vi1`→`comp-vi`；`wire-in1/wire-in2/comp-gnd1/comp-gnd2` 释义按单入双出重写（wire-in2=「T2 基极→接地」）。遵守 r134：无结论性判断、无答案常数。

## 四、build.py（第 1、3 段）

- title：「单入双出差分放大 · 闯关挑战（案例1）- 游戏交互」。
- zoneA 案例行：「案例1：单入双出差分放大 · 求静态工作点与差模/共模动态指标」；已知行不变。

## 五、接入与版本

| 项 | 值 |
|---|---|
| data.js | df-b3 分支 game：`interactive/df-b3.html?v=1`，thumbImg `assets/thumb-df-b3.png?v=1`，desc「单端输入、双端输出差分对：求静态工作点与差模、共模动态指标」 |
| index.html | `data.js?v=12.68` → 12.69（手改）→ **12.70**（thumb-gen 自动递增，以现值为准） |
| 缩略图 | `网站/assets/thumb-df-b3.png`（thumb-gen --wait 生成，156,694 B） |

## 六、自检证据（全绿）

| 检查 | 结果 |
|---|---|
| `build.py --dry` | DRY OK：24 处替换全部唯一；生成 415,342 B |
| svg-layout-check | EXIT=0（②③④⑤⑥⑦⑨ 全过；⑧ rc1/rc2 两端导线不均衡 1.71 为 df-b1 同款提示，不判失败） |
| `dfb3_flow2.js` | FLOW_OK 4 断言：L1=48 进 L2、L2 满分 100 通关、附加路径（?lvl=2&ms=2 点 q-ieq2 作答）、无 JS 错误 |
| `deliver_check_dfb3.js` | http + file 双通道 DELIVER_OK（title/43 组/2 关） |
| `dfb3_probe_narration.js` | NARRATION_OK 81/81（禁用词 0 命中、padHint 7 条 ≤520px、data.js desc 不漏题） |
| 截图目检 | init/电路区 zoom/l1_ms1：右接地符号连接自然、v_i 竖排标注同参考图、输出区同 b1，无重叠 |

## 七、已知继承项（同 df-b1，勿单独改）

- zoneA 案例行 36px 末尾「…动态指标」被右侧面板遮住尾部（df-b1 定稿同款，模板族一致；如要改须四页统一并经用户裁决）。
- 调试钩子：`?lvl=1..2`、`&ms=n`（1 基）、`?lvl=done`；回归脚本 `dfb3_flow2.js` / `deliver_check_dfb3.js` / `dfb3_probe_narration.js`（均在 `.workbuddy/`）。


## ★ 第145轮（2026-11-15）：恒流源内阻 r_O 悬停并联示意
- 全 4 个差分页统一：默认隐藏的 `<g id="fx-ro-hover">` 置于 `#circuit-wrap` 末尾、`#fx-layer` 之后；hover `comp-io` → 浅蓝(#7dd3fc)虚线并联支路 + 27×53 内阻 + `r_O` 标注，整体 `opacity=0.7`；移开归 0。`pointer-events:none`，不影响点 `I_O` 作答。
- 几何：接点 `(536,380)/(536,490)` 接 I_O 上/下端引线（避开 y=350 公共发射极导线与 −V_EE 端子）；右侧竖线 x660；电阻中心 `(660,433.5)` 与恒流源圆同轴；标注 `x=683.5/y=444`；虚线 `stroke-dasharray="9 7"`。
- 生成链：本页由 `.workbuddy/tmp_dfbN/build.py` 生成（**改页须改片段重跑**）；同步 `frag_B2.html` + `build.py` 第 18 段（共 **25 处**补丁）。**本轮同时修正 tmp_dfb2/3/4 默认输出名误写 `df-b1.html` 的既有缺陷**（曾致 4 次重跑互相覆盖同一页）。
- 验收：`verify_r145.js` 本页 19 断言全 PASS；`svg-layout-check.py` EXIT=0；**FLOW_OK 满分 100**；DELIVER_OK 双通道；`probe_narration` OK；截图目检（df-b1 hover/idle）。
- 版本：`df-b3.html?v=1→2`；index `data.js?v=12.75`；首屏静态不变 → thumb 不动。详见 `制作规范.md` 第145轮规约。
- 备注：输入侧变体结构未动；仅新增悬停层与生成脚本补丁。
## ★ 第147轮（2026-11-15 晚）：r_O 并联净距减半 + hover 触发区统一
- 用户指令：「rO与恒流源并联离恒流源太远啦，将距离减小一半，而且只有将鼠标移到IO文字与箭头才能触发显示rO，改成移动到恒流源、文字或箭头上都触发显示rO。」
- 几何：以「恒流源圆右缘 562 → 电阻左缘」净距为准，84.5 → **42.25px**（精确减半）；右侧竖线/电阻中心 660 → **617.75**、电阻 x 646.5 → **604.25**、r_O 标注 x 683.5 → **641.25**，27×53 尺寸与上下接点 (536,380)/(536,490) 不变。**本页 r145 小节记的 x660 / 646.5 / 683.5 是旧值，以本条为准。**
- **本页无 r146 共模等效层**：恒流源圆区原本即可触发（未被透明层拦截），本轮统一改为几何热区，使文字→箭头→圆之间连续、无空隙闪烁。
- 触发改造：`build.py` 第 18 段 IIFE 改为 `comp-io.getBBox()` 几何热区（覆盖恒流源圆 + I_O 文字 + 箭头），用 `getScreenCTM().inverse()` 把鼠标换到局部坐标判定，±2px 余量；保留「恒流源不可见不显示」与「移开即隐藏」。上/下引线不在热区内，不误触发。
- 命中隔离：同一 IIFE 的 `syncHit()` 对 `#fx-layer` 内隐藏的 `fx-cm-*` 可点子组**及其全部后代**写 inline `pointer-events:none`（`rect.hot` 自带 CSS `all`，只设父组无效）；显示态只清本轮写入的 inline，父层 style 交还 `showCmTail/showCmSplit`；用 `MutationObserver` 监听 `#fx-layer` 的 style 变化即时同步，带 `syncing` 重入标志。
- 生成链：本页由 `tmp_dfb3/build.py`（25 处补丁）+ `frag_B2.html` 重跑生成；补丁 `patch_r147.py` / `patch_r147b.py` / `patch_r147c.py` / `patch_r147d.py`；备份 `.workbuddy/archive/bak-r147/`。`r146_layers.html` 与 r146 片段未改。
- 验收：`verify_r147.js` 本页 17 项断言全 PASS（4 页共 **68/68**）；`verify_r145.js` **76/76**；`probe_r146.js` **80/80**；本页 `dfb3_flow2.js` **FLOW_OK 满分 100**、`probe_narration` **81/81**、`deliver_check` 双通道 **DELIVER_OK**、`svg-layout-check.py` **EXIT=0**；截图 `shots-r147/df-b3_ro_hover.png` 目检（虚线框明显收窄、不压 I_O / −V_EE / 输出侧元件 / 右面板）。
- 版本：lab `df-b3.html?v=2→3`；index `data.js?v=12.76→12.77`；首屏静态不变（悬停层默认隐藏）→ **thumb 不动**。
- 详见 `制作规范.md` 第147轮规约。

## ★ 第148轮（2026-11-16）：步骤精简、真下标、节点补齐、K_CMR 三按钮、分值均分

- **分值**：本页仍 2 关，按动作均分改为 **Q点 34 / 动态 66**（旧 48/52 作废），配平通过。
- **L1 去重**：5 子步 → **4 子步**，删「V_EQ 代入符号」步；末步两行 `fullExpr`（`V_BQ=□`、`V_EQ=□−□=−□`）共 4 空。
- **按钮一致性**：`I_EQ` 填空步加 `padExtra: [tkl('r','be')]`，确认按钮上方显示 `r_be` 装饰按钮（不可点）。
- **节点与真下标**：新增 `node-vcc`（`(536,5)` 白圆）；单端输入 `comp-vi` 的 `i`、`v_i1/v_i2` 的 `i1/i2`、`r_O` 的 `O` 全部改 `tspan.sublow` 真下标。本页无共模等效关，故无置零地端节点。
- **K_CMR**：改 `K_CMR=□/□≈□`，`A_vd`/`A_vc`/`∞` 三按钮随机排序。
- **未改**：本页 `A_vc` 框架仍为 `A_vc=0`；双端输出的 `v_o1`/`v_o2` 保持原样。
- **生成链**：`gen_r148_config.py` 重写 `tmp_dfb3/frag_CONFIG.js`；`patch_r148.py`、`patch_r148b.py`（补 `node-vcc` 登记）、`patch_r148c.py`（`renderSubLine` guard）；本页 `build.py` **29 处**补丁；备份 `archive/bak-r148/`。
- **验收**：`probe_r148.js` 本页全过（4 页 **114/114**）；`dfb3_flow2.js` → `flow_r148.js df-b3` **FLOW_OK 满分 100**；`dfb3_probe_narration.js` **82/82**（`ms=5→4`）；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb3.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；截图 `shots-r148/new_b3_first.png` 目检通过。
- **版本**：lab `df-b3.html?v=3→4`；`thumb-df-b3.png?v=2→3`（重截）；index `data.js?v=12.78`。
- 详见 `制作规范.md` 第148轮规约。
## ★ 第149轮（2026-11-17）：R_o 步 r_be 按钮、乘法两空可交换、提示精简、符号键同款

- **需求 1**：`R_o 表达式` 步加 `padExtra: [tkl('r','be')]`，「确认」正上方出现 `r_be` 装饰按钮，与 `R_id` 步按钮区一致；`R_id = 2·r_be` 与 `R_o = 2·R_C` 两空改同构 `alts` 多解 + 同 `grp`（`rid-mul` / `ro-mul`）+ alts 项 `key`，`2·r_be` / `r_be·2`、`2·R_C` / `R_C·2` 均判对，`2·2`、`r_be·r_be`、`R_C·R_C` 被拒。
- **需求 2 / 3**：`renderMix` 顶部提示删除 `✓/▶/·` 步骤数串，只留「第 x / y 步 · 名称」；`K_CMR` 的 `A_vd`/`A_vc`/`∞` 三个 `.sym-key` 补与 `.num-key` 同款 CSS（紫底、白字、hover 黄描边），不再是黑色实心块。
- **用户裁决**：「交换顺序」＝乘法两空的 `2` 与 `r_be` 前后顺序任意（非两个指标的做题顺序互换）；`r_be` 补到 4 页 `R_o` 步。
- **生成链**：`patch_r149_config.py` 改 `tmp_dfb3/frag_CONFIG.js`；`patch_r149.py`（8 项 add）、`patch_r149b.py`（修 `pickBtn` 的 `data-ans` 在 alts 空下取空串的根因）改 `build.py`。本页 **38 处**补丁；备份 `archive/bak-r149/`；`template_diffamp/build.py __eq_test.html` 与 `df-b1.html` **424,331 B 字节一致**。
- **验收**：`probe_r149.js` 本页全过（4 页共 **74/74**）；`probe_r148.js` **114/114**；`flow_r148.js df-b3` **满分 100**；`dfb3_probe_narration.js` **82/82**；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb3.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；截图 `shots-r149/after_b1_L2_*` 同款目检通过（A 型两页引擎与配置一致）。
- **版本**：lab `df-b3.html?v=4→5`；`thumb-df-b3.png?v=3→4`；index `data.js?v=12.79`。
- 详见 `制作规范.md` 第149轮规约。

## ★ 第150轮（2026-11-17）：padExtra 恢复 hasNum（本页 R_o 按钮不变）

- **背景**：用户裁决单端输出案例（b2/b4）`R_o` 步「上方原本没有数字按钮，也移除 rbe 按钮」。本页为双端输出，`R_o = □·□` 有数字键盘与「确认」键，`r_be` 装饰按钮**保留**；`I_EQ1` 步的 `r_be` 也保留。
- **改动**：`patch_r150.py` 撤销 5 份 `build.py` 的 `r149-padextra-no-hasnum` 补丁，`padExtra` 渲染恢复 `hasNum` 条件（r148 口径）。本页所有带 `padExtra` 的步都有数字键盘，故视觉与交互**无变化**；本页补丁数 38→**37 处**。
- **同时**：B 型 `frag_B2.html` 移除拆分态两个地端交点白色节点（本页无 `fx-cm-split` 层，不受影响）。
- **验收**：`probe_r150.js` **38/38**（含本页 A 型 11 键+1 装饰按钮、`I_EQ1` 步 `r_be`）；`probe_r149.js` **74/74**；`probe_r148.js` **114/114**；`flow_r148.js df-b3` **满分 100**；`dfb3_probe_narration.js` **82/82**；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb3.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；模板等价基线与`df-b1.html` **424,242 B 字节一致**。
- **版本**：lab `df-b3.html?v=5→6`；thumb 首屏未变保持 `?v=4`；index `data.js?v=12.80`。
- 详见 `制作规范.md` 第150轮规约。

## ★ 第151轮（2026-11-17）：本页未改动

- 本轮只修单端输出两页（b2/b4）共模拆分态 `2r_O` 的电阻本体点击热区；本页无 `#fx-cm-split` 层，**页面字节与功能均未改变**（424,242 B，模板等价基线继续一致）。
- `probe_r151.js` 只跑 b2/b4；本页例行回归仍全绿：`probe_r150.js` **38/38**、`probe_r148.js` **114/114**、`flow_r148.js df-b3` **满分 100**、`dfb3_probe_narration.js` **82/82**、`deliver_check_dfb3.js` **DELIVER_OK**、布局 **EXIT=0**。
- 版本：lab 保持 `df-b3.html?v=6`；index 随 `data.js` 递增到 `12.81`。
- 详见 `制作规范.md` 第151轮规约。

## ★ 第152轮（2026-11-17）：本页未改动

- 本轮只把单端输出两页（b2/b4）拆分态 `2r_O` 下方地端下移 18px 与端口地端同轴；本页无 `#fx-cm-split` 层，**页面字节与功能均未改变**（424,242 B，模板等价基线继续一致）。
- `probe_r152.js` 只跑 b2/b4；本页例行回归仍全绿：`probe_r150.js` **38/38**、`probe_r149.js` **74/74**、`probe_r148.js` **114/114**、`verify_r147.js` **68/68**、`verify_r145.js` **76/76**、`flow_r148.js df-b3` **满分 100**、`dfb3_probe_narration.js` **82/82**、`deliver_check_dfb3.js` **DELIVER_OK**、布局 **EXIT=0**。
- 版本：lab 保持 `df-b3.html?v=6`、thumb `?v=4`；index 随 `data.js` 递增到 `12.82`。
- 详见 `制作规范.md` 第152轮规约。

## ★ 第153轮（2026-11-18）：Vi / r_O 下标缩小 1/3

- 4 页统一下标改造：新增 `.subsm { font-size:50%; baseline-shift:sub; }`，本页单端输入 `v_i` 的下标 `i` 与 hover `#fx-ro-hover` 的 `r_O` 的 `O` 由 75%→50%（父 37px：27.75→18.5px）；`v_o` / `v_o1` / `v_o2` 与面板 `tkl()` 生成的下标保持 75%。本页无共模置零层，`-VEE` 节点需求不适用。
- `probe_r153.js` **68/68**（本页 2 个 subsm、字号比 0.5 / 0.75、无 JS 错误）；例行回归 `probe_r150` 38/38、`probe_r149` 74/74、`probe_r148` 118/118、`verify_r147` 68/68、`verify_r145` 76/76、`flow_r148.js df-b3` 满分 100、`dfb3_probe_narration.js` 82/82、`deliver_check_dfb3.js` DELIVER_OK、布局 **EXIT=0**；等价基线 424,402 B。
- 截图：`shots-r153/df-b3_vi_r153.png`、`df-b3_ro_r153.png`。
- 版本：lab `df-b3.html?v=6→7`、thumb `?v=4→5`（首屏改动已重截）；index `data.js?v=12.83`。
- 详见 `制作规范.md` 第153轮规约。

## ★ 第155轮（2026-11-22）：用户裁决只改单端输出案例，本页完全回退
- 用户先要求 4 页上移 50px，随后裁决「只改单端输出的案例吧」→ 范围收窄为 B 型 `df-b2` / `df-b4`，**本页（A 型单入双出）不改动**。
- `patch_r155b.py` 已撤销 `tmp_dfb3` 的 `r155-expr-dy` 引擎补丁与 `exprDy: -50` 配置行；重新生成后本页与 `archive/bak-r155/`（r154 交付态）**字节完全一致（423,476 B）**；A 型生成链补丁数保持 **37**。
- 本页第 2 关 `R_o 表达式`（`?lvl=2&ms=8`）虚线框中心仍 **625.2**、与按钮区净距 70.4px（原样）；`probe_r155.js` **65/65** 已断言本页「Δ=0、无 exprDy、与 r154 字节一致」并验证真实鼠标仍可命中；截图 `shots-r155/df-b3_ro_r155.png` 为未改动对照。
- 版本：lab 回退 `df-b3.html?v=7`、thumb `?v=5` 保持；index `data.js?v=12.85`。详见 `制作规范.md` 第155轮规约。

