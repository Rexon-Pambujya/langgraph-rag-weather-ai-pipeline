import pytest
from src.langgraph_pipeline import desicion_node

def test_desicion_node_weather():
    state = {'input': "What's the weather in New York?"}
    result = desicion_node(state, None, None)
    assert result['action'] == 'weather'

def test_desicion_node_pdf_rag():
    state = {'input': "Tell me about the document's main points."}
    result = desicion_node(state, None, None)
    assert result['action'] == 'pdf_rag'