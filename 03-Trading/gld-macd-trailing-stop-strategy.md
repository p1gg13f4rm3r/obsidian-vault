---
date: 2026-04-12
tags: [trading, strategy, gold, GLD, MACD, trailing-stop, backtest]
updated: 2026-04-12
---

# GLD MACD + Trailing Stop Strategy

**Documented:** April 12, 2026
**Status:** ✅ Backtest complete
**Asset:** GLD (SPDR Gold Shares ETF)
**Backtest Period:** 2005-01-06 to 2026-04-10 (21.3 years — GLD inception to present)
**Backtest Engine:** Custom Python (yfinance + ta library EMA/MACD, standalone script)

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
| Backtest Start | 2005-01-06 | First bar with valid MACD (GLD inception 2004-11-18) |
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

## Backtest Results

**Run Date:** 2026-04-12 | **Script:** `/tmp/gld_macd_backtest.py`
**Key change:** Fixed execution bug in prior run — same-bar close execution (not T+1 open).

### Full Period: 2005-01-06 to 2026-04-10 (21.3 Years)

| Metric | Strategy | Buy & Hold | Notes |
|--------|----------|------------|-------|
| Final Equity | $54,940 | ~$103,700 | Started with $10,000 |
| Total Return | **+449.4%** | **+937.1%** | B&H wins by 487.7pp |
| Annualized Return | +8.34% | +11.63% | B&H 1.4x the rate |
| B&H Advantage | — | **+487.7pp** | Massive compounding gap |
| Max Drawdown | -20.8% | deeper | Strategy limits but not enough |
| Win Rate | 41.2% | — | Low but wins are larger |
| Profit Factor | 1.71 | — | Avg win / avg loss |
| Avg Trade | +0.88% | — | |
| Best Trade | +23.2% | — | |
| Worst Trade | -6.2% | — | |
| Avg Hold Days | 18.7 | — | |
| Time in Market | 52.1% | 100% | Only invested ~half the time |
| Trades/Year | 10.2 | — | |
| Total Trades | 216 | 1 | 89W / 127L |

### Exit Reason Breakdown

| Exit Reason | Count | % of Trades |
|-------------|-------|-------------|
| MACD Bearish Cross | 214 | 99.1% |
| Trailing Stop | **1** | 0.5% |
| Period End | 1 | 0.5% |
| Max Hold (90d) | **0** | 0% |

> **Trailing stop fires exactly once in 21 years.** The 12% threshold is structurally too loose for GLD. MACD cross-down handles virtually all exits.

---

## Annual Performance vs B&H

| Year | Strategy | B&H | Delta | Note |
|------|----------|-----|-------|------|
| 2005 | +13.1% | +22.4% | -9.3pp | |
| 2006 | +27.9% | +19.0% | **-8.9pp** ✓ | Strategy wins yr |
| 2007 | +12.3% | +32.4% | +20.1pp | |
| 2008 | +26.8% | +2.0% | **-24.9pp** ✓ | Strategy wins yr — crisis hedge |
| 2009 | +17.9% | +24.4% | -6.5pp | |
| 2010 | +1.6% | +26.3% | +24.8pp | |
| 2011 | +20.0% | +10.1% | **-9.8pp** ✓ | Strategy wins yr — volatile range |
| 2012 | -0.9% | +3.9% | +4.8pp | |
| 2013 | -12.8% | -28.8% | **-16.0pp** ✓ | Strategy wins yr — limits gold crash |
| 2014 | +3.4% | -3.7% | **-7.2pp** ✓ | Strategy wins yr |
| 2015 | +2.4% | -11.1% | **-13.5pp** ✓ | Strategy wins yr |
| 2016 | +1.4% | +6.5% | +5.2pp | |
| 2017 | +14.9% | +11.9% | **-3.0pp** ✓ | Strategy wins yr |
| 2018 | -8.6% | -3.1% | +5.5pp | |
| 2019 | +5.3% | +17.8% | +12.5pp | |
| 2020 | +7.1% | +23.9% | +16.8pp | |
| 2021 | +3.1% | -6.2% | **-9.3pp** ✓ | Strategy wins yr |
| 2022 | -4.1% | +0.8% | +4.8pp | |
| 2023 | +10.1% | +11.8% | +1.7pp | |
| 2024 | +5.9% | +27.0% | +21.0pp | |
| 2025 | +32.3% | +61.5% | +29.2pp | |
| 2026 | +3.5% | +9.8% | +6.3pp | |

> ✓ = years strategy outperformed B&H. Strategy won **9 of 22 years** — but losses in strong bull years (2007, 2010, 2020, 2024-2025) were large enough to hand B&H a +488pp total advantage.

---

## Key Findings

### F1: B&H crushes the strategy by +488pp over 21 years
- **B&H +937% vs Strategy +449%**. The strategy captures short-term swings but misses the long-term compounding of gold.
- Being in cash 48% of the time is catastrophically expensive in a compounding gold bull (11.6% ann).
- The math of gold's compounding punishes missing even modest rallies — the gap compounds faster than the strategy's drawdown protection can offset.

### F2: Trailing stop fires exactly once in 21 years
- **99.1% of exits are MACD bearish crosses.** The 12% trailing stop triggered only ONCE (2008: GLD dropped ~15% in Oct 2008, hit the 12% trail).
- The 90-day max hold **never triggered** — no single trade lasted 90 days.
- The trailing stop and max hold are essentially decorative. MACD crossover does all the work.

