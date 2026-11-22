# df-b4（单入单出差分放大 · 案例1）制作记录

> 创建：2026-11-15（r144），会话「游戏-差分放大-单入单出差分放大案例1，如图 @image#1:Clipboard_Screenshot.png」（r141 命名规约：会话名＝首句原话）。
> 基线：`template_diffamp/` 模板族；片段目录 `.workbuddy/tmp_dfb4/`（**由 tmp_dfb2 复制**，改页须改片段重跑 build.py，禁直改生成的 HTML）。
> 参考图（用户截图白底合成后确认）：v_i 左管基极单端输入、T2 基极直接接地；R_L 竖放接**左管集电极**对地，v_o 取左管集电极对地；尾路恒流源 I_O→−V_EE（无 R_EE 电阻，内阻不画出）。

## 一、拓扑（相对 df-b1/b2/b3 的组合）

| 部位 | 取自 | 内容 |
|---|---|---|
| 输入侧 | **df-b3**（逐字复用） | `comp-vi1`→`comp-vi`（v_i 单端输入）；右管基极经 `wire-in2` 直接接地，`comp-gnd2` 移位至 (880,230) 短 stub 挂地 |
| 输出侧 | **df-b2**（逐字复用） | R_L 竖放 (456.5,158)、`comp-gndo` 输出接地 (470,239)、单绿点 (440,138)+v_o 文字、＋/v_o/－ 纵列 x=520（baseline 180/228/276） |
| 记号 | 本轮用户裁决 | 恒流源内阻 **R_EE → r_O**：已知行、ANNOS comp-io、A_vc 框架分母全部改 r_O；**电路图不画出内阻**（裁决原话「但不用将内阻画出来」） |
| comp-gnd1 | 本轮补改 | `data-name`「v_i1 负端」→「v_i 负端」（首轮遗漏，构建后补） |

- 输出与输入**同侧**（左管）→ 反相输出，与规范矩阵 b4 列 A_vd 吻合。

## 二、公式口径（用户裁决，矩阵 b4 列）

| 量 | 表达式 | 关卡形态 |
|---|---|---|
| A_vd | −β(R_C∥R_L)/(2·r_be)（R_L 全接入） | 同 b2：fw + fill 5 空（β3/R_C3/R_L3/常数2 0/r_be3 = 12） |
| R_id | 2·r_be | 同 b1/b2 |
| R_o | R_C（单端输出） | 同 b2：fw(单框正确) + fill 1 空 4 分 |
| A_vc | **−β(R_C∥R_L)/(r_be+2·r_O)**（有限小值，r_O＝恒流源内阻） | fw 三项全符号：正确式 / 差模分母误用式(2·r_be) / 0 |
| K_CMR | A_vd/A_vc（有限值） | 直接填空 `K_CMR=□/□`，符号按钮 2 键（2+2=4） |

- 第 1 关（Q 点）与 df-b1 逐字相同（I_EQ1=I_EQ2=I_O/2、V_EQ=−0.7V），48 分；第 2 关 52 分，Σ=100。
- 计分单元 10 个（b2 同款）；`frag_CONFIG` 仅改头注释、A_vc 框架分母记号、STAGE_UNITS（comp-vi1→comp-vi、删 comp-vi2，31 项）。

## 三、自检证据（2026-11-15，全绿）

| 检查 | 结果 |
|---|---|
| `patch_b4.py --dry` | 15 处片段补丁全部唯一（b1 基底原子补丁法） |
| `build.py --dry` → 生成 | DRY OK 24 处替换唯一；WROTE 415,005 B |
| `svg-layout-check.py df-b4.html` | **EXIT=0**（③ 0 / ③b 无 / ④ 全连 / ⑤ 0 / ⑥ 安全 / ⑦ 最小 95.5 OK；⑧ R_C 44:74 为 b1 固有提示） |
| `dfb4_flow.js` | **FLOW_OK 5 断言**：L1=48 进 L2、L2 满分 100 通关、r_be 点 I_EQ2、R_o 点 comp-rc2、无 JS 错误 |
| `deliver_check_dfb4.js` | **DELIVER_OK**（http+file 双通道，42 组 / 2 关） |
| `dfb4_probe_narration.js` | **NARRATION_OK 80/80**（禁用词 0 命中、padHint 7 条 ≤520px、data.js desc 不漏题） |
| 截图目检 | s_default / s_input / s_output：单入接地符号自然、输出区 R_L/gnd/绿点/极性列无重叠、已知行完整含「恒流源 I_O（内阻 r_O）」 |

