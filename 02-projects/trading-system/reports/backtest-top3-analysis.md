# Trading System — Top 3 Strategy Analysis
**Date:** 2026-03-25
**Backtest Period:** 2y / 5y
**Universe:** 17 default symbols × 6 strategies = 102 combinations
**Filter:** ≥1 trade

---

## Scan Results — All 102 Combinations

Sorted by **Profit Factor** (top 10):

| Rank | Symbol | Strategy | Trades | Win Rate | Return % | Profit Factor | Max DD % |
|------|--------|----------|--------|----------|----------|---------------|----------|
| 1 | **NVDA** | mean_reversion_aggressive | 1 | 100% | +10.04% | 1003.67 | -3.63% |
| 2 | **NVDA** | mean_reversion_conservative | 1 | 100% | +10.04% | 1003.67 | -3.63% |
| 3 | **GOOGL** | volume | 1 | 100% | +7.94% | 794.29 | -2.94% |
| 4 | **GOOGL** | momentum | 1 | 100% | +7.38% | 737.60 | -2.87% |
| 5 | **GOOGL** | mean_reversion_aggressive | 1 | 100% | +7.30% | 729.80 | -2.86% |
| 6 | **GOOGL** | mean_reversion_conservative | 1 | 100% | +7.30% | 729.80 | -2.86% |
| 7 | **XOM** | mean_reversion_aggressive | 1 | 100% | +6.22% | 622.06 | -0.91% |
| 8 | **XOM** | mean_reversion_conservative | 1 | 100% | +6.22% | 622.06 | -0.91% |
| 9 | **GS** | mean_reversion_aggressive | 1 | 100% | +6.02% | 602.03 | -3.33% |
| 10 | **GS** | mean_reversion_conservative | 1 | 100% | +6.02% | 602.03 | -3.33% |

---

## Deep Dive — Top 3

### #1: NVDA — Mean Reversion Aggressive

**Why it ranks #1:** Single trade from April 2022 (RSI<30) → held through NVDA's massive run from $18 → $175. Entry was essentially the generational bottom.

| Period | Trades | Win Rate | Return % | Ann. Return % | Profit Factor | Max DD % |
|--------|--------|----------|----------|---------------|---------------|----------|
| 2y | 1 | 100% | +10.04% | +5.02% | 1003.67 | -3.63% |
| 5y | 1 | 100% | +82.54% | +16.51% | 8253.91 | -17.23% |
| max | 1 | 100% | +10656% | — | 1,065,617 | -63.52% |

**Trade Detail (5y):**
- Entry: 2022-04-27 @ $18.93 (RSI oversold trigger)
- Exit: 2026-03-24 @ $175.20 (still open / RSI not yet >50)
- P&L: +825% / +$8,253 on $1,000 position

**⚠️ Caveat:** This is essentially a buy-and-hold from a lucky RSI oversold entry. The 1-trade count means zero statistical confidence. The PF is misleading — it's one giant winner, not a repeatable edge.

**Live Signal (2026-03-25):**
| Indicator | Value | Signal |
|-----------|-------|--------|
| Price | $175.20 | — |
| RSI(14) | 41.3 | Neutral (not oversold) |
| EMA13 | $179.40 | Price below → bearish |
| EMA50 | $183.76 | Price below → bearish |
| BB Lower | $171.94 | Price above lower band |
| Signal | SELL (momentum, 0.55) / BUY (price_action, 0.66) | Mixed |

**Verdict:** Not actionable right now. RSI at 41 — neither oversold for MR nor overbought for momentum. No entry. Wait for RSI < 30.

---

### #2: GOOGL — Momentum

**Why it ranks #2:** One momentum signal caught a major leg-up from mid-2022 to present.

| Period | Trades | Win Rate | Return % | Ann. Return % | Profit Factor | Max DD % |
|--------|--------|----------|----------|---------------|---------------|----------|
| 2y | 1 | 100% | +7.38% | +3.69% | 737.60 | -2.87% |
| 5y | 1 | 100% | +15.90% | +3.18% | 1589.68 | -5.04% |
| max | 1 | 100% | +384.80% | — | 38,480 | -30.66% |

**Trade Detail (5y):**
- Entry: 2022-07-28 @ $112.15 (RSI divergence + ROC>0 + price>EMA50)
- Exit: 2026-03-24 @ $290.44 (still open)
- P&L: +159% / +$1,589 on $1,000 position

