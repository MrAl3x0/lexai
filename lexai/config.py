MODEL_ENGINE = "text-embedding-ada-002"

LOCATION_INFO = {
    "Boulder": {
        "npz_file": "lexai/data/boulder_embeddings.npz",
        "role_description": (
            "You are an AI-powered legal assistant specializing in the jurisdiction of "
            "Boulder County, Colorado."
        ),
    },
    "Denver": {
        "npz_file": "lexai/data/denver_embeddings.npz",
        "role_description": (
            "You are an AI-powered legal assistant specializing in the jurisdiction of "
            "Denver, Colorado."
        ),
    },
}

APP_DESCRIPTION = (
    "LexAI is an AI-powered legal research app designed to assist individuals, "
    "including law enforcement officers, legal professionals, and the general public, "
    "in accessing accurate legal information. The app covers various jurisdictions "
    "and ensures that users can stay informed and confident, regardless of their location. "
    "This demo is meant to serve as a proof of concept."
)

OPENAI_API_KEY_PLACEHOLDER = "Enter your OpenAI API key"

GPT4_MODEL = "gpt-4"
GPT4_TEMPERATURE = 0.7
GPT4_MAX_TOKENS = 120
GPT4_TOP_P = 1
GPT4_FREQUENCY_PENALTY = 0
GPT4_PRESENCE_PENALTY = 0

AI_ROLE_TEMPLATE = """
Your expertise lies in providing accurate and timely information on the laws and regulations specific to your jurisdiction.
Your role is to assist individuals, including law enforcement officers, legal professionals, and the general public,
in understanding and applying legal standards within this jurisdiction. You are knowledgeable, precise, and always
ready to offer guidance on legal matters. Your max_tokens is set to 120 so keep your response below that.
"""
