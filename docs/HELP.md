# 帮助与常见问题

[English step-by-step guide — Chapter 13](chapter13.html) · [可复制 Markdown](CHAPTER_13_SLAB_SKILLS.md)

| 我想做什么 | 去哪里 |
|---|---|
| 下载、安装、升级或回退 | [INSTALL](INSTALL.md) |
| 上传自己的 skill / 修改别人 skill | [CONTRIBUTING](../CONTRIBUTING.md) |
| 看标准目录和新建模板 | [FORMAT](FORMAT.md) |
| 开 Abaqus 参数扫描或调整 beam | [PARAMETRIC_TUTORIAL](PARAMETRIC_TUTORIAL.md) |
| 用 Codex 验证可用性 | [CODEX_VALIDATION](CODEX_VALIDATION.md) |
| 看本次真实测试范围 | [VALIDATION](VALIDATION.md) |
| 管理协作者、发布、Pages | [MAINTAINERS](MAINTAINERS.md) |
| 查看来源与可复用经验 | [DESIGN_AND_SOURCES](DESIGN_AND_SOURCES.md) |

**为什么还是文字？** Skill 的调度入口是带 YAML 的 SKILL.md；文字负责判断与工作流。工具型 skill 的 scripts/assets 提供真正的程序和 UI。指令型研究 skill 可能主要是文字，仍需明确输入、输出和人工评测。

**别人能直接改吗？** 任何人可 Fork 后提交 PR；直接改主仓库需要被邀请为协作者。Fork 修改不影响原仓库，合并 PR 后原仓库才变化。

**Codex 没发现 skill？** 核对安装器打印的目标路径，确认目录有 SKILL.md 和资源；尝试新任务。按当前安装版本选择 ~/.agents/skills 或内置 skill-installer 使用的 CODEX_HOME/skills；避免同名副本。可要求 Codex 列出实际读取路径。

**安装报 Refusing to overwrite？** 备份旧目录到搜索路径之外，在临时目录验证新版本后重新安装。不要仅覆盖 SKILL.md。

**ModuleNotFoundError: yaml？** 用同一个 Python 运行 `python -m pip install -r requirements-dev.txt`；普通运行脚本多使用标准库，但 catalog 检查器需要 PyYAML。

**路径里有空格？** 给路径加双引号；命令在仓库根目录运行。Windows Abaqus 用实际 abaqus.bat；PATH 没配置时不能只写 abaqus。

**页面打不开？** 本地 HTML 可双击；目录页需要 HTTP 服务以读取 catalog：`python -m http.server 8765`，再打开 http://localhost:8765。公开 Pages 刚提交时需等部署完成。

**界面不能下载？** 点复制 JSON；如果浏览器拒绝复制，展开配置、选择文本并 Ctrl+C，保存 UTF-8 的 .json 文件。不要把解析预览当成求解器测量。

**参数扫描没有启动求解器？** 默认预览，实际执行必须 --execute；检查 --max-jobs 和有效 Abaqus 环境。许可证不可用时保存失败日志，恢复前修好环境。

**Frozen hash changed？** 计划、输入或工具被修改。保留原证据，重新 prepare 到新目录。不要手改 manifest 来绕过一致性检查。

**Failed / interrupted case 不重试？** --resume 会核对状态，重试失败还需 --retry-failed。各 attempt 保留，不能把早期失败覆盖掉。

**能直接用于我的 buckling/超材料/机器人模型吗？** 研究与验证工作流可迁移；具体材料、几何、接触和边界需要模型 adapter。当前可执行 Abaqus 例子是弹性 B21 梁；稳定性证明另需适合课题的平衡路径/扰动/特征值证据。

**提出问题：** [Issues](https://github.com/DJDeborah/slab-skills/issues)，按模板给出最小例子和版本。仓库目前没有保证的响应时间。
