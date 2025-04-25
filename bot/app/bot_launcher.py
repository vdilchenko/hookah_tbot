from telegram.ext import Application
from .handlers import setup_handlers
from .config import Config


def run_bot():
    app = Application.builder().token(Config.BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling()