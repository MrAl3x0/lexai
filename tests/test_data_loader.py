import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from lexai.core.data_loader import load_embeddings


@pytest.fixture
def temp_npz_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "test_data.npz"
    np.savez(
        file_path,
        embeddings=np.random.rand(4, 768),
        urls=["https://a.com", "https://b.com",
              "https://c.com", "https://d.com"],
        titles=["A", "B", "C", "D"],
        subtitles=["a", "b", "c", "d"],
        contents=["alpha", "beta", "gamma", "delta"],
    )
    return file_path


@pytest.fixture
def broken_npz_missing_embeddings(tmp_path: Path) -> Path:
    file_path = tmp_path / "broken_missing_embeddings.npz"
    np.savez(file_path, urls=["a"], titles=["b"],
             subtitles=["c"], contents=["d"])
    return file_path


@pytest.fixture
def broken_npz_missing_columns(tmp_path: Path) -> Path:
    file_path = tmp_path / "broken_missing_columns.npz"
    np.savez(file_path, embeddings=np.random.rand(1, 768), urls=["x"])
    return file_path


def test_load_embeddings_success(temp_npz_file):
    embeddings, metadata = load_embeddings(temp_npz_file)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (4, 768)
    assert isinstance(metadata, pd.DataFrame)
    assert list(metadata.columns) == ["url", "title", "subtitle", "content"]
    assert metadata.shape == (4, 4)


def test_load_embeddings_missing_key(broken_npz_missing_embeddings):
    with pytest.raises(KeyError, match="Missing key 'embeddings'"):
        load_embeddings(broken_npz_missing_embeddings)


def test_load_metadata_missing_key(broken_npz_missing_columns):
    with pytest.raises(KeyError, match="Missing key 'titles'"):
        load_embeddings(broken_npz_missing_columns)


def test_load_embeddings_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_embeddings("nonexistent_file.npz")
