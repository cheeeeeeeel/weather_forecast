
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")

if not API_KEY:
    raise ValueError("API ключ не обнаружен в окружении.")

if not API_BASE_URL:
    raise ValueError("Адрес API не обнаружен в окружении.")

