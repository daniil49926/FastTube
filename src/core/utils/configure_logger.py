import json
import logging
import os

from core.settings import settings

__logger = None

if settings.TESTING:
    __logger = logging.getLogger("test")


def configure_and_get_logger() -> logging.Logger:
    global __logger
    if __logger:
        return __logger

    with open(
        f"{os.path.dirname(os.path.abspath(settings.BASE_DIR))}\\logging_config.json",
        "r",
    ) as cf:
        json_config = json.load(cf)
        logging.config.dictConfig(json_config)

    __logger = logging.getLogger("main")
    return __logger
