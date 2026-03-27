"""Signal generation engine."""

from datetime import datetime
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np

from . import indicators as ind_module


def generate_signals(
    symbol: str,
    strategies: Optional[List[str]] = None,
    indicators_df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """Generate signals for a symbol. Return list of signal dicts.
    
    Args:
        symbol: Trading symbol (e.g., 'AAPL')
        strategies: List of strategy names to run. If None, runs all strategies.
        indicators_df: DataFrame with OHLCV data and precomputed indicators.
                      If None, indicators will be computed from data.
    
    Returns:
        List of signal dictionaries matching the Signal Format.
    """
    if indicators_df is None or indicators_df.empty:
        return []
    
    # Ensure indicators are computed
    if 'rsi' not in indicators_df.columns:
        indicators_df = ind_module.add_indicators(indicators_df)
    
    # Default strategies if none specified
    if strategies is None:
        strategies = [
            'trend_following',
            'mean_reversion_aggressive',
            'mean_reversion_conservative',
            'momentum',
            'price_action',
            'volume'
        ]
    
    signals_list = []
    latest_indicators = ind_module.get_latest_indicators(indicators_df)
    
    for strategy_name in strategies:
        try:
            # Dynamically import the strategy module
            if strategy_name == 'trend_following':
                from .strategies import trend_following
                signal = trend_following.generate_signal(indicators_df)
            elif strategy_name == 'mean_reversion_aggressive':
                from .strategies import mean_reversion_aggressive
                signal = mean_reversion_aggressive.generate_signal(indicators_df)
            elif strategy_name == 'mean_reversion_conservative':
                from .strategies import mean_reversion_conservative
                signal = mean_reversion_conservative.generate_signal(indicators_df)
            elif strategy_name == 'momentum':
                from .strategies import momentum
                signal = momentum.generate_signal(indicators_df)
            elif strategy_name == 'price_action':
                from .strategies import price_action
                signal = price_action.generate_signal(indicators_df)
            elif strategy_name == 'volume':
                from .strategies import volume
                signal = volume.generate_signal(indicators_df)
            else:
                continue
            
            if signal is not None:
                # Ensure signal has all required fields
                signal['symbol'] = symbol
                signal['timestamp'] = datetime.now().isoformat()
                signal['indicators'] = latest_indicators
                signals_list.append(signal)
                
        except Exception as e:
            print(f"Error generating signal for {strategy_name}: {e}")
            continue
    
    return signals_list


def combine_signals(signals_list: List[Dict[str, Any]], method: str = 'strength_weighted') -> Dict[str, Any]:
    """Combine multiple signals into a single decision."""
    if not signals_list:
        return {
            'signal': 'HOLD',
            'strength': 0.0,
            'reason': 'No signals generated'
        }
    
    if method == 'strength_weighted':
        buy_signals = [s for s in signals_list if s.get('signal') == 'BUY']
        sell_signals = [s for s in signals_list if s.get('signal') == 'SELL']
        
        buy_strength = sum(s.get('strength', 0) for s in buy_signals)
        sell_strength = sum(s.get('strength', 0) for s in sell_signals)
        
        if buy_strength > sell_strength * 1.2:
            return {
                'signal': 'BUY',
                'strength': buy_strength / len(buy_signals) if buy_signals else 0,
                'reason': f"Based on {len(buy_signals)} buy signals",
                'all_signals': signals_list
            }
        elif sell_strength > buy_strength * 1.2:
            return {
                'signal': 'SELL',
                'strength': sell_strength / len(sell_signals) if sell_signals else 0,
                'reason': f"Based on {len(sell_signals)} sell signals",
                'all_signals': signals_list
            }
        else:
            return {
                'signal': 'HOLD',
                'strength': max(buy_strength, sell_strength),
                'reason': f"Conflicting signals: {len(buy_signals)} buy, {len(sell_signals)} sell",
                'all_signals': signals_list
            }
    
    return {
        'signal': 'HOLD',
        'strength': 0.0,
        'reason': 'Unknown method',
        'all_signals': signals_list
    }
