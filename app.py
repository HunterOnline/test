import logging

from aiogram import Dispatcher
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils import executor
from aiogram.utils.executor import Executor
from aiohttp import web

from data import config
from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, ip
from loader import SSL_CERTIFICATE, ssl_context, db, bot
from utils.set_bot_commands import set_default_commands
from webserver.handler import app, dp
from utils.db_api import db_gino
   

async def on_startup(app):
    await bot.set_webhook(
        url=WEBHOOK_URL,
        certificate=SSL_CERTIFICATE
    )

    webhook = await bot.get_webhook_info()
    logging.info(f"{webhook}")
    import filters
    import middlewares

    filters.setup(dp)
    middlewares.setup(dp)
    
    from utils.notify_admins import on_startup_notify
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()

    print("Готово")
    

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


app.on_startup.append(on_startup)
web.run_app(app, host="0.0.0.0", port=config.WEBHOOK_PORT, ssl_context=ssl_context)
