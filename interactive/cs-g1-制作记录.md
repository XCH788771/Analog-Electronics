# cs-g1 制作记录（双电源分压偏置共源 · 案例1）

> ⚠️ **2026-10-26 内容归位修正**：此前 cs-g1.html 与 cs-g3.html 内容错位（本页所述「双电源分压偏置共源·案例1」被写进了 cs-g3.html，而「单电源完整版·案例3」被写进了 cs-g1.html）。经用户裁决，两页内容已互换归位——**本记录对应当前 cs-g1.html（双电源分压偏置共源 · 案例1）**。原「单电源完整版」内容已迁至 `cs-g3.html` 与 `cs-g3-制作记录.md`。互换脚本 `tools/swap_csg1g3.py`（从备份源幂等重建），原文件备份于 `.workbuddy/archive/bak-csg1g3-swap-20261026/`。


> 页面：`网站/interactive/cs-g3.html`｜构建链：`.workbuddy/tmp_csg3/build_cs_g3.py`（模板 `_game-template.html` + 区A/B/C/D + ANNOS + 19 处引擎补丁 P1–P19）｜定稿：2026-10-24 深夜

## 题面与设计
- **电路**：双电源（+V_DD / −V_SS）分压偏置共源放大，R_si＋v_s 信号源、C_b1/C_b2 耦合、R_s **无旁路电容**、R_g1/R_g2 分压、R_d、R_L 未接（空载 V_o 端口）。已知 g_m 与各电阻、电源电压，求动态性能指标。
- **因只给 g_m（无器件方程），Q 点不可解 → 三关制动态专属结构**：
  - 第1关 绘制直流通路 20 分（gate 三电源先行：src 置零短路 / vdd·vss 保留；cb1·cb2 断路；5 目标×4 分）
  - 第2关 绘制交流微变等效 20 分（6 目标×3 分＝18：src 保留 / vdd·vss 置零接地 / cb1·cb2 短路 / comp-t 等效；subSteps 交流通路→整理电路(moveIds: comp-rg1/comp-rd 不计分)→等效场效应管 TQUIZ 四问）
  - 第3关 动态指标 mix 60 分（Av/Ri/Ro 3 框架×6＋7 空×6＝60；A_v=−g_m·R_d/(1+g_m·R_s)、R_i=R_g1∥R_g2、R_o≈R_d；Ri 两空 grp `ri-par` 交换律）

## 计分口径（P18/P19，本轮治本）
- 模板 TQUIZ 池硬编码 `pool:2`，隐含约束 **pts = per×(n−1)＋2**（cj-g3 L4：8×2+2=18 自洽）。
- 本页 L2 为 6 目标 pts=20：per=round(20/6)=3 → 5×3+2=**17 差 3 分**（回归实测 per=17）。
- **修复**：池改为 `Math.round(cur().cfg.pts / cur().cfg.targets.length) + 2`（=3+2=5），合计 5×3+5=**20 ✓**；调试钩子 `?ts=` 同口径（P19）。等效项分值全部由问答池结算的语义保持不变。
- 回归：`interactive/regress_cs_g3.js` 正确路径 **100/100 finished、重新挑战归零、0 pageerror**（连跑 3 次稳定）。

## 踩坑记录
1. **模板 splice start_mark**（区 C）：写「/* ▼▼▼ 替换区 C」会匹配到模板三行块注释**第一行中间**，zoneC 被插进未闭合注释 → GAME_CONFIG 运行时未定义（node --check 查不出）。正确 start_mark 须含闭合行「④关 gate 门控 + targets 二级菜单（串/并、置零） */」（无「方式」二字）。
2. **svg-layout-check ④ 端点悬空豁免**：导线项 data-name 含「晶体管/电容/接地」才豁免——MOS 栅极条/三段沟道开路端属符号固有画法，comp-t 的 data-name 必须含「晶体管」（「场效应管」不算）。
3. **q-gm 热区**：初版 (450,105) 热区压 R_d 黄标签 → 移 (440,368)（s 标注与 R_s 之间空白区，hot rect 404,340,72×56）。仅 mix 关显示（updateQlabels dyn），与 L2 等效态 v_gs 列（x=445）无冲突。
4. **面板文案**：模板写死「晶体管等效」→ P17 改「场效应管等效」。
5. **回归菜单路径**：L2 双电源为「置零→接地」两级菜单；L1 src 为「置零→短路」。写一级标签会重试失败。
6. **软警告在案**：comp-rs 两端导线 96:40=2.40>1.5（上端需跨接 T 源极到 R_s，cj-g3 同款先例，不判失败）。

## 注册与联动
- `data.js` cs_b1.game 第 3 项：`案例3 · 电路闯关挑战（100分）`，`cs-g3.html?v=1`，thumb `thumb-cs-g3.png?v=2`；index `data.js?v=11.38`。
- 交付检查：`.workbuddy/deliver_check_csg3.js` 双通道（8765 预览服务 + file://）PASS，0 pageerror。
- 编号说明：cs-g1（分压式偏置·案例1）/ cs-g2（恒流源偏置·案例2）由并行会话占用，本页顺延案例3（用户 2026-10-24 会话顺序裁决）。

## G 极直角化修改（2026-10-26，用户指令参照 cs-g5 恒流源案例1）
- **问题**：栅极水平导线（V_i→C_b1→栅极节点→MOS）原接栅极竖条**中点**（wire-gate `M 320 265 H 400` 接条 235-295 中点）成 T 形，与 cs-g5 修改前同款。
- **修改**（zoneB.html 17 处原子补丁，build_cs_g3.py 重建）：栅极节点整列下移到栅极条**下端端点** y=295——wire-rg1b（185→295）、wire-gate（320→400 @295，直角）、节点圆 (320,295)、wire-rg2a（295→350）、wire-base-in（220→320 @295）；输入行随下 30 对齐：wire-vi-top、wire-rs-top、comp-vi 上端子圆 (150,295)、C_b1 双板 273-317、C_b1 标注 y=257；fx 层 fx-cb1/fx-vi 桥随行；整理层 comp-rg1 顶引线/顶节点圆随行（220,295）；**g 标注移至栅极条下方 (390,337)**（cs-g5 同款位置口径）；V_i 三标注 330/400/475 → 350/413/476（cs-g5 同款间距，修「＋」压端子圆 −2.6 硬错误）。
- **软警告在案**（栅极节点下移固有，不判失败）：comp-rg2 两端 55:85=1.55、comp-rsi 17:48=2.82（cs-g5 同性质 56:95 先例）。
- **验证**：布局自检 EXIT=0；默认/整理/等效三态截图目检（直角清晰、g 标注不压线、整理层 R_g1 顶节点连贯）；**真实鼠标命中**：C_b1 极板（273-317）→短路/断路菜单 ✓、comp-t 栅极区→等效菜单 ✓（★Playwright 单步 mouse.move 不触发 mouseenter，须域外两段式进场）；满分回归 100/100；deliver_check_csg3.js 双通道 PASS；thumb-cs-g3.png 已刷新，index data.js?v=11.44。

## 场效应管符号几何微调（2026-10-27，用户三项要求）

补丁脚本 `tools/patch_cs1_mos.py`（8 处 rep 唯一性校验，已同步写备份源 `bak-csg1g3-swap-20261026/cs-g3.html`）：

1. **D、S 与 B 间距减小 1/3**：44 → 29（D 引线 y 221→236、S 引线 y 309→294、B 保持 265）；三段沟道相应变短（段长 32→18、间隙 12→11）：D 段 227-245、B 段 256-274、S 段 285-303。连带：wire-d-stub 178→236、wire-src-a 294→385、衬底圆点 (458,294)。
2. **字母 B 右移对齐**：x 445→486（与 R_d 电阻体 x=468..504 中心 486 同一竖直线，即漏极节点/漏极竖线同轴）；y 248→278（37px 黑体视觉中心 ≈ 基线-13 → 265，与箭头水平中线同轴）。
3. **B 极箭头放大一倍**：polygon 418,265/432,259/432,271 → 418,265/446,253/446,277（长 14→28、高 12→24，尖端仍指沟道）；衬底引线起点随底边 M 446 265 H 458 V 294。

