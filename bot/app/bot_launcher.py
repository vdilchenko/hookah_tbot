from telegram.ext import Application
from app.handlers import setup_handlers
from app.config import Config


def run_bot():
    app = Application.builder().token(Config.BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling()