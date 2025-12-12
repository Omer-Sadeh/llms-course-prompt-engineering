import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.experiment_runner import ExperimentRunner

class TestExperimentRunner:

    @pytest.fixture
    def mock_deps(self):
        mock_llm = MagicMock()
        mock_evaluator = MagicMock()
        mock_generator = MagicMock()
        
        # Setup generator mock
        mock_generator.generate_dataset.return_value = [
            {'question': 'q1', 'answer': 'a1'},
            {'question': 'q2', 'answer': 'a2'}
        ]
        
        return mock_llm, mock_evaluator, mock_generator

    def test_init(self, mock_deps):
        llm, evaluator, generator = mock_deps
        runner = ExperimentRunner(llm_client=llm, evaluator=evaluator, generator=generator)
        
        assert runner.llm == llm
        assert runner.evaluator == evaluator
        assert runner.generator == generator
        assert len(runner.dataset) == 2
        # Verify few shot examples were also generated (dataset size 4 asked in code)
        assert generator.generate_dataset.call_count == 2 

    def test_strategies(self, mock_deps):
        llm, evaluator, generator = mock_deps
        runner = ExperimentRunner(llm_client=llm, evaluator=evaluator, generator=generator)
        
        item = {'question': 'Is A B?', 'answer': 'Yes'}
        
        # Test Baseline
        runner._strategy_baseline(item)
        llm.generate.assert_called_with(prompt='Is A B?')
        
        # Test Basic
        runner._strategy_basic(item)
        assert "system" in llm.generate.call_args[1]
        
        # Test COT
        runner._strategy_cot(item)
        assert "step by step" in llm.generate.call_args[1]['prompt']

    def test_run_all_experiments(self, mock_deps):
        llm, evaluator, generator = mock_deps
        # Mock responses
        llm.generate.return_value = "Model Response"
        evaluator.calculate_distance.return_value = 0.1
        
        runner = ExperimentRunner(llm_client=llm, evaluator=evaluator, generator=generator)
        
        # Patch save_results to avoid filesystem writes
        with patch.object(runner, '_save_results') as mock_save:
            df = runner.run_all_experiments()
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2 * 4 # 2 items * 4 strategies
            assert "vector_distance" in df.columns
            assert "latency" in df.columns
            mock_save.assert_called_once()

    def test_process_single_item(self, mock_deps):
        llm, evaluator, generator = mock_deps
        runner = ExperimentRunner(llm_client=llm, evaluator=evaluator, generator=generator)
        
        strategy_func = MagicMock(return_value="Output")
        evaluator.calculate_distance.return_value = 0.5
        
        result = runner._process_single_item(
            {'question': 'q', 'answer': 'a'},
            "TestStrategy",
            strategy_func
        )
        
        assert result['strategy'] == "TestStrategy"
        assert result['model_output'] == "Output"
        assert result['vector_distance'] == 0.5
        strategy_func.assert_called_once()
