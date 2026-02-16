"""
FAANG Stock Analysis Dashboard
Interactive dashboard for analyzing FAANG stocks with technical indicators.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import load_faang_data, get_available_tickers, get_date_range, prepare_stock_data
from metrics import get_all_metrics, calculate_max_drawdown
from analysis import generate_insight_summary
from visualizations import (
    create_price_chart_with_indicators,
    create_rsi_chart,
    create_macd_chart,
    create_volume_chart,
    create_drawdown_chart,
    create_volatility_chart,
    create_return_distribution,
    create_cumulative_return_chart,
    create_multi_stock_comparison,
)

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FAANG Stock Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.2rem; padding-bottom: 0; max-width: 1200px; }

/* ── Header ── */
.dash-header {
    text-align: center;
    padding: 1.2rem 0 0.3rem 0;
}
.dash-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(135deg, #818cf8, #c084fc, #f0abfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.dash-header p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 0.3rem 0 0 0;
}

/* ── Section titles ── */
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.15rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.section-desc {
    font-size: 0.82rem;
    color: #64748b;
    margin: 0 0 0.8rem 0;
    line-height: 1.5;
}

/* ── KPI metric cards ── */
[data-testid="stMetricValue"] {
    font-size: 1.5rem;
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stMetricDelta"] {
    font-size: 0.75rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #cbd5e1;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stCheckbox label {
    color: #94a3b8 !important;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.sidebar-brand {
    text-align: center;
    padding: 0.5rem 0 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
}
.sidebar-brand h2 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0;
}
.sidebar-brand p {
    font-size: 0.72rem;
    color: #64748b;
    margin: 0.2rem 0 0 0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    height: 42px;
    padding: 0 20px;
    border-radius: 6px 6px 0 0;
    font-weight: 600;
    font-size: 0.85rem;
}

/* ── Signal cards ── */
.signal-card {
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
}
.signal-card h4 { margin: 0 0 0.5rem 0; font-size: 0.9rem; }
.signal-card p { margin: 0; font-size: 0.82rem; line-height: 1.5; }

.signal-bullish { background: rgba(34,197,94,0.08); border-left: 4px solid #22c55e; }
.signal-bearish { background: rgba(239,68,68,0.08); border-left: 4px solid #ef4444; }
.signal-neutral { background: rgba(99,102,241,0.08); border-left: 4px solid #818cf8; }
.signal-warn    { background: rgba(245,158,11,0.08); border-left: 4px solid #f59e0b; }

/* ── Footer ── */
.footer-text {
    text-align: center;
    color: #475569;
    font-size: 0.75rem;
    padding: 1.5rem 0 1rem 0;
}

/* ── Divider ── */
.soft-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <h1>FAANG Stock Analysis Dashboard</h1>
    <p>Technical Analysis & Risk Assessment — Apple · Amazon · Google · Meta · Microsoft</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div class="sidebar-brand">
    <h2>Dashboard Controls</h2>
    <p>Select stock and time range</p>
</div>
""", unsafe_allow_html=True)

try:
    available_tickers = get_available_tickers()
    min_date, max_date = get_date_range()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

TICKER_LABELS = {
    'AAPLE': 'Apple',
    'AMAZON': 'Amazon',
    'GOOGLE': 'Google',
    'META': 'Meta',
    'MICROSOFT': 'Microsoft',
    'NVIDIA': 'Nvidia',
}

selected_ticker = st.sidebar.selectbox(
    "Stock",
    options=available_tickers,
    format_func=lambda x: TICKER_LABELS.get(x, x),
    index=0,
)

start_date = st.sidebar.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("To", value=max_date, min_value=start_date, max_value=max_date)

risk_free_rate = 0.02

st.sidebar.markdown("---")
show_comparison = st.sidebar.checkbox("Multi-stock comparison", value=False)

