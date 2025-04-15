import yfinance as yf
import os
import pandas as pd

def fetch_stock_data(stock_symbol):
    """Fetch the latest historical stock data using Yahoo Finance and overwrite existing data."""
    file_path = f"data/{stock_symbol}_stock_data.csv"
    
    print(f"Fetching latest stock data for {stock_symbol}...")
    
    try:
        stock = yf.Ticker(stock_symbol)
        df = stock.history(period="2y")  # Fetch last 2 years of data

        if df.empty:
            print(f"Error: No data found for {stock_symbol}.")
            return None

        # Keep only relevant columns
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        df.to_csv(file_path, index=True)
        print(f"Stock data saved to {file_path}")
        
        return file_path
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None
