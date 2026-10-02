# 本次验证报告

测试日期 2026-10-02。便携工具 Windows/Python 3.12.14；求解器 Abaqus/Explicit 3DEXPERIENCE R2019x，ODB reader Python 2.7.3。区分结构、程序行为、求解器测量与科研判断。

## 安装与自动检查

- catalog 与 13 个 SKILL.md/UI 元数据及资源链接校验通过。
- 53 项 unittest 通过：旧研究/FEM/安装检查 38 项，新增参数化 15 项；包含冻结参数/工具/输入/证据被修改、失败重试、数量上限和求解器返回 0 但无 history 的负对照。
- 完整目录安装与拒绝覆盖逻辑有测试；四项研究端到端合成演示可运行。
- GitHub CI 配置 Windows/Ubuntu × Python 3.10/3.12；在线结果以 [Actions](https://github.com/DJDeborah/slab-skills/actions) 为准，不包含需要许可证的 Abaqus。

指令型 skill 的结构通过不等于已做真实研究效果盲评。各项范围见 [catalog](../catalog.json)。

## 新参数化工具：实际求解

弹性 B21 悬臂梁，L=100 mm、h=1 mm、10 单元、E=210000 N/mm²、U2=-0.1 mm、加载时长 0.25 s，double=both，无 mass scaling。

| 宽度 b/mm | 最终 RF2/N | 解析 RF2/N | 相对误差 | 窗口最大 KE/IE | 结果 |
|---|---:|---:|---:|---:|---|
| 8 | -0.04202165455 | -0.042 | 0.05156% | 0.08011% | completed / audit pass |
| 10 | -0.05252707005 | -0.0525 | 0.05156% | 0.08011% | completed / audit pass |

最终 U2 均为 -0.10000000149011612 mm。审计窗口 t/T∈[0.5,1]，IE 屏蔽阈值为 peak IE 的 1%；完整 meaningful-history KE/IE 最大约 0.603%，ALLAE=0。窗口门限 5%，反力门限 3%。宽度增加的反力趋势与线性参考一致，但两点扫描不能证明所有参数范围有效。

真实 --resume 结果：`solver_launched=false, launched=0, skipped_completed=2, completed=2, total=2`。已完成 case 的历史、质量结果、STA 和 ODB 哈希在本机重新核对。公开 [输入与测量导出](../validation/parametric-workflow/) 包含通用 JSON/INP/history/quality/status；原始 ODB 与完整控制台不公开。

## Beam 界面：真实浏览器

- 真实浏览器打开、调整厚度 1→2，解析反力 -0.0525→-0.42 N；截图保存在 docs/assets。
- 点击复制 beam JSON，状态报告复制成功；读取实际显示配置，保存后进入 prepare_explicit，ROOT/TIP 注册与生成 INP 成功，见 [UI observation](../validation/ui-observation.json)。
- 下载按钮点击后产生成功提示，但浏览器工具未稳定返回下载文件；因此未标记自动下载文件捕获通过。复制路径可用。导入路径代码含注册检查，独立浏览器文件导入尚未验证。

## 已继承的 FEM 证据

旧四项包有三个真实 beam 单元/加载时长敏感性案例以及被拒绝的单精度案例；报告见 [RESEARCH_V0_VALIDATION](RESEARCH_V0_VALIDATION.md)，原始导出在 validation/research-v0.1.0。它们属于先前测量，不作为本次 13 项新增实测数量。

## 科学边界

当前 adapter 的实测只支持弹性直线 B21 梁数值 smoke。解析 fold/pitchfork 是已知标量分支 oracle，未验证一般 FEM continuation。没有完成真实超材料 buckling、接触、材料非线性、机器人控制任务，也没有研究意义/gap/写作的盲评。按 [Codex 验证指南](CODEX_VALIDATION.md) 对自己的课题追加基准、反例、收敛与人工审阅。
