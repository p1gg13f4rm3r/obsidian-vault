import yfinance as yf
slv = yf.Ticker('SLV')
data = slv.history(period='2d')
current_price = data['Close'].iloc[-1]
prev_close = data['Close'].iloc[-2]
change_pct = ((current_price - prev_close) / prev_close) * 100
print(f'PRICE:{current_price:.2f}')
print(f'CHANGE_PCT:{change_pct:.2f}')