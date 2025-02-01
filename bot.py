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

# Проверяем доступность библиотеки python-telegram-bot
try:
    import importlib.util
    spec = importlib.util.find_spec("telegram")
    if spec is None:
        raise ModuleNotFoundError
    from telegram import Update, ReplyKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
except ModuleNotFoundError:
    logging.error("\u274C Ошибка: Библиотека 'python-telegram-bot' не установлена или недоступна.")
    logging.error("Попробуйте установить её командой: pip install python-telegram-bot")
    raise

# Настройки логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Получение токена из Railway (переменной окружения)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logging.error("\u274C Ошибка: TELEGRAM_BOT_TOKEN не установлен. Добавьте его в переменные окружения.")
    raise ValueError("TOKEN not found")

# Хранилище транзакций
transactions = []
try:
    translator = GoogleTranslator(source="auto", target="ru")
except Exception as e:
    logging.warning(f"\u26A0 Ошибка при инициализации переводчика: {e}")
    translator = None

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["Доход", "Расход", "Отчет", "Прогноз"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Привет! Я твой финансовый бот. Записывай доходы и расходы, а я сделаю аналитику!", reply_markup=markup)

# Запуск бота
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    logging.info("🚀 Бот запущен и работает!")
    try:
        await app.run_polling()
    except Exception as e:
        logging.error(f"\u274C Ошибка во время выполнения бота: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logging.error(f"\u274C Ошибка: {e}. Используется существующий event loop.")
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен пользователем.")
