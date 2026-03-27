"""
Backtesting engine for strategy evaluation.

Algorithm:
1. Fetch historical data for symbol (use fetcher + add indicators)
2. Iterate through bars, generate signals using the strategy
3. Entry: next day OPEN after signal, buy for $1000 worth
4. Exit rules:
   - Strategy-specific exit (from strategy module)
   - Minimum hold: 5 days
5. Track: entry_date, entry_price, exit_date, exit_price, pnl_pct
6. Calculate: total_return, annualized_return, max_drawdown, win_rate,
   profit_factor, total_trades, avg_duration_days
"""

import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import pandas as pd

logger = logging.getLogger(__name__)

# ── Resolve project root ──────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

from src.data import fetcher
from src.analysis import indicators as ind_mod
from src.analysis.strategies import (
    trend_following,
    mean_reversion_aggressive,
    mean_reversion_conservative,
    momentum,
    price_action,
    volume,
)

STRATEGY_MAP = {
    'trend_following':           trend_following,
    'mean_reversion_aggressive': mean_reversion_aggressive,
    'mean_reversion_conservative': mean_reversion_conservative,
    'momentum':                  momentum,
    'price_action':              price_action,
    'volume':                   volume,
}

ALL_STRATEGIES = list(STRATEGY_MAP.keys())


# ── Period → start date ───────────────────────────────────────────────────────

def _period_start(period: str) -> str:
    """Convert yfinance period string to a start date YYYY-MM-DD."""
    now = datetime.now()
    mapping = {
        '1mo': 30, '3mo': 90, '6mo': 180,
        '1y': 365, '2y': 730, '5y': 1825,
    }
    days = mapping.get(period, 365)
    start = now - timedelta(days=days)
    return start.strftime('%Y-%m-%d')


# ── Core backtest ─────────────────────────────────────────────────────────────

def _run_single_backtest(
    symbol: str,
    strategy_name: str,
    period: str = '2y',
    initial_capital: float = 10_000.0,
    position_size: float = 1_000.0,
) -> Dict[str, Any]:
    """Run backtest for a single strategy on a single symbol."""

    # 1. Fetch & add indicators
    df = fetcher.fetch_symbol(symbol, period=period)
    if df is None or df.empty or len(df) < 60:
        return _empty_result(strategy_name, symbol, period)

    df = ind_mod.add_indicators(df)
    df = df.dropna(subset=['rsi', 'ema_13', 'ema_50', 'ema_200',
                            'bb_upper', 'bb_middle', 'bb_lower'])
    if len(df) < 30:
        return _empty_result(strategy_name, symbol, period)

    strategy_mod = STRATEGY_MAP.get(strategy_name)
    if strategy_mod is None:
        return _empty_result(strategy_name, symbol, period)

    # 2. Simulate bar-by-bar
    cash       = initial_capital
    position   = None   # {'entry_bar': int, 'entry_price': float, 'quantity': float}
    trades     = []
    equity     = []
    bars       = df.reset_index(drop=True)
    n          = len(bars)

    for i in range(n):
        date_i = bars.iloc[i]['date'] if 'date' in bars.columns else str(bars.index[i])
        price_i = float(bars.iloc[i]['close'])
        bar_df  = bars.iloc[:i+1]

        # ── Check for exit ──────────────────────────────────────────────────
        if position is not None:
            hold_days = i - position['entry_bar']
            sig_exit  = strategy_mod.generate_exit_signal(bar_df) if hasattr(strategy_mod, 'generate_exit_signal') else None

            if (hold_days >= 5) and (sig_exit in ('SELL', 'EXIT') or (sig_exit is not None and sig_exit)):
                exit_price = float(bars.iloc[min(i+1, n-1)]['open'])
                pnl_pct    = (exit_price - position['entry_price']) / position['entry_price']
                pnl_dollar = pnl_pct * position['quantity'] * position['entry_price']
                cash      += position['quantity'] * exit_price
                trades.append({
                    'entry_date':   position['entry_date'],
                    'entry_price':  position['entry_price'],
                    'exit_date':    date_i,
                    'exit_price':   exit_price,
                    'pnl_pct':      round(pnl_pct * 100, 4),
                    'pnl_dollar':   round(pnl_dollar, 2),
                    'hold_days':    hold_days,
                    'symbol':        symbol,
                    'strategy':     strategy_name,
                })
                position = None

        # ── Check for entry ─────────────────────────────────────────────────
        if position is None and cash >= position_size:
            sig = strategy_mod.generate_signal(bar_df)
            if sig is not None and sig.get('signal') in ('BUY', 'LONG'):
                next_idx     = min(i + 1, n - 1)
                entry_price  = float(bars.iloc[next_idx]['open'])
                quantity     = position_size / entry_price
                cash        -= position_size
                position     = {
                    'entry_bar':   next_idx,
                    'entry_date':  date_i,
                    'entry_price': entry_price,
                    'quantity':    quantity,
                }

        # ── Equity snapshot ─────────────────────────────────────────────────
        equity_val = cash + (position['quantity'] * price_i if position else 0)
        equity.append({'date': date_i, 'equity': equity_val})

    # ── Close any open position at end ─────────────────────────────────────────
    if position is not None:
        exit_price  = float(bars.iloc[-1]['close'])
        pnl_pct     = (exit_price - position['entry_price']) / position['entry_price']
        pnl_dollar  = pnl_pct * position['quantity'] * position['entry_price']
        cash        += position['quantity'] * exit_price
        trades.append({
            'entry_date':   position['entry_date'],
            'entry_price':  position['entry_price'],
            'exit_date':    bars.iloc[-1]['date'] if 'date' in bars.columns else str(bars.index[-1]),
            'exit_price':   exit_price,
            'pnl_pct':      round(pnl_pct * 100, 4),
            'pnl_dollar':   round(pnl_dollar, 2),
            'hold_days':    len(bars) - position['entry_bar'],
            'symbol':        symbol,
            'strategy':     strategy_name,
        })
        position = None

    # ── Compute metrics ────────────────────────────────────────────────────────
    final_equity = cash
    total_return = (final_equity - initial_capital) / initial_capital * 100

    winning   = [t for t in trades if t['pnl_dollar'] > 0]
    losing    = [t for t in trades if t['pnl_dollar'] <= 0]
    n_trades  = len(trades)

    win_rate  = len(winning) / n_trades * 100 if n_trades else 0.0
    avg_gain  = sum(t['pnl_pct'] for t in winning) / len(winning) if winning else 0.0
    avg_loss  = sum(t['pnl_pct'] for t in losing)  / len(losing)  if losing  else 0.0
    total_g   = sum(t['pnl_dollar'] for t in winning)
    total_l   = abs(sum(t['pnl_dollar'] for t in losing))
    profit_factor = total_g / total_l if total_l else (total_g or 0.0)

    # Max drawdown
    eq_series = pd.Series([e['equity'] for e in equity])
    rolling_max = eq_series.cummax()
    drawdown    = (eq_series - rolling_max) / rolling_max * 100
    max_dd      = drawdown.min() if not drawdown.empty else 0.0

    # Annualised return
    years    = (datetime.now() - datetime.strptime(_period_start(period), '%Y-%m-%d')).days / 365
    ann_ret  = total_return / years if years > 0 else total_return

    return {
        'strategy':             strategy_name,
        'symbol':               symbol,
        'period':              period,
        'start_date':          _period_start(period),
        'end_date':            datetime.now().strftime('%Y-%m-%d'),
        'initial_capital':     initial_capital,
        'final_equity':         round(final_equity, 2),
        'total_return_pct':    round(total_return, 4),
        'annualized_return_pct': round(ann_ret, 4),
        'max_drawdown_pct':    round(max_dd, 4),
        'win_rate':            round(win_rate, 2),
        'avg_gain_pct':        round(avg_gain, 4),
        'avg_loss_pct':        round(abs(avg_loss), 4),
        'profit_factor':       round(profit_factor, 4),
        'total_trades':        n_trades,
        'winning_trades':      len(winning),
        'losing_trades':       len(losing),
        'avg_trade_duration_days': round(
            sum(t['hold_days'] for t in trades) / n_trades, 1
        ) if n_trades else 0,
        'trades':              trades,
        'status':              'completed',
    }


