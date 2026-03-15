class StateManager:
    def __init__(self) -> None:
        self.last_sent_signals = {}

    def should_send(self, symbol: str, candle_time: str, signal: str) -> bool:
        key = f"{symbol}:{candle_time}"
        previous_signal = self.last_sent_signals.get(key)

        if previous_signal == signal:
            return False

        self.last_sent_signals[key] = signal
        return True