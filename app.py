from loader import db_user
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    try:
        db_user.create_user_table()

    except Exception as e:
        print(e)

    db_user.unload_user_data()

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor

    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
