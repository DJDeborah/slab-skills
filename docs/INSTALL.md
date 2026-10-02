# 下载、安装与更新

## 路线 A：下载 ZIP，无需 Git

1. 打开 [Releases](https://github.com/DJDeborah/slab-skills/releases/latest)，下载 `slab-skills-v0.1.0.zip`。
2. 解压到你可读写的目录。确认里面有 `skills`、`tools` 和 `README.md`。
3. 在该目录打开终端。`python --version` 应为 3.10 或更新版本。
4. 选装两个工具型 skill：

```powershell
python tools/install.py --user --skill beam-parameter-interface --skill abaqus-parametric-workflow
```

5. 新建/重新打开 Codex 任务，使用 `$beam-parameter-interface`。安装器输出实际目标位置。已有任务的 skills 列表可能需要重新加载。

## 路线 B：Git 克隆

```powershell
git clone https://github.com/DJDeborah/slab-skills.git
cd slab-skills
python tools/install.py --user
```

`--user` 把整个目录复制到 `~/.agents/skills`；`--project` 放到指定项目 `.agents/skills`：

```powershell
python tools/install.py --project "D:\my-research" --skill research-gap
```

macOS/Linux 同样运行这些 Python 命令，项目路径改成 `/path/to/project`。只打开 HTML 界面不需要 Python。

## 路线 C：Codex 内置 skill-installer

在 Codex 中输入：

```text
使用 $skill-installer 从 https://github.com/DJDeborah/slab-skills 安装
skills/beam-parameter-interface 和 skills/abaqus-parametric-workflow，
保留每个 skill 的 scripts、references、assets 和 agents 目录。
```

系统 skill-installer 的目标通常是 `$CODEX_HOME/skills`。它与本仓库用户安装器的 `~/.agents/skills` 是不同路径；选其中一条路线，避免同名副本冲突。如果你的 Desktop 版本只识别 CODEX_HOME，可查看实际环境再指定：

```powershell
python tools/install.py --dest "$env:CODEX_HOME\skills" --skill beam-parameter-interface
```

该示例要求 CODEX_HOME 已设置；不要使用示例替换你的真实设置。可在 Codex 中要求列出已识别的 skill 并核对目录。官方位置规则见 [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills)。

## 完整目录为何重要

`SKILL.md` 是入口，`agents/openai.yaml` 提供显示名和默认调用，`scripts` 是程序，`references` 是按需加载知识，`assets` 放示例配置/UI。只复制 SKILL.md 会破坏相对引用。安装器复制所有资源且拒绝覆盖已有目录。

## 更新与版本固定

1. 克隆用户先 `git status`，有修改时先提交到自己的分支；再 `git pull --ff-only`。ZIP 用户下载新版本并解压到新目录。
2. 阅读 Release 的变更和验证结果。需要复现论文结果时固定 tag：`git checkout v0.1.0`。
3. 先把新版本安装到临时目录：`python tools/install.py --dest ../slab-skills-test`。
4. 在 Codex 中验证新版本。退出占用目录的程序，把旧安装目录**移动到 skills 搜索路径之外**备份，然后安装新版本。
5. 不要把个人案例结果存进安装目录；放在项目输出目录。

重名报错说明已经存在该 skill，不是安装中途覆盖失败。安装器不做静默升级。回退时恢复备份，并重新加载 Codex。

## 可选：作为本地插件合集

仓库带 portable plugin.json 与 .codex-plugin 兼容清单。已实测的主路线仍是上述 skill 安装；下面市场路线依据 [当前官方插件格式](https://developers.openai.com/plugins/build/plugins)，本次没有操作你的现有市场配置。

把完整合集放入自己的项目 `plugins/slab-skills`。将 [marketplace.example.json](../templates/marketplace.example.json) 条目合并到项目 `.agents/plugins/marketplace.json`，保留其他已有条目；source.path 指向 `./plugins/slab-skills`。重新启动/刷新 Desktop，在本地插件来源检查发现并安装，再于新任务调用 skill。若你的版本不支持该来源，使用完整目录安装路线。
