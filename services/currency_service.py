import os
import requests
from telebot import TeleBot

def get_currency_rate(first_currency, second_currency):
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
    
    return response_message