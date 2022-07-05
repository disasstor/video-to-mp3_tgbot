from aiogram.utils import executor
from create_bot import dp
import logging
from handlers.main_handler import register_handlers_main

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Bot online')


register_handlers_main(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
