from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


def create_pagination_kb(*buttons):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=LEXICON_RU[button] if button in LEXICON_RU else button,
                                          callback_data=button) for button in buttons])
    return kb_builder.as_markup()