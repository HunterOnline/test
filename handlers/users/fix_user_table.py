from aiogram import types

from data.config import ADMINS
from loader import dp
from aiogram.dispatcher.filters import Command
from utils.db_api import quick_commands
from utils.db_api.db_gino import db


@dp.message_handler(Command("count_user"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    await message.answer(f'Всего значений в БД User: {await quick_commands.count_users()}')


@dp.message_handler(Command("del_all_users"), user_id=ADMINS, )
async def del_all_users(message: types.Message):
    await db.gino.drop_all()
    await message.answer('БД Users Удалено ВСЕХ ПОЛЬЗОВАТЕЛЕЙ')


@dp.message_handler(Command("arr_user"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    users = await quick_commands.select_all_users()
    mess_string = [f"{num}. {str(i['name'])}" for num, i in enumerate(users, start=1)]
    await message.answer(("\n".join(mess_string)))
