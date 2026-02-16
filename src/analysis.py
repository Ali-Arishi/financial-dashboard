"""
Analysis Module
Generates text-based insights and analysis from financial data.
"""

import pandas as pd
import numpy as np

def analyze_trend(df):
    """
    Analyze the current trend based on moving averages and price action.
    
    Returns:
        dict: containing 'status', 'summary', 'details'
    """
    if df.empty or len(df) < 30:
        return {"status": "Neutral", "summary": "Insufficient data", "details": []}
        
    latest = df.iloc[-1]
    price = latest['Close']
    
    details = []
    bullish_signals = 0
    bearish_signals = 0
    
    # SMA Analysis
    if 'SMA_21' in df.columns:
        sma21 = latest['SMA_21']
        if price > sma21:
            details.append(f"Price (${price:.2f}) is above the 21-day SMA (${sma21:.2f}), indicating short-term strength.")
            bullish_signals += 1
        else:
            details.append(f"Price (${price:.2f}) is below the 21-day SMA (${sma21:.2f}), indicating short-term weakness.")
            bearish_signals += 1
            
    if 'SMA_50' in df.columns and 'SMA_200' in df.columns:
        sma50 = latest['SMA_50']
        sma200 = latest['SMA_200']
        
        if sma50 > sma200:
             details.append("50-day SMA is above 200-day SMA (Golden Cross alignment).")
             bullish_signals += 1
        else:
             details.append("50-day SMA is below 200-day SMA (Death Cross alignment).")
             bearish_signals += 1

    # Determine overall status
    if bullish_signals > bearish_signals:
        status = "Bullish"
        summary = "Uptrend"
    elif bearish_signals > bullish_signals:
        status = "Bearish"
        summary = "Downtrend"
    else:
        status = "Neutral"
        summary = "Sideways / Mixed"
        
    return {
        "status": status, 
        "summary": summary,
        "details": details
    }

def analyze_volatility(df):
    """
    Analyze volatility context.
    
    Returns:
        dict: containing 'status', 'summary', 'details'
    """
    if 'Volatility_7d' not in df.columns:
        return {"status": "Unknown", "summary": "N/A", "details": []}
        
    current_vol = df['Volatility_7d'].iloc[-1]
    avg_vol = df['Volatility_7d'].mean()
    
    details = [f"Current 7-day volatility is {current_vol:.1%} (Average: {avg_vol:.1%})."]
    
    if current_vol > avg_vol * 1.5:
        status = "High"
        summary = "Elevated Risk"
        details.append("Volatility is significantly higher than average. Expect wider price swings.")
    elif current_vol < avg_vol * 0.7:
        status = "Low"
        summary = "Calm"
        details.append("Volatility is compressed. A breakout (or breakdown) could be imminent.")
    else:
        status = "Normal"
        summary = "Standard"
        details.append("Volatility is within normal historical ranges.")
        
    return {
        "status": status,
        "summary": summary,
        "details": details
    }

def analyze_momentum(df):
    """
    Analyze momentum using RSI and MACD.
    """
    latest = df.iloc[-1]
    details = []
    
    # RSI
    rsi = latest.get('RSI_14', 50)
    if rsi > 70:
        details.append(f"RSI is {rsi:.1f} (Overbought). potential for a pullback.")
    elif rsi < 30:
        details.append(f"RSI is {rsi:.1f} (Oversold). Potential for a bounce.")
    else:
        details.append(f"RSI is {rsi:.1f} (Neutral).")
        
    # MACD
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
        macd = latest['MACD']
        signal = latest['MACD_Signal']
        if macd > signal:
            details.append("MACD is above the signal line (Bullish momentum).")
        else:
            details.append("MACD is below the signal line (Bearish momentum).")
            
    return {
        "details": details
    }

def generate_insight_summary(df, ticker):
    """
    Generate a comprehensive insight summary for the ticker.
    """
    trend = analyze_trend(df)
    vol = analyze_volatility(df)
    mom = analyze_momentum(df)
    
    return {
        "ticker": ticker,
        "trend": trend,
        "volatility": vol,
        "momentum": mom,
        "latest_close": df['Close'].iloc[-1]
    }
