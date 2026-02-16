"""
Visualizations Module
Creates interactive charts using Plotly for FAANG stock analysis.
Professional dark-themed charts with enhanced readability.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


# Shared dark theme layout
CHART_THEME = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(17,17,17,0.8)',
    font=dict(family='Inter, sans-serif', color='#e2e8f0'),
    title_font=dict(size=14, color='#cbd5e1'),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.06)',
        zeroline=False,
        title_font=dict(size=12),
        tickformat='%d %b\n%Y',
        tickfont=dict(size=10),
        hoverformat='%d %b %Y',
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.06)',
        zeroline=False,
        title_font=dict(size=12),
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(size=11),
    ),
    margin=dict(l=40, r=20, t=45, b=50),
    hovermode='x unified',
)


def _apply_theme(fig, height=420):
    """Apply shared theme to a figure."""
    fig.update_layout(**CHART_THEME, height=height)
    return fig


def create_price_chart_with_indicators(df):
    """Price chart with candlestick, Bollinger Bands, and moving averages."""

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.03,
    )

    # Bollinger Bands shaded area
    if 'Bollinger_Upper' in df.columns and 'Bollinger_Lower' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Bollinger_Upper'],
            mode='lines', name='Bollinger Upper',
            line=dict(color='rgba(99,102,241,0.25)', width=1),
            showlegend=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Bollinger_Lower'],
            mode='lines', name='Bollinger Lower',
            line=dict(color='rgba(99,102,241,0.25)', width=1),
            fill='tonexty',
            fillcolor='rgba(99,102,241,0.08)',
            showlegend=True,
        ), row=1, col=1)

    # Candlestick chart (if OHLC available)
    if all(c in df.columns for c in ['Open', 'High', 'Low', 'Close']):
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name='Price',
            increasing_line_color='#22c55e',
            decreasing_line_color='#ef4444',
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'],
            mode='lines', name='Close',
            line=dict(color='#818cf8', width=2),
        ), row=1, col=1)

    # Moving averages
    if 'SMA_7' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_7'],
            mode='lines', name='SMA 7',
            line=dict(color='#38bdf8', width=1.2, dash='dot'),
        ), row=1, col=1)
    if 'SMA_21' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_21'],
            mode='lines', name='SMA 21',
            line=dict(color='#fb923c', width=1.2, dash='dot'),
        ), row=1, col=1)

    # Volume sub-chart
    if 'Volume' in df.columns:
        colors = np.where(df['Close'] >= df['Open'], 'rgba(34,197,94,0.5)', 'rgba(239,68,68,0.5)')
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'],
            marker_color=colors, name='Volume',
            showlegend=False,
        ), row=2, col=1)

    theme = {**CHART_THEME}
    theme['legend'] = dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, bgcolor='rgba(0,0,0,0)', font=dict(size=11))
    theme['margin'] = dict(l=40, r=20, t=55, b=50)
    fig.update_layout(
        **theme,
        title='Stock Price with Bollinger Bands & Moving Averages',
        height=560,
        xaxis_rangeslider_visible=False,
    )
    fig.update_xaxes(
        tickformat='%d %b\n%Y',
        tickfont=dict(size=9),
        hoverformat='%d %b %Y',
        row=1, col=1,
    )
    fig.update_xaxes(
        tickformat='%d %b\n%Y',
        tickfont=dict(size=9),
        row=2, col=1,
    )
    fig.update_yaxes(title_text='Price ($)', row=1, col=1)
    fig.update_yaxes(title_text='Vol', row=2, col=1)
    return fig


def create_rsi_chart(df):
    """RSI chart with overbought/oversold zones."""

    fig = go.Figure()

    # Overbought zone
    fig.add_hrect(y0=70, y1=100, fillcolor='rgba(239,68,68,0.08)',
                  line_width=0, annotation_text='Overbought',
                  annotation_position='top left',
                  annotation_font=dict(size=10, color='#ef4444'))
    # Oversold zone
    fig.add_hrect(y0=0, y1=30, fillcolor='rgba(34,197,94,0.08)',
                  line_width=0, annotation_text='Oversold',
                  annotation_position='bottom left',
                  annotation_font=dict(size=10, color='#22c55e'))

    # RSI line
    fig.add_trace(go.Scatter(
        x=df.index, y=df['RSI_14'],
        mode='lines', name='RSI (14)',
        line=dict(color='#a78bfa', width=2),
    ))

    # Reference lines
    fig.add_hline(y=70, line_dash='dash', line_color='rgba(239,68,68,0.5)', line_width=1)
    fig.add_hline(y=30, line_dash='dash', line_color='rgba(34,197,94,0.5)', line_width=1)
    fig.add_hline(y=50, line_dash='dot', line_color='rgba(255,255,255,0.15)', line_width=1)

    fig.update_layout(title='Relative Strength Index (RSI-14)', yaxis=dict(range=[0, 100]))
    return _apply_theme(fig, 350)


def create_macd_chart(df):
    """MACD chart with histogram."""

    fig = go.Figure()

    # Histogram
    macd_hist = df['MACD'] - df['MACD_Signal']
    colors = np.where(macd_hist >= 0, 'rgba(34,197,94,0.45)', 'rgba(239,68,68,0.45)')

    fig.add_trace(go.Bar(
        x=df.index, y=macd_hist,
        name='Histogram', marker_color=colors,
    ))

    # MACD & Signal lines
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MACD'],
        mode='lines', name='MACD',
        line=dict(color='#818cf8', width=2),
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MACD_Signal'],
        mode='lines', name='Signal',
        line=dict(color='#fb923c', width=2),
    ))

    fig.add_hline(y=0, line_color='rgba(255,255,255,0.15)', line_width=1)
    fig.update_layout(title='MACD (Moving Average Convergence Divergence)')
    return _apply_theme(fig, 350)


def create_volume_chart(df):
    """Volume chart with color-coded bars."""

    colors = np.where(df['Close'] >= df['Open'], 'rgba(34,197,94,0.6)', 'rgba(239,68,68,0.6)')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'],
        name='Volume', marker_color=colors,
    ))
    fig.update_layout(title='Trading Volume', showlegend=False)
    return _apply_theme(fig, 320)


def create_drawdown_chart(prices):
    """Drawdown chart showing peak-to-trough declines."""

    rolling_max = prices.expanding().max()
    drawdown_series = (prices - rolling_max) / rolling_max

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=drawdown_series.index,
        y=drawdown_series * 100,
        mode='lines', name='Drawdown',
        fill='tozeroy',
        line=dict(color='#ef4444', width=1.5),
        fillcolor='rgba(239,68,68,0.15)',
    ))
    fig.update_layout(title='Drawdown Analysis')
    fig.update_yaxes(title_text='Drawdown (%)')
    return _apply_theme(fig, 350)


def create_volatility_chart(df):
    """Rolling volatility chart."""

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Volatility_7d'] * 100,
        mode='lines', name='7-Day Volatility',
        line=dict(color='#a78bfa', width=1.8),
        fill='tozeroy',
        fillcolor='rgba(167,139,250,0.1)',
    ))
    fig.update_layout(title='Rolling Volatility (7-Day)')
    fig.update_yaxes(title_text='Volatility (%)')
    return _apply_theme(fig, 350)


def create_return_distribution(daily_returns):
    """Histogram of daily returns."""

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=daily_returns * 100, nbinsx=60,
        name='Daily Returns',
        marker=dict(
            color='rgba(99,102,241,0.6)',
            line=dict(color='rgba(99,102,241,0.9)', width=1),
        ),
    ))
    fig.update_xaxes(title_text='Daily Return (%)')
    fig.update_yaxes(title_text='Frequency')
    fig.update_layout(title='Daily Return Distribution', showlegend=False)
    return _apply_theme(fig, 350)


def create_cumulative_return_chart(df):
    """Cumulative return chart."""

    fig = go.Figure()
    if 'Cumulative_Return' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Cumulative_Return'] * 100,
            mode='lines', name='Cumulative Return',
            line=dict(color='#34d399', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(52,211,153,0.08)',
        ))
    fig.update_layout(title='Cumulative Returns')
    fig.update_yaxes(title_text='Cumulative Return (%)')
    return _apply_theme(fig, 380)


def create_multi_stock_comparison(all_data):
    """Compare normalized price performance of multiple stocks.
    
    Parameters:
        all_data: dict of {ticker: DataFrame}
    """
    colors = {
        'AAPLE': '#818cf8',
        'AMAZON': '#fb923c',
        'GOOGLE': '#34d399',
        'META': '#38bdf8',
        'MICROSOFT': '#f472b6',
        'NVIDIA': '#facc15',
    }

    fig = go.Figure()
    for ticker, df in all_data.items():
        if len(df) == 0:
            continue
        normalized = (df['Close'] / df['Close'].iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=df.index, y=normalized,
            mode='lines', name=ticker,
            line=dict(color=colors.get(ticker, '#94a3b8'), width=2),
        ))

    fig.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.2)', line_width=1)
    fig.update_yaxes(title_text='Normalized Price (Base=100)')
    theme = {**CHART_THEME}
    theme['legend'] = dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, bgcolor='rgba(0,0,0,0)', font=dict(size=11))
    fig.update_layout(**theme, title='Stock Performance Comparison', height=420)
    return fig
