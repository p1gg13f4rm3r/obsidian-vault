"""
Report generation module.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def generate_report(
    date: Optional[str] = None,
    latest: bool = False
) -> str:
    """
    Generate a trading report.
    
    Args:
        date: Specific date for report (YYYY-MM-DD)
        latest: Generate latest report
    
    Returns:
        Report as formatted string
    """
    logger.debug(f"Generating report for date={date}, latest={latest}")
    
    if latest or date is None:
        report_date = datetime.now().strftime('%Y-%m-%d')
    else:
        report_date = date
    
    report_lines = [
        "=" * 60,
        f"TRADING SYSTEM REPORT - {report_date}",
        "=" * 60,
        "",
        "Portfolio Summary",
        "-" * 40,
        f"Total Value:      $0.00",
        f"Cash:             $0.00",
        f"Positions:        0",
        f"Day P&L:          $0.00",
        "",
        "Top Performers",
        "-" * 40,
        "No positions held",
        "",
        "Signals Summary",
        "-" * 40,
        "BUY signals:      0",
        "SELL signals:     0",
        "HOLD signals:     0",
        "",
        "Recent Trades",
        "-" * 40,
        "No recent trades",
        "",
        "=" * 60,
        f"Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
    ]
    
    return '\n'.join(report_lines)


def generate_daily_report(symbols: list) -> Dict[str, Any]:
    """
    Generate a daily analysis report for all symbols.
    
    Args:
        symbols: List of symbols to include
    
    Returns:
        Dictionary with report data
    """
    logger.debug(f"Generating daily report for {len(symbols)} symbols")
    
    from ..analysis import signals
    
    signal_results = signals.generate_signals(symbols=symbols, daily=True)
    
    buy_signals = []
    sell_signals = []
    hold_signals = []
    
    for symbol, data in signal_results.items():
        signal = data.get('signal', 'HOLD')
        if signal == 'BUY':
            buy_signals.append({'symbol': symbol, **data})
        elif signal == 'SELL':
            sell_signals.append({'symbol': symbol, **data})
        else:
            hold_signals.append({'symbol': symbol, **data})
    
    return {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total_symbols': len(symbols),
        'buy_signals': buy_signals,
        'sell_signals': sell_signals,
        'hold_signals': hold_signals,
        'summary': {
            'buy_count': len(buy_signals),
            'sell_count': len(sell_signals),
            'hold_count': len(hold_signals)
        }
    }


def generate_performance_report(
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    """
    Generate performance report for a date range.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        Performance metrics dictionary
    """
    logger.debug(f"Generating performance report: {start_date} to {end_date}")
    
    return {
        'period': {
            'start': start_date,
            'end': end_date
        },
        'metrics': {
            'total_return': 0.0,
            'annualized_return': 0.0,
            'volatility': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'win_rate': 0.0
        },
        'trades': {
            'total': 0,
            'winners': 0,
            'losers': 0
        },
        'status': 'generated'
    }


def save_report(report: str, filename: Optional[str] = None) -> str:
    """
    Save a report to file.
    
    Args:
        report: Report content
        filename: Output filename (auto-generated if None)
    
    Returns:
        Path to saved file
    """
    import os
    
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{timestamp}.txt"
    
    reports_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'reports'
    )
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(report)
    
    logger.debug(f"Report saved to {filepath}")
    return filepath
