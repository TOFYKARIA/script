import os
from typing import Optional

# Bot configuration
BOT_TOKEN: Optional[str] = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in environment variables")

# API configuration
API_BASE_URL = "https://api.rule34.xxx/index.php"
API_TIMEOUT = 30  # seconds

# Search configuration
RESULTS_PER_PAGE = 50
INLINE_RESULTS_LIMIT = 50
DEFAULT_RATING = "explicit"

# Cache configuration
CACHE_TIMEOUT = 3600  # 1 hour
MAX_CACHE_ITEMS = 1000

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = "INFO"

# File paths
LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/bot.log"

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)