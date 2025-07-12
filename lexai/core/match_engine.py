"""
Core logic for generating legal responses based on user queries and location.

This module embeds the matching engine that performs semantic search using vector
similarity and invokes GPT-4 to generate responses. It returns structured data
for rendering in the UI.
"""

import logging
from html import escape

import openai

from lexai.config import AI_ROLE_TEMPLATE, LOCATION_INFO
from lexai.core.data_loader import load_embeddings
from lexai.core.matcher import find_top_matches
from lexai.services.openai_client import get_chat_completion, get_embedding

logger = logging.getLogger(__name__)


def generate_matches(query: str, location: str) -> dict:
    """
    Generate a legal response and references for a given query and location.

    Returns a dictionary with keys:
        - "response": the GPT-generated answer string
        - "references": list of dicts with keys: url, title, subtitle
        - "error_html": optional HTML string if an error occurred
    """
    if location not in LOCATION_INFO:
        logger.error(f"Invalid location: {location}")
        return {
            "error_html": (
                "<p><strong>Input Error:</strong> "
                f"Invalid location: '{escape(location)}'.</p>"
            )
        }

    try:
        query_embedding = get_embedding(query)
        location_data = LOCATION_INFO[location]
        embeddings, metadata = load_embeddings(location_data["npz_file"])

        if embeddings.shape[0] != len(metadata):
            raise ValueError(
                "Mismatch between number of embeddings and metadata entries.")

        top_matches = find_top_matches(query_embedding, embeddings, metadata)
        system_prompt = f"{location_data['role_description']}\n{AI_ROLE_TEMPLATE}"
        match_summary = str(top_matches)
        ai_response = get_chat_completion(system_prompt, match_summary, query)

        return {
            "response": ai_response,
            "matches": top_matches
        }

    except openai.AuthenticationError:
        logger.error("Invalid OpenAI API key.")
        return {
            "error_html": (
                "<p style='color: #d9534f;'><strong>Error:</strong> "
                "Invalid OpenAI API key.</p>"
            )
        }
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return {
            "error_html": (
                "<p style='color: #d9534f;'><strong>OpenAI Error:</strong> "
                f"{escape(str(e))}</p>"
            )
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return {
            "error_html": (
                "<p style='color: #d9534f;'><strong>File Error:</strong> "
                f"{escape(str(e))}</p>"
            )
        }
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return {
            "error_html": (
                "<p><strong>Input Error:</strong> "
                f"{escape(str(e))}</p>"
            )
        }
    except Exception as e:
        logger.exception("Unhandled exception during generate_matches.")
        return {
            "error_html": (
                "<p style='color: #d9534f;'><strong>Unexpected error:</strong> "
                f"{escape(str(e))}</p>"
            )
        }
