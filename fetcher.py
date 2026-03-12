import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(symbols, period="1y"):
    data = yf.download(symbols, period=period, progress=False, auto_adjust=True)['Close']
    return data

def calculate_returns(prices):
    return prices.pct_change().dropna()

def get_market_stats(symbols, period="1y"):
    prices  = get_stock_data(symbols, period)
    returns = calculate_returns(prices)

    stats = {}
    for symbol in symbols:
        daily_ret  = returns[symbol]
        ann_return = daily_ret.mean() * 252
        ann_vol    = daily_ret.std() * np.sqrt(252)
        sharpe     = (ann_return - 0.07) / ann_vol

        stats[symbol] = {
            "annual_return" : round(ann_return * 100, 2),
            "annual_vol"    : round(ann_vol * 100, 2),
            "sharpe_ratio"  : round(sharpe, 2),
            "daily_returns" : daily_ret
        }

    return stats, returns