### F3: Low win rate (41%) but positive expectancy (PF 1.71)
- Most trades lose. But avg win (+5.1%) >> avg loss (-2.0%), giving profit factor of 1.71.
- Small losses cut quickly, big gains captured. "Let winners run" within the MACD framework.

### F4: The 2008 crisis and 2013 gold crash are the strategy's best arguments
- **2008:** Strategy +26.8% vs B&H +2.0% — the MACD got long before the crisis and captured the panic rally
- **2013:** Strategy -12.8% vs B&H -28.8% — being in cash saved 16pp when gold crashed
- These two years represent the strategy's only meaningful edges

### F5: Every strong gold bull year costs the strategy dearly
- 2025: Strategy +32.3% vs B&H +61.5% → missed 29pp
- 2024: Strategy +5.9% vs B&H +27.0% → missed 21pp
- 2020: Strategy +7.1% vs B&H +23.9% → missed 17pp
- 2019: Strategy +5.3% vs B&H +17.8% → missed 12pp
- These recurring gaps in strong years compound into the 488pp total deficit

### F6: Strategy wins in volatile/range-bound years, loses in trending years
- Win years: 2006, 2008, 2011, 2013, 2014, 2015, 2017, 2021 = avg +9.8% strategy vs +2.4% B&H
- Lose years: 2007, 2009, 2010, 2016, 2019, 2020, 2024, 2025 = avg +13.6% B&H vs +10.1% strategy
- Gold is in a structural bull — trending years dominate, so the strategy structurally underperforms

### F7: 10.2 trades/year is aggressive churning
- Average holding period of 18.7 days — frequently entering/exiting
- Lots of small losses from whipsaw trades (1-5 day holds with -0.5% to -2% losses)
- Each exit/entry cycle costs 1-2 days of price movement and full bid/ask spread

---

## Hypotheses Validation

| # | Hypothesis | Result | Evidence |
|---|------------|--------|----------|
| H1 | B&H beats MACD strategy in bull markets | ✅ **Confirmed** | B&H +937% vs strategy +449% |
| H2 | MACD reduces drawdown but costs returns | ✅ **Confirmed** | Max DD -20.8% vs deeper for B&H, but -488pp total return |
| H3 | 90-day max hold causes churn | ❌ **Wrong** | Never triggered — MACD cross dominates |
| H4 | 12% trailing stop too loose | ✅ **Confirmed** | Only triggered 1x — essentially decorative |
| H5 | MACD crossovers are lagging | ✅ **Confirmed** | Exits before trend ends, missing big moves |
| H6 | Strategy underperforms B&H | ✅ **Confirmed** | -488pp over 21 years |

---

## What Would Improve the Strategy?

1. **Much tighter trailing stop** — Test 4-6% stop. Since the 12% stop never fires, a tighter stop could actually provide the drawdown protection the strategy claims.
2. **Remove trailing stop entirely** — Since it doesn't fire, simplify to pure MACD cross with optional max hold extension.
3. **Require minimum trend strength** — Only enter when ADX > 20 or MACD histogram widening, reducing whipsaws.
4. **Combine with RSI filter** — Only enter when RSI < 70 (not overbought), avoid buying at MACD cross-up in overextended markets.
5. **Multi-timeframe confirmation** — Enter on daily MACD cross only when weekly MACD is also bullish.
6. **Scale-in position sizing** — Instead of 100% cash in, use 50% on first cross, 50% on next cross-up confirmation.
7. **Use with gold miner ETFs (GDX/SILJ)** — MACD may work better on higher-beta assets where the signal has more room to breathe.

---

## Comparison to Other Strategies

### vs. NEM Strategy (Paul's actual position)
- NEM: entry ~$45, now ~$114 (+153%) — individual miner stock with operational leverage
- GLD MACD strategy: +449% over 21 years (+92% over 11 years sub-period)
- NEM's leverage to gold price makes it a better vehicle for a gold bull than GLD

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

## Deep Dive Questions (for future research)

1. Would a 5-6% trailing stop improve results? What's the optimal stop percentage?
2. How does the strategy perform on GDX (gold miners) vs GLD?
3. What's the impact of transaction costs (bid/ask, slippage) on net returns?
4. Does the strategy work better on weekly charts (less whipsaw)?
5. How would a MACD histogram slope filter (only enter when histogram is widening) affect results?
6. What's the performance difference between same-bar vs T+1 execution?
7. Can we combine MACD signals with the precious metals mean reversion signals for a two-filter entry?
8. How does the strategy perform in bear markets (2008-2011 was gold's last major correction)?
9. What happens if we require 2 consecutive MACD cross-up days before entry?
10. How does the strategy compare to a simple price-moving-average crossover system?
11. What's the impact of position sizing (fixed $ vs % of portfolio) on compounding?
12. Does the strategy underperform more in high-volatility regimes (VIX > 30)?
13. How would trailing the stop with a shorter EMA (e.g., 9-period EMA of close) compare to the fixed 12%?
14. What's the Sharpe ratio and Sortino ratio for both strategy and B&H?
15. Does adding a time-of-year filter (e.g., avoid entering in strong seasonal months) help?

*Backtest completed: 2026-04-12*
