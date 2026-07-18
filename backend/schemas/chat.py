"""Pydantic schemas for chat requests and responses."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    character_name: str = Field(..., description="Character card file name without extension")
    user_message: str = Field(..., min_length=1)
    history: list[dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    character_name: str
    reply: str
