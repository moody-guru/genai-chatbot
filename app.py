import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="Groq Chatbot", page_icon="💬")
st.title("💬 Groq Chatbot")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None
if not api_key:
    st.error("GROQ_API_KEY is not set. Add it to your local .env file or Streamlit secrets.")
    st.stop()

try:
    model_name = os.getenv("GROQ_MODEL") or st.secrets.get(
        "GROQ_MODEL", "openai/gpt-oss-120b"
    )
except Exception:
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
llm = ChatGroq(model=model_name, api_key=api_key, temperature=0.7)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = [SystemMessage(content="You are a helpful, friendly assistant.")]
    for message in st.session_state.messages:
        if message["role"] == "user":
            conversation.append(HumanMessage(content=message["content"]))
        else:
            conversation.append(AIMessage(content=message["content"]))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = llm.invoke(conversation)
                answer = response.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as exc:
                st.error(f"Groq request failed: {exc}")

with st.sidebar:
    st.caption(f"Model: `{model_name}`")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
