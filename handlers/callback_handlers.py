from telebot import types
import logging
from functools import partial

from services.crypto_service import get_crypto_pairs, get_crypto_pair_single
from services.currency_service import get_currency_rate
from services.weather_service import check_weather
from handlers.command_handlers import get_compliment
from handlers.command_handlers import menu

def setup_callback_handlers(bot):

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "crypto_menu":
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton('Кастомные курсы криптовалют', callback_data='custom_crypto')
            button2 = types.InlineKeyboardButton('Курс BTC/USDT', callback_data='BTC')
            button3 = types.InlineKeyboardButton('Курс ETH/USDT', callback_data='ETH')
            button4 = types.InlineKeyboardButton('Курс LTC/USDT', callback_data='LTC')
            back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_main')
            keyboard.add(button1, button2, button3, button4, back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите криптовалюту:', reply_markup=keyboard)

        elif call.data == "custom_crypto":
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            msg = bot.send_message(call.message.chat.id, 'Напишите названия пар через запятую для получения текущего курса\n\nНапример: /BTCUSDT, DOGEUSDT, LTCUSDT')
            bot.register_next_step_handler(msg, partial(get_crypto_pairs, bot=bot))
        elif call.data == 'BTC':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            crypto_rate = get_crypto_pair_single('BTCUSDT')
            bot.send_message(call.message.chat.id, crypto_rate)
        elif call.data == 'ETH':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            crypto_rate = get_crypto_pair_single('ETHUSDT')
            bot.send_message(call.message.chat.id, crypto_rate)
        elif call.data == 'LTC':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            crypto_rate = get_crypto_pair_single('LTCUSDT')
            bot.send_message(call.message.chat.id, crypto_rate)

        elif call.data == "currency_menu":
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton('Курс USD/RUB', callback_data='USD/RUB')
            button2 = types.InlineKeyboardButton('Курс EUR/RUB', callback_data='EUR/RUB')
            button3 = types.InlineKeyboardButton('Курс USD/ARS', callback_data='USD/ARS')
            button4 = types.InlineKeyboardButton('Курс CNY/RUB', callback_data='CNY/RUB')
            back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_main')
            keyboard.add(button1, button2, button3, button4, back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите валютную пару:', reply_markup=keyboard)

        elif call.data == 'USD/RUB':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            currency_rate = get_currency_rate('USD', 'RUB')
            bot.send_message(call.message.chat.id, currency_rate)
        elif call.data == 'EUR/RUB':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            currency_rate = get_currency_rate('EUR', 'RUB')
            bot.send_message(call.message.chat.id, currency_rate)
        elif call.data == 'USD/ARS':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            currency_rate = get_currency_rate('USD', 'ARS')
            bot.send_message(call.message.chat.id, currency_rate)
        elif call.data == 'CNY/RUB':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            currency_rate = get_currency_rate('CNY', 'RUB')
            bot.send_message(call.message.chat.id, currency_rate)

        elif call.data == "weather":
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton('Погода в Москве', callback_data='Moscow')
            button2 = types.InlineKeyboardButton('Погода в Казани', callback_data='Kazan')
            button3 = types.InlineKeyboardButton('Погода в Нижнем Новгороде', callback_data='Nizhniy')
            button4 = types.InlineKeyboardButton('Погода в Манчестере', callback_data='Manchester')
            back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_main')
            keyboard.add(button1, button2, button3, button4, back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите город:', reply_markup=keyboard)
        elif call.data =='Moscow':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            weather = check_weather('Москва')
            bot.send_message(call.message.chat.id, weather)
        elif call.data =='Kazan':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            weather = check_weather('Казань')
            bot.send_message(call.message.chat.id, weather)
        elif call.data =='Nizhniy':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            weather = check_weather('Нижний+Новгород')
            bot.send_message(call.message.chat.id, weather)   
        elif call.data =='Manchester':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            weather = check_weather('Манчестер')
            bot.send_message(call.message.chat.id, weather)

        elif call.data == 'compliment':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            compliment = get_compliment()
            bot.send_message(call.message.chat.id, compliment)

        elif call.data == 'back_to_main':
            logging.info(f"Received command: {call.data} from user {call.from_user.username}")
            menu(bot, call.message)
