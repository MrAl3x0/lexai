"""
HTML formatting utilities for the LexAI application.

This module contains functions that transform structured data
into HTML snippets for display in the user interface.
"""

from html import escape


def format_legal_response(response_text: str) -> str:
    """
    Wrap the AI-generated legal response in HTML for UI rendering.

    Parameters
    ----------
    response_text : str
        The main response text from the assistant.

    Returns
    -------
    str
        HTML-formatted string with a 'Response' header and the content.
    """
    return (
        "<p><strong>Response:</strong></p>"
        f"<p>{escape(response_text)}</p>"
    )


def format_references(matches: list[dict]) -> str:
    """
    Format a list of top document matches into an HTML reference list.

    Parameters
    ----------
    matches : list of dict
        List of matched legal documents, each containing 'url', 'title', and 'subtitle'.

    Returns
    -------
    str
        HTML-formatted reference section with clickable links.
    """
    if not matches:
        return "<p><strong>References:</strong> None found.</p>"

    html = "<p><strong>References:</strong></p><ul>"
    for match in matches:
        url = escape(match.get("url", "#"))
        title = escape(match.get("title", "Untitled"))
        subtitle = escape(match.get("subtitle", ""))
        html += (
            "<li>"
            f"<a href=\"{url}\" target=\"_blank\" rel=\"noopener noreferrer\">"
            f"{title}: {subtitle}</a></li>"
        )
    html += "</ul>"
    return html
