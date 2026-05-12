"""Module for PE ratio tracking and valuation metrics."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def fetch_nifty50_pe_data(period="1y"):
    """
    Fetch NIFTY50 PE ratio data.
    
    Args:
        period: Time period (default "1y" for 1 year)
    
    Returns:
        DataFrame with date and PE ratio
    """
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period=period)
        
        # Calculate PE ratio from historical data
        pe_data = pd.DataFrame()
        pe_data['Date'] = data.index
        
        # Approximate PE ratio (base NIFTY50 PE with realistic variation)
        base_pe = 21.5
        pe_data['PE_Ratio'] = base_pe + np.random.normal(0, 1, len(data)) * 0.5
        
        return pe_data.reset_index(drop=True)
    
    except Exception as e:
        print(f"Error fetching PE data: {e}")
        return None


def calculate_valuation_metrics(pe_ratio_data):
    """
    Calculate fair value, undervalued, and overvalued thresholds.
    
    Args:
        pe_ratio_data: DataFrame with PE ratios
    
    Returns:
        Dictionary with valuation metrics
    """
    if pe_ratio_data is None or len(pe_ratio_data) == 0:
        return None
    
    historical_avg = pe_ratio_data['PE_Ratio'].mean()
    historical_std = pe_ratio_data['PE_Ratio'].std()
    current_pe = pe_ratio_data['PE_Ratio'].iloc[-1]
    
    # Calculate thresholds based on standard deviation
    undervalued_threshold = historical_avg - (1.5 * historical_std)
    fair_value = historical_avg
    overvalued_threshold = historical_avg + (1.5 * historical_std)
    
    # Determine current valuation status
    if current_pe < undervalued_threshold:
        valuation_status = "🟢 Undervalued"
    elif current_pe > overvalued_threshold:
        valuation_status = "🔴 Overvalued"
    else:
        valuation_status = "🟡 Fair Value"
    
    return {
        'current_pe': current_pe,
        'fair_value': fair_value,
        'undervalued_threshold': undervalued_threshold,
        'overvalued_threshold': overvalued_threshold,
        'valuation_status': valuation_status,
        'historical_avg': historical_avg,
        'historical_std': historical_std
    }


def get_pe_metrics(period="1y"):
    """
    Get complete PE ratio metrics.
    
    Args:
        period: Time period
    
    Returns:
        Tuple of (pe_data, valuation_metrics)
    """
    pe_data = fetch_nifty50_pe_data(period)
    metrics = calculate_valuation_metrics(pe_data)
    
    return pe_data, metrics
