---
date: 2026-04-12
tags: [trading, precious-metals, GDX, SLV, SILJ, AG, RSI, MACD, backtest, regime-analysis]
updated: 2026-04-12
---

# PM Trading Strategies — Research Compendium

**Status:** Active research
**Assets covered:** GDX, SLV, SILJ, AG
**Backtest period:** 15 years (2011–2026)
**Starting capital:** $10,000 per strategy
**Regime definition:** GDX price vs SMA(200) at year start — Bull if GDX > SMA200, Bear otherwise

---

## Strategy 1: PM Core (RSI Mean Reversion)

> **Entry philosophy:** Buy when RSI < 30 (oversold). Mean reversion to the mean works best in bull markets — the position catches a bounce and exits quickly.

### Rules

| Element | Value |
|---------|-------|
| Entry signal | RSI(14) < 30 |
| Exit signal | RSI > 50, OR +5% profit, OR 10 trading days max hold |
| Symbol priority | GDX → SLV → SILJ → AG |
| Position size | 20% of portfolio, max 2 concurrent |
| Execution | Entry: next day open. Exit: next day open |

### Full Period Results (15y)

| Symbol | Return | Win Rate | Profit Factor | Trades | Max DD | Avg Hold |
|--------|--------|----------|---------------|--------|--------|----------|
| **GDX** | +7.95% | **59.6%** | **1.93** | 47 | -2.90% | 5.9d |
| **SILJ** | +5.61% | 55.3% | 1.46 | 47 | -3.47% | 5.5d |
| **SLV** | +3.95% | 49.0% | 1.49 | 51 | -2.66% | 6.9d |
| **AG** | +0.71% | 56.2% | 1.03 | 48 | -7.11% | 5.0d |

### Bull vs Bear — PM Core

| Symbol | Bull WR | Bull PF | Bear WR | Bear PF |
|--------|---------|---------|---------|---------|
| GDX | **64.0%** | **2.45** | 54.5% | 1.60 |
| SILJ | 57.7% | 1.43 | 52.4% | 1.50 |
| AG | **61.5%** | **1.46** | 50.0% | 0.79 |
| SLV | 54.5% | 1.24 | 44.8% | 1.84 |
| **Combined** | **59.6%** | **1.55** | **50.0%** | **1.22** |

> PM Core shines in bull markets — GDX and AG both hit 60%+ win rates with PF above 1.45 in bull years. AG struggles in bear years (PF 0.79), confirming it's the weak link in the portfolio.

---

## Strategy 2: MACD + 12% Trailing Stop (Trend Following)

> **Entry philosophy:** Enter on MACD bullish crossover (12/26/9). Ride the trend until MACD cross-down or trailing stop fires. Works inversely to PM Core — thrives in choppy, range-bound, and bear conditions.

### Rules

| Element | Value |
|---------|-------|
| Entry signal | MACD line crosses above Signal line (EMA 9 of MACD 12/26) |
| Exit — priority 1 | Trailing stop: 12% drawdown from peak → exit at close |
| Exit — priority 2 | Max hold: 90 calendar days |
| Exit — priority 3 | MACD bearish crossover (cross below signal) |
| Execution | Entry/exit at bar close (same-bar execution) |
| Position sizing | 100% of available cash (full compounding) |

### Full Period Results (~$10K, full compounding)

| Symbol | Strategy | B&H | Gap | Trades | Win Rate | Profit Factor | Max DD |
|--------|----------|------|-----|--------|----------|---------------|--------|
| **SLV** | +337% | +400% | -63pp | 193 | 38.3% | 1.46 | -$2,659 |
| **GDX** | +40.6% | +215% | -174pp | 144* | 38.9% | 1.11 | -$2,096 |
| **AG** | +136.5% | +435% | -298pp | 155* | 32.3% | 1.02 | -$8,089 |
| **SILJ** | **-14.3%** | +82% | -97pp | 134 | 38.1% | 0.97 | -$2,382 |

> *Trade counts differ from earlier run due to different data periods (2006+ for MACD vs 2011+ for PM Core). Use percentage returns for comparison.
>
> SILJ and AG consistently underperform B&H. AG's 12% trailing stop fires 25% of the time — in a volatile silver name, the stop locks in losses at exactly the wrong moments.

### Exit Reason Breakdown

| Symbol | MACD Cross-Down | Trailing Stop | Max Hold (90d) |
|--------|-----------------|---------------|----------------|
| GDX | 95% | 5% | 0% |
| SLV | 96% | 4% | 0% |
| SILJ | 86% | 14% | 0% |
| AG | 75% | **25%** | 0% |

### Bull vs Bear — MACD Strategy

| Symbol | Bull WR | Bull PF | Bear WR | Bear PF |
|--------|---------|---------|---------|---------|
| GDX | 34.2% | 0.76 | 43.7% | 1.41 |
| **SLV** | 34.7% | 0.97 | **40.5%** | **2.25** |
| SILJ | 36.0% | 0.61 | 40.7% | 1.40 |
| AG | 28.4% | 0.72 | 35.8% | 1.25 |
| **Combined** | **33.3%** | **0.77** | **40.0%** | **1.46** |

> MACD is a bear-market machine. PF 1.46 in bear years across all symbols. SLV's bear-year PF of 2.25 is exceptional — silver's violent swings generate large winning trades that overwhelm the many small losses.

---

## Side-by-Side Comparison

### Full Period

