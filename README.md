# 🌤️ LangGraph RAG + Weather App

This project demonstrates an **agentic AI pipeline** built using **LangChain**, **LangGraph**, and **LangSmith** — integrating **real-time weather fetching** via OpenWeatherMap API and **document-based question answering** (RAG) using **Qdrant vector database** and **Hugging Face embeddings**.

---

## 🚀 Features

- **Agentic Decision Pipeline** (via `LangGraph`):
  - Dynamically decides whether the query is about **weather** or **PDF content**.
- **Weather Agent**:
  - Fetches **real-time weather data** from **OpenWeatherMap API**.
- **RAG Agent**:
  - Uses **Retrieval-Augmented Generation (RAG)** to answer questions based on uploaded PDFs.
- **Vector Store**:
  - Stores embeddings in **Qdrant** for fast semantic search.
- **Embeddings**:
  - Uses free **Hugging Face sentence-transformer** model.
- **Evaluation**:
  - Integrated **LangSmith evaluation** pipeline for testing.
- **Streamlit UI**:
  - User-friendly interface for chatting and PDF ingestion.

---

## 🏗️ Project Structure

````
LangGraph-RAG-Weather/
│
├── src/
│ ├── config.py # Environment variable & configuration management
│ ├── weather.py # Fetches weather data from OpenWeatherMap
│ ├── rag.py # RAG pipeline with Groq LLM + Qdrant retriever
│ ├── embeddings_store.py # Qdrant client, collection setup, and upsert logic
│ ├── pdf_ingest.py # PDF loading and text chunking
│ ├── langgraph_pipeline.py # Core LangGraph pipeline: decision, weather, rag nodes
│ ├── langsmith_eval.py # LangSmith evaluation integration
│
├── app/
│ └── streamlit_app.py # Streamlit web interface
│
├── tests/
│ ├── test_decision_node.py # Tests LangGraph decision routing
│ ├── test_weather.py # Tests weather fetching
│ ├── test_rag.py # Tests RAG chain invocation
│
├── requirements.txt # Python dependencies
├── .env.example # Example environment variables
└── README.md # Documentation (this file)

```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/LangGraph-RAG-Weather.git
cd LangGraph-RAG-Weather

````

### 2️⃣ Create and Activate Virtual Environment

```
python -m venv venv
source venv/bin/activate  # on macOS/Linux
venv\Scripts\activate     # on Windows

```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a .env file in the project root (or rename .env.example) with the following:

```
OPEN_WEATHER_API =
GROQ_API =
QDRANT_URL =
QUADRANT_API =
LANGSMITH_API =
```

## 🧠 Running the Application

### 1️⃣ Start Qdrant (Vector Database)

Run Qdrant using Docker (recommended):

docker run -p 6333:6333 qdrant/qdrant

### 2️⃣ Launch the Streamlit App

streamlit run app/streamlit_app.py

Then open your browser at http://localhost:8501

##💬 How It Works
###🧩 1. LangGraph Decision Logic

The pipeline first analyzes the user query:

If it contains words like weather, temperature, forecast, it triggers the weather agent.

Otherwise, it invokes the PDF RAG agent.

###🌦️ 2. Weather Agent

Calls fetch_weather_by_city() from weather.py.

Uses OpenWeatherMap API to retrieve:

Temperature

Humidity

Wind Speed

Condition Description

### 📄 3. PDF RAG Agent

Loads uploaded PDF using PyPDFLoader.

Splits it into chunks using RecursiveCharacterTextSplitter.

Generates embeddings with HuggingFaceEmbeddings.

Stores in Qdrant.

Uses Groq (Llama 3.1-8B) via ChatGroq for contextual QA retrieval.

### 🧠 4. LangSmith Evaluation (Optional)

The langsmith_eval.py script allows you to evaluate model performance using predefined examples.

##🧪 Running Tests

Unit tests are included under tests/.

Run them using:

```
pytest -v
```

Example tests:

test_decision_node.py → Validates agent routing

test_weather.py → Mocks API responses

test_rag.py → Tests RAG chain and output

## 📚 Key Technologies

Category Library / Service
Agentic Flow LangGraph
Orchestration LangChain
Evaluation LangSmith
Vector DB Qdrant
Embeddings Hugging Face Sentence Transformers
LLM Groq (Llama 3.1-8B)
Frontend Streamlit
Environment dotenv
Testing pytest

## 🧩 Example Queries

Weather:

“What’s the weather in Mumbai right now?”

PDF RAG:

“Summarize the introduction section of the uploaded document.”

🧰 Troubleshooting

Qdrant not reachable?
Ensure Docker container is running at http://localhost:6333.

Invalid API Key?
Double-check your .env values and restart the app.

Embedding model not found?
Install sentence-transformers manually:

```
pip install sentence-transformers
```

👨‍💻 Author

Rexon David Pambujya
📍 Mumbai, India
📧 rexonpambujya2001@gmail.com
