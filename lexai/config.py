"""
Configuration constants for the LexAI application.

Includes application-wide text, dropdown options, and file paths.
"""

import os

EMBEDDING_MODEL = "text-embedding-ada-002"

LOCATION_INFO = {
    "Boulder": {
        "npz_file": os.getenv(
            "BOULDER_NPZ_FILE", "lexai/data/boulder_embeddings.npz"
        ),
        "role_description": (
            "You are an AI-powered legal assistant specializing in the jurisdiction "
            "of Boulder County, Colorado."
        ),
    },
    "Denver": {
        "npz_file": os.getenv("DENVER_NPZ_FILE", "lexai/data/denver_embeddings.npz"),
        "role_description": (
            "You are an AI-powered legal assistant specializing in the jurisdiction "
            "of Denver, Colorado."
        ),
    },
}

GPT4_MODEL = "gpt-4"
GPT4_TEMPERATURE = 0.7
GPT4_MAX_TOKENS = 120
GPT4_TOP_P = 1
GPT4_FREQUENCY_PENALTY = 0
GPT4_PRESENCE_PENALTY = 0

AI_ROLE_TEMPLATE = (
    "Your expertise lies in providing accurate and timely information on the laws and "
    "regulations specific to your jurisdiction. Your role is to assist individuals, "
    "including law enforcement officers, legal professionals, and the general public. "
    "You help them understand and apply legal standards within this jurisdiction. You "
    "are knowledgeable, precise, and always ready to offer guidance on legal matters. "
    "Your max_tokens is set to 120, so keep your response below that."
)
