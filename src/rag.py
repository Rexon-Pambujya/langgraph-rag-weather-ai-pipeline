import os
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from src.embeddings_store import get_qdrant_vectorstore
from src.config import Config

def build_rag_chain(model_name: str = "llama-3.1-8b-instant", temperature: float = 0.0):
    if Config.GROQ_API_KEY and not os.getenv("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY
    llm = ChatGroq(model_name=model_name, temperature=temperature)
    vectorstore = get_qdrant_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    prompt = PromptTemplate.from_template(
        "Use the following pieces of context to answer the question at the end. "
        "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n"
        "{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    return chain

def answer_question(question: str):
    chain = build_rag_chain()
    result = chain.invoke({"query": question})
    return result

