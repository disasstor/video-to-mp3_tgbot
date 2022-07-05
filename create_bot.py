from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_bot import BOT_TOKEN

storage = MemoryStorage()

bot = Bot(token=str(BOT_TOKEN))
dp = Dispatcher(bot, storage=storage)
