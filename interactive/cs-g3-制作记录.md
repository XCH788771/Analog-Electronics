# cs-g3 游戏闯关 · 分压式偏置共源放大电路 · 案例3 — 制作记录

> ⚠️ **2026-10-26 内容归位修正**：此前本页内容与 cs-g1.html 错位（「单电源分压式偏置共源完整版」被写进了 cs-g1.html，而双电源案例1 被写进了本页）。经用户裁决，两页内容已互换归位——**本记录对应当前 cs-g3.html（单电源分压式偏置共源 · 案例3）**。双电源案例1 内容见 `cs-g1.html` 与 `cs-g1-制作记录.md`。互换脚本 `tools/swap_csg1g3.py`，原文件备份于 `.workbuddy/archive/bak-csg1g3-swap-20261026/`。


> 状态：**已定稿**（2026-10-24 深夜）。布局自检 `tools/svg-layout-check.py` **EXIT=0**（0 错 0 警）；自动化回归 `tools/cs-g1-flow-test.js` **全路径通过**（路径A 满分 100、路径B 容错 99、真实鼠标命中、重新挑战归零，0 pageerror）；15 个钩子态 + 真实流程态截图目检通过。
> 文件：`网站/interactive/cs-g1.html`（381,635 字节 / 2,566 行，由 `_game-template.html` 经 **Temp/build_cs_g1.py 原子补丁重建**，蓝本 cj-g1 共射引擎）。
> 入口：`data.js` → `cs-b1`（共源放大电路）→ `cases.game` **案例1**（lab `interactive/cs-g1.html?v=2`、thumbImg `assets/thumb-cs-g1.png?v=6`，ready:true）；index.html `data.js?v=11.40`。
> 生成链：`Temp/cs_g1_regionB.svg`（电路整块）+ `Temp/cs_g1_regionC.js`（GAME_CONFIG + STAGE_UNITS）→ `Temp/build_cs_g1.py`（内容锚点行块替换 5 区块 + **26 处引擎 rep**（唯一性校验）+ 残留 BJT id 检查 + 必需 id 检查 + pts=100 校验 + 关卡数校验；`io.open newline=''` 保 LF）。
> 回归脚本：`网站/interactive/tools/cs-g1-flow-test.js`（路径A 全对 / 路径B Av框架错1次 / 路径C 真实鼠标 / 路径D 重新挑战归零）。截图脚本：`tools/cs-g1-shot.js`（15 态 → `assets/shots/cs-g1-*.png`）。

## 电路结构与教学核心（用户截图口径 = 原题完整电路）

**标准分压式偏置共源（N 沟道增强型 MOSFET）放大电路**：+V_DD（右上端子）→ 顶轨；R_G1（左上竖）→ 分压节点 → R_G2（左下竖）→ 地轨；分压节点 → R_G（栅极节点下方竖块）→ 栅极节点（输入导线，带圆点）→ 栅极引线右行至 MOSFET 栅极；V_i 端口 → C_1 → 栅极节点；MOSFET（栅极竖条 + 沟道竖线 + D/G/S 三水平引线，**栅极引线上箭头指向左**）；漏极节点 → R_D（上）∥ C_2 → R_L → 地（V_o 跨 R_L，反相）；源极节点 → R_S → 地 ∥ C_S 旁路。题面：「如图共源放大电路，已知 g_m，各电阻及电源电压，求动态性能指标」，**不给数值、全部符号表达式**。

**公式口径（完整还原原题：R_S 被 C_S 旁路、R_G 串联于分压节点与栅极之间、含 R_L 负载）**：
- A_v = **−g_m·(R_D∥R_L)**（共源反相；漏负号、R_D∥R_L 同级并联为两个干扰项）
- R_i = **R_G + (R_G1∥R_G2)**（栅极电流为零；R_G 与分压支路并联组合串联）
- R_o ≈ **R_D**（受控源开路，R_L 为外接负载不计入）

## 关卡设计（单阶段三关，总分 100）

| 关 | 内容 | 计分 |
|---|---|---|
| 第1关 绘制交流微变等效电路 | draw：gate `['comp-vdd']`；subSteps 三步——① 交流通路（c1/c2/cs 短路各 5 + vdd 置零接地 5）② 整理电路（rs 移除 5 + R_G1/R_D 翻转下挂）③ 等效场效应管（t-equiv 不计分，TQUIZ **五连问池 2** 独立结算）；6 目标 round(27/6)=5，5×5+2=27 | **27** |
| 第2关 电压放大倍数 | mix：A_v 框架（3 选 1，qpts 4 pen 1）+ 表达式 3 空×8（空0=g_m 点跨导标注 q-gm；空1/2=R_D∥R_L，grp `av-par` 可交换，ansIds 收 comp-rd/comp-rdd/comp-rl） | **28** |
| 第3关 输入电阻与输出电阻 | mix：Ri 框架（qpts 6 pen 2）+ Ri 表达式 3 空×8（空0=R_G；空1/2=R_G1∥R_G2，grp `ri-par`，ansIds 收 comp-rg1/comp-rg1d/comp-rg2）；Ro 框架（qpts 5 pen 2）+ Ro 表达式 1 空×10（R_D，ansIds 收 comp-rd/comp-rdd） | **45** |

**27+28+45=100**；填空空分均整除（8/8/8、8/8/8、10），框架 pen 按 qpts 配置。L2/L3 均为「框架 → 填空」交错，mix 引擎按 `steps[si].type` 动态驱动。

## TQUIZ 等效五连问（第1关第3步，池 2）

1. G、S 之间相当于什么？→ **开路**（G–S 输入电阻无穷大；dots g+s）
2. D、S 之间相当于什么？→ **受控源**（reveal `fx-t-src` 菱形受控源；dots d+s）
3. 受控源电流 i_d 方向？→ **↓i_d**（reveal `fx-t-id` 红色向下箭头；dots d）
4. 该受控源的类型？→ **电压控制电流源**（dots d）
5. 受控源电流大小与哪个电压成正比？→ **栅源电压**（dots g+s）

答错从池扣 1，无论对错都推进下一问并画出正确结果（与 cj/lin 系列口径一致）。选项条位置 `cx:450, cy:332`（等效态顶轨收起后的空白带中心）。DOM 文本无下划线（`↓i_d` 渲染为 `↓i`+下标 d）。

## 引擎侧 ★换案例 数据点（均在 Temp/build_cs_g1.py）

- `GAME_CONFIG`：单阶段（动态分析）三关；L1 `gate:['comp-vdd']` + `fadeWith`（c1 连锁移除输入回路、c2 连锁移除输出回路、cs 连锁移除源极旁路支路）；`subSteps` 三步（ids / ids+moveIds / ids）；L2/L3 `mix` `subs`（fw+fill 交错），`stageUnits` 0/1
- `STAGE_UNITS`：两组共 **43 个非 fx-layer 交互单元**（布局自检完备性要求）；下挂件 comp-rg1d/comp-rdd 在 fx-layer 内、不列入（命中由填空 ansIds 与 highlightStage 单独通道处理）
- `ANNOS`：43 条空壳（游戏页不挂悬停注解/语音，防直接提示答案；与 STAGE_UNITS 并集齐配）
- `CAP_FX`：c1/c2/cs → fx-c1/fx-c2/fx-cs；`execAct`：vcc-gnd（rep `showFx('fx-vcc')`→`showFx('fx-vdd')` 保留 act 名）/ rs-remove / re-remove 已移除 / cap-short·cap-open；补 `vi-keep/vi-open` 引用清理
- `showEquiv`：`showFx('fx-tmodel', true)`（含 fx-t-src / fx-t-gm / fx-t-id / fx-dot-g/d/s）；本案例**不需 eq-layer / 不需 setCircuitShift**（等效态骨架不动，仅切模型层）
- `moveCompDown`：rg1 分支（右移 rg1-label）→ `showFx('rarr-rg1')` 并 `pointerEvents='all'`；rd 分支（右移 rarr-rd）→ fadeGroup node-drain
- `TQUIZ` / `tquizOptHtml` / `startTQuiz pool:2` / `showTQuizMenu` 文案「场效应管等效」；`menuItemsFor`：comp-rg1→与RG2串/并、comp-rd→与RL串/并（下移串/并菜单）
- `resetCircuit`：清零清单 fx-c1/fx-c2/fx-cs/fx-vdd/fx-rs/fx-tmodel/fx-t-gm/fx-t-src/fx-t-id/fx-dot-g/d/s、rarr-rg1/rarr-rd + `.rg2-label` 恢复原位 + `.vcc-label` 显隐复位
- `renderProgress`：nStatic=3 + 单阶段标签「动态分析」；`renderDone`：「动态性能指标掌握扎实」
- 调试钩子：`?lvl=1..3` 逐关 / `?lvl=1&tidy=1` 整理+等效布局 / `?lvl=1&ts=1..5` 等效各问、`&ts=6` 全部完成态 / `?lvl=2&ms=2`（L2 填空）/ `?lvl=3&ms=2·3·4`（L3 Ri填空/Ro框架/Ro填空）/ `?lvl=done`

## 自检记录（2026-10-24 深夜）

- **布局自检** `tools/svg-layout-check.py cs-g1.html` **EXIT=0**：43 单元 / STAGE_UNITS / ANNOS 全覆盖、标签 0 冲突、导线全连接、无交叉、边界安全；5 处导线不均衡为提示级（拓扑决定，不判失败）。`comp-t` data-name 含「场效应管」三字（过悬空豁免，与 cs-g2 口径一致）；C1 标注 `x=213 y=245`、rg2-label 独立 class（避让 ≥14px）。
- **语法**：内联脚本 `node --check` 通过（构建脚本已校验）。
- **回归** `tools/cs-g1-flow-test.js` **全路径通过**：
  - 路径A（全对）：L1 27 → L2 28 → L3 45，**总分 100 finished**，分项 [27,28,45]
  - 路径B（L2 A_v 框架错 1 次，pen 1 → 28→27）：L1 27 → L2 27 → L3 45，**总分 99 finished**
  - 路径C（真实鼠标）：`?lvl=1` 悬停 comp-vdd 两级菜单（置零→接地）命中记分；`?lvl=3` 点虚线框 + 真实鼠标点 comp-rg(390,285)/comp-rg1(250,140) 均命中并记分
  - 路径D（重新挑战）：通关后点「重新挑战」→ score=0 / level=1 / finished=false
  - 四条路径均 **0 pageerror / 0 console.error**
- **截图目检**：15 态（default / l1 / l1-tidy / l1-ts1..6 / l2 / l2-fill / l3 / l3-ri-fill / l3-ro-fw / l3-ro-fill）全部正常——默认态元件齐全无压线、整理态电源置零+RS 移除变导线+RG1/RD 下挂、TQUIZ 五态揭示件（菱形受控源 + ↓i_d 红箭头 + g_m·V_gs 红标注）正确、mix 关面板三选项与填空框布局合理不压电路、提示文案去答案化。
- **缩略图**：`tools/thumb-gen.js cs-g1 --wait 3000` 生成 `assets/thumb-cs-g1.png`（1280×720，182KB，PNG 校验通过），画面文字含「案例1：分压式偏置共源 · 求动态性能指标」正确；data.js `thumbImg ?v=5→6`、index.html `data.js?v=11.39→11.40` 已联动击破。

