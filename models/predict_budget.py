import pandas as pd
import joblib

# Load the trained model and scaler
model = joblib.load("models/budget_ai_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Load column names from CSV (excluding target)
df = pd.read_csv("financial_data.csv")
feature_columns = df.drop(columns=["price_of_item"]).columns

# Example user input (modify this with real user data)
new_user_data = {
    "income": 400000,
    "rent": 100,
    "utilities": 100,
    "groceries": 200,
    "dining_out": 100,
    "entertainment": 20,
    "subscriptions": 20,
    "transportation": 100,
    "savings": 000,
    "debt": 13000
}

# Convert to DataFrame and scale it
new_user_df = pd.DataFrame([new_user_data])[feature_columns]
new_user_scaled = scaler.transform(new_user_df)

# Make a prediction
prediction = model.predict(new_user_scaled)

# Output the result
if prediction[0] == 1:
    print("Purchase is affordable.")
else:
    print("Purchase is NOT affordable.")
