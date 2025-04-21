from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes, CallbackQueryHandler, MessageHandler, filters
)
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("TOKEN")

# Функція розрахунку

def calculate_wake_times(sleep_time: str):
    try:
        sleep_dt = datetime.strptime(sleep_time, "%H:%M") + timedelta(minutes=15)
    except ValueError:
        return "❌ Невірний формат. Введи у форматі HH:MM (23:45)"

    wake_times = []
    for cycle in range(3, 7):
        wake_dt = sleep_dt + timedelta(minutes=cycle * 90)
        wake_times.append(f"{wake_dt.strftime('%H:%M')}  ({cycle} циклів)")

    return "🌞 Ідеальні часи для пробудження:\n" + "\n".join(wake_times)

# Команда /start

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🌬Засинаю зараз", callback_data='now'),
            InlineKeyboardButton("⏰ Вкажу час", callback_data='custom')
        ],
        [
            InlineKeyboardButton("ℹ️ Інструкція", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(Обери дію нижче:, reply_markup=reply_markup)

# Обробник кнопок

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'now':
        now_time = datetime.now().strftime("%H:%M")
        result = calculate_wake_times(now_time)
        await query.edit_message_text(result)

    elif query.data == 'custom':
        await query.edit_message_text(Укажи час у форматі HH:MM (наприклад: 23:45),
                                      )

    elif query.data == 'help':
        help_text = (
            "👋 Привіт! Я допомагаю обрати ідеальний час пробудження.\n"
            "\n🕒 /sleep 23:30 — якщо знаєш, коли засинаєш\n"
            "🌬 /now — засинаєш зараз\n"
        )
        await query.edit_message_text(help_text)

# Команда /help

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Напиши /start, щоб обрати дію або введи \n/sleep 23:45 — якщо знаєш час засинання\n/now — якщо засинаєш зараз"
    )

# /now команда

async def now_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now_time = datetime.now().strftime("%H:%M")
    result = calculate_wake_times(now_time)
    await update.message.reply_text(result)

# /sleep 23:30

async def sleep_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(Введи час, наприклад: /sleep 23:45)
        return
    result = calculate_wake_times(context.args[0])
    await update.message.reply_text(result)

# Старт бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("now", now_command))
    app.add_handler(CommandHandler("sleep", sleep_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Бот працює...")
    app.run_polling()
