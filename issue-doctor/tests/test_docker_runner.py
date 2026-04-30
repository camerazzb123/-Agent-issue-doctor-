from issue_doctor.docker_runner import DockerRunner


def test_docker_runner_has_method():
    runner = DockerRunner()
    assert hasattr(runner, "is_docker_available")
    assert hasattr(runner, "run_repro")
