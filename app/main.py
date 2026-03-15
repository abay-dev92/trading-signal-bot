import time

from app.binance_client import BinanceClient
from app.config import (
    SYMBOL,
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


def build_message(symbol: str, price: float, ema_fast: float, ema_slow: float, rsi: float, signal: str) -> str:
    return (
        f"Signal Bot Alert\n"
        f"Pair: {symbol}\n"
        f"Price: {price:.2f}\n"
        f"EMA {EMA_FAST_PERIOD}: {ema_fast:.2f}\n"
        f"EMA {EMA_SLOW_PERIOD}: {ema_slow:.2f}\n"
        f"RSI {RSI_PERIOD}: {rsi:.2f}\n"
        f"Signal: {signal}"
    )


def main() -> None:
    client = BinanceClient()
    last_sent_signal = None

    print("Bot started...")

    while True:
        try:
            df = client.fetch_ohlcv(SYMBOL, TIMEFRAME, LIMIT)

            df = add_ema(df, EMA_FAST_PERIOD, "ema_9")
            df = add_ema(df, EMA_SLOW_PERIOD, "ema_21")
            df = add_rsi(df, RSI_PERIOD)

            signal = SignalStrategy.generate_signal(df)
            last_row = df.iloc[-1]

            price = float(last_row["close"])
            ema_fast = float(last_row["ema_9"])
            ema_slow = float(last_row["ema_21"])
            rsi = float(last_row["rsi"])

            print(
                f"[{last_row['timestamp']}] "
                f"Price={price:.2f} | "
                f"EMA9={ema_fast:.2f} | "
                f"EMA21={ema_slow:.2f} | "
                f"RSI={rsi:.2f} | "
                f"Signal={signal}"
            )

            if signal != "NO SIGNAL" and signal != last_sent_signal:
                message = build_message(
                    symbol=SYMBOL,
                    price=price,
                    ema_fast=ema_fast,
                    ema_slow=ema_slow,
                    rsi=rsi,
                    signal=signal,
                )

                TelegramNotifier.send_message(message)
                print("Telegram alert sent.")
                last_sent_signal = signal

            time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("Bot stopped by user.")
            break
        except Exception as error:
            print(f"Bot error: {error}")
            time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()