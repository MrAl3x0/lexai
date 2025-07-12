import logging
from html import escape

import openai

from lexai.config import AI_ROLE_TEMPLATE, LOCATION_INFO
from lexai.core.data_loader import load_embeddings
from lexai.core.matcher import find_top_matches
from lexai.services.openai_client import get_chat_completion, get_embedding

logger = logging.getLogger(__name__)


def generate_matches(query: str, location: str) -> str:
    if location not in LOCATION_INFO:
        logger.error(f"Invalid location: {location}")
        return (
            "<p><strong>Input Error:</strong> "
            f"Invalid location: '{escape(location)}'</p>"
        )

    try:
        query_embedding = get_embedding(query)
        location_data = LOCATION_INFO[location]
        embeddings, metadata = load_embeddings(location_data["npz_file"])

        if embeddings.shape[0] != len(metadata):
            raise ValueError(
                "Mismatch between number of embeddings and metadata entries"
            )

        top_matches = find_top_matches(query_embedding, embeddings, metadata)

        system_prompt = (
            f"{location_data['role_description']}\n{AI_ROLE_TEMPLATE}"
        )
        ai_response = get_chat_completion(
            system_prompt, str(top_matches), query)

        response_html = (
            "<p><strong>Response:</strong></p>"
            f"<p>{escape(ai_response)}</p>"
        )
        reference_html = "<p><strong>References:</strong></p><ul>"

        for match in top_matches:
            url = escape(match["url"])
            title = escape(match["title"])
            subtitle = escape(match["subtitle"])
            reference_html += (
                f'<li><a href="{url}" target="_blank">'
                f"{title}: {subtitle}</a></li>"
            )

        reference_html += "</ul>"
        return response_html + reference_html

    except openai.AuthenticationError:
        logger.error("Invalid OpenAI API key.")
        return (
            "<p style='color: #d9534f;'><strong>Error:</strong> "
            "Invalid OpenAI API key.</p>"
        )
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return (
            "<p style='color: #d9534f;'><strong>OpenAI Error:</strong> "
            f"{escape(str(e))}</p>"
        )
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return (
            "<p style='color: #d9534f;'><strong>File Error:</strong> "
            f"{escape(str(e))}</p>"
        )
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return (
            "<p><strong>Input Error:</strong> "
            f"{escape(str(e))}</p>"
        )
    except Exception as e:
        logger.exception("Unhandled exception during generate_matches.")
        return (
            "<p style='color: #d9534f;'><strong>Unexpected error:</strong> "
            f"{escape(str(e))}</p>"
        )
