import os
import sys
import streamlit as st

# Ensure project root is on sys.path so `import src...` works
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.langgraph_pipeline import run_pipeline
from src.embeddings_store import upsert_documents_to_qdrant
from src.pdf_ingest import load_and_split_pdf
from src.config import Config


st.set_page_config(page_title="LangGraph RAG + Weather App", layout="wide")
st.title("LangGraph RAG + Weather App")
st.markdown("Type a question about the weather or upload a PDF to get started.")


# Sidebar for PDF upload and ingestion
st.sidebar.header("Upload PDF for RAG")
uploaded_pdf = st.sidebar.file_uploader("Choose a PDF", type=["pdf"], accept_multiple_files=False)
if st.sidebar.button("Ingest PDF"):
    if not uploaded_pdf:
        st.sidebar.error("Please upload a PDF first.")
    else:
        # Save uploaded file to a temporary location for the loader
        temp_dir = os.path.join(os.getcwd(), ".tmp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_pdf.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        try:
            docs = load_and_split_pdf(temp_path)
            upsert_documents_to_qdrant(docs)
            st.sidebar.success(f"Ingested {len(docs)} documents from {uploaded_pdf.name}")
        except ValueError as e:
            st.sidebar.error(str(e))
        except Exception as e:
            st.sidebar.error(f"Failed to ingest PDF: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

def send_message(user_text:str):
    st.session_state.messages.append({"role": "user","text": user_text})
    with st.spinner("Processing..."):
        response = run_pipeline(user_text)
        answer = response.get("final", "Sorry, I couldn't process your request.")
        st.session_state.messages.append({"role": "assistant", "text": answer})

# User input
user_input = st.text_input("Enter your question about the weather or PDF content:", key="input")
if st.button("Send"):
    send_message(user_input)

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Assistant:** {msg['text']}")

    