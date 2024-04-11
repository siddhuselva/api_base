import logging
from .core.config import settings


if settings.DEBUG:
    log_level = logging.DEBUG
else:
    log_level = logging.ERROR

logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
