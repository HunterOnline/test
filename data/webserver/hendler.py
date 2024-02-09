import aiohttp
from aiogram.dispatcher.webhook import get_new_configured_app

from aiohttp import web

from data import config
import handlers

import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,
                    )


async def post_webhook(request):
    request: aiohttp.web.Request

    post_data = await request.post()
    logging.info(f"{post_data=}")

    return web.json_response({"ok": True})


async def get_webhook(request):
    request: aiohttp.web.Request

    get_data = request.rel_url.query
    for key, value in get_data.items():
        logging.info(f"{key}: {value}")

    return web.json_response({"ok": True})

dp = handlers.dp
app = get_new_configured_app(dispatcher=dp, path=config.WEBHOOK_PATH)

app.router.add_post('/myapp', post_webhook)
app.router.add_get('/myapp', get_webhook)
