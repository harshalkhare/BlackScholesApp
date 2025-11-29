from tvDatafeed import TvDatafeed, Interval


def fetch_ltp(symbol: str, exchange: str = 'NSE',
              username: str = None, password: str = None,
              timeout: int = 10, verbose: bool = False) -> float | None:

    try:
        #tv = TvDatafeed(username="vepunapa", password="Brightside@01@")
        tv= TvDatafeed()

        data = tv.get_hist(symbol=symbol, exchange=exchange,
                           interval=Interval.in_1_minute, n_bars=1)

        return float(data['close'].iloc[0]) if not data.empty else None

    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to fetch LTP for {symbol}.{exchange}: {e}")
        return None

"""
    Fetches the Last Traded Price (LTP) for a given symbol using TradingView data.

    Args:
        symbol (str): Ticker symbol (e.g., 'NIFTY', 'TATASTEEL')
        exchange (str): Exchange code (default: 'NSE')
        username (str, optional): TradingView username
        password (str, optional): TradingView password
        timeout (int): Timeout for data fetch (unused but can be extended)
        verbose (bool): Print messages on failure (default: False)

    Returns:
        float | None: Last traded price or None on failure
    """