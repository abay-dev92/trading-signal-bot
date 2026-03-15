import pandas as pd


class SignalStrategy:
    @staticmethod
    def generate_signal(df: pd.DataFrame) -> str:
        if df.empty:
            return "NO SIGNAL"

        last_row = df.iloc[-1]

        ema_fast = last_row["ema_9"]
        ema_slow = last_row["ema_21"]
        rsi = last_row["rsi"]

        if pd.isna(ema_fast) or pd.isna(ema_slow) or pd.isna(rsi):
            return "NO SIGNAL"

        if ema_fast > ema_slow and rsi < 70:
            return "BUY"

        if ema_fast < ema_slow and rsi > 30:
            return "SELL"

        return "NO SIGNAL"