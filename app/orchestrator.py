from app.models import AssistantRequest, AssistantResult, Decision, TraceStep

BLOCKED_CAPABILITIES = {
    "shell or filesystem": ("shell", "filesystem", "delete", "erase", "wipe"),
    "secret disclosure": ("api key", "secret", "token", "credential", "password", "private key"),
    "production change": ("production deploy", "deploy to production", "release to production"),
}
REVIEW_ACTIONS = {
    "project delegation": ("project", "repository", "implement", "build"),
    "external communication": ("send email", "send message", "post", "publish"),
    "external data transfer": ("upload", "download", "share", "export"),
    "account or access change": ("grant access", "invite", "permission"),
    "deployment": ("deploy", "release"),
    "financial action": ("payment", "purchase", "transfer money"),
}


def _classify(message: str) -> tuple[str, str]:
    text = message.casefold()
    if any(term in text for term in ("weather", "forecast")):
        return "weather_query", "public_weather"
    if any(term in text for term in ("calculate", "sum", "multiply")):
        return "calculation", "safe_calculator"
    if any(term in text for term in ("project", "repository", "implement", "build")):
        return "project_delegation", "engineering_agent"
    return "conversation", "conversation_response"


def simulate(request: AssistantRequest) -> AssistantResult:
    intent, adapter = _classify(request.message)
    text = request.message.casefold()
    blocked = sorted(
        capability
        for capability, terms in BLOCKED_CAPABILITIES.items()
        if any(term in text for term in terms)
    )
    review = sorted(
        action
        for action, terms in REVIEW_ACTIONS.items()
        if any(term in text for term in terms)
    )
    if blocked:
        decision = Decision.BLOCK
        requires_human = False
        response = "The request was blocked by local policy before any adapter could run."
    elif review or intent == "project_delegation":
        decision = Decision.REVIEW
        requires_human = True
        response = "The request was converted to a scoped ticket for human approval."
    else:
        decision = Decision.ALLOW
        requires_human = False
        response = "The synthetic adapter completed within its allowlisted capability."

    trace = [
        TraceStep(stage="classify", status="complete", detail=f"Intent: {intent}", elapsed_ms=18),
        TraceStep(stage="select", status="complete", detail=f"Adapter: {adapter}", elapsed_ms=7),
        TraceStep(
            stage="policy",
            status=decision.value,
            detail="Deterministic local evaluation",
            elapsed_ms=3,
        ),
    ]
    if decision is Decision.ALLOW:
        trace.append(
            TraceStep(
                stage="adapter", status="complete", detail="Synthetic response only", elapsed_ms=24
            )
        )
    return AssistantResult(
        intent=intent,
        adapter=adapter,
        decision=decision,
        response=response,
        requires_human=requires_human,
        trace=trace,
    )
