"""
Gradio interface builder for the LexAI application.

This module defines the UI using Gradio and connects it to
the LexAI service layer.
"""

import logging

import gradio as gr

from lexai.config import LOCATION_INFO
from lexai.services.lexai_service import LexAIService

logger = logging.getLogger(__name__)

APP_DESCRIPTION = """
LexAI is an AI-powered legal assistant that provides jurisdiction-specific guidance.
It combines GPT-4 with semantic search to retrieve relevant legal information quickly.
"""

DISCLAIMER_TEXT = """
<div style='text-align: center; font-size: 0.9em; color: gray; margin-top: 1em;'>
Results may be inaccurate. Always verify with a legal professional.
</div>
"""

EXAMPLE_QUERIES = [
    ["Is building a rock cairn outdoors allowed by law?", "Boulder"],
    ["Can I legally possess a dog as a pet?", "Denver"],
    ["Am I allowed to go shirtless in public?", "Boulder"],
    ["What is the max legal height for a structure?", "Denver"],
    ["Is indoor furniture on porches allowed?", "Boulder"],
    ["Can I graze llamas on public land?", "Denver"],
]


def build_interface():
    """
    Constructs and returns the Gradio Blocks interface for LexAI.

    This includes input fields for the user's legal query and location,
    a response display area, and sample example queries.
    """
    with gr.Blocks(title="LexAI") as iface:
        gr.HTML("<h1 style='text-align: center;'>LexAI</h1>")
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
                response_output = gr.HTML(
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

        gr.HTML(DISCLAIMER_TEXT)

    logger.info("LexAI interface built.")
    return iface
