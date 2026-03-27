"""Volume-based strategy.

Entry: OBV rising AND price > EMA13 AND volume > 20-day volume MA
Exit: OBV falling OR volume collapse below MA
LOW signal frequency — rarely triggers
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate volume-based signal from indicators DataFrame."""
    if len(df) < 25:  # Need enough bars for volume MA and EMA13
        return None
    
    latest = df.iloc[-1]
    prev1 = df.iloc[-2] if len(df) > 1 else None
    prev2 = df.iloc[-3] if len(df) > 2 else None
    
    # Check if we have enough data for indicators
    if (pd.isna(latest.get('obv')) or pd.isna(latest.get('ema_13')) or 
        pd.isna(latest.get('volume_sma_20'))):
        return None
    
    price = float(latest['close'])
    ema_13 = float(latest['ema_13'])
    volume = float(latest['volume'])
    volume_ma = float(latest['volume_sma_20'])
    obv = float(latest['obv'])
    
    # Previous values for trend detection
    prev_obv = float(prev1['obv']) if prev1 is not None and not pd.isna(prev1['obv']) else obv
    prev2_obv = float(prev2['obv']) if prev2 is not None and not pd.isna(prev2['obv']) else prev_obv
    
    # Check OBV trend (rising = higher highs and higher lows)
    obv_rising = (obv > prev_obv) and (prev_obv >= prev2_obv)
    obv_falling = (obv < prev_obv) and (prev_obv <= prev2_obv)
    
    # Entry conditions
    above_ema13 = price > ema_13
    volume_expanding = volume > volume_ma * 1.15  # Volume above MA by 15%
    
    if obv_rising and above_ema13 and volume_expanding:
        # Calculate strength based on volume and OBV momentum
        vol_ratio = volume / volume_ma if volume_ma > 0 else 1
        obv_momentum = (obv - prev_obv) / prev_obv if prev_obv > 0 else 0
        
        strength = 0.60 + min(vol_ratio * 0.15, 0.25) + min(obv_momentum * 10, 0.15)
        strength = min(strength, 1.0)
        
        return {
            'signal': 'BUY',
            'strategy': 'volume',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'OBV rising, price above EMA13, volume {vol_ratio:.1f}x MA'
        }
    
    # Exit conditions
    volume_collapsed = volume < volume_ma * 0.7
    
    if obv_falling:
        return {
            'signal': 'SELL',
            'strategy': 'volume',
            'strength': 0.55,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': 'OBV turning down'
        }
    
    elif volume_collapsed:
        return {
            'signal': 'SELL',
            'strategy': 'volume',
            'strength': 0.45,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Volume collapse to {volume/volume_ma*100:.0f}% of MA'
        }
    
    return None
