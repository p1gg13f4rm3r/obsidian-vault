#!/usr/bin/env python3
"""
Daily RSI Alert — Precious Metals Universe
Alerts when any PM symbol has RSI < 35 (mean reversion entry zone).
Run before market open on trading days.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data import fetcher
from src.analysis import indicators as ind_mod

SYMBOLS = ['GLD', 'GDX', 'SLV', 'SILJ', 'NEM', 'AG']
RSI_THRESHOLD = 35

results = []
for sym in SYMBOLS:
    df = fetcher.fetch_symbol(sym, period='3mo')
    if df.empty:
        continue
    df = ind_mod.add_indicators(df)
    latest = df.iloc[-1]
    rsi = latest.get('rsi')
    price = latest.get('close')
    ema_13 = latest.get('ema_13')
    ema_50 = latest.get('ema_50')
    bb_lower = latest.get('bb_lower')
    date_str = str(latest.name.date()) if hasattr(latest.name, 'date') else str(latest.name)

    if rsi is None or price is None:
        continue

    rsi = float(rsi)
    price = float(price)

    entry = {
        'symbol': sym,
        'date': date_str,
        'price': price,
        'rsi': rsi,
        'ema_13': float(ema_13) if ema_13 else None,
        'ema_50': float(ema_50) if ema_50 else None,
        'bb_lower': float(bb_lower) if bb_lower else None,
    }

    if rsi < RSI_THRESHOLD:
        entry['signal'] = 'BUY — RSI oversold'
        entry['strength'] = round(0.40 + (30 - min(rsi, 30)) / 10, 2) if rsi < 30 else 0.40
        results.append(entry)

if not results:
    # No signals — still print a clean "all clear"
    print(f"✅ RSI Alert — {SYMBOLS} | No entries (RSI >= {RSI_THRESHOLD})")
    all_prices = []
    for sym in SYMBOLS:
        df = fetcher.fetch_symbol(sym, period='3mo')
        if not df.empty:
            df = ind_mod.add_indicators(df)
            latest = df.iloc[-1]
            rsi = latest.get('rsi')
            price = latest.get('close')
            if rsi is not None and price is not None:
                all_prices.append(f"{sym} RSI={float(rsi):.1f}")
    print("  Status: " + " | ".join(all_prices))
else:
    print(f"🔔 RSI ALERT — {len(results)} symbol(s) with RSI < {RSI_THRESHOLD}")
    for r in results:
        bb_pct = ((r['price'] - r['bb_lower']) / r['bb_lower'] * 100) if r['bb_lower'] else 0
        print(f"\n  {r['symbol']} — {r['signal']}")
        print(f"  Price: ${r['price']:.2f} | RSI: {r['rsi']:.1f} | Strength: {r['strength']:.2f}")
        print(f"  EMA13: ${r['ema_13']:.2f} | EMA50: ${r['ema_50']:.2f} | BB_lower: ${r['bb_lower']:.2f}")
        print(f"  Price is {bb_pct:.1f}% above BB lower band")
        print(f"  vs EMA13: {'ABOVE' if r['price'] > r['ema_13'] else 'BELOW'} | vs EMA50: {'ABOVE' if r['price'] > r['ema_50'] else 'BELOW'}")
