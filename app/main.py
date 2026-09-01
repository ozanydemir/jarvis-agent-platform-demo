from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import AssistantRequest, AssistantResult
from app.orchestrator import simulate

app = FastAPI(title="Jarvis Agent Platform Demo", version="0.1.0")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "synthetic-adapters"}


@app.post("/simulate", response_model=AssistantResult)
def run(request: AssistantRequest) -> AssistantResult:
    return simulate(request)
