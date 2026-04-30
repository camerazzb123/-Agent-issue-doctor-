# 贡献指南

欢迎为 `issue-doctor` 贡献！

## 贡献方式

- 提交 bug 报告
- 提交功能建议
- 修复代码并创建 PR
- 补充文档、测试或示例

## 开发流程

1. Fork 本仓库
2. 克隆到本地
3. 创建新分支：
   ```powershell
   git checkout -b feature/your-feature-name
   ```
4. 编写代码并测试
5. 提交到远程分支：
   ```powershell
   git push origin feature/your-feature-name
   ```
6. 在 GitHub 上创建 Pull Request

## 代码规范

- 使用 Python 3.10+
- 保持代码简洁、模块化
- 增加对应单元测试
- 更新 `README.md` 或示例文档

## 测试

运行测试：

```powershell
python -m pip install -e .
python -m pytest
```
