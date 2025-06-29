# Import logging configuration
from logging.config import dictConfig
import logging
from pydantic import BaseModel
from typing import ClassVar


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "qfaascore"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: ClassVar[int] = 1
    disable_existing_loggers: ClassVar[bool] = False
    formatters: ClassVar[dict] = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: ClassVar[dict] = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: ClassVar[dict] = {
        "qfaascore": {"handlers": ["default"], "level": LOG_LEVEL},
    }

# Config logging
dictConfig({
    "version": LogConfig.version,
    "disable_existing_loggers": LogConfig.disable_existing_loggers,
    "formatters": LogConfig.formatters,
    "handlers": LogConfig.handlers,
    "loggers": LogConfig.loggers,
})
logger = logging.getLogger("qfaascore")