import logging

from lexai.ui.gradio_interface import build_interface


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.info("Launching LexAI...")
    iface = build_interface()
    iface.launch()


if __name__ == "__main__":
    main()