## 四、接入与版本

| 项 | 值 |
|---|---|
| data.js | df-b4 分支 game：`interactive/df-b4.html?v=1`，thumbImg `assets/thumb-df-b4.png?v=2`（thumb-gen 自动递增），案例卡 desc「单端输入、单端输出差分对：求静态工作点与差模、共模动态指标」 |
| 缩略图 | `网站/assets/thumb-df-b4.png`（151,827 B，thumb-gen --wait） |
| index.html | `data.js?v=12.73` → **12.74**（thumb-gen 自动递增） |
| 回归脚本 | `.workbuddy/dfb4_flow.js` / `deliver_check_dfb4.js` / `dfb4_probe_narration.js`（dfb2 同名脚本 sed 克隆） |

## 五、已知继承项（勿单页擅改）

- zoneA 案例行 36px 尾部「…动态指标」被右侧面板遮尾：b1/b2/b3/b4 同款，须四页统一并经用户裁决。
- ⑧ 导线均衡 44:74：R_C 上引线 44 / 下引线 74，模板固有比例。
- 引擎段 9~17c 未触碰，模板等价基线不受影响。
- r_O 与 R_EE 是**兄弟案例的记号分歧**（b2 用 R_EE、b4 用 r_O）：如需统一记号须用户裁决并同步 b2/b4 与规范矩阵。


