---
date: 2026-04-12
tags: [trading, precious-metals, strategy, GDX, SLV, SILJ, AG, mean-reversion]
---

# PM Core Strategy — Strategy #1

**Documented:** 2026-04-12
**Status:** Backtested (2011-04-16 → 2026-04-12, 15 years)

---

## Strategy Summary

| Field | Value |
|-------|-------|
| **Entry** | RSI < 30 |
| **Exit** | RSI > 50 OR +5% profit target OR 10-day max hold |
| **Symbols** | GDX → SLV → SILJ → AG (priority order) |
| **Skip** | NEM, GLD |
| **Position size** | 20% per trade |
| **Max concurrent** | 2 trades |

**Core thesis:** Buy precious metal assets when RSI hits 30 (oversold), hold until RSI normalizes above 50, but take profits at +5% or after 10 days — whichever comes first.

---

## 15-Year Backtest Results (2011–2026)

**Setup:** $1,000 per trade, one symbol at a time, equal weight across 4 symbols.
**Actual data:** Real closing prices from Yahoo Finance. Commissions not included.

### Per-Symbol Performance

| Symbol | Final Equity | Return % | Ann. Return | Win Rate | Trades | Avg Gain | Avg Loss | Profit Factor | Max DD | Avg Hold |
|--------|-------------|----------|-------------|----------|--------|----------|----------|---------------|--------|----------|
| **GDX** | $10,795 | **+7.95%** | +0.56%/yr | **59.6%** | 47 | +5.88% | -4.48% | **1.93** | **-2.90%** | 5.9d |
| **SLV** | $10,395 | +3.95% | +0.28%/yr | 49.0% | 51 | +4.83% | -3.13% | 1.49 | -2.66% | 6.9d |
| **SILJ** | $10,561 | +5.61% | +0.45%/yr | 55.3% | 47 | +6.84% | -5.79% | 1.46 | -3.47% | 5.5d |
| **AG** | $10,071 | +0.71% | +0.05%/yr | 56.2% | 48 | +7.77% | -9.65% | 1.03 | -7.11% | 5.0d |

### Combined 4-Symbol Portfolio

| Metric | Value |
|--------|-------|
| **Total P&L** | **+$1,822** |
| **Total trades** | 193 |
| **Overall win rate** | **54.9%** (106W / 87L) |
| **Avg gain** | +6.27% |
| **Avg loss** | -5.49% |
| **Profit factor** | 1.39 |
| **Max single trade loss** | -$292.80 (SILJ, Mar 2020 COVID crash) |

---

## Exit Reason Breakdown

Out of 193 total trades:

| Exit Reason | Count | % of Trades |
|-------------|-------|-------------|
| **RSI > 50** (normal exit) | 84 | 43.5% |
| **+5% profit target hit** | 71 | 36.8% |
| **10-day max hold** | 38 | 19.7% |

**Key insight:** The +5% profit target fires in 37% of trades — meaning more than a third of all wins are captured at +5% before RSI even normalizes. The profit target is doing real work.

---

## Year-by-Year Performance (Combined 4 Symbols)

| Year | Trades | Win Rate | Net P&L | Notes |
|------|--------|----------|---------|-------|
| 2012 | 7 | 43% | +$2 | Partial year (SILJ starts late) |
| 2013 | 26 | 50% | **-$127** | SILJ bear market begins |
| 2014 | 25 | 40% | **-$257** | PM bear — hardest year |
| 2015 | 20 | 35% | **-$311** | PM bear — consecutive losses |
| 2016 | 12 | 83% | **+$532** | Miners revival — SILJ +133% |
| 2017 | 14 | 79% | **+$669** | Best year by P&L |
| 2018 | 14 | 43% | +$66 | Choppy, range-bound |
| 2019 | 6 | 67% | +$83 | Strong PM bull — fewer signals |
| 2020 | 8 | 50% | **-$187** | COVID crash — someRSI exits painful |
| 2021 | 17 | 65% | **+$333** | Recovery + chop |
| 2022 | 14 | 29% | **-$178** | Bear market — worst win rate |
| 2023 | 21 | 67% | **+$549** | Strong second half |
| 2024 | 5 | 100% | **+$361** | Few signals, all winners |
| 2025 | 2 | 100% | **+$131** | Partial — very few RSI<30 entries |
| 2026 | 2 | 100% | **+$157** | Partial |

---

## Symbol Priority

### GDX — **First choice**
- Best risk-adjusted returns (PF: 1.93)
- Lowest max drawdown (-2.90%)
- Highest win rate (59.6%)
- Gold miners ETF — diversified, liquid

### SLV — **Second choice**
- Decent PF (1.49) but win rate only 49%
- Lower volatility than SILJ/AG
- Good proxy for silver direction

### SILJ — **Third choice**
- Higher volatility, higher reward potential
- PF: 1.46, max DD: -3.47%
- Best used when silver is trending

### AG — **Last resort**
- Lowest PF (1.03) — avg loss nearly equals avg gain
- Max DD of -7.11% is the worst of the four
- Silver miners have highest single-stock risk

### Skip: NEM, GLD
- NEM: single stock risk, individual mine operations
- GLD: barely moves — RSI<30 is too rare (~1 trade/year)

---

## Top 10 Winners (15-Year Backtest)

