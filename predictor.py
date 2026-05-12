"""Module for ML-based predictions and forecasting."""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta


class NiftyPredictor:
    """Predict NIFTY50 trends and prices using ML."""
    
    def __init__(self, data):
        self.data = data.copy()
        self.scaler = MinMaxScaler()
    
    def simple_trend_prediction(self, days=7):
        """
        Simple trend prediction using moving averages.
        Returns: up/down/neutral trend for next N days
        """
        prices = self.data['Close_Price'].values
        
        # Calculate short and long term moving averages
        sma_short = pd.Series(prices).rolling(window=5).mean()
        sma_long = pd.Series(prices).rolling(window=20).mean()
        
        current_short = sma_short.iloc[-1]
        current_long = sma_long.iloc[-1]
        
        if current_short > current_long:
            trend = "📈 Bullish"
            confidence = min(((current_short - current_long) / current_long) * 100, 95)
        elif current_short < current_long:
            trend = "📉 Bearish"
            confidence = min(((current_long - current_short) / current_long) * 100, 95)
        else:
            trend = "➡️ Neutral"
            confidence = 50
        
        return {
            'trend': trend,
            'confidence': confidence,
            'forecast_days': days
        }
    
    def price_forecast(self, days=30):
        """Forecast future prices using linear regression."""
        prices = self.data['Close_Price'].values
        x = np.arange(len(prices))
        
        # Simple linear regression
        z = np.polyfit(x, prices, 1)
        p = np.poly1d(z)
        
        last_price = prices[-1]
        future_x = np.arange(len(prices), len(prices) + days)
        future_prices = p(future_x)
        
        # Calculate expected change
        expected_change = ((future_prices[-1] - last_price) / last_price) * 100
        
        return {
            'current_price': last_price,
            'forecast_price_30d': future_prices[-1],
            'expected_change_percent': expected_change,
            'forecast_prices': future_prices
        }
    
    def volatility_prediction(self):
        """Predict future volatility based on historical patterns."""
        returns = self.data['Daily_Change_Percent'].dropna()
        
        current_volatility = returns.std()
        recent_volatility = returns.tail(10).std()
        
        if recent_volatility > current_volatility:
            volatility_trend = "⚠️ Increasing"
        elif recent_volatility < current_volatility:
            volatility_trend = "✅ Decreasing"
        else:
            volatility_trend = "➡️ Stable"
        
        return {
            'current_volatility': current_volatility,
            'recent_volatility': recent_volatility,
            'volatility_trend': volatility_trend,
            'risk_level': 'High' if current_volatility > 2.5 else 'Medium' if current_volatility > 1.5 else 'Low'
        }


def get_all_predictions(data):
    """Get all predictions for the data."""
    predictor = NiftyPredictor(data)
    
    return {
        'trend': predictor.simple_trend_prediction(7),
        'price_forecast': predictor.price_forecast(30),
        'volatility': predictor.volatility_prediction()
    }
