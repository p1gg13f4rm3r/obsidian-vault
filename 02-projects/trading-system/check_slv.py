import yfinance as yf
import datetime

ticker = yf.Ticker('SLV')
info = ticker.info

price = info.get('currentPrice') or info.get('regularMarketPrice')
prev_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
rsi = info.get('rsi14')

change_pct = ((price - prev_close) / prev_close) * 100 if prev_close else None

print(f'Price: {price}')
print(f'Prev Close: {prev_close}')
print(f'Change %: {change_pct:.2f}%' if change_pct else 'Change %: N/A')
print(f'RSI: {rsi}')
print(f'Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
