from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.file_handling import book
from lexicon.lexicon import LEXICON_RU


def create_bookmarks_keyboard(*args: int):
    kb_builder = InlineKeyboardBuilder()
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(text=f'{button} - {book[button][:100]}', callback_data=str(button)))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU['edit_bookmarks_button'], callback_data='edit_bookmarks'),
                   InlineKeyboardButton(text=LEXICON_RU['cancel'], callback_data='cancel'), width=2)
    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON_RU["del"]} {button} - {book[button][:100]}',
            callback_data=f'{button}del'))
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON_RU['cancel'],
                        callback_data='cancel'))
    return kb_builder.as_markup()