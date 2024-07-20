import telebot
from telebot import types
import requests
import logging
from openai import OpenAI
import openai
import random
from bs4 import BeautifulSoup
from time import gmtime, strftime
from dotenv import load_dotenv
import os

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions used by the bot
def get_user_display_name(user):
    # Get first name or username of the sender
    if user.username:
        return f"@{user.username}"
    else:
        return user.first_name
    
def get_crypto_pairs(message):
    # Get crypto prices and percentage change
    inquiry = message.text[len('/'):].strip()
    crypto = [pair.strip().upper() for pair in inquiry.split(',')]
    key = "https://api.binance.com/api/v3/ticker/24hr?symbol="
    responses = []
    
    for pair in crypto:
        try:
            data = requests.get(f'{key}{pair}').json()
            responses.append(f"В данный момент цена на пару {data['symbol']} составляет {round(float(data['lastPrice']), 2)}. Изменение за последние 24 часа составляет {round(float(data['priceChangePercent']), 2)}%")
        except:
            responses.append(f"Пара {pair} не обнаружена")
    
    response_message = "\n\n".join(responses)
    bot.send_message(message.chat.id, response_message)

def get_crypto_pair_single(pair, chat_id):
    # Get single crypto price and percentage change
    key = "https://api.binance.com/api/v3/ticker/24hr?symbol="
    try:
        data = requests.get(f'{key}{pair}').json()
        response_message = f"В данный момент цена на пару {data['symbol']} составляет {round(float(data['lastPrice']), 2)}. Изменение за последние 24 часа составляет {round(float(data['priceChangePercent']), 2)}%"
    except:
        response_message = f"Пара {pair} не обнаружена"
    bot.send_message(chat_id, response_message)

currency_api = os.getenv('currency_api')

def get_currency_rate(first_currency, second_currency, chat_id):
    key = os.getenv('currency_api')
    try:
        link = f'{key}{first_currency}'
        response = requests.get(link)
        data = response.json()
        if response.status_code == 200 and "conversion_rates" in data:
            rate = data["conversion_rates"].get(second_currency, None)
            if rate is not None:
                response_message = f"В данный момент курс пары {first_currency}/{second_currency} составляет {round(float(rate), 2)} {second_currency}"
            else:
                response_message = f"Пара {first_currency}/{second_currency} не обнаружена"
        else:
            response_message = "Ошибка в получении данных от API"
    except Exception as e:
        response_message = f"Пара не обнаружена, ошибка: {str(e)}"
    bot.send_message(chat_id, response_message)

def check_weather(city):
  
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

    responce = requests.get(f"https://www.google.com/search?q=погода+в+{city}+на+сегодня", headers=headers)
    print(responce)

    soup = BeautifulSoup(responce.text, "html.parser")

    rain_chance = soup.select("#wob_pp")[0].getText()
    temperature = soup.select("#wob_tm")[0].getText()
    title = soup.select("#wob_dc")[0].getText()
    humidity = soup.select("#wob_hm")[0].getText()
    time = soup.select("#wob_dts")[0].getText()
    wind = soup.select("#wob_ws")[0].getText()

    weather = f'На сегодня погода в городе {city} следующая:\n\nТемпература: {temperature}°\n{title}\nВероятность осадков: {rain_chance}\nВлажность воздуха: {humidity}\nСкорость ветра: {wind}'

    return weather

