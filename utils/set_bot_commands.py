from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("arr_user", "Массив юзеров(Admin)"),
        types.BotCommand("count_user", "Счетчик юзеров (Admin)"),
        types.BotCommand("download_db", "Скачать DB (Admin)")
    ])
