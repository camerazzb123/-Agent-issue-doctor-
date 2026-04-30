# 无法启动测试套件

## 问题描述

运行 `python -m pytest` 时出现错误，无法执行测试。

## 错误信息

Traceback (most recent call last):
  File "tests/test_example.py", line 5, in <module>
    from issue_doctor import main
ModuleNotFoundError: No module named 'issue_doctor'

## 复现步骤

1. 克隆仓库
2. 创建虚拟环境
3. 运行 `python -m pytest`

## 期望结果

测试套件能够正常执行。
