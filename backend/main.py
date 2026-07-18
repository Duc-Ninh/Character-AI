"""FastAPI entrypoint for the AI Roleplay backend."""

from fastapi import FastAPI

from backend.api.routes.chat import router as chat_router

app = FastAPI(title="AI Roleplay API", version="0.1.0")
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Simple health endpoint."""
    return {"status": "ok"}
