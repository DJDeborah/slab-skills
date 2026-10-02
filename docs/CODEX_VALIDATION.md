# 在 Codex 中验证 skill 是否好用

按“能安装 → 能运行 → 数值可信 → 对真实研究有帮助”逐层验证。前一层通过不替代后一层。每次记录版本、输入、命令、输出和失败信息。

## A. 格式与安装

```powershell
python -m pip install -r requirements-dev.txt
python tools/validate_catalog.py --out local-runs/catalog-check.json
python tools/install.py --dest ../slab-validation-install
python -m unittest discover -s tests -v
python tools/run_demo.py --out local-runs/research-demo
```

检查所有目录和引用完整；安装目录应保留所有资源。新建 Codex 任务，先调用一个 skill，请 Codex 说明读取了哪些资源、输入缺什么、输出写到哪里。

## B. 新工具的行为验证

```text
使用 $beam-parameter-interface。打开界面，将厚度 1 mm 改成 2 mm，
保持其他输入不变，记录反力与截图。设置非法长度 0，验证错误提示。
恢复默认，复制 JSON 并生成 FEM 输入；检查 ROOT/TIP 的实际注册节点。
```

通过标准：h 翻倍反力绝对值变为八倍；非法值不能产生有效运行配置；导出 JSON 的参数与当前显示相符；ROOT/TIP 精确命中预期节点。浏览器下载、复制和导入需分别记录是否实测。

```text
使用 $abaqus-parametric-workflow。用自带两案扫描准备与预览，
在有效 Abaqus 环境执行；检查每个 case 的完成证据、能量和解析误差。
然后 resume，确认启动数为 0、跳过数为 2。
复制输出到临时目录后修改一个被冻结文件，确认恢复被拒绝。
```

不要改原始发布证据；故障验证在副本做。数值标准取自注册配置，不用“作业 exit code=0”代替求解和物理检查。

## C. 意义、Gap 与写作的真实任务评测

为待评课题准备公开论文列表或授权材料，以及你已知的最强反例。不要将私有材料推到仓库。

```text
使用 $research-significance：给出 3 个可能的贡献，每项列出会改变的科学或
设计决策、证据、竞争解释与一项最便宜的判别测试；缺证据时明确标注。
使用 $research-gap：保存查询词、日期、来源和筛选条件；用原始论文做能力矩阵，
主动检索能推翻 gap 的反例，输出范围受限且可证伪的 gap。
使用 $research-writing：根据现有证据改写 introduction 和结果段，
输出 claim→evidence 映射；不增加未做的实验，不删掉关键 Main/SI 证据。
```

人工检查：来源是否真实且支持主张；是否找到你给定的反例；是否区分未检索/未报告/已排除；关键单位和边界是否保留；结论有没有超出证据。与不启用 skill 的同一任务比较，固定材料和模型版本，由不知道分组的同事评价。

## D. 接受与改进

每项评测保存任务输入摘要、版本、原始输出、审阅意见和通过/失败条件。失败时修改最具体的指令、工具或判据，再用新的材料复测。科学工作流效果目前尚未有统一盲评结果；可通过 Issue/PR 提交匿名可重现案例来改进。
