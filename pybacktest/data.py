# coding: utf8

# part of pybacktest package: https://github.com/ematvey/pybacktest

""" Set of data-loading helpers """

import pandas as pd
import pandas_datareader.data as web


def load_from_yahoo(ticker='SPY', start='1900', adjust_close=False):
    """ Loads data from Yahoo. After loading it renames columns to shorter
    format, which is what Backtest expects.

    Set `adjust close` to True to correct all fields with with divident info
    provided by Yahoo via Adj Close field.

    Defaults are in place for convenience. """

    if isinstance(ticker, list):
        return pd.Panel(
            {t: load_from_yahoo(
                ticker=t, start=start, adjust_close=adjust_close)
             for t in ticker})

    data = web.DataReader(ticker, data_source='yahoo', start=start)
    data = data.rename(columns={'Open': 'O', 'High': 'H', 'Low': 'L',
                                'Close': 'C', 'Adj Close': 'AC',
                                'Volume': 'V'})
    if adjust_close:
        adj = data['AC'] - data['C']
        data['O'] += adj
        data['H'] += adj
        data['L'] += adj
        data['C'] += adj
        data = data.drop('AC', axis=1)

    return data