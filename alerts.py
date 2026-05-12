"""Module for price alerts and notifications."""

import streamlit as st
from datetime import datetime
import pytz


class PriceAlertManager:
    """Manage price and percentage alerts."""
    
    def __init__(self):
        self.alerts = []
    
    def add_price_alert(self, price_threshold, alert_type="above"):
        """
        Add a price threshold alert.
        alert_type: "above" or "below"
        """
        alert = {
            'type': 'price',
            'threshold': price_threshold,
            'alert_type': alert_type,
            'created_at': datetime.now(pytz.timezone('Asia/Kolkata'))
        }
        self.alerts.append(alert)
        return alert
    
    def add_percentage_alert(self, percentage_threshold, alert_type="up"):
        """
        Add a percentage change alert.
        alert_type: "up" or "down"
        """
        alert = {
            'type': 'percentage',
            'threshold': percentage_threshold,
            'alert_type': alert_type,
            'created_at': datetime.now(pytz.timezone('Asia/Kolkata'))
        }
        self.alerts.append(alert)
        return alert
    
    def check_alerts(self, current_price, daily_change_percent):
        """Check if any alerts are triggered."""
        triggered_alerts = []
        
        for alert in self.alerts:
            if alert['type'] == 'price':
                if alert['alert_type'] == 'above' and current_price >= alert['threshold']:
                    triggered_alerts.append(f"🔔 Price Alert: Index crossed above ₹{alert['threshold']:.2f}")
                elif alert['alert_type'] == 'below' and current_price <= alert['threshold']:
                    triggered_alerts.append(f"🔔 Price Alert: Index fell below ₹{alert['threshold']:.2f}")
            
            elif alert['type'] == 'percentage':
                if alert['alert_type'] == 'up' and daily_change_percent >= alert['threshold']:
                    triggered_alerts.append(f"🔔 Percentage Alert: Daily gain of {alert['threshold']:.2f}% achieved")
                elif alert['alert_type'] == 'down' and daily_change_percent <= -alert['threshold']:
                    triggered_alerts.append(f"🔔 Percentage Alert: Daily loss of {alert['threshold']:.2f}% reached")
        
        return triggered_alerts
    
    def display_alert_ui(self):
        """Display alert configuration UI in Streamlit."""
        st.sidebar.subheader("⚡ Set Alerts")
        
        alert_type = st.sidebar.radio("Alert Type", ["Price Alert", "Percentage Alert"], key="alert_type_radio")
        
        if alert_type == "Price Alert":
            price = st.sidebar.number_input("Price Threshold (₹)", min_value=1000.0, step=100.0, key="price_threshold")
            threshold_type = st.sidebar.selectbox("Alert when", ["Price goes above", "Price goes below"], key="price_select")
            
            if st.sidebar.button("Set Price Alert", key="price_alert_btn"):
                alert_type_map = {"Price goes above": "above", "Price goes below": "below"}
                self.add_price_alert(price, alert_type_map[threshold_type])
                st.sidebar.success("✅ Price alert set!")
        
        else:
            percentage = st.sidebar.number_input("Percentage Change (%)", min_value=0.1, max_value=10.0, step=0.1, key="pct_threshold")
            change_type = st.sidebar.selectbox("Alert when", ["Daily gain >= %", "Daily loss <= %"], key="pct_select")
            
            if st.sidebar.button("Set Percentage Alert", key="pct_alert_btn"):
                change_type_map = {"Daily gain >= %": "up", "Daily loss <= %": "down"}
                self.add_percentage_alert(percentage, change_type_map[change_type])
                st.sidebar.success("✅ Percentage alert set!")


def send_notification(message):
    """Display in-app notification."""
    st.warning(message)
