"""Trend following strategy.

Entry: Price > EMA50 AND EMA50 > EMA200 (golden cross); ADX > 25
Exit: Price < EMA50 OR ADX < 20
Strength: based on ADX level
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate trend following signal from indicators DataFrame."""
    if len(df) < 50:  # Need at least EMA200 length
        return None
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else None
    
    # Check if we have enough data for indicators
    if pd.isna(latest['ema_50']) or pd.isna(latest['ema_200']):
        return None
    
    price = float(latest['close'])
    ema_50 = float(latest['ema_50'])
    ema_200 = float(latest['ema_200'])
    adx = float(latest['adx'])
    
    # Entry conditions (golden cross pattern)
    golden_cross = price > ema_50 and ema_50 > ema_200
    strong_trend = adx > 25
    
    # Exit conditions
    bearish_cross = price < ema_50
    weak_trend = adx < 20
    
    # Check for existing position direction
    # For simplicity, we focus on current market conditions
    
    if golden_cross and strong_trend:
        # Calculate strength based on ADX
        if adx >= 40:
            strength = 0.85 + min((adx - 40) / 60, 0.15)  # 0.85-1.0
        elif adx >= 30:
            strength = 0.60 + (adx - 30) / 33  # 0.60-0.85
        else:
            strength = 0.40 + (adx - 25) / 12.5  # 0.40-0.60
        
        return {
            'signal': 'BUY',
            'strategy': 'trend_following',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Golden cross with ADX={adx:.1f}'
        }
    
    elif bearish_cross or weak_trend:
        # Exit signal or short opportunity
        if adx < 20:
            reason = f'Trend weakening, ADX={adx:.1f}'
        else:
            reason = f'Price below EMA50'
        
        return {
            'signal': 'SELL',
            'strategy': 'trend_following',
            'strength': 0.5,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': reason
        }
    
    return None
