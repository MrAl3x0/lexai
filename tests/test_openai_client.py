from unittest.mock import MagicMock, patch

import numpy as np

from lexai.services.openai_client import get_chat_completion, get_embedding


@patch("lexai.services.openai_client.client")
def test_get_embedding_success(mock_client):
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_client.embeddings.create.return_value = mock_response

    embedding = get_embedding("Test input")
    assert isinstance(embedding, np.ndarray)
    np.testing.assert_array_equal(embedding, np.array([0.1, 0.2, 0.3]))


@patch("lexai.services.openai_client.client")
def test_get_chat_completion_success(mock_client):
    mock_choice = MagicMock()
    mock_choice.message.content = "Here is your legal summary."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    response = get_chat_completion(
        role_description="You are a legal assistant.",
        top_matches_str="1. Case A\n2. Case B",
        query="What is the precedent for X?"
    )
    assert isinstance(response, str)
    assert response == "Here is your legal summary."