★踩坑：曾把栅极条同步缩到 246-284，导致 `wire-gate` 端点 (400,295) 悬空（布局自检 exit 1）——栅极条 235-295 本就短于沟道（60 vs 76）且中心正好 265，**无需缩短**，已回退。

特写验证：`tools/shot_cs1_mos.js`（动态读 circuit-wrap translate + comp-t bbox 设 viewBox 放大）。验收：布局自检 exit 0；autoclear 三路径 100/97/归零 0 pageerror；缩略图重截（thumb ?v=11、lab ?v=6、index data.js?v=11.48）。

## 电路整体重绘（2026-10-27 晚，用户原图：单电源分压式偏置共源·案例1）

用户裁决：此前的双电源电路（含 −V_SS / R_s / R_si / V_s / C_b2）画错了，**非本案例电路**。按用户截图重绘。

**正确电路**：+V_DD(5V) 顶轨 → R_g1 60kΩ / R_d 3.9kΩ；漏极节点直接引出 v_o（无输出耦合电容）；漏极支路红色 i_D 箭头；R_g1/R_g2 40kΩ 分压；C_b1 耦合 v_i 输入；MOS 管 T 衬底 B 接源极；**源极直落公共地线（无 R_s）**；接地符号在底轨中部。删除：−V_SS、R_s、R_si、V_s、C_b2。

**构建**：`tools/_rebuild_cs1_v2.py`（幂等：从 `bak-csg1g3-swap-20261026/cs-g3.html` 恢复旧版再重建；提取复用 comp-t 符号 / 偏置段 / comp-vi / comp-cb1 / fx 各层 / eq-rg1 / eq-rg2，重写主干 + ANNOS + GAME_CONFIG + STAGE_UNITS + 引擎补丁 14 处）。★已同步 cs-g4.html（导航案例1 副本，仅注释页名差异）。

**闯关（三关 18+22+60=100）**：
- L1 直流通路 draw=18：v_i 置零短路 / V_DD 保留 / C_b1 断路（3 目标 ×6）；act 新增 vi-short/vi-open/vi-keep
- L2 交流微变等效 draw=22：v_i 保留 / V_DD 置零接地 / C_b1 短路（3×6=18）+ 等效四问池 **tquizPool:4**（新配置项，startTQuiz 优先读 cfg.tquizPool）
- L3 动态指标 mix=60：框架 6×3 + 填空 8/8/8/8/10；A_v=−g_m·R_d（干扰：丢负号 / 误带 1+g_m·R_s 分母）、R_i=R_g1∥R_g2（grp ri-par）、R_o≈R_d

**引擎要点**：showEquiv 隐藏清单新增 wire-d-stub（漏极竖线含 i_D 装饰，等效态须随 comp-t 隐藏）与 wire-vo；moveCompDown 两者齐下后收 `['wire-vdd-ext','comp-vdd']`；CAP_FX 单电容；nextHint CAPS=['comp-cb1']；eq-layer 源极线 `M 486 525 V 420 H 530`（受控源下端→源极落点→地轨，无 eq-rs）。

**踩坑**：
1. between() 提取**不含结束锚**——SEG_DOTS 需手动补 `</g></g>`，否则 fx-layer 提前失闭合、rearr/eq 层暴露给布局检查（comp-rg1 自身重叠假报）；
2. 模板占位符 `__SEG_X__` 若出现两次（注释行+正文），str.replace 全量替换会重复注入；
3. ANNOS 块结尾多写一个 `}` → 页面 `Unexpected token '}'` 全挂；
4. 电阻值标注（60kΩ/40kΩ/3.9kΩ）与 37px 标签 bbox 间距须 ≥4px（60kΩ 放电阻体右侧 346,130；3.9kΩ 放 R_d 右侧 514,146 避开 60kΩ）；
5. 案例行 36px 中文上限 ≈24 字，超出被右面板（全局 x=980）裁切。

**验收**：布局自检 exit 0（28 交互单元 / STAGE_UNITS 48 / ANNOS 28）；真实鼠标三路径 100 [18,22,60] / 97 [18,22,57] / 归零，0 pageerror；7 态截图目检通过；cs-g4 布局同过；deliver_check 四通道（cs-g1+cs-g4 × localhost+file://）PASS。thumb-cs-g4 ?v=4（画面文字已核对新版）、index data.js?v=11.54。★swap_csg1g3.py 已标记废弃（cs-g1 与 cs-g3 不再互为副本）。

## 电阻符号缩小（2026-10-27 深夜，用户要求：高×2/3、宽×3/4）

补丁脚本 `tools/patch_cs1_res.py`（22 处 rep 唯一性校验，幂等安全中止）：

| 电阻 | 原尺寸 | 新尺寸 | 中心锚 |
|---|---|---|---|
| R_g1 / R_g2（默认态） | 36×90 | 27×60 | y 中心 140 / 395 不变 |
| R_d（默认态） | 36×80 | 27×53 | y 中心 100→100.5（R_d 标签 y 108→113 随中心下移） |
| 整理层 rarr-rg1 / rarr-rd | 36×90 | 27×60 | 中心不变，仅引线端点贴合新边 |
| 等效层 eq-rg1 / eq-rg2 | 36×90 | 27×60 | 同上 |

三层（默认/整理/等效）统一缩小，避免关卡推进时电阻尺寸跳变。x 方向以导线为中心对称缩（320→306.5..333.5、486→472.5..499.5、220→206.5..233.5、640→626.5..653.5）。

★维护：`tools/_rebuild_cs1_v2.py` 末尾追加 ⑮ 步——重建后自动调用 patch_cs1_res.py（其内嵌模板仍是旧尺寸，不补丁会回退）。

验收：布局自检 exit 0（端点全连接、无互压）；三态截图目检（默认/整理/等效）电阻明显变短变细、引线无缝、标注无重叠；autoclear 三路径 100 [18,22,60] / 97 / 归零，0 pageerror。

### 第103轮（2026-10-27 深夜）全站电阻统一 27×53

- 需求（用户）：所有案例中的电阻统一为 27×53。
- 本页改动 **4 个电阻**（含 comp-t-model 内的 r_be）：竖放一律 `27×53`、横放一律 `53×27`， **几何中心不变**；同步所有端点恰为旧体缘且轴向贯穿中心的 path/line（含 `fx-*` 短接线）；标签坐标不动。
- 工具：`.workbuddy/patch_resistors.py`（字符级绝对定位 + 冲突检测 + 保持行尾 + 干跑）； 分析器 `.workbuddy/analyze_resistors.py` 输出改动前后几何与受影响引线清单。
- 验收：svg-layout-check EXIT=0；默认态截图目检通过（电阻规格一致、两端引线连通、标签不压线）。
- 版本：data.js lab `（未引用）`；index `data.js?v=11.59`（thumb-gen --all 自动击破）； 缩略图已重截（电阻属首屏可见内容，按第83轮规约必须联动）。
- 归档：`.workbuddy/archive/bak-res-20261027/`（18 页 html + data.js + index.html + 16 张旧缩略图）。

## 三项修订（2026-10-29，用户要求）

补丁：`tools/patch_cs1_rdvo.py`（14 处）+ `tools/patch_cs1_qpoint.py`（20 组）。

**① R_d 上移 15px、v_o 水平导线上移 10px**：R_d rect 74-127 → 59-112（引线/标签/3.9kΩ 随动）；漏极节点 y 178→168（wire-vo / node-drain / comp-vo / wire-d-stub 及 i_D 杆·箭头·标注整体 −10）。等效态层（y=178 栅漏对齐布局）未动——两态间 v_o 端子有 10px 跳变，属整理/等效大改版内的正常过渡。

**② Vᵢ 置零短接桥两端接驳修正**：根因是输入导线起点 x=158（端子圆右缘）而绿色短接桥与底侧地线都接端子圆心 x=150——上端 T 形不闭合。改 wire-vi-top `M 158 295 H 206` → `M 150 295 H 206`，与 wire-gnd-l1（150,525）对称。

