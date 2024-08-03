import os
from dotenv import load_dotenv

load_dotenv()

tg_api = os.getenv('tg_api')
open_ai_api = os.getenv('open_ai_api')
currency_api = os.getenv('currency_api')