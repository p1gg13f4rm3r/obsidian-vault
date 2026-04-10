"""VWAP Mean Reversion strategy.

Entry: Price pulls back to VWAP (within 1%) from an extended position
       AND RSI approaching oversold/overbought territory
Exit:  Price far from VWAP OR RSI normalization

Meant to fire more frequently than the strict RSI<30 threshold.
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate VWAP mean reversion signal from indicators DataFrame."""
    if len(df) < 5:
        return None

    latest = df.iloc[-1]
    prev1 = df.iloc[-2] if len(df) > 1 else None
    prev2 = df.iloc[-3] if len(df) > 2 else None

    # Check required indicators
    if (pd.isna(latest.get('vwap')) or
        pd.isna(latest.get('rsi')) or
        pd.isna(latest.get('ema_13'))):
        return None

    price = float(latest['close'])
    vwap = float(latest['vwap'])
    rsi = float(latest['rsi'])
    ema_13 = float(latest['ema_13'])

    prev_price = float(prev1['close']) if prev1 is not None else price
    prev2_price = float(prev2['close']) if prev2 is not None else prev_price

    vwap_ratio = price / vwap if vwap > 0 else 1.0

    # ── Helpers ──────────────────────────────────────────────
    def build_signal(sig, strat, strength, reason):
        return {
            'signal': sig,
            'strategy': strat,
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': reason
        }

    # ── BUY: Price extended below VWAP, pulling back ────────
    # Price is below VWAP by at least 1.5% (oversold zone)
    below_vwap = price < vwap * 0.985

    # Previous bar was even further below (capitulation improving)
    prev_below = prev_price < vwap * 0.985
    prev2_below = prev2_price < vwap * 0.985 if prev2 is not None else prev_below

    # Current price is closer to VWAP than prev bar (recovering)
    recovering = price > prev_price

    # RSI is oversold OR just leaving oversold (potential bottom)
    rsi_oversold = rsi < 40
    rsi_leaving_oversold = (rsi > 30) and (rsi < 45)

    # Only enter if price is recovering toward VWAP, not still falling
    if below_vwap and (recovering or prev_below) and (rsi_oversold or rsi_leaving_oversold):
        # Strength scales with how extended we are from VWAP
        deviation = (vwap - price) / vwap  # how far below we are
        vol_ratio = float(latest['volume']) / float(latest['volume_sma_20']) \
            if not pd.isna(latest.get('volume_sma_20')) and latest['volume_sma_20'] > 0 else 1.0

        strength = 0.55 + min(deviation * 10, 0.15) + min(vol_ratio * 0.10, 0.20)
        strength = min(strength, 0.90)

        reason = (f'Price {vwap_ratio*100:.1f}% of VWAP, '
                  f'RSI={rsi:.1f}, recovering toward VWAP')
        return build_signal('BUY', 'vwap_reversion', strength, reason)

    # ── SELL: Price extended above VWAP, pulling back ────────
    above_vwap = price > vwap * 1.015

    # Previous bar was even further above (momentum exhausting)
    prev_above = prev_price > vwap * 1.015
    prev2_above = prev2_price > vwap * 1.015 if prev2 is not None else prev_above

    # Current price is closer to VWAP than prev bar (pulling back)
    pulling_back = price < prev_price

    # RSI is overbought OR just leaving overbought
    rsi_overbought = rsi > 60
    rsi_leaving_overbought = (rsi < 70) and (rsi > 55)

    if above_vwap and (pulling_back or prev_above) and (rsi_overbought or rsi_leaving_overbought):
        deviation = (price - vwap) / vwap
        vol_ratio = float(latest['volume']) / float(latest['volume_sma_20']) \
            if not pd.isna(latest.get('volume_sma_20')) and latest['volume_sma_20'] > 0 else 1.0

        strength = 0.55 + min(deviation * 10, 0.15) + min(vol_ratio * 0.10, 0.20)
        strength = min(strength, 0.90)

        reason = (f'Price {vwap_ratio*100:.1f}% of VWAP, '
                  f'RSI={rsi:.1f}, pulling back from extended')
        return build_signal('SELL', 'vwap_reversion', strength, reason)

    return None
