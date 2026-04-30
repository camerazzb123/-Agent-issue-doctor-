"""PR management helper for issue-doctor."""
import subprocess
from pathlib import Path
from typing import Optional


class PRManager:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path.cwd()

    def _run_git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=self.repo_root, capture_output=True, text=True)

    def is_git_repo(self) -> bool:
        result = self._run_git("rev-parse", "--is-inside-work-tree")
        return result.returncode == 0

    def create_branch(self, branch_name: str) -> bool:
        result = self._run_git("checkout", "-b", branch_name)
        if result.returncode != 0:
            print(result.stderr)
        return result.returncode == 0

    def stage_patch(self, patch_path: Path) -> bool:
        result = self._run_git("apply", str(patch_path))
        if result.returncode != 0:
            print(result.stderr)
            return False
        return True

    def commit_patch(self, message: str) -> bool:
        result_stage = self._run_git("add", "-A")
        if result_stage.returncode != 0:
            print(result_stage.stderr)
            return False
        result_commit = self._run_git("commit", "-m", message)
        if result_commit.returncode != 0:
            print(result_commit.stderr)
            return False
        return True
