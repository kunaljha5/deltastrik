def load_config():
    """
    Placeholder config loader.
    Eventually this will read deltastrik/data/settings.yaml or user config.
    For now, just return a simple dict.
    """
    return {
        "model": "gpt-oss:latest",
        "temperature": 0.7,
        "max_tokens": 1024,
    }
