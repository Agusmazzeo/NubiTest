import logging
import logging.config
import os


def log_path(filename: str):
    log_dir = os.environ.get("LOG_DIR", ".")
    filename = filename + ".log"
    return os.sep.join((log_dir, filename))


def configure_logger(name: str) -> logging.Logger:

    console_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s")
    file_formatter = logging.Formatter(
        fmt='{"time":"%(asctime)s", "level": "%(levelname)s", "name":"%(name)s", "msg":"%(message)s"}')
    error_formatter = logging.Formatter(
        fmt='{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "file": "%(pathname)s",  "line": %(lineno)s, "msg": "%(message)s"}')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(
        "DEBUG" if os.environ.get("DEBUG_MODE") else "INFO")

    file_handler = logging.FileHandler(filename=log_path(
        filename=name), mode="a+", encoding="latin1", delay=None)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel("INFO")

    error_log_handler = logging.FileHandler(filename=log_path(
        filename=f"{name}_error"), mode="a+", encoding="latin1", delay=None)
    error_log_handler.setFormatter(error_formatter)
    error_log_handler.setLevel("WARNING")

    logger = logging.getLogger(name=name)
    logger.setLevel("DEBUG")

    for handler in [console_handler, file_handler, error_log_handler]:
        logger.addHandler(handler)
    return logger