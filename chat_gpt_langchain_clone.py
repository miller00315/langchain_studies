from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import streamlit as st

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title="Custom assistant",
)

st.subheader("Millerson")

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

# creating the messages (chat history) in the Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_message = st.text_input(label="System role")

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(SystemMessage(content=system_message))

user_prompt = st.chat_input(placeholder="Send a message")

if user_prompt:
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append(
            SystemMessage(content="You are a helpful assistant.")
        )

    st.session_state.messages.append(HumanMessage(content=user_prompt))

    with st.spinner("Working in your request"):
        response = chat.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))

if st.session_state.messages:
    for index, msg in enumerate(st.session_state.messages[1:]):
        with st.chat_message(
            "Momos", avatar="🦖" if isinstance(msg, HumanMessage) else "🤖"
        ):
            st.write(msg.content)
