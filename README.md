# LexAI Demo

## AI-Powered Legal Research Assistant

This repository hosts a demonstration of LexAI, an AI-powered legal research assistant designed to provide relevant legal information based on user queries and specified locations. This project serves as a proof of concept, showcasing the integration of large language models (LLMs) with local embedding data for specialized information retrieval.

### Features

* AI-Powered Responses: Utilizes OpenAI's GPT models to generate natural language responses to legal queries.
* Location-Specific Information: Provides legal information tailored to specific jurisdictions (currently Boulder County, Colorado, and Denver, Colorado).
* Semantic Search: Employs embeddings and vector similarity search to find the most relevant legal documents.
* Interactive Web Interface: Built with Gradio for an easy-to-use, browser-based demonstration.

### Getting Started

Follow these steps to set up and run the LexAI demo on your local machine.

#### 1. Clone the Repository

First, clone this repository to your local machine:

```shell
git clone https://github.com/alexulanch/lexai-demo.git
cd lexai-demo
```

#### 2. Install Dependencies

Install the required Python packages using pip. The dependencies are `pandas`, `numpy`, `openai`, `gradio`, `scipy`, and `python-dotenv`.

```shell
pip install -r requirements.txt
```

#### 3. Obtain and Configure OpenAI API Key

This application relies on the OpenAI API. You will need an API key to use the models for embeddings and chat completions (e.g., text-embedding-ada-002, gpt-4).

**Important: Never hardcode your API key directly into your code or commit it to version control!**

**Using a `.env` file (for local development)**

1.  Create a new file named `.env` in the **root directory** of your project (the same directory as `pyproject.toml` and `requirements.txt`).
2.  Add your OpenAI API key to this file in the following format:

    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    Replace `"your_openai_api_key_here"` with your actual API key. The quotes are optional but good practice if your key contains special characters.
3.  **Ensure `.env` is in `.gitignore`:** The `.gitignore` file in this repository should already include `.env` to prevent it from being accidentally committed.

#### 4. Run the Application

Once your API key is configured, you can launch the Gradio application:

```shell
python -m lexai
```

The application will start, and you will see a local URL (e.g., `http://127.0.0.1:7860`) in your terminal. Open this URL in your web browser to interact with the LexAI Demo.

### Project Structure

The project is organized into a clear and modular structure:

```
lexai-demo/
├── .devcontainer/             # Development container configuration (for VS Code Dev Containers)
│   └── devcontainer.json
├── lexai/                     # Main Python package for the application
│   ├── __init__.py
│   ├── __main__.py            # Application entry point (Gradio app)
│   ├── config.py              # Application-wide configuration and constants
│   ├── core/                  # Core logic components
│   │   ├── data_loader.py     # Handles loading of embedding data
│   │   └── matcher.py         # Logic for finding semantic matches
│   └── services/              # External service integrations
│       └── openai_client.py   # Client for interacting with OpenAI API
├── pyproject.toml             # Project metadata and build configuration (PEP 517/518)
├── requirements.txt           # Python package dependencies
└── .gitignore                 # Specifies files/directories to ignore in Git
```

* `lexai/__main__.py`: This is the heart of the Gradio application, defining the UI and orchestrating the calls to core logic and services.
* `lexai/config.py`: Stores global application settings, model names (e.g., `MODEL_ENGINE = "text-embedding-ada-002"`, `GPT4_MODEL = "gpt-4"`), and role descriptions.
* `lexai/core/`: Contains the fundamental algorithms and data processing logic, such as loading embeddings (`data_loader.py`) and performing similarity searches (`matcher.py`).
* `lexai/services/`: Encapsulates interactions with external APIs, specifically the OpenAI API (`openai_client.py`).
* `.devcontainer/`: Provides configuration for consistent development environments using VS Code Dev Containers.
* `pyproject.toml`: A modern standard for defining project metadata and build system requirements.

### Usage

1.  Enter your legal question in the "Query" textbox.
2.  Select the desired "Location" (Boulder or Denver) from the dropdown.
3.  Click the "Submit" button to get an AI-generated response and relevant legal references.
4.  Use the "Clear" button to reset the input and output.
5.  Explore the "Examples" provided to quickly test the application.

### Error Handling

The application includes basic error handling for common issues:

* `Invalid OpenAI API key...`: This indicates that the `OPENAI_API_KEY` environment variable is either missing, empty, or incorrect. Please double-check your `.env` file or system environment variable setup.
* `OpenAI API Error...`: General errors from the OpenAI API (e.g., rate limiting, network issues).
* `File Error...`: Problems loading the embedding data files (e.g., `npz` files). Ensure they are correctly placed and accessible.
* `Input Error...`: Issues with the input provided to the application.

### Contributing

Contributions are welcome. If you have suggestions for improvements or encounter issues, please open an issue or submit a pull request.

### License

MIT

### Acknowledgements

* Built with Gradio
* Powered by OpenAI