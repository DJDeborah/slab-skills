# Skill 结构与模板

Codex skill 的入口本来就是结构化 Markdown。区别在于是否具有可识别的元数据、完整资源、明确操作和可执行验证。本合集使用标准 skill 目录，不要求仅为增加文件而加入无用程序。

```text
skills/my-skill-name/
├── SKILL.md              # 必需：YAML frontmatter + 工作流
├── agents/openai.yaml    # Codex 显示名、简短描述、默认调用
├── scripts/              # 按需：可执行工具与失败处理
├── references/           # 按需：方法、边界、判据、论文来源
└── assets/               # 按需：输入 JSON、UI、模板、小案例
```

`SKILL.md` 必须从以下格式开始：

```yaml
---
name: my-skill-name
description: Describe the task and when Codex should use this skill.
---
```

主体建议写输入、前置条件、最小操作、输出、验证方法、停止/失败条件和适用边界。通过相对链接按需读取资源，避免把全部参考文献塞进入口。`agents/openai.yaml` 的 default_prompt 包含 `$my-skill-name`；short_description 25–64 字符。模板见 [skill-template](../templates/skill-template)。

catalog 每个条目需要 `name/category/summary_zh/license/runtime/verification/source`。category 可用 research、writing、mechanics、simulation、interface、handoff，其他值也会展示；UI 不把分类当科学质量等级。

根 `plugin.json` 是 portable Agent Plugins 清单，另附 `.codex-plugin/plugin.json` 兼容清单。标准目录安装已实测；插件市场入口提供手动教程，尚未实测所有 Desktop 版本的市场发现。

一个可复用的 FEM skill 不应硬编码作者几何的节点编号。先注册命名区域、选择器、期望节点/面数量和自由度，再交给模型适配器。梁示例 ROOT/TIP 的位置随长度更新；新壳体/接触/实体模型需单独实现 adapter，并用自己的基准证明边界映射和结果。
