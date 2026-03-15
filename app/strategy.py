import pandas as pd


class SignalStrategy:
    @staticmethod
    def generate_signal(df: pd.DataFrame) -> tuple[str, pd.Series | None]:
        if len(df) < 3:
            return "NO SIGNAL", None

        closed_row = df.iloc[-2]

        ema_fast = closed_row["ema_fast"]
        ema_slow = closed_row["ema_slow"]
        rsi = closed_row["rsi"]

        if pd.isna(ema_fast) or pd.isna(ema_slow) or pd.isna(rsi):
            return "NO SIGNAL", None

        if ema_fast > ema_slow and rsi < 70:
            return "BUY", closed_row

        if ema_fast < ema_slow and rsi > 30:
            return "SELL", closed_row

        return "NO SIGNAL", closed_row