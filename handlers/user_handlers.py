from copy import deepcopy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command


from database.database import users_db, user_dict_template
from services.file_handling import book
from lexicon.lexicon import LEXICON_RU
from keyboards.pagination_kb import create_pagination_kb
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData

router = Router()


@router.message(Command('start'))
async def process_start(message: Message):
    await message.answer(LEXICON_RU['/start'])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command('help'))
async def process_help(message: Message):
    await message.answer(LEXICON_RU['/help'])


@router.message(Command('beginning'))
async def process_beginning(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_kb('backward', f'{users_db[message.from_user.id]["page"]}/{len(book)}', 'forward'))


@router.message(Command('continue'))
async def process_continue(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_kb('backward', f'{users_db[message.from_user.id]["page"]}/{len(book)}', 'forward'))


@router.message(Command('bookmarks'))
async def process_bookmarks(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(text=LEXICON_RU['bookmarks'], reply_markup=create_bookmarks_keyboard(*users_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON_RU['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def process_forward(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_kb('backward', f'{users_db[callback.from_user.id]["page"]}/{len(book)}', 'forward'))
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_forward(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_kb('backward', f'{users_db[callback.from_user.id]["page"]}/{len(book)}', 'forward'))
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_pages(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(users_db[callback.from_user.id]['page'])
    await callback.answer('страница добавлена в закладки')


@router.callback_query(IsDigitCallbackData())
async def process_bookmark(callback: CallbackQuery):
    await callback.answer('lol??')
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(text=text, reply_markup=create_pagination_kb('backward', f'{users_db[callback.from_user.id]["page"]}/{len(book)}', 'forward'))


@router.callback_query(F.data == 'edit_bookmarks')
async def edit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU[callback.data], reply_markup=create_edit_keyboard(*users_db[callback.from_user.id]['bookmarks']))
    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def process_cancel(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['cancel'])
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def process_del(callback: CallbackQuery):
    await callback.message.answer(text=f'{callback.data}')
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON_RU['bookmarks'], reply_markup=create_bookmarks_keyboard(*users_db[callback.from_user.id]['bookmarks']))
    else:
        await callback.message.edit_text(text=LEXICON_RU['no_bookmarks'])
    await callback.answer()