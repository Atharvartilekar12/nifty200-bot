import yfinance as yf
import pandas as pd
import ta
import datetime

def get_trade_signals(stock):
    try:
        df = yf.download(stock + ".NS", period="5d", interval="15m")
        df.dropna(inplace=True)
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        df['SMA_20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()

        if df.empty or len(df) < 20:
            return None

        last = df.iloc[-1]
        if last['Close'] > last['SMA_20'] and last['RSI'] < 70:
            return {
                'type': 'BUY',
                'price': round(last['Close'], 2),
                'target': round(last['Close'] * 1.01, 2),
                'sl': round(last['Close'] * 0.99, 2)
            }
        elif last['Close'] < last['SMA_20'] and last['RSI'] > 30:
            return {
                'type': 'SELL',
                'price': round(last['Close'], 2),
                'target': round(last['Close'] * 0.99, 2),
                'sl': round(last['Close'] * 1.01, 2)
            }
        else:
            return None
    except:
        return None

nifty_200 = ["RELIANCE", "INFY", "TCS", "HDFCBANK", "ICICIBANK", "LT", "SBIN", "HCLTECH", "ITC", "WIPRO"]
today = datetime.datetime.now().strftime("%Y-%m-%d")

print(f"📊 Intraday Trade Ideas for {today}:\n")

count = 0
for stock in nifty_200:
    signal = get_trade_signals(stock)
    if signal:
        print(f"{signal['type']} {stock} @ {signal['price']} | Target: {signal['target']} | SL: {signal['sl']}")
        count += 1
    if count >= 3:
        break
      
