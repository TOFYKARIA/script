from aiogram import types
from aiogram.fsm.context import FSMContext
import logging
from typing import Dict
from api_client import APIClient
from keyboards import get_navigation_keyboard, get_item_keyboard

# Cache for search results
search_cache: Dict[int, Dict] = {}

async def cmd_start(message: types.Message):
    """
    Handles /start command
    """
    logging.info(f"Received /start command from user {message.from_user.id}")
    await message.answer(
        "👋 Привет! Я бот для поиска информации.\n"
        "Используйте команду /search <запрос> для поиска."
    )
    logging.info(f"Sent welcome message to user {message.from_user.id}")

async def cmd_search(message: types.Message, api_client: APIClient):
    """
    Handles /search command with dependency injection
    """
    logging.info(f"Received /search command from user {message.from_user.id} with text: {message.text}")
    query = message.text.replace('/search', '').strip()
    if not query:
        await message.answer("❌ Пожалуйста, укажите поисковый запрос!")
        return

    try:
        # Fetch results from API
        logging.info(f"Fetching results for query: {query}")
        results = await api_client.search_items(query)

        if not results:
            await message.answer("😕 По вашему запросу ничего не найдено.")
            return

        # Cache results
        search_cache[message.from_user.id] = {
            "query": query,
            "page": 1,
            "results": results
        }

        # Send first result
        result = results[0]
        await message.answer(
            f"🔍 Найдено: {result['title']}\n"
            f"📝 Описание: {result['description'][:200]}...",
            reply_markup=get_navigation_keyboard(1, len(results) > 1)
        )
        logging.info(f"Sent search results to user {message.from_user.id}")

    except Exception as e:
        logging.error(f"Search error for user {message.from_user.id}: {str(e)}")
        await message.answer("😢 Произошла ошибка при поиске. Попробуйте позже.")

async def callback_navigate(call: types.CallbackQuery, api_client: APIClient):
    """
    Handles navigation callbacks with dependency injection
    """
    logging.info(f"Received navigation callback from user {call.from_user.id} with data: {call.data}")
    user_id = call.from_user.id

    if user_id not in search_cache:
        await call.answer("❌ Поиск устарел. Сделайте новый запрос.")
        return

    data = call.data.split("_")
    if len(data) != 2 or not data[1].isdigit():
        await call.answer("❌ Некорректные данные")
        return

    page = int(data[1])
    cache = search_cache[user_id]

    # Fetch new page if needed
    if len(cache["results"]) < page:
        new_results = await api_client.search_items(cache["query"], page)
        if new_results:
            cache["results"].extend(new_results)

    if page <= len(cache["results"]):
        result = cache["results"][page - 1]
        await call.message.edit_text(
            f"🔍 Найдено: {result['title']}\n"
            f"📝 Описание: {result['description'][:200]}...",
            reply_markup=get_navigation_keyboard(
                page,
                page < len(cache["results"])
            )
        )
        logging.info(f"Updated search results for user {user_id} to page {page}")
    else:
        await call.answer("❌ Больше результатов нет")