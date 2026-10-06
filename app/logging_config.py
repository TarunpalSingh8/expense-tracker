import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """Log to console and to a rotating file in ./logs."""
    os.makedirs("logs", exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        file_handler = RotatingFileHandler("logs/app.log", maxBytes=100_000, backupCount=3)
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        root.addHandler(console)
