from src.config.config import Config


def test_config_loading():
    # This might fail if the file doesn't exist, but we created it.
    config = Config.load("config/settings.yaml")
    assert config.llm.model is not None
    assert config.experiment.dataset_size > 0
    assert config.paths.data is not None