# Initialize sticker list
sticker_ids_list = ['CAACAgIAAxkBAAEHAAGiZpkZs9oH4eonmGf5UjGfQiWX2FkAAiIjAALwPjBJYbF91qYKBv01BA', 'CAACAgIAAxkBAAEHAAGyZpkaXEwj3JW-dhqcvRn0ykdNkxMAArETAAJtdjhJmpo2eyFTFCs1BA', 'CAACAgIAAxkBAAEHAAGwZpkaWiAwn35B84zEGXGGjnyYtsUAAroYAAKWZTlJlh5OxagEy5w1BA', 'CAACAgIAAxkBAAEHAAGuZpkaWJ3EIlKYzC6cLCvHdUTBhQoAAvEcAAK1YThJzQpnjd68OcQ1BA', 'CAACAgIAAxkBAAEHAAGsZpkaVntQ9f380BE6Js8R9lWQnYQAAvceAAKFrTFJxkTZkxwAAdwcNQQ', 'CAACAgIAAxkBAAEHAAGqZpkaVNYAAZ0uiaF1i3xsEvi-4u3UAAKsHwAChUAxSW8HXeM311e3NQQ', 'CAACAgIAAxkBAAEHAAGoZpkaUURU5L9LsrzEJN8m9oC26BIAAoEdAAKo6DFJAsoSiQABiMXSNQQ', 'CAACAgIAAxkBAAEHAAGmZpkaT1LBRBCdRSX2GPqUWyQbGQcAAukaAAJVzjlJmEIotxfTPdQ1BA',
'CAACAgIAAxkBAAEHAAHQZpkb30TNnQM6q0-d2DnDmBkx0MUAArAaAAL6UDhJDQVE8W68yJ81BA', 'CAACAgIAAxkBAAEHAAHSZpkcAu6fvGUQUs9_GeQ9EZnL7psAAloaAAJA8_hJ5hEKr1wI-2I1BA', 'CAACAgIAAxkBAAEHAAHWZpkcGKwMLxlF9-AbXQNJiQtgUDoAAq8XAAI8FjlJ08aRcUha4r81BA',
'CAACAgIAAxkBAAEHAAHYZpkcM0WkkYailEbbKbxB_9UhziMAAqwfAAKFQDFJbwdd4zfXV7c1BA',
'CAACAgIAAxkBAAEHAAHaZpkcR68BLqAj92pdKcIvXg07E9oAArQYAAKjVzhJk0t3hCyPMkc1BA', 'CAACAgIAAxkBAAEHASBmmSEXZsZOOp9fHJNKDYIPRjAmlgACrhQAAsK5GEj-zaH7fRn1-zUE', 'CAACAgIAAxkBAAEHAR5mmSERURIFGbQ_8atpd_Thhh05rgACThQAAuh5IEgUTutarQ8FuTUE', 'CAACAgIAAxkBAAEHARxmmSEPDlrF5kbrJr7STlB2DSQ4pAACGhcAAoCBIEgyFrIa5zZmyjUE', 'CAACAgIAAxkBAAEHARpmmSEMpwVbLeoqngochaQbTiBUugADFgACCBQYSM6OTIUYpwpZNQQ', 'CAACAgIAAxkBAAEHARZmmSECAwaz-dYggrpL8A5rAx3_aAACZBQAAjQwIUjiMtSYvTg4yzUE', 'CAACAgIAAxkBAAEHAQ5mmSD8ovkqBjUIZAyq80H1JgwFKAACoBgAAow0GUiyMQktUxPRUjUE', 'CAACAgIAAxkBAAEHAQxmmSD6ZX22G1tEg8rYdGxYCW4QAAOXFwAC4QQAAUiERNze3vuohDUE', 'CAACAgIAAxkBAAEHAQpmmSD4yWfbKJGyts5y8LcHwAfPSgAChRwAAicPgEt74MNvvidN2DUE']

# Initialize tg bot
tg_api = os.getenv('tg_api')
bot = telebot.TeleBot(tg_api)

