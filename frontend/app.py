from __future__ import annotations

import json
from pathlib import Path

import requests
import streamlit as st

import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
CHARACTERS_DIR = Path(__file__).resolve().parents[1] / "characters"


def load_characters() -> dict[str, dict[str, str]]:
    characters: dict[str, dict[str, str]] = {}
    for path in CHARACTERS_DIR.glob("*.json"):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            characters[path.stem] = data
    return characters


def post_chat_message(payload: dict[str, object]) -> requests.Response:
    endpoints = ["/api/chat", "/chat"]
    last_response: requests.Response | None = None

    for endpoint in endpoints:
        response = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=30)
        if response.status_code != 404:
            return response
        last_response = response

    assert last_response is not None
    return last_response


st.set_page_config(page_title="AI Roleplay", page_icon="🎭")
st.title("🎭 AI Roleplay Starter")

characters = load_characters()
if not characters:
    st.error("No character cards found in /characters")
    st.stop()

selected = st.selectbox("Choose a character", options=sorted(characters.keys()))
selected_card = characters[selected]
st.caption(selected_card.get("description", ""))

opening_message = selected_card.get("first_message", "")

if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.get("active_character") != selected:
    st.session_state.active_character = selected
    st.session_state.history = []
    if opening_message:
        st.session_state.history.append({"role": "assistant", "content": opening_message})

if not st.session_state.history and opening_message:
    st.session_state.history.append({"role": "assistant", "content": opening_message})

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = post_chat_message(
            {
                "character_name": selected,
                "message": user_input,
                "history": st.session_state.history[:-1],
            }
        )
        response.raise_for_status()
        reply = response.json().get("reply", "No reply received.")
    except requests.RequestException as exc:
        reply = f"Backend error: {exc}"

    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
