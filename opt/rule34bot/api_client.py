import aiohttp
import logging
from typing import Optional, Dict, List
import asyncio
from config import API_BASE_URL, API_TIMEOUT

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._retries = 3
        self._retry_delay = 1

    async def ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
            )

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def search_items(self, query: str, page: int = 0) -> List[Dict]:
        await self.ensure_session()
        
        try:
            params = {
                "page": "dapi",
                "s": "post",
                "q": "index",
                "json": 1,
                "limit": 100,
                "pid": page,
                "tags": query.strip()
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            for attempt in range(self._retries):
                try:
                    async with self._session.get(
                        API_BASE_URL,
                        params=params,
                        headers=headers
                    ) as response:
                        if response.status == 200:
                            data = await response.json(content_type=None)
                            if not isinstance(data, list):
                                return []

                            return [
                                {
                                    'file_url': item.get('file_url', ''),
                                    'preview_url': item.get('preview_url', ''),
                                    'width': int(item.get('width', 0)),
                                    'height': int(item.get('height', 0))
                                }
                                for item in data
                                if self._validate_item(item)
                            ]
                        elif response.status != 429:  # Skip retry on non-rate-limit errors
                            logger.error(f"API error: {response.status}")
                            return []
                except Exception as e:
                    if attempt == self._retries - 1:
                        raise
                    await asyncio.sleep(self._retry_delay * (attempt + 1))

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def _validate_item(self, item: Dict) -> bool:
        """Validate API response item"""
        if not item.get('file_url'):
            return False

        file_url = item['file_url'].lower()
        if not any(file_url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
            return False

        width = int(item.get('width', 0))
        height = int(item.get('height', 0))
        if width > 5000 or height > 5000:
            return False

        return True
