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
RESULTS_PER_PAGE = 100
INLINE_RESULTS_LIMIT = 50

# Cache configuration
CACHE_TIMEOUT = 3600  # 1 hour
MAX_CACHE_ITEMS = 1000

# Ensure logs directory exists
os.makedirs("/opt/rule34bot/logs", exist_ok=True)
