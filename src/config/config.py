"""
Configuration loader module.
"""
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent

@dataclass
class LLMConfig:
    model: str
    temperature: float
    base_url: str

@dataclass
class ExperimentConfig:
    dataset_size: int
    seed: int
    embedding_model: str

@dataclass
class PathsConfig:
    data: Path
    results: Path
    figures: Path

@dataclass
class Config:
    llm: LLMConfig
    experiment: ExperimentConfig
    paths: PathsConfig

    @classmethod
    def load(cls, config_path: str = "config/settings.yaml") -> 'Config':
        """Load configuration from a YAML file."""
        path = PROJECT_ROOT / config_path
        if not path.exists():
            raise FileNotFoundError(f"Config file not found at {path}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            
        return cls(
            llm=LLMConfig(**data['llm']),
            experiment=ExperimentConfig(**data['experiment']),
            paths=PathsConfig(
                data=PROJECT_ROOT / data['paths']['data'],
                results=PROJECT_ROOT / data['paths']['results'],
                figures=PROJECT_ROOT / data['paths']['figures']
            )
        )

# Global configuration instance
try:
    config = Config.load()
except Exception as e:
    print(f"Warning: Could not load default config: {e}")
    config = None