## ★ 踩坑与决策

1. **并行会话冲突（关键）**：构建期间 `cs-g1.html` 被另一会话活跃写入（四关 26/26/24/24 简化设计、moveCompDown 仍是 BJT 版、缺 R_S/C_S/R_G/R_L 与原题不符），data.js 入口已挂 `?v=1`。按「同一页面严禁两会话并行修改」纪律先请示，**用户裁决用本设计整体覆盖**——备份旧版至 `.workbuddy/archive/bak-cs-g1-20261024/cs-g1-parallel-session.html` 后写盘。
2. **残留 BJT id 检查**：构建脚本原漏 `execAct` 的 `case 'vcc-gnd'` 仍 `showFx('fx-vcc')` → 补 rep `fx-vcc→fx-vdd`（保留 act 名）；并扩充 leftover 清单（comp-rb1/rc/re/ce/fx-re/ce/rarr-rb1/rc/eq-rb1/2/fx-t-rbe/ib/fx-dot-b/q-vbq/comp-src 等），同时排除与本题**撞名件**（wire-gnd-l/m/r、wire-c2-out、wire-rl-bot、wire-rs-top/bot 等本案例复用名）与保留的 `setEPos` 壳（含 fx-dot-e 引用，null 保护）。
3. **regionB rearr-layer 位置错误**：原 `rearr-layer` 注释称在 fx-layer 内，实际写在 fx-layer 闭合标签之外 → 整理件被静态布局检查误判。修复：将 rarr-rg1/rarr-rd 整组移入 fx-layer 闭合前，确保不参与静态检查（以截图目检把关等效态）。
4. **布局自检完备性**：STAGE_UNITS 须恰好覆盖 43 个非 fx-layer 交互单元、ANNOS 须 43 条；`comp-t` data-name 须含「场效应管」过悬空豁免；C1 标注 y 由 140→245、rg2-label 加独立 class 避让标签冲突。
5. **thumb-gen 参数 bug**：无 `--wait` 时 `argv[waitIdx+1]` 误删首个位置 id → 必须 `cs-g1 --wait 3000` 才保留 id（规避方式已写入脚本用法注释）。
6. **案例编号口径（关键，依用户 21:45 裁决）**：用户 2026-10-24 21:45 裁决明确「cs-g1=分压式案例1、cs-g2=案例2、cs-g3=双电源分压案例3，三者均为分压式属有意设计、编号无冲突、不得自行改编号」。本页虽源于用户早期「分压式放大案例3」的提法，但该提法实际对应 cs-g3（已落位定稿为案例3）；按裁决本页统一为 **案例1**（页面标题/案例行/数据入口一致），与 cs-g2=案例2 的 cs 系列编号对齐。如需改回显示案例3 须先与 cs-g3 编号冲突问题一并请示用户。

## 待办 / 备注

- `Temp/` 下 `build_cs_g1.py` / `cs_g1_regionB.svg` / `cs_g1_regionC.js` 为可复现构建蓝本，如需微调电路或关卡可直接改源文件重建（rep 唯一性校验保证不破坏模板）。
- 真实鼠标命中已验证 comp-vdd 两级菜单与 comp-rg/comp-rg1 填空；若后续新增交互件，须同步补 `hit-off` 隔离与真实鼠标回归。

## 修订记录（2026-10-26 22:50）

- **场效应管符号修正**：原 `comp-t` 采用「实线沟道 + 多余中部长横线带箭头 + 无衬底 B」的非标准/易混淆画法，与「游戏-共源放大-恒流源放大案例1」(cs-g5) 的增强型标准符号不一致。用户要求改为与 cs-g5 一致。
  - 改为 cs-g5 同款增强型 NMOS 画法：**三段断开沟道**（零栅压无沟道）、**栅极电极竖条**与沟道平行（栅氧化层电容耦合、绝缘）、**衬底 B 引线 + 内向箭头**（N 沟道）、**g/d/s/B 端子标注**。
  - 保持端子坐标不变（栅极引线 470,178 / 漏极 530,140 / 源极 530,216），故接线、L1 `t-equiv`（fadeGroup 隐藏 comp-t 后显示 fx-tmodel 受控源）、L2/L3 填空作答判定均不受影响。
  - 布局自检 `svg-layout-check.py` 经两次迭代：初版 d/s 与 B 标注 bbox 互压（B 居中 y178 与上下 d/s 纵向重叠）→ 将 d 上移(y150→128)、s 下移(y210→238)、d 右移(x553→558 清 R_D 贴边警告)，复检 EXIT=0（0 标签冲突 / 0 贴边）。
  - 截图目检 default 与 equiv 两态均正确：default 三段断开沟道+衬底 B 清晰无压线；equiv 下 comp-t 已隐藏、fx-tmodel 按 TQUIZ 进度逐问揭示（非 bug）。
  - 回归 `tools/cs-g1-flow-test.js` 四路径（100/99/真实鼠标/重新挑战）仍 0 pageerror。
  - 缩略图 `thumb-gen.js cs-g1 --wait 3000` 重截（首屏含新 FET），`thumbImg ?v=6→7`、index `data.js?v=11.45`、`lab ?v=2→3` 已联动击破。

## 修订记录（2026-10-26 23:50 栅极几何对齐 cs-g5）

- **背景**：22:50 已将 `comp-t` 符号对齐 cs-g5 增强型 NMOS，但**端子坐标保持未动**——栅极条仍在 x=470、沟道 x=530，间距 **60px**，是 5 个共源页中唯一"栅极孤悬"者（cs-g2/g5 间距 28、cs-g3/g4 间距 14）。用户据此要求「参照 cs-g5 的 gate-align，把 G 极改成一致」。本次是 22:50 符号对齐的**几何延续**。
- **默认态**：栅极条 470→502（贴近沟道 530，间距 28，对齐 cs-g5）；g 标签 448→492；栅极引线 `wire-gate-out` 终点 470→502。
- **等效态（fx-tmodel，叠加式；setEPos 空操作、端点固定）**：G 端子圆 470→502；受控源菱形右移 24（左尖 498→522，与 G 端子净距 14）；D-S 上/下支路由竖线改为小拐折 `path` 连接漏/源节点 (530) 与菱形 (554)；g_m 标注热区/文字右移（rect 566→586、text 572→590）避开 C_2(x670)；i_d 箭头随菱形 530→554；`fx-dot-g` 红点 470→502。红点 D(530,140)/S(530,216) 保持漏/源节点不动。
- **为何不照搬 cs-g5 下挂式等效态**：cs-g5 用 `eq-layer` 整体重排（栅极线/漏极线上移 y176、受控源下挂、S 由 setEPos 动态移），cs-g1 用 fx-tmodel 叠加 + setEPos 空操作，两套引擎；且 cs-g1 等效态右侧 g_m/C_2 空间紧凑。故选「默认态完整对齐 + 等效态最小避让」，**未重写引擎**，回归确认三关交互不被破坏。
- **验证**：`svg-layout-check.py` EXIT=0；`cs-g1-flow-test.js` 四路径 100/99/真实鼠标/归零，0 pageerror；默认态截图栅极贴近沟道无重叠；等效态(`?lvl=1&ts=6`)实测 fx-tmodel opacity=1、G 端子(右缘 508)与菱形(左尖 522)净距 14、g_m 右缘(屏 549)不压 C_2。
- **版本联动**：`thumb-gen.js cs-g1 --wait 3500` 重截默认态 → `thumbImg ?v=8`、index `data.js?v=11.46`；`lab ?v=3→4`。补丁脚本 `.workbuddy/tmp_cs1/patch_g1_gate.py`（15 处 rep 唯一性校验）；改动前备份 `.workbuddy/archive/bak-g1-gate-20261026/`。

## 修订记录（2026-10-27 20:55 栅极引线直角化 · G 极接栅极竖线下端）

- **动因**：用户要求「将 V_i 上方的水平导线、C1，以及 G 极水平导线下移到 G 极竖线底端对齐，形成直角形状」（对齐 cs-g5/cs-g1 的 G 极画法）。原 `wire-gate-out` = `M 390 178 H 502` 接在栅极竖条（x=502, y150→206）**中点 178**，成 T 形。
- **★几何约束（为何整列不能下移 28）**：偏置分压支路 `wire-rg1b` 竖在 x=250（y185→330），正好夹在 C1（x220）与栅极节点（x390）之间；输入列若整列下移到 y=206，必与该竖线在 (250,206) **真交叉**（布局自检 ⑤ 硬错误，exit 1）。绕开该竖线的三条路都不可行：①分压支路移到端口左侧（x<110）→ 标签宽 78px 越出画布左缘，且「整理电路」`rarr-rg1` 需 x=170 的下挂位；②移到栅极条右侧（x>502）→ 被漏极横线 y=140（530→622）截断；③R_G1 上下挪动 → 只要 tap 在 330、R_G1 在轨下，其下端引线必跨 y=206。
- **实现（L 形折弯，节点随之下移）**：`wire-in-gate` `M 220 178 H 390` → `M 220 178 H 390 V 206`；`node-gate` (390,178)→(390,**206**)（栅极竖线下端高度）；`wire-gate-out` `M 390 178 H 502` → `M 390 206 H 502`（自节点水平进入竖条下端 = 直角）；`wire-rg-top` 起点 178→206（R_G 本体 240-330 不动）。
- **等效态**：G 端子圆 `cx=502 cy=178` → `cy=206`、`fx-dot-g` 红点同步（qdot），受控源菱形 (530,178)/g_m 标注不动（G 端子 502,206 距左尖 522,178 净距 20）。
- **验证**：`svg-layout-check.py` EXIT=0（②互压 0 / ③标签冲突 0 / ③b 穿行 0 / ⑤交叉 0）；`tools/cs-g1-flow-test.js` 四路径 26→100 [27,28,45] / 99 / 真实鼠标命中 comp-rg·comp-rg1 / 重新挑战归零，0 pageerror；默认态与等效态截图目检通过。
- **版本联动**：`thumb-gen.js cs-g3 --wait 3000` 重截（首屏含新走线）→ `thumbImg ?v=5→6`、index `data.js?v=11.48→11.49`；`lab ?v=2→3`。
- **备份**：`.workbuddy/tmp_csg3/cs-g3.before-rightangle.html`（改动前）、`.workbuddy/archive/bak-thumb-20261027/thumb-cs-g3.before-rightangle.png`；补丁脚本 `.workbuddy/tmp_csg3/patch_gate_rightangle.py`（8 处 rep 唯一性校验）。

## ★更正（2026-10-27 21:12）——上一条 20:55 修订系改错页面，已整体回退

- **原因**：用户指出「这一个案例的文件是 cs-g2.html」。该次直角化改造目标页判断错误，实际应由 **cs-g2**（分压式·案例2）承接，cs-g3 未获指示。
- **回退内容**：`网站/interactive/cs-g3.html` 以 `.workbuddy/tmp_csg3/cs-g3.before-rightangle.html` 覆盖还原（md5 `cd0d32c8…`，`wire-gate-out` 复原为 `M 390 178 H 502`，接栅极竖条中点＝T 形）；`assets/thumb-cs-g3.png` 以 `.workbuddy/archive/bak-thumb-20261027/thumb-cs-g3.before-rightangle.png` 还原；`data.js` 回退 `lab ?v=2`、`thumbImg ?v=5`。
- **保留事实**：cs-g3 栅极引线目前仍是 **T 形**（接栅极竖条 x=502 的中点 178）。若要按 cs-g5 口径改直角，注意 `wire-rg1b`(x=250) 挡路，需走 L 形折弯方案（补丁已备，等指示）。

