# ==============================================================================
# lexai: Core Logic
#
# This module contains the core functionality for the legal research assistant,
# including data loading, embedding generation, and interaction with the
# OpenAI API.
# ==============================================================================

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from openai import OpenAI
from dotenv import load_dotenv

# --- Configuration & Initialization ---

load_dotenv()

try:
    client = OpenAI()
except Exception as e:
    print(f"Error: OpenAI client could not be initialized. Ensure the OPENAI_API_KEY is set. Details: {e}")
    exit()

MODEL_ENGINE = "text-embedding-ada-002"

LOCATION_INFO = {
    "Boulder": {
        "npz_file": "embeddings/boulder_embeddings.npz",
        "role_description": "You are an AI-powered legal assistant specializing in the jurisdiction of Boulder County, Colorado."
    },
    "Denver": {
        "npz_file": "embeddings/denver_embeddings.npz",
        "role_description": "You are an AI-powered legal assistant specializing in the jurisdiction of Denver, Colorado."
    }
}

# --- Core Function ---

def generate_matches(query, location):
    """
    Generates legal information matches based on a user's query and location.
    """
    try:
        # 1. Create a vector embedding for the user's query.
        embedding_response = client.embeddings.create(
            input=query,
            model=MODEL_ENGINE
        )
        query_embedding = np.array(embedding_response.data[0].embedding)

        # 2. Load data for the selected jurisdiction.
        location_data = LOCATION_INFO.get(location)
        if not location_data:
            raise ValueError(f"Configuration Error: No data found for the selected location: '{location}'.")

        npz_file = location_data['npz_file']
        role_description = location_data['role_description']

        try:
            # Attempt to load the data file for the jurisdiction.
            data = np.load(npz_file, allow_pickle=True)
            embeddings = data['embeddings']
            jurisdiction_data = pd.DataFrame({
                'url': data['urls'],
                'title': data['titles'],
                'subtitle': data['subtitles'],
                'content': data['contents']
            })
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at '{npz_file}'. Please ensure you have downloaded the Git LFS files by running 'git lfs pull'.")
        except Exception as e:
            # A more specific error for pickle/format issues.
            raise Exception(f"Failed to load or interpret data from '{npz_file}'. The file may be corrupt or incompatible. Ensure you have the latest version via 'git lfs pull'. Original error: {e}")

        # 3. Find the most relevant documents.
        distances = cdist(query_embedding.reshape(1, -1), embeddings, metric='cosine')[0]
        indices = np.argsort(distances)[:3]
        top_matches = jurisdiction_data.iloc[indices].to_dict('records')

        # 4. Generate a response with the chat model.
        system_prompt = f'''
          {role_description}
          Your expertise lies in providing accurate and timely information on the laws and regulations specific to your jurisdiction.
          Your role is to assist individuals in understanding and applying legal standards.
          You are knowledgeable, precise, and must base your response on the provided context.
          Keep your response concise and under 120 tokens.
          '''

        chat_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "system", "content": f"Use the following context to answer the user's query: {str(top_matches)}"},
                {"role": "user", "content": query},
            ],
            temperature=0.7,
            max_tokens=120,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        message = chat_response.choices[0].message.content.strip()

        # 5. Format the output as HTML.
        html_response = f"<p><strong>Response:</strong></p><p>{message}</p>"
        html_references = "<p><strong>References:</strong></p><ul>"
        for match in top_matches:
            safe_url = match["url"].replace('"', '&quot;')
            html_references += f'<li><a href="{safe_url}" target="_blank">{match["title"]}: {match["subtitle"]}</a></li>'
        html_references += "</ul>"

        return html_response + html_references

    except Exception as e:
        error_notice = '''<p style="font-family: Arial, sans-serif; font-size: 16px; color: #D8000C;">
    <strong>Error:</strong> An issue occurred while processing your request.
</p>'''
        print(f"An error occurred in generate_matches: {e}")
        return f"<p>{error_notice} <br><strong>Details:</strong> {str(e)}</p>"
