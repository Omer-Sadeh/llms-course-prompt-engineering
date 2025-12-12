import pytest
from unittest.mock import MagicMock, patch
from src.utils.metrics import SimilarityEvaluator
import numpy as np

class TestSimilarityEvaluator:

    @patch('src.utils.metrics.SentenceTransformer')
    def test_init(self, mock_st):
        evaluator = SimilarityEvaluator(model_name="test-model")
        mock_st.assert_called_with("test-model")
        assert evaluator.model == mock_st.return_value

    @patch('src.utils.metrics.SentenceTransformer')
    def test_init_failure(self, mock_st):
        mock_st.side_effect = Exception("Load failed")
        with pytest.raises(Exception):
            SimilarityEvaluator()

    @patch('src.utils.metrics.SentenceTransformer')
    def test_calculate_distance(self, mock_st):
        evaluator = SimilarityEvaluator()
        
        # Mock encode to return dummy embeddings
        # shape (2, 384)
        mock_st.return_value.encode.return_value = np.array([[1, 0], [0, 1]])
        
        dist = evaluator.calculate_distance("text1", "text2")
        # cosine distance between [1,0] and [0,1] is 1.0
        assert dist == 1.0

    @patch('src.utils.metrics.SentenceTransformer')
    def test_calculate_distance_empty(self, mock_st):
        evaluator = SimilarityEvaluator()
        dist = evaluator.calculate_distance("", "text")
        assert dist == 1.0

    @patch('src.utils.metrics.SentenceTransformer')
    def test_calculate_batch_distances(self, mock_st):
        evaluator = SimilarityEvaluator()
        
        # We need to mock calculate_distance logic or the inner encode logic
        # Simpler to mock calculate_distance if we could, but it's a method on self.
        # So we mock encode again.
        mock_st.return_value.encode.return_value = np.array([[1, 0], [1, 0]]) # identical
        
        dists = evaluator.calculate_batch_distances(["a"], ["a"])
        assert dists == [0.0]

    @patch('src.utils.metrics.SentenceTransformer')
    def test_calculate_batch_distances_mismatch(self, mock_st):
        evaluator = SimilarityEvaluator()
        with pytest.raises(ValueError):
            evaluator.calculate_batch_distances(["a"], ["b", "c"])