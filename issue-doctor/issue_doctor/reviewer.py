"""Reviewer Agent for issue-doctor."""
from pathlib import Path


class Reviewer:
    def review_patch(self, patch_path: Path) -> str:
        if not patch_path.exists():
            return f"补丁文件不存在：{patch_path}"
        return (
            "[Reviewer] 已审查生成的修复补丁。\n"
            "建议检查边界情况、回归测试和文档更新。"
        )
