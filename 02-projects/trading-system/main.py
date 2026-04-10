#!/usr/bin/env python3
"""
Trading System CLI Entry Point
Main command-line interface for the trading system.
"""

import argparse
import json
import logging
import os
import sys

# Add src/ to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data import fetcher
from src.data import cache as data_cache
from src.analysis import signals
from src.portfolio import stats
from src.backtest import engine
from src.reports import generator


def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_config(config_path: str = None) -> dict:
    """Load configuration from specified path or default."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config')
    return {'config_path': config_path}


def load_symbols(config_path: str) -> dict:
    """Load symbols from config file."""
    symbols_file = os.path.join(config_path, 'symbols.json')
    try:
        with open(symbols_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Symbols config not found: {symbols_file}")
        return {'default': [], 'custom': []}
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in symbols config: {symbols_file}")
        return {'default': [], 'custom': []}


def cmd_analyze(args, config: dict):
    """Handle analyze command."""
    try:
        from src.data import fetcher
        from src.analysis import indicators as ind_mod

        symbol_list = args.symbols.split(',') if args.symbols else None  # None = all from config
        strategy_list = [args.strategy] if args.strategy else None

        # If no symbols specified, load all from config
        if symbol_list is None:
            symbols_data = load_symbols(config.get('config_path', 'config'))
            symbol_list = [s['symbol'] for s in symbols_data.get('default', [])]

        all_signals = []
        for sym in symbol_list:
            sym = sym.strip()
            # Fetch data
            df = fetcher.fetch_symbol(sym, period='3mo')
            if df.empty:
                print(f"Warning: No data for {sym}, skipping.", file=sys.stderr)
                continue
            # Add indicators
            df = ind_mod.add_indicators(df)
            # Generate signals
            sigs = signals.generate_signals(sym, strategies=strategy_list, indicators_df=df)
            all_signals.extend(sigs)

        if args.json:
            print(json.dumps(all_signals, indent=2, default=str))
        else:
            if not all_signals:
                print("No signals generated.")
            else:
                for sig in all_signals:
                    ind = sig.get('indicators', {})
                    print(f"\n{sig['symbol']} | {sig['signal']:4s} | {sig['strategy']:30s} | "
                          f"Strength: {sig['strength']:.2f} | Price: ${sig['price']:.2f}")
                    print(f"  RSI: {ind.get('rsi', 'N/A')}  "
                          f"EMA13: {ind.get('ema_13', 'N/A')}  "
                          f"EMA50: {ind.get('ema_50', 'N/A')}  "
                          f"BB_lower: {ind.get('bb_lower', 'N/A')}")

        sys.exit(0)
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        import traceback; traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_report(args, config: dict):
    """Handle report command."""
    try:
        date = args.date
        latest = args.latest
        
        result = generator.generate_report(date=date, latest=latest)
        
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print("Report Generated:")
            print("-" * 50)
            print(result)
        
        sys.exit(0)
    except Exception as e:
        logging.error(f"Report generation failed: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_portfolio(args, config: dict):
    """Handle portfolio command."""
    try:
        from src.portfolio import tracker

        if args.status:
            open_pos = tracker.get_open_positions()
            closed   = tracker.get_closed_trades()
            print(f"Portfolio Status: Active")
            print("-" * 50)
            print(f"Open Positions:   {len(open_pos)}")
            print(f"Closed Trades:   {len(closed)}")
            print(f"Cash:            $0.00")
            sys.exit(0)

        elif args.stats:
            result = stats.get_portfolio_summary()

            if args.json:
                # default=str handles np.float64 / numpy types
                print(json.dumps(result, indent=2, default=str))
            else:
                print("Portfolio Statistics:")
                print("-" * 50)
                for key, value in result.items():
                    print(f"  {key}: {value}")

            sys.exit(0)

        elif args.add:
            sym     = (args.add or args.symbol or 'SPY').upper()
            strat   = args.strategy or 'mean_reversion_aggressive'
            entry_p = float(args.entry or 0)
            qty     = float(args.quantity or 1)
            from datetime import date
            entry_d = str(date.today())

            trade_id = tracker.add_trade(
                symbol=sym,
                strategy=strat,
                entry_date=entry_d,
                entry_price=entry_p,
                quantity=qty,
            )
            print(f"Position added successfully! (trade_id={trade_id})")
            sys.exit(0)

        else:
            print("Use --status, --stats, or --add")
            sys.exit(1)

    except Exception as e:
        logging.error("Portfolio command failed: %s", e)
        import traceback; traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _sanitize(obj):
    """Convert numpy types to native Python for clean CLI display."""
    import numpy as np
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(x) for x in obj]
    return obj


def cmd_backtest(args, config: dict):
    """Handle backtest command."""
    try:
        result = engine.run_backtest(
            strategy=args.strategy,
            symbol=args.symbol,
            period=args.period,
            all_strategies=args.all_strategies,
        )

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print("Backtest Results:")
            print("-" * 50)
            clean = _sanitize(result)
            if isinstance(clean, dict) and 'results' in clean:
                # all-strategies output
                print(f"  symbol: {clean.get('symbol')}")
                print(f"  period: {clean.get('period')}")
                for strat, res in clean.get('results', {}).items():
                    res_s = _sanitize(res)
                    print(f"\n  [{strat}]")
                    for k, v in res_s.items():
                        if k not in ('trades',):
                            print(f"    {k}: {v}")
            else:
                for key, value in _sanitize(clean).items():
                    if key != 'trades':
                        print(f"  {key}: {value}")

        sys.exit(0)
    except Exception as e:
        logging.error("Backtest failed: %s", e)
        import traceback; traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_symbols(args, config: dict):
    """Handle symbols command."""
    try:
        config_path = config['config_path']
        symbols_data = load_symbols(config_path)
        
        if args.list:
            print("All Symbols:")
            print("-" * 50)
            for sym in symbols_data.get('default', []):
                print(f"  {sym['symbol']} - {sym['name']} ({sym['category']})")
            sys.exit(0)
        
        elif args.list_custom:
            custom = symbols_data.get('custom', [])
            if not custom:
                print("No custom symbols defined.")
            else:
                print("Custom Symbols:")
                print("-" * 50)
                for sym in custom:
                    print(f"  {sym['symbol']} - {sym['name']}")
            sys.exit(0)
        
        elif args.add:
            new_symbol = args.add.upper()
            # Add to custom symbols (simplified)
            print(f"Adding symbol: {new_symbol}")
            print("Note: Custom symbol management coming soon!")
            sys.exit(0)
        
        elif args.remove:
            symbol_to_remove = args.remove.upper()
            print(f"Removing symbol: {symbol_to_remove}")
            print("Note: Symbol removal coming soon!")
            sys.exit(0)
        
        else:
            print("Use --list, --list-custom, --add, or --remove")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Symbols command failed: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_data(args, config: dict):
    """Handle data command."""
    try:
        if args.fetch:
            symbol = args.fetch.upper()
            print(f"Fetching data for: {symbol}")
            df = fetcher.fetch_symbol(symbol)
            if df.empty:
                print(f"No data returned for {symbol}", file=sys.stderr)
                sys.exit(1)
            # Compute indicators before saving
            from src.analysis import indicators as ind_mod
            df = ind_mod.add_indicators(df)
            # Save to SQLite cache
            data_cache.save_data(symbol, df)
            print(f"Data fetched and cached successfully for {symbol}")
            if args.json:
                print(json.dumps({"symbol": symbol, "rows": len(df), "latest_date": str(df.index[-1]) if len(df) else None}, indent=2))
            sys.exit(0)
        
        elif args.refresh_all:
            print("Refreshing all symbol data...")
            symbols_data = load_symbols(config['config_path'])
            all_symbols = [s['symbol'] for s in symbols_data.get('default', [])]
            from src.analysis import indicators as ind_mod
            for symbol in all_symbols:
                print(f"  Refreshing {symbol}...", end=" ")
                df = fetcher.fetch_symbol(symbol)
                if df.empty:
                    print(f"FAILED (no data)")
                    continue
                df = ind_mod.add_indicators(df)
                data_cache.save_data(symbol, df)
                print(f"OK ({len(df)} rows)")
            print("All data refreshed successfully!")
            sys.exit(0)
        
        else:
            print("Use --fetch SYMBOL or --refresh-all")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Data command failed: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all commands and options."""
    parser = argparse.ArgumentParser(
        description='Trading System CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global options - must be defined before subparsers
    parser.add_argument('--config', type=str, default=None,
                        help='Path to config directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output (DEBUG logging)')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output results as JSON')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze symbols')
    analyze_parser.add_argument('--daily', action='store_true',
                                help='Use daily data for analysis')
    analyze_parser.add_argument('--symbols', type=str,
                                help='Comma-separated list of symbols')
    analyze_parser.add_argument('--strategy', type=str,
                                help='Trading strategy to use')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('--date', type=str,
                              help='Report date (YYYY-MM-DD)')
    report_parser.add_argument('--latest', action='store_true',
                              help='Generate latest report')
    
    # Portfolio command
    portfolio_parser = subparsers.add_parser('portfolio', help='Portfolio tracking')
    portfolio_group = portfolio_parser.add_mutually_exclusive_group(required=True)
    portfolio_group.add_argument('--status', action='store_true',
                                help='Show portfolio status')
    portfolio_group.add_argument('--stats', action='store_true',
                                help='Show portfolio statistics')
    portfolio_group.add_argument('--add', type=str,
                                help='Add a position')
    portfolio_parser.add_argument('--symbol', type=str,
                                 help='Symbol for new position')
    portfolio_parser.add_argument('--strategy', type=str,
                                 help='Strategy for new position')
    portfolio_parser.add_argument('--entry', type=float,
                                 help='Entry price for new position')
    portfolio_parser.add_argument('--quantity', type=int,
                                 help='Quantity for new position')
    
    # Backtest command
    backtest_parser = subparsers.add_parser('backtest', help='Run backtest')
    backtest_parser.add_argument('--strategy', type=str,
                                help='Strategy to backtest')
    backtest_parser.add_argument('--symbol', type=str,
                                help='Symbol to backtest')
    backtest_parser.add_argument('--period', type=str, default='1y',
                                help='Backtest period (e.g., 1y, 2y)')
    backtest_parser.add_argument('--all-strategies', action='store_true',
                                help='Run all strategies')
    
    # Symbols command
    symbols_parser = subparsers.add_parser('symbols', help='Manage symbols')
    symbols_group = symbols_parser.add_mutually_exclusive_group(required=True)
    symbols_group.add_argument('--add', type=str,
                              help='Add a symbol')
    symbols_group.add_argument('--remove', type=str,
                              help='Remove a symbol')
    symbols_group.add_argument('--list', action='store_true',
                              help='List all symbols')
    symbols_group.add_argument('--list-custom', action='store_true',
                              help='List custom symbols')
    
    # Data command
    data_parser = subparsers.add_parser('data', help='Data management')
    data_group = data_parser.add_mutually_exclusive_group(required=True)
    data_group.add_argument('--fetch', type=str,
                           help='Fetch data for a symbol')
    data_group.add_argument('--refresh-all', action='store_true',
                           help='Refresh all symbol data')
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Load config
    config = load_config(args.config)
    
    # Route to command handler
    if args.command == 'analyze':
        cmd_analyze(args, config)
    elif args.command == 'report':
        cmd_report(args, config)
    elif args.command == 'portfolio':
        cmd_portfolio(args, config)
    elif args.command == 'backtest':
        cmd_backtest(args, config)
    elif args.command == 'symbols':
        cmd_symbols(args, config)
    elif args.command == 'data':
        cmd_data(args, config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
