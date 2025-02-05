from pathlib import Path

import logging

import datetime

from config import settings


LOGS_DIR = Path(settings.LOGS_DIR)
FORMAT = "%(levelname)-7s| %(module)15s:%(funcName)-20s:%(lineno)-4s | [%(asctime)s] | MSG = %(message)s"
COLORS = {
    "DEBUG":    "\033[36m",  # Cyan
    "INFO":     "\033[32m",  # Green
    "WARNING":  "\033[33m",  # Yellow
    "ERROR":    "\033[31m",  # Red
}


def setup_logs_dir(path: Path):
    path.mkdir(exist_ok=True)


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        rec_copy = super().format(record)
        return COLORS[record.levelname] + rec_copy + "\033[0m" # color reset


class FileFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)


def configure_logger(logger: logging.Logger, level: int = logging.DEBUG):
    setup_logs_dir(LOGS_DIR)
    
    file_handler = logging.FileHandler(f"{LOGS_DIR}/{datetime.date.today()}.log")
    console_handler = logging.StreamHandler()
    
    file_formatter = FileFormatter(FORMAT)
    console_formatter = ColoredFormatter(FORMAT)
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
    logger.getChild("httpcore").setLevel(logging.WARNING)
    logger.getChild("httpx").setLevel(logging.WARNING)