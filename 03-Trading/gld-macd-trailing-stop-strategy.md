---
date: 2026-04-12
tags: [trading, strategy, gold, GLD, MACD, trailing-stop, backtest]
updated: 2026-04-12
---

# GLD MACD + Trailing Stop Strategy

**Documented:** April 12, 2026
**Status:** Backtest pending — deep dive TBD
**Asset:** GLD (SPDR Gold Shares ETF)
**Backtest Period:** 2015-01-01 to 2026-04-11 (11.3 years)

---

## Strategy Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Asset | GLD | SPDR Gold Shares ETF |
| MACD Fast EMA | 12 periods | Short-term EMA |
| MACD Slow EMA | 26 periods | Long-term EMA |
| Signal Line | 9 periods | Trigger line for crossover signals |
| Trailing Stop | 12% | Stop loss from peak price during position |
| Max Hold Days | 90 days | Force exit after 90 calendar days in position |
| Backtest Start | 2015-01-01 | |
| Backtest End | 2026-04-11 | |
| Total Period | 11.3 years | |

---

## Entry Rules

1. **Bullish MACD Crossover** — When MACD line crosses above the Signal line (9-period EMA of MACD), generate a BUY signal.
2. Entry price: Next day's open price (no same-day trading).

## Exit Rules

Triggers a SELL on the next open when ANY of the following occurs:

| Exit Trigger | Priority | Description |
|-------------|----------|-------------|
| Trailing Stop Hit | Primary | Price falls 12% or more from the peak price since entry |
| Bearish MACD Crossover | Secondary | MACD line crosses below Signal line |
| Max Hold Expiry | Tertiary | 90 calendar days elapsed since entry |
| Period End | Final | End of backtest window (2026-04-11) |

> **Note:** Priority order applies when multiple exits trigger simultaneously. In practice, whichever exit triggers first on a given day closes the position.

---

## Trade Mechanics

### Position Management
- **Position Type:** Single-asset long-only (GLD)
- **Sizing:** 100% of capital in one position (no stacking)
- **Entry/Exit Price:** Next-day open (T+1 execution, no slippage assumption for backtest)

### Trailing Stop Logic
```
peak_price = highest_price_since_entry
drawdown = (peak_price - current_price) / peak_price
if drawdown >= 0.12:
    EXIT on next open
```
- The stop trail rises with price — it never retreats.
- A 12% trail means you give the position room to fluctuate ±12% before locking in a loss.

### Max Hold Days
- Counterparty to the trailing stop — ensures no permanent capital lockup.
- Forces exit after 90 days regardless of P&L, then immediately re-enters if MACD still bullish.

---

## Deep Dive Questions for Analysis

### Performance
- [ ] **Total Return** — Strategy vs Buy & Hold (GLD buy-and-hold over same period)
- [ ] ** annualized Return** — Strategy vs B&H
- [ ] **Max Drawdown** — Strategy worst drawdown vs B&H worst drawdown
- [ ] **Sharpe Ratio** — Risk-adjusted return comparison
- [ ] **Win Rate** — % of trades that were profitable
- [ ] **Average Trade Return** — Mean P&L per trade (%)
- [ ] **Average Holding Period** — Did most trades hit the 90-day limit or exit earlier?
- [ ] **Best/Worst Trade** — Extreme outcomes

### Trade-level Analysis
- [ ] **Number of Trades** — Total round-trip trades over 11.3 years
- [ ] **Trades per Year** — Average turnover rate
- [ ] **% Exits by Trailing Stop** — How many exits were 12% trail vs MACD cross vs 90-day?
- [ ] **% Exits by Max Hold** — Did time-based exits drive many trades?
- [ ] **Consecutive Wins/Losses** — Streak analysis
- [ ] **Time in Market** — % of trading days invested vs in cash

### Benchmark Comparison
- [ ] **B&H Return** — What would $1 have become in GLD buy-and-hold?
- [ ] **Strategy Return** — What would $1 have become with this strategy?
- [ ] **Excess Return** — Strategy advantage/disadvantage vs B&H
- [ ] **Alpha Generation** — Does the strategy add value, or does B&H win through compounding?

