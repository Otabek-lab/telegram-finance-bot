import os
import logging
import asyncio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
from deep_translator import GoogleTranslator
from sklearn.linear_model import LinearRegression

# Настройки логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Получение токена из Railway (переменной окружения)
TOKEN = "7160148421:AAFutJR4gqFwkfokRm7JKfhXqVqM4zL9120"  # Используем тестовый токен по умолчанию

# Хранилище транзакций
transactions = []
translator = GoogleTranslator(source="auto", target="ru")

# Заглушка для функционала Telegram API
async def start():
    print("Привет! Я твой финансовый бот. Записывай доходы и расходы, а я сделаю аналитику!")

# Запуск бота
async def main():
    print("🚀 Бот запущен и работает! (Заглушка без Telegram API)")
    await start()

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())
