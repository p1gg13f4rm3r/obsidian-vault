"""Price action strategy.

Entry: Price bounces from support (EMA50 or BB lower) 
       OR breaks resistance with volume > 20-day MA volume
Exit: Price falls below support OR retests broken resistance
LOW signal frequency — rarely triggers
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate price action signal from indicators DataFrame."""
    if len(df) < 25:  # Need enough bars for analysis
        return None
    
    latest = df.iloc[-1]
    prev1 = df.iloc[-2] if len(df) > 1 else None
    prev2 = df.iloc[-3] if len(df) > 2 else None
    
    # Check if we have enough data for indicators
    if (pd.isna(latest.get('ema_50')) or pd.isna(latest.get('bb_lower')) or 
        pd.isna(latest.get('volume_sma_20'))):
        return None
    
    price = float(latest['close'])
    ema_50 = float(latest['ema_50'])
    bb_lower = float(latest['bb_lower'])
    bb_upper = float(latest['bb_upper'])
    volume = float(latest['volume'])
    volume_ma = float(latest['volume_sma_20'])
    prev_price = float(prev1['close']) if prev1 is not None else price
    prev2_price = float(prev2['close']) if prev2 is not None else prev_price
    
    # Support levels
    support = min(ema_50, bb_lower)
    
    # Detect bounce from support
    # Previous bars were at or below support, current bar closes above
    prev_low = float(prev1['low']) if prev1 is not None else price
    bounce_from_support = (prev_low <= support * 1.02) and (price > support)
    
    # Detect break of resistance with volume confirmation
    # Calculate simple resistance (recent swing high or BB upper)
    recent_highs = df['high'].iloc[-10:-1]
    resistance = float(max(recent_highs.max(), bb_upper)) if len(recent_highs) > 0 else bb_upper
    
    volume_confirmed = volume > volume_ma * 1.2
    broke_resistance = (prev_price < resistance) and (price > resistance)
    
    # Entry signals
    if bounce_from_support:
        # Moderate volume on bounce is good
        vol_ratio = volume / volume_ma if volume_ma > 0 else 1
        strength = 0.55 + min(vol_ratio * 0.15, 0.25)  # 0.55-0.80
        
        return {
            'signal': 'BUY',
            'strategy': 'price_action',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Bounce from support level {support:.2f}'
        }
    
    elif broke_resistance and volume_confirmed:
        # Breakout with volume confirmation - stronger signal
        vol_ratio = volume / volume_ma if volume_ma > 0 else 1
        strength = 0.70 + min((vol_ratio - 1) * 0.25, 0.30)  # 0.70-1.0
        
        return {
            'signal': 'BUY',
            'strategy': 'price_action',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Breakout above resistance {resistance:.2f} with volume {vol_ratio:.1f}x MA'
        }
    
    # Exit signals
    # Price falls below support
    fell_below_support = price < support * 0.98
    
    # Retest of broken resistance (price returns to broken level)
    retest_resistance = (price < resistance * 1.02) and (prev_price > resistance)
    
    if fell_below_support:
        return {
            'signal': 'SELL',
            'strategy': 'price_action',
            'strength': 0.65,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Price fell below support {support:.2f}'
        }
    
    elif retest_resistance:
        return {
            'signal': 'SELL',
            'strategy': 'price_action',
            'strength': 0.50,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Retest of broken resistance at {resistance:.2f}'
        }
    
    return None
