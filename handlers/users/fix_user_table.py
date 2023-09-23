
from aiogram import types

from data.config import ADMINS
from loader import dp, db_user
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("count_user"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    await message.answer(f'Всего значений в БД User: {db_user.count_user()[0][0]}')


@dp.message_handler(Command("del_all_users"), user_id=ADMINS, )
async def del_all_users(message: types.Message):
    db_user.delete_all()
    db_user.unload_user_data()
    await message.answer('БД Users Удалено ВСЕХ ПОЛЬЗОВАТЕЛЕЙ')


@dp.message_handler(Command("arr_user"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    user = [f"{str(i[0])}. {i[2]}" for i in db_user.select_all_sets()]
    await message.answer("\n".join(user))