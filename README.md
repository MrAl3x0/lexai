# LexAI Demo

## AI-Powered Legal Research Assistant

This repository hosts a demonstration of **LexAI**, an AI-powered legal research assistant designed to provide relevant legal information based on user queries and specified locations. This project serves as a proof of concept, showcasing the integration of large language models (LLMs) with local embedding data for specialized information retrieval.

### Features

![LexAI Demo Screenshot](assets/screenshot.png)

- **AI-Powered Responses**: Utilizes OpenAI's GPT-4 model to generate natural language responses to legal queries.
- **Location-Specific Information**: Provides legal information tailored to specific jurisdictions (currently Boulder County, Colorado, and Denver, Colorado).
- **Semantic Search**: Employs embeddings and vector similarity search to find the most relevant legal documents.
- **Interactive Web Interface**: Built with Gradio for an easy-to-use, browser-based demonstration.

---

### Getting Started

Follow these steps to set up and run the LexAI demo on your local machine.

#### 1. Clone the Repository

```bash
git clone https://github.com/alexulanch/lexai-demo.git
cd lexai-demo
```

This project uses [Git LFS](https://git-lfs.github.com/) to manage the embedding data.

If you’re **not using the provided dev container**, install Git LFS before cloning:

```bash
git lfs install
git lfs pull
```
---

#### 2. Install Dependencies

Install the required Python packages using pip. The dependencies are: `pandas`, `numpy`, `openai`, `gradio`, `scipy`, and `python-dotenv`.

```bash
pip install -r requirements.txt
```

---

#### 3. Configure Your OpenAI API Key

This application relies on the OpenAI API. You will need an API key to access the models used for embeddings and chat completions (e.g., `text-embedding-ada-002`, `gpt-4`).

**Using a `.env` file (recommended for local development):**

1. Create a file named `.env` in the root directory of the project.
2. Add your API key to the file like this:

    ```dotenv
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

3. Ensure `.env` is listed in `.gitignore` to avoid committing it by mistake.

---

#### 4. Run the Application

Start the Gradio app:

```bash
python -m lexai
```

You’ll see a local URL like `http://127.0.0.1:7860` — open it in your browser to use LexAI Demo.

---

### Project Structure

```
lexai-demo/
├── .devcontainer/             # Dev container config for VS Code
│   └── devcontainer.json
├── lexai/                     # Main Python package
│   ├── __init__.py
│   ├── __main__.py            # Gradio app entry point
│   ├── config.py              # Global app config and constants
│   ├── core/                  # Core logic components
│   │   ├── data_loader.py     # Loads embedding data
│   │   └── matcher.py         # Semantic search logic
│   └── services/              # External API integrations
│       └── openai_client.py   # Interacts with OpenAI API
├── pyproject.toml             # Project metadata and build config
├── requirements.txt           # Python dependencies
└── .gitignore                 # Files/directories Git should ignore
```

---

### Usage

1. Enter your legal question in the "Query" textbox.
2. Select the desired "Location" (Boulder or Denver) from the dropdown.
3. Click "Submit" to get an AI-generated response and relevant legal references.
4. Use the "Clear" button to reset.
5. Explore the example queries provided.

---

### Error Handling

The app handles several common error cases:

- `Invalid OpenAI API key...`: Check your `.env` file or environment variable setup.
- `OpenAI API Error...`: Rate limits, network issues, etc.
- `File Error...`: Missing or unreadable `.npz` embedding files.
- `Input Error...`: Malformed or missing user input.

---

### Contributing

Contributions are welcome! Open an issue or pull request with ideas or fixes.

---

### License

MIT

---

### Acknowledgements

- Built with [Gradio](https://gradio.app)
- Powered by [OpenAI](https://openai.com)
