# ==============================================================================
# lexai: Application Entry Point
#
# This script defines and launches the Gradio web interface, connecting the
# user interface to the core logic of the application.
# ==============================================================================

import gradio as gr
from .core import generate_matches, LOCATION_INFO

# --- Gradio User Interface ---

DESCRIPTION = """
**lexai: AI-Powered Legal Research Assistant**

lexai is an AI legal assistant designed to deliver accurate legal information based on your queries and selected jurisdiction.
This demo serves as a proof of concept, using OpenAI's GPT-4 and text-embedding models to provide AI-generated responses and references.

**How to Use:**
1.  Enter your legal question in the "Query" box.
2.  Select the relevant "Location" from the dropdown.
3.  Click "Submit" to get your response.

**Note:** This application requires a valid OpenAI API key with access to GPT-4, which must be set as an `OPENAI_API_KEY` environment variable.
"""

# Define the Gradio interface.
iface = gr.Interface(
    fn=generate_matches,
    inputs=[
        gr.Textbox(label="Query", placeholder="e.g., Is it legal to build a rock cairn in a park?"),
        gr.Dropdown(choices=list(LOCATION_INFO.keys()), label="Location")
    ],
    outputs=gr.HTML(),
    title="lexai Demo",
    description=DESCRIPTION,
    examples=[
        ["What are the rules for operating a short-term rental like an Airbnb?", "Boulder, CO"],
        ["What are the local regulations regarding noise complaints in residential areas?", "Denver, CO"],
        ["What permits are required to operate a food truck?", "Denver, CO"],
        ["Are there specific leash laws for dogs in open space parks?", "Boulder, CO"],
    ],
    allow_flagging="never"
)

# --- Application Launch ---

def main():
    """Launches the Gradio web server."""
    iface.launch()

if __name__ == "__main__":
    main()