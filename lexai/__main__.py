import logging
import os
import openai
import gradio as gr
from dotenv import load_dotenv

if not os.getenv("OPENAI_API_KEY"):
    load_dotenv(override=True)

from lexai.config import (
    LOCATION_INFO,
    APP_DESCRIPTION,
    AI_ROLE_TEMPLATE,
)

from lexai.core.data_loader import load_embeddings_data
from lexai.core.matcher import find_top_matches
from lexai.services.openai_client import get_embedding, get_chat_completion

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_matches(query: str, location: str) -> str:
    """
    Generate legal information matches based on the user's query and location.

    This function orchestrates the process of generating legal information matches
    using OpenAI's models and local embedding data. It returns an HTML response
    containing the AI-generated response and references to relevant legal information.

    Parameters
    ----------
    query : str
        The user's query for legal information.
    location : str
        The location for which the user is seeking legal information.
        Possible values are "Boulder" and "Denver".

    Returns
    -------
    str
        An HTML response containing the AI-generated response and references
        to relevant legal information. In case of an error, an error message
        is returned in HTML format.
    """
    try:
        logging.info(f"Generating embedding for query: '{query}'")
        query_embedding = get_embedding(query)

        location_data = LOCATION_INFO.get(location)
        if not location_data:
            logging.error(f"No data found for location '{location}'.")
            raise ValueError(
                f"No data found for location '{location}'. Please select a valid location."
            )

        npz_file = location_data["npz_file"]
        role_description_base = location_data["role_description"]

        logging.info(f"Loading embeddings data from: {npz_file}")
        embeddings, jurisdiction_data = load_embeddings_data(npz_file)

        logging.info("Finding top matches...")
        top_matches = find_top_matches(
            query_embedding, embeddings, jurisdiction_data, num_matches=3
        )

        full_ai_role = f"{role_description_base}\n{AI_ROLE_TEMPLATE}"
        top_matches_str = str(
            top_matches
        )

        logging.info("Getting chat completion from OpenAI...")
        ai_message = get_chat_completion(full_ai_role, top_matches_str, query)

        html_response = "<p><strong>Response:</strong></p><p>" + ai_message + "</p>"
        html_references = "<p><strong>References:</strong></p><ul>"
        for match in top_matches:
            url = match.get("url", "#")
            title = match.get("title", "No Title")
            subtitle = match.get("subtitle", "No Subtitle")
            html_references += (
                f'<li><a href="{url}" target="_blank">{title}: {subtitle}</a></li>'
            )
        html_references += "</ul>"

        logging.info("Successfully generated response and references.")
        return html_response + html_references

    except openai.AuthenticationError:
        logging.error("OpenAI Authentication Error: Invalid API key provided.")
        return """<p style="font-family: Arial, sans-serif; font-size: 16px; color: #d9534f;">
    <strong>Error:</strong> Invalid OpenAI API key. Please ensure your `OPENAI_API_KEY` environment variable is correctly set.
</p>"""
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API Error: {e}")
        return f"""<p style="font-family: Arial, sans-serif; font-size: 16px; color: #d9534f;">
    <strong>OpenAI API Error:</strong> {str(e)}
</p>"""
    except FileNotFoundError as e:
        logging.error(f"File Not Found Error: {e}")
        return f"""<p style="font-family: Arial, sans-serif; font-size: 16px; color: #d9534f;">
    <strong>File Error:</strong> {str(e)} Please ensure embedding files are correctly placed.
</p>"""
    except ValueError as e:
        logging.error(f"Value Error: {e}")
        return f"""<p style="font-family: Arial, sans-serif; font-size: 16px; color: #333;">
    <strong>Input Error:</strong> {str(e)}
</p>"""
    except Exception as e:
        logging.exception(
            "An unexpected error occurred during generate_matches.")
        return f"""<p style="font-family: Arial, sans-serif; font-size: 16px; color: #d9534f;">
    <strong>Notice:</strong> An unexpected error occurred while processing your request. Please see the details below:
    <br>{str(e)}
</p>"""


with gr.Blocks(title="LexAI") as iface:
    gr.HTML("<h1 style='text-align: center;'>LexAI</h1>")
    gr.Markdown(APP_DESCRIPTION)

    with gr.Row():
        with gr.Column(scale=2):
            query_input = gr.Textbox(
                label="Query", lines=3, placeholder="Enter your legal question here...")
            location_input = gr.Dropdown(choices=list(
                LOCATION_INFO.keys()), label="Location", value=list(LOCATION_INFO.keys())[0])
            with gr.Row():
                clear_btn = gr.Button("Clear", variant="secondary")
                submit_btn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=3):
            response_output = gr.HTML(
                value="<p><strong>Response:</strong></p>",
                show_label=False
            )
            gr.Button("Flag", variant="secondary")

    def handle_submit(query, location):
        return gr.update(value=generate_matches(query, location))

    def handle_clear():
        return gr.update(value="<p><strong>Response:</strong></p>")

    submit_btn.click(fn=handle_submit, inputs=[
                     query_input, location_input], outputs=[response_output])
    clear_btn.click(fn=handle_clear, outputs=[response_output])

    gr.Examples(
        examples=[
            ["Is it legal for me to use rocks to construct a cairn in an outdoor area?", "Boulder"],
            ["Is it legal to possess a dog and take ownership of it as a pet?", "Denver"],
            ["Am I allowed to go shirtless in public spaces?", "Boulder"],
            ["What is the maximum height I can legally build a structure?", "Denver"],
            ["Is it legal to place indoor furniture on an outdoor porch?", "Boulder"],
            ["Can I legally graze livestock like llamas on public land?", "Denver"],
        ],
        inputs=[query_input, location_input]
    )

if __name__ == "__main__":
    logging.info("Starting LexAI Gradio application...")
    iface.launch()