## 修订记录（2026-10-27 21:45 场效应管符号清理 · 清孤立节点）

- **动因**：用户指出 cs-g3 电路「绘制得乱七八糟」，要求重绘。附截图在本地渲染为深色背景下的白色元件轮廓、无法还原可读电路文字（疑似截图时字体/细线未渲染），故按标准拓扑 + 恒流源案例1（cs-g5）同款增强型 MOSFET 风格做清理。
- **改动（保留全部节点坐标，确保 fx-layer 等效态 / rearr-layer 整理态逻辑不变）**：
  1. `comp-t` 重绘：栅极竖条（x=502, y144-212）与三段沟道（x=530，断口拉开至 140/168/196）保持；衬底 B 箭头放大并明确指向沟道（N 沟道向内），B 引线向右伸长；**g/d/s/B 四个标注全部移到符号外空白**（g 482,238 / d 562,122 / s 562,248 / B 592,190），消除原「B 紧贴符号」的拥挤。
  2. 删除误导性孤立节点圆 `node-rd-top`（顶轨与 +VDD 延伸线在 x=640,y=5 处为共线拐角，非节点）；同步从 `STAGE_UNITS`、ANNOS、`fadeGroup` 收起循环三处移除该 id 引用。
- **★澄清（与 20:55 直角化修订的关系）**：制作记录前述「栅极引线直角化」(node-gate 移 y=206、wire-gate-out `M 390 206 H 502`) 当前 cs-g3 已不保留——data.js 的 `lab`/`thumbImg` 版本号曾被重置回 ?v=2/?v=5，表明该修订被回退或覆盖。现栅极引线为 T 形 `M 390 178 H 502`（接栅极竖条中点），电路截图目检整洁，**本轮不再强改直角**（若需对齐 cs-g5 直角栅极可一键再应用）。
- **验证**：`svg-layout-check.py` EXIT=0（仅 5 条提示级导线不均，拓扑决定）；`tools/cs-g3-flow-test.js`（由 `cs-g1-flow-test.js` 更名，实际指向 cs-g3.html）四路径 **100/99/真实鼠标命中 comp-rg·comp-rg1/重新挑战归零** 0 pageerror；默认态与等效态截图目检通过。
- **挂接**：data.js cs-b1 案例3 `lab ?v=2→3`、`thumbImg ?v=6`（thumb-gen 重截）、index `data.js?v=11.53`；缩略图首屏目检整洁。
- **回归脚本更名**：`tools/cs-g1-flow-test.js` → `tools/cs-g3-flow-test.js`（文件名与实际测试对象 cs-g3 一致；原文件头注释同步指 cs-g3.html）。

## 修订记录（2026-10-27 22:12 电阻缩小 · 高 2/3 宽 3/4）

- **动因**：用户要求「将电阻变小，高变成原来的 2/3，宽变成原来的 3/4」。
- **改动**：原电阻框 90×36 → **60×27**。涉及 8 枚电阻：默认态 `comp-rg1 / comp-rg2 / comp-rg / comp-rd / comp-rl / comp-rs` + 整理层 `comp-rg1d / comp-rdd`（交流等效下挂件，同步缩小保持一致）。每枚缩小后**连线同步收紧**以贴合新电阻体两端、保持节点连接：
  - `comp-rg1`：保持底缘 y=185（其底部导线 `wire-rg1b` 若上移会跨过 `wire-in-gate` 横线 y=178 造成导线交叉，布局判硬错），故向上缩（rect y 125、top 导线 `M 250 5 V 125`）。
  - `comp-rg2`：居中缩（rect y 390、top 导线 `330→390`、bottom 导线 `450→525`）。
  - `comp-rg`：居中缩（rect y 255、top 导线 `178→255`、bottom 导线 `315→330 H 250`）。
  - `comp-rd`：保持底缘＝漏极节点 y=140（rect y 80、top 导线 `5→80`）。
  - `comp-rl`：居中缩（rect y 250、top 导线 `140→250`、bottom 导线 `310→525`）。
  - `comp-rs`：保持顶缘＝源极节点 y=266（rect y 266 不变、bottom 导线 `326→525`）。
  - 整理层 `comp-rg1d`（rect 156.5,390 / 路径 `330 H170 V390` / `170 450 V525`）、`comp-rdd`（rect 686.5,250 / 路径 `140 V250` / `700 310 V525`）。
  - 标签字号保持 37，标签位置随新电阻体中心微调（rg1→y162、rd→y117、rs→y303，其余维持中心+7）。
- **验证**：`svg-layout-check.py` EXIT=0（0 处导线交叉、仅 4 条提示级导线不均）；`tools/cs-g3-flow-test.js` 四路径 **100/99/真实鼠标命中 comp-rg·comp-rg1/重新挑战归零** 0 pageerror；缩略图 `thumb-gen.js --wait 3000` 重截首屏目检整洁（六电阻均缩小且连线无断点）。
- **挂接**：data.js cs-b1 案例3 `lab ?v=3→4`、`thumbImg ?v=6→8`（thumb-gen 自动推）、index `data.js?v=11.53→11.56`。

### 第103轮（2026-10-27 深夜）全站电阻统一 27×53

- 需求（用户）：所有案例中的电阻统一为 27×53。
- 本页改动 **7 个电阻**（含 comp-t-model 内的 r_be）：竖放一律 `27×53`、横放一律 `53×27`， **几何中心不变**；同步所有端点恰为旧体缘且轴向贯穿中心的 path/line（含 `fx-*` 短接线）；标签坐标不动。
- 工具：`.workbuddy/patch_resistors.py`（字符级绝对定位 + 冲突检测 + 保持行尾 + 干跑）； 分析器 `.workbuddy/analyze_resistors.py` 输出改动前后几何与受影响引线清单。
- 验收：svg-layout-check EXIT=0；默认态截图目检通过（电阻规格一致、两端引线连通、标签不压线）。
- 版本：data.js lab `4→5`；index `data.js?v=11.59`（thumb-gen --all 自动击破）； 缩略图已重截（电阻属首屏可见内容，按第83轮规约必须联动）。
- 归档：`.workbuddy/archive/bak-res-20261027/`（18 页 html + data.js + index.html + 16 张旧缩略图）。

## 2026-10-28 场效应管整体下移 40px（用户指令）
- 需求（用户）：场效应管向下移 40px，RG2、RG、RS、C1 同步下移到合适位置。
- 实现（仅改 cs-g3.html，未动其它案例）：
  - comp-t（FET 符号）全部 y+40；其栅/源/漏三端随动。
  - 栅极节点 node-gate 与输入导线 wire-in-gate 保持在 y=178（避免与 x=250 的 RG1 竖线 wire-rg1b 产生交叉），FET 栅极改由 wire-gate-out 折线（390,178→502,178→502,218）接入；C1 由短竖引线 (220,218)→(220,178) 接到输入导线。
  - RG2/RG/RS 各 y+40；分压节点 node-div 随之下移 40（RG1 下端引线 wire-rg1b 自动延长），使 RG/RG2 自然连接不断开。
  - 漏极节点 node-drain 保持不动（RD/C2 在上端固定），FET 漏极引线改为 `M 530 176.5 V 140 H 670`（向上接到固定漏极节点）。
  - 源极节点 node-source 随 FET 下移 40；旁路 C_S 引线 wire-cs-top 起点同步 +40。
  - 特效层：fx-c1 短路桥、fx-tmodel 等效模型（受控源菱形中心 178→198、栅极端子 cy 218、源极端 +40、漏极端保持 140）、fx-rs 短接桥均同步跟随。
- 工具：`tools/patch_cs_g3_move_fet.py`（49 处原子替换，唯一性校验）；`tools/patch_cs_g3_fix_cross.py`（修正栅极节点交叉 4 处）。
- 验收：svg-layout-check EXIT=0（仅 5 条提示级导线不均，不判失败）；回归 `tools/cs-g3-flow-test.js` 四路径全过（A=100/B=99/C2 真实鼠标命中 comp-rg·comp-rg1/D 重新挑战归零，0 pageerror）；截图目检 FET 下移后三端引线干净、无异常交叉。
- 版本：data.js lab `5→6`、thumbImg `9→10`、index `data.js?v=11.64`；缩略图已重截。
- 回归脚本坐标更新：comp-rg 真实鼠标点击 SVG 坐标 (390,285)→(390,325)（RG 中心随下移变更）。

## 2026-10-28 17:45 输入通路对齐 · FET 净下移 30px · RS 居中（第107轮）
- 用户指令：场效应管下移30px；RS 下移到 S 极与地之间的中间位置；G 极水平导线与竖线的直角做垂直翻转，C1 及左右端导线与翻转后的水平导线对齐；Vᵢ 文字与 ＋/－ 号下移到与地之间的中间。
- **FET 净下移 30px**：上一轮 +40 全量回调 10px（栅极竖条 174-242、三段沟道、衬底 B、g/d/s/B 标注、热区全部 -10；node-source 256→246）。
- **输入通路翻转为一条直水平线 y=208**（栅极竖条中心）：
  - wire-gate-out 由 `M 390 178 H 502 V 218`（先横后竖下拐）改为 `M 390 208 H 502`（水平直达栅条中部，直角消除）；
  - wire-in-gate 由 `M 220 218 V 178 H 390`（先竖后横上拐）改为 `M 220 208 H 390`；
  - C1 两板 y 186-230（中心 208）、fx-c1 短路桥、wire-vi-in、Vᵢ 上端子 (110,208) 全部对齐 y=208；C1 标注随板下移至 275；node-gate 移至 (390,208)；wire-rg-top 起点 208。
- **R_G1 随输入线下移 30px**（体 128.5-181.5→158.5-211.5，标注 162→192）：几何上输入线必须横穿 x=250，唯有穿过 R_G1 体底才不与 wire-rg1b 导线交叉——新布局复刻原「线在体底上方 3.5px」关系（208/211.5），验证通过。
- **R_S 居中 S(246)—地(525)**：中点 385.5，体 359-412，标注 393；wire-rs-top `M 530 246 V 359`、wire-rs-bot `M 530 412 V 525`、fx-rs 同步。
- **Vᵢ 标注组下移 22px**（＋ 297 / Vᵢ 367 / － 437，组中心 367≈(208+525)/2）。
- fx-tmodel 同步：G 端子/红点 (502,208)、受控源菱形中心 193（源侧引线接 246）、g_m·v_gs 标注 -5、i_d 箭头 -5。
- 工具：`tools/patch_cs_g3_input_align.py`（49 处原子替换，唯一性校验；首次运行 pair39 菱形 path 串不匹配未写盘，修正后一次通过）。
- 验收：svg-layout-check EXIT=0（0 交叉，仅 3 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检输入直线、RS 居中、Vᵢ 居中均符合。
- 回归脚本坐标更新：comp-rg1 真实鼠标点击 (250,140)→(250,185)（RG1 中心随下移变更）。
- 版本：data.js lab `6→7`、thumbImg `11→13`（thumb-gen 自动再推）、index `data.js?v=11.65`；缩略图已重截。

