"""GitHub API integration for issue-doctor."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


class GitHubAgent:
    def __init__(self, repo_full_name: str, token: Optional[str] = None):
        self.repo_full_name = repo_full_name
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"

    def _make_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "issue-doctor/0.1",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        url = urllib.parse.urljoin(self.api_base, path)
        payload = None
        if data is not None:
            payload = json.dumps(data).encode("utf-8")
        request = urllib.request.Request(url, data=payload, method=method)
        for name, value in self._make_headers().items():
            request.add_header(name, value)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            message = exc.read().decode("utf-8")
            raise RuntimeError(f"GitHub API 请求失败：{exc.code} {message}")

    def comment_issue(self, issue_number: int, body: str) -> Dict[str, Any]:
        path = f"/repos/{self.repo_full_name}/issues/{issue_number}/comments"
        return self._request("POST", path, {"body": body})

    def create_pull_request(self, title: str, head: str, base: str = "main", body: str = "") -> Dict[str, Any]:
        path = f"/repos/{self.repo_full_name}/pulls"
        return self._request("POST", path, {"title": title, "head": head, "base": base, "body": body})

    def search_issues(self, query: str) -> List[Dict[str, Any]]:
        path = f"/search/issues?q={urllib.parse.quote(query)}+repo:{self.repo_full_name}"
        result = self._request("GET", path)
        return result.get("items", [])
