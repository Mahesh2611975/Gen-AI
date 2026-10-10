from dotenv import load_dotenv
load_dotenv()

### db, llm, tools, create_agent, system_prompt

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver   
from langchain.agents import create_agent
import streamlit as st

db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

db.run("""
    
   CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (
        status IN ('pending', 'in_progress', 'completed')
    ) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

model = ChatGroq(model="openai/gpt-oss-20b")

tollkit = SQLDatabaseToolkit(db=db,llm=model)
tools = tollkit.get_tools()
memory = InMemorySaver()




system_prompt = """
You are a task management assistant that interacts with a SQLite
database containing a table named 'task'.

TASK RULES:
1. Limit SELECT queries to a maximum of 10 results.
2. Order task lists by created_at DESC.
3. After CREATE, UPDATE, or DELETE, verify the change using SELECT.
4. Display task lists in a structured table.
5. Use only these statuses: pending, in_progress, completed.

CRUD OPERATIONS:
CREATE: INSERT INTO task (title, description, status)
READ: SELECT * FROM task ORDER BY created_at DESC LIMIT 10
UPDATE: UPDATE task SET status=? WHERE id=?
DELETE: DELETE FROM task WHERE id=?

Table schema: id, title, description, status, created_at.
"""


@st.cache_resource
def get_agent():
    agent = create_agent(
        model = model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent

agent =get_agent()


st.subheader(" TaskBot - manage your task")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])
prompt = st.chat_input("Ask me to manage your tasks..")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("ai"):
        with st.spinner("processing...."):
            response = agent.invoke(
                {"messages":[{"role":"user", "content":prompt}]},
                {"configurable":{"thread_id":"1"}}
            )
            result = response["messages"][-1].content
            st.markdown(result)
            st.session_state.messages.append({"role":"ai", "content":result})

     