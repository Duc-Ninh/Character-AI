"""Chat API endpoints."""

from fastapi import APIRouter, HTTPException

from backend.core.character_manager import CharacterManager
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


@router.get("/characters", response_model=list[str])
def list_characters() -> list[str]:
    """Return available character cards."""
    return CharacterManager.list_characters()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Generate character response for a user message."""
    try:
        character = CharacterManager.get_character(request.character_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    reply = llm_service.generate_reply(
        character=character,
        user_message=request.user_message,
        history=request.history,
    )
    return ChatResponse(character_name=character.name, reply=reply)
