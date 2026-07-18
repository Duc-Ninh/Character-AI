from __future__ import annotations

from openai import OpenAI
import google.generativeai as genai

from app.core.config import get_settings


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_reply(self, prompt: str) -> str:
        provider = self.settings.llm_provider
        if provider == "openai":
            return self._generate_openai(prompt)
        if provider == "gemini":
            return self._generate_gemini(prompt)
        return self._generate_mock(prompt)

    def _generate_openai(self, prompt: str) -> str:
        if not self.settings.openai_api_key:
            return self._generate_mock(prompt)

        client = OpenAI(api_key=self.settings.openai_api_key)
        response = client.responses.create(
            model=self.settings.openai_model,
            input=prompt,
        )
        return response.output_text

    def _generate_gemini(self, prompt: str) -> str:
        if not self.settings.gemini_api_key:
            return self._generate_mock(prompt)

        genai.configure(api_key=self.settings.gemini_api_key)
        model = genai.GenerativeModel(self.settings.gemini_model)
        response = model.generate_content(prompt)
        return response.text or ""

    @staticmethod
    def _generate_mock(prompt: str) -> str:
        snippet = prompt[-300:]
        return f"[Mock reply] {snippet}"
