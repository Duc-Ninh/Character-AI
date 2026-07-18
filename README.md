# Character-AI

Starter template for an AI roleplay application.

## Project structure

- `backend/app/api`: FastAPI routes
- `backend/app/core`: app configuration
- `backend/app/services`: character and LLM services
- `backend/app/models`: request/response schemas
- `characters/`: character cards in JSON format
- `frontend/`: Streamlit UI

## Run backend

```bash
uvicorn app.main:app --app-dir backend --reload
```

## Run frontend

```bash
streamlit run frontend/app.py
```

## Environment

Copy `.env.example` to `.env` and set your API keys.
