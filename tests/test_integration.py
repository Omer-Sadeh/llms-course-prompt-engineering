"""
Integration tests for the Prompt Engineering Analysis workflow.
"""
from unittest.mock import MagicMock

import pytest

from src.config.config import config
from src.experiment_runner import ExperimentRunner
from src.utils.data_generator import SyllogismGenerator
from src.utils.llm_client import OllamaClient
from src.utils.metrics import SimilarityEvaluator


@pytest.fixture
def mock_llm_client():
    client = MagicMock(spec=OllamaClient)
    client.check_connection.return_value = True
    client.generate.return_value = "Yes, therefore it is true."
    return client

@pytest.fixture
def mock_evaluator():
    evaluator = MagicMock(spec=SimilarityEvaluator)
    evaluator.evaluate.return_value = 0.1
    return evaluator

def test_full_experiment_workflow(mock_llm_client, mock_evaluator):
    """
    Test the complete workflow from experiment execution to result generation.
    """
    # Use a small dataset for integration test
    original_size = config.experiment.dataset_size
    config.experiment.dataset_size = 2
    
    try:
        generator = SyllogismGenerator(seed=42)
        runner = ExperimentRunner(llm_client=mock_llm_client, evaluator=mock_evaluator, generator=generator)
        
        # Run experiments
        df = runner.run_all_experiments()
        
        # Verify Results structure
        assert not df.empty
        assert "strategy" in df.columns
        assert "vector_distance" in df.columns
        assert len(df) >= 2 * 4 # 2 items * 4 strategies (Baseline, Basic, Few-Shot, CoT)
        
        # Verify interactions
        assert mock_llm_client.generate.called
        assert mock_evaluator.evaluate.called
        
    finally:
        config.experiment.dataset_size = original_size
