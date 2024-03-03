import os
import pytest


@pytest.fixture
def clear_log():
    """Pytest fixture that clears the contents of a log file.

    This fixture retrieves the project path from the environment variable "PROJECT_PATH" and creates a log file path using the project path. It then opens the log file in write mode, effectively clearing its contents, and yields control.

    Usage:
        This fixture can be used in pytest tests by including it as an argument in the test function.

        Example:
        def test_something(clear_log):
            # Clear the log file before running the test
            ...
    """
    project_path = os.environ.get("PROJECT_PATH")
    log_file = f"{project_path}/root.log"
    with open(log_file, "w"):
        pass
    yield
