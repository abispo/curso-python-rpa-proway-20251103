import datetime
import logging
import os

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from telegram import Bot, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

class AutomacaoProwayBot(Bot):
    def __init__(self):
        return super().__init__(os.getenv("TELEGRAM_TOKEN"))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.message.from_user.first_name

    timestamp = datetime.datetime.now(datetime.UTC).strftime(
        "%H:%M:%S de %d/%m/%Y"
    )

    await update.message.reply_text(f"Olá {user_name}. Você digitou '{user_text}'. Agora são {timestamp}.")

bot_app = ApplicationBuilder().bot(AutomacaoProwayBot()).build()
bot_app.add_handler(MessageHandler(filters.TEXT, echo))

if __name__ == "__main__":
    logger.info("Iniciando bot em modo POLLING...")
    bot_app.run_polling()