from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.config import get_settings


REQUIRED_FIELDS = {
    "name",
    "description",
    "personality",
    "scenario",
    "first_message",
    "mes_example",
}


class CharacterService:
    def __init__(self) -> None:
        settings = get_settings()
        self.characters_dir = Path(settings.characters_dir)

    def get_character(self, character_name: str) -> dict[str, Any]:
        file_name = f"{character_name}.json"
        file_path = self.characters_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Character '{character_name}' was not found")

        with file_path.open("r", encoding="utf-8") as character_file:
            character = json.load(character_file)

        missing = REQUIRED_FIELDS - set(character.keys())
        if missing:
            raise ValueError(f"Character card is missing required fields: {sorted(missing)}")

        return character

    def list_characters(self) -> list[str]:
        if not self.characters_dir.exists():
            return []
        return sorted(path.stem for path in self.characters_dir.glob("*.json"))
