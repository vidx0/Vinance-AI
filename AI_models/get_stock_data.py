import yfinance as yf
import os
import pandas as pd

def fetch_stock_data(stock_symbol):
    """Fetch historical stock data using Yahoo Finance and save as CSV."""
    file_path = f"data/{stock_symbol}_stock_data.csv"

    # Check if data already exists
    if os.path.exists(file_path):
        print(f"Using existing data file for {stock_symbol}.")
        return file_path

    print(f"Fetching stock data for {stock_symbol}...")
    
    try:
        stock = yf.Ticker(stock_symbol)
        df = stock.history(period="2y")  # Fetch last 2 years of data

        if df.empty:
            print(f"Error: No data found for {stock_symbol}.")
            return None

        # Keep only relevant columns
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.to_csv(file_path)
        print(f"Stock data saved to {file_path}")

        return file_path
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None
