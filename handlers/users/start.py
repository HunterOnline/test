from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_button import main_button
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привіт, {message.from_user.full_name}!\n🏥..🚑...МeDbot на зв\'язку!\n В мене поки що невеликий функціонал, працюю в тестовому режимі!' , reply_markup=main_button)
