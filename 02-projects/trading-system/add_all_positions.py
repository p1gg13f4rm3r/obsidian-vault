#!/usr/bin/env python3
"""Add all 6 PM positions as mean_reversion_aggressive entries."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.portfolio import tracker
from src.data import fetcher
from datetime import date

symbols = ['GLD', 'GDX', 'SLV', 'SILJ', 'NEM', 'AG']

for sym in symbols:
    df = fetcher.fetch_symbol(sym, period='5d')
    close_col = [c for c in df.columns if c.lower() in ('close', 'adj close')][0]
    price = float(df[close_col].iloc[-1])
    qty = 1

    trade_id = tracker.add_trade(
        symbol=sym,
        strategy='mean_reversion_aggressive',
        entry_date=str(date.today()),
        entry_price=price,
        quantity=qty,
    )
    print(f"Added: {sym} × {qty} @ ${price:.2f}  (trade_id={trade_id})")
