"""Technical indicators calculation module."""

import pandas as pd
import numpy as np
from datetime import datetime

# Import from ta submodules
from ta.trend import EMAIndicator, MACD, ADXIndicator, SMAIndicator
from ta.momentum import RSIIndicator, ROCIndicator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add all indicators to DataFrame. Returns df with new columns added."""
    df = df.copy()
    
    # EMA (Exponential Moving Average)
    df['ema_13'] = EMAIndicator(df['close'], window=13).ema_indicator()
    df['ema_50'] = EMAIndicator(df['close'], window=50).ema_indicator()
    df['ema_200'] = EMAIndicator(df['close'], window=200).ema_indicator()
    
    # RSI (Relative Strength Index)
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    
    # Bollinger Bands
    bb = BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_lower'] = bb.bollinger_lband()
    
    # MACD
    macd = MACD(df['close'], window_fast=12, window_slow=26, window_sign=9)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_hist'] = macd.macd_diff()
    
    # ADX (Wilder's smoothing)
    adx = ADXIndicator(df['high'], df['low'], df['close'], window=14)
    df['adx'] = adx.adx()
    
    # OBV
    df['obv'] = OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
    
    # VWAP (approximate with cumsum)
    df['vwap'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    
    # ROC (Rate of Change)
    df['roc'] = ROCIndicator(df['close'], window=12).roc()
    
    # Volume SMA (20-day for comparison)
    df['volume_sma_20'] = SMAIndicator(df['volume'], window=20).sma_indicator()
    
    return df


def get_latest_indicators(df: pd.DataFrame) -> dict:
    """Return dict of latest values for all indicators."""
    latest = df.iloc[-1]
    
    indicators = {
        'ema_13': float(latest['ema_13']) if pd.notna(latest.get('ema_13')) else None,
        'ema_50': float(latest['ema_50']) if pd.notna(latest.get('ema_50')) else None,
        'ema_200': float(latest['ema_200']) if pd.notna(latest.get('ema_200')) else None,
        'rsi': float(latest['rsi']) if pd.notna(latest.get('rsi')) else None,
        'bb_upper': float(latest['bb_upper']) if pd.notna(latest.get('bb_upper')) else None,
        'bb_middle': float(latest['bb_middle']) if pd.notna(latest.get('bb_middle')) else None,
        'bb_lower': float(latest['bb_lower']) if pd.notna(latest.get('bb_lower')) else None,
        'macd': float(latest['macd']) if pd.notna(latest.get('macd')) else None,
        'macd_signal': float(latest['macd_signal']) if pd.notna(latest.get('macd_signal')) else None,
        'macd_hist': float(latest['macd_hist']) if pd.notna(latest.get('macd_hist')) else None,
        'adx': float(latest['adx']) if pd.notna(latest.get('adx')) else None,
        'obv': float(latest['obv']) if pd.notna(latest.get('obv')) else None,
        'vwap': float(latest['vwap']) if pd.notna(latest.get('vwap')) else None,
        'roc': float(latest['roc']) if pd.notna(latest.get('roc')) else None,
        'volume_sma_20': float(latest['volume_sma_20']) if pd.notna(latest.get('volume_sma_20')) else None,
        'close': float(latest['close']),
        'volume': float(latest['volume']),
        'date': str(latest.name) if hasattr(latest.name, '__str__') else str(latest.name)
    }
    
    return indicators


def detect_support_resistance(df: pd.DataFrame, lookback: int = 20) -> dict:
    """Detect support and resistance levels using pivot points and recent highs/lows."""
    if len(df) < lookback:
        lookback = len(df)
    
    recent = df.tail(lookback)
    
    # Recent highs and lows
    highest_high = float(recent['high'].max())
    lowest_low = float(recent['low'].min())
    
    # Pivot points (classic formula)
    pivot = (recent.iloc[-1]['high'] + recent.iloc[-1]['low'] + recent.iloc[-1]['close']) / 3
    r1 = 2 * pivot - recent.iloc[-1]['low']
    s1 = 2 * pivot - recent.iloc[-1]['high']
    r2 = pivot + (recent.iloc[-1]['high'] - recent.iloc[-1]['low'])
    s2 = pivot - (recent.iloc[-1]['high'] - recent.iloc[-1]['low'])
    
    # Find swing highs and lows
    swing_highs = []
    swing_lows = []
    
    for i in range(2, len(recent) - 2):
        # Swing high: higher than both adjacent bars
        if (recent.iloc[i]['high'] > recent.iloc[i-1]['high'] and 
            recent.iloc[i]['high'] > recent.iloc[i+1]['high'] and
            recent.iloc[i]['high'] > recent.iloc[i-2]['high'] and 
            recent.iloc[i]['high'] > recent.iloc[i+2]['high']):
            swing_highs.append(float(recent.iloc[i]['high']))
        
        # Swing low: lower than both adjacent bars
        if (recent.iloc[i]['low'] < recent.iloc[i-1]['low'] and 
            recent.iloc[i]['low'] < recent.iloc[i+1]['low'] and
            recent.iloc[i]['low'] < recent.iloc[i-2]['low'] and 
            recent.iloc[i]['low'] < recent.iloc[i+2]['low']):
            swing_lows.append(float(recent.iloc[i]['low']))
    
    # Cluster nearby levels (within 1% tolerance)
    def cluster_levels(levels, tolerance=0.01):
        if not levels:
            return []
        sorted_levels = sorted(levels)
        clusters = [[sorted_levels[0]]]
        
        for level in sorted_levels[1:]:
            if level <= clusters[-1][-1] * (1 + tolerance):
                clusters[-1].append(level)
            else:
                clusters.append([level])
        
        # Return average of each cluster
        return [np.mean(cluster) for cluster in clusters]
    
    resistance_levels = sorted(set(cluster_levels(swing_highs) + [r1, r2, highest_high]), reverse=True)
    support_levels = sorted(set(cluster_levels(swing_lows) + [s1, s2, lowest_low]))
    
    return {
        'resistance': resistance_levels[:5],  # Top 5 resistance levels
        'support': support_levels[:5],        # Top 5 support levels
        'pivot': float(pivot),
        'r1': float(r1),
        's1': float(s1),
        'r2': float(r2),
        's2': float(s2),
        'lookback': lookback
    }
