import logging
import random
from telebot import types
from time import gmtime, strftime
from services.compliment_service import get_compliment
from services.crypto_service import get_crypto_pairs, get_crypto_pair_single
from services.currency_service import get_currency_rate
from services.weather_service import check_weather
from services.gpt_service import call_llm_api
from utils.bot_helpers import get_user_display_name, sticker_ids_list

logger = logging.getLogger(__name__)

def setup_command_handlers(bot):

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user_name = message.from_user.username
        logger.info(f"Received /start command from user @{user_name}")
        bot.send_message(message.chat.id, """\
Салам алейкум, мужчины! Я здесь исключительно для жесточайших рофлов и смешных реакций. Напиши /help, чтобы увидеть мои настоящие возможности.
""")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        user_name = message.from_user.username
        logger.info(f"Received /help command from user @{user_name}")
        bot.send_message(message.chat.id, """\
Список моих команд: \n
/insult - оскорбить пользователя, чьё сообщение было переслано \n
/fisting - пробить очко пользователю, чьё сообщение было переслано \n
/menu - показать меню бота \n
/sticker - вызвать рандомный стикер \n
/man - собрать Билли \n
/compliment - прислать рандомный комплимент \n                   
/billy + текст запроса - вызвать Билли-бота \n\n
По вопросам обращаться к создателю
""")

    @bot.message_handler(commands=['compliment'])
    def handle_compliment(message):
        user_name = message.from_user.username
        logger.info(f"Received /comliment command from user @{user_name}")
        compliment = get_compliment()
        bot.send_message(message.chat.id, compliment)

    @bot.message_handler(commands=['billy'])
    def handle_billy_command(message):
        user_name = message.from_user.username
        logger.info(f"Received /billy command from user @{user_name}")
        call_llm_api(message, bot)

    @bot.message_handler(commands=['insult'])
    def insult(message):
        insult_text = 'ты гомосексуал'
        logger.info(f"Received /insult command from user {message.from_user.id}")
        if message.reply_to_message:
            user_name = get_user_display_name(message.reply_to_message.from_user)
            logger.info(f"Insulting replied user: {user_name}")
            bot.send_message(message.chat.id, f"{user_name}, {insult_text}")
        elif message.forward_from:
            user_name = get_user_display_name(message.forward_from)
            logger.info(f"Insulting forwarded user: {user_name}")
            bot.send_message(message.chat.id, f"{user_name}, {insult_text}")
        elif message.forward_sender_name:
            user_name = message.forward_sender_name
            logger.info(f"Insulting forwarded user by name: {user_name}")
            bot.send_message(message.chat.id, f"{user_name}, {insult_text}")
        else:
            logger.warning("Insult command used without replying or forwarding a message.")
            bot.send_message(message.chat.id, "Эту команду нужно использовать, отвечая на сообщение или пересылая сообщение.")

    @bot.message_handler(commands=['fisting'])
    def fisting(message):
        fisting_text = 'твоё очко пробито, сладкий'
        logger.info(f"Received /fisting command from user {message.from_user.id}")
        if message.reply_to_message:
            user_name = get_user_display_name(message.reply_to_message.from_user)
            logger.info(f"Fisting replied user: {user_name}")
            bot.send_message(message.chat.id, f"{user_name}, {fisting_text}")
        elif message.forward_from:
            user_name = get_user_display_name(message.forward_from)
            logger.info(f"Fisting forwarded user: {user_name}")
            bot.send_message(message.chat.id, f"{user_name}, {fisting_text}")
        elif message.forward_sender_name:
            user_name = message.forward_sender_name
            logger.info(f"Fisting forwarded user by name: {user_name}")
            bot.send_message(message.chat.id, f"{user_name}, {fisting_text}")
        else:
            logger.warning("Fisting command used without replying or forwarding a message.")
            bot.send_message(message.chat.id, "Эту команду нужно использовать, отвечая на сообщение или пересылая сообщение.")

    @bot.message_handler(commands=['debug'])
    def debug(message):
        logger.info(f"Debug command received from user {message.from_user.username}")
        logger.info(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

    @bot.message_handler(commands=['menu'])
    def handle_menu(message):
        menu(bot, message)

    @bot.message_handler(commands=['sticker'])
    def send_sticker(message):
        user_name = message.from_user.username
        logger.info(f"Received /sticker command from user @{user_name}")
        bot.send_sticker(message.chat.id, random.choice(sticker_ids_list))

    @bot.message_handler(commands=['man'])
    def send_sticker(message):
        user_name = message.from_user.username
        logger.info(f"Received /man command from user @{user_name}")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHATxmmSH7TkoCuCamNkbc48XmWLQp5wACVgAD4w02ApNW4flaQu7JNQQ')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHAT5mmSH9RyYqkZEQv1d0CT8G88jKIwACVwAD4w02AleGFMLRveHgNQQ')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHAUBmmSH_8wh016RV7-Q-KnOWPfWCmgACWAAD4w02Aig3M5_g3MDhNQQ')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHAUJmmSIBZUFltLTclslEn0GN5Qy47QACWQAD4w02Al4ar6aidooaNQQ')

def menu(bot, message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Курсы криптовалют', callback_data='crypto_menu')
    button2 = types.InlineKeyboardButton('Курсы валют', callback_data='currency_menu')
    button3 = types.InlineKeyboardButton('Погода', callback_data='weather')
    button4 = types.InlineKeyboardButton('Комплимент', callback_data='compliment')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Текущий список функций: ', reply_markup=keyboard)