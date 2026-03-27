#!/usr/bin/env python3
"""Close trade #1."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.portfolio import tracker
from datetime import date

result = tracker.close_trade(
    trade_id=1,
    exit_date=str(date.today()),
    exit_price=83.33,
)
print('Closed:', result)
