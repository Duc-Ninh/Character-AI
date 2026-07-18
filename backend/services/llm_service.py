"""LLM provider integrations (OpenAI and Gemini)."""

from __future__ import annotations

from typing import Iterable

import google.generativeai as genai
from openai import OpenAI

from backend.core.config import settings
from backend.schemas.character import CharacterCard


class LLMService:
    """Generates chat responses using configured provider."""

    def __init__(self) -> None:
        self.provider = settings.llm_provider
        self.model_name = settings.model_name

    def generate_reply(
        self,
        character: CharacterCard,
        user_message: str,
        history: Iterable[dict[str, str]],
    ) -> str:
        if self.provider == "gemini":
            return self._gemini_reply(character, user_message, history)
        return self._openai_reply(character, user_message, history)

    def _base_prompt(self, character: CharacterCard) -> str:
        return (
            f"You are roleplaying as {character.name}.\n"
            f"Description: {character.description}\n"
            f"Personality: {character.personality}\n"
            f"Scenario: {character.scenario}\n"
            f"Example dialogue: {character.mes_example}\n"
            "Stay in character and answer naturally."
        )

    def _history_to_text(self, history: Iterable[dict[str, str]]) -> str:
        lines: list[str] = []
        for turn in history:
            role = turn.get("role", "user")
            content = turn.get("content", "")
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

    def _openai_reply(
        self,
        character: CharacterCard,
        user_message: str,
        history: Iterable[dict[str, str]],
    ) -> str:
        if not settings.openai_api_key:
            return "OPENAI_API_KEY is missing. Add it to your .env file."

        client = OpenAI(api_key=settings.openai_api_key)
        messages = [
            {"role": "system", "content": self._base_prompt(character)},
            {"role": "assistant", "content": character.first_message},
        ]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(model=self.model_name, messages=messages)
        return response.choices[0].message.content or ""

    def _gemini_reply(
        self,
        character: CharacterCard,
        user_message: str,
        history: Iterable[dict[str, str]],
    ) -> str:
        if not settings.gemini_api_key:
            return "GEMINI_API_KEY is missing. Add it to your .env file."

        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(model_name=self.model_name)
        prompt = (
            f"{self._base_prompt(character)}\n\n"
            f"Conversation so far:\n{self._history_to_text(history)}\n"
            f"User: {user_message}"
        )
        response = model.generate_content(prompt)
        return response.text or ""
