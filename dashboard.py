"""Streamlit dashboard for NIFTY50 daily performance and PE ratio."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_fetcher import process_nifty_data, fetch_nifty50_data
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="NIFTY50 Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("📈 NIFTY50 Dashboard")
st.markdown("Daily performance metrics and analysis for the past 1 year")

# Sidebar for controls
st.sidebar.header("Dashboard Controls")
time_period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y"],
    index=3
)

# Fetch data
@st.cache_data
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

st.divider()

# Charts
st.subheader("📊 NIFTY50 Daily Price & Changes")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Price Trend", "Daily Change (Points)", "Daily Change (%)"])

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

st.info("✅ Dashboard auto-updates with latest NIFTY50 data. Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
