import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from typing import Any

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

    distances = cdist(query_embedding.reshape(1, -1), embeddings, metric="cosine")[0]
    indices = np.argsort(distances)[:num_matches]
    subset: pd.DataFrame = jurisdiction_data.loc[indices]
    top_matches: list[dict[str, Any]] = subset.to_dict("records")

    return top_matches