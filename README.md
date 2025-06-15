# **lexai: AI-Powered Legal Research Assistant**

lexai is an AI legal assistant that delivers accurate legal information based on user queries and jurisdictions. Using OpenAI's GPT-4 and text-embedding models, it offers a user-friendly interface to get AI-generated responses and references to source material.

## **Disclaimer**

**Important:** The legal documents used to generate the embeddings for this project were last updated in **June 2022**. The information provided may not reflect the most current laws or legal precedents. This tool should be used for informational purposes only and is not a substitute for professional legal advice.

## **Features**

- **Natural Language Queries**: Ask legal questions in plain English.
- **Jurisdiction-Specific**: Get answers tailored to specific legal jurisdictions (currently supports Boulder and Denver, CO).
- **Source Referencing**: Responses include links to the original legal texts used to generate the answer.
- **Powered by GPT-4**: Leverages OpenAI's most advanced models for high-quality responses.
- **Professional Structure**: Organized into a scalable and maintainable package.

## **Getting Started**

Follow these instructions to set up and run the project locally.

### **Prerequisites**

- Python 3.8+
- An OpenAI API key with access to the gpt-4 model.
- [Git LFS](https://git-lfs.com) installed on your system.

### **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/your-username/lexai.git\](https://github.com/your-username/lexai.git)  
   cd lexai

2. Download the Embedding Data:  
   This project uses Git LFS to manage large embedding files. Pull the data with the following command:  
   git lfs pull

   _If_ this command fails, you may need to [_install Git LFS_](https://git-lfs.com) _first._

3. **Create a virtual environment (recommended):**  
   python3 \-m venv venv  
   source venv/bin/activate \# On Windows, use \`venv\\Scripts\\activate\`

4. **Install the required dependencies:**  
   pip3 install \-r requirements.txt

5. Set up your environment variables:  
   Create a file named .env in the root of your project directory and add your OpenAI API key:  
   OPENAI_API_KEY="your-api-key-goes-here"

   _(The .gitignore file will prevent this file from being committed.)_

## **Usage**

### **Running the Application**

To launch the lexai web application, run the main module from the project's root directory:

python3 \-m lexai_app.main

This will start the Gradio web server and provide a local URL to open in your browser.

### **Running Tests**

To verify that the core logic is working correctly, run the automated tests using pytest:

python3 \-m pytest

## **License**

This project is licensed under the MIT License. See the [LICENSE](http://docs.google.com/LICENSE) file for details.
