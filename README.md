# LexAI

LexAI is an AI legal assistant that delivers accurate legal information based on user queries and jurisdictions. Using OpenAI's GPT-4 and text-embedding models, it offers a user-friendly interface with AI-generated responses and references.

## Status
**Current Status**: In Development

**Last Updated**: 2025-07-04

**Progress Summary**: The application is functional but is still under active development.

## Tech Stack
- **Language(s)**: Python
- **Frameworks / Libraries**: Gradio
- **Tools / Services**: OpenAI API

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alexulanch/lexai.git
   cd lexai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the project**:
   ```bash
   python app.py
   ```

4. **Environment Variables**:  
   Create a `.env` file and define the following:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage
To use LexAI, run the application and open the provided URL in your web browser. Enter your legal query, select a jurisdiction, and provide your OpenAI API key to receive legal information and references.

## To-Do / Roadmap
- [ ] Add support for more jurisdictions.
- [ ] Improve the accuracy of the legal information provided.
- [ ] Implement a user authentication system.

## Known Issues
- The application may occasionally produce inaccurate or incomplete information.

## Notes
This project requires an OpenAI API key with access to GPT-4.

## License
This project is licensed under the MIT license. See the `LICENSE` file for more information.

