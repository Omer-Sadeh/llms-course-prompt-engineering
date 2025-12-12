from unittest.mock import MagicMock, patch

import pytest

from src.utils.llm_client import OllamaClient, start_ollama_server


class TestOllamaClient:
    
    @pytest.fixture
    def mock_ollama_client(self):
        with patch('src.utils.llm_client.ollama.Client') as mock_client_cls:
            mock_instance = MagicMock()
            mock_client_cls.return_value = mock_instance
            yield mock_instance

    def test_init(self, mock_ollama_client):
        client = OllamaClient(model="test-model", temperature=0.5, base_url="http://test:11434")
        assert client.model == "test-model"
        assert client.temperature == 0.5
        # Verify the client library was initialized with the host
        # Note: Depending on implementation, we check if ollama.Client was called
        # The code does: self.client = ollama.Client(host=base_url)
        # So we can check that.

    @patch.object(OllamaClient, '_load_cache', return_value={})
    @patch.object(OllamaClient, '_save_cache')
    def test_generate_success(self, mock_save, mock_load, mock_ollama_client):
        client = OllamaClient()
        # Mock the internal client's generate method
        client.client.generate.return_value = {'response': 'Test response'}
        
        response = client.generate("Hello", system="Sys")
        assert response == "Test response"
        client.client.generate.assert_called_once()
        args = client.client.generate.call_args[1]
        assert args['model'] == "llama3"
        assert args['prompt'] == "Hello"
        assert args['system'] == "Sys"
        assert args['options']['temperature'] == 0.0

    @patch.object(OllamaClient, '_load_cache', return_value={})
    def test_generate_failure(self, mock_load, mock_ollama_client):
        client = OllamaClient()
        client.client.generate.side_effect = Exception("API Error")
        
        response = client.generate("Hello")
        assert "Error: API Error" in response

    def test_check_connection_success(self, mock_ollama_client):
        client = OllamaClient()
        client.client.list.return_value = {}
        assert client.check_connection() is True

    def test_check_connection_failure(self, mock_ollama_client):
        client = OllamaClient()
        client.client.list.side_effect = Exception("Connection Refused")
        assert client.check_connection() is False

    def test_list_models(self, mock_ollama_client):
        client = OllamaClient()
        client.client.list.return_value = {
            'models': [
                {'name': 'llama3'},
                {'name': 'mistral'}
            ]
        }
        models = client.list_models()
        assert "llama3" in models
        assert "mistral" in models
        assert len(models) == 2

    @patch('src.utils.llm_client.subprocess.Popen')
    @patch('src.utils.llm_client.time.sleep')
    @patch.object(OllamaClient, 'check_connection')
    def test_start_ollama_server_success(self, mock_check, mock_sleep, mock_popen):
        # First check fails, second succeeds
        mock_check.side_effect = [False, True]
        
        result = start_ollama_server(max_retries=2)
        assert result is True
        mock_popen.assert_called_once()

    @patch('src.utils.llm_client.subprocess.Popen')
    @patch('src.utils.llm_client.time.sleep')
    @patch.object(OllamaClient, 'check_connection')
    def test_start_ollama_server_failure(self, mock_check, mock_sleep, mock_popen):
        mock_check.return_value = False
        
        result = start_ollama_server(max_retries=1)
        assert result is False
