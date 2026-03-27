"""
Market data fetcher using yfinance.
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


def fetch_symbol(symbol: str, period: str = '1y',
                 force_refresh: bool = False) -> pd.DataFrame:
    """
    Fetch OHLCV data for a single symbol.

    Args:
        symbol:     Stock ticker (e.g. 'AAPL')
        period:     yfinance period string (1d/5d/1mo/3mo/6mo/1y/2y/5y/ytd/max)
        force_refresh: Ignored — cache layer lives in cache.py

    Returns:
        DataFrame with columns [open, high, low, close, volume] and date index
        (YYYY-MM-DD strings). Empty DataFrame on failure.
    """
    try:
        ticker = yf.Ticker(symbol)
        data   = ticker.history(period=period)
        if data.empty:
            logger.warning("No data for %s", symbol)
            return pd.DataFrame()

        # Flatten MultiIndex columns if any
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data.index = data.index.tz_localize(None)   # drop timezone for SQLite compat
        data.index.name = 'date'
        data = data.reset_index()
        data['date'] = data['date'].dt.strftime('%Y-%m-%d')
        # Keep only OHLCV
        data = data[['date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        data = data.dropna(subset=['close'])
        return data

    except Exception as e:
        logger.error("Error fetching %s: %s", symbol, e)
        return pd.DataFrame()


def fetch_multiple(symbols: List[str], period: str = '1y',
                   force_refresh: bool = False) -> Dict[str, pd.DataFrame]:
    """Fetch multiple symbols. Returns dict of symbol -> DataFrame."""
    return {s: fetch_symbol(s, period, force_refresh) for s in symbols}


def get_quote(symbol: str) -> Optional[Dict[str, Any]]:
    """Return latest quote fields for a symbol."""
    try:
        t = yf.Ticker(symbol)
        info = t.info or {}
        return {
            'symbol':   symbol,
            'price':    info.get('regularMarketPrice') or info.get('currentPrice'),
            'change':   info.get('regularMarketChangePercent'),
            'volume':   info.get('regularMarketVolume'),
            'timestamp': datetime.now().isoformat(),
        }
    except Exception as e:
        logger.warning("Quote failed for %s: %s", symbol, e)
        return None


def refresh_all_symbols() -> Dict[str, Any]:
    """
    Refresh data for all configured symbols.

    Returns:
        Summary of refresh operation
    """
    import json
    import os

    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
    symbols_file = os.path.join(config_path, 'symbols.json')

    try:
        with open(symbols_file, 'r') as f:
            symbols_data = json.load(f)

        all_symbols = [s['symbol'] for s in symbols_data.get('default', [])]
        results = fetch_multiple(all_symbols)

        success_count = sum(1 for df in results.values() if not df.empty)
        return {
            'total': len(all_symbols),
            'success': success_count,
            'failed': len(all_symbols) - success_count,
        }
    except Exception as e:
        logger.error("Error refreshing all symbols: %s", e)
        return {'error': str(e)}
