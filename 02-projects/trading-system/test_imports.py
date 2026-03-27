#!/usr/bin/env python3
"""Quick smoke test — run from project root."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.data import fetcher, cache, symbols
from src.analysis import indicators, signals
from src.portfolio import tracker, stats
from src.backtest import engine
from src.reports import generator
print("ALL IMPORTS OK")
