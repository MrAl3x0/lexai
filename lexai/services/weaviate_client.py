"""
Weaviate client for LexAI, handling connection, schema definition,
and basic data operations for legal document chunks.
"""

import json
import logging

import weaviate

from lexai.config import (
    WEAVIATE_API_KEY,
    WEAVIATE_OPENAI_EMBEDDING_MODEL,
    WEAVIATE_URL,
)

logger = logging.getLogger(__name__)


class WeaviateClient:
    """
    Client class for interacting with the Weaviate vector database.
    Handles connection, schema management, and basic data object operations.
    """

    def __init__(self):
        """
        Initializes the Weaviate client.
        """
        try:
            auth_config = None
            if WEAVIATE_API_KEY:
                auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)

            self.client = weaviate.Client(
                url=WEAVIATE_URL,
                auth_client_secret=auth_config
            )
            logger.info(f"Weaviate client initialized for URL: {WEAVIATE_URL}")
            if not self.client.is_ready():
                logger.warning("Weaviate instance is not ready or reachable.")
            else:
                logger.info("Weaviate instance is ready.")

        except Exception as e:
            logger.error(f"Failed to initialize Weaviate client: {e}")
            raise

    def get_or_create_schema(self, class_name: str = "LegalDocumentChunk"):
        """
        Ensures the 'LegalDocumentChunk' schema exists in Weaviate.
        If it doesn't exist, it creates it with a flexible structure.

        Args:
            class_name (str): The name of the class (collection) to manage.
        """
        try:
            class_info = self.client.schema.get(class_name)
            logger.info(
                f"Class '{class_name}' already exists. Schema:\n"
                f"{json.dumps(class_info, indent=2)}"
            )
            return
        except weaviate.exceptions.UnexpectedStatusCodeException as e:
            if "not found" in str(e).lower():
                logger.info(
                    f"Class '{class_name}' not found. Creating schema...")
            else:
                logger.error(f"Error checking schema for '{class_name}': {e}")
                raise e
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while checking schema for "
                f"'{class_name}': {e}"
            )
            raise

        schema = {
            "class": class_name,
            "description": (
                "A chunk of legal document content with associated metadata."
            ),
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "vectorizeClassName": True,
                    "model": WEAVIATE_OPENAI_EMBEDDING_MODEL,
                    "type": "text"
                }
            },
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The textual content of the document chunk.",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False
                        }
                    }
                },
                {
                    "name": "url",
                    "dataType": ["text"],
                    "description": "Original URL of the full legal document.",
                },
                {
                    "name": "title",
                    "dataType": ["text"],
                    "description": "Main title of the legal document.",
                },
                {
                    "name": "jurisdiction",
                    "dataType": ["text"],
                    "description": (
                        "The specific jurisdiction (e.g., 'Boulder', 'Denver')."
                    ),
                    "indexFilterable": True,
                    "indexSearchable": False
                },
                {
                    "name": "documentType",
                    "dataType": ["text"],
                    "description": "Type of legal document ('Statute').",
                    "indexFilterable": True,
                    "indexSearchable": False
                },
                {
                    "name": "lastUpdated",
                    "dataType": ["date"],
                    "description": "Date the document was last updated or scraped.",
                    "indexFilterable": True
                },
                {
                    "name": "effectiveDate",
                    "dataType": ["date"],
                    "description": (
                        "Date the specific rule/law became effective (if applicable)."
                    ),
                    "indexFilterable": True
                },
                {
                    "name": "chunkId",
                    "dataType": ["text"],
                    "description": "A unique identifier for this specific chunk.",
                    "indexFilterable": True,
                    "indexSearchable": False
                },
                {
                    "name": "parentDocumentId",
                    "dataType": ["text"],
                    "description": (
                        "Identifier for the document from which this chunk originated."
                    ),
                    "indexFilterable": True,
                    "indexSearchable": False
                },
                {
                    "name": "additionalMetadata",
                    "dataType": ["text"],
                    "description": (
                        "JSON string containing jurisdiction-specific metadata "
                        "(e.g., 'article': '1', 'section': 'A')."
                    ),
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": True
                        }
                    }
                }
            ]
        }

        try:
            self.client.schema.create_class(schema)
            logger.info(
                f"Schema for class '{class_name}' created successfully.")
        except weaviate.exceptions.UnexpectedStatusCodeException as e:
            if "already exists" in str(e).lower():
                logger.warning(
                    f"Class '{class_name}' already exists. Skipping creation.")
            else:
                logger.error(f"Error creating schema for '{class_name}': {e}")
                raise e
        except Exception as e:
            logger.error(
                f"An unexpected error occurred during schema creation for "
                f"'{class_name}': {e}",
                exc_info=True
            )
            raise

    def add_data_object(
        self,
        data_object: dict,
        class_name: str = "LegalDocumentChunk",
    ):
        """
        Adds a single data object (a legal document chunk) to the Weaviate class.

        Args:
            data_object (dict): A dictionary representing the data object,
                                 must include 'content' and adhere to the schema.
            class_name (str): The name of the class (collection) to add data to.

        Returns:
            str: The UUID of the newly created data object in Weaviate.

        Raises:
            ValueError: If 'content' is missing from the data_object.
            Exception: For other Weaviate-related errors during data creation.
        """
        if "content" not in data_object:
            logger.error(
                "Attempted to add data object without 'content' property.")
            raise ValueError("Data object must contain 'content' property.")

        if (
            "additionalMetadata" in data_object and
            isinstance(data_object["additionalMetadata"], dict)
        ):
            try:
                data_object["additionalMetadata"] = json.dumps(
                    data_object["additionalMetadata"])
            except TypeError as e:
                logger.error(
                    f"Failed to serialize additionalMetadata to JSON: {e}")
                raise ValueError(
                    "additionalMetadata must be JSON serializable: "
                    f"{e}"
                )

        try:
            uuid = self.client.data_object.create(
                data_object=data_object,
                class_name=class_name
            )
            logger.debug(f"Added data object with UUID: {uuid}")
            return uuid
        except Exception as e:
            logger.error(f"Error adding data object to Weaviate: {e}")
            raise

    def search_similar(self,
                       query_embedding: list[float],
                       class_name: str,
                       limit: int = 3,
                       filters: dict = None) -> list[dict]:
        """
        Searches for similar legal document chunks in Weaviate.
        This method will be implemented in a later phase.
        """
        logger.warning(
            "search_similar method is not yet implemented in this client.")
        return []
