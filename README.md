# lexai: AI-Powered Legal Research Assistant

**lexai** is an AI legal assistant that delivers accurate legal information based on user queries and jurisdictions. Using OpenAI's GPT-4 and text-embedding models, it offers a user-friendly interface to provide AI-generated responses and references to source material.

## Disclaimer

**Important:** The legal documents used to generate the embeddings for this project were last updated in **June 2022**. The information provided may not reflect the most current laws or legal precedents. This tool should be used for **informational purposes only** and is **not a substitute for professional legal advice**.

## Features

- **Natural Language Queries** — Ask legal questions in plain English.
- **Jurisdiction-Specific** — Get answers tailored to specific legal jurisdictions (currently supports Boulder and Denver, CO).
- **Source Referencing** — Responses include links to the original legal texts used to generate the answer.
- **Powered by GPT-4** — Leverages OpenAI's most advanced models for high-quality responses.
- **Professional Structure** — Organized into a scalable and maintainable package.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.8+
- An OpenAI API key with access to the GPT-4 model
- [Git LFS](https://git-lfs.com) installed on your system

### Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/lexai.git
    cd lexai
    ```

2. **Download the embedding data**  
    This project uses Git LFS to manage large embedding files:
    ```bash
    git lfs pull
    ```
    _If this command fails, you may need to [install Git LFS](https://git-lfs.com) first._

3. **Create a virtual environment (recommended)**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Install required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up your environment variables**  
    Create a file named `.env` in the root of your project directory:
    ```
    OPENAI_API_KEY="your-api-key-goes-here"
    ```
    _(The `.gitignore` file will prevent this file from being committed.)_

## Usage

### Running the application

Start the Gradio web app from the root directory:
```bash
python3 -m lexai_app.main
```
This will start the server and provide a local URL to open in your browser.

### Running Tests

Run automated tests with:
```bash
python3 -m pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

