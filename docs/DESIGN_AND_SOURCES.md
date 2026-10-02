# 从优秀使用习惯到可分享资源

## 总结的工作方式

从授权项目中的已有交付、历史脚本与 skill 包整理出六项可迁移习惯：

1. 把 significance 写成会改变的科学/设计决策，附竞争解释与判别实验。
2. 为 gap 保留查询、覆盖范围与能力矩阵，主动查反例，限制首次性说法。
3. 建模前注册几何、参考态、单位、载荷、支撑和输出；解析与 FEM 共用定义。
4. 小批量测试后冻结扫描，保留 case ID、源文件哈希、失败 attempt 与恢复证据。
5. 写作时维护 claim→evidence，不丢掉 Main/SI 中支撑结论的必要内容。
6. 交付阶段注明已证实/尚未证实/下一步最便宜测试，让别人能接着做。

本次公开实现只保留通用逻辑、合成输入和通用梁测量。原始研究路径、私有 specimen、未发表手稿与完整历史对话不公开。这里是对可复用模式的总结，不是完整用户使用历史统计。

## 合集来源与许可

- research-significance/gap/writing/fem-explicit-bifurcation：整合自 [DJDeborah/research-mechanics-skills](https://github.com/DJDeborah/research-mechanics-skills)，MIT；旧四项的来源见 [原来源表](SOURCES.md)。
- helix-rod-design、cauchy-micropolar-modeling、fem-cae-verification、mechanics-research-handoff：来自同一授权工作目录的 mechanics-skills-lab 生成包。本次以通用规范/程序整理为 MIT。
- rapid-mechanics-hypothesis、register-analytical-fem、research-evidence-handoff：来自授权工作目录 research-workflow-pack 通用 skill。
- abaqus-parametric-workflow、beam-parameter-interface：本次新写的通用工具；前者基于本作者四项包的 beam adapter，并重新实现队列/冻结/恢复；后者是新的独立 UI。

catalog 的 source 字段记录各项来源，verification 记录验证范围。未把外部科学 skill 的代码混入后声称已经统一验证。

## 外部开源参考

OpenAI 历史 [skills 仓库](https://github.com/openai/skills) 提供 skill-creator 与 skill-installer 结构；[官方 Skills 说明](https://learn.chatgpt.com/docs/build-skills) 解释安装和按需资源。旧 skills 仓库已标注弃用，当前官方示例转到 [openai/plugins](https://github.com/openai/plugins)。它们用于格式和安装路线参考，不是当前梁模型科学有效性的证据。

社区候选 [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) 可以作为科学文献/写作/软件生态的检索入口；[UCL-ERL/skills](https://github.com/UCL-ERL/skills) 可作为其他开放 skill 结构的阅读入口。使用前核对最新目录、许可、依赖、环境和单项证据。这两者没有作为本合集新增代码的来源，也没有宣称其力学模型或完整工作流通过本次测试。

GitHub 贡献/上传/Pages 的操作依据官方文档，相关链接放在对应教程。所有截图来自当前界面实际运行；示意图为本项目原创。外部论文与商用求解器保留各自许可，MIT 只覆盖本仓库可分享内容。
