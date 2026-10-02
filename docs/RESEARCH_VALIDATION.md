# Codex 使用验证指南

脚本能检查明确的数据关系，但无法单独证明一个 Skill 让 Codex 的科学判断变好。验证分为安装发现、资源运行、任务行为与真实研究迁移四层。

## 1. 验证安装和资源

按 INSTALL 安装完整目录，新开 Codex 任务，输入 `$skill-name`。记录看到的 Skill 名称与实际加载路径。让 Codex列出准备使用的脚本和参考文件，核对它读取了对应 SKILL.md；如果未触发，先处理发现路径，不评价后续答案。

先跑 `python -m unittest discover -s tests -v` 和 `python tools/run_demo.py --out local-runs/demo`。应看到测试通过与输出 JSON，不应出现凭空补出的文献或实际试件结果。审计 JSON 的 `scope` 应说明它检查到哪一层。

## 2. 四种行为测试

在独立任务中使用下列输入，保持同一模型设置、同一材料与同一时间预算。仓库里的测试夹具用于格式检查；行为测试需要阅读与判断。

| Skill | 给 Codex 的测试情境 | 应出现的行为 | 不应出现的结论 |
|---|---|---|---|
| significance | 两个构型曲线不同，但加载速度也不同；现有数据全被用来拟合 | 给出惯性竞争解释与控制实验；标明 calibration | 已证明新机制、已盲预测 |
| gap | 一个检索词找不到文章，但近邻术语下有文章研究同一能力 | 改用同义词和反例检索，打开原文，缩小 gap | first-ever、没人研究过 |
| writing | 新稿更短，删掉核心控制图与失败样本 | 先做保存清单，恢复证据链，清楚解释失败边界 | 只改漂亮英文、隐去失败 |
| FEM | RF 有下降，某个 Hessian 特征值为零，但没有 FEM 平衡分支和模态 | 分开 observable、局部稳定性、分支与落点；列缺失证据 | 已验证 FE bifurcation 或必然 snap |

可复制的 significance 测试请求：

```text
$research-significance
我有两个边界条件下不同的 force-displacement 曲线，但加载时长也不同，
并且所有样本都参与了拟合。请形成意义陈述、竞争机制、反例标准和下一步最小测试。
没有给出数值数据，请不要编造已经通过的数值结论。
```

可复制的 FEM 测试请求：

```text
$fem-explicit-bifurcation
给定 force drop 与解析模型的零特征值，能否写成 FEM 分岔已验证？
请按证据层级回答，再生成包内直梁算例的 INP 与 registration；先不提交求解。
检查边界选择和工作目录，列出迁移到接触超材料还需实现的 adapter。
```

## 3. 检查明确的失败输入

在项目副本中进行，保留原始文件：

1. significance：把同一个 case ID 同时放入 calibration_cases 与 holdout_cases，运行审计。应拒绝泄漏。
2. gap：把 claim_type 改为 universal，或者给 nearest_studies 一个日志里没有的 study_id。应拒绝；unknown 不应变成 absent。
3. writing：从审计稿删去 `[figure:F1]`，保留 required_assets 中的 F1；或者修改已有证据文件。应分别报核心图遗漏或 hash 不符。
4. FEM：把 ROOT bbox 移到另一个节点。选择数即使仍为 1，也应被本算例物理约束检查拦下。把能量 history 的 ALLKE 放大，应报惯性超限。

这些测试已经包含在本地自动化套件中。Abaqus 的旧启动器还可能在 Python 提取失败时返回 0，所以必须检查 `history.json` 是否实际生成。

## 4. 做无 Skill／有 Skill 的配对比较

选三个没有参与写 Skill 的任务：一个新研究想法、一组新文献、一段存在证据问题的论文文本；再选一个不同的真实 FEM 项目检查适配质量。分别开无 Skill 和有 Skill 的独立 Codex 任务，用完全相同的输入，记录模型、推理档位、用时、工具成本和输出路径。

每个任务检查：

- 科学判断：是否识别关键竞争解释和缺失证据？是否把结论限定在证据范围？
- 文献质量：引用能否打开，定位是否支持该能力判断，是否找到最近的反例？
- 实用输出：是否产生可填写或可运行的实际材料，脚本是否真正执行并留下结果？
- 保存能力：关键图、失败案例、变量定义与代码入口是否保住？
- 效率：得到同等可信结果需要多少时间与人工修复？

最好由不知道版本的领域同事评价。先写判定标准，再看答案；别用答案长度或关键词出现次数替代科学质量。记录较差结果和人工修改，不只选最好看的一个。只有完成这样的比较，才能声称 Skill 改善了 agent 的判断或写作质量。本次交付没有声称完成独立模型 A/B 评估。

## 5. 验证真实 FEM 迁移

先用 `tools/run_abaqus_smoke.py --sensitivity` 确認直梁执行与后处理。再为实际模型替换 geometry/material/contact/regions/imperfection/load control，并检查选择的节点、面、方向和 DOF。比较适合研究问题的反力、位移、能量、事件顺序和路径，而不只看最终图片。

Explicit：检查稳定段与跳跃段各自的能量、时间分辨率、加载速度、质量缩放和阻尼敏感性。静态分岔：核实实际平衡残差、接触可行性、受约束切线模态、分支延拓与必要的高阶分析。动态落点还需要实际时间演化；Riks 轨迹不能代替它。

自动通过的直梁 smoke 与解析 normal form 不能推出真实接触结构已通过 buckling／post-buckling／snap 验证。