**③ 新增第 2 关「静态工作点估算」（纯表达式版，用户选定）**：
- V_GSQ = V_DD·R_g2/(R_g1+R_g2)；I_DQ = I_DO(V_GSQ/V_GS(th) − 1)²；V_DSQ = V_DD − I_DQ·R_d。干扰项：分母漏电阻 / 漏乘 V_DD；漏 −1 / 减序颠倒；极性 + / 丢电源项。
- 新增 3 枚红色电量标注 **q-ido (560,270) / q-vth (548,342) / q-idq (560,414)**（qlabel-layer 内，26px 间距 72；引擎 `cfg.qlabels` 过滤：本关只显这 3 枚，q-gm 仍只在动态关显示）；fw 子步带 qid（rg2/t/rd）驱动红色闪烁定位。
- 已知行补符号「V_GS(th)、I_DO」（无数值）；ANNOS +3。
- **计分改两阶段四关：12 + 24 + 22 + 42 = 100**（L1 18→12 即 3×4；L4 60→42 即框架 3×4 + 填空 6×5；L2 mix=框架 3×3 + 填空 15）。关号顺延：交流等效→第3关、动态指标→第4关（title/announce 同步）；调试钩子 ts/tidy 目标关 2→3、S.draw[1]→S.draw[2]。
- 引擎点：completeLevel 直流通路视图保留给同阶段后续关（Q点关沿用 DC 态）；arrangeMixSubs 无 qorder 时保序；框架选项 Fisher-Yates 洗牌（correct 标记判定，与位置无关）。

**验收**：布局自检 exit 0；四关结构校验（12+24[9+15]+22+42=100）0 pageerror；autoclear 三路径 **100 [12,24,22,42] / 98 [12,22,22,42]（L2 框架错一次 −2）/ 归零**；9 态截图目检（框架分式+虚线框、I_DQ 分式字面 V_GSQ+平方²、红色标注无压线、已知行含新参数完整显示、结算 4 行分项）；deliver_check 双通道 PASS。★cs-g4 已由并行会话改为双电源版并接管导航案例1 入口，本页修订未同步 cs-g4。

### 第 2 关前置微调（2026-10-29 下午，用户要求）：C_b1 断路连锁移除补全

- 需求：点击 C_b1 断路后，① 移除 C_b1 右端到分压节点的导线（wire-base-in）；② 移除 R_g2 下方节点圆。
- 实现：
  - `fadeWith['comp-cb1']` 由 `['wire-vi-top','comp-vi','wire-gnd-l1']` 扩为 **+ `'wire-base-in'`, `'node-rg2'`**（随输入回路一并半隐 0.15，与输入段同一移除视觉语言）。
  - **节点圆拆组**：原 (320,525) 白点嵌在 wire-gnd-m 组内无法单独移除 → 拆为独立组 `<g id="node-rg2" data-id="node-rg2">`（默认渲染不变）；ANNOS +1；STAGE_UNITS 第2组（全件组）+`node-rg2`（第1组=直流通路组不加——该节点在 DC 态会被移除）。
  - 第 1 关 `why` 文案同步：「C_b1 右板至分压节点的导线与 R_g2 下端节点一并移除」。
- 保留判定：分压节点 (320,295) 三线交汇（rg1b↓/gate→/rg2a↓）节点圆保留；R_g2 下端在 DC 态退化为两线拐角故移除；AC 通路态 C_b1 短接、输入地线段回归，节点圆正确保留（整理/等效步不涉及）。
- 验收：svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；真实浏览器截图目检（C_b1 断路后右板导线与 R_g2 下端节点圆均已半隐、拐角干净、DC 态通路完整）；deliver_check 双通道 PASS。无 data.js/index 版本联动（cs-g1 导航外副本）。

### 地端右移 + 接地端节点（2026-10-29 晚，用户要求）

补丁：`tools/patch_cs1_gnd.py`（4 处）+ `tools/patch_cs1_gnd2.py`（3 处）。

**① 接地符号右移到 S 极垂直导线处**：comp-gnd 整体右移 83px（竖引线 403→486；三条横线 375-431→458-514 / 385-421→468-504 / 393-413→476-496）。
**② 新增接地端节点**：独立组 `node-gnd` (486,525) r7——公共地线主段、S 极垂直导线、接地引线三线交汇点；ANNOS +1；STAGE_UNITS 两组（直流组/全件组）均 +node-gnd（DC 态该节点保留：接地符号与 S 极落点常在）。

**③ 顺手修复整理/等效态既有缺陷**：下挂 R_d 落点 (640,525) 悬空——主地轨 wire-gnd-m 只到 486。新增 `fx-gnd-ext`（M 486 525 H 640，fx-layer 内默认隐藏）：moveCompDown('comp-rd') 时点亮，等效态随 rarr-rd 保留，resetCircuit 清零清单已补（★换案例注记同步：新增特效层必须入清单）。默认/DC 态地轨仍止于 486，无多余线。

验收：svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；四态截图目检（默认地线止于新节点、DC 态节点保留、整理/等效 R_d 底端接地、接地符号与源极竖线同轴）；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。

### 去参数（2026-10-29 深夜，用户要求）：题干与电路图只保留元件号

补丁：`tools/patch_cs1_noparam.py`（19 处，残留扫描 0）。

- **已知行**：「已知：g_m、R_g1、R_g2、R_d、V_DD、V_GS(th)、I_DO」——去掉 =60kΩ/=40kΩ/=3.9kΩ/=5V，只留元件号与符号。
- **电路图**：删 R_g1「60kΩ」/ R_g2「40kΩ」/ R_d「3.9kΩ」三处数值标注；电源端子删「(5V)」，V_DD 单行下移至 y=16 与端子圆心垂直对齐。电极号 g/d/s/B/T、C_b1/R_*/V_*/i_D/q-* 符号标注全部保留。
- **联动**：comp-rd data-name 去参数；ANNOS 四条（comp-vdd/rg1/rg2/rd）屏显+TTS 语音同步去数值（60千欧/40千欧/3.9千欧/5伏）；台账注释改注「参数已隐去，原值见制作记录」。
- 关卡影响：无——第2/4关为纯表达式版（填符号不代数值），不依赖页面数值。
- 验收：布局自检 exit 0；真实浏览器文本核查（SVG 可见文本无 60kΩ/40kΩ/3.9kΩ/5V）+ 默认态截图目检（无空缺错位压线）；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS。

### v_o 标注增大一倍（2026-10-29 深夜，用户要求）

补丁：`tools/patch_cs1_vo.py`（1 处）。comp-vo 标注 font-size 37→74px；基线 y 176→190、x 726→722（补偿放大后的视觉中心偏移，保持与输出端子圆垂直居中、左缘间隙不变）。下标比例 75% 随字号自动缩放。
验收：布局自检 exit 0（74px 标签无压线/越界）；默认/等效态截图目检（与端子对齐、间隙合理）；autoclear 100/98/归零 0 pageerror；deliver_check PASS。

### v_o 缩至 2/3 + 场效应管右移 28px（2026-10-29 深夜，用户要求）

补丁：`tools/patch_cs1_t28.py`（14 处）+ 栅极导线跟随修正（wire-gate H 400→428，栅极条右移后端点必须跟随，否则端点悬空硬错）。

**① v_o 74 → 49px**（74 的 2/3 取整），y 190→181、x 722→726（重新与端子圆垂直居中）。
**② 场效应管整体右移 28px**：栅极条 400→428、沟道三段 414→442、漏/源引线 M 414→442（右端仍接 486 不动）、B 引线折点 **458→486 与 S 极直角点 (486,294) 重合**（源极引线/B 竖段/wire-src-a 三线交汇，节点圆随移 458→486）、箭头 polygon +28、热区 rect x 386→414。
**③ 字符同步**：g 390→418（随本体）；B 486→514、T 516→544（原位被新竖线穿过，右移让位，与 L2 红色标注 I_DO（文字中心 608）间隙 10px 达标）；d/s 标在引线端不动；q-ido/q-vth/q-idq 不动。
验收：布局自检 exit 0（曾抓出 wire-gate 端点悬空硬错并修正）；默认态/L2 态截图目检（B 折点与 S 直角重合、字符无压线、I_DO 间隙充足、v_o 居中）；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS。