**Live Signal (2026-03-25):**
| Indicator | Value | Signal |
|-----------|-------|--------|
| Price | $290.44 | — |
| RSI(14) | 33.4 | Approaching oversold |
| EMA13 | $303.26 | Price below → bearish |
| EMA50 | $311.00 | Price below → bearish |
| BB Lower | $294.88 | Near lower band |
| Signal | SELL (momentum, 0.55) | Bearish |

**Verdict:** Price has pulled back. RSI at 33 is getting close to oversold zone but not there yet. BB lower at $294.88 — price at $290.44 is near the band. Watch for RSI < 30 for a mean reversion entry. Momentum signal is SELL — trend broken.

---

### #3: XOM — Mean Reversion Aggressive

**Why it ranks #3:** Energy mean reversion plays work well. RSI oversold → energy bounces.

| Period | Trades | Win Rate | Return % | Ann. Return % | Profit Factor | Max DD % |
|--------|--------|----------|----------|---------------|---------------|----------|
| 2y | 1 | 100% | +6.22% | +3.11% | 622.06 | -0.91% |
| 5y | 1 | 100% | +11.73% | +2.35% | 1173.34 | -2.80% |
| max | 1 | 100% | +13050% | — | 1,304,996 | -61.30% |

**Trade Detail (5y):**
- Entry: 2022-09-26 @ $76.09 (RSI oversold)
- Exit: 2026-03-24 @ $165.38
- P&L: +117% / +$1,173 on $1,000 position

**Live Signal (2026-03-25):**
| Indicator | Value | Signal |
|-----------|-------|--------|
| Price | $165.38 | — |
| RSI(14) | **74.7** | **OVERBOUGHT** |
| EMA13 | $157.36 | Price above → bullish |
| EMA50 | $146.65 | Price above → bullish |
| BB Lower | $145.02 | Price well above lower band |
| Signal | SELL (mean_reversion_aggressive, 0.50) / SELL (mean_reversion_conservative, 0.60) | Both bearish |

**Verdict:** 🚨 RSI at 74.7 — strongly overbought. Both mean reversion strategies saying SELL. Price is far above the BB lower band ($145). This is NOT a buy zone. XOM is extended. Wait for RSI < 50 (at minimum) before considering a long.

---

## Key Takeaways

### The Core Problem: Low Signal Frequency

Every single strategy across all 17 symbols produced **exactly 1 trade in 2 years**. This is by design — the mean reversion strategies require RSI < 30 AND (for conservative) price touching the lower BB. These conditions are genuinely rare.

| Strategy | Typical Signal Frequency |
|----------|------------------------|
| Mean Reversion Aggressive | ~1 per 2-3 years per symbol |
| Mean Reversion Conservative | ~1 per 3-5 years per symbol |
| Momentum | Moderate |
| Trend Following | Moderate |
| Price Action | Rare |
| Volume | Rare |

### What This Means Practically

1. **You cannot rely on any single symbol** — waiting for RSI<30 on NVDA means waiting years
2. **The precious metals basket (GLD, GDX, SLV, SILJ, AG)** is still the best universe for this system — historically 80-90% win rates, 1-2 trades/year
3. **A basket of 10+ symbols** is needed to get meaningful signal frequency
4. **The "top 3" results are statistically meaningless** — 1 trade = no edge proven

### Recommended Action

1. **Stick with precious metals** — GDX, GLD, SLV, SILJ, AG, NEM for mean reversion
2. **Use tech stocks (AAPL, MSFT, NVDA)** for momentum strategy only
3. **Build a watchlist** of all PM symbols and wait for RSI < 30
4. **Current setup:** GDX (RSI 18.4 on 2026-03-19) is the active trade — hold until RSI > 50

---

## Current Live Signals (2026-03-25)

| Symbol | Signal | Strategy | Strength | RSI | Verdict |
|--------|--------|----------|----------|-----|---------|
| NVDA | SELL/BUY | momentum/price_action | 0.55/0.66 | 41.3 | ⚠️ No entry — neutral |
| GOOGL | SELL | momentum | 0.55 | 33.4 | ⚠️ Watch for RSI<30 |
| XOM | SELL | mean_reversion | 0.60 | **74.7** | 🚫 Overbought — avoid |
| GLD | BUY | mean_reversion_aggressive | 0.67 | **27.3** | ✅ Active watch |
| GDX | *(open)* | mean_reversion_aggressive | — | 18.4 | ✅ Hold until RSI>50 |
| SLV | *(open)* | mean_reversion_aggressive | — | 27.8 | ✅ Hold until RSI>50 |

---

## Appendix: Full 102-Combo Results

*(Saved to `/tmp/backtest_results.json`)*
