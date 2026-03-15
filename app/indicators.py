import pandas as pd


def add_ema(df: pd.DataFrame, period: int, column_name: str) -> pd.DataFrame:
    result = df.copy()
    result[column_name] = result["close"].ewm(span=period, adjust=False).mean()
    return result


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    result = df.copy()

    delta = result["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    result["rsi"] = 100 - (100 / (1 + rs))

    return result