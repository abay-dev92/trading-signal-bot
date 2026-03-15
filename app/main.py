import time

from app.binance_client import BinanceClient
from app.config import (
    SYMBOLS,
    TIMEFRAME,
    LIMIT,
    EMA_FAST_PERIOD,
    EMA_SLOW_PERIOD,
    RSI_PERIOD,
    CHECK_INTERVAL_SECONDS,
)
from app.indicators import add_ema, add_rsi
from app.strategy import SignalStrategy
from app.telegram_notifier import TelegramNotifier
from app.logger_config import setup_logger
from app.state_manager import StateManager

logger = setup_logger()


def build_message(
    symbol: str,
    price: float,
    ema_fast: float,
    ema_slow: float,
    rsi: float,
    signal: str,
    candle_time: str,
) -> str:
    return (
        f"📈 Signal Bot Alert\n"
        f"Pair: {symbol}\n"
        f"Timeframe: {TIMEFRAME}\n"
        f"Price: {price:.2f}\n"
        f"EMA {EMA_FAST_PERIOD}: {ema_fast:.2f}\n"
        f"EMA {EMA_SLOW_PERIOD}: {ema_slow:.2f}\n"
        f"RSI {RSI_PERIOD}: {rsi:.2f}\n"
        f"Signal: {signal}\n"
        f"Candle time: {candle_time}"
    )


def process_symbol(client: BinanceClient, state_manager: StateManager, symbol: str) -> None:
    df = client.fetch_ohlcv(symbol, TIMEFRAME, LIMIT)

    df = add_ema(df, EMA_FAST_PERIOD, "ema_fast")
    df = add_ema(df, EMA_SLOW_PERIOD, "ema_slow")
    df = add_rsi(df, RSI_PERIOD)

    signal, closed_row = SignalStrategy.generate_signal(df)

    if closed_row is None:
        logger.warning(f"{symbol} | not enough data")
        return

    price = float(closed_row["close"])
    ema_fast = float(closed_row["ema_fast"])
    ema_slow = float(closed_row["ema_slow"])
    rsi = float(closed_row["rsi"])
    candle_time = str(closed_row["timestamp"])

    logger.info(
        f"{symbol} | Price={price:.2f} | "
        f"EMA{EMA_FAST_PERIOD}={ema_fast:.2f} | "
        f"EMA{EMA_SLOW_PERIOD}={ema_slow:.2f} | "
        f"RSI={rsi:.2f} | Signal={signal}"
    )

    if signal == "NO SIGNAL":
        return

    if not state_manager.should_send(symbol, candle_time, signal):
        logger.info(f"{symbol} | duplicate signal skipped")
        return

    message = build_message(
        symbol=symbol,
        price=price,
        ema_fast=ema_fast,
        ema_slow=ema_slow,
        rsi=rsi,
        signal=signal,
        candle_time=candle_time,
    )

    TelegramNotifier.send_message(message)
    logger.info(f"{symbol} | telegram alert sent")


def main() -> None:
    client = BinanceClient()
    state_manager = StateManager()

    logger.info("Bot started")

    while True:
        try:
            for symbol in SYMBOLS:
                process_symbol(client, state_manager, symbol)

            time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as error:
            logger.exception(f"Bot error: {error}")
            time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()