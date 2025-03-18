import numpy as np
import joblib
import sys
import yfinance as yf

def fetch_latest_stock_data(stock_symbol):
    """Fetch latest stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(stock_symbol)
        df = stock.history(period="1d")

        if df.empty:
            print(f"Error: No latest data found for {stock_symbol}.")
            return None

        # Extract latest stock data
        latest_data = df.iloc[-1]
        return [
            latest_data['Open'],
            latest_data['High'],
            latest_data['Low'],
            latest_data['Close'],
            latest_data['Volume'],
            0.0  # Placeholder sentiment score
        ]
    except Exception as e:
        print(f"Error fetching latest data for {stock_symbol}: {e}")
        return None

def predict_stock(stock_symbol):
    """Load trained model and predict the next day's stock price."""
    model_filename = f"AI_models/{stock_symbol}_model.pkl"
    scaler_filename = f"AI_models/{stock_symbol}_scaler.pkl"

    try:
        # Load model and scaler
        model = joblib.load(model_filename)
        scaler = joblib.load(scaler_filename)

        # Get latest stock data
        latest_data = fetch_latest_stock_data(stock_symbol)
        if latest_data is None:
            print("Skipping prediction due to missing data.")
            return

        # Reshape and scale the input
        model_input = np.array([latest_data]).reshape(1, -1)
        model_input = scaler.transform(model_input)

        # Make prediction
        predicted_price = model.predict(model_input)[0]
        print(f"Predicted next close price for {stock_symbol}: {predicted_price:.2f}")
        return predicted_price

    except Exception as e:
        print(f"Error loading model or making prediction: {e}")

# Run script with a stock symbol argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict_stock.py <STOCK_SYMBOL>")
    else:
        stock_symbol = sys.argv[1].upper()
        predict_stock(stock_symbol)
