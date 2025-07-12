"""
OpenAI client interface for LexAI.

This module provides helper functions to interact with the OpenAI API,
including embedding generation and GPT-4 chat completions.
"""

import os

import numpy as np
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.embedding import Embedding

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
    Generates a numerical embedding for the provided text using OpenAI's model.

    Parameters
    ----------
    text : str
        The input text to embed.

    Returns
    -------
    np.ndarray
        The embedding vector as a NumPy array.
    """
    response: Embedding = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return np.array(response.data[0].embedding)


def get_chat_completion(
    role_description: str,
    context_summary: str,
    query: str,
) -> str:
    """
    Generates a GPT-4 response based on the user’s query and legal context.

    Parameters
    ----------
    role_description : str
        Describes the assistant's role and intended tone or expertise.
    context_summary : str
        A stringified summary of relevant legal documents or search results.
    query : str
        The user's legal question.

    Returns
    -------
    str
        The assistant's response.
    """
    response: ChatCompletion = client.chat.completions.create(
        model=GPT4_MODEL,
        messages=[
            {"role": "system", "content": role_description.strip()},
            {"role": "system", "content": context_summary.strip()},
            {"role": "user", "content": query.strip()},
            {"role": "assistant", "content": ""},
        ],
        temperature=GPT4_TEMPERATURE,
        max_tokens=GPT4_MAX_TOKENS,
        top_p=GPT4_TOP_P,
        frequency_penalty=GPT4_FREQUENCY_PENALTY,
        presence_penalty=GPT4_PRESENCE_PENALTY,
    )
    return response.choices[0].message.content.strip()