## 2026-10-28 22:50 第二轮下移 · FET 再 +30px（净 +60）· RS 重居中（第108轮）
- 用户重复下达同一指令，判定为「在当前基础上再下移 30px」（上一轮已净 +30，本轮后 FET 净 +60：栅条 204-272 中心 238、node-source 276）。
- R_S 重新居中 S(276)—地(525)：中点 400.5，体 374-427，标注 408；fx-rs 同步。
- 栅极输入水平线 208→238：wire-gate-out / wire-in-gate / C1 两板(216-260)与标注(305) / fx-c1 / wire-vi-in / Vᵢ 上端子 / node-gate / wire-rg-top 全部对齐 y=238，输入通路仍为一条直水平线。
- R_G1 再随线下移 30px（体 188.5-241.5，标注 222），复刻「输入线穿体底上方 3.5px」防交叉关系。
- Vᵢ 标注组下移至端口顶(238)与地(525)中点：＋312 / Vᵢ382 / －452（组中心 382）。
- fx-tmodel：G 端子/红点 (502,238)、受控源菱形中心 208、源侧引线接 276、g_m·v_gs 与 i_d 箭头 +15。
- 工具：`tools/patch_cs_g3_move2.py`（49 处原子替换，唯一性校验，一次通过）。
- 验收：svg-layout-check EXIT=0（0 交叉，仅 3 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检符合。
- 回归脚本坐标更新：comp-rg1 点击 (250,185)→(250,215)。
- 版本：data.js lab `7→8`、thumbImg `13→15`（thumb-gen 自动再推）、index `data.js?v=11.66`；缩略图已重截。

## 2026-10-28 22:55 第三轮下移 · FET 再 +30px（净 +90）· RS 重居中（第109轮）
- 用户再次下达同一指令，判定为「在当前基础上再下移 30px」（本轮后 FET 净 +90：栅条 234-302 中心 268、node-source 306）。
- R_S 重新居中 S(306)—地(525)：中点 415.5，体 389-442，标注 423；fx-rs 同步。
- 栅极输入水平线 238→268：wire-gate-out / wire-in-gate / C1 两板(246-290)与标注(335) / fx-c1 / wire-vi-in / Vᵢ 上端子 / node-gate / wire-rg-top 全部对齐 y=268，输入通路仍为一条直水平线。
- R_G1 再随线下移 30px（体 218.5-271.5，标注 252），复刻「输入线穿体底上方 3.5px」防交叉关系。
- Vᵢ 标注组下移至端口顶(268)与地(525)中点：＋327 / Vᵢ397 / －467（组中心 397）。
- fx-tmodel：G 端子/红点 (502,268)、受控源菱形中心 223、源侧引线接 306、g_m·v_gs 与 i_d 箭头 +15。
- 工具：`tools/patch_cs_g3_move3.py`（49 处原子替换，唯一性校验，一次通过）。
- 验收：svg-layout-check EXIT=0（0 交叉，仅 4 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检符合。
- 回归脚本坐标更新：comp-rg1 点击 (250,215)→(250,245)。
- 版本：data.js lab `8→9`、thumbImg `15→17`（thumb-gen 自动再推）、index `data.js?v=11.67`；缩略图已重截。

## 2026-10-28 23:20 第110轮 · 结构性重排（栅极横置 R_G / 漏源 35px 转角 / R_L 居中）
- 用户四项指令：
  1) RG1 上移 50px；RG 换到水平导线上；C1 及左右导线下移到与栅极竖条底端对齐成直角。
  2) D 极加 35px 水平导线；RD 及上下引线右移与水平连接成 90° 转角；C2 接点下移到垂直引线中间。
  3) S 极同加 35px 水平导线；RS 与 CS 右移、上端导线接成 90° 转角；CS 分支点下移 30、CS 下移到垂直导线中间。
  4) 移除 RL 下方节点；RL 下移到垂直导线中间。
- **栅极支路**：R_G1 体 168.5-221.5（标注 202）；分压节点 node-div 移到 (250,302)（即栅极水平线上的四向交汇：上 R_G1、下 R_G2、左右输入导线）；R_G 改横置体 363.5-416.5 × 288.5-315.5（标注移至线上方 390,275）；wire-in-gate `M 220 302 H 363.5`、wire-gate-out `M 416.5 302 H 502`（栅条底端直角接入）；**wire-rg-top / wire-rg-bot 删除**、**node-gate 删除**（STAGE_UNITS/ANNOS/fadeWith 同步清理）。
- **漏极支路**：新增 wire-rd-lead `M 530 226.5 H 565 V 181.5`（35px 水平+垂直，90°转角）、wire-rd-bot `M 565 181.5 V 136.5`；R_D 体右移至 551.5-578.5（标注 535,117）、wire-rd-top `M 565 5 V 83.5`；node-drain 移到 (565,181.5)（C2 分支点）；wire-drain-out `M 565 181.5 H 670`；C2 板 159.5-203.5（标注 144）。
- **源极支路**：wire-rs-top `M 530 306 H 565 V 336`（35px 水平+垂直，90°转角）＋新增 wire-rs-lead `M 565 336 V 389`；R_S 体右移至 551.5-578.5（标注 535,423）；wire-cs-top `M 565 336 H 633 V 422.5`（分支点 (565,336) 加节点圆）；C_S 板 611-655 × 422.5/438.5（标注 675,407/675,463）；wire-cs-bot `M 633 438.5 V 525`；地轨节点随移 565/633；接地符号右移至 565；**wire-gnd-r 删除 (800,525) 节点圆**。
- **负载支路**：R_L 体 327-380（垂直导线 181.5-525 中点 353.25；标注 360）；wire-rl-top `M 800 181.5 V 327`、wire-rl-bot `M 800 380 V 525`；V_o 括注随 R_L 下移 73（268/353/438）。
- **整理态联动**：rarr-rd 下挂点随输出节点 181.5、体 327-380 对齐 R_L；moveCompDown(comp-rd) 增加 fadeGroup('wire-rd-bot')（R_D 下移后该上段引线随本体隐藏，漏极路径=沟道→转角→181.5→C2 不断线）。
- **标注避让**：d 移至 (578,214)、s 移至 (578,322)（避开新引线穿行判定）；Vᵢ 文字组下移至 ＋354/Vᵢ414/－474（组中心 414≈(302+525)/2，且避开端口端子圆）。
- **fx 层**：fx-c2 181.5、fx-cs 633×422.5-438.5、fx-rs 565×389-442；fx-tmodel 重排（G 端子/红点 502,302、D 红点 530,226.5、受控源菱形 241-291 中心 266、gm 标注 (586,244)/文本 276、i_d 箭头随动）。
- 工具：`tools/patch_cs_g3_reflow.py`（79 处原子替换，一次通过）＋标注避让小补丁（d/s/Vᵢ 共 5 处）。
- 验收：svg-layout-check **EXIT=0**（0 交叉、0 标签冲突、端点全连接、③b 导线穿行无；仅 5 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检四项全部到位。
- 回归坐标：comp-rg (390,325)→(390,302)、comp-rg1 (250,245)→(250,195)。
- 版本：data.js lab `9→10`、thumbImg `17→19`（thumb-gen 自动再推）、index `data.js?v=11.68`；缩略图已重截。

## 2026-10-28 23:55 第111轮 · 输入回路重构 + D/S/B 引线重排 + 右移对齐
- 用户四项指令：① C1 左移 25px；C1→G 极直连且与分压竖线交叉不连通（去节点）；R_G 下挂（下引 50px＋90° 转角向左接分压节点，R_G 居水平段中间）。② C_S 分支节点下移到 R_S 上端导线中间；C_S 下移到其竖直导线中间。③ D/S 引线改接沟道上/下段中点并延长到与 B 端右对齐（x=578）；R_D/R_S/C_S 右移 13px；移除漏极/源极节点圆与 C_S 上方 ＋ 号；B 经导线下接 S 极。
- **输入回路**：C1 板 181/195（标注 188）、fx-c1 随动；wire-in-gate `M 195 302 H 502` 直连栅极（横穿 x=250 处恰为 wire-rg1b/wire-rg2a 共享端点→判「连接」不判交叉，节点圆删除即不连通）；**wire-gate-out 删除**；R_G 下挂：新增 `wire-rg-drop` `M 390 302 V 352 H 346.5`（带 (390,302) 节点圆）+ `wire-rg-link` `M 293.5 352 H 250`（解析器不支持多 M 子路径故拆两条），R_G 体 (293.5,338.5) 中心 (320,352)、标注 (320,400)；node-div 圆移到 (250,352)（R_G 接入 T 结点）。
- **漏极支路**：R_D 右移 13（体 564.5，标注 548）；wire-rd-lead `M 530 236.25 H 578 V 181.5`（D 接沟道上段中点 236.25、右行至 x=578 转角上行）；wire-rd-bot `M 578 181.5 V 136.5`；wire-drain-out 起点 578；**node-drain 圆删除**（C2 分支 T 无点）；整理态 fadeWith 仅去 node-drain 引用，wire-rd-lead 保留沟道→输出通路。
- **源极支路**：S 接沟道下段中点 294；wire-rs-top `M 530 294 H 578 V 341.5`；R_S 上端导线中点 (578,341.5)=C_S 分支节点（圆随移）；wire-rs-lead `M 578 341.5 V 389`；R_S 体 564.5；wire-rs-bot 578；C_S 板 624/668 × 425.25/441.25（竖直导线 341.5→525 中点 433.25）、wire-cs-bot 646、fx-cs 随动、**C_S 上方 ＋ 号删除**、标注 688；**node-source 圆删除**。
- **B 接 S**：箭头 polygon 移 y=266（沟道中段中点）、引线 `M 554 266 H 578 V 294` 垂直下接 S 转角（endpoint-on-corner 判连接，无点，同 cs-g5 先例）；B 标注 (592,280) 不动。
- **地轨随动**：wire-gnd-m 至 578、m2 至 646、gnd-r 起 646；节点圆 578/646；接地符号整体 +13（竖线 578）。
- **fx-tmodel 随动**：lead-in `M 530 236.25 V 240 H 554`、菱形 `M 554 240 L 586 265 L 554 290 L 522 265 Z`、lead-out `M 554 290 V 294 H 530`、i_d 箭头 ±1、红点 d(530,236.25)/s(530,294)、G(502,302) 不变。
- **标注避让（③b 教训）**：d/s 初版置于水平引线上/下方 (554,222)/(554,334) 被 ③b「导线从标签与元件之间穿过」判硬错（B 箭头 polygon bbox 与标签 x 重叠、y 带内含 236.25/294 导线）；改放符号右侧 x=592（与全部 comp-t 子件无 x 重叠→规则永不触发）(592,214)/(592,330)。
- 工具：`tools/patch_cs_g3_wiring.py`（57 处原子替换，一次通过）＋ d/s 标注小补丁。备份 `.workbuddy/archive/bak-cs-g3-20261028-2352.html`。
- 验收：svg-layout-check **EXIT=0**（0 交叉、0 标签冲突、③b 无、端点全连接；仅 4 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检四项全部到位；deliver_check PASS（8765 服务重启后）。
- 回归坐标：comp-rg (390,302)→(320,352)；comp-rg1 (250,195) 不变。
- 版本：data.js lab `10→11`、thumbImg `19→20`（thumb-gen 自动再推）、index `data.js?v=11.69`；缩略图已重截。

