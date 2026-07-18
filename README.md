# Character-AI Starter Template

Starter template for an AI roleplay application inspired by Character.AI and MiraiMind.

## Project Structure

```text
backend/
  api/routes/chat.py
  core/config.py
  core/character_manager.py
  services/llm_service.py
  schemas/
  main.py
characters/
  sample_character.json
frontend/
  app.py
.env.example
requirements.txt
```

## Backend (FastAPI)

Run the backend API:

```bash
uvicorn backend.main:app --reload
```

Endpoints:
- `GET /health`
- `GET /api/characters`
- `POST /api/chat`

## Frontend (Streamlit)

Run the frontend:

```bash
streamlit run frontend/app.py
```

By default, frontend requests are sent to `http://localhost:8000/api`.

## Environment Configuration

Copy `.env.example` to `.env` and set provider keys:
- `OPENAI_API_KEY` for OpenAI
- `GEMINI_API_KEY` for Gemini
- `LLM_PROVIDER` to choose provider (`openai` or `gemini`)
- `MODEL_NAME` to set model