### Signal Quality
- [ ] **MACD Crossover Lag** — How often did late crossovers cause false signals?
- [ ] **Whipsaw Trades** — Trades opened and closed quickly (< 10 days) with small gains/losses
- [ ] **Rolling 12-Month Return** — Does strategy outperform in some regimes (e.g., bull markets) but not others?
- [ ] **Market Regime Sensitivity** — Performance in uptrend vs downtrend vs range-bound GLD

### Trailing Stop Tuning (what-if)
- [ ] **12% stop too tight?** — Would 15% or 20% stop improve returns?
- [ ] **12% stop too loose?** — Would 8% or 10% improve Sharpe?
- [ ] **Scenario:** In 2025 GLD rose +61.5% — did the 12% trail ever trigger mid-rally? (It shouldn't have — peak kept climbing.)

### Entry/Exit Timing
- [ ] **T+1 Open Execution** — Any sensitivity to same-day vs next-day entry?
- [ ] **Close of Day Signal** — Would using close price for signal and next open for execution change results significantly?

---

## Expected Behavior in Current GLD Environment (April 2026)

> GLD approximately +61.5% trailing 12 months (as of April 2026). Current price ~$413.

**Trailing Stop Observations:**
- A 12% trailing stop on GLD's current ~$413 price means stop triggers at ~$363
- GLD hasn't been near $363 during this rally — the stop would not have been hit
- The strategy likely held through the entire 2025-2026 bull run

**90-Day Max Hold Observations:**
- With GLD in a sustained uptrend, many entries would exit at the 90-day limit only to immediately re-enter
- This creates a potential churn problem — frequent trading during trending markets

**Key Question:** Does the trailing stop actually help in a gold bull, or does the 90-day max hold generate excessive churn without adding value over B&H? This is what the backtest should answer.

---

## Comparison to Other Strategy Frameworks

### vs. Paul NEM Strategy (entry ~$45, currently ~$114, +153%)
- NEM is a single-stock precious metals miner — individual company risk
- GLD is physical gold exposure — no single-company risk
- The 12% trailing stop on NEM may behave very differently than on GLD due to volatility differences

### vs. Precious Metals Mean Reversion Strategy (existing doc)
- Mean reversion targets ratio extremes (BCOM/GLD, GSR)
- MACD crossover targets trend-following entries
- These are complementary: mean reversion says *when* to overweight gold; MACD strategy says *how* to trade GLD itself

### vs. DD-Protection Trim Rule
- Paul has a rule: trim 50% when position is down >20% from 52-week high
- This is a *hedging* rule for existing holdings, not an entry/exit system
- The MACD trailing stop is a *directional* entry/exit system

---

## Hypotheses to Validate with Backtest

| # | Hypothesis | How to Test |
|---|------------|-------------|
| H1 | B&H beats MACD strategy in GLD bull markets | Compare strategy vs B&H annual returns |
| H2 | MACD strategy reduces drawdown but costs returns | Compare max drawdown vs return tradeoff |
| H3 | 90-day max hold causes excessive churn in trends | Count re-entries; measure time in market |
| H4 | 12% trailing stop is too loose for GLD's volatility | Test 8%, 10%, 12%, 15% stops |
| H5 | MACD crossovers in GLD are lagging indicators | Compare crossover dates vs price peaks |
| H6 | Strategy underperforms B&H over full 11Y period | Total return comparison is the ultimate test |

---

## Implementation Notes

### Strategy Configuration (for trading system)
```json
{
  "name": "gld_macd_trailing_stop",
  "asset": "GLD",
  "macd_fast_ema": 12,
  "macd_slow_ema": 26,
  "signal_ema": 9,
  "trailing_stop_pct": 0.12,
  "max_hold_days": 90,
  "period_start": "2015-01-01",
  "period_end": "2026-04-11"
}
```

### Symbols Available in Trading System
- GLD is already in the symbol list (from `config/symbols.json`)
- Supports both futures (GC=F) and ETF (GLD) analysis

---

## Next Steps

1. **Run the backtest** — `./venv/bin/python main.py --backtest --config gld_macd_trailing_stop`
2. **Fill in the Deep Dive Questions** above with actual backtest data
3. **Test parameter variations** — 8%, 10%, 15% trailing stops; 60/120-day max hold
4. **Compare to B&H** — The simplest and most important benchmark
5. **Write analysis** — Document findings in a deep-dive section below

---

*Backtest results will be populated once the backtest is run.*
