import re
from dataclasses import dataclass

import streamlit as st

from chatbot.constants import ASSISTANT, CHAT_HISTORY, LLM_MODEL, USER
from chatbot.model import ModelLoader


@dataclass
class ChatMessage:
    role: str
    message: str


def chat_history_init(current_page: str) -> None:
    if st.session_state.page != current_page:
        del st.session_state[CHAT_HISTORY]
        st.session_state[CHAT_HISTORY] = list()


def view_chat_history() -> None:
    avatar = {USER: "🐼", ASSISTANT: "🤖"}
    for chat_message in st.session_state[CHAT_HISTORY]:
        with st.chat_message(chat_message.role, avatar=avatar[chat_message.role]):
            st.markdown(chat_message.message)


def chat_history_to_str(conversation: list[ChatMessage]) -> str:
    conversation_history = ""
    for chat_message in conversation:
        conversation_history += f"{chat_message.role}: {chat_message.message}\n"
    return conversation_history


@st.cache_resource(show_spinner=False)
def load_llm_model() -> tuple:
    model, tokenizer = ModelLoader.load(LLM_MODEL)
    return model, tokenizer


def clean_eos_token(text: str, eos_token: str) -> str:
    return re.sub(f"{eos_token}$", "", text)
