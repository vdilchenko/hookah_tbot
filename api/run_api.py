import sys
from app.server import run_api
from app.config import Config, setup_logging

if __name__ == "__main__":
    setup_logging(Config.API_LOG_PATH, "API")
    run_api()