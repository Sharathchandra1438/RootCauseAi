import json
import logging
import sys
from datetime import datetime, timezone

SERVICE_NAME = "inventory-service"


class JsonFormatter(logging.Formatter):
    """Turns a log record into one line of JSON."""

    def format(self, record):
        log = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "service": SERVICE_NAME,
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "fields"):
            log.update(record.fields)

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log)

def get_logger():
    logger = logging.getLogger(SERVICE_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger