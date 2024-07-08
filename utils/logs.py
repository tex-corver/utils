import dataclasses
import json
import logging
import os
from typing import Any
from . import configuration, dictionary
from .values import parsers

lib_config = configuration.load_config()

DEFAULT_LOG_CONFIG = {
    "format": {
        "inline": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "datatime": "%Y-%m-%d %H:%M:%S",
    },
    "metadata": {
        "fixed_keys": {
            "application",
            "environment",
            "host",
        },
        "keys": {}
    },
    "logger": {
        "file_name": f"{os.environ.get("SERVICE","")}.log",
        "file_mode": "a",
        "level": "INFO",
        "verbose": False,
        "outputs": [
            "stdout", "file",
        ]
    }
}


def get_config() -> dict[str, Any]:
    return lib_config.get("log", {})

def load_config() -> dict[str, Any]:
    global lib_config

    lib_config["log"] = dictionary.merge_dicts(
        DEFAULT_LOG_CONFIG,
        lib_config.get("log", {}),
    )

    lib_config["log"]["metadata"]["keys"] = set(
        lib_config["log"]["metadata"].get("keys", set())
    )
