from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.reading import router as reading_router
from backend.app.api.routes.progress import router as progress_router
from backend.app.api.routes.vocab import router as vocab_router
from backend.app.core.config import settings
from backend.app.schemas.response_schema import HealthResponse


app = FastAPI(title=settings.api_title, version=settings.api_version)

app.add_middleware(
	CORSMiddleware,
	allow_origins=list(settings.cors_allow_origins),
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(reading_router)
app.include_router(auth_router)
app.include_router(vocab_router)
app.include_router(progress_router)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
	return HealthResponse(status="ok")

