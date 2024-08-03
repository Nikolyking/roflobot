import logging
import random
import openai
from openai import OpenAI
from telebot import TeleBot
from utils.bot_helpers import sticker_ids_list
from config.settings import open_ai_api

openai.api_key = open_ai_api
client_gpt = OpenAI(api_key = open_ai_api)

def call_llm_api(message, bot: TeleBot):
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