# 上传 Skill：贡献者完整教程

你可以贡献新 skill、修复代码、补参考文献、增加验证案例或改进教程。公开仓库支持所有 GitHub 用户通过 Fork → PR 贡献；无需成为协作者。

## 第一次上传：网页路线

1. 登录 GitHub，打开 [slab-skills](https://github.com/DJDeborah/slab-skills)，点击右上角 **Fork → Create fork**。在自己账号下得到副本。
2. 从 [skill 模板](templates/skill-template) 建立目录 `skills/my-skill-name/`；按 [格式说明](docs/FORMAT.md) 修改 frontmatter、默认调用与资源。
3. 在自己的 Fork 新建分支，比如 `add/my-skill-name`。
4. 打开 Fork 的 `skills`，用 **Add file → Upload files** 上传完整 skill 文件夹，或 **Create new file** 输入 `skills/my-skill-name/SKILL.md`。网页通常支持拖入文件夹；若目录层级未保留，使用 Git 路线。
5. 更新根目录 `catalog.json`，写用途、运行依赖、来源/许可和已经完成的验证范围。目录页读取该 catalog；目录名必须与 `name` 一致。
6. 在 Fork 的分支提交。回到主仓库，点击 **Compare & pull request**，选择 base `DJDeborah/slab-skills:main`，compare 为你的 Fork 分支。
7. 按 PR 模板写清问题、输入/输出、例子、执行过的检查、依赖和模型范围。提交 PR，等待自动检查与维护者审阅。
8. 如果要求修改，在相同分支继续提交；PR 会自动更新。合并后新 skill 出现在 main，正式 ZIP 需等下一次 Release。

网页上传有大小限制，不适合 ODB 等大文件。使用小型匿名示例；大型数据提供有许可和版本的外部链接。详见 [GitHub 上传文档](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)。

## 推荐：Git 路线

先在网页 Fork；下面把 `YOUR_NAME` 换成自己的 GitHub 用户名：

```powershell
git clone https://github.com/YOUR_NAME/slab-skills.git
cd slab-skills
git remote add upstream https://github.com/DJDeborah/slab-skills.git
git switch -c add/my-skill-name
```

复制模板到 `skills/my-skill-name`，编辑完整目录并更新 catalog。然后：

```powershell
python -m pip install -r requirements-dev.txt
python tools/validate_catalog.py
python -m unittest discover -s tests -v
python tools/run_demo.py --out local-runs/contributor-demo
python tools/install.py --dest ../slab-install-check --skill my-skill-name
git add skills/my-skill-name catalog.json
git commit -m "Add my-skill-name with example and validation"
git push -u origin add/my-skill-name
```

打开 GitHub 出现的 **Compare & pull request**，填写说明并提交。新增代码还应增加有意义的测试；纯说明型 skill 提供一个可复核的使用案例和人工检查标准即可。上传截图时保留真实运行上下文并去除私人路径。

## 后续同步

```powershell
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
git switch -c improve/my-skill-name
```

有本地修改时先提交或妥善保存再同步。官方 Fork/PR 说明见 [GitHub 贡献项目](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)。

## 审核标准

- 有明确触发场景、输入、输出、适用边界；名称使用小写连字符。
- 资源完整、依赖可重建、命令可复制；不要使用作者机器绝对路径。
- 写清楚实际验证过什么。区分格式检查、辅助脚本测试、求解器测量和真实研究判断。
- 外部代码保留上游许可、出处和必要声明；无法明确分享权限时不要提交。
- 使用公开或合成示例；不提交密码、个人信息、未公开研究文件、许可证地址或大规模求解结果。
- CI 通过。复杂物理模型另外附网格/时间/能量/边界和独立基准证据。

直接写权限由仓库拥有者在 Settings → Collaborators 授予具体 GitHub 账号。普通贡献者走 Fork/PR 即可；是否接受贡献由维护者决定。
