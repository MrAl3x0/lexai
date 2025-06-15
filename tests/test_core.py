# ==============================================================================
# tests/test_core.py
#
# Unit tests for the core logic of the lexai application.
# ==============================================================================

import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch

# To make the test runner find the `lexai_app` package, we might need to adjust the path.
# This is a common pattern in testing.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexai_app.core import generate_matches

# --- Test Fixtures ---

@pytest.fixture
def mock_openai_client(mocker):
    """Mocks the OpenAI client and its methods."""
    # Mock the client instance
    mock_client = MagicMock()

    # Mock the embeddings response
    mock_embedding = MagicMock()
    mock_embedding.embedding = np.random.rand(1536).tolist() # Simulate a 1536-dim embedding
    mock_embeddings_response = MagicMock()
    mock_embeddings_response.data = [mock_embedding]
    mock_client.embeddings.create.return_value = mock_embeddings_response

    # Mock the chat completion response
    mock_chat_choice = MagicMock()
    mock_chat_choice.message.content = "This is a mocked legal response."
    mock_chat_response = MagicMock()
    mock_chat_response.choices = [mock_chat_choice]
    mock_client.chat.completions.create.return_value = mock_chat_response

    # Use mocker to patch the OpenAI() call in the core module
    return mocker.patch('lexai_app.core.client', mock_client)


@pytest.fixture
def mock_numpy_load(mocker):
    """Mocks np.load to return fake data instead of reading from a file."""
    # Create fake data that simulates what's in the .npz file
    fake_embeddings = np.random.rand(5, 1536)
    fake_data = {
        'embeddings': fake_embeddings,
        'urls': ['http://fake.url/1', 'http://fake.url/2', 'http://fake.url/3', 'http://fake.url/4', 'http://fake.url/5'],
        'titles': ['Fake Title 1', 'Fake Title 2', 'Fake Title 3', 'Fake Title 4', 'Fake Title 5'],
        'subtitles': ['Fake Subtitle 1', 'Fake Subtitle 2', 'Fake Subtitle 3', 'Fake Subtitle 4', 'Fake Subtitle 5'],
        'contents': ['Fake content 1.', 'Fake content 2.', 'Fake content 3.', 'Fake content 4.', 'Fake content 5.']
    }
    return mocker.patch('numpy.load', return_value=fake_data)


# --- Test Cases ---

def test_generate_matches_success(mock_openai_client, mock_numpy_load):
    """
    Tests the happy path of the generate_matches function.
    Ensures that with valid inputs and mocked dependencies, it returns a valid HTML string.
    """
    query = "What is the law on public parks?"
    location = "Boulder"

    result = generate_matches(query, location)

    # Assert that the function was called with the correct arguments
    mock_openai_client.embeddings.create.assert_called_with(input=query, model="text-embedding-ada-002")
    mock_numpy_load.assert_called_with("embeddings/boulder_embeddings.npz", allow_pickle=True)

    # Assert that the output is a string and contains expected HTML fragments
    assert isinstance(result, str)
    assert "<p><strong>Response:</strong></p>" in result
    assert "This is a mocked legal response." in result
    assert "<p><strong>References:</strong></p>" in result
    assert '<li><a href="http://fake.url/' in result # Check if reference links are created


def test_generate_matches_invalid_location():
    """
    Tests that the function handles an invalid location gracefully.
    """
    query = "Test query"
    location = "InvalidCity"

    result = generate_matches(query, location)

    # The function should catch the ValueError and return an error HTML
    assert "Error:" in result
    assert "No data found for the selected location" in result


def test_generate_matches_openai_api_error(mock_openai_client, mock_numpy_load):
    """
    Tests that the function handles an API error from OpenAI gracefully.
    """
    # Configure the mock to raise an exception when called
    mock_openai_client.chat.completions.create.side_effect = Exception("OpenAI API is down")

    query = "Test query"
    location = "Denver"

    result = generate_matches(query, location)

    # The function should catch the generic exception and return an error HTML
    assert "Error:" in result
    assert "An issue occurred while processing your request" in result
    assert "OpenAI API is down" in result # The specific error message should be in the details