from downloader.config import LOG_LOCATION
from loguru import logger

def setup():
    logger.remove(0)
    logger.add(LOG_LOCATION)

def log_err(intuit_tid, msg):
    logger.error(f"intuit_tid: ({intuit_tid}) | {msg}")