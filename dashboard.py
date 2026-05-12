"""Streamlit dashboard for NIFTY50 daily performance and PE ratio."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_fetcher import process_nifty_data, fetch_nifty50_data
from pe_analyzer import get_pe_metrics
from alerts import PriceAlertManager
from predictor import get_all_predictions
import pandas as pd
from datetime import datetime
import pytz

# Page configuration
st.set_page_config(page_title="NIFTY50 Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("📈 NIFTY50 Dashboard")
st.markdown("Daily performance metrics and analysis for the past 1 year")

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# Add refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

time_period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y"],
    index=3
)

# Fetch data (refresh cache every 1 hour = 3600 seconds)
@st.cache_data(ttl=3600)
def get_nifty_data(period):
    return process_nifty_data(period)

# Load data
data = get_nifty_data(time_period)

# Calculate statistics
current_price = data['Close_Price'].iloc[-1]
previous_price = data['Close_Price'].iloc[-2] if len(data) > 1 else current_price
daily_change_points = current_price - previous_price
daily_change_percent = (daily_change_points / previous_price * 100) if previous_price != 0 else 0

# Display top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Price", f"₹{current_price:,.2f}")

with col2:
    st.metric("Daily Change (Points)", f"{daily_change_points:+,.2f}", 
              delta=f"{daily_change_percent:+.2f}%")

with col3:
    avg_price = data['Close_Price'].mean()
    st.metric("Average Price (Period)", f"₹{avg_price:,.2f}")

with col4:
    period_high = data['Close_Price'].max()
    period_low = data['Close_Price'].min()
    st.metric("52-Week Range", f"₹{period_low:,.0f} - ₹{period_high:,.0f}")

# Initialize and display alerts
alert_manager = PriceAlertManager()
alert_manager.display_alert_ui()

# Check and display triggered alerts
triggered_alerts = alert_manager.check_alerts(current_price, daily_change_percent)
if triggered_alerts:
    st.divider()
    for alert in triggered_alerts:
        st.info(alert)

st.divider()

# Charts
st.subheader("📊 NIFTY50 Daily Price & Changes")

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Price Trend", "Daily Change (Points)", "Daily Change (%)", "PE Ratio Analysis", "Predictions"])

with tab1:
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close_Price'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))
    
    fig_price.update_layout(
        title="NIFTY50 Close Price",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )
    st.plotly_chart(fig_price, use_container_width=True)

with tab2:
    # Daily change in points with color coding
    colors = ['green' if x > 0 else 'red' for x in data['Daily_Change_Points'].fillna(0)]
    
    fig_points = go.Figure()
    fig_points.add_trace(go.Bar(
        x=data['Date'],
        y=data['Daily_Change_Points'],
        name='Daily Change (Points)',
        marker=dict(color=colors, opacity=0.7)
    ))
    
    fig_points.update_layout(
        title="NIFTY50 Daily Change in Points",
        xaxis_title="Date",
        yaxis_title="Change (Points)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        showlegend=False
    )
    st.plotly_chart(fig_points, use_container_width=True)

with tab3:
    # Daily change in percentage with color coding
    colors_pct = ['green' if x > 0 else 'red' for x in data['Daily_Change_Percent'].fillna(0)]
    
    fig_percent = go.Figure()
    fig_percent.add_trace(go.Bar(
        x=data['Date'],
        y=data['Daily_Change_Percent'],
        name='Daily Change (%)',
        marker=dict(color=colors_pct, opacity=0.7)
    ))
    
    fig_percent.update_layout(
        title="NIFTY50 Daily Change in Percentage",
        xaxis_title="Date",
        yaxis_title="Change (%)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        showlegend=False
    )
    st.plotly_chart(fig_percent, use_container_width=True)

with tab4:
    st.subheader("💹 PE Ratio Analysis")
    pe_data, pe_metrics = get_pe_metrics(time_period)
    
    if pe_metrics:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current PE Ratio", f"{pe_metrics['current_pe']:.2f}")
        with col2:
            st.metric("Fair Value PE", f"{pe_metrics['fair_value']:.2f}")
        with col3:
            st.metric("Status", pe_metrics['valuation_status'])
        with col4:
            st.metric("Std Deviation", f"{pe_metrics['historical_std']:.2f}")
        
        # PE Ratio Chart with thresholds
        fig_pe = go.Figure()
        fig_pe.add_trace(go.Scatter(
            x=pe_data['Date'], 
            y=pe_data['PE_Ratio'], 
            name='PE Ratio',
            line=dict(color='#1f77b4', width=2)
        ))
        fig_pe.add_hline(y=pe_metrics['fair_value'], line_dash="dash", line_color="green", annotation_text="Fair Value")
        fig_pe.add_hline(y=pe_metrics['overvalued_threshold'], line_dash="dash", line_color="red", annotation_text="Overvalued")
        fig_pe.add_hline(y=pe_metrics['undervalued_threshold'], line_dash="dash", line_color="blue", annotation_text="Undervalued")
        
        fig_pe.update_layout(
            title="NIFTY50 PE Ratio Trend",
            xaxis_title="Date",
            yaxis_title="PE Ratio",
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )
        st.plotly_chart(fig_pe, use_container_width=True)
        
        # Valuation explanation
        st.info(f"""
        **Valuation Guide:**
        - 🟢 **Undervalued**: PE < {pe_metrics['undervalued_threshold']:.2f} (Good buying opportunity)
        - 🟡 **Fair Value**: {pe_metrics['undervalued_threshold']:.2f} ≤ PE ≤ {pe_metrics['overvalued_threshold']:.2f} (Fairly priced)
        - 🔴 **Overvalued**: PE > {pe_metrics['overvalued_threshold']:.2f} (Potentially expensive)
        """)

with tab5:
    st.subheader("🔮 Predictions & Forecasting")
    predictions = get_all_predictions(data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trend_data = predictions['trend']
        st.metric("7-Day Trend", trend_data['trend'], f"{trend_data['confidence']:.1f}% confidence")
    
    with col2:
        forecast = predictions['price_forecast']
        st.metric("30-Day Price Target", f"₹{forecast['forecast_price_30d']:,.2f}", 
                  f"{forecast['expected_change_percent']:+.2f}%")
    
    with col3:
        vol = predictions['volatility']
        st.metric("Volatility Status", vol['volatility_trend'], f"Risk: {vol['risk_level']}")
    
    st.divider()
    
    # Price forecast chart
    forecast = predictions['price_forecast']
    future_dates = pd.date_range(start=data['Date'].iloc[-1], periods=len(forecast['forecast_prices']) + 1)[1:]
    
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=data['Date'], y=data['Close_Price'], name='Historical Price', line=dict(color='blue')))
    fig_forecast.add_trace(go.Scatter(x=future_dates, y=forecast['forecast_prices'], name='30-Day Forecast', 
                                      line=dict(color='orange', dash='dash')))
    
    fig_forecast.update_layout(
        title="NIFTY50 Price Forecast (30 Days)",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

st.divider()

# Data table
st.subheader("📋 Detailed Data View")

# Format data for display
display_data = data.copy()
display_data['Close_Price'] = display_data['Close_Price'].apply(lambda x: f"₹{x:,.2f}")
display_data['Daily_Change_Points'] = display_data['Daily_Change_Points'].apply(lambda x: f"{x:+,.2f}" if pd.notna(x) else "N/A")
display_data['Daily_Change_Percent'] = display_data['Daily_Change_Percent'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")

# Show latest data first
display_data_sorted = display_data.sort_values('Date', ascending=False)

st.dataframe(
    display_data_sorted,
    use_container_width=True,
    hide_index=True
)

# Summary statistics
st.divider()
st.subheader("📈 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_daily_change = data['Daily_Change_Percent'].mean()
    st.metric("Avg Daily Change %", f"{avg_daily_change:+.2f}%")

with col2:
    volatile = data['Daily_Change_Percent'].std()
    st.metric("Volatility (Std Dev)", f"{volatile:.2f}%")

with col3:
    positive_days = (data['Daily_Change_Percent'] > 0).sum()
    total_days = len(data) - 1  # -1 because first day has NaN
    st.metric("Positive Days", f"{positive_days} / {total_days}")

with col4:
    max_daily_gain = data['Daily_Change_Points'].max()
    max_daily_loss = data['Daily_Change_Points'].min()
    st.metric("Max Daily Swing", f"{max_daily_gain - max_daily_loss:,.0f} pts")

# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
st.info("✅ Dashboard auto-updates with latest NIFTY50 data. Last updated: " + current_time_ist)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px; margin-top: 40px; padding: 20px;'>
    <p>Developed and Designed by <strong>Lokesh Kumar</strong> © 2026</p>
    <p><a href='https://github.com/LokeshKumar038/nifty50-dashboard' style='color: #0066cc; text-decoration: none;'>View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
