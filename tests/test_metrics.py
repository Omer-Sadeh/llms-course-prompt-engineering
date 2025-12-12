import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from src.utils.metrics import SimilarityEvaluator

@pytest.fixture
def mock_model():
    with patch("src.utils.metrics.SentenceTransformer") as mock:
        instance = mock.return_value
        # Mock encode to return dummy embeddings
        instance.encode.return_value = np.array([[1.0, 0.0], [0.0, 1.0]]) # Orthogonal vectors
        yield instance

def test_calculate_distance(mock_model):
    evaluator = SimilarityEvaluator()
    dist = evaluator.calculate_distance("text1", "text2")
    # Orthogonal vectors should have cosine distance of ~1.0
    # Note: sklearn cosine_distance returns 1 - cos_sim.
    # cos_sim([1,0], [0,1]) = 0. dist = 1 - 0 = 1.
    assert pytest.approx(dist, 0.001) == 1.0

def test_identical_text_distance(mock_model):
    evaluator = SimilarityEvaluator()
    # Ensure identical vectors return 0 distance
    mock_model.encode.return_value = np.array([[1.0, 0.0], [1.0, 0.0]])
    dist = evaluator.calculate_distance("text1", "text1")
    assert pytest.approx(dist, 0.001) == 0.0
