"""Streamlit frontend for AI Roleplay chat."""

from __future__ import annotations

import requests
import streamlit as st

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000/api")

st.set_page_config(page_title="AI Roleplay", page_icon="🗨️")
st.title("AI Roleplay Starter")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    character_response = requests.get(f"{API_BASE_URL}/characters", timeout=10)
    character_response.raise_for_status()
    characters = character_response.json()
except Exception as exc:  # pragma: no cover - frontend runtime guard
    st.error(f"Could not load characters from backend: {exc}")
    st.stop()

if not characters:
    st.warning("No character cards found in /characters.")
    st.stop()

selected_character = st.selectbox("Choose a character", characters)

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    payload = {
        "character_name": selected_character,
        "user_message": user_input,
        "history": st.session_state.history,
    }
    try:
        chat_response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=30)
        chat_response.raise_for_status()
        reply = chat_response.json().get("reply", "")
    except Exception as exc:  # pragma: no cover - frontend runtime guard
        reply = f"Backend error: {exc}"

    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
