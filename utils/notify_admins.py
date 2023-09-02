import logging

from aiogram import Dispatcher

from data.config import admins
from keyboards.default.main_button import main_button


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text='🏥..🚑...МeDbot...loaded...', reply_markup=main_button)

        except Exception as err:
            logging.exception(err)


# async def on_startup_menu():
#     for users in db_user.select_all_sets():
#
#         try:
#
#             await dp.bot.send_message(text='#@Ebash_new_bot....loaded...menu', chat_id=users[1], reply_markup=menu)
#
#         except Exception as err:
#
#             logging.exception(err)
