import os
from dotenv import load_dotenv

load_dotenv()

SYMBOLS = [symbol.strip() for symbol in os.getenv("SYMBOLS", "BTC/USDT,ETH/USDT").split(",")]
TIMEFRAME = os.getenv("TIMEFRAME", "15m")
LIMIT = int(os.getenv("LIMIT", "100"))

EMA_FAST_PERIOD = int(os.getenv("EMA_FAST_PERIOD", "9"))
EMA_SLOW_PERIOD = int(os.getenv("EMA_SLOW_PERIOD", "21"))
RSI_PERIOD = int(os.getenv("RSI_PERIOD", "14"))

CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")