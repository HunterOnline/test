import logging

from aiogram import Dispatcher

from data.config import ADMINS
from keyboards.default.main_button import main_button


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(chat_id=ADMINS, text='🏥..🚑...МeDbot...loaded...',) # reply_markup=main_button

    except Exception as err:
        logging.exception(err)

