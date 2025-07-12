"""
Matching engine for LexAI.

This module provides functionality to find the closest legal documents
to a user query using cosine similarity on embedding vectors.
"""

from typing import Any

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def find_top_matches(
    query_embedding: np.ndarray,
    embeddings: np.ndarray,
    jurisdiction_data: pd.DataFrame,
    num_matches: int = 3,
) -> list[dict[str, Any]]:
    """
    Finds the top N closest matches to a query embedding within a set of embeddings.

    Parameters
    ----------
    query_embedding : np.ndarray
        The embedding of the user's query.
    embeddings : np.ndarray
        The array of embeddings from the legal jurisdiction data.
    jurisdiction_data : pd.DataFrame
        DataFrame containing the metadata (url, title, subtitle, content)
        corresponding to the embeddings.
    num_matches : int, optional
        The number of top matches to retrieve, by default 3.

    Returns
    -------
    list[dict[str, Any]]
        A list of dictionaries, where each dictionary represents a top match
        and contains its 'url', 'title', 'subtitle', and 'content'.
    """
    if jurisdiction_data.empty or embeddings.shape[0] == 0:
        return []

    if jurisdiction_data.shape[0] != embeddings.shape[0]:
        raise ValueError(
            "Number of embeddings and metadata entries must match.")

    if query_embedding.ndim != 1 or query_embedding.shape[0] != embeddings.shape[1]:
        raise ValueError(
            "Query embedding must match the dimensionality of the embeddings."
        )

    distances = cdist(query_embedding.reshape(1, -1),
                      embeddings, metric="cosine")[0]
    safe_num_matches = min(num_matches, len(jurisdiction_data))
    indices = np.argsort(distances)[:safe_num_matches]
    subset = jurisdiction_data.iloc[indices]

    return subset.to_dict("records")
