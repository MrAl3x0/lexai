# lexai/services/openai_client.py
"""
OpenAI client interface for LexAI.

This module provides helper functions to interact with the OpenAI API,
including embedding generation and GPT-4 chat completions.
"""

import logging

import numpy as np
import openai
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
    OPENAI_API_KEY,
)

logger = logging.getLogger(__name__)

if not OPENAI_API_KEY:
    logger.error(
        "OPENAI_API_KEY environment variable is not set. Please configure it.")
    client = None
else:
    client = OpenAI(api_key=OPENAI_API_KEY)


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

    Raises
    ------
    openai.AuthenticationError
        If the OpenAI API key is not set.
    openai.OpenAIError
        For other errors during the OpenAI API call.
    """
    if client is None:
        raise openai.AuthenticationError(
            "OpenAI client not initialized: API key is missing.")

    try:
        response: Embedding = client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL
        )
        return np.array(response.data[0].embedding)
    except openai.AuthenticationError as e:
        logger.error(f"Authentication error during embedding generation: {e}")
        raise
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error during embedding generation: {e}")
        raise
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during embedding generation: {e}")
        raise


def get_chat_completion(
    system_prompt: str,
    context_summary: str,
    user_query: str,
) -> str:
    """
    Generates a GPT-4 response based on the user`s query and provided legal context.

    Parameters
    ----------
    system_prompt : str
        The system-level instructions for the AI's role and behavior.
        This typically includes the role description and general AI template.
    context_summary : str
        A stringified summary of relevant legal documents or search results,
        which provides factual basis for the AI's response.
    user_query : str
        The user's direct question or prompt.

    Returns
    -------
    str
        The assistant's generated response.

    Raises
    ------
    openai.AuthenticationError
        If the OpenAI API key is not set.
    openai.OpenAIError
        For other errors during the OpenAI API call.
    """
    if client is None:
        raise openai.AuthenticationError(
            "OpenAI client not initialized: API key is missing."
        )

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {
            "role": "user",
            "content": (
                "Context: " + context_summary.strip() + "\n\n" +
                "Query: " + user_query.strip()
            ),
        },
    ]

    try:
        response: ChatCompletion = client.chat.completions.create(
            model=GPT4_MODEL,
            messages=messages,
            temperature=GPT4_TEMPERATURE,
            max_tokens=GPT4_MAX_TOKENS,
            top_p=GPT4_TOP_P,
            frequency_penalty=GPT4_FREQUENCY_PENALTY,
            presence_penalty=GPT4_PRESENCE_PENALTY,
        )
        return response.choices[0].message.content.strip()
    except openai.AuthenticationError as e:
        logger.error(f"Authentication error during chat completion: {e}")
        raise
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error during chat completion: {e}")
        raise
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during chat completion: {e}")
        raise
