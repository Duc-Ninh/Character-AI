"""Pydantic schema for character cards."""

from pydantic import BaseModel


class CharacterCard(BaseModel):
    name: str
    description: str
    personality: str
    scenario: str
    first_message: str
    mes_example: str
