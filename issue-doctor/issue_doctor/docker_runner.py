"""Docker-based reproduction support for issue-doctor."""
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional


class DockerRunner:
    def __init__(self, image: str = "python:3.12-slim"):
        self.image = image

    def is_docker_available(self) -> bool:
        result = subprocess.run(["docker", "version"], capture_output=True, text=True)
        return result.returncode == 0

    def run_repro(self, commands: List[str], repo_root: Optional[Path] = None) -> bool:
        if not self.is_docker_available():
            print("[DockerRunner] Docker 未安装或不可用，跳过复现。")
            return False

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            if repo_root:
                target = temp_path / "repo"
                shutil.copytree(repo_root, target)
            script_path = temp_path / "run_repro.sh"
            script_text = "\n".join(commands)
            script_path.write_text(script_text, encoding="utf-8")
            cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{temp_dir}:/workspace",
                "-w",
                "/workspace",
                self.image,
                "bash",
                str(script_path.name),
            ]
            print(f"[DockerRunner] 运行 Docker 复现：{' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return result.returncode == 0
