import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

_LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(_LOG_DIR / "errors.log", maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)