## 2026-10-29 08:45 第112轮 · FET 上移 20px · 输入线/C1/Vᵢ 随动 · RD/C2 上移 · 补两节点
- 用户指令：场效应管上移20px；G 极导线、C1 同时上移20；Vᵢ 与＋/－号跟随，Vᵢ 的－号再下移15；RD、C2 上移20，C2 左右导线随动对齐；C2 与 D 极连接处加节点；RD 上端加节点。
- **FET 上移 20px**：栅条 214-282、三段沟道 206.5-226/238-254/266-282、衬底 B 箭头 y=246、B 引线 `M 554 246 H 578 V 274`、热区 y=188；g/d/s/B 标注 308/194/310/260；fx-tmodel G(502,282)、D(530,216.25)、S(530,274)、菱形 220-270 中心 245、gm 标注 224/256、i_d 箭头随动；红点三点随动。
- **源极支路**：S 引线 `M 530 274 H 578 V 341.5`（水平段随 FET 上移，分支点 (578,341.5) 及以下 R_S/C_S 不动）。
- **输入线/C1/Vᵢ 上移 20**：wire-in-gate `M 195 282 H 502`、wire-vi-in `M 110 282 H 181`、Vᵢ 上端子 (110,282)、C1 板 260-304（标注 349）、fx-c1 282；Vᵢ 组 ＋334/Vᵢ394/－459（－号先随上移 20 再回下 15，净上移 5）。**wire-rg-drop `M 390 282 V 352 H 346.5`**（R_G 不动，下引 50→70px，data-name 与 ANNOS 文案同步改 70px）。
- **★防交叉拆段**：输入线移到 y=282 后与分压竖线 x=250 中段相交→判「导线交叉」硬错；将 wire-rg1b 在 y=282 拆为上段 `M 250 221.5 V 282`＋新增 **wire-rg1b2** `M 250 282 V 302`，交叉点变两段端点→判「连接不连通」（无节点圆，视觉不变）。wire-rg1b2 已注册 STAGE_UNITS＋ANNOS＋fadeGroup(comp-rg1 收起)。
- **RD/C2 上移 20**：wire-rd-top `M 578 5 V 63.5`＋**新节点 (578,5)**（RD 上端与电源轨 T 交汇）；R_D 体 63.5-116.5（标注 97）；wire-rd-lead `M 530 216.25 H 578 V 161.5`；wire-rd-bot `M 578 161.5 V 116.5`；wire-drain-out `M 578 161.5 H 670`＋**新节点 (578,161.5)**（C2-D 连接处/漏极输出节点）；C2 板 139.5-183.5（标注 124）；wire-c2-out / wire-rl-top 随移 161.5（R_L 体不动）；fx-c2 161.5；rarr-rd 下挂点 161.5。
- 工具：`tools/patch_cs_g3_lift.py`（57 处原子替换，唯一性校验，一次通过）。备份 `.workbuddy/archive/bak-cs-g3-20261029-0845.html`。
- 验收：svg-layout-check **EXIT=0**（0 交叉、0 标签冲突、③b 无、端点全连接；仅 3 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror；回归坐标无需变更）；截图目检（整页＋FET 局部）两处新节点可见、输入直线、－号偏下均符合。
- 版本：data.js lab `11→12`、thumbImg `21→22`（thumb-gen 自动再推）、index `data.js?v=11.70`；缩略图已重截。

## 2026-10-29 22:35 第113轮 · 电阻居中微调 + +VDD 左移 + V_o 记号贴拐角
- 用户指令：① RG1 上移到 C1 右端导线与 VDD 水平导线之间的中间位置；RG2 上移到垂直导线中间位置；RS 文字、电阻与 C_S 电容水平同轴。② +VDD 文字左移 30px，VDD 导线缩短对齐。③ RL 上移到垂直导线中间位置，V_o 的＋/－号移到 RL 两端垂直导线拐角右侧。
- **R_G1**：中心 195→143.5（VDD 轨 y=5 与输入线 y=282 的中点），体 117-170；wire-rg1a `M 250 5 V 117`、wire-rg1b `M 250 170 V 282`（wire-rg1b2 282→302 不变）；标注 y 202→150。
- **R_G2**：中心 460→438.5（分压节点 352→地 525 的中点），体 412-465；wire-rg2a `V 412`、wire-rg2b `M 250 465 V 525`；标注 467→446。
- **R_S 与 C_S 同轴**：R_S 中心 415.5→433.5（对齐 C_S 板 425.25/441.25 中心 433.25），体 407-460；wire-rs-lead `V 407`、wire-rs-bot `M 578 460 V 525`；标注 423→440；fx-rs 短接桥 407-460。C_S 不动。
- **+VDD 左移 30**：端子圆 (860,5)→(830,5)、标注 x 860→830；wire-vdd-ext `M 640 5 H 821`（止于端子外缘 821）；fx-vdd 置零接地符号 4 条线整体 −30。
- **R_L**：中心 353.5→343.25（输出竖线 161.5→525 的中点），体 317-370；wire-rl-top `V 317`、wire-rl-bot `M 800 370 V 525`；标注 360→350；整理态 rarr-rd 同步（体 317-370，与 R_L 对齐）。
- **V_o 记号**：＋ 268→175（右贴上拐角 (800,161.5)）、－ 438→538（右贴下拐角 (800,525)=地线高度）、V_o 353→357（居中 343.25）；comp-vo 热区 y 218-448 扩为 150-565。
- 工具：`tools/patch_cs_g3_lift2.py`（33 处原子替换，唯一性校验，一次通过）。备份 `.workbuddy/archive/bak-cs-g3-20261029-2235.html`。
- 验收：svg-layout-check **EXIT=0**（0 交叉、0 标签冲突、③b 无、端点全连接；仅 1 条提示级导线不均）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检七项全部符合。
- 回归坐标更新：comp-vdd 悬停 (860,5)→(830,5)（端子左移）；comp-rg1 点击 (250,195)→(250,143)（体 117-170 中心 143.5）。
- 版本：data.js lab `12→13`、thumbImg `23→24`（thumb-gen 自动再推）、index `data.js?v=11.74`；缩略图已重截。

## 2026-10-29 23:05 第114轮 · C1 标注移到电容上方
- 用户指令：将 C1 文字放到电容上方。
- comp-c1 标注 y 349→244（电容板 260-304 上方，间距与 C2 同风格），x=188 居中两板不变。
- 验收：svg-layout-check EXIT=0（0 交叉、0 标签冲突、③b 无、端点全连接）；回归四路径全过（0 pageerror）；截图目检标注居中于电容上方、无重叠。
- 版本：data.js lab `13→14`、thumbImg `25→26`、index `data.js?v=11.77`；缩略图已重截。

## 第107轮（2026-11-01）：移除 MOS 管符号旁全部单字母标注
- 删 g/d/s/B 共 4 条 hot-label 及「<!-- 端子标注… -->」注释；衬底引线/箭头（T 结 486,330）不动。
- 验收：布局 EXIT=0；FET 特写目检无字母；cs-g3-flow-test 回归过；缩略图重截（thumbImg ?v=28）。版本 ?v=15。

## 2026-11-02 09:45 第115轮 · V_i －号下移 · 分压支路右移30 · C_S 同轴 · 整体左移30 + R_L/V_o 右移50
- 用户指令：① Vᵢ 的－极下移40px；② R_G1/R_G2/R_G 右移30px，R_G1/R_G2 文字移到电阻右侧；③ C_S 文字与电容水平同轴；④ 整个电路左移30px，然后 R_L、V_o 及其＋/－极性右移50px。
- **① Vᵢ －号** y 459→499（贴近下端子圆 (110,525) 上方，净距 ≈16px）。
- **② 分压支路右移30**（文件坐标）：wire-vdd-rail 起点 250→280、wire-rg1a/rg1b/rg1b2/rg2a/rg2b x 250→280、comp-rg1/rg2 体 x 236.5→266.5、node-div (250,352)→(280,352)、comp-rg 体 293.5→323.5（中心 350）、R_G 标注 320→350、wire-rg-link `M 323.5 352 H 280`、wire-rg-drop `M 390 282 V 352 H 376.5`（右段短接 13.5px）；R_G1/R_G2 标注改右侧 x=309.5 text-anchor=start（y 150/446 不变）。输入导线与分压竖线交叉点随移至 (280,282)，仍为 rg1b/rg1b2 共享端点（连接不连通，无节点圆）。
- **③ C_S 标注** y 463→440（板 425.25/441.25 中心 433.25，与 R_S 标注同基线）。
- **④ 整体左移30**：circuit-wrap `translate(18, 260)`→`translate(-12, 260)`（检查器/回归脚本均动态读取 tx，全电路含 fx 层统一平移）；R_L/V_o 组右移50（文件坐标）：wire-c2-out `H 850`、wire-rl-top/bot x 850、comp-rl 体 836.5、R_L 标注 820、comp-vo 热区 x 880、＋/V_o/－ x 908、wire-gnd-r `H 850`。净效果：除 R_L/V_o（净 +20）外全部 −30。
- 工具：`tools/patch_cs_g3_r115.py`（28 处原子替换，唯一性校验，一次通过）。备份 `.workbuddy/archive/bak-cs-g3-20261102-0945.html`。
- 验收：svg-layout-check **EXIT=0**（0 交叉、0 标签冲突、③b 无、端点全连接、边界安全；仅 2 条提示级导线不均：comp-rg 44:14、comp-rg2 110:60，不判失败）；回归四路径全过（A=100/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检五项全部符合。
- 回归坐标更新：comp-rg (320,352)→(350,352)、comp-rg1 (250,143)→(280,143)。
- 版本：data.js lab `15→16`、thumbImg `28→29`（thumb-gen 自动再推）、index `data.js?v=11.93`；缩略图已重截。

## 2026-11-02 13:45 第116轮 · Vᵢ 居中于＋/－之间 + 第1关新增 Vᵢ 处理步骤（保留/置零）
- 用户指令：① Vᵢ 下移到＋、－号中间位置；② 增加 Vᵢ 的处理步骤，添加置零和保留选项。
- **① Vᵢ 标注** y 394→417（＝(334+499)/2，与 V_o「基线取两记号基线中点」同约定）。
- **② Vᵢ 处理步骤**（镜像 cs-g2 第1关做法）：
  - targets 新增 `{ id:'comp-vi', name:'输入信号源Vi', menu:[保留(vi-keep,对)/置零(vi-zero,错)] }`（排 comp-vdd 之后）。
  - subSteps[0].ids 加入 comp-vi（`['comp-vdd','comp-vi','comp-c1','comp-c2','comp-cs']`，受 gate=['comp-vdd'] 门控：电源处理完才解锁）。
  - execAct 新增 `case 'vi-keep': break;`（交流通路必须保留信号源）/ `case 'vi-zero': break;`（错误项不改电路仅扣分）。
  - **分值重排**：targets 6→7 项，每项池 round(27/7)=4，6×4=24＋TQUIZ 池 2→**3**＝27（startTQuiz 与 ?ts= 预览钩子两处 pool 同步改）；注释口径同步。
  - announce/why 文案补「输入信号源/信号源保留」；?tidy 预览钩子补 `execAct('comp-vi','vi-keep')`。
