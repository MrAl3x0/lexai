import numpy as np
import pandas as pd
import os


def load_embeddings_data(npz_file_path: str) -> tuple[np.ndarray, pd.DataFrame]:
    """
    Loads embeddings and associated jurisdiction data from a .npz file.

    Parameters
    ----------
    npz_file_path : str
        The full path to the .npz file containing the embeddings and metadata.

    Returns
    -------
    tuple[np.ndarray, pd.DataFrame]
        A tuple containing:
        - embeddings (np.ndarray): The loaded numerical embeddings.
        - jurisdiction_data (pd.DataFrame): A DataFrame with 'url', 'title',
          'subtitle', and 'content' columns.

    Raises
    ------
    FileNotFoundError
        If the specified .npz file does not exist.
    KeyError
        If expected keys ('embeddings', 'urls', 'titles', 'subtitles', 'contents')
        are not found in the .npz file.
    """

    if not os.path.exists(npz_file_path):
        raise FileNotFoundError(f"Embedding file not found: {npz_file_path}")

    data = np.load(npz_file_path, allow_pickle=True)

    required_keys = ["embeddings", "urls", "titles", "subtitles", "contents"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Missing key '{key}' in {npz_file_path}")

    embeddings = data["embeddings"]
    jurisdiction_data = pd.DataFrame(
        {
            "url": data["urls"],
            "title": data["titles"],
            "subtitle": data["subtitles"],
            "content": data["contents"],
        }
    )
    return embeddings, jurisdiction_data
