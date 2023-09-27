
from aiogram import types

from data.config import ADMINS
from loader import dp, db_user
from aiogram.dispatcher.filters import Command



@dp.message_handler(Command("download_db"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    await message.answer_document(open("data/user_db.db", "rb"))
