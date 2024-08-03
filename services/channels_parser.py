from telethon import TelegramClient
import asyncio
import os
from telethon.tl.types import MessageEntityTextUrl

# from config.settings import API_ID, API_HASH

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

client = TelegramClient('Daily_news parser', API_ID, API_HASH,
                        device_model="Google Pixel 7",
                        system_version="10.13.4",
                        app_version="8.4",
                        lang_code="en",
                        system_lang_code="en-US")

chat = 'antonchehovanalitk'

async def parse():
    await client.start(phone=PHONE_NUMBER)
    post = await client.get_messages(chat, 1, search='#обзорнадень')
    if post:
        message = post[0].message
        urls = post[0].entities
        text_url = [url for url in urls if isinstance(url, MessageEntityTextUrl)]
        text_url_details = [{'offset': url.offset, 'url': url.url, 'length': url.length} for url in text_url]
        
        return message, text_url_details
    else:
        return None