## 第107轮（2026-11-01）：移除 MOS 管符号旁全部单字母标注
- 删 g/d/s/B/T 共 5 条 hot-label 及「<!-- 电极标注 -->」注释；符号本体（栅极条/沟道/短截线/衬底箭头）不动。
- 本页当前未挂导航（案例1 入口由 cs-g4 接管），无 lab 链接与缩略图引用，不递增版本号。
- 验收：布局 EXIT=0；FET 特写目检无字母；cs-g1-autoclear 回归 98/100 双路径过。

### 工作点标注改版 + 语音注音（2026-11-01，用户四项要求）

补丁：`tools/patch_cs1_qmark.py`（21 处），备份 `/tmp/cs-g1.before-qmark.html`。

**① TTS 注音**：语音串（parts/announce，共 9 条 16 处）「栅」→「山」（shān 一声，国家标准读音；屏显文字 36 处「栅」全部保留，只改语音串）。

**② 电流箭头**：右移 25px（x 486→511，脱离 D 极导线成独立旁注箭头）；杆 186–206→172–214（20→42px）；头部 16×15→22×23（points 511,238 500,215 522,215）；**i_D 文字删除**；wire-d-stub data-name 与台账注释同步改为「红色箭头指示漏极电流方向」。

**③ I_DQ 上移**：q-idq 从 (608,448) 移至 (536,215)——与箭头（y 172–238，中心 205）水平同轴，文字左缘 536 = 箭头线 511 + 25px；热区 (530,183,100,42)。

**④ V_GSQ / V_DSQ 竖排柱**：
- **q-vth 显示改 V_GSQ**（data-id 不变，作答链路 ansIds=['q-vth'] 保持）：＋(545,374)/V_GSQ(545,410)/－(545,446) 竖排柱 @x=545，位于 G–S 之间偏下（图1 绿框位）；data-name/ANNOS 改「栅源静态电压 V_GSQ（＋/− 标出极性）」。
- **新增 q-vdsq**：＋(545,258)/V_DSQ(545,294)/－(545,330)，位于 D–S 之间（图2 绿框位）；ANNOS 新增（V_DSQ = V_DD − I_DQ·R_d，＋在 D、−在 S）；qlabels +q-vdsq。
- **I_DO 右移 32px**（text 608→640、rect 560→592）让出 V_DSQ 柱空间。
- 热区间隙：q-idq 底 225 / q-vdsq 230–338 / q-vth 346–454 / q-ido 592–688，互不重叠，最近邻 ≥4px（可见字符 ≥20px）。

**保留说明**：I_DQ 表达式填空第 2 空仍为 V_GS(th)（转移特性方程分母，已知行参数），点击目标 q-vth（现为 V_GSQ 标注）不变——如需改方程结构须用户裁决。已知行 V_GS(th)、I_DO 参数保留（求解目标 V_GSQ/V_DSQ/I_DQ 不入已知行）。

验收：svg-layout-check exit 0；默认态截图（独立箭头无文字无标注）+ L2 态截图（四组红色标注齐备、不压线不重叠）；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS；语音串「栅」0 残留、屏显 36 处保留。无 data.js/index 版本联动（导航外副本）。


### 工作点标注改版 + 语音注音（2026-11-01，用户四项要求）

补丁：`tools/patch_cs1_qmark.py`（21 处），备份 `/tmp/cs-g1.before-qmark.html`。

**① TTS 注音**：语音串（parts/announce，共 9 条 16 处）「栅」→「山」（shān 一声，国家标准读音；屏显文字 36 处「栅」全部保留，只改语音串）。

**② 电流箭头**：右移 25px（x 486→511，脱离 D 极导线成独立旁注箭头）；杆 186-206 → 172-214（20→42px）；头部 16×15→22×23；**i_D 文字删除**；wire-d-stub data-name 与台账注释同步改为「红色箭头指示漏极电流方向」。

**③ I_DQ 上移**：q-idq 从 (608,448) 移至 (536,215)，与箭头（y 172-238，中心 205）水平同轴，文字左缘 536 = 箭头线 511 + 25px；热区 (530,183,100,42)。

**④ V_GSQ / V_DSQ 竖排柱**：
- **q-vth 显示改 V_GSQ**（data-id 不变，作答链路 ansIds=['q-vth'] 保持）：＋(545,374)/V_GSQ(545,410)/－(545,446) 竖排柱，位于 G-S 之间偏下（图1 绿框位）；data-name/ANNOS 改「栅源静态电压 V_GSQ（＋/− 标出极性）」。
- **新增 q-vdsq**：＋(545,258)/V_DSQ(545,294)/－(545,330)，位于 D-S 之间（图2 绿框位）；ANNOS 新增（V_DSQ = V_DD − I_DQ·R_d，＋在 D、−在 S）；qlabels +q-vdsq。
- **I_DO 右移 32px**（text 608→640、rect 560→592）让出 V_DSQ 柱空间。
- 热区间隙：q-idq 底 225 / q-vdsq 230-338 / q-vth 346-454 / q-ido 592-688，互不重叠。

**保留说明**：I_DQ 表达式填空第 2 空仍为 V_GS(th)（转移特性方程分母，已知行参数），点击目标 q-vth（现为 V_GSQ 标注）不变，如需改方程结构须用户裁决。已知行 V_GS(th)、I_DO 参数保留。

验收：svg-layout-check exit 0；默认态+L2 态截图目检；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS；语音串「栅」0 残留、屏显 36 处保留。无 data.js/index 版本联动（导航外副本）。


### 工作点标注第二轮（2026-11-01，用户三项要求）

补丁：`tools/patch_cs1_qmark2.py`（10 处），备份 `/tmp/cs-g1.before-qmark2.html`。

**① 箭头仅第 2 关显示**：电流箭头（line+polygon）从 wire-d-stub 移入 q-idq 组（qlabel-layer 内）——L1/L3 整层 opacity 0、L4 动态 mix 走 dyn 分支隐藏（非 q-gm 全隐）、默认态不显示；第 2 关随 I_DQ 标注一起显示。wire-d-stub data-name 去箭头描述。

**② 移除 I_DO**：q-ido 组 + ANNOS 条目删除，qlabels 去 q-ido；I_DQ 表达式中 I_DO 由填空改为**固定符号 token**（已知参数不作答，与已知行 I_DO 呼应），其 2 分并入 V_GS(th) 空（2→4 分），L2 总分 24 配平不变。

**③ V_GSQ 移到绿框位**（对应截图：＋ 在管子左、文字在沟道右下、－ 在文字下）：
- ＋(408,272)：栅条左侧、栅极高度（沟道与栅节点之间区域）；
- V_GSQ(526,330)：源极竖线右侧、沟道右下（绿框位）；－(526,366) 其下；
- 热区拆两块：(395,244,26,32)（＋）+ (492,296,72,76)（文字+－，避开源极竖线 486）。
- **V_DSQ 柱右移 75px**（x 545→620，rect 583,230,90,108）：I_DO 删除后空间空闲，为 V_GSQ 文字让位（原位与 V_GSQ 新位重叠）。

验收：svg-layout-check exit 0；三态截图目检——默认态无箭头无标注（干净）、第 2 关箭头+I_DQ+V_GSQ（＋栅左/V_GSQ 沟道右下/－其下）+V_DSQ 柱齐备不压线、第 4 关与默认裁剪逐字节相同（Q 点标注全隐）；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check PASS。无 data.js/index 版本联动（导航外副本）。


### 第2关标注微调（2026-11-01，用户两项指令）

补丁：`tools/patch_cs1_qmv.py`（6 处），备份 `/tmp/cs-g1.before-qmv.html`。

