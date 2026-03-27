"""Symbol management - load, save, and manage symbols from config."""

import os
import json
import logging

logger = logging.getLogger(__name__)

DEFAULT_SYMBOLS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "category": "tech"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "category": "tech"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "category": "tech"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "category": "tech"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.", "category": "tech"},
    {"symbol": "META", "name": "Meta Platforms", "category": "tech"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "category": "tech"},
    {"symbol": "JPM", "name": "JPMorgan Chase", "category": "finance"},
    {"symbol": "BAC", "name": "Bank of America", "category": "finance"},
    {"symbol": "GS", "name": "Goldman Sachs", "category": "finance"},
    {"symbol": "XOM", "name": "Exxon Mobil", "category": "energy"},
    {"symbol": "CVX", "name": "Chevron Corp.", "category": "energy"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "category": "healthcare"},
    {"symbol": "UNH", "name": "UnitedHealth Group", "category": "healthcare"},
    {"symbol": "PFE", "name": "Pfizer Inc.", "category": "healthcare"},
]


def _get_config_path():
    """Get path to config/symbols.json, resolved relative to this file's directory."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(this_dir)
    project_root = os.path.dirname(base_dir)
    config_dir = os.path.join(project_root, "config")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "symbols.json")


def _load_raw():
    """Load raw JSON from config file."""
    config_path = _get_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return None


def _save_raw(data):
    """Save raw JSON to config file."""
    config_path = _get_config_path()
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)


def load_symbols():
    """Load from config/symbols.json, return list of dicts with symbol/name/category."""
    data = _load_raw()
    if data is None:
        logger.info("No symbols.json found, creating with defaults")
        _save_raw({"symbols": DEFAULT_SYMBOLS, "custom": []})
        return DEFAULT_SYMBOLS.copy()

    symbols = data.get("symbols", [])
    custom = data.get("custom", [])
    return symbols + custom


def save_symbols(symbols, custom=None):
    """Save list of dicts back to config/symbols.json."""
    if custom is None:
        custom = [s for s in symbols if s.get("custom", False)]
        default_symbols = [s for s in symbols if not s.get("custom", False)]
    else:
        default_symbols = symbols

    _save_raw({"symbols": default_symbols, "custom": custom})


def add_symbol(symbol, name, category):
    """Add a custom symbol."""
    data = _load_raw()
    if data is None:
        data = {"symbols": DEFAULT_SYMBOLS.copy(), "custom": []}

    custom = data.get("custom", [])
    if any(s.get("symbol") == symbol for s in custom):
        logger.warning("Symbol %s already exists in custom list", symbol)
        return

    custom.append({"symbol": symbol, "name": name, "category": category, "custom": True})
    data["custom"] = custom
    _save_raw(data)
    logger.info("Added custom symbol: %s (%s)", symbol, name)


def remove_symbol(symbol):
    """Remove a custom symbol."""
    data = _load_raw()
    if data is None:
        return

    custom = data.get("custom", [])
    original_len = len(custom)
    custom = [s for s in custom if s.get("symbol") != symbol]

    if len(custom) == original_len:
        logger.warning("Symbol %s not found in custom list", symbol)
        return

    data["custom"] = custom
    _save_raw(data)
    logger.info("Removed custom symbol: %s", symbol)


def get_symbols_by_category(category):
    """Filter by category."""
    symbols = load_symbols()
    return [s for s in symbols if s.get("category") == category]


def get_all_symbols():
    """Return all default + custom symbols."""
    return load_symbols()


def get_custom_symbols():
    """Return only custom symbols."""
    data = _load_raw()
    if data is None:
        return []
    return data.get("custom", [])
