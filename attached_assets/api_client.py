import aiohttp
import asyncio
from typing import Optional, Dict, List
import logging
from config import API_BASE_URL, API_TIMEOUT

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._retries = 3
        self._retry_delay = 1

    async def ensure_session(self):
        """Создание или получение существующей сессии"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
            )

    async def close(self):
        """Закрытие сессии"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _make_request(self, params: Dict) -> Optional[List[Dict]]:
        """Выполнение запроса с повторными попытками"""
        await self.ensure_session()

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
                        return await response.json(content_type=None)
                    elif response.status == 429:  # Too Many Requests
                        if attempt < self._retries - 1:
                            await asyncio.sleep(self._retry_delay * (attempt + 1))
                            continue
                    logger.error(f"API error: {response.status}")
                    return None
            except Exception as e:
                logger.error(f"Request error: {str(e)}")
                if attempt < self._retries - 1:
                    await asyncio.sleep(self._retry_delay * (attempt + 1))
                    continue
        return None

    async def search_items(self, query: str, page: int = 0) -> List[Dict]:
        """Поиск изображений с фильтрацией результатов"""
        try:
            formatted_tags = query.strip()
            if not formatted_tags:
                return []

            logger.info(f"Searching with tags: {formatted_tags}")

            params = {
                "page": "dapi",
                "s": "post",
                "q": "index",
                "json": 1,
                "limit": 100,
                "pid": page,
                "tags": formatted_tags
            }

            data = await self._make_request(params)

            if not isinstance(data, list):
                return []

            valid_items = []
            for item in data:
                # Проверка и нормализация данных
                file_url = item.get('file_url', '')
                if not file_url or not any(
                    file_url.lower().endswith(ext)
                    for ext in ['.jpg', '.jpeg', '.png', '.gif']
                ):
                    continue

                width = int(item.get('width', 0))
                height = int(item.get('height', 0))
                if width > 5000 or height > 5000:
                    continue

                valid_items.append({
                    'file_url': file_url,
                    'preview_url': item.get('preview_url', ''),
                    'sample_url': item.get('sample_url', ''),
                    'width': width,
                    'height': height,
                    'tags': item.get('tags', ''),
                    'score': int(item.get('score', 0))
                })

            logger.info(f"Found {len(valid_items)} valid items")
            return valid_items

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    async def fetch_data(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Fetches data from the API with error handling
        """
        await self.ensure_session()
        try:
            async with self._session.get(
                f"{API_BASE_URL}/{endpoint}",
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"API error: {response.status} - {await response.text()}")
                    return None
        except Exception as e:
            logger.error(f"Request error: {str(e)}")
            return None