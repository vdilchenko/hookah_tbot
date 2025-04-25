import pathlib
from loguru import logger
import sys, os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent


class Config:
    # Пути
    DATA_PATH = BASE_DIR / "data" / "tobacco_data.csv"
    API_LOG_PATH = BASE_DIR / "logs" / "api.log"
    BOT_LOG_PATH = BASE_DIR / "logs" / "bot.log"
    
    # Настройки API
    API_HOST = "0.0.0.0"
    API_PORT = 80
    
    # Настройки бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")


def setup_logging(log_path: str, service_name: str):
    """Настройка логирования для сервиса."""
    logger.remove()
    
    # Логи в файл
    logger.add(
        log_path,
        rotation="1 MB",
        retention="7 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG"
    )
    
    # Логи в консоль (исправленный формат)
    logger.add(
        sys.stdout,
        format="<cyan>" + service_name + "</cyan> | <level>{level}</level> | {message}",
        level="INFO",
        colorize=True
    )
