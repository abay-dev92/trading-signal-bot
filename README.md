# Crypto Signal Bot

Python bot for crypto market monitoring using Binance data, RSI/EMA strategy, and Telegram alerts.

## Features

- Binance OHLCV market data
- EMA fast / EMA slow strategy
- RSI filter
- Signal generation on closed candles
- Telegram alerts
- Multi-pair monitoring
- Logging to file
- Duplicate signal protection

## Stack

- Python
- CCXT
- Pandas
- Requests
- python-dotenv

## Configuration

Create `.env` file based on `.env.example`.

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m app.main
```

## Example alert

```text
📈 Signal Bot Alert
Pair: BTC/USDT
Timeframe: 15m
Price: 68432.11
EMA 9: 68390.24
EMA 21: 68270.85
RSI 14: 61.33
Signal: BUY
Candle time: 2026-03-16 12:15:00
```