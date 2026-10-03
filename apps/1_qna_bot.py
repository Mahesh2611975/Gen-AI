from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


# from langchain_ollama import ChatOllama
# llm = ChatOllama(
  #  model="qwen2.5:1.5b", 
 #   temperature=0
#)

#que = "Who is the president of India ?"

#result = llm.invoke(que)
#print(result.content)

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash")

st.title("Generative AI Chatbot")
st.markdown(" my first chatbot using Google Gemini API and Streamlit.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)


query = st.chat_input("Ask me anything:")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role": "ai", "content": res.content})
