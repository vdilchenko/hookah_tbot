import sys
from app.bot_launcher import run_bot
from app.config import Config, setup_logging

if __name__ == "__main__":
    setup_logging(Config.BOT_LOG_PATH, "BOT")
    run_bot()