import pytest
from unittest.mock import patch
from src.rag import answer_question


@patch('src.rag.build_rag_chain')
def test_rag_chain_called(mock_build_chain):
    class FakeChain:
        def __call__(self, args):
            return {"result": "Answer from PDF.", "source_documents": []}
    
    mock_build_chain.return_value = FakeChain()
    out = answer_question("What wrote X?")
    assert "Answer from PDF" in out.get("result")
