---
date: 2026-04-12
tags: [trading, strategy, gold, GLD, MACD, trailing-stop, backtest]
updated: 2026-04-12
---

# GLD MACD + Trailing Stop Strategy

**Documented:** April 12, 2026
**Status:** ✅ Backtest complete
**Asset:** GLD (SPDR Gold Shares ETF)
**Backtest Period:** 2015-02-20 to 2026-04-10 (11.13 years)
**Backtest Engine:** Custom Python (yfinance + ta library EMA/MACD)

---

## Strategy Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Asset | GLD | SPDR Gold Shares ETF |
| MACD Fast EMA | 12 periods | Short-term EMA |
| MACD Slow EMA | 26 periods | Long-term EMA |
| Signal Line | 9 periods | EMA of MACD — trigger for crossovers |
| Trailing Stop | 12% | Exit when price falls 12% from peak |
| Max Hold Days | 90 days | Force exit after 90 calendar days |
| Backtest Start | 2015-02-20 | First bar with valid MACD data |
| Backtest End | 2026-04-10 | Last available trading day |
| Execution | Same-bar close | Entry/exit at bar close price |
| Position Sizing | Full compounding | 100% of available cash per trade |

---

## Entry Rules

1. **Bullish MACD Crossover** — When MACD line crosses above Signal line (EMA 9 of MACD), generate BUY.
2. **Execution:** At the **close of the same bar** that generated the signal (same-bar execution).

## Exit Rules

Check each bar in priority order — first triggered exit wins:

| Priority | Exit Trigger | Description |
|----------|-------------|-------------|
| 1 | Trailing Stop | Price falls 12% from peak since entry → exit at close |
| 2 | Max Hold | 90 calendar days elapsed since entry → exit at close |
| 3 | Bearish MACD | MACD line crosses below Signal line → exit at close |
| 4 | Period End | Backtest end date reached → close at last close |

---

## Trailing Stop Logic

```
peak_price = max price since entry (inclusive of entry bar)
drawdown   = (peak_price - current_close) / peak_price
if drawdown >= 0.12:
    EXIT at today's close
```
The stop trail rises with price — never retreats. A 12% trail gives ~12% breathing room before locking in a loss.

---

## Backtest Results (ACTUAL)

**Run Date:** 2026-04-12 | **Script:** `/tmp/gld_macd_backtest.py`

### Summary

| Metric | Strategy | Buy & Hold | Notes |
|--------|----------|------------|-------|
| Final Equity | $19,217 | ~$37,919 | Started with $10,000 |
| Total Return | **+92.2%** | **+279.2%** | B&H wins by 187pp |
| Annualized Return | +6.0% | +12.7% | B&H 2x the rate |
| Max Drawdown | **-16.0%** | -54.6% | Strategy limits DD significantly |
| Win Rate | 35.6% | — | Low but wins are big |
| Profit Factor | **1.68** | — | Avg win / avg loss |
| Avg Trade | +0.62% | — | |
| Best Trade | +21.8% | — | |
| Worst Trade | -6.2% | — | |
| Avg Hold Days | 17.8 | — | |
| Time in Market | 51.7% | 100% | Only invested ~half the time |
| Trades/Year | 10.6 | — | |
| Total Trades | 118 | — | 42W / 76L |

### Exit Reason Breakdown

| Exit Reason | Count | % of Trades |
|-------------|-------|-------------|
| MACD Bearish Cross | 116 | 98.3% |
| Trailing Stop | 1 | 0.8% |
| Period End | 1 | 0.8% |
| Max Hold (90d) | **0** | 0% |

### Annual Performance vs B&H

| Year | Strategy | B&H | Diff |
|------|----------|-----|------|
| 2015 | -3.1% | -3.1% | 0.0% |
| 2016 | +5.0% | +7.9% | -2.9% |
| 2017 | +8.2% | +11.9% | -3.7% |
| 2018 | -9.4% | -3.1% | -6.3% |
| 2019 | +6.9% | +17.8% | -10.9% |
| 2020 | +18.4% | +23.9% | -5.5% |
| 2021 | +7.3% | -6.2% | +13.5% |
| 2022 | -2.0% | +0.8% | -2.8% |
| 2023 | +12.0% | +11.8% | +0.2% |
| 2024 | +14.3% | +27.0% | -12.7% |
| 2025 | +50.7% | +61.5% | -10.8% |
| 2026 YTD | +5.9% | +5.9% | 0.0% |

---

## Key Findings

