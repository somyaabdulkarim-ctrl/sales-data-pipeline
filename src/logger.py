import logging
from pathlib import Path

from src.config import LOG_FILE_PATH


Path(LOG_FILE_PATH).parent.mkdir(
    parents=True,
    exist_ok=True
)

logger = logging.getLogger("sales_data_pipeline")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LOG_FILE_PATH)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)