# Initialize OpenAI model
open_ai_api = os.getenv('open_ai_api')
openai.api_key = open_ai_api
client_gpt = OpenAI(api_key = open_ai_api)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create start command
    user_name = message.from_user.username
    logger.info(f"Received /start command from user @{user_name}")
    bot.send_message(message.chat.id, """\
Салам алейкум, мужчины! Я здесь исключительно для жесточайших рофлов и смешных реакций. Напиши /help, чтобы увидеть мои настоящие возможности
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    # Create help command
    user_name = message.from_user.username
    logger.info(f"Received /help command from user @{user_name}")
    bot.send_message(message.chat.id, """\
Список моих команд: \n
/insult - оскорбить пользователя, чьё сообщение было переслано \n
/fisting - пробить очко пользователю, чьё сообщение было переслано \n
/menu - показать меню бота \n
/sticker - вызвать рандомный стикер \n
/man - собрать Билли \n
/billy + текст запроса - вызвать Билли-бота \n
""")
    
@bot.message_handler(commands=['billy'])
def call_llm_api(message):
    try:
        # Extract the question from the message
        question = message.text[len('/billy '):].strip()
        logging.info(f"Question is: {question}")
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": """
            Представь, что ты чат-бот ассистент в мессенджере. Тебя зовут Билли Херрингтон. Ты взаимодействуешь исключительно с мужчинами. Ты должен действовать как персонаж из "gachimuchi". Ты должен отвечать развёрнуто. Если кто-то задает тебе вопрос, ты должен отвечать как сильный взрослый мужчина с гейскими наклонностями, добавляя юмор и уверенность в свои ответы. Используй при этом характерные фразы и стиль общения, чтобы максимально передать этот образ. Будь максимально вежливым, но не упускай возможность пошутить и показать свою уверенность и харизму. Ты можешь легко шутить про мужскую красоту и части тела. Не бойся отвечать грязно, если это улучшит твой ответ. Также можешь обильно использовать подходящие образу стикеры.
            """},
            {"role": "user", "content": question}
        ]

        # Call the OpenAI API
        completion = client_gpt.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Get the response content
        response = completion.choices[0].message.content

        # Log the response
        logging.info(f"Response is: {response}")

        # Send the response back to the user
        bot.send_message(message.chat.id, response)
        bot.send_sticker(message.chat.id, random.choice(sticker_ids_list))

    except Exception as e:
        logging.error(f"Error in call_llm_api: {e}")
        bot.send_message(message.chat.id, "Sorry, there was an error processing your request.")

@bot.message_handler(commands=['insult'])
def insult(message):
    # Create insulting command
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
    # Create fisting command
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
    # logger.info(message)

@bot.message_handler(commands=['menu'])
def menu(message):
    # Create keyboard for the menu
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Курсы криптовалют', callback_data='crypto_menu')
    button2 = types.InlineKeyboardButton('Курсы валют', callback_data='currency_menu')
    button3 = types.InlineKeyboardButton('Погода', callback_data='weather')
    keyboard.add(button1, button2, button3)

    # Send message with a keyboard
    bot.send_message(message.chat.id, 'Текущий список функций: ', reply_markup=keyboard)

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
        msg = bot.send_message(call.message.chat.id, 'Напишите названия пар через запятую для получения текущего курса\n\nНапример: /BTCUSDT, DOGEUSDT, LTCUSDT')
        bot.register_next_step_handler(msg, get_crypto_pairs)
    elif call.data == 'BTC':
        get_crypto_pair_single('BTCUSDT', call.message.chat.id)
    elif call.data == 'ETH':
        get_crypto_pair_single('ETHUSDT', call.message.chat.id)
    elif call.data == 'LTC':
        get_crypto_pair_single('LTCUSDT', call.message.chat.id)

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
        get_currency_rate('USD', 'RUB', call.message.chat.id)
    elif call.data == 'EUR/RUB':
        get_currency_rate('EUR', 'RUB', call.message.chat.id)
    elif call.data == 'USD/ARS':
        get_currency_rate('USD', 'ARS', call.message.chat.id)
    elif call.data == 'CNY/RUB':
        get_currency_rate('CNY', 'RUB', call.message.chat.id)

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
        weather = check_weather('Москва')
        bot.send_message(call.message.chat.id, weather)
    elif call.data =='Kazan':
        weather = check_weather('Казань')
        bot.send_message(call.message.chat.id, weather)
    elif call.data =='Nizhniy':
        weather = check_weather('Нижний+Новгород')
        bot.send_message(call.message.chat.id, weather)   
    elif call.data =='Manchester':
        weather = check_weather('Манчестер')
        bot.send_message(call.message.chat.id, weather)   

    elif call.data == 'back_to_main':
        menu(call.message)

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

logger.info('Bot running')
bot.infinity_polling()