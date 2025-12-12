from unittest.mock import patch

import pandas as pd
import pytest

from src.analysis import ResultAnalyzer


class TestResultAnalyzer:
    
    @pytest.fixture
    def mock_df(self):
        return pd.DataFrame({
            'strategy': ['A', 'A', 'B', 'B'],
            'vector_distance': [0.1, 0.2, 0.5, 0.6]
        })

    @patch('src.analysis.pd.read_csv')
    @patch('src.analysis.plt')
    @patch('src.analysis.sns')
    def test_generate_report(self, mock_sns, mock_plt, mock_read_csv, mock_df, tmp_path):
        mock_read_csv.return_value = mock_df
        
        # Point to a dummy file
        dummy_results = tmp_path / "results.csv"
        dummy_results.touch()
        
        analyzer = ResultAnalyzer(results_path=dummy_results)
        # Override output dir to tmp_path
        analyzer.output_dir = tmp_path
        
        analyzer.generate_report()
        
        # Verify CSV loading
        mock_read_csv.assert_called_once()
        
        # Verify Plots
        assert mock_plt.figure.call_count == 2
        assert mock_sns.barplot.call_count == 1
        assert mock_sns.violinplot.call_count == 1
        assert mock_plt.savefig.call_count == 2
        
        # Verify stats csv saved
        assert (tmp_path / "summary_stats.csv").exists()

    def test_load_results_not_found(self, tmp_path):
        non_existent = tmp_path / "fake.csv"
        analyzer = ResultAnalyzer(results_path=non_existent)
        with pytest.raises(FileNotFoundError):
            analyzer.load_results()
