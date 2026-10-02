# 仓库维护者手册

## 权限与审阅

仓库公开意味着可读、下载和 Fork。拥有者在 Settings → Collaborators 邀请具体账号，受邀者接受后才能直接写入。授予需要的最小权限。个人账号仓库与组织仓库可用角色不同，以当前 GitHub 设置为准。建议 main 使用 PR 审阅及 validate 必须通过，设置依套餐可用。

本次创建已启用 Issues、公开 Fork 和 GitHub Pages。未替未知贡献者授予写权限，也未把公开仓库做成无需审核的公共写入端点。

## 接收贡献

核对 LICENSE、出处、输入样例、触发条件、路径和证据边界；测试贡献者的完整目录安装。CI 只跑无许可证工具；需要 Abaqus 的 PR 应附版本、注册、数值结果及运行说明。来源不清楚或不可复现时请求具体修改。合并后更新 README 摘要、catalog 与 CHANGELOG。

## 发布

1. 从干净 main 运行 catalog 校验、测试、演示和安装验证。检查所有 tracked 文件，确认无私有数据与求解器许可证配置。
2. 更新 catalog/plugin 的版本及 CHANGELOG；提交发布准备。
3. 打 tag `git tag v0.x.y`，`git push origin main --tags`。
4. 在 GitHub Releases → Draft a new release，选择 tag，写清变化和实际验证范围；附完整目录 ZIP 与 SHA256。
5. ZIP 应来自 tracked 文件，不包含 local-runs、.git、.agents、ODB/CAE。Windows 可使用 Python zipfile 或 git archive。
6. 检查匿名访问、下载、安装和引用资源。报告 CI 结果，Abaqus 实测另列。

不改写已发布 tag；修复发布新版本。旧版本仍可用于复现。

## Pages 目录和 UI

Settings → Pages → Deploy from a branch → main → /(root)。根 index.html 读取 catalog.json，梁界面保持完整目录路径。`.nojekyll` 让静态资源按原路径发布。修改后查看 Pages build 状态；部署完成再验证 URL。详见 [GitHub Pages 官方文档](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

## 问题反馈

Issue 写明 skill、版本、操作系统、Python/求解器版本、最小输入、命令、期待/实际结果和精简错误。公开 Issue 不提交个人路径、token、许可地址或私有研究内容。需要敏感材料时先使用合成案例定位。
