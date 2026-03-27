#!/usr/bin/env python3
"""
Post-market quote fetcher.
Runs ~1 hour after market close (1:05 PM PT / 4:05 PM ET).

Incremental mode: if a symbol already exists in the DB, fetch only from the
last cached date forward to fill gaps. If no data exists, fetch max history
(5y) for initialization.
"""
import os
import sys
import json
import logging
from datetime import datetime, timedelta, date
import sqlite3

# Resolve project root (scripts/ -> project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.data import fetcher
from src.data.cache import init_db, save_data, get_latest_date
from src.analysis.indicators import add_indicators

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
SYMBOLS_FILE = os.path.join(CONFIG_DIR, "symbols.json")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "trading.db")


def load_symbols():
    with open(SYMBOLS_FILE) as f:
        data = json.load(f)
    symbols = [s["symbol"] for s in data.get("default", [])]
    custom = [s["symbol"] for s in data.get("custom", [])]
    return symbols + custom


def get_last_date(symbol: str) -> str | None:
    """Return the latest date in DB for symbol, or None if not cached."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "SELECT MAX(date) FROM daily_prices WHERE symbol=? AND source='yfinance'",
            (symbol,),
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row and row[0] else None
    except Exception:
        return None


def save_incremental(symbol: str, df, source="yfinance"):
    """Save only new rows — skip dates already in DB."""
    if df.empty:
        return 0

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saved = 0

    for _, row in df.iterrows():
        date_val = row.name
        if isinstance(date_val, str):
            date_str = date_val[:10]
        elif hasattr(date_val, "strftime"):
            date_str = date_val.strftime("%Y-%m-%d")
        else:
            date_str = str(date_val)[:10]

        # Check if already exists
        cur.execute(
            "SELECT 1 FROM daily_prices WHERE symbol=? AND date=? AND source=?",
            (symbol, date_str, source),
        )
        if cur.fetchone():
            continue  # already have this date, skip

        cur.execute("""
            INSERT INTO daily_prices
            (symbol, date, source, open, high, low, close, volume,
             ema_13, ema_50, ema_200, rsi,
             bb_upper, bb_middle, bb_lower,
             macd, macd_signal, macd_hist,
             adx, obv, vwap, roc, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol, date_str, source,
            row.get("open"), row.get("high"), row.get("low"), row.get("close"), row.get("volume"),
            row.get("ema_13"), row.get("ema_50"), row.get("ema_200"), row.get("rsi"),
            row.get("bb_upper"), row.get("bb_middle"), row.get("bb_lower"),
            row.get("macd"), row.get("macd_signal"), row.get("macd_hist"),
            row.get("adx"), row.get("obv"), row.get("vwap"), row.get("roc"),
            fetched_at,
        ))
        saved += 1

    conn.commit()
    conn.close()
    return saved


def fetch_and_save(symbol: str, period: str = "3mo") -> dict:
    """Fetch data, add indicators, save incrementally. Returns dict summary."""
    df = fetcher.fetch_symbol(symbol, period=period)
    if df.empty:
        return {"status": "failed", "reason": "no data returned", "new_rows": 0}

    df = add_indicators(df)
    df.set_index("date", inplace=True)
    new_rows = save_incremental(symbol, df, source="yfinance")
    return {"status": "ok", "total_rows": len(df), "new_rows": new_rows}


def main():
    logger.info("=== Post-market fetch started at %s ===", datetime.now().isoformat())
    symbols = load_symbols()
    logger.info("Symbols: %s", symbols)

    init_db()
    results = {"init": [], "incremental": [], "failed": []}

    today_str = date.today().strftime("%Y-%m-%d")

    for symbol in symbols:
        try:
            last_date = get_last_date(symbol)

            if last_date is None:
                # First time — fetch max available history
                logger.info("[INIT] %s — no DB record, fetching max history ...", symbol)
                res = fetch_and_save(symbol, period="max")
                if res["status"] == "ok":
                    results["init"].append({
                        "symbol": symbol,
                        "new_rows": res["new_rows"],
                        "total_rows": res["total_rows"],
                    })
                    logger.info("[INIT] %s — saved %d rows (5y history)", symbol, res["new_rows"])
                else:
                    results["failed"].append({"symbol": symbol, "reason": res["reason"]})
                    logger.error("[INIT] %s — failed: %s", symbol, res["reason"])

            else:
                # Already in DB — check if today's close is missing
                if last_date >= today_str:
                    logger.info("[SKIP] %s — already up to date (%s)", symbol, last_date)
                    continue

                logger.info("[INCR] %s — last date %s, fetching missing data ...", symbol, last_date)
                res = fetch_and_save(symbol, period="3mo")
                if res["status"] == "ok":
                    results["incremental"].append({
                        "symbol": symbol,
                        "new_rows": res["new_rows"],
                    })
                    logger.info("[INCR] %s — saved %d new rows", symbol, res["new_rows"])
                else:
                    results["failed"].append({"symbol": symbol, "reason": res["reason"]})
                    logger.error("[INCR] %s — failed: %s", symbol, res["reason"])

        except Exception as e:
            logger.error("Error processing %s: %s", symbol, e)
            results["failed"].append({"symbol": symbol, "reason": str(e)})

    logger.info("=== Done. Init: %d  Incremental: %d  Failed: %d ===",
                len(results["init"]), len(results["incremental"]), len(results["failed"]))

    # Print summary for cron delivery
    print(json.dumps(results, default=str))


if __name__ == "__main__":
    main()
