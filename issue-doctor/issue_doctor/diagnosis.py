"""Diagnosis Agent for issue-doctor."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .crawler import RepoCrawler


@dataclass
class DiagnosisReport:
    hypothesis: List[str]
    evidence: List[str]
    confidence: float
    reproduction_commands: List[str]
    suggested_fix: Optional[str]


class DiagnosisAgent:
    def __init__(self, crawler: RepoCrawler):
        self.crawler = crawler

    def diagnose(self, issue_text: str) -> DiagnosisReport:
        keywords = self._extract_keywords(issue_text)
        code_matches = self.crawler.search_code(keywords)
        hypothesis = self._build_hypothesis(issue_text, code_matches)
        reproduction = self._build_reproduction(issue_text)
        evidence = self._collect_evidence(code_matches)

        report = DiagnosisReport(
            hypothesis=hypothesis,
            evidence=evidence,
            confidence=0.65,
            reproduction_commands=reproduction,
            suggested_fix="请根据以上根因假设补充修复方案。",
        )
        return report

    def _extract_keywords(self, issue_text: str) -> List[str]:
        words = [word.strip(".,:()[]") for word in issue_text.split() if len(word) > 3]
        return list(dict.fromkeys(words))[:10]

    def _build_hypothesis(self, issue_text: str, code_matches: List[str]) -> List[str]:
        if code_matches:
            return [
                "可能由于关键模块匹配不到正确版本导致异常。",
                "可能是配置参数未按照文档填写导致路径错误。",
            ]
        return ["可能是依赖版本不兼容或使用方式不正确。"]

    def _build_reproduction(self, issue_text: str) -> List[str]:
        return ["python -m pytest tests/test_example.py"]

    def _collect_evidence(self, code_matches: List[str]) -> List[str]:
        evidence = []
        if code_matches:
            evidence.append(f"在仓库中找到 {len(code_matches)} 个潜在相关文件。")
        else:
            evidence.append("未在仓库中直接定位到相关代码片段。")
        return evidence
