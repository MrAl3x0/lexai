# LexAI

## AI-Powered Legal Research Assistant

LexAI is an AI assistant that delivers jurisdiction-specific legal information by integrating OpenAI's language models with local vector embeddings. The system uses semantic search to surface relevant legal references and provides a web interface for users to query the model interactively.

![LexAI Screenshot](assets/screenshot.png)

---

## Features

- **GPT-4 Integration**: Uses OpenAI's GPT-4 to generate concise, relevant legal responses.
- **Jurisdiction-Specific Search**: Preloaded embeddings for Boulder County and Denver, Colorado.
- **Semantic Search Engine**: Uses cosine similarity for embedding-based document retrieval.
- **Modern Web Interface**: Built with Gradio for real-time interaction.
- **Modular Design**: Separation of logic for UI, inference, and API handling.
- **Fully Tested**: Includes unit tests for embedding loading, matching logic, and OpenAI API integration.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/alexulanch/lexai.git
cd lexai
```

### 2. Install Git LFS (if needed)

This project uses [Git LFS](https://git-lfs.github.com/) for storing large `.npz` embedding files.

```bash
git lfs install
git lfs pull
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key and Embedding Paths

Create a `.env` file in the root directory:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
BOULDER_EMBEDDINGS_PATH=lexai/data/boulder_embeddings.npz
DENVER_EMBEDDINGS_PATH=lexai/data/denver_embeddings.npz
```

---

## Running the App

```bash
python -m lexai
```

Then open `http://127.0.0.1:7860` in your browser.

---

## Project Structure

```
.
├── LICENSE
├── README.md
├── assets
│   └── screenshot.png
├── lexai
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── match_engine.py
│   │   └── matcher.py
│   ├── data
│   │   ├── boulder_embeddings.npz
│   │   └── denver_embeddings.npz
│   ├── models
│   │   └── embedding_model.py
│   ├── services
│   │   └── openai_client.py
│   └── ui
│       ├── __init__.py
│       └── gradio_interface.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── tests
    ├── __init__.py
    ├── test_data_loader.py
    ├── test_matcher.py
    └── test_openai_client.py
```

---

## Testing

LexAI includes a full suite of unit tests using `pytest`.

To run the tests:

```bash
pytest
```

Tests are located in the `tests/` directory and cover:

- Embedding data loading
- Semantic similarity matching
- OpenAI API interaction

---

## License

MIT License

---

## Acknowledgements

- Built with [Gradio](https://gradio.app)
- Powered by [OpenAI](https://openai.com)
