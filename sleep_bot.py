from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("TOKEN")

def calculate_wake_times(sleep_time: str):
    try:
        sleep_dt = datetime.strptime(sleep_time, "%H:%M") + timedelta(minutes=15)
    except ValueError:
        return "Невірний формат часу. Використовуй HH:MM (наприклад, 23:45)."

    wake_times = []
    for cycle in range(3, 7):
        wake_dt = sleep_dt + timedelta(minutes=cycle * 90)
        wake_times.append(f"{wake_dt.strftime('%H:%M')} ({cycle} цикли)")

    return "Ідеальні часи для пробудження:\n" + "\n".join(f"- {t}" for t in wake_times)

async def sleep_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Вкажи час засинання. Наприклад:\n/sleep 23:45")
        return

    sleep_time = context.args[0]
    result = calculate_wake_times(sleep_time)
    await update.message.reply_text(result)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("sleep", sleep_command))
    print("Бот працює...")
    app.run_polling()
