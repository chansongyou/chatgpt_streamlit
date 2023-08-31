import logging
import os
import time

from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.stateful_chat import chat, add_message

load_dotenv()

logger = logging.getLogger(__name__)

st.title("My GPT")

DISABLE = "chat_disable"


def enable_chat_input():
    st.session_state[DISABLE] = False


def disable_chat_input():
    st.session_state[DISABLE] = True


with chat("my_chat"):
    if DISABLE not in st.session_state:
        st.session_state[DISABLE] = False

    if prompt := st.chat_input(
        "send message", disabled=st.session_state[DISABLE], on_submit=disable_chat_input
    ):
        add_message("human", prompt)

        def stream_prompt():
            for word in prompt.split():
                yield word + " "
                time.sleep(0.15)

        add_message("ai", "Echo :", stream_prompt)

        enable_chat_input()

        # Explicitly rerun app to enable chat_input. Code position is critical. Don't move this code out of 'if prompt' block.
        st.experimental_rerun()