st.sidebar.markdown("---")
if st.sidebar.button("Refresh Data", type="primary", use_container_width=True):
    st.cache_data.clear()

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_stock_data(ticker, start, end):
    df = load_faang_data(ticker=ticker, start_date=start.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d'))
    return prepare_stock_data(df)

try:
    stock_df = load_stock_data(selected_ticker, start_date, end_date)
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ── Metrics ──────────────────────────────────────────────────────────────────
try:
    metrics = get_all_metrics(stock_df['Close'], stock_df['Daily_Return'].dropna(), risk_free_rate)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

latest = stock_df.iloc[-1]
prev_close = stock_df.iloc[-2]['Close']
daily_change = ((latest['Close'] - prev_close) / prev_close) * 100
ann_return = metrics['Annualized Return']
ann_vol = metrics['Annualized Volatility']
sharpe = metrics['Sharpe Ratio']
max_dd_value = metrics['Max Drawdown']
stock_name = TICKER_LABELS.get(selected_ticker, selected_ticker)

# ══════════════════════════════════════════════════════════════════════════════
# KPI SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-title"><span class="dot" style="background:#818cf8;"></span> {stock_name} — Overview</div>
<div class="section-desc">{len(stock_df)} trading days · {stock_df.index[0].strftime('%b %Y')} to {stock_df.index[-1].strftime('%b %Y')}</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Price", f"${latest['Close']:.2f}", f"{daily_change:+.2f}%")
c2.metric("Annual Return", f"{ann_return:.1%}")
c3.metric("Volatility", f"{ann_vol:.1%}")
c4.metric("Sharpe Ratio", f"{sharpe:.2f}", "Good" if sharpe > 1 else "Poor", delta_color="normal" if sharpe > 1 else "inverse")
c5.metric("Max Drawdown", f"{max_dd_value:.1%}")
c6.metric("RSI (14)", f"{latest['RSI_14']:.1f}", "Overbought" if latest['RSI_14'] > 70 else ("Oversold" if latest['RSI_14'] < 30 else "Neutral"))

# ══════════════════════════════════════════════════════════════════════════════
# MULTI-STOCK COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
if show_comparison:
    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-title"><span class="dot" style="background:#38bdf8;"></span> Stock Comparison</div>
    <div class="section-desc">Normalized to 100 at the start of the period. Compare relative performance across all FAANG stocks.</div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_all_stocks(start, end):
        data = {}
        for t in available_tickers:
            try:
                data[t] = prepare_stock_data(
                    load_faang_data(ticker=t, start_date=start.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d'))
                )
            except Exception:
                pass
        return data

    all_data = load_all_stocks(start_date, end_date)
    st.plotly_chart(create_multi_stock_comparison(all_data), width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PRICE & VOLUME
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title"><span class="dot" style="background:#22c55e;"></span> Price & Volume</div>
<div class="section-desc">Candlestick chart with Bollinger Bands and moving averages. Volume subplot shows buying/selling pressure.</div>
""", unsafe_allow_html=True)
st.plotly_chart(create_price_chart_with_indicators(stock_df), width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# TECHNICAL INDICATORS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title"><span class="dot" style="background:#a78bfa;"></span> Technical Indicators</div>
<div class="section-desc">RSI: overbought >70, oversold <30. MACD: crossovers show trend changes. Volume: confirms price moves.</div>
""", unsafe_allow_html=True)

tab_rsi, tab_macd, tab_vol = st.tabs(["RSI", "MACD", "Volume"])
with tab_rsi:
    st.plotly_chart(create_rsi_chart(stock_df), width="stretch")
with tab_macd:
    st.plotly_chart(create_macd_chart(stock_df), width="stretch")
with tab_vol:
    st.plotly_chart(create_volume_chart(stock_df), width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# RISK & PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title"><span class="dot" style="background:#ef4444;"></span> Risk & Performance</div>
<div class="section-desc">Drawdown shows peak-to-trough declines. Volatility tracks rolling risk. Cumulative return shows total growth.</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(create_drawdown_chart(stock_df['Close']), width="stretch")
with col_b:
    st.plotly_chart(create_volatility_chart(stock_df), width="stretch")

col_c, col_d = st.columns(2)
with col_c:
    st.plotly_chart(create_cumulative_return_chart(stock_df), width="stretch")
with col_d:
    st.plotly_chart(create_return_distribution(stock_df['Daily_Return'].dropna()), width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# MARKET SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title"><span class="dot" style="background:#f59e0b;"></span> Market Signals</div>
<div class="section-desc">Quick-read summaries of current technical conditions for the selected stock.</div>
""", unsafe_allow_html=True)

latest_rsi = latest['RSI_14']
latest_macd = latest['MACD']
latest_signal = latest['MACD_Signal']

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    if latest_rsi > 70:
        css_class, title, detail = "signal-bearish", f"RSI Overbought ({latest_rsi:.1f})", "Stock may be overvalued. Watch for pullback."
    elif latest_rsi < 30:
        css_class, title, detail = "signal-bullish", f"RSI Oversold ({latest_rsi:.1f})", "Stock may be undervalued. Potential entry."
    else:
        css_class, title, detail = "signal-neutral", f"RSI Neutral ({latest_rsi:.1f})", "No extreme momentum detected."
    st.markdown(f'<div class="signal-card {css_class}"><h4>{title}</h4><p>{detail}</p></div>', unsafe_allow_html=True)

with col_s2:
    if latest_macd > latest_signal:
        css_class, title, detail = "signal-bullish", "MACD Bullish", "MACD above signal line — upward momentum."
    else:
        css_class, title, detail = "signal-bearish", "MACD Bearish", "MACD below signal line — downward momentum."
    st.markdown(f'<div class="signal-card {css_class}"><h4>{title}</h4><p>{detail}</p></div>', unsafe_allow_html=True)

with col_s3:
    if sharpe > 1.0:
        css_class, title = "signal-bullish", f"Sharpe Ratio: {sharpe:.2f} (Good)"
    elif sharpe > 0.5:
        css_class, title = "signal-warn", f"Sharpe Ratio: {sharpe:.2f} (Moderate)"
    else:
        css_class, title = "signal-bearish", f"Sharpe Ratio: {sharpe:.2f} (Poor)"
    detail = f"Volatility: {ann_vol:.0%} · Max Drawdown: {max_dd_value:.1%}"
    st.markdown(f'<div class="signal-card {css_class}"><h4>{title}</h4><p>{detail}</p></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DEEP INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title"><span class="dot" style="background:#6366f1;"></span> Deep Insights</div>
<div class="section-desc">AI-driven analysis of trend, volatility, and momentum context.</div>
""", unsafe_allow_html=True)

try:
    insights = generate_insight_summary(stock_df, selected_ticker)
    
    with st.container():
        ic1, ic2 = st.columns(2)
        
        with ic1:
            st.markdown(f"**Trend Analysis: {insights['trend']['summary']}**")
            for detail in insights['trend']['details']:
                st.markdown(f"- {detail}")
                
        with ic2:
            st.markdown(f"**Volatility Profile: {insights['volatility']['summary']}**")
            for detail in insights['volatility']['details']:
                st.markdown(f"- {detail}")
        
        st.markdown("**Momentum & Technicals**")
        for detail in insights['momentum']['details']:
            st.markdown(f"- {detail}")
            
except Exception as e:
    st.error(f"Could not generate insights: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# DATA & INFO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

with st.expander("View Raw Data"):
    display_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'RSI_14', 'MACD', 'MACD_Signal']
    available_cols = [c for c in display_cols if c in stock_df.columns]
    st.dataframe(stock_df[available_cols].tail(30).sort_index(ascending=False), width="stretch")

with st.expander("About the Data"):
    st.markdown("""
**Source:** FAANG Stock Market Data (Kaggle) · 2016–2023

| Indicator | Description |
|-----------|-------------|
| SMA 7 / 21 | Short & medium-term trend |
| Bollinger Bands | Volatility channel (2 std dev) |
| RSI (14) | Momentum oscillator (0–100) |
| MACD | Trend-following momentum |
| Sharpe Ratio | Risk-adjusted return |
| Max Drawdown | Largest peak-to-trough loss |
    """)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="footer-text">FAANG Stock Analysis Dashboard · '
    f'Data: Kaggle FAANG Dataset · '
    f'{datetime.now().strftime("%Y-%m-%d %H:%M")}</div>',
    unsafe_allow_html=True,
)
