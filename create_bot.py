from aiogram import Bot
from aiogram.bot.api import TelegramAPIServer
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_bot import BOT_TOKEN, LOCAL_SERVER_URL

storage = MemoryStorage()

LOCAL_SERVER = TelegramAPIServer.from_base(LOCAL_SERVER_URL)

bot = Bot(token=BOT_TOKEN, server=LOCAL_SERVER)
dp = Dispatcher(bot, storage=storage)
