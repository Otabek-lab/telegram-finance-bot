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

# Настройки логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Хранилище данных
transactions = []
translator = GoogleTranslator(source='auto', target='ru')

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Доход', 'Расход', 'Отчет', 'Прогноз']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Привет! Я твой финансовый бот. Записывай доходы и расходы, а я сделаю аналитику!", reply_markup=markup)

# Обработка ввода с автоопределением языка
def record_transaction(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    try:
        detected_lang = langdetect.detect(text)
        if detected_lang != 'ru':
            text = translator.translate(text)
    except Exception as e:
        update.message.reply_text("Ошибка определения языка.")
        return
    
    words = text.split()
    if len(words) < 3:
        update.message.reply_text("Используй формат: Доход 1000 Зарплата или Расход 500 Еда")
        return
    
    transaction_type = words[0].lower()
    if transaction_type not in ['доход', 'расход']:
        update.message.reply_text("Ошибка: укажите 'Доход' или 'Расход' в начале сообщения.")
        return
    
    try:
        amount = float(words[1])
        category = ' '.join(words[2:])
    except ValueError:
        update.message.reply_text("Ошибка: сумма должна быть числом.")
        return
    
    transactions.append({'date': datetime.now(), 'type': transaction_type, 'amount': amount, 'category': category})
    update.message.reply_text(f"✅ Записано: {transaction_type} {amount} в категории {category}")

# Генерация отчета в стиле Power BI
def generate_report(update: Update, context: CallbackContext) -> None:
    if not transactions:
        update.message.reply_text("❌ Нет данных для отчета.")
        return
    
    df = pd.DataFrame(transactions)
    income = df[df['type'] == 'доход'].groupby('category')['amount'].sum()
    expense = df[df['type'] == 'расход'].groupby('category')['amount'].sum()
    total_income = df[df['type'] == 'доход']['amount'].sum()
    total_expense = df[df['type'] == 'расход']['amount'].sum()
    
    report_text = f"📊 Финансовый отчет:\n💰 Доход: {total_income} сум\n💸 Расход: {total_expense} сум\n"
    
    fig, ax = plt.subplots(figsize=(8, 6))
    categories = pd.concat([income, expense], axis=1).fillna(0)
    categories.columns = ['Доход', 'Расход']
    categories.plot(kind='bar', ax=ax, color=['green', 'red'])
    ax.set_title('Доходы и Расходы по категориям')
    ax.set_ylabel('Сумма')
    plt.xticks(rotation=45)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    update.message.reply_text(report_text)
    update.message.bot.send_photo(update.message.chat_id, photo=buffer)

# Прогнозирование будущих расходов и доходов
def forecast(update: Update, context: CallbackContext) -> None:
    if not transactions:
        update.message.reply_text("❌ Нет данных для прогноза.")
        return
    
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days
    
    for trans_type in ['доход', 'расход']:
        subset = df[df['type'] == trans_type]
        if len(subset) > 1:
            X = subset[['days']]
            y = subset['amount']
            model = LinearRegression()
            model.fit(X, y)
            future_days = np.array([[df['days'].max() + 7], [df['days'].max() + 30]])
            predictions = model.predict(future_days)
            update.message.reply_text(f"📈 Прогноз для {trans_type}: \nЧерез неделю: {predictions[0]:.2f} сум\nЧерез месяц: {predictions[1]:.2f} сум")
        else:
            update.message.reply_text(f"⚠ Недостаточно данных для прогноза {trans_type}.")

# Основная функция
async def main() -> None:
    app = Application.builder().token("7160148421:AAFutJR4gqFwkfokRm7JKfhXqVqM4zL9120").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, record_transaction))
    app.add_handler(CommandHandler("report", generate_report))
    app.add_handler(CommandHandler("forecast", forecast))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
