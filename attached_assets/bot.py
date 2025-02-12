import os
import logging
import asyncio
from typing import Optional, Dict, List
import aiohttp
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultPhoto,
    BufferedInputFile
)
from aiogram.filters import Command
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in environment variables")

API_BASE_URL = "https://api.rule34.xxx/index.php"
API_TIMEOUT = 30  # seconds
RESULTS_PER_PAGE = 1000  # Максимальное количество результатов
INLINE_RESULTS_LIMIT = 150  # Максимум для Telegram API
MAX_CACHE_ITEMS = 1000  # Максимальное количество кэшированных запросов

# Кэш для хранения результатов поиска
search_cache = {}
CACHE_TIMEOUT = 3600  # 1 час
MAX_CACHE_ITEMS = 1000  # Максимальное количество кэшированных запросов

# Глобальная сессия API
api_session: Optional[aiohttp.ClientSession] = None

async def get_api_session() -> aiohttp.ClientSession:
    """Получение или создание сессии API"""
    global api_session
    if api_session is None or api_session.closed:
        api_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
        )
    return api_session

def clean_old_cache():
    """Очистка старого кэша"""
    current_time = time.time()
    expired_keys = [
        k for k, v in search_cache.items()
        if current_time - v['timestamp'] > CACHE_TIMEOUT
    ]
    for k in expired_keys:
        del search_cache[k]

    # Если кэш всё ещё слишком большой, удаляем самые старые записи
    if len(search_cache) > MAX_CACHE_ITEMS:
        sorted_items = sorted(
            search_cache.items(),
            key=lambda x: x[1]['timestamp']
        )
        for k, _ in sorted_items[:len(search_cache) - MAX_CACHE_ITEMS]:
            del search_cache[k]

async def search_images(query: str, page: int = 0) -> List[Dict]:
    """
    Поиск изображений через API с кэшированием
    """
    cache_key = f"{query}_{page}"
    current_time = time.time()

    # Очищаем старый кэш
    clean_old_cache()

    # Проверяем кэш
    if cache_key in search_cache:
        cached_data = search_cache[cache_key]
        if current_time - cached_data['timestamp'] < CACHE_TIMEOUT:
            logger.info(f"Using cached results for {cache_key}")
            return cached_data['results']

    session = await get_api_session()
    try:
        formatted_tags = query.strip()
        logger.info(f"Searching with tags: {formatted_tags}")

        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": 1,
            "limit": RESULTS_PER_PAGE,
            "pid": page,
            "tags": formatted_tags
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        async with session.get(API_BASE_URL, params=params, headers=headers) as response:
            logger.info(f"API response status: {response.status}")
            if response.status == 200:
                try:
                    data = await response.json(content_type=None)
                    logger.info(f"Received {len(data) if isinstance(data, list) else 0} results")
                    if isinstance(data, list):
                        valid_items = []
                        for item in data:
                            file_url = item.get('file_url', '')
                            if not file_url or not any(file_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                                continue

                            width = int(item.get('width', 0))
                            height = int(item.get('height', 0))
                            if width > 5000 or height > 5000:
                                continue

                            normalized_item = {
                                'file_url': file_url,
                                'preview_url': item.get('preview_url', item.get('sample_url', '')),
                                'sample_url': item.get('sample_url', item.get('preview_url', '')),
                                'width': width,
                                'height': height,
                                'tags': item.get('tags', ''),
                                'score': int(item.get('score', 0))
                            }
                            valid_items.append(normalized_item)

                        # Сохраняем в кэш
                        search_cache[cache_key] = {
                            'results': valid_items,
                            'timestamp': current_time
                        }

                        logger.info(f"Found {len(valid_items)} valid items")
                        return valid_items
                    return []
                except Exception as e:
                    logger.error(f"Error parsing API response: {str(e)}")
                    return []
            else:
                logger.error(f"API error: {response.status}")
                return []
    except asyncio.TimeoutError:
        logger.error("API request timeout")
        return []
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return []
    finally:
        await session.close()


router = Router()

@router.inline_query()
async def inline_search(query: InlineQuery):
    """Обработчик инлайн-запросов с поддержкой пагинации"""
    search_text = query.query.strip()
    offset = int(query.offset) if query.offset else 0
    logger.info(f"Received inline query: {search_text}, offset: {offset}")

    if not search_text:
        return await query.answer(
            results=[],
            switch_pm_text="🔍 Введите тег для поиска",
            switch_pm_parameter="start",
            cache_time=1
        )

    try:
        # Запрашиваем результаты с учетом смещения
        page = offset // RESULTS_PER_PAGE
        results = await search_images(search_text, page)

        if not results:
            return await query.answer(
                results=[],
                switch_pm_text="😕 Ничего не найдено",
                switch_pm_parameter="start",
                cache_time=1
            )

        inline_results = []
        start_idx = offset % RESULTS_PER_PAGE
        end_idx = min(start_idx + INLINE_RESULTS_LIMIT, len(results))

        for idx, item in enumerate(results[start_idx:end_idx], start=offset):
            try:
                file_url = item['file_url']
                thumb_url = item['preview_url']

                result = InlineQueryResultPhoto(
                    id=str(idx),
                    photo_url=file_url,
                    thumbnail_url=thumb_url,
                    photo_width=item['width'] or 100,
                    photo_height=item['height'] or 100,
                    caption=f"🏷 Теги: {item['tags'][:200]}..."
                )
                inline_results.append(result)
            except Exception as e:
                logger.error(f"Error creating inline result {idx}: {str(e)}")
                continue

        # Определяем, есть ли ещё результаты
        next_offset = str(offset + INLINE_RESULTS_LIMIT) if len(results) > end_idx else ""

        logger.info(f"Sending {len(inline_results)} results with next_offset {next_offset}")
        await query.answer(
            results=inline_results,
            next_offset=next_offset,
            cache_time=300,
            is_personal=True
        )

    except Exception as e:
        logger.error(f"Inline search error: {str(e)}")
        await query.answer(
            results=[],
            switch_pm_text="😢 Произошла ошибка",
            switch_pm_parameter="error",
            cache_time=1
        )

if __name__ == "__main__":
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        logger.info("Starting bot...")
        asyncio.run(dp.start_polling(bot))
    finally:
        if api_session:
            await api_session.close()
        logger.info("Bot stopped")