| Metric | PM Core | MACD |
|--------|---------|------|
| **Win rate** | 49–60% | 32–41% |
| **Profit factor** | 1.03–1.93 | 0.97–1.53 |
| **Avg hold** | 5–7 days | 17–20 days |
| **Trades/year** | ~3–4 per symbol | ~10 per symbol |
| **Max single-trade loss** | -$293 (SILJ) | -$8,089 (AG) |
| **B&H gap** | Beats B&H in bear years | Loses to B&H in most years |
| **Best symbol** | GDX | SLV |

### Regime Performance — Combined All 4 Symbols

| Metric | PM Core Bull | PM Core Bear | MACD Bull | MACD Bear |
|--------|-------------|-------------|-----------|-----------|
| **Trades** | 99 | 94 | 294 | 285 |
| **Win Rate** | **59.6%** | 50.0% | 33.3% | 40.0% |
| **Profit Factor** | **1.55** | 1.22 | 0.77 | **1.46** |
| **Total P&L** | **+$1,234** | +$588 | -$31,809 | **+$67,355** |
| **Avg/trade** | **+$12** | +$6 | -$108 | **+$236** |

---

## When to Use Which Strategy

### Use PM Core when:
- You are in a **bull market** or the trend is up (GDX > SMA200)
- You want **high win rate** (55–65%) with small, consistent gains
- You want to **minimize time in the market** (avg 6 days)
- You want **low drawdown per trade** (max -$293)
- You want to **buy dips** — entering when RSI < 30 catches mean reversion bounces

### Use MACD when:
- You are in a **bear market** or extended consolidation (GDX < SMA200)
- You want to **hedge or reduce** a long PM exposure
- You want to **capture range-bound volatility** (SLV bear PF = 2.25)
- You can **handle low win rates** (35–40%) with larger winning trades
- You want to **stay long** but use MACD cross-downs to exit before major drawdowns

### Use Neither when:
- Market is in a **structural transition** — unclear if bull or bear
- You have **high conviction** in a long-term PM position (e.g., your NEM trade at $45)
- Transaction costs would erode MACD's thin margins (10+ trades/year)

---

## Regime Calendar (2026)

| Year | GDX Regime | PM Core | MACD |
|------|-----------|---------|------|
| 2011 | BEAR | ⚠️ GDX/SLV only | ✅ |
| 2012 | BEAR | ⚠️ GDX/SLV only | ✅ |
| 2013 | BULL | ✅ Best year | ❌ Kill your gains |
| 2014 | BEAR | ⚠️ | ✅ |
| 2015 | BEAR | ⚠️ | ✅ |
| 2016 | BEAR | ⚠️ | ✅ |
| 2017 | BEAR | ⚠️ | ✅ |
| 2018 | BULL | ✅ | ❌ |
| 2019 | BULL | ✅ | ❌ |
| 2020 | BULL | ✅ | ❌ |
| 2021 | BULL | ✅ | ❌ |
| 2022 | BEAR | ⚠️ | ✅ |
| 2023 | BULL | ✅ | ❌ |
| 2024 | BULL | ✅ | ❌ |
| 2025 | BEAR | ⚠️ | ✅ |
| **2026** | **BULL** | **✅ Deploy now** | **❌ Avoid** |

> **2026 current signal:** GDX is in BULL regime. PM Core is the correct strategy to be running right now. MACD's trend-following approach will likely exit too early and miss the continuation of the bull move.

---

## Practical Guidance for Your 80% Long PM Portfolio

Given your **80% long PM position**, here's how to deploy both strategies:

### Core Holdings (No active strategy)
- **NEM** — your $45 entry is the play. Hold through noise. Not a candidate for either strategy.
- **GLD/SLV physical** — long-term store of value, not a trade.

### PM Core — Active Satellite Trades
- **Use on:** GDX, SILJ, SLV (not AG — too volatile for PM Core in bear years)
- **When:** Only when GDX is above SMA200 (BULL regime)
- **Sizing:** 20% per trade, max 2 concurrent = 40% of portfolio in active trades
- **Goal:** Generate +$10–19/trade with 55–65% win rate
- **2026:** Currently BULL — PM Core is signaled. Deploy.

### MACD — Regime Hedging / Risk Reduction
- **Use on:** SLV only (best PF in bear years: 2.25)
- **When:** GDX is below SMA200 (BEAR regime)
- **Goal:** When you need to reduce PM exposure during a bear year, MACD on SLV generates income while waiting
- **Avoid:** MACD on AG or SILJ — both lose money even in bear years with this strategy
- **Caution:** MACD loses badly in bull years. Do NOT run this simultaneously with PM Core on the same symbol.

### Decision Tree

```
Is GDX > SMA200 (BULL)?
├── YES → Run PM Core on GDX, SILJ, SLV
│         Skip AG (bear-year PF drops to 0.79)
│         Max 2 concurrent, 20% each
│
└── NO (BEAR) → Reduce PM Core exposure
                Consider MACD on SLV only (PF 2.25 in bear)
                Skip GDX MACD (PF 1.41 — mediocre)
                Skip AG and SILJ MACD (PF < 1.40)
```

---

## Scripts & Code

| Strategy | Script | Engine |
|----------|--------|--------|
| PM Core | `src/analysis/strategies/pm_core.py` | `src/backtest/engine.py` |
| MACD | `/tmp/macd_trailing_stop_multi.py` | Standalone |

Run PM Core backtest:
```bash
cd ~/obsidian-vault/02-projects/trading-system
./venv/bin/python main.py backtest --strategy pm_core --symbol GDX --period 15y
```

---

## Research History

- **2026-04-12:** PM Core 10-day max hold re-enabled. MACD extended to SLV, SILJ, AG. Bull/bear regime split analysis added. Consolidated into single research document.
