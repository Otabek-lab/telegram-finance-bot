import os
import logging
import langdetect
import numpy as np
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
from deep_translator import GoogleTranslator
from sklearn.linear_model import LinearRegression

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Получение токена из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка токена
if not TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден. Добавь переменную окружения в Railway!")

# Хранилище данных
transactions = []
translator = GoogleTranslator(source='auto', target='ru')

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Доход', 'Расход', 'Отчет', 'Прогноз']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Привет! Я твой финансовый бот. Записывай доходы и расходы, а я сделаю аналитику!", reply_markup=markup)

# Обработка транзакций
async def record_transaction(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    try:
        detected_lang = langdetect.detect(text)
        if detected_lang != 'ru':
            text = translator.translate(text)
    except Exception:
        await update.message.reply_text("Ошибка определения языка.")
        return

    words = text.split()
    if len(words) < 3:
        await update.message.reply_text("Используй формат: Доход 1000 Зарплата или Расход 500 Еда")
        return
    
    transaction_type = words[0].lower()
    if transaction_type not in ['доход', 'расход']:
        await update.message.reply_text("Ошибка: укажите 'Доход' или 'Расход' в начале сообщения.")
        return
    
    try:
        amount = float(words[1])
        category = ' '.join(words[2:])
    except ValueError:
        await update.message.reply_text("Ошибка: сумма должна быть числом.")
        return

    transactions.append({'date': datetime.now(), 'type': transaction_type, 'amount': amount, 'category': category})
    await update.message.reply_text(f"✅ Записано: {transaction_type} {amount} в категории {category}")

# Генерация отчета
async def generate_report(update: Update, context: CallbackContext) -> None:
    if not transactions:
        await update.message.reply_text("❌ Нет данных для отчета.")
        return
    
    df = pd.DataFrame(transactions)
    income = df[df['type'] == 'доход'].groupby('category')['amount'].sum()
    expense = df[df['type'] == 'расход'].groupby('catego
