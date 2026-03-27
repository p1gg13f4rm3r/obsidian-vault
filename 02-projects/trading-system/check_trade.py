#!/usr/bin/env python3
"""Check open trade status vs current price."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.portfolio import tracker
from src.data import fetcher
import json

# Show all trades
all_trades = tracker.get_all_trades()
print('=== ALL TRADES ===')
for t in all_trades:
    print(json.dumps(t, indent=2, default=str))

# Show open positions vs current price
print('\n=== OPEN POSITIONS vs CURRENT PRICE ===')
open_pos = tracker.get_open_positions()
if not open_pos:
    print('No open positions.')
for pos in open_pos:
    sym = pos['symbol']
    entry = pos['entry_price']
    qty = pos['quantity']
    trade_id = pos['id']
    current = fetcher.fetch_symbol(sym, period='5d')
    if current.empty:
        print(f'\nTrade #{trade_id}: {sym} - could not fetch current price')
        continue
    close_col = [c for c in current.columns if c.lower() in ('close', 'adj close')][0]
    price = current[close_col].iloc[-1]
    pnl = (price - entry) * qty
    pnl_pct = ((price / entry) - 1) * 100
    print(f'\nTrade #{trade_id}: {sym} ({pos["strategy"]})')
    print(f'  Entry:   ${entry:.2f} on {pos["entry_date"]}')
    print(f'  Current: ${price:.2f}')
    print(f'  Qty:     {qty}')
    print(f'  P&L:     ${pnl:.2f} ({pnl_pct:+.2f}%)')
