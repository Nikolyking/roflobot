import logging
import os
from dotenv import load_dotenv
import telebot
from config.settings import tg_api
from handlers.command_handlers import setup_command_handlers
from handlers.callback_handlers import setup_callback_handlers

load_dotenv()

# Set up main logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize tg bot
bot = telebot.TeleBot(tg_api)

# Set up handlers
setup_command_handlers(bot)
setup_callback_handlers(bot)

logger.info('Bot running')
bot.infinity_polling()