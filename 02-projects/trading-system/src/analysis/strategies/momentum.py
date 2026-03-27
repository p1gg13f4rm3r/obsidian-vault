"""Momentum strategy.

Entry: RSI divergence detection (price makes lower low, RSI makes higher low) 
       AND ROC > 0 AND price > EMA50
Exit: RSI crosses below 50 OR ROC < -5
"""

from datetime import datetime
import pandas as pd
import numpy as np


def generate_signal(df: pd.DataFrame) -> dict:
    """Generate momentum signal from indicators DataFrame."""
    if len(df) < 25:  # Need enough bars for divergence detection
        return None
    
    latest = df.iloc[-1]
    prev1 = df.iloc[-2] if len(df) > 1 else None
    prev5 = df.iloc[-6] if len(df) > 5 else None
    prev10 = df.iloc[-11] if len(df) > 10 else None
    
    # Check if we have enough data for indicators
    if pd.isna(latest['rsi']) or pd.isna(latest['roc']) or pd.isna(latest['ema_50']):
        return None
    
    price = float(latest['close'])
    rsi = float(latest['rsi'])
    roc = float(latest['roc'])
    ema_50 = float(latest['ema_50'])
    
    # Previous RSI values for divergence check
    prev_rsi_values = df['rsi'].iloc[-10:-1].dropna()
    
    # Detect bullish divergence
    # Price: current is lower than price ~5-10 bars ago
    # RSI: current is higher than RSI ~5-10 bars ago
    bullish_divergence = False
    if len(prev_rsi_values) >= 5 and prev5 is not None and prev10 is not None:
        price_5_ago = float(prev5['close'])
        price_10_ago = float(prev10['close']) if prev10 is not None else float(df.iloc[-11]['close'])
        rsi_5_ago = float(df.iloc[-6]['rsi']) if not pd.isna(df.iloc[-6]['rsi']) else rsi
        rsi_10_ago = float(df.iloc[-11]['rsi']) if not pd.isna(df.iloc[-11]['rsi']) else rsi
        
        # Check for divergence in the lookback window
        for i in range(3, len(prev_rsi_values)):
            idx = -i
            price_past = float(df.iloc[idx - 3]['close']) if idx - 3 >= -len(df) else None
            rsi_past = float(prev_rsi_values.iloc[i - 1]) if i - 1 < len(prev_rsi_values) else None
            
            if price_past is not None and rsi_past is not None:
                # Price made a lower low, RSI made a higher low
                if price < price_past and rsi > rsi_past:
                    bullish_divergence = True
                    break
    
    # Entry conditions
    has_momentum = roc > 0
    above_ema50 = price > ema_50
    
    if bullish_divergence and has_momentum and above_ema50:
        # Calculate strength based on ROC and RSI
        if roc > 10:
            strength = 0.80 + min(roc / 50, 0.2)  # 0.80-1.0
        elif roc > 5:
            strength = 0.60 + (roc - 5) / 25  # 0.60-0.80
        else:
            strength = 0.45 + roc / 22  # 0.45-0.60
        
        return {
            'signal': 'BUY',
            'strategy': 'momentum',
            'strength': round(strength, 2),
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': f'Bullish divergence with ROC={roc:.1f}%, RSI={rsi:.1f}'
        }
    
    # Exit conditions
    rsi_exit = rsi < 50
    momentum_loss = roc < -5
    
    if rsi_exit or momentum_loss:
        reason = 'RSI below 50' if rsi_exit else f'Negative momentum ROC={roc:.1f}%'
        return {
            'signal': 'SELL',
            'strategy': 'momentum',
            'strength': 0.55,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'reason': reason
        }
    
    return None
