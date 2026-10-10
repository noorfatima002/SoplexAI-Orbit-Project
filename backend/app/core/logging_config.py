import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Log to stdout (Docker collects it). Never log secrets, API keys or full emails bodies."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
        force=True,
    )