- **面板计数**：第1关「已处理 X/8 项」→ 动态变 X/9（targets 7＋moveIds 2）。
- 回归脚本：driveFull / driveRestart 两处 L1 直驱均插入 `chooseDrawOption('comp-vi',{act:'vi-keep',ok:true})`。
- 验收：svg-layout-check **EXIT=0**（仅 2 条提示级导线不均）；回归四路径全过（A=100 各关[27,28,45]/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；**新增真实鼠标专项验证**：悬停 Vᵢ 文字弹菜单 [保留,置零]→选置零「错误，扣1分」(池4→3)→再选保留得 3 分（VDD 4＋Vi 3＝7），0 pageerror（VI-MENU-OK）；截图目检 Vᵢ 居中＋/－之间同线对齐。
- 版本：data.js lab `16→17`、thumbImg `30→31`、index `data.js?v=11.94`；缩略图已重截。

## 2026-11-02 14:30 第117轮 · 整理态几何修正（RG1 并联同轴/RD 标签右置/节点修复）
- 用户指令：① RG2 文字下移同轴并保 15px 间距；RG2 下方地线节点错位修复。② 整理时 RG1↔RG2 并联：收起 RG2 上方节点之上导线，RG1 与 RG2 水平同轴、文字右置同轴；RD 下移后文字右置。③ RD 整理后移除 D 极多余节点。
- **① 地线节点错位修复**：第115轮分压支路右移30后节点圆未随动——wire-gnd-l `H 250→H 280`、节点圆 (250,525)→(280,525)、wire-gnd-m `M 250→M 280`。默认态节点圆现正对 R_G2 下引线。
- **① RG2 标签**：默认态 (309.5,446,start) 本就同轴（bbox 实测块中心 437.6 vs 体心 438.5，偏差 <1px），用户所见错位源于 resetCircuit/tidy 两处过期回位（218/427/end 与 290/427/start，均与第113/115轮后的新坐标不符）——**两处重摆逻辑整体废除**，标签固定 (309.5,446,start)（与体右缘净距 16px≈15）。
- **② RG1 整理态（rarr-rg1）**：
  - 体 y 390-450(h=60)→**412-465(h=53)**（与 R_G2 水平同轴；同时回归 27×53 标准）。
  - 顶引线 `M 250 330 H 170 V 390`→`M 280 352 H 170 V 412`（原起点 (250,330) 在第115轮右移后已悬空；改接分压节点 (280,352)）。
  - 下引线 `M 170 450 V 525`→`M 170 465 V 525`；节点圆 (170,525) 不变。
  - 标签 x=146(end)→**x=193.5(start) y=446**（体右侧 10px、与 R_G2 标签同基线；实测 bbox 宽 62.2，右缘 255.7 距 R_G2 体 10.8px；15px 方案会只剩 5.8px 故收 10px）。
  - **收起节点上段导线**：moveCompDown('comp-rg1') 动态改 `wire-rg2a` d `M 280 302 V 412`→`M 280 352 V 412`（节点以上 302-352 段随 R_G1 下挂失去连接意义）；resetCircuit 恢复全长。
- **② RD 整理态标签（rarr-rd）**：x=668(end)→**x=722.5(start) y=350**（体右侧 9px、与体心 343.5 同轴）。原左置 (668,350) 与 C_S 支路 L 形线（y=341.5 横段＋x=646 竖段）相交压线。
- **② R_L 静态标签** end 820→**824**（避让右置后的 RD 标签；实测 RD bbox 722.5→769.3、RL 778.8→824，净隙 9.5px，原 728.5 方案重叠 0.5px）。
- **③ D 极多余节点**：wire-drain-out 节点圆加 `id="node-drain"`（578,161.5）；moveCompDown('comp-rd') 时 opacity=0（RD 下挂后该点只剩漏极引线上行→C_2 右行的 L 形转角，T 交点意义消失）；resetCircuit 复现（通用 `#circuit-wrap g` 循环不覆盖 circle，须显式恢复）。rarr-rd 自带 (700,161.5) 节点（与 wire-c2-out 真 T 交）保留。
- 工具：`tools/patch_cs_g3_r117.py`（14 处）＋`patch_cs_g3_r117b.py`（5 处，标签间距微调）；备份 `bak-cs-g3-20261102-1358.html`。验收截图脚本 `cs-g3-r117-shot.js`（默认/整理/reset 三态＋CHK 断言）。
- 验收：svg-layout-check **EXIT=0**（0 交叉/0 冲突/端点全连接；2 条提示级导线不均不判失败）；回归四路径全过（A=100[27,28,45]/B=99/C1 悬停/C2 真实鼠标命中/D 归零，0 pageerror）；截图目检三态全符。**踩坑**：截图脚本 `&ts=0` 会使 ?ts 钩子 `step=-1` 报 `TQUIZ[-1].dots` TypeError——ts 合法值 1..6（旧 cs-g3-shot.js 未报错只因 pageerror 监听挂晚）。
- 版本：data.js lab `17→18`、thumbImg `32→34`（thumb-gen 自动再推）、index `data.js?v=11.95`；缩略图已重截。

## 2026-11-02 17:00 第118轮 · C_2 居中输出导线 + 信号源/直流电源不分先后
- 用户指令：① C_2 右移到水平导线中间；② 处理信号源与直流电源时不区分先后顺序。
- **① C_2 居中**：输出水平段 578（漏极输出节点）→850（R_L 支路），中点 714——板 670/684→**707/721**（两侧短接线各 129px 对称）、标注 x 677→714、wire-drain-out `H 670→H 707`、wire-c2-out `M 684→M 721`、短接桥 fx-c2 同步 707-721。
  - 连锁：rarr-rd 下挂支路 x 700→**690**（原位置节点圆 r=7 右缘 707 与新桥板/桥体相切；移后圆 683-697 与桥 707 净隙 10px）——体 676.5-703.5、顶/底引线与节点圆 (690,161.5)/(690,525)、标签 722.5→**712.5**（右缘 759.3 与 R_L 标签 778.8 净隙 19.5）。默认态 rarr 层隐藏互不影响。
- **② 门控不分先后**：`gate: ['comp-vdd']` → `['comp-vdd','comp-vi']`（targetAvailable 对 gate 内成员免检，二者均可先处理；电容仍须两者都处理完才解锁）。gateMsg/gateTodo/gateDoneMsg 与 announce 文案补「两者不分先后」；文件头注释口径同步。
  - **补 chooseDrawOption 门控护栏**（与 pickDrawUnit/menuItemsFor 同口径）：直驱 API 原本绕过门控可给电容计分，现未解锁时提示 gateMsg、不计分不扣分。flow-test 直驱顺序 vdd→vi→caps 不受影响。
- 验证：`cs-g3-r118-order-test.js` 两条路径——Vi先(4分)→点C1被拦(仍4分+门控提示)→VDD后C1解锁；VDD先同理。真实鼠标：门控前悬停 C1 无菜单、悬停 Vᵢ 出 [保留,置零] 且保留记 4 分；VDD 处理后悬停 C1 出 [短路,断路]。0 pageerror。
- 验收：svg-layout-check **EXIT=0**；回归四路径全过（A=100[27,28,45]/B=99/C/D，0 pageerror）；截图目检 C2 居中（左右短接线等长）与整理态 RD（节点-桥净隙、标签分离）。
- 版本：data.js lab `18→19`、thumbImg `34→35`（thumb-gen 自动再推）、index `data.js?v=11.96`；缩略图已重截。备份 `bak-cs-g3-20261102-1700.html`。

## 2026-11-02 17:25 第119轮 · RS 移除连带收 C_S 支路 + 等效五问对齐 cs-g1 口径
- 用户指令：① 整理电路点 R_S「移除」后，同时移除原 C_S 的短路线及节点；② 场效应管等效步骤方式参照 cs-g1（分压式案例1）改成一样的效果。
- **① rs-remove 连锁收起**（与 cs-g2 同口径）：`execAct('rs-remove')` 增补 `fadeGroup('wire-cs-top'/'wire-cs-bot')`（含源极分支节点圆 (578,341.5)，随组隐藏）+ `showFx('fx-cs', false)`（绿短接桥）+ `showFx('node-cs-gnd', false)`。新 id `node-cs-gnd`＝地线延伸段 (646,525) 的 C_S 入地节点圆（在 wire-gnd-m2 组内，不能整组隐藏故单独加 id）；resetCircuit 显式恢复（与 node-drain 同款）。整理态源极只余 fx-rs 一条竖线入地。
- **② 等效五问对齐 cs-g1**：TQUIZ 改为 ①G–S 开路 ②v_gs 极性「上＋下－」（reveal fx-t-vgs）③G–D 开路 ④D–S 受控源（reveal fx-t-src）⑤↓i_d（reveal fx-t-id + idlabel fx-t-idlabel）；Q1/Q3/Q4 选项改 ['短路','开路','受控源']（与 cs-g1 一致）。
  - fx-tmodel 新增 `fx-t-vgs` 极性柱（x=502 G 端子正下方：＋322 / v_gs 400 / －478，#ffe66d 28px，R_S 移除后源极接地、－落低电位，语义同 cs-g1 竖柱）。
  - **g_m·v_gs 标注从 fx-t-src 常显移出**：新组 `fx-t-idlabel`（data-id 仍 q-gm 供第2/3关填空作答，坐标不变 590,256），第5问作答后与 fx-t-id 箭头同现；answerTQuiz 增 `if (q.idlabel) showFx(q.idlabel, true)`；?ts 钩子 forEach 增 idlabel 同现。
  - tquizOptHtml 换 cs-g1 版：↑/↓ → 箭头+g_m·v_gs（TQ_SUBM/TQ_SUBGS 行内下标）、上＋下－ → 竖排极性柱选项（44px 宽 inline-flex）。
  - **踩坑：新插入 fx-t-idlabel 漏写 opacity="0" 初始属性**——fx 屄件显隐全靠 markup 属性起步（初始加载不走 resetCircuit），漏写导致 ts=5 预览标注提前常显。已补。
- 回归脚本答案表同步（两处）：`['开路','受控源','↓i_d','电压控制电流源','栅源电压']` → `['开路','上＋下－','开路','受控源','↓i_d']`。
- 验证：直驱断言 rs-remove 后 cst/csb/fxcs/ncg 全 "0"、fxrs "1"、score 24，resetCircuit 全恢复；门控护栏两次拦截验证（漏 vi / 漏 c1c2 时 rs-remove 被拦不计分）；0 pageerror。截图目检：整理态 C_S 支路全消、地线只剩源极/RD 两节点；ts2 极性柱选项条渲染完整；ts5 标注未提前；ts6 全要素齐全无重叠。svg-layout-check EXIT=0；回归四路径全过（A=100[27,28,45]/B=99/C/D 归零）。
- 版本：data.js lab `19→20`、thumbImg `36→38`（thumb-gen 自动再推）、index `data.js?v=11.97`；缩略图已重截。备份 `bak-cs-g3-20261102-1720.html`。工具 `patch_cs_g3_r119.py`、截图 `cs-g3-r119-shot.js`。

## 2026-11-02 18:25 第120轮 · RG 下引线右移对称居中 + 整理态输出线对齐 D 极 + 等效态对齐 cs-g1（输入线上移/S 极入地路径移除）
- 用户指令：① RG 右端垂直导线右移到节点与直角点中间，RG 文字与电阻右移到水平导线中间；② RD 下移后 D 极水平导线下移与 D 极对齐；③ 场效应管等效后的电路变化参照 cs-g1：移除原 S 极到地端导线、G 极水平导线上移与 D 极对齐。
- **① RG 对称居中**：wire-rg-drop 竖线 x 390→**446**（＝输入线节点 390 与栅极条底角 502 的中点；节点圆随动 (446,282)）；R_G 体 323.5-376.5→**336.5-389.5**（居 280-446 中点 363，左右引线各 **56.5px 完全对称**）、标签 x 350→363；wire-rg-link `M 336.5 352 H 280`。
- **② 整理态输出线下移对齐 D 极**（y 161.5→216.25；新函数 `applyTidyOutput(down)`，moveCompDown('comp-rd') 置 true、resetCircuit 置 false）：
  - wire-rd-lead `M 530 216.25 H 578 V 161.5`→`M 530 216.25 H 690`（D 极直行至 RD 下挂点，撤销上行 Z 形拐）；wire-drain-out→`M 690 216.25 H 707`；wire-c2-out/wire-rl-top 随降。
  - C_2 板 194.25-238.25、标注 179；fx-c2 桥 216.25（本体短路隐藏系既有设计，绿桥位置须随线）；V_o ＋175→229.75、V_o 357→384、热区 rect 150/415→204/360（－ 538 不动=下拐角）。
  - **rarr-rd 静态改**（仅整理/等效态可见）：顶引线 `M 690 216.25 V 317`、节点圆 cy 216.25；R_D/R_L 标签 (712.5/824,350) 不变。
  - 顺带修隐性 bug：**setCircuitShift 基准 x=18 与静态 translate(-12,260) 不一致**——重玩 resetCircuit 后整图右移 30px；已统一 -12。
- **③ 等效态对齐 cs-g1**（showEquiv 增补；新函数 `applyEquivInput(up)`，resetCircuit 置 false）：
  - 输入主线（G 极水平导线）上移 282→**216.25** 与 D 极对齐：wire-vi-in/wire-in-gate、V_i 上端子 cy、C_1 板 194.25-238.25＋标注 178（本体短路隐藏、绿桥随动）、wire-rg-drop 竖线上延 `M 446 216.25 V 352 H 389.5`＋节点 cy、分压竖线交叉点分段随移（rg1b `V 216.25` / rg1b2 `M 280 216.25 V 302`，端点落线上=连接、视觉仍「交叉不连通」）、fx-tmodel G 端子与 fx-dot-g cy、fx-t-vgs ＋322→256 / v_gs 400→367（－478 不动=地电位）。
  - **原 S 极到地端导线整体移除**：fadeGroup wire-rs-top/wire-rs-lead/wire-rs-bot＋showFx fx-rs=false；wire-gnd-m 节点圆 (578,525) 加 id **node-rs-gnd** 随收（resetCircuit 复现）。
  - **受控源支路直落地线**（cs-g1 口径「经受控源支路直接落地」）：fx-t-src 底段 `M 554 270 V 274 H 530`→`… H 530 V 525`，落地点 (530,525) 加节点圆（T 交）；fx-dot-s (530,274) 落在竖线上不变。
- 回归坐标：flow-test comp-rg 悬停 (350,352)→(363,352)。
- 验证：svg-layout-check **EXIT=0**；回归四路径全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零，0 pageerror）；MOVED/RESET 全字段断言一致（wrap 恒 -12）；截图目检默认（RG 对称居中）/整理（输出线等高 D 极、节点-绿桥分立）/ts5（标注未提前）/ts6（G 线=D 线、受控源落地、S 路径全消）。
- 版本：data.js lab `20→21`、thumbImg `38→40`（thumb-gen 自动再推）、index `data.js?v=11.98`；缩略图已重截。备份 `bak-cs-g3-20261102-1815.html`。工具 `patch_cs_g3_r120.py`（16 处）。

## 2026-11-02 23:35 第121轮 · 等效态 R_G 竖直化居中 + 栅极线缩短 40px + S 红点落地补节点
- 用户指令：① 等效后 R_G 逆时针转 90° 与 R_G2 垂直同轴、导线节点随动，R_G1/R_G2 整体右移让 R_G 正对两者中间；② G 极水平导线右端缩短 40px、红点随动，另一红点放到地线上与 G 红点垂直同轴；③ 地端添加节点。
- **① R_G 竖直化（applyEquivInput 扩展，仅等效态；resetCircuit(false) 全复原）**：
  - 体 (336.5,338.5,53×27)→**(266.5,257.5,27×53)**（x=280 与 R_G2 同轴；居栅极引线 216.25—分压节点 352 之间，上下引线各 41.25/41.5 对称）；标签 (363,400,middle)→**(309.5,291.5,start)**（本体右侧同轴位）。
  - 上引线 wire-rg-drop `M 446 216.25 V 352 H 389.5`→`M 280 216.25 V 257.5`，接线节点圆 cx 446→**280**（随导线与节点「垂直同轴」移到栅极引线上）；下引线 wire-rg-link `M 336.5 352 H 280`→`M 280 310.5 V 352`。
  - **R_G1/R_G2 整体右移 55px**（170→**225** / 280→**335**，R_G(280) 恰为两者中点）：rarr-rg1 全套（引线/体/节点/标签 248.5）、comp-rg2 体 321.5＋标签 364.5、wire-rg2a→`M 280 352 H 335 V 412`、wire-rg2b→`M 335 465 V 525`；R_G2 入地节点圆 (280,525) 加 id **node-rg2-gnd** 随移 cx=335（wire-gnd-l 组内单独控制）。
- **② 栅极线缩短**：wire-in-gate 等效态 `H 502`→`H 462`；G 端子圆、fx-dot-g、fx-t-vgs 三行（＋/v_gs/－）x 全部 502→**462**。
- **③ S 红点落地＋地节点**：fx-dot-s 等效态 (530,274)→**(462,525)**（公共地线上、与 G 红点垂直同轴）；新增 `fx-gnd-node-s` 组（(462,525) r7 白节点，fx-layer 内、红点层之前——作答中红点盖住节点，完成态红点隐藏后节点标示接地点）；applyEquivInput 控制 opacity。
- **踩坑与修复**：applyEquiv(false) 初版按残留 moved['comp-rg1'] 回 wire-rg2a 整理态值，会在 restart（resetCircuit 先于 initState 清 moved）把全长导线错恢复成 352 起——改为 false 分支一律 `M 280 302 V 412`（resetCircuit 原显式恢复行保留为双保险）。
- 验证：svg-layout-check **EXIT=0**；回归四路径全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零，0 pageerror）；MOVED/RESET 全字段断言一致；截图目检默认/整理态不变、等效态三竖直电阻（225/280/335，中者居上位）、G/S 红点同轴 462、地线四节点（225/335/462/530）。
- 版本：data.js lab `21→22`、thumbImg `40→41`、index `data.js?v=11.99`；缩略图已重截。备份 `bak-cs-g3-20261102-2335.html`。工具 `patch_cs_g3_r121.py`（4 处）＋复位修复 1 处。

## 2026-11-03 20:50 第122轮 · 整理态收轨左段＋RD 上节点 · 等效态栅极/D 极线收紧与受控源随动
- 用户指令：① 整理时先点 RG1 下移（RG1∥RG2 后），移除 R_D 上方节点往左的导线、包括节点；② 等效后 G 极水平线左端缩 20px、红点随动、地线红点同左移 20px、v_gs 标注同步；D 极水平线左端缩 40px、红点随动、受控源位置等同步更新。
- **① 轨左段收起**：R_G1 下挂后 `wire-rg1a` 淡出，电源轨左段（280—578）左端悬空——`moveCompDown('comp-rg1')` 增补：`wire-vdd-rail` d `M 280 5 H 640`→`M 578 5 H 640`；R_D 上端节点圆 (578,5) 加 id `node-rd-top` 并 opacity=0（剩 L 形拐角不需节点）。右段 578—640＋ext 仍接 R_D 与 +V_DD；两电阻全下挂时整轨照旧收起。resetCircuit 恢复全长＋节点（与 wire-rg2a 同款显式恢复）。
- **② 等效态几何**（applyEquivInput up 分支；resetCircuit(false) 全复原）：
  - 栅极线 `M 195 216.25 H 462`→`M 215 216.25 H 442`；**C_1 链整体右移 20px 保持相接**（板 181/195→201/215、标注 188→208、fx-c1 绿桥 181-195→201-215、wire-vi-in 右端 H 181→H 201——只缩线不移 C_1 会在桥右留 20px 断口）。
  - G 端子圆、fx-dot-g、fx-dot-s（地线红点）、fx-gnd-node-s 地节点、fx-t-vgs 三行：x 462→**442**（S 红点仍与 G 红点垂直同轴）。
  - D 极线 `M 530 216.25 H 690`→`M 570 216.25 H 690`（**只改等效态**：tidy 态场效应管仍在，d 段中点 530 必须相连——分支放 applyEquivInput 而非 applyTidyOutput）；fx-dot-d cx 530→570（新增动态，原先 530 恒值）。
  - **受控源模型静态坐标整体 +40**（仅等效态显示）：fx-t-src 三段 `530/554→570/594`、菱形 594±32、落地节点 (530,525)→**(570,525)**、fx-t-id 箭头 554→594。
  - **g_m·v_gs 标注 (590,256)→(590,318) 菱形右下**：随模型 +40 右移会到 630..712、压 R_D 下挂线 x=690——改置下方空区（热区 rect 584,290,82,44；左距落地竖线 20、右距 R_D 体 11.5、上距横连线 12）。q-gm 仍为 L2/L3 填空热区。
  - **接地符号 comp-gnd 等效态右移 32px**（transform translate(32,0)，复位归零）：落地节点 570+ r7 与符号竖杆 578 仅差 1px 相触；移至 610 后与 570 节点/CS 节点(646,若保留)/R_D 落点(690)均 ≥27px。
- **踩坑（测试脚本侧，非页面）**：同一页面 resetCircuit() 后重驱动时 moved 残留使 moveCompDown 早退（真正「重新挑战」走 initState 重建 S 无此问题）——组合断言须每次新开页面。
- 验证：svg-layout-check **EXIT=0**（仅既有提示级 1 条）；四路径回归全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零，0 pageerror）；逐字段断言 RG1-only（轨 578 起＋节点隐藏）/等效（442/570/标注/符号）/复位全复原；截图目检 rg1only 顶轨、ts1（桥-线无缝、双红点同轴）、ts6（模型区、标注避让、符号间隙）。
- 版本：data.js lab `22→23`、thumbImg `42→44`（thumb-gen 自动再推）、index `data.js?v=12.00`；缩略图已重截。备份 `bak-cs-g3-20261103-2030.html`。工具 `patch_cs_g3_r122.py`（19 处）、截图 `cs-g3-r122-shot.js`。