- **① Vi 的 － 下移 25px**：(150,476)→(150,501)，靠近下端子圆（525）但不压（字形底 ~503 vs 圆顶 517）。
- **② V_GSQ 下移 25px、左移 120px**：(526,330)→(406,355)，落位于 R_g2 上引线右侧、栅极导线（y=295）下方空白区。
- **③ G 极红色 ＋ 下移 45px、左移 295px**：(408,272)→(113,317)，落位输入端子上端子圆（150,295）左上方（与黄色 Vi ＋(150,350) 无重叠：x 102-124 vs 137-163）。
- **④ G-S 组红色 － 左移 60px**：(526,366)→(466,366)，位于沟道右侧与源极竖线（486）之间（字右缘 476，净距 10px）。
- 热区随动：＋ 热区 (395,244,26,32)→(100,291,26,32)；V_GSQ＋－ 联合热区 (492,296,72,76)→(374,329,106,44)。
- 位置关系备注：V_GSQ 新位与第 3 关 g_m 标注（440,368）空间相近，但两者分属第 2/第 3 关（qlabels 互斥显示），永不同屏，无冲突。

验收：svg-layout-check exit 0；默认态截图（红色全隐、Vi － 新位不压端子圆）+ 第 2 关截图（＋/V_GSQ/− 新位齐备、无压线无重叠）目检通过；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror（q-vth 新热区真实点击可达）；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。


### V_DD 端子标注 + C_b1 改称 C_1 + 红＋移黄框位（2026-11-01，用户三项指令）

补丁：`tools/patch_cs1_c1vdd.py`（3 处 rep + 4 组全局替换），备份 `/tmp/cs-g1.before-c1vdd.html`。

**① V_DD 端子标注**：改为「＋V_DD」（前加全角＋）；x 726→728（与端子圆右缘 708 间隔 20px）；基线 y 16→18 与端子圆 (700,5) 垂直同轴。class `.vdd-label` 不变（直流通路/交流态淡出逻辑不受影响）。

**② C_b1 → C_1 全局改称**（37 处）：SVG 元件标注 `C<tspan>b1</tspan>`→`C₁`（1 处）、ANNOS 屏显 `C<sub>b1</sub>`（7 处）、data-name/name/why/注释 `C_b1`（22 处）、TTS 语音串 `Cb1`→`C1`（7 处）。**内部 data-id `comp-cb1`、fx-cb1、fadeWith/resetCircuit 清单全部不动**（避免破坏断路移除链路与回归脚本）；残留扫描 C_b1/Cb1/sub">b1 = 0。

**③ 第 2 关 V_GSQ 的红色 ＋ 移到截图黄框位**：(113,317)→(360,322)——分压节点 (320,295) 右下方、栅极导线（y=295）下方、V_GSQ 文字 (406,355) 左上方；热区 (100,291,26,32)→(346,296,28,28)。

验收：svg-layout-check exit 0；默认态截图（＋V_DD 同轴带＋号、C₁ 标注居中）+ 第 2 关截图（红＋在黄框位、不压线、与 V_GSQ/− 关系正确）目检通过；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。


### 标注布局大改版（2026-11-01，用户五项指令）

补丁：`tools/patch_cs1_qlayout.py`（9 处），备份 `/tmp/cs-g1.before-qlayout.html`。

**① V_i 下移到 ＋、－ 中间**：(150,413)→(150,426)（＋350/－501 中点 425.5）。
**② V_GSQ 正确框架 V_DD 方框放后面**：正确项与 fullExpr 改为 `V_GSQ = R_g2/(R_g1+R_g2) · [V_DD]`（分式在前、V_DD 框在后）；干扰①同构改 `R_g2/R_g1 · [框]`、干扰②不变；填空顺序随动 [R_g2 2, R_g1 1, R_g2 1, V_DD 2]，总分配平不变。
**③ I_DQ 箭头移到 D 极导线左侧**：x 511→461（距竖线 486 仍 25px）；为避开漏极水平引线（y=236），箭头整体上收（杆 174-208、头 208-232，尺寸不变 22×24）；I_DQ 文字移到箭头左侧同距 25px（anchor end x=436，y=215 不变）；热区 (384,176,88,58)。
**④ V_DSQ 左移 60px 并与衬底 B 箭头水平同轴**：x 620→560；竖排柱中心 y 294→265（B 箭头轴）：＋(560,229)/V_DSQ(560,265)/－(560,301)——＋贴近漏极引线(236)、－贴近源极引线(294)，符合 D/S 极性；热区 (523,209,74,100)。
**⑤ 新增两条红色标注**（仅第2关显示）：
- **q-vt**：V_T（开启电压/阈值电压）@ (406,396)，V_GSQ (406,355) 正下方；ANNOS 新增（V_GS 超过 V_T 才形成导电沟道）；热区 (382,371,62,30)。
- **q-ido**：I_DO @ (505,200)——D 极导线 (486) 右侧、无箭头（用户明确要求）；ANNOS 新增（饱和漏极电流，转移特性已知参数）；热区 (500,176,66,30)。
- qlabels 第2关改为 ['q-vth','q-vt','q-idq','q-ido','q-vdsq'] 五条全显。

空间关系核验：I_DO(176-206) 与 V_DSQ 柱(209-309) 无重叠；V_T(371-401) 与 R_g2(x≤333.5) 不冲突；箭头左缘 458.5 距沟道(444.5) 14px；I_DQ 文字(386-436) 在沟道左侧、栅极条(235-295)上方。

验收：svg-layout-check exit 0；默认态（Vi 居中）+ 第2关（箭头/文字/I_DO/V_DSQ/V_T 全部到位、无压线无重叠）+ 框架面板（V_GSQ=分式·框，V_DD 框在最后）截图目检通过；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。


### I_DO / V_T 方框化 + V_GSQ 加号右移（2026-11-01 午，用户两项指令）

补丁：`tools/patch_cs1_box2.py`（9 处），备份 `/tmp/cs-g1.before-box2.html`。

**① V_GSQ 的 ＋ 右移 20px**：(360,322)→(380,322)（分压节点右下、栅极导线下方）；热区 (346,296,28,28)→(366,296,28,28)。与 V_GSQ 文字纵向净距 5px（≥4 过检）。

**② I_DO 与 V_T 改为方框（第 2 关表达式填空）**：
- I_DQ fill 的 fullExpr：固定符号 `I_DO` → `{box:1}`；blanks 改两条：`{ansIds:['q-ido'], label I_DO, pts:2}` + `{ansIds:['q-vt'], label V_T, pts:2}`（原单条 V_GS(th) 4 分拆回 2+2）。
- **分母空答案改点 q-vt（V_T）**——原来点 q-vth（V_GSQ 标注，语义不符的遗留，本轮用户指令落实为 V_T）。
- **已知行 V_GS(th) → V_T**（与方程、图中红标一致）；why 文案改 `I_DO(V_GSQ/V_T − 1)²`；分值注释同步（填空 2/2/1/1、2/2、1/1/3 = 15，L2 总 24 不变）。
- ANNOS q-vt/q-ido 加「第 2 关可点击填入方框」；q-vt data-name 同步。

验收：svg-layout-check exit 0；截图目检——第 2 关红＋新位不压线、I_DQ 表达式面板两方框（等号后与分母）、V_GSQ 完成态正常、已知行 V_T；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror（两新空真实作答可达）；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。


### I_DQ 方程的 V_GSQ 也方框化（2026-11-01 午，用户指令）

补丁：`tools/patch_cs1_vgsqbox.py`（4 处），备份 `/tmp/cs-g1.before-vgsqbox.html`。

- I_DQ fill 的 fullExpr 分子 `V_GSQ` 文字 → `{box:1}`，表达式变为 `I_DQ = [框]([框]/[框] − 1)²` 三方框。
- blanks 三条：I_DO（q-ido，2 分）→ V_GSQ（**q-vth**，1 分）→ V_T（q-vt，1 分）＝ 4 分配平，L2 总 24 不变；分值注释同步。
- ANNOS q-vth / data-name 补「第 2 关可点击填入 I_DQ 方程方框」。

验收：svg-layout-check exit 0；截图目检（三方框面板、填空完成态推进到 V_DSQ 框架、本关 16/24 符合 3+6+3+4）；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror（三空真实作答可达）；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。


### 第 2 关自动移除 v_o 及输出导线（2026-11-01 午 3，用户指令）

