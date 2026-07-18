"""Character card loading utilities."""

from __future__ import annotations

import json
from pathlib import Path

from backend.schemas.character import CharacterCard

CHARACTERS_DIR = Path(__file__).resolve().parents[2] / "characters"


class CharacterManager:
    """Loads and serves character cards from JSON files."""

    @staticmethod
    def list_characters() -> list[str]:
        return sorted(path.stem for path in CHARACTERS_DIR.glob("*.json"))

    @staticmethod
    def get_character(name: str) -> CharacterCard:
        path = CHARACTERS_DIR / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Character '{name}' not found.")

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return CharacterCard(**data)
