from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated


class ChatState(BaseModel):
    messages:Annotated[list, add_messages]

llm = ChatGroq(model="openai/gpt-oss-20b")

def chatBotNode(state:ChatState ) -> ChatState:
    res =llm.invoke(state.messages)
    state.messages=[res]
    return state


memory = InMemorySaver()

graph = StateGraph(ChatState)

# Add the chatbot node
graph.add_node("chatBot", chatBotNode)

# Define the flow
graph.add_edge(START, "chatBot")
graph.add_edge("chatBot", END)

# Compile the graph with memory
graph = graph.compile(checkpointer=memory)



config = {"configurable":{"thread_id":"2"}}

while True:
    query = input("user:")
    if query.lower() in ["quit", "exit","bye"]:
        print("thanks for using me !")
        break


    res = graph.invoke(
        {"messages":[{"role":"user","content":query}]},
        config
    )

    ans = res["messages"][-1].content
    print("Ai:", ans)


