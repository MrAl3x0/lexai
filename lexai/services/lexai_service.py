"""
LexAI service layer for handling user queries.

This module defines a service class that interfaces with the core match engine,
processes the results, and formats them for display in the UI.
"""

from lexai.core.match_engine import generate_matches
from lexai.ui.formatters import format_legal_response, format_references


class LexAIService:
    """
    Service class that handles legal queries by invoking the match engine and
    formatting the results for UI presentation.
    """

    @staticmethod
    def handle_query(query: str, location: str) -> str:
        """
        Handles a user query and returns an HTML-formatted response.

        This method:
        - Calls the semantic match engine with the given query and location.
        - Extracts both the AI-generated response and the list of matched legal entries.
        - Constructs an HTML string that includes the AI's response followed by
          a reference list linking to legal documents.

        Parameters
        ----------
        query : str
            The legal question asked by the user.
        location : str
            The jurisdiction to search within.

        Returns
        -------
        str
            A formatted HTML string with the AI response and relevant matches.
        """
        result = generate_matches(query, location)

        gpt_response = result.get("response", "").strip()
        matches = result.get("matches", [])

        if (
            not isinstance(matches, list)
            or not matches
            or not isinstance(matches[0], dict)
        ):
            return format_legal_response(gpt_response or "No matches found.")

        return (
            format_legal_response(gpt_response) +
            format_references(matches)
        )
