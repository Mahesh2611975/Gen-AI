from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


# -----------------------------
# LLM
# -----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0, streaming=True
)


# -----------------------------
# Google Search Tool
# -----------------------------

search = GoogleSerperAPIWrapper()
tools = [search.run]


# -----------------------------
# Streamlit Memory
# -----------------------------

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# Agent
# -----------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt=(
        "You are an amazing AI agent and can search on Google "
        "when necessary to answer the user's question."
    )
)


# -----------------------------
# Streamlit UI
# -----------------------------

st.subheader("🤖 QuickAnswer - Answers at the speed of thought")


# Display previous messages
for message in st.session_state.history:

    role = message["role"]
    content = message["content"]

    st.chat_message(role).markdown(content)


# Chat input
query = st.chat_input("Ask Anything ?")


if query:

    # Show user message
    st.chat_message("user").markdown(query)

    # Save user message
    st.session_state.history.append({
        "role": "user",
        "content": query
    })


    # Run agent
    response = agent.stream(
        {"messages": [{"role": "user","content": query}]},
        {"configurable": {"thread_id": "1"}},
        stream_mode="messages"
    )

    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()

        message = ""

        for chunk in response:
            message = message + chunk[0].content
            space.write(message)
    
        st.session_state.history.append({"role": "assistant","content": message})

 