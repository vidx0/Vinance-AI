import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
import joblib
import sys
from AI_models.get_stock_data import fetch_stock_data  # Import fetch function

def train_stock_model(stock_symbol):
    """Train a stock prediction model for a given stock symbol."""
    file_path = fetch_stock_data(stock_symbol)
    if file_path is None:
        print(f"Skipping training for {stock_symbol} due to missing data.")
        return
    
    # Load stock data
    df = pd.read_csv(file_path)

    # Add placeholder sentiment score (for future integration)
    df['Sentiment'] = 0.0  

    # Shift 'Close' column to create labels (predicting next day's Close price)
    df['Future_Close'] = df['Close'].shift(-1)

    # Drop the last row since it has no label
    df.dropna(inplace=True)

    # Features (X) and labels (y)
    X = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Sentiment']].values  
    y = df['Future_Close'].values  

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train XGBoost model
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
    model.fit(X_train, y_train)

    # Test the model
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Mean Absolute Error for {stock_symbol}: {mae:.2f}")

    # Save model & scaler
    model_filename = f"AI_models/{stock_symbol}_model.pkl"
    scaler_filename = f"AI_models/{stock_symbol}_scaler.pkl"
    joblib.dump(model, model_filename)
    joblib.dump(scaler, scaler_filename)

    print(f"Training complete. Model saved to {model_filename}")

# Run script with a stock symbol argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python train_stock_model.py <STOCK_SYMBOL>")
    else:
        stock_symbol = sys.argv[1].upper()  # Convert input to uppercase
        train_stock_model(stock_symbol)
