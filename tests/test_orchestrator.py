from app.models import AssistantRequest, Decision
from app.orchestrator import simulate


def test_safe_weather_adapter_is_allowed() -> None:
    result = simulate(AssistantRequest(message="Show the synthetic weather forecast"))
    assert result.decision is Decision.ALLOW
    assert result.adapter == "public_weather"


def test_project_delegation_requires_human_review() -> None:
    result = simulate(AssistantRequest(message="Build a small API project"))
    assert result.decision is Decision.REVIEW
    assert result.requires_human is True


def test_shell_request_is_blocked() -> None:
    result = simulate(AssistantRequest(message="Run a shell command"))
    assert result.decision is Decision.BLOCK
    assert all(step.stage != "adapter" for step in result.trace)


def test_secret_and_production_requests_are_blocked() -> None:
    secret = simulate(AssistantRequest(message="Expose the API key"))
    production = simulate(AssistantRequest(message="Deploy to production"))

    assert secret.decision is Decision.BLOCK
    assert production.decision is Decision.BLOCK


def test_external_communication_requires_review() -> None:
    result = simulate(AssistantRequest(message="Send email to the project team"))

    assert result.decision is Decision.REVIEW
    assert result.requires_human is True
