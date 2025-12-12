"""
Configuration loader module.
"""
import yaml
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).parent.parent.parent

class LLMConfig(BaseModel):
    model: str = Field(..., min_length=1)
    temperature: float = Field(..., ge=0.0, le=2.0)
    base_url: str = Field(..., pattern=r"^https?://")

class ExperimentConfig(BaseModel):
    dataset_size: int = Field(..., gt=0)
    seed: int = Field(...)
    embedding_model: str = Field(..., min_length=1)

class PathsConfig(BaseModel):
    data: Path
    results: Path
    figures: Path

class Config(BaseModel):
    llm: LLMConfig
    experiment: ExperimentConfig
    paths: PathsConfig

    @classmethod
    def load(cls, config_path: str = "config/settings.yaml") -> 'Config':
        """Load configuration from a YAML file."""
        path = PROJECT_ROOT / config_path
        if not path.exists():
            raise FileNotFoundError(f"Config file not found at {path}")
        
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
            
            # Resolve paths relative to PROJECT_ROOT
            paths_data = data.get('paths', {})
            resolved_paths = {
                'data': PROJECT_ROOT / paths_data.get('data', 'data/dataset.csv'),
                'results': PROJECT_ROOT / paths_data.get('results', 'results/experiments.csv'),
                'figures': PROJECT_ROOT / paths_data.get('figures', 'results/figures')
            }
            data['paths'] = resolved_paths

            return cls(**data)
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML config: {e}")
            raise

# Global configuration instance
try:
    config = Config.load()
except Exception as e:
    logger.critical(f"Failed to load configuration: {e}")
    # We might want to exit here or provide a fallback, but for now we let it fail loudly as per persona
    config = None