# issue-doctor

GitHub Issue 智能诊断与自动修复 Agent

## 项目简介

`issue-doctor` 是一个为开源项目维护者设计的智能 Issue 诊断与自动修复原型框架。它将核心流程拆分为多个 Agent：Triager、Repo Crawler、Diagnosis、Fixer、Reviewer，帮助快速定位问题、构造复现、生成修复补丁，并自动运行测试。

## 核心功能

- `Triager`：自动提取 Issue 中的异常信息、环境信息、复现步骤；若信息不足，生成追问建议
- `Repo Crawler`：根据错误堆栈提取关键词，搜索仓库代码、历史提交、Issue/PR
- `Diagnosis`：构建根因假设、尝试最小复现、匹配文档与依赖 changelog
- `Fixer`：生成修复方案、patch 或代码修改，并运行测试验证
- `Reviewer`：为生成的 PR 做自我审查，评估边界情况与破坏性变更

## 目录结构

- `issue_doctor/`：核心模块代码
- `tests/`：单元测试示例
- `examples/`：示例 Issue 文本和场景说明

## 安装

```bash
python -m pip install -e .
python -m pip install -r requirements-dev.txt
```

## 使用示例

```bash
python -m issue_doctor triage --issue examples/sample_issue.md
python -m issue_doctor analyze --issue examples/sample_issue.md --repo .
python -m issue_doctor fix --issue examples/sample_issue.md --repo .
python -m issue_doctor reproduce --issue examples/sample_issue.md --repo .
python -m issue_doctor github-sync --repo-full-name owner/repo --issue-number 123
python -m issue_doctor submit-pr --patch issue_doctor_fix.patch --repo-full-name owner/repo --branch issue-doctor/fix
```

## 新增扩展功能

- `reproduce`：使用 Docker 在隔离环境中尝试最小复现问题
- `github-sync`：与 GitHub Issue 交互，自动评论同步诊断结果
- `submit-pr`：在 Git 仓库中创建补丁分支、提交修复并创建 PR

## GitHub 令牌配置

要使用 `github-sync` 或 `submit-pr`，请先设置环境变量：

```bash
export GITHUB_TOKEN=your_token
```

Windows PowerShell：

```powershell
$env:GITHUB_TOKEN = "your_token"
```

## GitHub 仓库配置

项目已经包含：

- `.github/workflows/python-package.yml`：自动运行 `pytest` 的 GitHub Actions CI
- `.github/ISSUE_TEMPLATE/bug_report.md`：Bug 报告模板
- `.github/ISSUE_TEMPLATE/feature_request.md`：功能建议模板
- `.github/pull_request_template.md`：PR 模板

推送到 GitHub 后，这些文件会自动生效。

## 贡献指南

详细贡献流程请参考 `CONTRIBUTING.md`。

## 设计理念

- 用代码构建完整项目原型，方便上传到 GitHub
- 保持模块化、易于扩展和真实项目对接
- 支持后续插件化：接入 GitHub API、Docker 复现、LLM 推理

## 开发方向

1. 补全 GitHub Issue 监听与评论接口
2. 接入 repo grep/commit history 搜索
3. 添加 Docker 最小复现支撑
4. 集成测试执行与 PR 自动提交

## 许可证

MIT
