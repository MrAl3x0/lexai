"""
Entry point for launching the LexAI application.

This script configures logging and starts the Gradio interface.
"""

import logging

from lexai.ui.gradio_interface import build_interface


def run_lexai_app():
    """
    Configures logging and launches the LexAI Gradio interface.
    """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.info("Launching LexAI...")
    iface = build_interface()
    iface.launch()


if __name__ == "__main__":
    run_lexai_app()