| Date | Symbol | Return | P&L | Exit |
|------|--------|--------|-----|------|
| 2020-03-18 | SILJ | +18.5% | +$185 | profit_5pct |
| 2016-01-19 | AG | +15.1% | +$151 | profit_5pct |
| 2026-03-19 | GDX | +13.7% | +$137 | profit_5pct |
| 2024-09-06 | AG | +13.5% | +$135 | profit_5pct |
| 2013-12-19 | SILJ | +11.9% | +$119 | profit_5pct |
| 2016-09-16 | AG | +11.0% | +$110 | profit_5pct |
| 2022-08-31 | SLV | +10.9% | +$109 | profit_5pct |
| 2020-03-20 | SLV | +10.8% | +$108 | profit_5pct |
| 2019-05-29 | SILJ | +10.5% | +$105 | profit_5pct |
| 2017-05-04 | AG | +10.4% | +$104 | profit_5pct |

**Pattern:** The biggest winners almost all exit via the +5% profit target — they hit +5% quickly and the strategy locks them in rather than giving them back.

---

## Top 10 Losers (15-Year Backtest)

| Date | Symbol | Return | P&L | Exit |
|------|--------|--------|-----|------|
| 2020-03-09 | SILJ | -29.3% | -$293 | rsi_exit |
| 2014-10-27 | AG | -25.5% | -$255 | rsi_exit |
| 2016-10-03 | AG | -18.7% | -$187 | rsi_exit |
| 2020-03-12 | SLV | -18.4% | -$184 | rsi_exit |
| 2015-07-20 | AG | -18.0% | -$179 | rsi_exit |
| 2022-05-05 | AG | -15.7% | -$157 | rsi_exit |
| 2015-07-10 | GDX | -14.9% | -$149 | rsi_exit |
| 2023-02-15 | AG | -13.8% | -$138 | rsi_exit |
| 2013-04-02 | AG | -13.7% | -$137 | rsi_exit |
| 2013-04-02 | SLV | -12.7% | -$127 | rsi_exit |

**Pattern:** Every big loss exits via RSI normalization (RSI still > 50, meaning the position stayed underwater the whole time). These are entries made during sustained bear markets where RSI stayed low and price kept falling even as the strategy held.

---

## Scaling to Real Portfolio

The backtest uses $1,000 per trade on $10,000 capital (10% deployed).
Scale to your actual portfolio:

| Your Portfolio | Per Trade (20%) | Scale Factor |
|---------------|------------------|--------------|
| $50,000 | $10,000 | 10x |
| $100,000 | $20,000 | 20x |
| $200,000 | $40,000 | 40x |

**$100K example:**
- $1,822 × 20 scale = **+$36,440 over 15 years** (~$2,430/yr)
- Not a standalone strategy — this is the **core** layer on top of buy-and-hold

---

## Risk Profile

| Scenario | Impact |
|----------|--------|
| **Bear market (2014-2015)** | Win rate drops to 35-40%. Consecutive losses. Max DD: -$311 in a single year. |
| **COVID crash (2020)** | Strategy caught at RSI<30 entry just before crash. Worst single trade: -$293 on SILJ. |
| **Strong bull (2016, 2017)** | Win rate 79-83%. Best years. Strategy keeps missing entries as RSI never drops to 30. |
| **Chop (2018, 2023)** | Moderate win rate, small gains. Strategy works but not great. |

**The fundamental risk:** RSI<30 entries in a sustained bear market get caught, and the strategy holds through deep drawdowns waiting for RSI>50. The 10-day max hold helps but doesn't solve it.

---

## PM Core vs PM Tactical

| | PM Core (this strategy) | PM Tactical |
|--|------------------------|------------|
| **Entry** | RSI < 30 | EMA9 cross / pullback / VWAP |
| **Exit** | RSI>50 OR +5% OR 10d | +6% / -2% stop / VWAP |
| **Trade frequency** | ~3-4/year per symbol | ~15-18/year per symbol |
| **Win rate** | 55% | 53-55% |
| **Profit factor** | 1.39 | 1.10-1.25 |
| **Best for** | Big trend captures | Choppiness, small wins |

**Use both.** PM Core is the slow, high-conviction entry. PM Tactical is the active satellite layer that generates frequent small wins during chop.

---

## Running the Strategy

```bash
# Analyze PM basket for core signals
cd ~/obsidian-vault/02-projects/trading-system
./venv/bin/python main.py analyze --symbols GDX,SLV,SILJ,AG --strategy pm_core

# Backtest
./venv/bin/python main.py backtest --strategy pm_core --symbol GDX --period 15y
```

---

## Key Rules (Print and Follow)

1. **Only trade GDX, SLV, SILJ, AG** — skip NEM and GLD
2. **Wait for RSI < 30** — no entry unless oversold
3. **20% per trade, max 2 concurrent** — never risk more than 40% in this strategy
4. **Exit at RSI > 50** — don't hold longer waiting for more
5. **Take +5% if it comes first** — don't be greedy
6. **10-day hard exit** — if neither RSI>50 nor +5% happens, close it
7. **In bear markets (consecutive losses):** Pause. The strategy kills itself in sustained downtrends.
8. **In strong bulls:** Be patient. RSI<30 is rare when momentum is strong — fewer but higher quality entries.

---

*Backtest period: 2011-04-16 to 2026-04-12. Commissions not modeled. Past performance does not guarantee future results. DYOR.*
