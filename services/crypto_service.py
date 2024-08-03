import requests
from telebot import TeleBot
import logging

def get_crypto_pairs(message, bot: TeleBot):
    inquiry = message.text[len('/'):].strip()
    logging.info(inquiry)
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
    

def get_crypto_pair_single(pair):
    key = "https://api.binance.com/api/v3/ticker/24hr?symbol="
    
    try:
        data = requests.get(f'{key}{pair}').json()
        response_message = f"В данный момент цена на пару {data['symbol']} составляет {round(float(data['lastPrice']), 2)}. Изменение за последние 24 часа составляет {round(float(data['priceChangePercent']), 2)}%"
    
    except:
        response_message = f"Пара {pair} не обнаружена"
    
    return response_message