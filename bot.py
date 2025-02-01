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
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Настройки логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Получение токена из Railway (переменной окружения)
TOKEN = "7160148421:AAFutJR4gqFwkfokRm7JKfhXqVqM4zL9120"  # Используем реальный токен

# Хранилище транзакций
transactions = []
translator = GoogleTranslator(source="auto", target="ru")

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["Доход", "Расход", "Отчет", "Прогноз"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Привет! Я твой финансовый бот. Записывай доходы и расходы, а я сделаю аналитику!", reply_markup=markup)

# Запуск бота
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Бот запущен и работает!")
    await app.run_polling()

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())
