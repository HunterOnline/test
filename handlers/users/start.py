import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_button import main_button
from loader import dp
from utils.db_api import quick_commands

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f'Привіт, {message.from_user.full_name}!\n🏥..🚑...МeDbot на зв\'язку!\n В мене поки що невеликий функціонал, працюю в тестовому режимі!',
        reply_markup=main_button)
    print (await quick_commands.select_all_users())
    try:
            user_id = message.from_user.id
            name = message.from_user.get_mention()
            await quick_commands.add_user(user_id, name)

            logging.info(f"{message.from_user.full_name} -> записани в БД")

    except Exception as e:
            print(e)
