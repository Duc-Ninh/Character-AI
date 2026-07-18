"""Application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Environment-driven settings."""

    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")


settings = Settings()
