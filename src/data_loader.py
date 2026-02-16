"""
Data Loader Module
Loads FAANG stock data from Kaggle dataset CSV file.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


# Default path to FAANG dataset
DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "faang_stock_prices.csv"


def load_faang_data(ticker=None, csv_path=None, start_date=None, end_date=None):
    """
    Load FAANG stock data from CSV file.
    
    Parameters:
    -----------
    ticker : str, optional
        Stock ticker to filter (AAPLE, AMAZON, GOOGLE, META, MICROSOFT). If None, returns all.
    csv_path : str or Path, optional
        Path to CSV file. Defaults to data/faang_stock_prices.csv
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format
    end_date : str, optional
        End date in 'YYYY-MM-DD' format
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with FAANG stock data including technical indicators
    """
    if csv_path is None:
        csv_path = DEFAULT_DATA_PATH
    
    # Read CSV file
    df = pd.read_csv(csv_path)
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter by ticker if specified
    if ticker is not None:
        df = df[df['Ticker'] == ticker].copy()
    
    # Filter by date range if specified
    if start_date is not None:
        start_date = pd.to_datetime(start_date)
        df = df[df['Date'] >= start_date]
    
    if end_date is not None:
        end_date = pd.to_datetime(end_date)
        df = df[df['Date'] <= end_date]
    
    # Set Date as index
    df = df.set_index('Date').sort_index()
    
    return df


def get_available_tickers(csv_path=None):
    """
    Get list of available stock tickers in the dataset.
    
    Parameters:
    -----------
    csv_path : str or Path, optional
        Path to CSV file
    
    Returns:
    --------
    list
        List of available ticker symbols
    """
    if csv_path is None:
        csv_path = DEFAULT_DATA_PATH
    
    df = pd.read_csv(csv_path)
    return sorted(df['Ticker'].unique().tolist())


def get_date_range(csv_path=None):
    """
    Get the date range available in the dataset.
    
    Parameters:
    -----------
    csv_path : str or Path, optional
        Path to CSV file
    
    Returns:
    --------
    tuple
        (min_date, max_date) as datetime objects
    """
    if csv_path is None:
        csv_path = DEFAULT_DATA_PATH
    
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df['Date'].min(), df['Date'].max()


def prepare_stock_data(df):
    """
    Prepare stock data for analysis (add any missing calculations).
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Raw stock data from CSV
    
    Returns:
    --------
    pandas.DataFrame
        Prepared data with additional calculated fields
    """
    result_df = df.copy()
    
    # Ensure daily returns are calculated (should already be in CSV)
    if 'Daily_Return' not in result_df.columns:
        result_df['Daily_Return'] = result_df['Close'].pct_change()
    
    # Calculate cumulative returns
    result_df['Cumulative_Return'] = (1 + result_df['Daily_Return']).cumprod() - 1
    
    return result_df