def _empty_result(strategy: str, symbol: str, period: str) -> Dict[str, Any]:
    return {
        'strategy': strategy, 'symbol': symbol, 'period': period,
        'total_return_pct': 0.0, 'win_rate': 0.0, 'profit_factor': 0.0,
        'total_trades': 0, 'winning_trades': 0, 'losing_trades': 0,
        'max_drawdown_pct': 0.0, 'annualized_return_pct': 0.0,
        'avg_trade_duration_days': 0, 'trades': [],
        'status': 'no_data',
    }


# ── Public API ───────────────────────────────────────────────────────────────

def run_backtest(
    strategy: Optional[str] = None,
    symbol:   Optional[str] = None,
    period:   str = '2y',
    all_strategies: bool = False,
) -> Dict[str, Any]:
    """
    CLI-friendly wrapper.

    - single strategy + symbol → single result dict
    - all_strategies=True     → dict with 'results' key
    """
    sym  = (symbol or 'SPY').upper()
    strat = strategy or 'mean_reversion_aggressive'

    if all_strategies:
        results = {}
        for s in ALL_STRATEGIES:
            logger.info("Backtesting %s / %s", sym, s)
            results[s] = _run_single_backtest(sym, s, period)
        return {
            'all_strategies': True,
            'symbol': sym,
            'period': period,
            'results': results,
        }

    return _run_single_backtest(sym, strat, period)


def backtest_strategy(
    symbol: str,
    strategy: str,
    start_date: str = None,
    end_date: str = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Legacy compatibility wrapper. Ignores start/end dates — uses yfinance period."""
    del start_date, end_date, parameters  # unused
    return _run_single_backtest(symbol.upper(), strategy)


def compare_strategies(symbol: str, period: str = '1y') -> Dict[str, Any]:
    """Compare all strategies for a symbol."""
    results = run_backtest(all_strategies=True, symbol=symbol, period=period)
    rows = [
        {
            'strategy':   k,
            'return_pct': v.get('total_return_pct', 0),
            'win_rate':   v.get('win_rate', 0),
            'pf':         v.get('profit_factor', 0),
            'trades':     v.get('total_trades', 0),
            'max_dd':     v.get('max_drawdown_pct', 0),
        }
        for k, v in results.get('results', {}).items()
    ]
    rows.sort(key=lambda x: x['return_pct'], reverse=True)
    return {'symbol': symbol.upper(), 'period': period, 'comparison': rows}
