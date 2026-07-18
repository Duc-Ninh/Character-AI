from __future__ import annotations

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    character_name: str = Field(..., description="Character card name")
    message: str = Field(..., description="Current user message")
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
