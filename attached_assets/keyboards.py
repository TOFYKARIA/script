from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_navigation_keyboard(page: int, has_next: bool) -> InlineKeyboardMarkup:
    """
    Creates navigation keyboard with prev/next buttons
    """
    builder = InlineKeyboardBuilder()

    if page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=f"page_{page-1}"
        )

    if has_next:
        builder.button(
            text="Вперед ➡️",
            callback_data=f"page_{page+1}"
        )

    builder.adjust(2)
    return builder.as_markup()

def get_item_keyboard(item_id: str) -> InlineKeyboardMarkup:
    """
    Creates keyboard for individual items
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📌 Подробнее",
        callback_data=f"details_{item_id}"
    )
    return builder.as_markup()