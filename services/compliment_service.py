import requests
from bs4 import BeautifulSoup
import random
import logging
from telebot import TeleBot

def get_compliment():
    try:
        url = "https://love.romanticcollection.ru/blog/500-trogatelnyh-komplimentov-devushke/"
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        compliments = soup.select('ol.wp-block-list li')
        messages = [compliment.get_text(strip=True) for compliment in compliments]
        text = random.choices(messages)[0]

        logging.info(f"Compliment is is: {text}")
    
    except Exception as e:
        text = f"Error in call_llm_api: {e}"
        logging.error(text)

    return text