## 2026-11-03 22:10 第123轮 · 等效态接地符号居中＋节点 · v_gs －号贴地线 · S 红点与 D 红点同轴 · 受控源竖直支路重构
- 用户指令：① 等效后地端移到下方水平地线中间点并加节点；② v_gs 的 － 号下移靠近地线；③ D、S 等效时地线红点与 D 极导线端红点垂直同轴；④ 受控源菱形上顶点与 D 极导线端点对齐、菱形下移到垂直导线中间位置、菱形内加水平线连接左右顶点。
- **① 接地符号居中＋节点**：地线全长 110—850，中点 **480**——comp-gnd 等效态 transform `translate(32,0)`→`translate(-98,0)`（578→480）；新增 `fx-gnd-node` 组（(480,525) r7 白节点，由 applyEquivInput 控显隐，resetCircuit 隐藏清单补入）。原 `fx-gnd-node-s` 废除（其「S 红点下节点」职责由 fx-t-src 落地节点 (570,525) 承担）。
- **② v_gs － 号**：等效态 y 478→**505**（applyEquivInput 新增 ts[2] 分支，复位回 478）——极性柱 256/367/505，－ 距地线 525 约 20px。
- **③ S 红点同轴 D 红点**：fx-dot-s 等效态 (442,525)→**(570,525)**（与 fx-dot-d 570 同轴、正对受控源支路落地点）；复位回 (530,274)。
- **④ 受控源竖直支路重构（fx-t-src）**：
  - 顶段 `M 570 216.25 V 220 H 594`→`M 570 216.25 V 346`（上顶点与 D 极线端点 (570,216.25) 同轴直下）；
  - 菱形 `594±32@245`→**(570,371)**：`M 570 346 L 602 371 L 570 396 L 538 371 Z`（垂直导线 216.25—525 中点 370.6≈371；64×50 尺寸不变）；
  - **新增内部横线** `M 538 371 H 602`（连接左右顶点）；
  - 底段 `M 594 270 V 274 H 570 V 525`→`M 570 396 V 525`；
  - i_d 箭头随菱形：line 594 (225-248)→**570 (352-374)**、polygon 594,263…→`570,389 561,374 579,374`（菱形内、穿横线）；
  - g_m·v_gs 标注 (590,318) 不动——菱形下移后仍在其右上空区（x 584-666 距 R_D 体 676.5 净隙 10px），q-gm 填空热区随之不变。
- 验证：svg-layout-check **EXIT=0**（仅既有提示级 1 条）；数值断言 EQUIV/RESET 全字段正确、0 pageerror；回归四路径全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零）；截图目检 ts4（双红点同轴 570、地线节点 480/570/690）与 ts6（菱形居中带横线、箭头、接地符号+节点、g_m·v_gs 无重叠）。
- 版本：data.js lab `23→24`、thumbImg `44→46`（thumb-gen 自动再推）、index `data.js?v=12.01`；缩略图已重截。备份 `bak-cs-g3-20261103-2210.html`。工具 `patch_cs_g3_r123.py`（9 处）。

## 2026-11-03 22:40 第124轮 · S 红点回归 G 极同轴 · i_d 箭头上移导线中段 · 第2关受控源右侧 g_m 标注
- 用户指令：① GS 之间等效时地线红点与 G 极红点错位，将地线红点左移与 G 极红点垂直同轴；② g_m·v_gs 与箭头位置不合适——箭头上移到受控源上端导线中间位置、g_m·v_gs 文字与箭头水平同轴；③ 第2关在受控源右侧添加 g_m，与受控源距离 15px。
- **① S 红点回归 G 极同轴**：fx-dot-s 等效态 (570,525)→**(442,525)**（applyEquivInput up 分支；第123轮曾按「与 D 红点同轴」移 570，用户裁决改回与 G 红点 (442,216.25) 同轴，G—S 两点对齐更符合「G、S 之间」问答语义）。地线上三标记分离清晰：红点 442 / 接地符号＋节点 480 / 受控源落地节点 570。复位仍回 (530,274)。
- **② i_d 箭头与 g_m·v_gs 上移同轴**（第5问揭示）：
  - fx-t-id：line `570 (352-374)`→**`570 (263-285)`**、polygon `570,389 561,374 579,374`→**`570,300 561,285 579,285`**——整体（长 37）中心 y≈281.5 = 受控源上端导线 216.25—346 的中点 281.1（第124轮箭头叠画在导线上，菱形内只余横连线）；
  - fx-t-idlabel：text (590,318)→**(590,291)**（28px 字视觉中线 ≈281 = 箭头中心；起点 x=590 距箭头杆 20、右缘约 666 距 R_D 下挂线 690 净 24）；热区 rect y 290→**257**（h 48，257-305 覆盖新位置）。
- **③ 第2关受控源右侧 g_m 标注（新增 fx-gm-tag）**：
  - 位于 fx-tmodel 内、fx-t-idlabel 之后：text (617,381,start)（左缘 617 = 菱形右顶点 602 + 15px，基线 381 与菱形中心 371 同轴）、热区 rect (611,349,62,44)；
  - 带 `class="interactive" data-id="q-gm"`：第2关点它可直接作答（与 fx-t-idlabel 同 id 双热区，blinkGroup 取 DOM 前者闪烁 fx-t-idlabel——g_m·v_gs 处反馈）；
  - **显隐由 render() 控制**：`showFx('fx-gm-tag', S.level === 2 && !S.finished)`（第1/3关隐藏；render 幂等重设，与 resetCircuit 清单兼容）；resetCircuit 隐藏清单补入 fx-gm-tag。
- 验证：svg-layout-check **EXIT=0**（仅既有提示级 1 条：comp-rg2 两端导线 1.83）；回归四路径全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零，0 pageerror）；新脚本 `cs-g3-r124-check.js` 断言 9/9：dotG/dotS 同轴 442、S 红 y=525、箭头 263/285/300、标注基线 291、gm-tag 第1关隐/第2关显(617,381)/第3关隐；放大截图目检 gnd-zoom（地线三标记分离、－ 与红点不重叠）与 src-zoom（箭头-文字同轴、g_m 距菱形 15px、不压 R_D 线）。
- 版本：data.js lab `24→25`、index `data.js?v=12.02`（首屏默认态无变化，thumbImg 保持 46）。备份 `bak-cs-g3-20261103-2240.html`。工具 `patch_cs_g3_r124.py`（6 处）。

## 2026-11-03 23:00 第125轮 · 等效态 R_D/R_L 与受控源水平同轴 · i_d 箭头长度翻倍
- 用户指令：① 点击场效应管等效后的电路，将 R_D 和 R_L 与受控源水平同轴；② g_m·v_gs 的箭头变成现在的 2 倍长度。
- **① R_D/R_L 同轴受控源**（applyEquivInput up 分支新增段；等效必经整理态——targetAvailable 按 subSteps 顺序解锁，step3 仅 comp-t）：
  - 下移 27.5px 使电阻体中心 371 = 受控源菱形中心：rarr-rd 与 comp-rl 体 y 317→**344.5**（下沿 397.5）；上下引线各 **128.25/127.5** 均衡（R_D：`M 690 216.25 V 344.5` / `M 690 397.5 V 525`；R_L：`M 850 216.25 V 344.5` / `M 850 397.5 V 525`）；标签基线 350→**377.5**（两标签仍同轴，且与 V_o 列不相扰）；
  - 复位（false 分支，仅 resetCircuit 调用）全部回默认值：体 317、R_D 引线 216.25→317/370→525、R_L 上引线 **161.5**→317（与 applyTidyOutput(false) 的默认态值一致，无双写冲突）、下引线 370→525。节点 (690,216.25)/(690,525) 不动。
- **② i_d 箭头 2 倍长度**（fx-t-id）：箭杆 22→**44**（line y 244.5—288.5）、三角 15→**30**（polygon `570,318.5 561,288.5 579,288.5`），总长 37→**74**；三角宽保持 18（±9）不变。中心仍 **281.5**：上端距 D 极线 216.25 净 28、尖端距菱形上顶点 346 净 27.5，与 g_m·v_gs（基线 291）保持水平同轴。
- 验证：svg-layout-check **EXIT=0**（仅既有提示级 1 条）；新脚本 `cs-g3-r125-check.js` 断言 9/9（体 344.5、中心 371=菱形中心、标签 377.5、四条引线 d 值、箭头 244.5/288.5/318.5、复位全复原）；四路径回归全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零，0 pageerror）＋ r118 顺序门控测试通过；整页与放大截图目检：菱形/R_D/R_L 一排水平对齐、长箭头与标注同轴、标签无压线。
- 版本：data.js lab `25→26`、index `data.js?v=12.03`（首屏默认态无变化，thumbImg 保持 46）。备份 `bak-cs-g3-20261103-2300.html`。工具 `patch_cs_g3_r125.py`（2 处）。

## 2026-11-03 23:10 第126轮 · 等效态整图上移 30px
- 用户指令：点击场效应管等效后，将电路上移 30px。
- **实现**（setCircuitShift 复用＋showEquiv 恢复调用）：
  - setCircuitShift up 分支 220→**230**（translate(-12,230)，即等效态整图上移 30px；down 分支 260 不变）——up 分支自第120轮起为死代码，本轮恢复语义；
  - showEquiv() 在 fadeGroup/showFx 之后、applyEquivInput 之前调用 `setCircuitShift(true)`（第120轮曾取消等效态整图上移，本轮按用户要求恢复）；
  - resetCircuit 首行 setCircuitShift(false) 归位 260（既有逻辑，无需改动）。
  - 整图 transform 只影响 circuit-wrap（电路＋fx 层＋整理层），右面板 game-ui 在 wrap 外不动；等效五问红点/标注/受控源全部随组移动。
- 验证：svg-layout-check **EXIT=0**（仅既有提示级 1 条）；`cs-g3-r126-check.js` 断言：等效态 computed transform `matrix(1,0,0,1,-12,230)`、复位 `(-12,260)`、0 pageerror；四路径回归全过（A=100[27,28,45]/B=99/C 真实鼠标/D 归零——mkPt/mkPt2 经 wrapOff 读 computed transform 自动补偿位移，无需改坐标）；整页截图目检：顶轨屏幕 y≈235，与题面净距充足、底部留白增大，无裁切无压题面。
- 版本：data.js lab `26→27`、index `data.js?v=12.04`（首屏默认态无变化，thumbImg 保持 46）。备份 `bak-cs-g3-20261103-2310.html`。工具 `patch_cs_g3_r126.py`（2 处）。

## ★ 第116轮（2026-11-09）：结算页得分项改左对齐
- renderDone 得分项由居中改为左对齐：新增 doneLeftX(arr)（量最长行宽→整块在面板内居中→各行 anchor:start 左缘统一），
  行距与行序不变。回归 align_done_test 断言 PASS（各行左缘一致、右缘不溢出、0 pageerror）；deliver_check 双通道 ok。
- 版本：lab ?v= 递增（data.js 同步）、index data.js?v=12.39；缩略图不动（结算页非首屏）。
