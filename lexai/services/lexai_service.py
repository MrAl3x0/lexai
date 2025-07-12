"""
Service layer for handling LexAI application logic.

Provides an abstraction between the UI and the core matching engine.
"""

from lexai.core.match_engine import generate_matches


class LexAIService:
    @staticmethod
    def handle_query(query: str, location: str) -> str:
        """
        Process a user query by invoking the match engine.

        Parameters:
            query (str): The legal question from the user.
            location (str): The jurisdiction for the query.

        Returns:
            str: HTML-formatted response with AI-generated content and references.
        """
        return generate_matches(query, location)