补丁：`tools/patch_cs1_voq.py`（3 处），备份 `/tmp/cs-g1.before-voq.html`。

- 新增 `applyQPointView()`：fadeGroup('comp-vo', true) + fadeGroup('wire-vo', true)（全隐 opacity 0 + hit-off，不干扰命中）。
- **completeLevel**：进入 mix 且 stageUnits === 0（第 2 关）时调用——直流通路视角下 v_o 属交流量，标注、端子圆与输出导线一并移除；漏极节点圆保留（仍在 R_d—T 漏极竖直连线上）。
- **调试钩子** ?lvl=2 同步调用（预览一致）。
- 恢复：进入第 3 关时 completeLevel 原有 `resetCircuit()` 统一清 opacity/hit-off，v_o 自动恢复；第 4 关 mix 不触发（stageUnits 1）。无 JS 硬编码坐标。

验收：真实流程验证——L2 时 comp-vo/wire-vo opacity=0、L3 恢复 visible（0 pageerror）；第 2/3 关输出区域截图目检（L2 端子区干净、L3 v_o 完整恢复）；svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。


### 第 2 关同步移除漏极节点（2026-11-01 午 4，用户指令）

补丁：applyQPointView() 加 `fadeGroup('node-drain', true)`（直接 Edit，1 处；备份沿用 `/tmp/cs-g1.before-voq.html` + 修改后快照）。

- 输出导线移除后漏极退化为两点直通（R_d 下端—T 漏极共线），节点圆随 v_o 一并移除——与第 1 关 R_g2 下端节点同逻辑。第 3 关 resetCircuit 自动恢复（V_DSQ 等效态仍需该节点）。
- 验收：真实流程断言 L2 node-drain opacity=0、L3 恢复 visible、0 pageerror；L2 截图目检（竖线连续无圆点）；布局 exit 0；autoclear 三路径 100/98/归零；deliver_check PASS。无 data.js/index 版本联动。


### I_DQ 框架 V_GSQ 方框化 + 全页同级运算不区分顺序（2026-11-01 午 5，用户指令＋「以后同运算级别不区分先后」的长期规约）

补丁：`tools/patch_cs1_orderfree.py`（5 处），备份 `/tmp/cs-g1.before-orderfree.html`。

**① I_DQ 计算框架**：三选项（正确＋两干扰）tokens 中分子 `V_GSQ` 全部改为方框（`fr([{box}],[{box}])`），面板呈「I_DQ=[框]([框]/[框]±1)²」。

**② 同级运算填空不区分顺序**（按制作规范 428 行标准写法：ansIds 双合法 id + 同 grp + labels 映射 + 同分值）：
- V_DSQ 乘积 `I_DQ·R_d` → grp `vdsq-prod`，两空均可点 q-idq/comp-rd，分值 1/3→**2/2** 配平（总 5 不变）；
- V_GSQ 分母 `R_g1+R_g2` → grp `vgsq-den`（分值已同 1/1）；
- A_v 乘积 `g_m·R_d` → grp `av-prod`（分值已同 6/6）；
- R_i 并联 ri-par 上轮已有。
- 已审计全页 fill：V_GSQ 的分子/分母属不同级别（分式结构由框架固定）、I_DO/V_T 各一级、V_DD 独立即减项非成对——均无同级成对空，无遗漏。

**验收**：真实浏览器专项测试——正向反序（V_GSQ 分母 R_g2 先/R_g1 后、V_DSQ 乘积 R_d 先/I_DQ 后、Av 反序）全部判对且第 2 关满分 24；负向（同 grp 重复填同一量 R_g1×2）正确判错扣分；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；I_DQ 框架面板截图目检（三选项全方框）；deliver_check 双通道 PASS。

### 第 3 关 R_d 下移直连 + 上端接 v_o 导线交点 + 删下端节点（2026-11-01 午 6，用户指令）

补丁：`tools/patch_cs1_rdmove.py`（4 处），备份 `/tmp/cs-g1.before-rdmove.html`；专项脚本 `tools/cs-g1-rdmove-check.js`。

- **① 菜单直连**：menuItemsFor 中 comp-rd 点「下移」不再弹「与输出串/并」二级选项，直接 `chooseMoveOption(id, true)` 下挂并联（源极接地、输出直接引出，本就无歧义）；comp-rg1 二级选项保留。
- **② 上端接 v_o 导线**：rarr-rd 上端引线 178→168（整理态 v_o 水平导线高度），节点圆（r=8）随迁至交点 (640,168)；上端 path/circle 加 id `rarr-rd-top`/`rarr-rd-node`。等效态（漏极横线 y=178 栅漏对齐布局）在 showEquiv() 中动态改回 `M 640 178 V 333.5`/cy=178，resetCircuit() 复位 168——消除原「整理/等效两态 v_o 端子 10px 跳变」遗留。
- **③ 删下端节点**：R_d 下端 (640,525) 落在地轨延伸段端点（L 形拐角），节点圆删除，两态均无。
- 验收：真实鼠标悬停菜单仅「下移」1 项、点击后菜单消失且 moved=true；整理态截图（上端节点在 v_o 线交点、下端无圆）；等效态 ts=1 截图（上端回 178 交点）；svg-layout-check exit 0（端点全连接）；autoclear 三路径 100 [12,24,22,42] / 98 / 归零 0 pageerror；deliver_check 双通道 PASS。无 data.js/index 版本联动（导航外副本）。

### 等效态：源极直落地 + g/s 垂直同轴 + 受控源下移 + g_m·v_gs 标注改位（2026-11-01 午 7，用户指令）

补丁：`tools/patch_cs1_equiv.py`（7 处）＋ 3 处 Edit（fx-t-id 拆组 / TQUIZ idlabel / 钩子同步），备份 `/tmp/cs-g1.before-equiv.html`；专项脚本 `tools/cs-g1-equiv-shot.js`（ts=1/3/4/6 四态几何断言+截图）。

- **① 删地端上方导线**：eq-layer 源极线 `M 486 525 V 420 H 530` 整条移除，源极不再经 486 竖线/横线上引。
- **② S 红点垂直同轴**：fx-dot-s (486,420) → (420,525)——落在地线上、与 g 红点 (420,178) 同 x，G—S 开路段一眼可见；第 3 问 epos=530 时 s 点移到受控源落点 (530,525)（setEPos 目标 id 由遗留的 #fx-dot-e 修正为 #fx-dot-s）。
- **③ v_gs 列重排**：x=445，＋ y=213 / v_gs y=352 / － y=495，覆盖 g—s 新跨度（178—525），与菱形（500—560）净隙 35px。
- **④ 受控源直落地**：支路 x=530，上引线 178→319、菱形中心 (530,351)（=178—525 中点）、下引线 383→525，落地点 T 形交汇补节点圆 r=7。
- **⑤ g_m·v_gs 标注**：fx-t-src 菱形旁文字删除（作答前不显示）；fx-t-id 拆为箭头组 fx-t-id 与标注组 fx-t-idlabel（文字 g_m·v_gs，原 i_d 位 548,222 不变）——第 4 问弹出方向选项时即显数值（TQUIZ[3].idlabel + showTQuizMenu/钩子同步），作答后才画箭头；resetCircuit 清单补 fx-t-idlabel。
- 题面与选项仍用 i_d（方向问法），图注为数值 g_m·v_gs（i_d=g_m v_gs 教学口径），用户如需同步改题面再调。
- 验收：四态几何断言（s 点 420↔530、各层 opacity 时序、fx-t-src 内 0 text）；截图目检 ts=4/6（g_m·v_gs 与 R_d 竖线净隙 14px、无压线）；布局 exit 0；autoclear 三路径 100/98/归零；deliver_check PASS。无版本联动（导航外副本）。

### 第 2 关 I_DQ 箭头与文字上移 20px（2026-11-01 午 8，用户指令）

直接 Edit（q-idq 组 4 处坐标：line 174-208→154-188、polygon 头 232→212/188、热区 rect y=176→156、I_DQ 文字 y=215→195），备份沿用 `/tmp/cs-g1.before-equiv.html`（本组此后无改动）。专项截图 `tools/cs-g1-idq-shot.js`。
- 箭头顶端 154 在漏极节点（168）上方 14px，x=461 距 D 导线 25px 不变，与 R_d 引线/漏极节点/I_DO 均无重叠；svg-layout-check exit 0、autoclear 三路径 100/98/归零、deliver_check PASS。

