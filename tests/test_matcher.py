import numpy as np
import pandas as pd
import pytest

from lexai.core.matcher import find_top_matches


@pytest.fixture
def sample_embeddings():
    return np.array(
        [
            [1.0, 0.1, 0.1],
            [0.8, 0.3, 0.2],
            [0.5, 0.5, 0.5],
            [0.1, 0.1, 1.0],
            [0.0, 0.0, 0.0],
        ],
        dtype=np.float32,
    )


@pytest.fixture
def sample_jurisdiction_data():
    return pd.DataFrame(
        {
            "url": ["url1", "url2", "url3", "url4", "url5"],
            "title": ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"],
            "subtitle": [
                "Subtitle A",
                "Subtitle B",
                "Subtitle C",
                "Subtitle D",
                "Subtitle E",
            ],
            "content": [
                "Content X",
                "Content Y",
                "Content Z",
                "Content W",
                "Content V",
            ],
        }
    )


@pytest.fixture
def sample_query_embedding():
    return np.array([1.0, 0.0, 0.0], dtype=np.float32)


@pytest.fixture
def empty_embeddings():
    return np.empty((0, 3), dtype=np.float32)


@pytest.fixture
def empty_jurisdiction_data():
    return pd.DataFrame(columns=["url", "title", "subtitle", "content"])


def test_returns_expected_number_of_matches(
    sample_query_embedding, sample_embeddings, sample_jurisdiction_data
):
    matches = find_top_matches(
        sample_query_embedding,
        sample_embeddings,
        sample_jurisdiction_data,
        num_matches=3,
    )
    assert len(matches) == 3
    assert [match["title"] for match in matches] == [
        "Title 1",
        "Title 2",
        "Title 3",
    ]


def test_returns_all_available_matches_if_less_than_requested(
    sample_query_embedding, sample_embeddings, sample_jurisdiction_data
):
    matches = find_top_matches(
        sample_query_embedding,
        sample_embeddings,
        sample_jurisdiction_data,
        num_matches=10,
    )
    assert len(matches) == len(sample_embeddings)
    assert matches[0]["title"] == "Title 1"


def test_returns_empty_list_for_empty_embeddings(
    sample_query_embedding, empty_embeddings, empty_jurisdiction_data
):
    matches = find_top_matches(
        sample_query_embedding,
        empty_embeddings,
        empty_jurisdiction_data,
        num_matches=3,
    )
    assert matches == []


def test_returns_empty_list_for_empty_jurisdiction_data(
    sample_query_embedding, sample_embeddings, empty_jurisdiction_data
):
    matches = find_top_matches(
        sample_query_embedding,
        sample_embeddings,
        empty_jurisdiction_data,
        num_matches=3,
    )
    assert matches == []


def test_output_contains_expected_keys(
    sample_query_embedding, sample_embeddings, sample_jurisdiction_data
):
    matches = find_top_matches(
        sample_query_embedding,
        sample_embeddings,
        sample_jurisdiction_data,
        num_matches=1,
    )
    match = matches[0]
    assert set(match.keys()) == {"url", "title", "subtitle", "content"}
    assert match["url"] == "url1"
    assert match["title"] == "Title 1"
    assert match["subtitle"] == "Subtitle A"
    assert match["content"] == "Content X"


def test_handles_single_embedding_and_row(
    sample_query_embedding, sample_embeddings, sample_jurisdiction_data
):
    matches = find_top_matches(
        sample_query_embedding,
        sample_embeddings[:1],
        sample_jurisdiction_data.iloc[:1],
        num_matches=3,
    )
    assert len(matches) == 1
    assert matches[0]["title"] == "Title 1"


def test_raises_for_invalid_query_embedding_shape(
    sample_embeddings, sample_jurisdiction_data
):
    invalid_vector = np.array([1.0, 2.0], dtype=np.float32)
    with pytest.raises(ValueError, match="dimensionality of the embeddings"):
        find_top_matches(
            invalid_vector,
            sample_embeddings,
            sample_jurisdiction_data,
            num_matches=1,
        )

    scalar_value = np.array(1.0, dtype=np.float32)
    with pytest.raises(ValueError):
        find_top_matches(
            scalar_value,
            sample_embeddings,
            sample_jurisdiction_data,
            num_matches=1,
        )
