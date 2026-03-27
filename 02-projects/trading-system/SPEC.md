# Trading System — Project Specification

> Last updated: 2026-03-25

---

## Table of Contents

1. [Overview](#1-overview)
2. [Project Structure](#2-project-structure)
3. [Data Layer](#3-data-layer)
4. [Analysis Layer](#4-analysis-layer)
5. [Backtesting](#5-backtesting)
6. [Portfolio Tracking](#6-portfolio-tracking)
7. [Reporting](#7-reporting)
8. [CLI Interface](#8-cli-interface)
9. [Daily Cron Job](#9-daily-cron-job)
10. [Database Schema](#10-database-schema)
11. [Development Rules](#11-development-rules)

---

## 1. Overview

A Python-based discretionary trading system that:
- Collects and stores historical OHLCV data with technical indicators for a curated symbol universe
- Runs backtests across 6 strategies
- Tracks open/closed trades in SQLite
- Generates signals and reports
- Runs post-market automatically via cron

**Rule: Always fetch maximum available history on first init. Never hardcode a cutoff date.**

---

## 2. Project Structure

```
trading-system/
├── config/
│   ├── symbols.json        ← symbol universe (default + custom)
│   ├── strategies.json      ← strategy parameter configs
│   └── api_keys.json       ← reserved for data API keys
├── data/
│   └── trading.db           ← SQLite database (OHLCV cache + trades + signals)
├── scripts/
│   └── post_market_fetch.py ← post-market cron task script
├── src/
│   ├── analysis/
│   │   ├── indicators.py    ← all technical indicator calculations
│   │   ├── signals.py       ← signal generation logic
│   │   └── strategies/      ← one file per strategy
│   │       ├── trend_following.py
│   │       ├── mean_reversion_aggressive.py
│   │       ├── mean_reversion_conservative.py
│   │       ├── momentum.py
│   │       ├── price_action.py
│   │       └── volume.py
│   ├── backtest/
│   │   └── engine.py        ← backtesting engine
│   ├── data/
│   │   ├── fetcher.py       ← yfinance data fetching
│   │   └── cache.py        ← SQLite cache layer
│   ├── portfolio/
│   │   ├── tracker.py       ← trade logging and tracking
│   │   └── stats.py         ← portfolio statistics
│   └── reports/
│       └── generator.py     ← report generation
├── main.py                  ← CLI entry point
├── requirements.txt
└── .venv/                   ← uv virtual environment
```

**Project location:** `~/obsidian-vault/02-projects/trading-system/`
**Python:** uv env at `trading-system/.venv/bin/python` (use `uv run python` from project root)
**Data source:** Yahoo Finance via `yfinance`

---

## 3. Data Layer

### Symbol Universe (`config/symbols.json`)

23 default symbols across 4 categories:

| Category | Symbols |
|---|---|
| Technology | AAPL, MSFT, GOOGL, AMZN, NVDA, META |
| Financial | JPM, BAC, GS, XLF |
| Energy | XOM, CVX |
| Healthcare | JNJ, UNH, PFE |
| ETFs | SPY, QQQ |
| Commodities | GLD, SLV, GDX, SILJ, NEM, AG |

Custom symbols can be added to the `custom` array without modifying defaults.

### Fetcher (`src/data/fetcher.py`)

- Uses `yfinance` to pull OHLCV data
- `fetch_symbol(symbol, period)` → DataFrame with `date, open, high, low, close, volume`
- `fetch_multiple(symbols, period)` → dict of symbol → DataFrame
- `get_quote(symbol)` → latest quote dict (price, change, volume)

### Cache Layer (`src/data/cache.py`)

- SQLite at `data/trading.db`
- **`get_db_path()` resolves relative to `__file__`** — do not hardcode paths
- `init_db()` — creates tables if absent
- `get_cached_data(symbol)` — read from DB
- `get_latest_date(symbol)` — newest date in DB for symbol
- `save_data(symbol, df)` — upsert (INSERT OR REPLACE)
- `save_incremental(symbol, df)` — only inserts rows not already in DB
- `is_stale(symbol)` — checks if cached data is older than N days

---

## 4. Analysis Layer

### Technical Indicators (`src/analysis/indicators.py`)

All computed using `ta` library + pandas:

| Indicator | Columns |
|---|---|
| EMA | `ema_9`, `ema_12`, `ema_21`, `ema_50`, `ema_200` |
| RSI | `rsi` (14-period) |
| Bollinger Bands | `bb_upper`, `bb_middle`, `bb_lower` |
| MACD | `macd`, `macd_signal`, `macd_hist` |
| ADX | `adx` |
| OBV | `obv` |
| VWAP | `vwap` |
| ROC | `roc` (rate of change) |

Function: `add_indicators(df)` — takes raw OHLCV DataFrame, returns with all indicators added.

### Strategies (`src/analysis/strategies/`)

Each strategy module exposes:
- `generate_signal(df)` → `{'signal': 'BUY'|'SELL'|'HOLD', 'strategy': ..., 'strength': float, 'price': float, 'reason': str}`
- Optional: `generate_exit_signal(df)` → exit signal string

| Strategy | Entry Logic | Exit Logic |
|---|---|---|
| `mean_reversion_aggressive` | RSI < 30 (oversold) | RSI > 50 |
| `mean_reversion_conservative` | RSI < 30 AND price within 2% of lower BB | RSI > 50 |
| `trend_following` | EMA 13 > EMA 50 + MACD bullish | EMA 13 < EMA 50 |
| `momentum` | Price > EMA + positive momentum | Momentum flip |
| `price_action` | Support breakout | Resistance hit |
| `volume` | Volume spike + price move | Volume normalization |

### Signal Generation (`src/analysis/signals.py`)

- `generate_signals(symbol, strategies, indicators_df)` — runs one or more strategies
- `detect_support_resistance(df)` — SR level detection
- Signals stored in `signals` table in DB

---

## 5. Backtesting

### Engine (`src/backtest/engine.py`)

- Bar-by-bar simulation with $10,000 initial capital, $1,000 position size
- Entry: next bar OPEN after signal
- Minimum hold: 5 days
- Exit: strategy-specific exit signal OR end of data

**Output metrics:**
- `total_return_pct`, `annualized_return_pct`
- `max_drawdown_pct`
- `win_rate`, `avg_gain_pct`, `avg_loss_pct`
- `profit_factor`
- `total_trades`, `winning_trades`, `losing_trades`
- `avg_trade_duration_days`

**Functions:**
- `run_backtest(strategy, symbol, period, all_strategies)` — main API
- `compare_strategies(symbol, period)` — rank all strategies by return

---

## 6. Portfolio Tracking

### Tracker (`src/portfolio/tracker.py`)

Manages `trades` and `signals` tables in `trading.db`:

**Trade operations:**
- `add_trade(...)` → opens a new position
- `close_trade(trade_id, exit_date, exit_price)` → closes and computes P&L
- `delete_trade(trade_id)`
- `get_open_positions()` / `get_closed_trades()` / `get_all_trades()`

**Signal operations:**
- `log_signal(signal_dict)` → stores signal
- `get_signals(symbol, strategy, limit)`

### Stats (`src/portfolio/stats.py`)

- `get_portfolio_summary()` → aggregate P&L, win rate, avg trade stats

---

## 7. Reporting

### Generator (`src/reports/generator.py`)

- `generate_report(date, latest)` → generates markdown/text report for a date
- Reports saved to `reports/` directory

---

## 8. CLI Interface

**Entry point:** `python main.py <command> [options]`

| Command | Options | Description |
|---|---|---|
| `analyze` | `--symbols`, `--strategy`, `--daily`, `--json` | Generate signals for symbols |
| `backtest` | `--strategy`, `--symbol`, `--period`, `--all-strategies` | Run backtest |
| `portfolio` | `--status`, `--stats`, `--add SYM` | Portfolio tracking |
| `report` | `--date`, `--latest` | Generate report |
| `symbols` | `--list`, `--list-custom`, `--add`, `--remove` | Manage symbols |
| `data` | `--fetch SYM`, `--refresh-all` | Data management |

Global flags: `--verbose` / `-v` (DEBUG logging), `--json` / `-j` (JSON output), `--config <dir>`

**Examples:**
```bash
cd ~/obsidian-vault/02-projects/trading-system
source venv/bin/activate

python main.py analyze --symbols AAPL,MSFT --strategy mean_reversion_aggressive
python main.py backtest --all-strategies --symbol SPY --period 2y
python main.py portfolio --stats
```

---

## 9. Daily Cron Job

**Job:** Post-Market Quote Fetch
**Schedule:** `5 21 * * 1-5` (1:05 PM PT = 4:05 PM ET + 1 hour)
**Delivery:** Discord

### Script: `scripts/post_market_fetch.py`

**Incremental logic (rule):**
1. If symbol has no data in DB → fetch `period="max"`, save all (initialization)
2. If symbol is up to date (last DB date ≥ today) → skip silently
3. If symbol has gaps → fetch `period="3mo"`, save only new rows (upsert)

**Dependencies installed in venv:** `yfinance`, `pandas`, `numpy`, `ta`

**Cron prompt delivers Discord summary:**
- ✅ All saved → "Post-market fetch done. Saved: N symbols — [list]"
- ⚠️ Any failures → "Saved: N | Failed: N — [failed symbols]"
- ❌ Error → error message posted to Discord

**Cron job ID:** `80e880fd05a7` (manage via `mcp_cronjob` tool)

---

## 10. Database Schema

### `daily_prices` (from `cache.py`)

| Column | Type | Description |
|---|---|---|
| `symbol` | TEXT | Ticker |
| `date` | DATE | Trading date |
| `source` | TEXT | Data source (default: `yfinance`) |
| `open`, `high`, `low`, `close` | REAL | OHLC prices |
| `volume` | INTEGER | Volume |
| `ema_9`, `ema_12`, `ema_21`, `ema_50`, `ema_200` | REAL | EMAs |
| `rsi` | REAL | RSI (14) |
| `bb_upper`, `bb_middle`, `bb_lower` | REAL | Bollinger Bands |
| `macd`, `macd_signal`, `macd_hist` | REAL | MACD |
| `adx`, `obv`, `vwap`, `roc` | REAL | Other indicators |
| `fetched_at` | DATETIME | When data was fetched |

Primary key: `(symbol, date, source)`

### `trades` (from `tracker.py`)

| Column | Type |
|---|---|
| `id` | INTEGER PK |
| `symbol`, `strategy` | TEXT |
| `entry_date`, `entry_price`, `quantity` | DATE/REAL |
| `exit_date`, `exit_price` | DATE/REAL (nullable) |
| `status` | TEXT (`open`/`closed`) |
| `pnl` | REAL |
| `notes` | TEXT |

### `signals` (from `tracker.py`)

| Column | Type |
|---|---|
| `id` | INTEGER PK |
| `symbol`, `strategy`, `signal_type` | TEXT |
| `strength`, `price` | REAL |
| `indicators` | TEXT (JSON) |
| `generated_at` | DATETIME |
| `traded` | BOOLEAN |

### `data_sources` (from `cache.py`)

Tracks fetch metadata per symbol.

---

## 11. Development Rules

### Golden Rules

1. **Fetch max history on first init** — never hardcode `period="5y"` or `period="15y"`. Use `period="max"` so each symbol gets its full available history.
2. **`get_db_path()` must be relative** — resolve from `__file__`, never hardcode `~/projects/02-projects/`. The project has already been migrated to `~/obsidian-vault/02-projects/`.
3. **Incremental saves** — use `INSERT OR REPLACE` or check-before-insert to avoid overwriting existing rows. Daily runs should only add new dates.
4. **uv for all dependencies** — never use system Python or the old venv. From project root use `uv run python`. Install packages with `uv pip install <pkg>`.
5. **Requirements** — keep `requirements.txt` in sync. Current required: `yfinance`, `pandas`, `numpy`, `ta`.

### DB Path Resolution (Critical)

```python
# WRONG — breaks when project moves
base = os.path.join(os.path.expanduser("~"), "projects", "02-projects", "trading-system")

# CORRECT — resolves relative to this file
base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Symbol Categories

When adding symbols, use the correct category:
- `Technology` — individual tech companies
- `Financial` — banks, financial services
- `Energy` — oil & gas
- `Healthcare` — pharma, health insurance
- `ETF` — index/sector ETFs
- `Commodities` — gold, silver, miners (GLD, SLV, GDX, SILJ, NEM, AG)
