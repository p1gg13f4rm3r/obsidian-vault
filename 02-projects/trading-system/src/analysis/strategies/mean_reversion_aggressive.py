"""Mean reversion - aggressive version.

Entry: RSI < 30 → BUY
Exit: RSI > 50
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate mean reversion (aggressive) signal from indicators DataFrame."""
    if len(df) < 20:  # Need at least RSI length
        return None
    
    latest = df.iloc[-1]
    
    # Check if we have enough data for RSI
    if pd.isna(latest['rsi']):
        return None
    
    price = float(latest['close'])
    rsi = float(latest['rsi'])
    
    if rsi < 30:
        # Oversold - potential mean reversion buy
        # Calculate strength based on how oversold
        if rsi < 20:
            strength = 0.75 + (20 - rsi) / 40  # 0.75-1.0 for very oversold
        elif rsi < 25:
            strength = 0.50 + (25 - rsi) / 10  # 0.50-0.75
        else:
            strength = 0.40 + (30 - rsi) / 10  # 0.40-0.50
        
        return {
            'signal': 'BUY',
            'strategy': 'mean_reversion_aggressive',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Oversold RSI={rsi:.1f}'
        }
    
    elif rsi > 50:
        # Overbought or normalized - exit signal
        return {
            'signal': 'SELL',
            'strategy': 'mean_reversion_aggressive',
            'strength': 0.5,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'RSI normalized at {rsi:.1f}'
        }
    
    return None
