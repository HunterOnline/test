import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_button import main_button
from loader import dp, db_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f'Привіт, {message.from_user.full_name}!\n🏥..🚑...МeDbot на зв\'язку!\n В мене поки що невеликий функціонал, працюю в тестовому режимі!',
        reply_markup=main_button)
    user_id = message.from_user.id
    users = db_user.buf_user_data
    if user_id in users:
        logging.info(f"{message.from_user.full_name} -> уже есть БД_S")
    else:
        try:
            user_id = message.from_user.id
            name = message.from_user.get_mention()
            db_user.add_user(user_id, name)
            db_user.unload_user_data()
            logging.info(f"{message.from_user.full_name} -> записани в БД")

        except Exception as e:
            print(e)
