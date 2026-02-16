"""
Financial Metrics Module
Calculates risk and performance metrics for portfolio analysis.
"""

import pandas as pd
import numpy as np


def calculate_annualized_return(daily_returns, trading_days=252):
    """
    Calculate annualized return from daily returns.
    
    Parameters:
    -----------
    daily_returns : pandas.Series
        Series of daily returns
    trading_days : int
        Number of trading days in a year (default: 252)
    
    Returns:
    --------
    float: Annualized return
    """
    mean_daily_return = daily_returns.mean()
    return mean_daily_return * trading_days


def calculate_annualized_volatility(daily_returns, trading_days=252):
    """
    Calculate annualized volatility from daily returns.
    
    Parameters:
    -----------
    daily_returns : pandas.Series
        Series of daily returns
    trading_days : int
        Number of trading days in a year (default: 252)
    
    Returns:
    --------
    float: Annualized volatility
    """
    daily_std = daily_returns.std()
    return daily_std * np.sqrt(trading_days)


def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.02, trading_days=252):
    """
    Calculate Sharpe Ratio.
    
    Parameters:
    -----------
    daily_returns : pandas.Series
        Series of daily returns
    risk_free_rate : float
        Annual risk-free rate (default: 2%)
    trading_days : int
        Number of trading days in a year (default: 252)
    
    Returns:
    --------
    float: Sharpe Ratio
    """
    ann_return = calculate_annualized_return(daily_returns, trading_days)
    ann_volatility = calculate_annualized_volatility(daily_returns, trading_days)
    
    if ann_volatility == 0:
        return 0
    
    return (ann_return - risk_free_rate) / ann_volatility


def calculate_max_drawdown(prices):
    """
    Calculate maximum drawdown from a price series.
    
    Parameters:
    -----------
    prices : pandas.Series
        Series of prices
    
    Returns:
    --------
    tuple: (max_drawdown, drawdown_series)
        - max_drawdown: Maximum drawdown value
        - drawdown_series: Series of drawdown values over time
    """
    rolling_max = prices.expanding().max()
    drawdown_series = (prices - rolling_max) / rolling_max
    max_drawdown = drawdown_series.min()
    
    return max_drawdown, drawdown_series


def calculate_rolling_volatility(daily_returns, window=30, trading_days=252):
    """
    Calculate rolling volatility.
    
    Parameters:
    -----------
    daily_returns : pandas.Series
        Series of daily returns
    window : int
        Rolling window size in days (default: 30)
    trading_days : int
        Number of trading days in a year (default: 252)
    
    Returns:
    --------
    pandas.Series: Rolling annualized volatility
    """
    return daily_returns.rolling(window=window).std() * np.sqrt(trading_days)


def calculate_ytd_return(prices):
    """
    Calculate year-to-date return.
    
    Parameters:
    -----------
    prices : pandas.Series
        Series of prices with datetime index
    
    Returns:
    --------
    float: YTD return
    """
    current_year = prices.index[-1].year
    ytd_prices = prices[prices.index.year == current_year]
    
    if len(ytd_prices) < 2:
        return 0
    
    start_price = ytd_prices.iloc[0]
    end_price = ytd_prices.iloc[-1]
    
    return (end_price - start_price) / start_price


def get_all_metrics(prices, daily_returns, risk_free_rate=0.02):
    """
    Calculate all key financial metrics.
    
    Parameters:
    -----------
    prices : pandas.Series
        Series of prices
    daily_returns : pandas.Series
        Series of daily returns
    risk_free_rate : float
        Annual risk-free rate
    
    Returns:
    --------
    dict: Dictionary containing all metrics
    """
    ytd_return = calculate_ytd_return(prices)
    ann_return = calculate_annualized_return(daily_returns)
    ann_volatility = calculate_annualized_volatility(daily_returns)
    sharpe_ratio = calculate_sharpe_ratio(daily_returns, risk_free_rate)
    max_dd, _ = calculate_max_drawdown(prices)
    
    return {
        'YTD Return': ytd_return,
        'Annualized Return': ann_return,
        'Annualized Volatility': ann_volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_dd
    }
