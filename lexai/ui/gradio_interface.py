""""
Gradio interface builder for the LexAI application.

This module defines the UI using Gradio and connects it to
the LexAI service layer.
"""

import logging

import gradio as gr

from lexai.config import LOCATION_INFO
from lexai.services.lexai_service import LexAIService

logger = logging.getLogger(__name__)

APP_DESCRIPTION = (
    "LexAI is an AI-powered legal assistant that provides fast, "
    "jurisdiction-specific legal guidance. This proof of concept "
    "demonstrates how large language models like GPT-4, when combined "
    "with structured legal data, can help users understand local laws "
    "in plain language. LexAI is designed to assist with everyday "
    "legal questions such as housing regulations, zoning restrictions, "
    "and public ordinances by delivering clear, localized answers. "
    "By making legal information more accessible, LexAI aims to empower "
    "individuals, property owners, and civic professionals to make informed "
    "decisions without needing to navigate dense legal texts or complex codes. "
    "As the platform evolves, it will incorporate more jurisdictions and topics, "
    "while continuously reflecting the most up-to-date and accurate "
    "legal information available."
)

DISCLAIMER_TEXT = (
    "<div style='text-align: center; font-size: 0.9em; color: gray; margin-top: 1em;'>"
    "This tool is for informational purposes only. Results may be inaccurate. "
    "Consult a licensed attorney for legal advice. Check any references provided."
    "</div>"
)

EXAMPLE_QUERIES = [
    ["Can I build a backyard fire pit at my home?", "Denver"],
    ["What permits are required to build an accessory dwelling unit (ADU)?", "Boulder"],
    ["Are there restrictions on short-term rentals (e.g., Airbnb)?", "Denver"],
    ["What are the setback requirements for residential construction?", "Boulder"],
    ["Is a fence over 6 feet allowed without a permit?", "Denver"],
    ["Can I run a home-based business from my residence?", "Boulder"],
]


def build_interface():
    """
    Constructs and returns the Gradio Blocks interface for LexAI.

    This includes input fields for the user's legal query and location,
    a response display area, and sample example queries.
    """
    with gr.Blocks(title="LexAI") as iface:
        gr.Markdown("<div style='text-align: center'><h1>LexAI</h1></div>")
        gr.Markdown(APP_DESCRIPTION)

        with gr.Row():
            with gr.Column(scale=2):
                query_input = gr.Textbox(
                    label="Query",
                    lines=3,
                    placeholder="Enter your legal question here..."
                )
                location_input = gr.Dropdown(
                    choices=list(LOCATION_INFO.keys()),
                    label="Location",
                    value=list(LOCATION_INFO.keys())[0]
                )
                with gr.Row():
                    clear_btn = gr.Button("Clear", variant="secondary")
                    submit_btn = gr.Button("Submit", variant="primary")

            with gr.Column(scale=3):
                response_output = gr.Markdown(
                    value="Response will appear here.",
                    show_label=False
                )
                gr.Button("Flag", variant="secondary")

        def handle_submit(query, location):
            return gr.update(value=LexAIService.handle_query(query, location))

        def handle_clear():
            return gr.update(value="Response will appear here.")

        submit_btn.click(
            fn=handle_submit,
            inputs=[query_input, location_input],
            outputs=[response_output]
        )
        clear_btn.click(
            fn=handle_clear,
            outputs=[response_output]
        )

        gr.Examples(
            examples=EXAMPLE_QUERIES,
            inputs=[query_input, location_input]
        )

        gr.Markdown(DISCLAIMER_TEXT)

    logger.info("LexAI interface built.")
    return iface
