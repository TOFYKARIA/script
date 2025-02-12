import os
import logging
from typing import Optional, Dict, List
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import (
    InlineQuery,
    InlineQueryResultPhoto
)
from config import BOT_TOKEN, API_TIMEOUT, INLINE_RESULTS_LIMIT
from api_client import APIClient

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='/opt/rule34bot/logs/bot.log'
)
logger = logging.getLogger(__name__)

# Инициализация компонентов
router = Router()
api_client = APIClient()

@router.inline_query()
async def inline_search(query: InlineQuery):
    """Обработчик inline-запросов"""
    search_text = query.query.strip()
    offset = int(query.offset) if query.offset else 0
    
    if not search_text:
        return await query.answer(
            results=[],
            switch_pm_text="🔍 Введите поисковый запрос",
            switch_pm_parameter="start"
        )

    try:
        results = await api_client.search_items(search_text, offset // 100)
        
        if not results:
            return await query.answer(
                results=[],
                switch_pm_text="😕 Ничего не найдено",
                switch_pm_parameter="start"
            )

        inline_results = []
        start_idx = offset % 100
        end_idx = min(start_idx + INLINE_RESULTS_LIMIT, len(results))

        for idx, item in enumerate(results[start_idx:end_idx], start=offset):
            try:
                result = InlineQueryResultPhoto(
                    id=str(idx),
                    photo_url=item['file_url'],
                    thumbnail_url=item['preview_url'],
                    photo_width=item['width'],
                    photo_height=item['height']
                )
                inline_results.append(result)
            except Exception as e:
                logger.error(f"Error creating inline result: {str(e)}")
                continue

        next_offset = str(offset + INLINE_RESULTS_LIMIT) if len(results) > end_idx else ""
        
        await query.answer(
            results=inline_results,
            next_offset=next_offset,
            cache_time=300,
            is_personal=True
        )

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        await query.answer(
            results=[],
            switch_pm_text="😢 Произошла ошибка",
            switch_pm_parameter="error"
        )

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    finally:
        if hasattr(api_client, 'close'):
            await api_client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
