import logging
import os
import pathlib
import yaml
import logging.config

logger = logging.getLogger(__file__)

config = None

DEFAULT_CONFIG_PATH = str(pathlib.Path(os.environ.get("PROJECT_PATH", "")) / ".configs")
config_path = None


def set_config_path(config_path_: str = None):
    global config_path
    config_path = config_path_


def get_config_path() -> str:
    global config_path
    if config_path is None:
        config_path = str(pathlib.Path(os.environ.get("PROJECT_PATH", "")) / ".configs")
    return config_path


def load_config_from_yaml(file_path: str) -> dict[str, any]:
    """Loads a YAML configuration file and returns it as a dictionary.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict[str, any]: The loaded configuration as a dictionary.

    Examples:
        >>> load_config_from_yaml("config.yaml")
        {'key1': 'value1', 'key2': 'value2', ...}

    Note:
        - This function assumes that the specified `file_path` points to a valid YAML file.
        - It uses the `yaml.safe_load` function to safely load the YAML content as a dictionary.
        - The loaded configuration is returned as a dictionary.

    Raises:
        None.
    """
    logger.debug("--------injecting configuration from file %s--------", file_path)
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
        return config


def load_logging_config(file_path: str = "logging.ini") -> None:
    """Loads a logging configuration from a specified file.

    Args:
        file_path (str, optional): The path to the logging configuration file. Defaults to "logging.ini".

    Returns:
        None

    Examples:
        >>> load_logging_config()
        (Loads the logging configuration from the default file "logging.ini")

        >>> load_logging_config("custom_logging.ini")
        (Loads the logging configuration from the file "custom_logging.ini")

    Note:
        - This function uses the `logging.config.fileConfig` method to load the logging configuration from the specified file.
        - If no `file_path` is provided, the default value "logging.ini" is used.
        - The function does not return any value.

    Raises:
        None.
    """
    log_config_file = f"{file_path}"
    logging.config.fileConfig(log_config_file)


def load_config_from_files(config_path: str) -> dict[str, any]:
    """Loads configuration files from the specified directory and returns a merged configuration
    dictionary.

    Args:
        config_path (str): The path to the directory containing the configuration files.

    Returns:
        dict[str, any]: The merged configuration dictionary.

    Examples:
        >>> load_config_from_files("config_directory")
        {'key1': 'value1', 'key2': 'value2', ...}

    Note:
        - This function assumes that the `config_path` argument points to a valid directory.
        - It uses the `os.walk` function to traverse through the directory and find configuration files.
        - The `handlers` dictionary maps file extensions to corresponding loader functions.
        - For each file found, the function determines its file type based on the extension and uses the corresponding loader function to load the configuration.
        - The loaded configuration dictionaries are merged into a single dictionary.
        - The merged configuration dictionary is returned.

    Raises:
        None.
    """
    config_files = os.walk(config_path)
    config = {}
    handlers = {
        ".yaml": load_config_from_yaml,
        ".yml": load_config_from_yaml,
        # "logging.ini": load_logging_config,
    }
    for dir_path, dir_names, files in config_files:
        for file in files:
            abs_path = f"{dir_path}/{file}"
            file_type = str(pathlib.Path(abs_path).suffix)
            if file_type in handlers:
                loader = handlers[file_type]
                config_ = loader(abs_path)
                config |= config_
                logger.debug("config from file %s:", abs_path)
                logger.debug("%s", config_)
    return config


def inject_config_to_env(config_path: str = None) -> dict[str, any] | None:
    """Injects configuration values into the environment variables and returns the loaded
    configuration dictionary.

    Args:
        config_path (str, optional): The path to the directory containing the configuration files. If not provided, the function assumes that the environment variable "PROJECT_PATH" is set and uses it to construct the default configuration directory path. Defaults to None.

    Returns:
        dict[str, any] or None: The loaded configuration dictionary. Returns None if no configuration directory is specified and the "PROJECT_PATH" environment variable is not set.

    Examples:
        >>> inject_config_to_env()
        {'key1': 'value1', 'key2': 'value2', ...}

        >>> inject_config_to_env("custom_config_directory")
        {'key1': 'value1', 'key2': 'value2', ...}

    Note:
        - If the `config_path` argument is not provided, the function assumes that the "PROJECT_PATH" environment variable is set and constructs the default configuration directory path by appending ".configs" to the value of "PROJECT_PATH".
        - The function uses the `load_config_from_files` function to load the configuration files from the specified or default directory.
        - Each key-value pair in the loaded configuration dictionary is injected into the environment variables, with the key converted to uppercase.
        - The loaded configuration dictionary is returned.
        - If no configuration directory is specified and the "PROJECT_PATH" environment variable is not set, the function returns None.

    Raises:
        None.
    """
    logger.debug("--------injecting configuration to environment--------")
    if config_path is None:
        config_path = get_config_path()
    config = load_config_from_yaml(config_path)
    logger.info(config)
    for key, val in config.items():
        if val is not None:
            os.environ[key.upper()] = str(val)
    return config


def set_config(new_config: dict[str, any] = None) -> dict[str, any]:
    global config
    config = new_config
    return config


def load_config(config_path: str = None) -> dict[str, any]:
    global config
    if config_path is None:
        config_path = get_config_path()
    config = load_config_from_files(config_path)
    additional_env_path = str(pathlib.Path(config_path) / "env.yaml")
    if os.path.isfile(additional_env_path):
        _ = inject_config_to_env(additional_env_path)
    return config


def get_config() -> dict[str, any]:
    global config
    if config is None:
        config = load_config(get_config_path())
    return config
