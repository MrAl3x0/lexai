import logging
import os
import openai
from dotenv import load_dotenv

from lexai.config import LOCATION_INFO, AI_ROLE_TEMPLATE
from lexai.core.data_loader import load_embeddings
from lexai.core.matcher import find_top_matches
from lexai.services.openai_client import get_embedding, get_chat_completion

logger = logging.getLogger(__name__)

if not os.getenv("OPENAI_API_KEY"):
    load_dotenv(override=True)


def generate_matches(query: str, location: str) -> str:
    try:
        location_data = LOCATION_INFO.get(location)
        if not location_data:
            raise ValueError(f"Invalid location: '{location}'")

        query_embedding = get_embedding(query)
        embeddings, metadata_df = load_embeddings(location_data["npz_file"])

        if embeddings.shape[0] != len(metadata_df):
            raise ValueError(
                "Mismatch between number of embeddings and metadata entries")

        top_matches = find_top_matches(
            query_embedding, embeddings, metadata_df)
        system_prompt = f"{location_data['role_description']}\n{AI_ROLE_TEMPLATE}"
        ai_response = get_chat_completion(
            system_prompt, str(top_matches), query)

        response_html = f"<p><strong>Response:</strong></p><p>{ai_response}</p>"
        reference_html = "<p><strong>References:</strong></p><ul>"

        for match in top_matches:
            url = match.get("url", "#")
            title = match.get("title", "Untitled")
            subtitle = match.get("subtitle", "")
            reference_html += f'<li><a href="{url}" target="_blank">{title}: {subtitle}</a></li>'

        reference_html += "</ul>"
        return response_html + reference_html

    except openai.AuthenticationError:
        logger.error("Invalid OpenAI API key.")
        return "<p style='color: #d9534f;'><strong>Error:</strong> Invalid OpenAI API key.</p>"
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return f"<p style='color: #d9534f;'><strong>OpenAI Error:</strong> {e}</p>"
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return f"<p style='color: #d9534f;'><strong>File Error:</strong> {e}</p>"
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return f"<p><strong>Input Error:</strong> {e}</p>"
    except Exception as e:
        logger.exception("Unhandled exception during generate_matches.")
        return f"<p style='color: #d9534f;'><strong>Unexpected error:</strong> {e}</p>"
