import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from filters import IsAdminFilter, MemberCanRestrictFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bot = Bot(token = TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)



dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)