## ★ 第145轮（2026-11-15）：恒流源内阻 r_O 悬停并联示意
- 全 4 个差分页统一：默认隐藏的 `<g id="fx-ro-hover">` 置于 `#circuit-wrap` 末尾、`#fx-layer` 之后；hover `comp-io` → 浅蓝(#7dd3fc)虚线并联支路 + 27×53 内阻 + `r_O` 标注，整体 `opacity=0.7`；移开归 0。`pointer-events:none`，不影响点 `I_O` 作答。
- 几何：接点 `(536,380)/(536,490)` 接 I_O 上/下端引线（避开 y=350 公共发射极导线与 −V_EE 端子）；右侧竖线 x660；电阻中心 `(660,433.5)` 与恒流源圆同轴；标注 `x=683.5/y=444`；虚线 `stroke-dasharray="9 7"`。
- 生成链：本页由 `.workbuddy/tmp_dfbN/build.py` 生成（**改页须改片段重跑**）；同步 `frag_B2.html` + `build.py` 第 18 段（共 **25 处**补丁）。**本轮同时修正 tmp_dfb2/3/4 默认输出名误写 `df-b1.html` 的既有缺陷**（曾致 4 次重跑互相覆盖同一页）。
- 验收：`verify_r145.js` 本页 19 断言全 PASS；`svg-layout-check.py` EXIT=0；**FLOW_OK 满分 100**；DELIVER_OK 双通道；`probe_narration` OK；截图目检（df-b1 hover/idle）。
- 版本：`df-b4.html?v=1→2`；index `data.js?v=12.75`；首屏静态不变 → thumb 不动。详见 `制作规范.md` 第145轮规约。
- 备注：r144「电路图不画出内阻」裁决保留为**默认态**；本轮补「hover 才显示」，记号 `r_O` 与 r144 一致。


## ★ 第146轮（2026-11-15）：动态分析拆成 4 关 + 共模等效电路 + 兄弟案例记号统一

- **用户裁决**：动态分析「拆成 4 关」、记号「全案统一 r_O」；本页原本即用 `r_O`，只需把 `df-b2` 的 `R_EE` 统一过来（r144 遗留分歧本轮消解）。本页由 2 关改为 **4 关**：Q点 48 → 差模动态 28 → 共模等效 draw 8 → 共模指标 16 = 100。
- **第 3 关 draw**：三电源 hover 选「置零」→ 电压源「接地/断路」、恒流源「断路（保留 rO）/短路（含 rO）/断路（忽略 rO）」；门控完成长尾只留 `r_O` 接地并播 `splitHint`；hover `cm-ro-tail` 选「拆成两个 2rO」→ 两管发射极垂直向下、各经 27×53 的 `2r_O` 接独立地端。一级/二级菜单均随机顺序；4 个状态层 `fx-cm-*` 放在 `#fx-layer` 内以通过布局检查。
- **第 4 关**：`A_vc` 框架 2 → 完整竖式 8（7 框、分母 `r_be+(1+β)·2r_O`）→ 简化式 2（`≈ −(R_C∥R_L)/(2r_O)`）→ `K_CMR=□/□` 4（口径不变）。输入侧仍为 b3 的 `comp-vi` 单端 + T2 基极直接接地，输出侧仍为 b2 的 `R_L` 竖放对地。
- **生成链**：`tmp_dfb4/build.py` / `frag_CONFIG.js`（替换区 C 4 关，替换区 D `STAGE_UNITS` 本页输入侧不同故保留）/ `frag_ANNOS.js`（`cm-*`）/ `frag_B2.html`（`r146_layers.html`）；补丁 `patch_r146.py` / `patch_r146c.py`；备份 `archive/bak-r146/`。模板族与 `df-b1`/`df-b3` 未改。
- **验收**：`flow_r146.js df-b4` **16/16 FLOW_OK 满分 100**；`probe_r146.js` **80/80**；`narration_r146.js df-b4` **170/170**；`deliver_check_dfb4.js` 双通道 **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；拆分态截图目检通过。`dfb4_flow.js` / `dfb4_probe_narration.js` 改为薄包装。
- **版本**：lab `df-b4.html?v=2→3`；`thumb-df-b4.png?v=2→3`（页面 mtime 变化，随 b2 一并 `thumb-gen.js --wait 3500` 重截）；index `data.js?v=12.75→12.76`。
- **遗留**：zoneA 案例行 36px 尾部被面板遮（b1~b4 同款，待统一裁决）；`splitHint` TTS 口径是否逐字匹配用户原话待复核。详见 `制作规范.md` 第146轮规约。
## ★ 第147轮（2026-11-15 晚）：r_O 并联净距减半 + hover 触发区统一
- 用户指令：「rO与恒流源并联离恒流源太远啦，将距离减小一半，而且只有将鼠标移到IO文字与箭头才能触发显示rO，改成移动到恒流源、文字或箭头上都触发显示rO。」
- 几何：以「恒流源圆右缘 562 → 电阻左缘」净距为准，84.5 → **42.25px**（精确减半）；右侧竖线/电阻中心 660 → **617.75**、电阻 x 646.5 → **604.25**、r_O 标注 x 683.5 → **641.25**，27×53 尺寸与上下接点 (536,380)/(536,490) 不变。**本页 r145 小节记的 x660 / 646.5 / 683.5 是旧值，以本条为准。**
- **根因（本页特有）**：r146 隐藏的 `fx-cm-ro-tail` 层子组 `pointer-events=all` 与 `rect.hot` 的 CSS `pointer-events:all` 仍参与命中，透明热区 `x512~608/y397~467` 盖住恒流源圆 `x510~562/y407~460`；网格扫描圆区 81/81 采样点归属 `cm-ro-tail`，故 `comp-io` 的 `mouseenter` 只在未被覆盖的 I_O 文字/箭头处触发。
- 触发改造：`build.py` 第 18 段 IIFE 改为 `comp-io.getBBox()` 几何热区（覆盖恒流源圆 + I_O 文字 + 箭头），用 `getScreenCTM().inverse()` 把鼠标换到局部坐标判定，±2px 余量；保留「恒流源不可见不显示」与「移开即隐藏」。上/下引线不在热区内，不误触发。
- 命中隔离：同一 IIFE 的 `syncHit()` 对 `#fx-layer` 内隐藏的 `fx-cm-*` 可点子组**及其全部后代**写 inline `pointer-events:none`（`rect.hot` 自带 CSS `all`，只设父组无效）；显示态只清本轮写入的 inline，父层 style 交还 `showCmTail/showCmSplit`；用 `MutationObserver` 监听 `#fx-layer` 的 style 变化即时同步，带 `syncing` 重入标志。
- 生成链：本页由 `tmp_dfb4/build.py`（30 处补丁）+ `frag_B2.html` 重跑生成；补丁 `patch_r147.py` / `patch_r147b.py` / `patch_r147c.py` / `patch_r147d.py`；备份 `.workbuddy/archive/bak-r147/`。`r146_layers.html` 与 r146 片段未改。
- 验收：`verify_r147.js` 本页 17 项断言全 PASS（4 页共 **68/68**）；`verify_r145.js` **76/76**；`probe_r146.js` **80/80**；本页 `dfb4_flow.js` **FLOW_OK 满分 100**、`probe_narration` **170/170**、`deliver_check` 双通道 **DELIVER_OK**、`svg-layout-check.py` **EXIT=0**；截图 `shots-r147/df-b4_ro_hover.png` 目检（虚线框明显收窄、不压 I_O / −V_EE / 输出侧元件 / 右面板）。
- 版本：lab `df-b4.html?v=3→4`；index `data.js?v=12.76→12.77`；首屏静态不变（悬停层默认隐藏）→ **thumb 不动**。
- 详见 `制作规范.md` 第147轮规约。

## ★ 第148轮（2026-11-16）：4 关分值均分、单端输出标注、A_vc 同页、共模绘制即时显示 r_O

- **分值**：4 关按动作均分改为 **Q点 22 / 差模动态 34 / 共模等效 draw 8 / 共模指标 36**（旧 48/28/8/16 作废），配平通过。
- **L1 去重**：5 子步 → **4 子步**，删「V_EQ 代入符号」步；`I_EQ` 步加 `padExtra: [tkl('r','be')]`（确认上方 `r_be` 装饰按钮）。
- **需求 2/3/4（电路）**：新增 `node-vcc`（`(536,5)`）；VCC/VEE 置零层与拆分态两个独立地端各补白色节点。负载接左集电极 → 绿色 `v_o` 改 **`v_o1`**、`node-col2` 变绿并右侧加 **`v_o2`**；单端输入 `comp-vi` 的 `i`、`v_i1/v_i2` 的 `i1/i2`、`r_O`/`2r_O` 的 `O` 全部 `tspan.sublow` 真下标。
- **K_CMR**：改 `K_CMR=□/□≈□`，`A_vd`/`A_vc`/`∞` 三按钮随机排序。
- **需求 3/6（A_vc）**：L4 由 4 子步合并为 **3 子步**；三项框架全为分式（`A_vc=0` 换成双端输出分式框架）；完整式与简化式同一步两行、共 10 框 10 空，简化式分子分母全手工填写；上方按钮由 `2rO` 换 `r_be`；`exprTop:536 / exprStep:88 / exprSize:36` 上移缩小。
- **需求 5（共模绘制关）**：恒流源圆 / `I_O` 文字 / 箭头三触发点统一弹菜单（在电路所属 `svg` 上监听 `mousemove`）；`cm-io-open` 立即 `showCmTail()` 显示 27×53 的 `r_O`；菜单随机 + `html` 富文本下标；`MutationObserver` 防悬停叠影。
- **生成链与修复**：`gen_r148_config.py` 重写 `tmp_dfb4/frag_CONFIG.js`；`patch_r148.py`、`patch_r148b.py`（补 `node-vcc` 登记，修布局检查 EXIT=1）、`patch_r148c.py`（`renderSubLine` guard，修 draw 关 `undefined`）。本页 `build.py` 共 **34 处**补丁；备份 `archive/bak-r148/`。
- **回归脚本**：`dfb4_flow.js` / `dfb4_probe_narration.js` 改为薄包装，统一走 `flow_r148.js` / `narration_r148.js`。
- **验收**：`probe_r148.js` 本页全过（4 页 **114/114**）；`flow_r148.js df-b4` **16/16 FLOW_OK 满分 100**；`narration_r148.js df-b4` **166/166**；`probe_r148_draw.js` **26/26**；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb4.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；截图 `new_b4_first.png`、`df-b4_r148_all_zero.png` / `df-b4_r148_split.png` 目检通过，**面板 `undefined` 已消失**。
- **版本**：lab `df-b4.html?v=4→5`；`thumb-df-b4.png?v=3→4`（重截）；index `data.js?v=12.78`。
- 详见 `制作规范.md` 第148轮规约。
## ★ 第149轮（2026-11-17）：R_o 步 r_be 按钮、乘法两空可交换、提示精简、符号键同款

- **需求 1**：`R_o 表达式` 单空步也加 `padExtra`，引擎去掉 `hasNum` 限制后在按钮区（与 A 型同坐标 `(colX, nkY0)`）显示 `r_be` 装饰按钮，本页无数字键盘与「确认」键仍可见；`R_id = 2·r_be` 两空改同构 `alts` 多解 + `grp:'rid-mul'` + alts 项 `key`，`2` 与 `r_be` 前后任意、重复答案被拒。`R_o = □` 单空无交换对象，保持原样。
- **需求 2 / 3**：`renderMix` 顶部提示删除 `✓/▶/·` 步骤数串，只留「第 x / y 步 · 名称」；`K_CMR` 的 `A_vd`/`A_vc`/`∞` 三个 `.sym-key` 补与 `.num-key` 同款 CSS，不再是黑色实心块，hover 黄色描边与数字键一致。
- **用户裁决**：「交换顺序」＝乘法两空的 `2` 与 `r_be` 前后顺序任意；`r_be` 补到 4 页 `R_o` 步（含本页无确认键场景）。
- **生成链**：`patch_r149_config.py` 改 `tmp_dfb4/frag_CONFIG.js`；`patch_r149.py`（8 项 add）、`patch_r149b.py`（修 `pickBtn` 的 `data-ans` 在 alts 空下取空串的根因）改 `build.py`。本页 **43 处**补丁；备份 `archive/bak-r149/`；模板等价基线与 `df-b1.html` 字节一致（424,331 B）。
- **验收**：`probe_r149.js` 本页全过（4 页共 **74/74**）；`probe_r148.js` **114/114**；`flow_r148.js df-b4` **16/16 FLOW_OK 满分 100**；`narration_r148.js df-b4` **166/166**；`probe_r148_draw.js` **26/26**；`verify_r147.js` **68/68**、`verify_r145.js` **76/76**；`deliver_check_dfb4.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；截图 `shots-r149/after_b2_L2_*` 目检通过（B 型两页引擎与配置一致）。
- **版本**：lab `df-b4.html?v=5→6`；`thumb-df-b4.png?v=4→5`；index `data.js?v=12.79`。
- 详见 `制作规范.md` 第149轮规约。

## ★ 第150轮（2026-11-17）：R_o 步移除 r_be 按钮、拆分态地端交点去节点

- **需求 ①**：本页 `R_o = □` 单空步没有数字键盘、也没有「确认」键，按用户裁决移除 `r_be` 装饰按钮，按钮区保持全空；`padHint`「点电路标注作答」与虚线框不变。`I_EQ1` 步（有数字键盘）的 `r_be` 保留。
- **需求 ②**：共模等效电路「拆成两个 `2r_O`」后，两个独立地端最上横线（`y=490`）与垂直竖线（`x=366/706`）交点的白色圆节点 `(366,490)` / `(706,490)` 已删除；横线、竖线、三条接地横线与 `2r_O` 电阻均不变。置零态 `+VCC` / `-VEE` 地端节点按 r148 保留。
- **生成链**：`patch_r150.py` 改 5 份 `build.py`（撤销 `padExtra` 去 `hasNum`）+ 本页 `frag_CONFIG.js`（移除 `R_o` 步 `padExtra`）；`patch_r150b.py` 改本页 `frag_B2.html`（删 `#fx-cm-split` 两个 `<circle>`）。本页 **42 处**补丁；备份 `archive/bak-r150/`。
- **验收**：`probe_r150.js` **38/38**（本页按钮区全空、无残留键、无 JS 错误）；`probe_r149.js` **74/74**（B 型断言已改「不显示 r_be」）；`probe_r148.js` **114/114**（`splitGnd===0`）；`probe_r148_draw.js` **26/26**；`flow_r148.js df-b4` **16/16 满分 100**；`narration_r148.js df-b4` **166/166**；`deliver_check_dfb4.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**。截图 `shots-r148/df-b4_r148_split.png`（地端无节点）与本页同款 `after_b2_L2_ro_fill.png` 目检通过（B 型两页引擎与片段一致）。
- **版本**：lab `df-b4.html?v=6→7`；thumb 首屏未变保持 `?v=5`；index `data.js?v=12.80`。
- 详见 `制作规范.md` 第150轮规约。

## ★ 第151轮（2026-11-17）：2r_O 电阻本体也可点

- **问题**：第 4 关填写 `A_vc` 表达式的 `2r_O` 时，点电阻无反应，只有点 `2r_O` 文字有效。
- **根因**：电阻本体 `<rect x=352.5 / 692.5 y=380 w=27 h=53>` 在 `g.interactive[data-id="cm-2ro-1/2"]` **之外**；`elementFromPoint` 打电阻取不到 `data-id`，`answerBlank` 无法判分。
- **修法**：`patch_r151.py` 给本页 `frag_B2.html` 两个 `g.interactive` 各补一个纯热区（左 `340,374,46,66`、右 `686,374,46,66`），完整盖住电阻并与文字热区重叠 4~5px 无缝衔接。引擎/配置/分值/话术均未动。
- **验收**：`probe_r151.js` **34/34**（本页 4 个目标：左右电阻 + 左右文字，均真实鼠标点选并判分正确）；`probe_r150.js` **38/38**、`probe_r149.js` **74/74**、`probe_r148.js` **114/114**、`probe_r148_draw.js` **26/26**；`flow_r148.js df-b4` **16/16 满分 100**；`narration_r148.js df-b4` **166/166**；`deliver_check_dfb4.js` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**。截图 `shots-r151/click_df-b4_resistor.png`、`hover_df-b4_resistor.png` 目检通过。
- **版本**：lab `df-b4.html?v=7→8`；thumb 首屏未变保持 `?v=5`；index `data.js?v=12.81`。
- 详见 `制作规范.md` 第151轮规约。

## ★ 第152轮（2026-11-17）：拆分态 2r_O 地端与端口地端水平同轴

- **用户原话**：「两个单端输出案例中，将rO拆成2个2rO时，将正文的地端与Vi和Vo的地端水平同轴。」
- **问题**：本页 `#fx-cm-split` 两个独立地端横线 `y=490/498/506`，比 `comp-gnd1`（`v_i` 端口负端）的 `508/516/524` 高 18px；同屏底部三个地端不齐平。
- **修法**：`patch_r152.py` 改本页 `frag_B2.html`：两条竖线 `433→490` 延长为 `433→508`；六个地端横线 `490/498/506 → 508/516/524`（stroke 3.5/3/2.5 逐条一致）。电阻本体、r151 电阻热区、文字热区、r150「交点无节点」、配置与话术均未动。`comp-gnd2`（T2 基极直接接地 `248/256/264`）与 `comp-gndo`（`R_L` 下端 `257/265/273`）属电路局部参考点，本轮不动。
- **验收**：`probe_r152.js` **16/16**（本页横线 508/516/524、屏幕同轴 Δ=0.00px、竖线到 508、电阻与热区未移位）；`probe_r151` 34/34、`probe_r150` 38/38、`probe_r149` 74/74、`probe_r148` 114/114、`probe_r148_draw` 26/26、`verify_r147` 68/68、`verify_r145` 76/76；`flow_r148.js df-b4` **16/16 满分 100**；`narration_r148.js df-b4` **166/166**；`deliver_check_dfb4` **DELIVER_OK**；`svg-layout-check.py` **EXIT=0**；等价基线与 `df-b1.html` 字节一致（424,242 B）。
- **截图**：`shots-r152/df-b4_split_r152.png`、`df-b4_split_bottom_r152.png` —— 底部地端齐平、竖线自然、无重叠压线。
- **版本**：lab `df-b4.html?v=8→9`；thumb 保持 `?v=5`（首屏未变）；index `data.js?v=12.82`。
- 详见 `制作规范.md` 第152轮规约。

## ★ 第153轮（2026-11-18）：-VEE 置零地端去节点 + Vi / r_O 下标缩小 1/3

- **用户原话**：「1、两个单端输出案例，绘制共模等效电路时，-VEE置零后，移除地端上与rO连接线上的节点。2、4个差分案例Vi1和Vi2的下标太大了，减小1/3，rO的下标O减小1/3。」
- **节点**：本页 `#fx-cm-gnd-vee` 删除 `(536,517,r=7)` 白色节点，原位只留 r153 注释；`fx-cm-gnd-vcc` 节点、`node-vcc`、r150 拆分态无节点、r152 地端 `508/516/524`、`comp-gnd2` 局部参考点全部未动。真实置零动作会淡出 `comp-vee` 端子圆，交点完全干净。
- **下标**：新增 `.subsm`（50%），本页 `v_i` 与 5 处 `r_O` 的 `O`（已知行、`#fx-ro-hover`、`fx-cm-ro-tail`、两处 `2r_O`）由 75%→50%；`v_o` / `v_o1` / `v_o2` 与面板 `tkl()` 下标保持 75%。
- **验收**：`probe_r153.js` **68/68**；`probe_r148` 118/118、`probe_r148_draw` 26/26、`probe_r149` 74/74、`probe_r150` 38/38、`probe_r151` 34/34、`probe_r152` 16/16、`verify_r147` 68/68、`verify_r145` 76/76；`flow_r148.js df-b4` **满分 100**、`narration_r148.js df-b4` 166/166、`deliver_check_dfb4` **DELIVER_OK**、`svg-layout-check.py` **EXIT=0**；等价基线 424,402 B。
- **截图**：`shots-r153/df-b4_vi_r153.png`、`df-b4_ro_r153.png`、`df-b4_vee_real_r153.png`、`df-b4_split_r153.png`。
- **版本**：lab `df-b4.html?v=9→10`；thumb `?v=5→6`（首屏改动已重截）；index `data.js?v=12.83`。
- 详见 `制作规范.md` 第153轮规约。

## ★ 第155轮（2026-11-22）：R_o 表达式上移 50px（仅单端输出两案例生效）
- 用户先要求 4 页上移 50px，随后裁决「只改单端输出的案例吧」→ 最终只有 B 型 `df-b2` / `df-b4` 生效，A 型两页由 `patch_r155b.py` 完全回退。
- 本页（B 型单入单出）第 2 关 `R_o 表达式`（`?lvl=2&ms=8`，单空）虚线框中心由 **625.2 → 575.2**（Δ=50.00px）；r150「按钮区完全为空」保持。
- 实现：**仅 `tmp_dfb2` / `tmp_dfb4` 两套** `build.py` 追加 `r155-expr-dy` 补丁、`frag_CONFIG.js` 仅本步加 `exprDy: -50`；B 型补丁 42→43，A 型三套回退后等价基线仍 **424,402 B**；`_game-template.html` 本体不动，对照 `ms=6` 的 `R_id 表达式` 仍 625.2。
- 验收：`probe_r155.js` **65/65**、布局 EXIT=0、收窄后全链复验全绿；截图 `shots-r155/df-b4_ro_r155.png`，目检表达式居中、无压线。
- 版本：lab `df-b4.html?v=10→11`、thumb `?v=6` 保持（首屏未变）；index `data.js?v=12.85`。详见 `制作规范.md` 第155轮规约。

