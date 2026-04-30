"""Fixer Agent for issue-doctor."""
from pathlib import Path
from typing import Optional

from .diagnosis import DiagnosisReport


class Fixer:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path.cwd()

    def create_fix(self, report: DiagnosisReport) -> Path:
        patch_path = self.repo_root / "issue_doctor_fix.patch"
        patch_text = self._build_patch_text(report)
        patch_path.write_text(patch_text, encoding="utf-8")
        return patch_path

    def _build_patch_text(self, report: DiagnosisReport) -> str:
        patch = [
            "diff --git a/README.md b/README.md",
            "index 0000000..0000000 100644",
            "--- a/README.md",
            "+++ b/README.md",
            "@@ -1,3 +1,4 @@",
            " # issue-doctor",
            "+# issue-doctor 自动修复补丁占位，用于测试 patch 提交流程",
            "",
        ]
        return "\n".join(patch)

    def run_tests(self) -> bool:
        print("[Fixer] 运行测试套件（原型模拟）。")
        return True
