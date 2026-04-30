"""RepoCrawler Agent for issue-doctor."""
import os
from pathlib import Path
from typing import List, Optional


class RepoCrawler:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path.cwd()

    def search_code(self, keywords: List[str], max_results: int = 20) -> List[str]:
        results = []
        for root, _, files in os.walk(self.repo_root):
            for filename in files:
                if filename.endswith((".py", ".md", ".yml", ".json", ".txt")):
                    path = Path(root) / filename
                    try:
                        content = path.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        continue
                    for keyword in keywords:
                        if keyword.lower() in content.lower():
                            results.append(str(path))
                            break
                    if len(results) >= max_results:
                        return results
        return results

    def search_history(self, keyword: str) -> List[str]:
        # 这里为原型提供简单的 commit 关键字搜索
        print(f"[RepoCrawler] 搜索历史记录关键词：{keyword}")
        return []
