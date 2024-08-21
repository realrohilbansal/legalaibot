from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import streamlit as st
import time
import logging
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from app.settings import load_env_variables
from app.logger import setup_logger
from data.vector_db import load_vector_db, save_vector_db
from data.embeddings import get_openai_embeddings

# Load environment variables and setup logging
openai_api_key = load_env_variables()
setup_logger()

st.set_page_config(page_title="LawGPT")
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("assets/Black Bold Initial AI Business Logo.jpg")

st.markdown("""
    <style>
    .stApp, .ea3mdgi6{ background-color:#000000; }
    div.stButton > button:first-child { background-color: #ffd0d0; }
    div.stButton > button:active { background-color: #ff6262; }
    div[data-testid="stStatusWidget"] div button { display: none; }
    .reportview-container { margin-top: -2em; }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    button[title="View fullscreen"]{ visibility: hidden;}
    button:first-child{ background-color : transparent !important; }
    </style>
""", unsafe_allow_html=True)

def reset_conversation():
    st.session_state.messages = []
    st.session_state.memory.clear()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Use OpenAI embeddings
embeddings = get_openai_embeddings(openai_api_key)

# Placeholder data for creating the vector database
data = [
    "Example legal text 1",
    "Example legal text 2",
    "Example legal text 3",
    # Add more data as needed
]

# Load vector database using FAISS
db_path = "./ipc_vector_db/vectordb"
vector_db = load_vector_db(db_path, embeddings, data)
db_retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

prompt_template = """<s>[INST]This is a chat template and As a legal chat bot specializing in Indian Penal Code queries, your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

# Use OpenAI LLM
llm = OpenAI(model_name="text-davinci-003", temperature=0.5, max_tokens=1024, openai_api_key=os.getenv("OPENAI_API_KEY"))

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True),
    retriever=db_retriever,
    combine_docs_chain_kwargs={'prompt': prompt}
)

for message in st.session_state.get("messages", []):
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))

input_prompt = st.chat_input("Say something")

if input_prompt:
    with st.chat_message("user"):
        st.write(input_prompt)

    st.session_state.messages.append({"role": "user", "content": input_prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking 💡..."):
            result = qa.invoke(input=input_prompt)

            message_placeholder = st.empty()
            full_response = "⚠️ **_Note: Information provided may be inaccurate._** \n\n\n"
            for chunk in result["answer"]:
                full_response += chunk
                time.sleep(0.02)
                message_placeholder.markdown(full_response + " ▌")
        st.button('Reset All Chat 🗑️', on_click=reset_conversation)

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
