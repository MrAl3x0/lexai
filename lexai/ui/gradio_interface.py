import logging

import gradio as gr

from lexai.config import APP_DESCRIPTION, LOCATION_INFO
from lexai.core.match_engine import generate_matches

logger = logging.getLogger(__name__)


def build_interface():
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
                ["Is it legal to construct a rock cairn in an outdoor area?", "Boulder"],
                ["Can I legally possess a dog as a pet?", "Denver"],
                ["Am I allowed to go shirtless in public?", "Boulder"],
                ["What is the max legal height for a structure?", "Denver"],
                ["Is indoor furniture on porches allowed?", "Boulder"],
                ["Can I graze llamas on public land?", "Denver"],
            ],
            inputs=[query_input, location_input]
        )

    logger.info("LexAI interface built.")
    return iface
