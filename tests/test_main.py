import pytest
from unittest.mock import MagicMock, patch
import sys
from src.main import main

class TestMain:

    @patch('src.main.OllamaClient')
    @patch('src.main.ExperimentRunner')
    @patch('src.main.ResultAnalyzer')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('sys.argv', ['main.py'])
    def test_main_success(self, mock_print, mock_input, mock_analyzer, mock_runner, mock_client):
        # Setup mocks
        client_instance = mock_client.return_value
        client_instance.check_connection.return_value = True
        client_instance.list_models.return_value = ['llama3']
        
        mock_input.return_value = "1" # Select first model
        
        main()
        
        # Verify flow
        client_instance.check_connection.assert_called()
        client_instance.list_models.assert_called()
        mock_runner.return_value.run_all_experiments.assert_called_once()
        mock_analyzer.return_value.generate_report.assert_called_once()

    @patch('src.main.OllamaClient')
    @patch('src.main.ExperimentRunner')
    @patch('src.main.ResultAnalyzer')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('sys.argv', ['main.py'])
    def test_main_invalid_selection_then_default(self, mock_print, mock_input, mock_analyzer, mock_runner, mock_client):
        # Setup mocks
        client_instance = mock_client.return_value
        client_instance.check_connection.return_value = True
        client_instance.list_models.return_value = ['llama3']
        
        # First input invalid, second input empty (default)
        mock_input.side_effect = ["99", ""] 
        
        # We need to loop manually if the code loops?
        # Looking at src/main.py, it does NOT loop. It just warns and continues with default.
        # "Invalid input. Using default model." or "Invalid selection. Using default model."
        
        mock_input.return_value = "99" # Invalid selection
        
        main()
        
        # Verify it ran with default model (logic handles this)
        mock_runner.return_value.run_all_experiments.assert_called_once()
        
    @patch('src.main.OllamaClient')
    @patch('src.main.ExperimentRunner')
    @patch('src.main.ResultAnalyzer')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('sys.argv', ['main.py'])
    def test_main_empty_selection(self, mock_print, mock_input, mock_analyzer, mock_runner, mock_client):
        client_instance = mock_client.return_value
        client_instance.check_connection.return_value = True
        client_instance.list_models.return_value = ['llama3']
        
        mock_input.return_value = "" # Default
        
        main()
        
        mock_runner.return_value.run_all_experiments.assert_called_once()

    @patch('src.main.OllamaClient')
    @patch('src.main.start_ollama_server')
    @patch('sys.argv', ['main.py'])
    def test_main_no_ollama(self, mock_start, mock_client):
        client_instance = mock_client.return_value
        client_instance.check_connection.return_value = False
        mock_start.return_value = False # Failed to start
        
        with pytest.raises(SystemExit):
            main()
            
        mock_start.assert_called_once()

    @patch('src.main.OllamaClient')
    @patch('sys.argv', ['main.py'])
    def test_main_no_models(self, mock_client):
        client_instance = mock_client.return_value
        client_instance.check_connection.return_value = True
        client_instance.list_models.return_value = []
        
        with pytest.raises(SystemExit):
            main()

    @patch('src.main.OllamaClient')
    @patch('src.main.ExperimentRunner')
    @patch('builtins.input')
    @patch('sys.argv', ['main.py'])
    def test_main_experiment_failure(self, mock_input, mock_runner, mock_client):
        client_instance = mock_client.return_value
        client_instance.check_connection.return_value = True
        client_instance.list_models.return_value = ['llama3']
        mock_input.return_value = "1"
        
        mock_runner.return_value.run_all_experiments.side_effect = Exception("Run failed")
        
        with pytest.raises(SystemExit):
            main()
