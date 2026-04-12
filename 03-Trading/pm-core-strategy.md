---
date: 2026-04-12
tags: [trading, precious-metals, pm-core, GDX, SLV, SILJ, AG, backtest]
---

# PM Core Strategy

**Status:** Active (10-day max hold re-enabled 2026-04-12)
**Backtest Period:** 15 years (2011-03 to 2026-04)

---

## Rules

### Entry
- RSI(14) < 30 (oversold)
- Rank: GDX → SLV → SILJ → AG (skip NEM, GLD)

### Exit
- RSI(14) > 50, **OR**
- +5% profit target, **OR**
- **10 trading days max hold** (circuit breaker)

### Position Sizing
- 20% of portfolio per trade
- Max 2 concurrent positions
- Entry price: next day open
- Exit price: next day open

---

## 15-Year Backtest Results (10-day rule ENABLED)

| Symbol | Total Return | Win Rate | Profit Factor | Max Drawdown | Avg Hold |
|--------|-------------|----------|---------------|--------------|----------|
| GDX | +7.95% | 59.6% | 1.93 | -2.90% | 5.9 days |
| SLV | +3.95% | 49.0% | 1.49 | -2.66% | 6.9 days |
| SILJ | +5.61% | 55.3% | 1.46 | -3.47% | 5.5 days |
| AG | +0.71% | 56.3% | 1.04 | -7.11% | 5.0 days |

> **Note:** Results assume $100K starting capital, 20% position size. Returns are dollar P&L, not percentage of portfolio.

### Why the 10-Day Rule Matters

The 10-day max hold is a **circuit breaker** that prevents positions from drifting in choppy, directionless markets. Without it:
- AG would have returned **-2.89%** instead of +0.71%
- SLV would have returned **+1.86%** instead of +3.95%
- 2013 losses would have been **$408 worse**

It slightly reduces profit in strong momentum years (2017, 2024) but saves significantly in bear/chop years.

---

## Symbol Priority

```
GDX (gold miners) → SLV (silver) → SILJ (silver miners) → AG (silver junior)
```

GDX first because it has the highest win rate (59.6%) and best profit factor (1.93). Skip NEM (individual stock risk) and GLD (too correlated to gold itself, less volatile = fewer RSI < 30 opportunities).

---

## Exit Rationale

| Exit Trigger | Why |
|--------------|-----|
| RSI > 50 | Momentum shift — stock is no longer oversold |
| +5% profit | Lock in gains quickly; PM mean reversion is fast |
| 10-day max hold | Prevents hold-through chop; circuit breaker |

---

## Code

`~/obsidian-vault/02-projects/trading-system/src/analysis/strategies/pm_core.py`

Engine enforcement: `~/obsidian-vault/02-projects/trading-system/src/backtest/engine.py`

---

## History

- **2026-04-12:** 10-day max hold re-enabled. Previously disabled per Paul request. Re-enabled after analysis showed it saves ~$667 in losses over 15 years, primarily by preventing AG and SLV from holding through chop.
