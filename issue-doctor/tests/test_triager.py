from issue_doctor.triager import Triager


def test_triager_extracts_stack_trace_and_questions():
    issue_text = """Bug: 程序崩溃\n\nTraceback (most recent call last):\n  File \"app.py\", line 10, in <module>\n    main()\nException: 测试错误\n\nSteps to reproduce:\n1. 运行 app.py\n"""
    triager = Triager()
    analysis = triager.process_issue(issue_text)

    assert "Traceback" in analysis.stack_trace[0]
    assert not analysis.questions
