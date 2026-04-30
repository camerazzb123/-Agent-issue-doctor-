import os

from issue_doctor.github_agent import GitHubAgent


def test_github_agent_builds_headers():
    token = "dummy-token"
    agent = GitHubAgent(repo_full_name="user/repo", token=token)
    headers = agent._make_headers()

    assert headers["Authorization"] == f"Bearer {token}"
    assert "User-Agent" in headers
