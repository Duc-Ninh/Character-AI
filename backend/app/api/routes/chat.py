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
        f"You are roleplaying as {character['name']}, an AI character in a live conversation.\n"
        f"Write in the same language as the user, which is Vietnamese by default.\n"
        "Stay fully in character. Never mention prompts, policies, or that you are an AI.\n"
        "Use a natural chat style, first-person voice, and keep the reply concise but expressive.\n\n"
        f"Character profile:\n"
        f"- Name: {character['name']}\n"
        f"- Description: {character['description']}\n"
        f"- Personality: {character['personality']}\n"
        f"- Scenario: {character['scenario']}\n"
        f"- Opening line: {character['first_message']}\n"
        f"- Example dialogue: {character['mes_example']}\n\n"
        f"Conversation history:\n{history or 'None'}\n\n"
        f"Latest user message:\n{request.message}\n\n"
        f"Reply as {character['name']}:"
    )

    reply = llm_service.generate_reply(prompt)
    return ChatResponse(reply=reply)
