# FAANG Stock Analysis Dashboard

An interactive technical analysis dashboard for FAANG stocks (Apple, Amazon, Google, Meta, Microsoft) with comprehensive technical indicators.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- FAANG stock dataset (included in `/data` folder)



The dashboard will open automatically in your default browser
https://ehpsntlc4njrffwa5uiijf.streamlit.app/ 

## 📊 Features

### Stock Selection
- **5 FAANG Stocks**: Apple (AAPL), Amazon (AMZN), Google (GOOGL), Meta (META), Microsoft (MSFT)
- **Date Range Filtering**: Customize analysis period
- **Interactive Controls**: Real-time updates

### Key Performance Indicators
- **YTD Return**: Year-to-date performance
- **Annualized Return**: Average annual return
- **Annualized Volatility**: Risk measure
- **Sharpe Ratio**: Risk-adjusted return metric
- **Maximum Drawdown**: Largest peak-to-trough decline

### Technical Indicators

#### Price Analysis
- **Price Chart** with Bollinger Bands
- **Moving Averages**: SMA 7 and SMA 21
- **Support/Resistance Levels**

#### Momentum Indicators
- **RSI (Relative Strength Index)**: Overbought/oversold signals
- **MACD**: Trend direction and momentum
- **Volume Analysis**: Trading activity patterns

#### Risk Analysis
- **Drawdown Chart**: Historical peak-to-trough declines
- **Rolling Volatility**: 7-day volatility tracking
- **Return Distribution**: Statistical analysis of returns

### Performance Metrics
- **Cumulative Returns**: Total return over period
- **Daily Returns Distribution**: Risk assessment
- **Volatility Tracking**: Price stability analysis

## 🛠️ Project Structure

```
financial-dashboard/
├── app.py                          # Main Streamlit dashboard
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   └── faang_stock_prices.csv     # Stock data with indicators
└── src/
    ├── __init__.py
    ├── analysis.py                 # insights
    ├── data_loader.py              # CSV data loading
    ├── metrics.py                  # Financial calculations
    └── visualizations.py           # Plotly charts
```

## 📈 Technical Indicators Explained

### RSI (Relative Strength Index)
- **Range**: 0-100
- **Overbought**: > 70 (potential sell signal)
- **Oversold**: < 30 (potential buy signal)
- **Neutral**: 30-70

### MACD (Moving Average Convergence Divergence)
- **Signal**: MACD line crossover with signal line
- **Bullish**: MACD above signal line
- **Bearish**: MACD below signal line
- **Histogram**: Difference between MACD and signal

### Bollinger Bands
- **Upper Band**: Price + 2 standard deviations
- **Lower Band**: Price - 2 standard deviations
- **Price touching upper band**: Potentially overbought
- **Price touching lower band**: Potentially oversold

## 📝 Data Source
https://www.kaggle.com/datasets/vishardmehta/faang-stock-market-data-with-technical-indicators/data

**Dataset**: FAANG Stock Market Data with Technical Indicators (Kaggle)
- **Period**: 2016-2026
- **Frequency**: Daily
- **Indicators**: Pre-calculated SMA, EMA, RSI, MACD, Bollinger Bands, Volatility

## ⚙️ Configuration

Customize analysis parameters in the sidebar:
- **Stock Selection**: Choose from 5 FAANG stocks
- **Date Range**: Filter by specific time period
- **Risk-Free Rate**: Adjust for Sharpe Ratio calculation (default: 2%)

## 🎯 Use Cases

- **Technical Analysis**: Identify entry/exit points using indicators
- **Risk Assessment**: Evaluate volatility and drawdown risks
- **Performance Tracking**: Monitor stock performance over time  
- **Comparative Analysis**: Compare different FAANG stocks
- **Strategy Backtesting**: Test trading strategies on historical data

## 📦 Dependencies

- streamlit >= 1.28.0
- pandas >= 2.0.0
- plotly >= 5.17.0
- numpy >= 1.24.0

## 💡 Tips for Analysis

1. **Multiple Indicators**: Use RSI, MACD, and Bollinger Bands together for confirmation
2. **Timeframe**: Adjust date range to focus on specific market events
3. **Risk Management**: Monitor drawdowns and volatility for position sizing
4. **Divergence**: Look for RSI/MACD divergence from price for reversal signals

## ⚠️ Disclaimer

- Past performance does not guarantee future results
- Technical indicators are lagging and should be used with other analysis methods
- This is for educational purposes only - not financial advice
- Always do your own research and consult financial advisors

## 🤝 Support

For questions about the dashboard or technical indicators, refer to the "About the Data & Indicators" section in the dashboard.

---

**Last Updated**: February 2026
