# NIFTY50 Dashboard

A comprehensive Streamlit-based dashboard for viewing NIFTY50 daily performance metrics, including daily changes in points and percentage over the past 1 year.

## 🚀 Live Dashboard

**Access the deployed dashboard:** https://lokeshnifty50.streamlit.app

The dashboard is live on Streamlit Community Cloud and updates automatically with the latest market data!

## Features

- 📈 **Daily Price Trend**: Visualize NIFTY50 closing prices over time
- 📊 **Daily Change in Points**: Bar chart showing daily point changes with color coding (green for gains, red for losses)
- 📉 **Daily Change in Percentage**: Bar chart showing daily percentage changes
- 📋 **Detailed Data Table**: View all historical data with formatted metrics
- 📊 **Summary Statistics**: 
  - Average daily change percentage
  - Volatility (standard deviation)
  - Number of positive trading days
  - Maximum daily swing
- 🎯 **Time Period Selection**: View data for 1 month, 3 months, 6 months, or 1 year

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "Coding Practice/stock screener"
   ```

2. **Create a Python virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## Project Structure

```
stock screener/
├── dashboard.py          # Main Streamlit app
├── data_fetcher.py       # Data fetching and processing module
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Data Source

- **NIFTY50 Data**: Fetched from Yahoo Finance using `yfinance` library
- **Symbol Used**: `^NSEI` (NIFTY50 Index)

## Dependencies

- **streamlit**: Web app framework for interactive dashboards
- **yfinance**: Yahoo Finance API for stock data
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **numpy**: Numerical computations

## Features Explanation

### Daily Change (Points)
Shows the absolute change in NIFTY50 index points from the previous trading day.

### Daily Change (%)
Shows the percentage change in NIFTY50 from the previous trading day.

### PE Ratio
*Note: Direct PE ratio data for NIFTY50 index may require additional data sources. This feature can be enhanced to fetch PE ratio from financial data providers.*

## Customization

You can modify the dashboard by:

1. **Changing the time period** in the sidebar
2. **Adding more indicators**: Modify `data_fetcher.py` to include additional calculations
3. **Styling**: Update colors and layouts in `dashboard.py` using Plotly configuration

## Troubleshooting

### No data displayed
- Ensure you have an active internet connection
- Verify that yfinance can access Yahoo Finance
- Try running again after a few seconds

### Dashboard won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.7 or higher: `python --version`

## Future Enhancements

- [ ] Add PE ratio data integration
- [ ] Include moving averages and technical indicators
- [ ] Add email alerts for significant changes
- [ ] Export data to CSV/Excel
- [ ] Add year-over-year comparison
- [ ] Include sector-wise breakdown

## Notes

- Data is cached for better performance
- The dashboard updates with the latest market data automatically
- Trading happens on business days only, so weekends and holidays may have gaps

---

For more information about NIFTY50 or to customize this dashboard further, refer to the [Yahoo Finance API Documentation](https://pypi.org/project/yfinance/) and [Streamlit Documentation](https://docs.streamlit.io/).
