import streamlit as st
import sys
import os
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv
load_dotenv()

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.graph_builder import build_graph



st.set_page_config(page_title="Stride Bot", layout="centered")
st.title("Stride.Bot")
st.markdown("Ask anything about leaves or project activities.")


if "agent" not in st.session_state:
    st.session_state.agent = build_graph()


THREAD_ID = "demo-user-thread-54"  


if "messages" not in st.session_state:
    st.session_state.messages = []

USER_AVATAR = "assets/user.png"
ASSISTANT_AVATAR = "assets/bot.png"

for msg in st.session_state.messages:
    role = msg["role"]
    avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR

    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])



# Chat input box
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user's message
    st.chat_message("user", avatar=USER_AVATAR).markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show assistant loader + final answer in the same bubble
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        message_box = st.empty()  # placeholder for dynamic content

        with st.spinner(""):


            try:
                state_input = {
                    "messages": [msg["content"] for msg in st.session_state.messages]
                }
                langfuse_handler = CallbackHandler()
                response = st.session_state.agent.invoke(
                    state_input,
                    config={"thread_id": THREAD_ID, "callbacks": [langfuse_handler]},
                )
                output = response.get("output", "No response from agent.")
            except Exception as e:
                output = f"❌ Error: {e}"

        # Replace the loader with the actual response
        message_box.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})