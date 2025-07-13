import logging

from lexai.ui.gradio_interface import build_interface

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

iface = build_interface()
iface.launch(server_name="0.0.0.0", server_port=7860)
