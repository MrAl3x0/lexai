"""
HTML formatting utilities for the LexAI application.

This module contains functions that transform structured data
into HTML snippets for display in the user interface.
"""

from html import escape


def format_legal_response(response_text: str) -> str:
    """
    Wrap the AI-generated legal response in HTML for UI rendering.
    """
    return (
        "<p><strong>Response:</strong></p>"
        f"<p>{escape(response_text)}</p>"
    )


def format_references(matches: list[dict]) -> str:
    """
    Format a list of top document matches into an HTML reference list.
    """
    if not matches:
        return "<p><strong>References:</strong> None found.</p>"

    reference_html = "<p><strong>References:</strong></p><ul>"
    for match in matches:
        url = escape(match.get("url", "#"))
        title = escape(match.get("title", "Untitled"))
        subtitle = escape(match.get("subtitle", ""))
        reference_html += (
            f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">'
            f"{title}: {subtitle}</a></li>"
        )
    reference_html += "</ul>"
    return reference_html
