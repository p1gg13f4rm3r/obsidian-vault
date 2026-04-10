"""SQLite cache layer for daily_prices and data_sources tables."""

import os
import sys
import sqlite3
import logging
from datetime import datetime, timedelta

import pandas as pd

logger = logging.getLogger(__name__)


def get_db_path():
    """Return path to trading.db (resolved relative to this file)."""
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "trading.db")


def init_db():
    """Create tables if they don't exist, return sqlite3 connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_prices (
            symbol TEXT,
            date DATE,
            source TEXT DEFAULT 'yfinance',
            open REAL, high REAL, low REAL, close REAL, volume INTEGER,
            ema_13 REAL, ema_50 REAL, ema_200 REAL,
            rsi REAL,
            bb_upper REAL, bb_middle REAL, bb_lower REAL,
            macd REAL, macd_signal REAL, macd_hist REAL,
            adx REAL, obv REAL, vwap REAL, roc REAL,
            fetched_at DATETIME,
            PRIMARY KEY (symbol, date, source)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_sources (
            symbol TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            first_fetched DATE,
            last_fetched DATE,
            record_count INTEGER DEFAULT 0,
            metadata TEXT
        )
    """)

    conn.commit()
    logger.info("Database initialized at %s", db_path)
    return conn


def is_stale(symbol, max_age_days=1):
    """Check if cached data is older than max_age_days."""
    conn = init_db()
    cursor = conn.cursor()
    cutoff = (datetime.now() - timedelta(days=max_age_days)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "SELECT last_fetched FROM data_sources WHERE symbol = ?",
        (symbol,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None or row[0] is None:
        return True

    last_fetched = row[0]
    return last_fetched < cutoff


def get_cached_data(symbol, start_date=None, end_date=None):
    """Return pandas DataFrame from cache."""
    conn = init_db()
    cursor = conn.cursor()

    query = "SELECT * FROM daily_prices WHERE symbol = ? AND source = 'yfinance'"
    params = [symbol]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date ASC"

    df = pd.read_sql_query(query, conn, params=params, index_col="date")
    conn.close()

    return df


def save_data(symbol, df, source='yfinance'):
    """Save a DataFrame to the cache (upsert by symbol+date)."""
    if df.empty:
        logger.info("No data to save for %s", symbol)
        return

    conn = init_db()
    cursor = conn.cursor()
    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df.iterrows():
        # Handle date from index OR from 'date' column
        date_val = None
        if df.index.name == 'date' or df.index.name is None:
            date_val = row.get('date', None)
        if date_val is None:
            date_val = row.name  # fallback to index
        if isinstance(date_val, str):
            date_str = date_val[:10]
        elif hasattr(date_val, 'strftime'):
            date_str = date_val.strftime("%Y-%m-%d")
        else:
            date_str = str(date_val)[:10]

        cursor.execute("""
            INSERT OR REPLACE INTO daily_prices
            (symbol, date, source, open, high, low, close, volume,
             ema_13, ema_50, ema_200, rsi,
             bb_upper, bb_middle, bb_lower,
             macd, macd_signal, macd_hist,
             adx, obv, vwap, roc, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol, date_str, source,
            row.get('open'), row.get('high'), row.get('low'), row.get('close'), row.get('volume'),
            row.get('ema_13'), row.get('ema_50'), row.get('ema_200'), row.get('rsi'),
            row.get('bb_upper'), row.get('bb_middle'), row.get('bb_lower'),
            row.get('macd'), row.get('macd_signal'), row.get('macd_hist'),
            row.get('adx'), row.get('obv'), row.get('vwap'), row.get('roc'),
            fetched_at
        ))

    record_count = len(df)
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO data_sources (symbol, source, first_fetched, last_fetched, record_count, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol) DO UPDATE SET
            last_fetched = excluded.last_fetched,
            record_count = excluded.record_count
    """, (symbol, source, today, today, record_count, None))

    conn.commit()
    conn.close()
    logger.info("Saved %d records for %s to cache", record_count, symbol)


def get_latest_date(symbol):
    """Return the most recent date for a symbol."""
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT MAX(date) FROM daily_prices WHERE symbol = ? AND source = 'yfinance'",
        (symbol,)
    )
    row = cursor.fetchone()
    conn.close()

    return row[0] if row and row[0] else None


def get_all_symbols():
    """Return list of cached symbols."""
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT symbol FROM daily_prices WHERE source = 'yfinance'")
    symbols = [row[0] for row in cursor.fetchall()]
    conn.close()

    return symbols
