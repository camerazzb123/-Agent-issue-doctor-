from issue_doctor.crawler import RepoCrawler
from issue_doctor.diagnosis import DiagnosisAgent


def test_diagnosis_returns_report():
    crawler = RepoCrawler(repo_root=None)
    diagnosis = DiagnosisAgent(crawler=crawler)
    report = diagnosis.diagnose("Error: failed to import module")

    assert report.confidence > 0
    assert report.hypothesis
    assert report.evidence
