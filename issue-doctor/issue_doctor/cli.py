"""Command line interface for issue-doctor."""
import argparse
from pathlib import Path

from .triager import Triager
from .crawler import RepoCrawler
from .diagnosis import DiagnosisAgent
from .fixer import Fixer
from .reviewer import Reviewer
from .docker_runner import DockerRunner
from .github_agent import GitHubAgent
from .pr_manager import PRManager


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="issue-doctor",
        description="GitHub Issue 智能诊断与自动修复 Agent 原型",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_triage = subparsers.add_parser("triage", help="分析并分类 Issue")
    parser_triage.add_argument("--issue", required=True, help="Issue 文本文件路径")

    parser_analyze = subparsers.add_parser("analyze", help="诊断 Issue 根因")
    parser_analyze.add_argument("--issue", required=True, help="Issue 文本文件路径")
    parser_analyze.add_argument("--repo", required=False, help="仓库根目录，可选")

    parser_fix = subparsers.add_parser("fix", help="生成修复建议并运行测试")
    parser_fix.add_argument("--issue", required=True, help="Issue 文本文件路径")
    parser_fix.add_argument("--repo", required=False, help="仓库根目录，可选")

    parser_reproduce = subparsers.add_parser("reproduce", help="使用 Docker 复现实验")
    parser_reproduce.add_argument("--issue", required=True, help="Issue 文本文件路径")
    parser_reproduce.add_argument("--repo", required=False, help="仓库根目录，可选")

    parser_review = subparsers.add_parser("review", help="自我审查生成的修复方案")
    parser_review.add_argument("--patch", required=True, help="修复补丁路径")

    parser_sync = subparsers.add_parser("github-sync", help="同步 GitHub Issue 数据")
    parser_sync.add_argument("--repo-full-name", required=True, help="GitHub 仓库全名，如 owner/repo")
    parser_sync.add_argument("--issue-number", type=int, help="Issue 编号，可选")

    parser_submit = subparsers.add_parser("submit-pr", help="生成并提交 PR 补丁")
    parser_submit.add_argument("--patch", required=True, help="修复补丁路径")
    parser_submit.add_argument("--repo-full-name", required=True, help="GitHub 仓库全名，如 owner/repo")
    parser_submit.add_argument("--branch", required=False, default="issue-doctor/fix", help="PR 分支名称")
    parser_submit.add_argument("--base", required=False, default="main", help="PR 目标分支")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    issue_file = Path(getattr(args, "issue", "")) if getattr(args, "issue", None) else None
    repo_root = Path(args.repo) if getattr(args, "repo", None) else None

    if args.command == "triage":
        content = issue_file.read_text(encoding="utf-8")
        triager = Triager()
        triager.process_issue(content)

    elif args.command == "analyze":
        content = issue_file.read_text(encoding="utf-8")
        crawler = RepoCrawler(repo_root=repo_root)
        diagnosis = DiagnosisAgent(crawler=crawler)
        report = diagnosis.diagnose(content)
        print(report)

    elif args.command == "fix":
        content = issue_file.read_text(encoding="utf-8")
        crawler = RepoCrawler(repo_root=repo_root)
        diagnosis = DiagnosisAgent(crawler=crawler)
        result = diagnosis.diagnose(content)
        fixer = Fixer(repo_root=repo_root)
        patch_path = fixer.create_fix(result)
        print(f"修复补丁生成：{patch_path}")

    elif args.command == "reproduce":
        content = issue_file.read_text(encoding="utf-8")
        crawler = RepoCrawler(repo_root=repo_root)
        diagnosis = DiagnosisAgent(crawler=crawler)
        report = diagnosis.diagnose(content)
        runner = DockerRunner()
        success = runner.run_repro(report.reproduction_commands, repo_root=repo_root)
        print("Docker 复现成功" if success else "Docker 复现失败")

    elif args.command == "review":
        reviewer = Reviewer()
        review = reviewer.review_patch(Path(args.patch))
        print(review)

    elif args.command == "github-sync":
        gh = GitHubAgent(repo_full_name=args.repo_full_name)
        if getattr(args, "issue_number", None):
            comment = gh.comment_issue(args.issue_number, "issue-doctor 已同步诊断信息，请检查最新建议。")
            print(f"已点评 Issue: {comment.get('html_url', 'unknown')}")
        else:
            print("请提供 --issue-number 来同步特定 Issue。")

    elif args.command == "submit-pr":
        fixer = Fixer(repo_root=repo_root)
        patch = Path(args.patch)
        if not patch.exists():
            print(f"补丁不存在：{patch}")
            return 1
        pr_manager = PRManager(repo_root=repo_root)
        if pr_manager.is_git_repo():
            branch = args.branch
            if pr_manager.create_branch(branch):
                if pr_manager.stage_patch(patch) and pr_manager.commit_patch("issue-doctor: 自动生成修复补丁"):
                    gh = GitHubAgent(repo_full_name=args.repo_full_name)
                    pr = gh.create_pull_request(
                        title="issue-doctor 自动修复建议",
                        head=branch,
                        base=args.base,
                        body="自动生成 PR，用于修复诊断到的 Issue。",
                    )
                    print(f"已创建 PR: {pr.get('html_url', 'unknown')}")
                else:
                    print("补丁提交失败，请检查 git 状态。")
            else:
                print("创建分支失败。")
        else:
            print("当前目录不是 Git 仓库，无法提交 PR。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