### F1: B&H absolutely crushes this strategy (confirmed H6)
- **-187pp vs B&H** over 11 years. The strategy captures short-term swings but misses the long-term compounding.
- GLD's buy-and-hold return of +279% reflects the full gold bull: from $115 (2015) to $437 (2026).
- Being in cash 48% of the time is extremely costly when gold is in a sustained uptrend.

### F2: Trailing stop barely fires — MACD cross dominates exits (confirmed H3 partially wrong)
- **98.3% of exits are MACD bearish crosses.** The 12% trailing stop triggered only ONCE.
- The 90-day max hold **never triggered** — no single trade lasted 90 days.
- This means the MACD crossover is doing all the work. The trailing stop is essentially decorative.

### F3: Low win rate but positive expectancy (confirmed H2 partially)
- 35.6% win rate — most trades lose.
- But avg win (+4.38%) >> avg loss (-1.45%), giving profit factor of 1.68.
- Small losses cut quickly, big gains captured. This is a "let winners run" approach within the MACD framework.

### F4: Strategy reduces drawdown significantly (-16% vs -55%)
- Being in cash 48% of the time naturally limits drawdown exposure.
- In the 2020 COVID crash: B&H drawdown was ~-15% peak-to-trough; strategy would have been in cash before the crash.
- However, this protection came at the cost of missing some of the recovery.

### F5: Year-by-year, strategy only beats B&H in 2021
- 2021 was the only year the strategy outperformed (+7.3% vs -6.2%).
- 2021 was a volatile sideways year — no clear trend — where the whipsaws actually helped.
- In strong trend years (2019, 2024, 2025), the strategy badly underperformed.

### F6: 10.6 trades/year is aggressive churning
- Average holding period of 17.8 days means the strategy is frequently entering/exiting.
- Lots of small losses from whipsaw trades (1-5 day holds with -0.5% to -2% losses).
- The churn is costly: each exit/entry cycle misses 1-2 days of price movement.

---

## Hypotheses Validation

| # | Hypothesis | Result | Evidence |
|---|------------|--------|----------|
| H1 | B&H beats MACD strategy in bull markets | ✅ **Confirmed** | B&H +279% vs strategy +92% |
| H2 | MACD reduces drawdown but costs returns | ✅ **Confirmed** | Max DD -16% vs -55%, but -187pp total return |
| H3 | 90-day max hold causes churn | ❌ **Wrong** | Never triggered — MACD cross dominates |
| H4 | 12% trailing stop too loose | ❌ **Wrong** | Only triggered 1x — not relevant |
| H5 | MACD crossovers are lagging | ✅ **Confirmed** | Most big gains exit before trend ends |
| H6 | Strategy underperforms B&H | ✅ **Confirmed** | -187pp over 11 years |

---

## What Would Improve the Strategy?

1. **Tighter stop or wider max hold** — Since trailing stop never fires, test 8% or 10% stop. Or increase max hold to 120-180 days to let winners run.
2. **Require minimum trend strength** — Only enter when MACD histogram is widening or ADX > 20, reducing whipsaws.
3. **Multi-bar MACD confirmation** — Require MACD above signal for 2+ consecutive days before entry.
4. **Combine with mean reversion filter** — Only enter when GLD is not at extreme (e.g., not overbought on RSI).
5. **Use GLD/SLV ratio** — Enter GLD when ratio favors physical over miners or vice versa.

---

## Comparison to Other Strategies

### vs. NEM Strategy (Paul's actual position)
- NEM: entry ~$45, now ~$114 (+153%) — individual miner stock
- GLD MACD strategy: +92% over same period — ETF with lower vol
- NEM's 153% return comes from leverage to gold price + operational leverage
- NEM's drawdown protection is less relevant — Paul is long-term bullish

### vs. Precious Metals Mean Reversion (BCOM/GLD)
- Mean reversion targets ratio extremes — completely different signal source
- MACD crossover is trend-following — catches directional moves
- These are **complementary**: use mean reversion to decide *weight*; use MACD to time *entries*

### vs. DD-Protection Trim (existing rule)
- Trim 50% when down >20% from 52W high — hedging rule for existing positions
- This MACD strategy is an **entry/exit system**, not a hedge
- A combined approach: hold NEM long-term, use MACD to time GLD/SLV additions

---

## Implementation Notes

The backtest was run as a standalone Python script (`/tmp/gld_macd_backtest.py`) because the trading system's built-in backtester doesn't support:
- Custom MACD parameters (12/26/9)
- Trailing stop logic
- 90-day max hold rule
- Same-bar execution model

To re-run:
```bash
cd ~/obsidian-vault/02-projects/trading-system
./venv/bin/python /tmp/gld_macd_backtest.py
```

---

*Backtest completed: 2026-04-12*

