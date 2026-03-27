"""
Data module for fetching and managing market data.
"""

from .fetcher import fetch_symbol, fetch_multiple

__all__ = ['fetch_symbol', 'fetch_multiple']
