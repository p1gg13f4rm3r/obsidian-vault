"""
Trade logging and tracking.
Stores trades and signals in SQLite (trading.db).
"""
import json
import logging
import os
import sqlite3
from datetime import datetime, date
from typing import Optional

logger = logging.getLogger(__name__)

# Resolve project root relative to this file
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "trading.db")

# ── DB helpers ────────────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_portfolio_db():
    """Ensure trades and signals tables exist."""
    conn = _get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol      TEXT    NOT NULL,
                strategy    TEXT    NOT NULL,
                entry_date  DATE    NOT NULL,
                entry_price REAL    NOT NULL,
                quantity    REAL    NOT NULL,
                exit_date   DATE,
                exit_price  REAL,
                status      TEXT    DEFAULT 'open',
                pnl         REAL,
                notes       TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol       TEXT    NOT NULL,
                strategy     TEXT    NOT NULL,
                signal_type  TEXT    NOT NULL,
                strength     REAL,
                price        REAL,
                indicators   TEXT,
                generated_at DATETIME,
                traded       BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
        logger.info("Portfolio DB initialised at %s", DB_PATH)
    finally:
        conn.close()

# ── Trade functions ───────────────────────────────────────────────────────────

def add_trade(symbol: str, strategy: str, entry_date: str | date,
              entry_price: float, quantity: float, notes: str = "") -> int:
    """Add a new open trade. Returns the trade ID."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        cur = conn.execute(
            """INSERT INTO trades (symbol, strategy, entry_date, entry_price, quantity, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (symbol, strategy, str(entry_date), entry_price, quantity, notes)
        )
        conn.commit()
        trade_id = cur.lastrowid
        logger.info("Trade added: id=%d symbol=%s strategy=%s qty=%.4f @ %.4f",
                     trade_id, symbol, strategy, quantity, entry_price)
        return int(trade_id)
    finally:
        conn.close()


def close_trade(trade_id: int, exit_date: str | date, exit_price: float) -> Optional[dict]:
    """Close an open trade. Returns the updated trade dict or None if not found."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        row = conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone()
        if not row:
            logger.warning("close_trade: trade %d not found", trade_id)
            return None

        if row["status"] == "closed":
            logger.warning("close_trade: trade %d already closed", trade_id)
            return dict(row)

        entry_price = row["entry_price"]
        quantity    = row["quantity"]
        pnl = (exit_price - entry_price) * quantity

        conn.execute(
            """UPDATE trades
               SET exit_date=?, exit_price=?, status='closed', pnl=?
               WHERE id=?""",
            (str(exit_date), exit_price, pnl, trade_id)
        )
        conn.commit()

        updated = conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone()
        logger.info("Trade closed: id=%d symbol=%s pnl=%.4f", trade_id, row["symbol"], pnl)
        return dict(updated)
    finally:
        conn.close()


def delete_trade(trade_id: int) -> bool:
    """Delete a trade by ID. Returns True if deleted."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        cur = conn.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def get_open_positions() -> list[dict]:
    """Return all open (status='open') trades."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT * FROM trades WHERE status='open' ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_closed_trades() -> list[dict]:
    """Return all closed trades."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT * FROM trades WHERE status='closed' ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_trade(trade_id: int) -> Optional[dict]:
    """Return a single trade by ID."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        row = conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_trades() -> list[dict]:
    """Return all trades (open + closed)."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT * FROM trades ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── Signal functions ──────────────────────────────────────────────────────────

def log_signal(signal: dict) -> int:
    """Store a generated signal in the DB."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        indicators_json = json.dumps(signal.get("indicators", {}))
        cur = conn.execute(
            """INSERT INTO signals
               (symbol, strategy, signal_type, strength, price, indicators, generated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                signal.get("symbol"),
                signal.get("strategy"),
                signal.get("signal"),
                signal.get("strength"),
                signal.get("price"),
                indicators_json,
                signal.get("timestamp", datetime.now().isoformat()),
            )
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def get_signals(symbol: str = None, strategy: str = None,
                 limit: int = 100) -> list[dict]:
    """Retrieve signals, optionally filtered by symbol and/or strategy."""
    init_portfolio_db()
    conn = _get_conn()
    try:
        query = "SELECT * FROM signals WHERE 1=1"
        params: list = []
        if symbol:
            query += " AND symbol = ?"
            params.append(symbol)
        if strategy:
            query += " AND strategy = ?"
            params.append(strategy)
        query += f" ORDER BY generated_at DESC LIMIT {limit}"
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_portfolio_db()
    print("tracker.py OK — DB ready at", DB_PATH)
