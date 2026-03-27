"""Mean reversion - conservative version.

Entry: RSI < 30 AND price within 2% of lower BB → BUY
Exit: RSI > 50
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate mean reversion (conservative) signal from indicators DataFrame."""
    if len(df) < 20:  # Need at least BB length
        return None
    
    latest = df.iloc[-1]
    
    # Check if we have enough data for indicators
    if pd.isna(latest['rsi']) or pd.isna(latest['bb_lower']):
        return None
    
    price = float(latest['close'])
    rsi = float(latest['rsi'])
    bb_lower = float(latest['bb_lower'])
    
    # Calculate how close price is to lower Bollinger Band
    distance_to_bb = (price - bb_lower) / bb_lower if bb_lower > 0 else 1
    
    # Entry conditions: RSI oversold AND price within 2% of lower BB
    oversold = rsi < 30
    near_bb_lower = distance_to_bb < 0.02
    
    if oversold and near_bb_lower:
        # Calculate strength based on RSI and distance to BB
        if rsi < 20 and distance_to_bb < 0.01:
            strength = 0.80 + min((20 - rsi) / 40, 0.1)  # 0.80-0.90
        elif rsi < 25:
            strength = 0.60 + (25 - rsi) / 25  # 0.60-0.80
        else:
            strength = 0.45 + (30 - rsi) / 25  # 0.45-0.60
        
        return {
            'signal': 'BUY',
            'strategy': 'mean_reversion_conservative',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Oversold RSI={rsi:.1f}, near BB lower ({distance_to_bb*100:.1f}%)'
        }
    
    elif rsi > 50:
        # RSI normalized - exit signal
        return {
            'signal': 'SELL',
            'strategy': 'mean_reversion_conservative',
            'strength': 0.6,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'RSI normalized at {rsi:.1f}'
        }
    
    return None