### 等效态第二轮：删绿桥 / 选项与图注改 g_m·v_gs / g_m 置于 v_gs 与菱形之间（2026-11-01 午 9，用户指令）

补丁 `tools/patch_cs1_equiv2.py`（7 处）＋ showEquiv/钩子 2 处 Edit，备份 `/tmp/cs-g1.before-equiv2.html`。
- **① 绿色短桥清除**：真正元凶是等效态下错位残留的 `fx-cb1`（C_1 短接桥，仍在默认位 (206,295)-(220,295)，R_g1 竖线左侧悬空）——eq-layer 内 178 处同款绿桥一并删除；showEquiv/调试钩子用 `showFx('fx-cb1', false)` 收起（fx 层按 id 查找，fadeGroup 按 data-id 查找查不到，首版误用已修正）；扫描断言等效态可见绿元素 = 0。
- **② 选项/题面/图注改 g_m·v_gs**：tquizOptHtml 渲染 ↑g_m·v_gs / ↓g_m·v_gs（TQ_SUBD 复用机制，判定仍按 label ok）；题面改「受控源支路电流为 g_m·v_gs，箭头方向是？」；图中箭头旁 g_m·v_gs 改为**作答后**与箭头同时显示（showTQuizMenu 不再提前显示，answerTQuiz 里随 reveal 同现；调试钩子 slice 逻辑天然一致）。
- **③ g_m 标注**：受控源菱形左侧新增 g_m（x=479, y=352，与 v_gs 同基线水平同轴），v_gs 列（＋/v_gs/－）左移 10px（445→435）腾位；随 fx-t-src 第 3 问显示。
- 验收：四态断言（ts=4 选项 ["↑gm·vgs","↓gm·vgs"] 且 opIdLabel=0、ts=6 opIdLabel=1、greenBridge=0、gmText=gm@479,352）；可见绿元素扫描 = []；布局 exit 0；autoclear 100/98/归零；deliver_check PASS。

### g_m 标注迁移：第 3 关删黄 g_m / 第 4 关作答后受控源右侧显红 g_m（2026-11-01 午 10，用户指令）

补丁 `tools/patch_cs1_gm4.py`（2 处；脚本无 dry 分支，直接唯一性校验后写盘，误跑第二次重放 FAIL 属正常），备份 `/tmp/cs-g1.before-gm4.html`。
- **① fx-t-src 内黄色 g_m 删除**：第 1—3 问及第 4 问选项期间菱形左侧均无 g_m，只剩黄色 v_gs 列。
- **② fx-t-idlabel 改为红色 g_m**：原箭头旁红色 g_m·v_gs（548,222）移除，文字改为单独 g_m，置于受控源**右侧** x=581（菱形右顶点 560 + 21px，与原左侧 479→500 的 21px 距离一致）、y=352 与 v_gs 同基线；仍走第 4 问**作答后**与箭头同现的 idlabel 机制（选项弹出时不显示）。
- 断言脚本 gmText 断言改读 #fx-t-idlabel（gm@581,352/#ff5252）并补 srcText=0 校验（fx-t-src 内无任何 text）。
- 验收：四态断言（ts=1/3/4 opIdLabel=0、ts=6 opIdLabel=1）；ts=6 截图目检（左 v_gs 右红 g_m，与 R_d 净隙足够）；svg-layout-check exit 0；autoclear 100/98/归零；deliver_check PASS。

### 用户纠正：恢复箭头旁 g_m·v_gs / q-gm 移到受控源右侧（2026-11-01 午 11，用户指令）

背景：午 10 误删箭头旁 g_m·v_gs（用户并未要求改这里）；且第 4 关（mix·phase1 只显 q-gm）的红色 q-gm (440,368) 恰好压在等效态 v_gs (435,352) 下方——用户说的「重叠在 vgs 下方的 gm」即它。补丁 `tools/patch_cs1_gm5.py`（2 处），备份 `/tmp/cs-g1.before-gm5.html`；专项 `tools/cs-g1-gm-check.js`（L3 完成态断言 + completeLevel 推进第 4 关断言 + 双截图）。

- **① 恢复箭头旁 g_m·v_gs**：fx-t-idlabel 回到 (548,222, anchor start)，第 4 问作答后与箭头同现；删除午 10 加在 fx-t-idlabel 里的右侧 g_m（581）。
- **② q-gm 移到受控源右侧**：标注 (440,368)→(581,352)（菱形右顶点 560+21px，与 v_gs 同基线），热区 rect 404,340→545,324（72×56 跟随）。第 4 关点它填 Av 表达式 g_m 位置更贴受控源、不再压 v_gs；第 2/3 关 qlabels 不含 q-gm，不受影响。
- **第 3 关完成态**：左侧仅黄 v_gs，箭头旁 g_m·v_gs，右侧无 gm（q-gm 由第 4 关才显示）——与用户「第 4 关时在受控源右侧显示个红色 gm 即可」吻合。
- 验收：L3 断言（idlabel opacity 1 / "gm·vgs"@548,222 / qlabel-layer 0）；L4 断言（level 4、q-gm 可见可点 @581,352、与 v_gs 盒间隔 110px、fx-t-idlabel 仍显示）；截图 gm-l3done.png / gm-l4.png 目检无压线；svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零（第 4 关点 q-gm 填表达式命中正常）；deliver_check PASS。

### TQUIZ 前插「v_gs 极性选择」问（2026-11-01 午 12，用户指令）

补丁 `tools/patch_cs1_polq.py`（3 处），备份 `/tmp/cs-g1.before-polq.html`。TQUIZ 由 4 问变 5 问，总分不变（池 4 分、每题错扣 1、正误均推进）。

- **新问 1/5**：dots=[fx-dot-g, fx-dot-s]（等效态 G/S 红点，.qdot 常驻闪烁动画即满足「闪烁」要求，零新增 CSS）；opts=['上＋下－','上－下＋'] 随机顺序（沿用 Fisher-Yates）；ok='上＋下－'（N 沟道 v_gs>0）；作答后 reveal fx-t-vgs（原问 2 的 reveal 保留，幂等）。
- **选项渲染**：tquizOptHtml 新增极性选项分支——竖排极性柱（上端符号 / v_gs 斜体 / 下端符号，17/15px），与图上标注形态一致；纯文本判定不受影响。
- **回归适配**：cs-g1-equiv-shot.js ts 序列 1/3/4/6 → 1/2/4/5/6（五问错位）；autoclear 按 TQUIZ.length/TQUIZ[k].ok 自动推导，零改动。
- 验收：ts=1 选项随机（textContent 序 ["－上vgs＋下","＋上vgs－下"]）、opVgs=0；ts=2 opVgs=1；ts=4 opSrc=0 且 dotS=530（epos 正常）；ts=5 opSrc=1；ts=6 opId/opIdLabel=1；截图 eq-ts1 目检（按钮竖排不重叠、题干「第 1/5 问：v_gs 的标注极性应怎样表示？」）；布局 exit 0；autoclear 100 [12,24,22,42] / 98 / 归零；deliver_check PASS。

### v_gs 极性选项精修：去「上/下」字 + v_gs 与 ＋/－ 垂直同轴（2026-11-01 午 13，用户指令）

直接 Edit tquizOptHtml 极性分支 2 处（脚本无坐标，未走补丁脚本），备份沿用 `/tmp/cs-g1.before-polq.html`。
- 选项改为纯竖排极性柱：`＋ / v_gs / －` 与 `－ / v_gs / ＋`（44px 定宽容器，三行 width:100%+text-align:center）。
- **踩坑**：调试测量曾误把下标 span（gs，贴在 v 右侧）的盒中心当作 v_gs 行偏右 4px，加了 left:-4px 补偿反而左偏——放大截图目检后撤销；最终三行盒中心严格一致（394/394/394 与 506/506/506），真实鼠标判定不变（label 仍为「上＋下－」/「上－下＋」）。
- 验收：pol-opt-zoom.png 目检同轴；autoclear 三路径 100/98/归零；deliver_check PASS。

