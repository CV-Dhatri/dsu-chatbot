import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DSU Student Helper",
    page_icon="🎓",
    layout="wide"
)

# --- API KEY SETUP ---
# (Ideally, put this in .streamlit/secrets.toml for production)
# For now, we keep it here for your local test.
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBGdlExfsWZciDHCiQfYzq8Qn8ZqxasCQI"  # <--- PASTE YOUR KEY HERE

# --- LOAD DATABASE (Cached for speed) ---
@st.cache_resource
def load_db():
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./db", embedding_function=embedding_function)
    return db

db = load_db()
retriever = db.as_retriever(search_kwargs={"k": 3})

# --- LOAD GEMINI MODEL ---
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.3)

# --- PROMPT TEMPLATE ---
template = """
You are a helpful, friendly assistant for Dayananda Sagar University (DSU).
Use the following context to answer the student's question.
If you don't know the answer, just say "I'm sorry, I don't have that info."

Context:
{context}

Question:
{question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

# --- RAG CHAIN ---
rag_chain = (
    {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
     "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def clear_chat_history():
    st.session_state.messages = []

# --- SIDEBAR UI ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/e/e5/Dayananda_Sagar_University_logo.png", width=150)
    st.title("🤖 DSU Bot")
    st.markdown("---")
    st.markdown("""
    **About this Bot:**
    This AI assistant uses **RAG (Retrieval-Augmented Generation)** to answer questions about:
    - 🏫 Course Details
    - 💰 Fee Structures
    - 📅 Admission Dates
    - 💼 Placements
    """)
    st.markdown("---")
    st.button("🗑️ Clear Chat History", on_click=clear_chat_history)
    st.markdown("---")
    st.caption("Powered by Gemini 1.5 Flash & LangChain")

# --- MAIN CHAT INTERFACE ---
st.title("🎓 Dayananda Sagar University Helper")
st.markdown("Welcome! Ask me anything about admissions, courses, or campus life.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if user_input := st.chat_input("Type your question here... (e.g., 'What is the fee for B.Tech?')"):
    # 1. Add user message to UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Checking university database..."):
            try:
                response = rag_chain.invoke(user_input)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")