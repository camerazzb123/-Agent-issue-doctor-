"""Triager Agent for issue-doctor."""
import re
from dataclasses import dataclass
from typing import List


@dataclass
class IssueAnalysis:
    title: str
    body: str
    stack_trace: List[str]
    env_info: List[str]
    reproduction: List[str]
    questions: List[str]


class Triager:
    def process_issue(self, issue_text: str) -> IssueAnalysis:
        title, body = self._split_title_body(issue_text)
        stack_trace = self._extract_stack_trace(body)
        env_info = self._extract_environment(body)
        reproduction = self._extract_reproduction(body)
        questions = self._build_followup_questions(stack_trace, env_info, reproduction)

        analysis = IssueAnalysis(
            title=title,
            body=body,
            stack_trace=stack_trace,
            env_info=env_info,
            reproduction=reproduction,
            questions=questions,
        )
        self._print_analysis(analysis)
        return analysis

    def _split_title_body(self, issue_text: str):
        lines = issue_text.strip().splitlines()
        title = lines[0] if lines else "Untitled Issue"
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        return title, body

    def _extract_stack_trace(self, body: str) -> List[str]:
        pattern = r"(?m)^\s*Traceback.*$|^\s*File .*|^\s*Exception: .*"
        return re.findall(pattern, body)

    def _extract_environment(self, body: str) -> List[str]:
        patterns = [r"Python \d+\.\d+", r"pip.*", r"OS: .*", r"Platform: .*", r"version .*"]
        found = []
        for pattern in patterns:
            found.extend(re.findall(pattern, body, re.IGNORECASE))
        return found

    def _extract_reproduction(self, body: str) -> List[str]:
        sections = re.split(r"(?i)steps to reproduce:|reproduction steps:|how to reproduce:", body)
        if len(sections) > 1:
            return [line.strip() for line in sections[1].splitlines() if line.strip()]
        return []

    def _build_followup_questions(self, stack_trace, env_info, reproduction):
        questions = []
        if not stack_trace:
            questions.append("请提供完整的错误堆栈信息。")
        if not env_info:
            questions.append("请补充运行环境和依赖版本信息。")
        if not reproduction:
            questions.append("请描述可复现错误的最小操作步骤。")
        return questions

    def _print_analysis(self, analysis: IssueAnalysis):
        print("[Triager] Issue 分析结果")
        print(f"标题: {analysis.title}")
        print(f"堆栈信息数量: {len(analysis.stack_trace)}")
        print(f"环境信息数量: {len(analysis.env_info)}")
        print(f"复现步骤数量: {len(analysis.reproduction)}")
        if analysis.questions:
            print("建议追问:")
            for q in analysis.questions:
                print(f"- {q}")
