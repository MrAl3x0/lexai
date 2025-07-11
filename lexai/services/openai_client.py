from openai import OpenAI
import numpy as np
import os
from lexai.config import (
    MODEL_ENGINE,
    GPT4_MODEL,
    GPT4_TEMPERATURE,
    GPT4_MAX_TOKENS,
    GPT4_TOP_P,
    GPT4_FREQUENCY_PENALTY,
    GPT4_PRESENCE_PENALTY,
)

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


def get_embedding(text: str) -> np.ndarray:
    """
    Generates an embedding for the given text using OpenAI's text-embedding model.

    The OpenAI API key is loaded from the OPENAI_API_KEY environment variable
    to authenticate the request.

    Parameters
    ----------
    text : str
        The input text to generate an embedding for.

    Returns
    -------
    np.ndarray
        A NumPy array representing the embedding of the input text.

    Raises
    ------
    openai.AuthenticationError
        If the OPENAI_API_KEY environment variable is not set or is invalid.
    openai.OpenAIError
        If there's another issue with the OpenAI API call, such as network problems.
    """
    response = client.embeddings.create(input=text, model=MODEL_ENGINE)
    return np.array(response.data[0].embedding)


def get_chat_completion(role_description: str, top_matches_str: str, query: str) -> str:
    """
    Generates a chat completion response using OpenAI's GPT-4 model.

    The OpenAI API key is loaded from the OPENAI_API_KEY environment variable
    to authenticate the request. The function constructs a conversation history
    with system and user roles to provide context to the language model.

    Parameters
    ----------
    role_description : str
        The system role description for the AI assistant, defining its persona
        and limitations.
    top_matches_str : str
        A string representation of the top legal information matches. This is
        provided as system context to help the AI formulate relevant responses.
    query : str
        The user's direct query or question.

    Returns
    -------
    str
        The AI-generated response message from the chat completion.

    Raises
    ------
    openai.AuthenticationError
        If the OPENAI_API_KEY environment variable is not set or is invalid.
    openai.OpenAIError
        If there's an issue with the OpenAI API call, such as rate limiting,
        or other API-related errors.
    """

    response = client.chat.completions.create(model=GPT4_MODEL,
                                              messages=[
                                                  {"role": "system",
                                                      "content": role_description.strip()},
                                                  {"role": "system",
                                                      "content": top_matches_str},
                                                  {"role": "user",
                                                      "content": query},
                                                  {"role": "assistant",
                                                      "content": ""},
                                              ],
                                              temperature=GPT4_TEMPERATURE,
                                              max_tokens=GPT4_MAX_TOKENS,
                                              top_p=GPT4_TOP_P,
                                              frequency_penalty=GPT4_FREQUENCY_PENALTY,
                                              presence_penalty=GPT4_PRESENCE_PENALTY)

    return response.choices[0].message.content.strip()
