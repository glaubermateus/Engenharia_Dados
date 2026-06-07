import logging
from pathlib import Path
from datetime import datetime

# =========================================
# LOG DIRECTORY
# =========================================

log_dir = Path("logs")

log_dir.mkdir(exist_ok=True)

# =========================================
# LOGGER
# =========================================

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            f"logs/etl_{datetime.now().strftime(format = '%d%m%Y_%H%M')}.log"
        ),

        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)