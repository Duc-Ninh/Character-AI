from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.character_service import CharacterService
from app.services.llm_service import LLMService

router = APIRouter()
character_service = CharacterService()
llm_service = LLMService()


@router.get("/characters")
def list_characters() -> dict[str, list[str]]:
    return {"characters": character_service.list_characters()}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        character = character_service.get_character(request.character_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    history = "\n".join(f"{item.role}: {item.content}" for item in request.history)
    prompt = (
        f"You are roleplaying as {character['name']}.\n"
        f"Description: {character['description']}\n"
        f"Personality: {character['personality']}\n"
        f"Scenario: {character['scenario']}\n"
        f"Example dialogue: {character['mes_example']}\n"
        f"Conversation history:\n{history}\n"
        f"User: {request.message}\n"
        "Respond in-character and stay concise."
    )

    reply = llm_service.generate_reply(prompt)
    return ChatResponse(reply=reply)