### 三项微调：I_DQ/I_DO 上移 15 / v_gs 选项垂直居中 / TQUIZ 顺序交换（2026-11-01 午 14，用户指令）

补丁脚本内联（3 处原子替换）＋ 1 处 Edit（v_gs top:-2px），备份 `/tmp/cs-g1.before-order.html`。

- **① 第 2 关**：q-idq 文字 y 195→180、q-ido 文字 y 200→185（各上移 15px），热区 rect 同步跟随（q-idq 156→141、q-ido 176→161）保持命中。截图 l2-idq-zoom.png 目检：I_DQ 与箭头同轴协调、I_DO 正常无重叠。
- **② v_gs 选项垂直居中**：放大目检发现 v_gs 墨迹重心偏下约 2px（下标下沉），v_gs 行加 position:relative;top:-2px；三行盒中心 287/304/325 → v_gs 视觉位于 ＋、－ 正中间。
- **③ TQUIZ 顺序交换**：第 1 问改回「G、S 之间相当于什么？」（reveal fx-t-vgs），第 2 问为「v_gs 的标注极性应怎样表示？」（dots 仍为 G/S 红点闪烁，去掉 reveal——v_gs 已由第 1 问显示，看着标注选极性）；选项随机顺序、判定逻辑不变。TQUIZ.length 仍 5，autoclear 自动适配。
- 验收：断言 TQUIZ[0].q='G、S…'/TQUIZ[1].q='v_gs…'、ts=2 弹极性选项；I_DQ 文字 y=180 / I_DO y=185；svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零；deliver_check PASS（8765 服务中途掉线，重启后复验通过）。

### 第 5 问箭头与 g_m·v_gs 下移 30px（2026-11-01 午 15，用户指令）

内联原子替换 2 处，备份 `/tmp/cs-g1.before-id30.html`。
- fx-t-id 箭头：line 196-230 → 226-260、polygon 头 244/229 → 274/259；fx-t-idlabel 文字 y 222→252。
- 断言 arrow=226-260、labelY=252；截图 id-down30-zoom.png 目检：文字与箭头同轴、距菱形上顶点（319）间隙充足、无压线。svg-layout-check exit 0；autoclear 三路径 100/98/归零；deliver_check PASS。

### v_gs 显示时机纠正：开路问不再带出 v_gs，极性问作答后才显示（2026-11-01 晚 1，用户指令）

内联原子替换 1 处，备份 `/tmp/cs-g1.before-vgsreveal.html`。
- TQUIZ[0]「G、S 之间相当于什么？」去掉 reveal: 'fx-t-vgs'；reveal 移到 TQUIZ[1]「v_gs 的标注极性应怎样表示？」——开路答完后 G—S 间仍是空白开路段（红点继续闪烁），选完极性 v_gs 与 ＋/－ 才出现。
- 验收：断言 ts=1/2 vgs=0、ts=3 vgs=1、ts=6 vgs=src=1；真实点击第 2 问正确项后 vgs 0→1；截图 vgsq-2-zoom / vgsq-3-zoom 目检（第 2 问电路无 v_gs、第 3 问 ＋ 已现）；svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零；deliver_check PASS（8765 服务再次掉线，重启后复验）。

### 第 2 关 I_DQ 常数/指数方框化 + 数字按钮行点选输入（2026-11-07，用户指令）

补丁 `tools/patch_cs1_numpad.py`（9 处，dry 全 OK 后写盘），备份 `/tmp/cs-g1.before-numpad.html`；专项脚本 `tools/cs-g1-numpad-check.js`（13 项断言 + 真实鼠标点击 + 截图）。移植自 cs-g2 r8 成熟方案。

- **① 方框化**：I_DQ 框架三条选项与 I_DQ 表达式中「−1」的常数 1 → 标准虚线框；「)²」的指数 2 → `box:{sup:1}` 小号上标框（w=0.82s、h=0.60s、rx=4、右上角，buildExpr 新增 sup 分支，data-num-sup 标记）。三框架选项均方框化不泄题。
- **② 数字按钮行**：I_DQ fill 子步新增 `numPad:true` → renderMix 在表达式上方画提示「常数：先点虚线框，再点数字」（BODY_TOP+100）+ 0~9 圆角按钮行（BODY_TOP+116 起，42×44 间距 8，.num-key 样式随 cs-g2）。其余子步（无数字空）不显示。
- **③ 作答链路**：num-key 点击 → 以 `num-<digit>` 走 answerBlank；常数空 ansIds=['num-1']/['num-2']、pts:0（不计分不扣分，保持 24 分配平——9 框架 + 2/1/1 + 2/1/1 + 2/2/2 填空 + 框架分不变）；答错只提示「常数不对，请再选一个数字」；回填常数/指数用绿色 27/20 号字（sup 框 20 号）。
- **计分终态**：L2 仍 24 = 3 框架×3 + V_GSQ 2/1/1 + I_DQ 2/1/1 + V_DSQ 1/2/2；全站 100 不变（autoclear [12,24,22,42] 复验）。
- 验收：13 项断言全 PASS（几何：keys.bot=512 < exprTop=538 净距 26px；x9=1464 ≤ 1530；上标框 34×25 vs 常数框 50×34 高 25px）；真实鼠标点错数字不填可重试、点 1/2 正确回填；idq-numpad-zoom.png 目检（按钮行整齐、间距合理、绿 1 与上标绿 2 形态正确）；svg-layout-check exit 0；autoclear 三路径 100/98/归零；deliver_check PASS（8765 服务重启后复验）。


### 等效态 v_o 端子圆对齐 + V_i ＋/－ 贴端子圆 15px（2026-11-07，用户指令）

直接 Edit 4 处（comp-vo 加 id / eq-layer Vi 文字 / showEquiv / resetCircuit），无独立补丁脚本。
- **① v_o 端子圆错位**：comp-vo 圆在 (700,168)（默认态导线 y=168），等效态输出导线为 eq-layer `M 530 178 H 692`（y=178）→ 圆错位 10px。circle/text 加 id `vo-circle`/`vo-label`；showEquiv() 置 cy=178、labelY=191，resetCircuit() 复位 168/181。
- **② V_i ＋/－ 贴圆**：eq-layer 端子圆 (150,178)/(150,525) r=8，原 ＋ y=290 / － y=430 离圆 71/79px。按墨迹 bbox 计：＋ y=234（墨迹顶 201 = 圆底 186+15）、－ y=494（墨迹底 502 = 圆顶 517−15）、v_i y=362（墨迹中心 351.3 ≈ 201..502 中点 351.5）。与默认态 comp-vi 同口径（默认态墨迹距圆 15px）。
- 验收：几何断言（vo 圆左缘 692=导线端点、gap＋=15 / gap－=15、默认态 cy=168 不变）；截图 vo-eqv6-zoom / vo-eqv6-vi 目检；svg-layout-check exit 0；autoclear 三路径 100 [12,24,22,42] / 98 / 归零；deliver_check PASS。

## ★ 第116轮（2026-11-09）：结算页得分项改左对齐
- renderDone 得分项由居中改为左对齐：新增 doneLeftX(arr)（量最长行宽→整块在面板内居中→各行 anchor:start 左缘统一），
  行距与行序不变。回归 align_done_test 断言 PASS（各行左缘一致、右缘不溢出、0 pageerror）；deliver_check 双通道 ok。
- 版本：lab ?v= 递增（data.js 同步）、index data.js?v=12.39；缩略图不动（结算页非首屏）。

## ★ 第117轮（2026-11-09）：整理/等效态电阻统一 27×53
- 本页遗留旧尺寸电阻（36×90/36×80/27×60/28×55）统一为 27×53：保持几何中心不变改 rect，上下引线端点同步；
  标签与体中心对齐故不动。svg-layout EXIT=0；等效/整理态截图目检引线无空隙；首屏不变缩略图不动。
- 版本：lab ?v= 递增（data.js 同步）；index data.js?v=12.40。
