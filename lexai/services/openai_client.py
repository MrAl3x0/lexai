import os

import numpy as np
from openai import OpenAI

from lexai.config import (
    EMBEDDING_MODEL,
    GPT4_FREQUENCY_PENALTY,
    GPT4_MAX_TOKENS,
    GPT4_MODEL,
    GPT4_PRESENCE_PENALTY,
    GPT4_TEMPERATURE,
    GPT4_TOP_P,
)

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


def get_embedding(text: str) -> np.ndarray:
    """
    Generates an embedding for the given text using OpenAI's embedding model.

    Parameters
    ----------
    text : str
        The input text to generate an embedding for.

    Returns
    -------
    np.ndarray
        A NumPy array representing the embedding.

    Raises
    ------
    openai.AuthenticationError
        If the API key is not set or invalid.
    openai.OpenAIError
        For other API-related issues.
    """
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return np.array(response.data[0].embedding)


def get_chat_completion(
    role_description: str,
    top_matches_str: str,
    query: str,
) -> str:
    """
    Generates a chat completion using OpenAI's GPT-4 model.

    Parameters
    ----------
    role_description : str
        Description of the assistant's persona and context.
    top_matches_str : str
        Summary of top legal matches used to guide the assistant.
    query : str
        The user’s legal query.

    Returns
    -------
    str
        The AI-generated response.

    Raises
    ------
    openai.AuthenticationError
        If the API key is not set or invalid.
    openai.OpenAIError
        For other API-related issues.
    """
    response = client.chat.completions.create(
        model=GPT4_MODEL,
        messages=[
            {"role": "system", "content": role_description.strip()},
            {"role": "system", "content": top_matches_str},
            {"role": "user", "content": query},
            {"role": "assistant", "content": ""},
        ],
        temperature=GPT4_TEMPERATURE,
        max_tokens=GPT4_MAX_TOKENS,
        top_p=GPT4_TOP_P,
        frequency_penalty=GPT4_FREQUENCY_PENALTY,
        presence_penalty=GPT4_PRESENCE_PENALTY,
    )

    return response.choices[0].message.content.strip()
