import os
import pathlib
from typing import Any

import yaml


class Configuration(dict[str, Any]):
    """
    A custom dictionary class for storing configuration settings.

    This class extends the built-in dict class to provide additional functionality for managing
    configuration settings.

    Example usage:
    config = Configuration()
    config['debug'] = True
    config['log_level'] = 'INFO'
    """


def load_config(config_path: str = ".configs") -> dict[str, Any]:
    """Load configuration files from the specified path and return a dictionary with the
    configuration settings.

    Args:
        config_path (str): The path where the configuration files are located. Defaults to
        ".configs".

    Returns:
        dict[str, Any]: A dictionary containing the configuration settings loaded from the files.
    """
    config = Configuration()

    for root, _, files in os.walk(config_path):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                with open(pathlib.Path(root) / file, "r", encoding="utf-8") as file:
                    sub_config = yaml.safe_load(file)
                    config.update(sub_config)

    return config


def get_config() -> dict[str, Any]:
    """Get configuration settings from a file."""
    return load_config()
