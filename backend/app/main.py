from fastapi import FastAPI

from app.api.routes.chat import router as chat_router

app = FastAPI(title="AI Roleplay Backend", version="0.1.0")
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
