import sys
import os
from contextlib import contextmanager
from sensibull_quotes import SensibullQuotes

@contextmanager
def suppress_stderr():
    devnull = open(os.devnull, 'w')
    old_stderr = sys.stderr
    sys.stderr = devnull
    try:
        yield
    finally:
        sys.stderr = old_stderr
        devnull.close()

def get_atm_iv_by_expiry(symbol: str, expiry_date: str):
    with suppress_stderr():
        quotes = SensibullQuotes()
        single_quote = quotes.get_quotes(symbol.upper())

        if symbol.upper() not in single_quote:
            return None

        instrument_token = single_quote[symbol.upper()]['instrument_token']
        live_data = quotes.get_live_derivative_prices(instrument_token)

    if not live_data or 'expiries' not in live_data:
        return None

    for expiry in live_data['expiries']:
        if expiry.get('expiry') == expiry_date:
            return expiry.get('atm_iv')

    return None

def get_atm_strike_by_expiry(symbol: str, expiry_date: str):
    with suppress_stderr():
        quotes = SensibullQuotes()
        single_quote = quotes.get_quotes(symbol.upper())

        if symbol.upper() not in single_quote:
            return None

        instrument_token = single_quote[symbol.upper()]['instrument_token']
        live_data = quotes.get_live_derivative_prices(instrument_token)

    if not live_data or 'expiries' not in live_data:
        return None

    for expiry in live_data['expiries']:
        if expiry.get('expiry') == expiry_date:
            return expiry.get('atm_strike')

    return None
