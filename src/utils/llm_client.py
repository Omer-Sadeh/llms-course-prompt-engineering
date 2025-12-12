"""
Ollama Client Wrapper.
"""
import hashlib
import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional

import ollama

logger = logging.getLogger(__name__)

def start_ollama_server(max_retries: int = 5) -> bool:
    """
    Attempts to start the Ollama server and waits for it to become responsive.
    
    Args:
        max_retries: Number of times to check for connection after starting.
        
    Returns:
        True if started and connected, False otherwise.
    """
    logger.info("Attempting to start Ollama server...")
    try:
        # Start ollama serve in the background
        # Redirect stdout/stderr to devnull to avoid cluttering console, or log file
        subprocess.Popen(
            ["ollama", "serve"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        # Wait for it to come up
        client = OllamaClient()
        for i in range(max_retries):
            logger.info(f"Waiting for Ollama server... ({i+1}/{max_retries})")
            time.sleep(2)
            if client.check_connection():
                logger.info("Ollama server started successfully.")
                return True
                
        logger.error("Timed out waiting for Ollama server to start.")
        return False
        
    except FileNotFoundError:
        logger.error("Ollama executable not found. Please install Ollama.")
        return False
    except Exception as e:
        logger.error(f"Failed to start Ollama server: {e}")
        return False

class OllamaClient:
    """Wrapper for Ollama API interaction with Caching."""

    def __init__(self, model: str = "llama3", temperature: float = 0.0, base_url: str = "http://localhost:11434", cache_dir: str = ".cache"):
        self.model = model
        self.temperature = temperature
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "llm_cache.json"
        self.cache = self._load_cache()

        # The official python client uses OLLAMA_HOST env var, but we can also set it if needed.
        # For now, we rely on the default behavior or env vars.
        # If we needed to change the host, we would use ollama.Client(host=base_url)
        try:
            self.client = ollama.Client(host=base_url)
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama Client with specific host: {e}. Using default.")
            self.client = ollama

    def _load_cache(self) -> Dict[str, str]:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
                return {}
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")

    def _get_cache_key(self, prompt: str, system: Optional[str]) -> str:
        key_content = f"{self.model}_{self.temperature}_{prompt}_{system}"
        return hashlib.md5(key_content.encode()).hexdigest()

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Generates a response from the model with caching.

        Args:
            prompt: The user prompt.
            system: Optional system prompt.

        Returns:
            The generated text response.
        """
        cache_key = self._get_cache_key(prompt, system)
        if cache_key in self.cache:
            logger.info("Cache hit for prompt.")
            return self.cache[cache_key]

        try:
            options: dict[str, Any] = {
                "temperature": self.temperature,
            }
            
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                system=system,
                options=options,
                stream=False
            )
            
            result = str(response['response'])
            self.cache[cache_key] = result
            self._save_cache()
            return result
            
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {e}")
            return f"Error: {e}"

    def check_connection(self) -> bool:
        """Checks if the Ollama server is reachable."""
        try:
            self.client.list()
            return True
        except Exception:
            # logger.error(f"Ollama connection failed: {e}") # Reduce noise during startup check
            return False

    def list_models(self) -> list[str]:
        """Lists available models."""
        try:
            response = self.client.list()
            # logger.info(f"Ollama list response: {response}") # Uncomment for debugging
            
            models: list[str] = []
            if 'models' in response:
                for m in response['models']:
                    # m could be a dict or an object
                    if isinstance(m, dict):
                        models.append(str(m.get('name', m.get('model', str(m)))))
                    else:
                        # Try to access 'name' or 'model' attribute if it's an object
                        models.append(str(getattr(m, 'name', getattr(m, 'model', str(m)))))
            return models
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
