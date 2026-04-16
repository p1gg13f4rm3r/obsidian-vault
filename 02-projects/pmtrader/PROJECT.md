# PMTrader - Precious Metals AI Trading Agent

## Project Overview

**PMTrader** is an AI-powered trading agent system for precious metals (gold, silver) trading. It implements quantitative trading strategies with backtesting capabilities, technical indicator analysis, and a modular strategy registry system.

### Source Code Location
`~/workspace/pmtrader`

### Tech Stack
- **Language:** Python
- **Database:** SQLite (pmtrader.db)
- **Key Libraries:** pandas (data analysis), sqlalchemy (database), yfinance (market data)
- **CLI Framework:** argparse-based command interface
- **Testing:** pytest

### Project Structure
```
pmtrader/
├── broker/           # Trading execution engine
├── database/        # SQLite schema and models
├── fetch/           # Yahoo Finance data fetching
├── feed/            # Price data iterator
├── indicators.py     # Technical indicator calculations
├── registry.py       # Ticker/strategy registry
├── signal_scanner.py # Signal generation
├── strategies/       # Trading strategy implementations
│   ├── registry.py   # Strategy registry
│   ├── rsi_mean_reversion.py
│   └── macd_trailing_stop.py
└── report/          # Performance reporting
```

---

## Trading Strategies

### 1. RSI Mean Reversion Strategy (`rsi`)

**Strategy Name:** RSIMeanReversionStrategy

**Purpose:** Mean reversion strategy that enters positions when RSI indicates oversold conditions, with circuit breakers for exit management.

**Entry Rules:**
- RSI(14) < oversold threshold (default: 30)
- **Bull market filter:** GC=F (gold futures) > SMA200 of GC=F (optional, enabled via `--regime bull`)
- **Consecutive days:** RSI must remain below oversold for N consecutive days (configurable)

**Exit Rules (any trigger):**
- RSI(14) > overbought threshold (default: 50)
- Profit target reached (default: +5%)
- Maximum hold period exceeded (default: 10 trading days)

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `rsi_period` | 14 | RSI calculation period |
| `oversold` | 30 | RSI entry threshold |
| `overbought` | 50 | RSI exit threshold |
| `profit_target` | 0.05 (5%) | Profit exit threshold |
| `max_hold_days` | 10 | Circuit breaker max hold |
| `sma200_period` | 200 | SMA period for regime detection |
| `regime_ticker` | GC=F | Ticker for bull/bear market detection |
| `bull_only` | False | Only enter trades during bull markets |
| `consecutive_oversold_days` | 1 | Days RSI must stay below oversold before entry |
| `position_size` | $10,000 | Dollar amount per trade |

**Backtest Results (2015-01-01 to present):**
| Ticker | oversold | consecutive_days | Win Rate | Total Return |
|--------|----------|-----------------|----------|--------------|
| GDX    | 35       | 2               | 76.9%    | 38.2%        |

**Example Command:**
```bash
uv run pmtrader backtest GLD --start 2020-01-01 --strategy rsi --oversold 35 --consecutive-days 2
```

---

### 2. MACD Trailing Stop Strategy (`macd`)

**Strategy Name:** MACDTrailingStopStrategy

**Purpose:** Momentum-following strategy using MACD crossovers for entry signals with a trailing stop for risk management.

**Entry Rules:**
- MACD line crosses above Signal line (bullish crossover)
- **Bull market filter:** Gold futures (GC=F) > SMA200(GC=F)

**Exit Rules (any trigger):**
- MACD line crosses below Signal line (bearish crossover)
- **Trailing stop triggered:** Close drops >12% from highest close since entry

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `ticker` | GLD | Primary ticker to trade |
| `fast_period` | 12 | MACD fast EMA period |
| `slow_period` | 26 | MACD slow EMA period |
| `signal_period` | 9 | MACD signal line period |
| `trailing_stop_pct` | 0.12 (12%) | Trailing stop percentage |
| `sma200_period` | 200 | SMA period for regime detection |
| `indicator_ticker` | GC=F | Gold futures for regime detection |
| `position_size` | $10,000 | Dollar amount per trade |

**Example Command:**
```bash
uv run pmtrader backtest GLD --start 2020-01-01 --strategy macd --trailing-stop 0.12
```

---

## Technical Indicators

PMTrader calculates and stores these technical indicators:

| Indicator | Periods |
|----------|---------|
| RSI | 5, 9, 14, 20 |
| SMA | 13, 50, 200 |
| EMA | 13, 50, 200 |

---

## Key Commands

```bash
# Run backtest
uv run pmtrader backtest GLD --start 2020-01-01 --strategy rsi --oversold 35 --consecutive-days 2

# Fetch data
uv run pmtrader fetch GLD,GDX

# Run tests
uv run pytest tests/ -v
```

---

## Tradeable Instruments

The system is designed for precious metals ETFs:
- **GLD** - SPDR Gold Shares
- **GDX** - VanEck Gold Miners ETF
- **SLV** - iShares Silver Trust
- **SILJ** - ETFS Silver Miners ETF
- **GC=F** - Gold Futures (used as indicator, not traded)
- **SI=F** - Silver Futures (used as indicator, not traded)

---

## State

- **Project Status:** Discovery Complete
- **Current Phase:** N/A (project is a documented existing codebase)
- **Last Updated:** 2026-04-15
