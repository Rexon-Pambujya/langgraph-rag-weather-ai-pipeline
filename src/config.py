import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenWeather
    API_KEY = os.getenv('API_KEY') or os.getenv('OPEN_WEATHER_API')
    BASE_URL = os.getenv('BASE_URL', 'http://api.openweathermap.org/data/2.5/weather')
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'London')
    UNITS = os.getenv('UNITS', 'metric')  # Options: 'metric', 'imperial', 'standard'
    LANGUAGE = os.getenv('LANGUAGE', 'en')  # Language code for the API response
    CACHE_EXPIRY = int(os.getenv('CACHE_EXPIRY', 600))  # Cache expiry time in seconds
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Logging level

    # Embeddings / Vector store
    EMBEDDINGS_MODEL = os.getenv('EMBEDDINGS_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY') or os.getenv('QUADRANT_API', '')
    QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME', 'langweather_docs')

    # LangSmith
    LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY') or os.getenv('LANGSMITH_API', '')
    LANGSMITH_TRACING = os.getenv('LANGSMITH_TRACING', 'false').lower() == 'true'
    LANGSMITH_ENDPOINT = os.getenv('LANGSMITH_ENDPOINT', 'https://api.smith.langchain.com')
    
    # LLM Providers (used by underlying SDKs)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY') or os.getenv('GROQ_API', '')