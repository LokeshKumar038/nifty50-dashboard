"""Module to fetch NIFTY50 historical data and PE ratio."""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_nifty50_data(period="1y"):
    """
    Fetch NIFTY50 historical data for the specified period.
    
    Args:
        period: Time period (default "1y" for 1 year)
    
    Returns:
        DataFrame with NIFTY50 data
    """
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period=period)
    return data


def fetch_nifty50_pe_ratio(period="1y"):
    """
    Fetch NIFTY50 PE ratio data.
    
    Args:
        period: Time period (default "1y" for 1 year)
    
    Returns:
        DataFrame with PE ratio data
    """
    # Using a different ticker or calculating from available data
    # Note: NIFTY50 PE ratio might need to be fetched from alternative sources
    nifty_info = yf.Ticker("^NSEI")
    return nifty_info.info


def calculate_daily_changes(data):
    """
    Calculate daily changes in points and percentage.
    
    Args:
        data: DataFrame with NIFTY50 OHLC data
    
    Returns:
        DataFrame with added columns for daily change
    """
    data_copy = data.copy()
    data_copy['Daily_Change_Points'] = data_copy['Close'].diff()
    data_copy['Daily_Change_Percent'] = data_copy['Close'].pct_change() * 100
    data_copy['Close_Price'] = data_copy['Close']
    
    return data_copy[['Close_Price', 'Daily_Change_Points', 'Daily_Change_Percent']]


def process_nifty_data(period="1y"):
    """
    Process NIFTY50 data for dashboard display.
    
    Args:
        period: Time period for historical data
    
    Returns:
        Processed DataFrame ready for visualization
    """
    data = fetch_nifty50_data(period)
    processed_data = calculate_daily_changes(data)
    
    # Reset index to have Date as a column
    processed_data = processed_data.reset_index()
    processed_data['Date'] = pd.to_datetime(processed_data['Date']).dt.date
    
    return processed_data
